import re

URL_REGEX = re.compile(
    r'^(http|https)://'
    r'(?P<host>[^\/\?:]+)'
    r'(?P<port>:[0-9]+)?'
    r'(?P<path>\/.*?)?'
    r'(?P<query>\?.*)?$'
)

SHORT_ID_REGEX = re.compile(
    r'^[a-zA-Z\d]{,16}$'
)
