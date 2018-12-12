import os
import socket

from statsd import StatsClient as BaseStatsClient


class StatsClient(BaseStatsClient):

    def __init__(self, host='localhost', port=8125, prefix=None,
                 maxudpsize=512, ipv6=False):
        hostname = self._get_hostname()
        if not prefix:
            prefix = hostname
        else:
            prefix = '{}.{}'.format(hostname, prefix)
        super().__init__(host, port, prefix, maxudpsize, ipv6)

    def _get_hostname(self):
        hostname = None
        if os.path.exists('/etc/hostname'):
            with open('/etc/hostname', 'r') as f:
                hostname = f.read().strip()
        elif 'HOSTNAME' in os.environ:
            hostname = os.environ['HOSTNAME']
        else:
            hostname = socket.gethostname()
        return hostname
