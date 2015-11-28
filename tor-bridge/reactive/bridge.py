import os
import random
import shutil
import string
from subprocess import check_call

from charmhelpers.core import hookenv, host
from charmhelpers.core.templating import render
from charmhelpers.fetch import apt_update, apt_install, add_source
from charms.reactive import hook, when, when_not, is_state, set_state, remove_state


@hook('config-changed')
def config():
    cfg = hookenv.config()
    if cfg.changed('port') and cfg.previous('port'):
        hookenv.close_port(cfg.previous('port'))
    hookenv.open_port(cfg['port'])
    set_state('tor.configured')


@when('tor.configured')
def update_torrc():
    remove_state('tor.configured')
    cfg = hookenv.config()
    render(source='torrc',
        target='/etc/tor/torrc',
        owner='root',
        perms=0o644,
        context={
            'cfg': cfg,
            'public_address': hookenv.unit_public_ip(),
            'private_address': hookenv.unit_private_ip(),
        })
    set_state('tor.start')
