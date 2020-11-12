import unittest

from adhesive.graph.time.ParsedDurationDefinition import ParsedDurationDefinition


class TestParsedDurationDefinition(unittest.TestCase):
    def test_parsing(self):
        duration = ParsedDurationDefinition.from_str("P1Y2M3DT4H5M6S")

        self.assertEqual(1, duration.year)
        self.assertEqual(2, duration.month)
        self.assertEqual(3, duration.day)
        self.assertEqual(4, duration.hour)
        self.assertEqual(5, duration.minute)
        self.assertEqual(6, duration.second)

    def test_parsing_only_month(self):
        duration = ParsedDurationDefinition.from_str("P1M")

        self.assertEqual(0, duration.year)
        self.assertEqual(1, duration.month)
        self.assertEqual(0, duration.day)
        self.assertEqual(0, duration.hour)
        self.assertEqual(0, duration.minute)
        self.assertEqual(0, duration.second)

    def test_parsing_only_minute(self):
        duration = ParsedDurationDefinition.from_str("PT1M")

        self.assertEqual(0, duration.year)
        self.assertEqual(0, duration.month)
        self.assertEqual(0, duration.day)
        self.assertEqual(0, duration.hour)
        self.assertEqual(1, duration.minute)
        self.assertEqual(0, duration.second)
