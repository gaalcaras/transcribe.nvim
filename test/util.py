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


class TestGetTimecode(unittest.TestCase):

    def test_get_timecodes_match(self):
        str_1 = '[00:23:53] test [78:32:98] string [00:23]'
        str_2 = '[00:23:83] test string'

        self.assertEqual(util.get_timecodes(str_1),
                         [{
                             'timecode': '[00:23:53]',
                             'start_index': 0,
                             'end_index': 10
                         },
                         {
                             'timecode': '[00:23]',
                             'start_index': 34,
                             'end_index': 41
                         }])
        self.assertIsNone(util.get_timecodes(str_2))
