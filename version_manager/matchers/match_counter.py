from .pattern import TrackedVersion, Pattern


class MatchCounter(Pattern):
    def __init__(
        self,
        tracked_version: TrackedVersion,
        delegate_pattern: Pattern,
        expected_count: int,
    ) -> None:
        self.tracked_version = tracked_version
        self.delegate_pattern = delegate_pattern
        self._expected_count = expected_count

    def apply_pattern(self, input: str) -> str:
        return self.delegate_pattern.apply_pattern(input)

    @property
    def match_count(self) -> int:
        if self._expected_count < 0:
            return self._expected_count

        return self.delegate_pattern.match_count

    @property
    def expected_count(self) -> int:
        return self._expected_count
