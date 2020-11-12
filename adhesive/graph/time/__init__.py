import re


TIME_PERIOD_RE = re.compile(r'^P((\d{1,4})Y)?((\d{1,2})M)?((\d{1,2})D)?(T((\d{1,2})H)?((\d{1,2})M)?((\d{1,2})S)?)?$')
REPEATING_RE = re.compile(r'^R(\d+)?$')
