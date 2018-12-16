from werkzeug.local import LocalProxy

from .statsd import StatsClient


class ObjectWrapper(object):

    def __init__(self, target=None):
        self.target = target

    def set_target(self, target):
        self.target = target

    def __call__(self):
        return LocalProxy(lambda: self.target)


statsd_wrapper = ObjectWrapper()
statsd_wrapper.set_target(StatsClient(host='statsd', port=8126))
statsd = statsd_wrapper()
