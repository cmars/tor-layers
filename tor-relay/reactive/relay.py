import os
import random
import shutil
import string
from subprocess import check_call

from charmhelpers.core import hookenv, host
from charmhelpers.core.templating import render
from charmhelpers.fetch import apt_update, apt_install, add_source
from charms.reactive import hook, when, when_not, is_state, set_state, remove_state


@hook('install')
def install():
    add_source('deb http://deb.torproject.org/torproject.org trusty main',
        key='A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89')
    apt_update()
    apt_install(['deb.torproject.org-keyring'])
    apt_install(['tor'])


@hook('config-changed')
def config():
    cfg = hookenv.config()
    if cfg.changed('relay_port') and cfg.previous('relay_port'):
        hookenv.close_port(cfg.previous('relay_port'))
    hookenv.open_port(cfg['relay_port'])
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
            'services': {},
            'public_address': hookenv.unit_public_ip(),
            'private_address': hookenv.unit_private_ip(),
            'relay_nickname': relay_nickname(),
        })
    set_state('tor.start')


def relay_nickname():
    cfg = hookenv.config()
    nick = cfg.get('relay_nickname')
    if nick:
        return nick
    return generated_nickname()


def generated_nickname():
    nickfile = os.path.join(hookenv.charm_dir(), 'relay_nickname')
    if os.path.exists(nickfile):
        with open(nickfile, 'r') as fh:
            return fh.read()
    nick = 'juju' + ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(12)])
    with open(nickfile, 'w') as fh:
        fh.write(nick)
    return nick
