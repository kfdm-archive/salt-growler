# Import Python libs
import pprint
import logging
import socket
from fnmatch import fnmatch
logging.basicConfig(level=logging.INFO)

# Import Salt libs
import salt.utils.event

import gntp.config


logger = logging.getLogger(__name__)

__opts__ = {
    'node': 'master',
    'sock_dir': '/var/run/salt/master',
}

GROWL_SETTINGS = {
    'applicationName': 'Salt',
    'notifications': ['Auth', 'Start', 'Job', 'Results', 'Other'],
}

TEMPLATE_RETURN = '''
Function: {fun}
Arguments: {fun_args}
ID: {id}
JID: {jid}
Return: {return}
'''.strip()

SENT_BY = socket.getfqdn()


class SaltGrowler(gntp.config.GrowlNotifier):
    def add_origin_info(self, packet):
        packet.add_header('Sent-By', SENT_BY)


def main():
    event = salt.utils.event.SaltEvent(
        __opts__['node'],
        __opts__['sock_dir']
    )
    logger.info('Listening on %s', event.puburi)

    growl = SaltGrowler(**GROWL_SETTINGS)
    growl.register()

    while True:
        ret = event.get_event(full=True)
        if ret is None:
            continue
        if ret['tag'] == 'salt/auth':
            continue

        logger.info('Tag: %s', ret['tag'])
        logger.debug('Event: %s', ret)
        try:
            kwargs = {
                'identifier': ret['tag'],
            }
            kwargs['sticky'] = True
            if ret['tag'] == 'salt/auth':
                growl.notify(
                    'Auth',
                    ret['tag'],
                    pprint.pformat(ret['data']),
                    **kwargs
                )

            # Specific matches
            elif fnmatch(ret['tag'], 'salt/minion/*/start'):
                growl.notify(
                    'Start',
                    ret['tag'],
                    ret['data'],
                    **kwargs
                )
            elif fnmatch(ret['tag'], 'salt/job/*/new'):
                growl.notify(
                    'Job',
                    ret['tag'],
                    pprint.pformat(ret['data']),
                    **kwargs
                )
            elif fnmatch(ret['tag'], 'salt/job/*/ret/*'):
                kwargs['sticky'] = True
                growl.notify(
                    'Results',
                    ret['tag'],
                    TEMPLATE_RETURN.format(**ret['data']),
                    **kwargs
                )
            else:
                logger.info('Unhandled tag: %s', ret['tag'])
                logger.debug(pprint.pformat(ret))
        except KeyError:
            logger.exception(pprint.pformat(ret))


if __name__ == '__main__':
    main()
