import unittest

from adhesive.graph.time.ParsedCycleDefinition import ParsedCycleDefinition


class TestParsedDurationDefinition(unittest.TestCase):
    def test_parsing_every_10_seconds(self):
        cycle = ParsedCycleDefinition.from_str("R/PT10S")

        self.assertEqual(0, cycle.year)
        self.assertEqual(0, cycle.month)
        self.assertEqual(0, cycle.day)
        self.assertEqual(0, cycle.hour)
        self.assertEqual(0, cycle.minute)
        self.assertEqual(10, cycle.second)
        self.assertEqual(-1, cycle.repeat_count)

    def test_parsing_every_month_max_twice(self):
        cycle = ParsedCycleDefinition.from_str("R2/PT1M")

        self.assertEqual(0, cycle.year)
        self.assertEqual(0, cycle.month)
        self.assertEqual(0, cycle.day)
        self.assertEqual(0, cycle.hour)
        self.assertEqual(1, cycle.minute)
        self.assertEqual(0, cycle.second)
        self.assertEqual(2, cycle.repeat_count)
