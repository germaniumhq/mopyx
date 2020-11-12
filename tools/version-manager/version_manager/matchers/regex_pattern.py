import re

from .pattern import Pattern, TrackedVersion


class RegExPattern(Pattern):
    def __init__(
        self,
        tracked_version: TrackedVersion,
        expression: str,
        extra_flags: int = re.M | re.S,
    ) -> None:
        try:
            self.RE = re.compile(expression, extra_flags)
        except Exception as e:
            raise Exception("Unable to compile regex expression: %s" % expression, e)
        self.tracked_version = tracked_version
        self._match_count = 0

    def apply_pattern(self, text: str) -> str:
        """
        Apply the regex pattern on the text, replacing the 2nd
        group from every match.
        """
        found_matches = []
        last_index = -1

        m = self.RE.search(text, pos=last_index)
        while m:
            self._match_count += 1
            last_index = m.start() + len(m.group(0))

            found_matches.append(m)

            m = self.RE.search(text, pos=last_index)

        original_index: int = 0
        original_text: str = text

        result: str = ""

        for match in found_matches:
            result += (
                original_text[original_index : match.start()]
                + match.group(1)
                + self.tracked_version.version
                + (match.group(3) if len(match.groups()) >= 3 else "")
            )

            original_index = match.start() + len(match.group(0))

        result += original_text[original_index : len(original_text)]

        return result

    @property
    def match_count(self) -> int:
        return self._match_count

    @property
    def expected_count(self) -> int:
        return 1
