import unittest

from adhesive.graph.time.ParsedDateDefinition import ParsedDateDefinition


class TestParsedDateDefinition(unittest.TestCase):
    def test_date_parsing(self):
        date_definition = ParsedDateDefinition.from_str("2019-11-04T04:33:32")

        self.assertEqual(2019, date_definition.date.year)
        self.assertEqual(11, date_definition.date.month)
        self.assertEqual(4, date_definition.date.day)
        self.assertEqual(4, date_definition.date.hour)
        self.assertEqual(33, date_definition.date.minute)
        self.assertEqual(32, date_definition.date.second)

    @unittest.expectedFailure
    def parsing_garbage_should_raise_an_exception(self):
        ParsedDateDefinition.from_str("garbage")
