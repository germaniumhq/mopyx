import unittest
from textwrap import dedent

from version_manager.matchers.regex_pattern import RegExPattern
from version_manager.matchers.pattern import TrackedVersion


class TestRegExPattern(unittest.TestCase):
    def test_double_replace(self):
        tracked_version = TrackedVersion("test_version")
        tracked_version.version = "zz"

        r = RegExPattern(tracked_version, "(aa)(bb)")
        result = r.apply_pattern("aabb")

        self.assertEqual("aazz", result)
        self.assertEqual(1, r.match_count)
        self.assertEqual(1, r.expected_count)

    def test_triple_replace_multiple_matches(self):
        """
        Just a normal replace on the version that uses all
        the three groups.
        """
        tracked_version = TrackedVersion("test_version")
        tracked_version.version = "zz"
        tracked_version.expected_count = 2

        r = RegExPattern(tracked_version, "^(.*?)(bb)(.*?)$")

        result = r.apply_pattern(
            dedent(
                """
            aa bb cc
            this is a line
            what bb is this
        """
            )
        )

        self.assertEqual(
            dedent(
                """
            aa zz cc
            this is a line
            what zz is this
        """
            ),
            result,
        )
        self.assertEqual(2, r.match_count)
        self.assertEqual(1, r.expected_count)


if __name__ == "__main__":
    unittest.main()
