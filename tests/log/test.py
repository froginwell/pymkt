import json
import unittest

from pymkt import log

from tests.utils.utils import captured_output


class LogTestCase(unittest.TestCase):

    def test_json_output(self):
        with captured_output() as (out, err):
            logger = log.get_logger('test')
            logger.info('hello')

        output = json.loads(out.getvalue().strip())
        self.assertEqual(output['name'], 'root.test')
        self.assertEqual(output['levelname'], 'INFO')
        self.assertEqual(output['message'], 'hello')
