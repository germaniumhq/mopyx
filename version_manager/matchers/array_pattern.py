from typing import List

from .pattern import Pattern, TrackedVersion


class ArrayPattern(Pattern):
    def __init__(
        self, tracked_version: TrackedVersion, delegate_patterns: List[Pattern]
    ) -> None:
        self.tracked_version = tracked_version
        self.delegate_patterns = delegate_patterns

    def apply_pattern(self, input: str) -> str:
        for pattern in self.delegate_patterns:
            input = pattern.apply_pattern(input)

        return input

    @property
    def match_count(self) -> int:
        return sum(map(lambda it: it.match_count, self.delegate_patterns))

    @property
    def expected_count(self) -> int:
        return sum(map(lambda it: it.expected_count, self.delegate_patterns))
