#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from localconf import *

SITEURL = 'http://localhost:8000'
FEED_DOMAIN = SITEURL

ASSET_DEBUG = True
PLUGINS = [p for p in PLUGINS if p not in ('minify', 'gzip_cache')]
