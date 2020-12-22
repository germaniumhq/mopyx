import enum


class BuildStatus(enum.Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    RUNNING = "running"
    IGNORED = "ignored"
    NEVER = "never"

