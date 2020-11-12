import unittest

from version_manager.matchers.maven_pattern import MavenPattern
from version_manager.matchers.pattern import TrackedVersion


class TestMavenPattern(unittest.TestCase):
    def test_maven_pattern(self):
        maven_code = """
            <dependency>
                <groupId>com.ciplogic</groupId>
                <artifactId>test</artifactId>
                <version>1.0.0-SNAPSHOT</version>
            </dependency>
            <dependency>
                <groupId>com.ciplogic</groupId>
                <artifactId>test2</artifactId>
                <version>1.0.0-SNAPSHOT</version>
            </dependency>
        """

        tracked_version = TrackedVersion("test_version")
        tracked_version.version = "2.0"

        m = MavenPattern(tracked_version, "maven:com.ciplogic:test")
        result = m.apply_pattern(maven_code)

        expected_code = """
            <dependency>
                <groupId>com.ciplogic</groupId>
                <artifactId>test</artifactId>
                <version>2.0</version>
            </dependency>
            <dependency>
                <groupId>com.ciplogic</groupId>
                <artifactId>test2</artifactId>
                <version>1.0.0-SNAPSHOT</version>
            </dependency>
        """

        self.assertEqual(expected_code, result)
        self.assertEqual(1, m.expected_count)
        self.assertEqual(1, m.match_count)


if __name__ == "__main__":
    unittest.main()
