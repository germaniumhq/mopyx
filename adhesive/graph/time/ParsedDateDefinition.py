import dateutil.parser


class ParsedDateDefinition:
    def __init__(self, *, date) -> None:
        self.date = date

    @staticmethod
    def from_str(s: str) -> 'ParsedDateDefinition':
        try:
            parsed_date = dateutil.parser.parse(s)

            date_definition = ParsedDateDefinition(date=parsed_date)

            return date_definition
        except Exception as e:
            raise Exception(f"Unable to parse date time {s}", e)
