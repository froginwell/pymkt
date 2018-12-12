from werkzeug.local import LocalProxy

from .statsd.stats_client import StatsClient


class ObjectWrapper(object):

    def __init__(self, target=None):
        self.target = target

    def set_target(self, target):
        self.target = target

    def __call__(self):
        return LocalProxy(lambda: self.target)


statsd_wrapper = ObjectWrapper()
statsd = statsd_wrapper()
