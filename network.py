import logging
from sh import sudo
from sh import ErrorReturnCode


def restart(interface='wlan0'):
    """ Utility function to restart the network interface. """
    logging.error('Internet connection problem')
    logging.info('Bringing wlan0 up')
    try:
        sudo('ifup', '--force', 'wlan0')
        logging.info('Restart succeeded')
    except ErrorReturnCode:
        logging.error('Restart failed')
