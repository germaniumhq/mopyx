import re

from .pattern import Pattern, TrackedVersion
from .regex_pattern import RegExPattern
from termcolor_util import eprint, yellow


class StringPattern(Pattern):
    RE = re.compile(r"^(.*?)(\^\^|##|\*\*)VERSION(##|\*\*|\$\$)(.*?)$")

    def __init__(self, tracked_version: TrackedVersion, expression: str) -> None:
        m = StringPattern.RE.match(expression)

        if not m:
            raise Exception("Unable to parse %s as a string pattern" % expression)

        if m.group(2) == "##" or m.group(3) == "#":
            eprint(
                yellow(
                    "Version matched using expression '%s' "
                    "still uses the old '##' notation for delimiting the "
                    "version. This is not supported anymore since # denotes "
                    "a comment in YAML. Use '**' instead." % expression
                )
            )

        regexp_value = (
            ("^()" if m.group(2) == "^^" else "(%s)" % re.escape(m.group(1)))
            + "(.*?)"
            + ("$" if m.group(3) == "$$" else "(%s)" % re.escape(m.group(4)))
        )

        self.tracked_version = tracked_version
        self.regex_pattern = RegExPattern(
            tracked_version, regexp_value, extra_flags=re.M
        )

    def apply_pattern(self, input_str: str) -> str:
        return self.regex_pattern.apply_pattern(input_str)

    @property
    def match_count(self) -> int:
        return self.regex_pattern.match_count

    @property
    def expected_count(self) -> int:
        return self.regex_pattern.expected_count
