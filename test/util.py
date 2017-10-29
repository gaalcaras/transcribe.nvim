import unittest
import rplugin.python3.transcribe.util as util


class TestFormatSeconds(unittest.TestCase):

    def test_fmtseconds_standard_format(self):
        self.assertEqual(util.fmtseconds(10.1987987), '00:00:10')
        self.assertEqual(util.fmtseconds(3600), '01:00:00')

    def test_fmtseconds_custom_format(self):
        self.assertEqual(util.fmtseconds(78.9897, '[{H}:{M}:{S}]'),
                         '[00:01:19]')


class TestTimeToSeconds(unittest.TestCase):

    def test_timetosec_standard_format(self):
        self.assertEqual(util.time_to_seconds('10:45:01'), 38701)
        self.assertEqual(util.time_to_seconds('00:05:41'), 341)
        self.assertEqual(util.time_to_seconds('05:41'), 341)

    def test_timetosec_custom_format(self):
        self.assertEqual(util.time_to_seconds('05:41', '%M:%S'), 341)
        self.assertEqual(util.time_to_seconds('01:26', '%H:%S'), 3626)
