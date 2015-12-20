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
    hookenv.status_set('maintenance', 'installing tor packages')

    # Installation is based on Tor installation instructions for Debian/Ubuntu:
    # https://www.torproject.org/docs/debian.html.en#ubuntu

    # Remove universe/multiverse from sources, to avoid the out-of-date tor
    # package.
    check_call(['sed', '-i.torinstall', '/universe/d;/multiverse/d;', '/etc/apt/sources.list'])
    check_call(['apt-get', 'clean'])

    add_source('deb http://deb.torproject.org/torproject.org trusty main',
        key='A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89')
    apt_update()

    # This may fail if torproject.org is blocked. OpenDNS censors it, for example.
    check_call(['apt-get', '-y', 'install', 'deb.torproject.org-keyring', 'tor'])

    hookenv.status_set('maintenance', 'tor installation complete')


@when('tor.start')
def restart_tor():
    remove_state('tor.start')
    if host.service_running('tor'):
        host.service_restart('tor')
    else:
        host.service_start('tor')
    set_state('tor.started')
    hookenv.status_set('active', 'tor service ready')


@when('tor.stop')
def stop_tor():
    remove_state('tor.stop')
    if host.service_running('tor'):
        host.service_stop('tor')
    hookenv.status_set('maintenance', 'tor service stopped')
