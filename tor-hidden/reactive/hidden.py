import glob
import os
from subprocess import check_call
from charmhelpers.core import hookenv
from charmhelpers.core.templating import render
from charms.reactive import when, set_state, remove_state


@when('reverseproxy.available')
def config_with_reverseproxy(reverseproxy):
    services = reverseproxy.services()
    cfg = hookenv.config()

    for service in services:
        service_dir = '/var/lib/tor/{}'.format(service['service_name'])
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
           }
           )
    remove_state('reverseproxy.available')
    set_state('tor.start')


@when('tor.started')
def update_status_hostnames():
    hostname_files = glob.glob('/var/lib/tor/*/hostname')
    status = ''
    for hostname_file in hostname_files:
        with open(hostname_file, 'r') as f:
            servicename = hostname_file.split('/')[4]
            hostname = f.read().strip()
            status = status + 'service {} running on {}, '.format(servicename, hostname)

    if status.endswith(', '):
        status = status[:-2]

    if status != '':
        hookenv.status_set('active', 'tor service ready: {}'.format(status.strip()))
