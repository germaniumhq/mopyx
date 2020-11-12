from adhesive.graph.time import TIME_PERIOD_RE, REPEATING_RE


class ParsedCycleDefinition:
    def __init__(self) -> None:
        self.year = 0
        self.month = 0
        self.day = 0
        self.hour = 0
        self.minute = 0
        self.second = 0
        self.repeat_count = -1

    @staticmethod
    def from_str(segments: str) -> 'ParsedCycleDefinition':
        cycle_segments = segments.split("/")
        result = ParsedCycleDefinition()

        if len(cycle_segments) != 2:
            raise Exception(f"Unable to parse the cycle definition {segments}. Segment count "
                            f"doesn't match. Expected 2, got {len(cycle_segments)} segments "
                            f"divided by /. ")

        m = REPEATING_RE.match(cycle_segments[0])
        if not m:
            raise Exception(f"Unable to parse repeating segment for cycle {segments}")

        result.repeat_count = int(m.group(1)) if m.group(1) else -1

        m = TIME_PERIOD_RE.match(cycle_segments[1])

        if not m:
            raise Exception(f"Unable to parse time segment for cycle {segments}")

        result.year = int(m.group(2)) if m.group(2) else 0
        result.month = int(m.group(4)) if m.group(4) else 0
        result.day = int(m.group(6)) if m.group(6) else 0
        result.hour = int(m.group(9)) if m.group(9) else 0
        result.minute = int(m.group(11)) if m.group(11) else 0
        result.second = int(m.group(13)) if m.group(13) else 0

        return result
