# Compatible by names with the six package


import sys


PY3 = sys.version_info[0] == 3


if PY3:
    string_types = str,
else:
    string_types = basestring,  # noqa: F821 undefined name 'basestring'
