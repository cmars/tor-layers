import os
import random
import shutil
import string
from subprocess import check_call

from charmhelpers.core import hookenv, host
from charmhelpers.core.templating import render
from charmhelpers.fetch import apt_update, apt_install, add_source
from charms.reactive import hook, when, when_not, is_state, set_state, remove_state


@when('reverseproxy.available')
def config_with_reverseproxy(reverseproxy):
    services = reverseproxy.services()
    cfg = hookenv.config()

    for service in services:
        service_dir = '/var/lib/tor/%s' % (service['service_name'])
        if not os.path.isdir(service_dir):
            check_call(['install', '-d', service_dir, '-o', 'debian-tor', '-m', '700'])

    bridges = []
    for bridge in cfg.get('bridges', '').split(','):
        fields = bridge.split()
        if len(fields) > 1:
            addr, fp = fields[:2]
            bridges.append({'addr': addr, 'fingerprint': fp})

    render(source='torrc',
        target='/etc/tor/torrc',
        owner='root',
        perms=0o644,
        context={
            'cfg': cfg,
            'services': services,
            'bridges': bridges,
            'public_address': hookenv.unit_public_ip(),
            'private_address': hookenv.unit_private_ip(),
        })
    remove_state('reverseproxy.available')
    set_state('tor.start')
