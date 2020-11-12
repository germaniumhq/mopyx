from adhesive.graph.time import TIME_PERIOD_RE


class ParsedDurationDefinition:
    def __init__(self) -> None:
        self.year = 0
        self.month = 0
        self.day = 0
        self.hour = 0
        self.minute = 0
        self.second = 0

    @staticmethod
    def from_str(segments: str) -> 'ParsedDurationDefinition':
        m = TIME_PERIOD_RE.match(segments)

        if not m:
            raise Exception(f"Unable to parse time period {segments}")

        result = ParsedDurationDefinition()

        result.year = int(m.group(2)) if m.group(2) else 0
        result.month = int(m.group(4)) if m.group(4) else 0
        result.day = int(m.group(6)) if m.group(6) else 0
        result.hour = int(m.group(9)) if m.group(9) else 0
        result.minute = int(m.group(11)) if m.group(11) else 0
        result.second = int(m.group(13)) if m.group(13) else 0

        return result
