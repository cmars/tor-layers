import charms.apt
from subprocess import check_call, check_output

from charmhelpers.core import hookenv, host
from charms.reactive import hook, when, set_state, remove_state


def get_series():
    return check_output(['lsb_release', '-sc'], universal_newlines=True).strip()


@hook('install')
def install():
    hookenv.status_set('maintenance', 'installing tor packages')

    # Installation is based on Tor installation instructions for Debian/Ubuntu:
    # https://www.torproject.org/docs/debian.html.en#ubuntu

    # Remove universe/multiverse from sources, to avoid the out-of-date tor
    # package.
    check_call(['sed', '-i.torinstall', '/universe/d;/multiverse/d;', '/etc/apt/sources.list'])
    charms.apt.add_source('deb http://deb.torproject.org/torproject.org {} main'.format(get_series()),
                          key='A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89')

    charms.apt.queue_install(['deb.torproject.org-keyring', 'tor'])


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
