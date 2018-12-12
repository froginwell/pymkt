import unittest

from pymkt import statsd
from pymkt.globals import statsd_wrapper
from pymkt.statsd import StatsClient


class StatsdTestCase(unittest.TestCase):

    def setUp(self):
        statsd_wrapper.set_target(StatsClient())

    def test_statsd(self):
        self.assertIsNone(statsd.incr('a.b'))
