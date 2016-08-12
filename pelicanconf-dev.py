#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from localconf import *

SITEURL = 'https://dev.chtoes.li'
FEED_DOMAIN = SITEURL
EXTRA_PATH_METADATA = {
    'extra/robots-dev.txt': {'path': 'robots.txt'},
    'extra/manifest.json': {'path': 'manifest.json'},
}
STATIC_PATHS = [
    'uploads',
    'extra/robots-dev.txt',
    'extra/manifest.json'
]
