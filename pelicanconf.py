#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import logging

AUTHOR = u'whatif'
SITENAME = u'Что если?'
SITEURL = 'http://dev.chtoes.li'
 
TIMEZONE = 'Europe/Moscow'

DEFAULT_LANG = u'ru'

PLUGIN_PATH = "plugins"
PLUGINS = ["neighbors", "sitemap"]
THEME = "themes/whatif"
PATH = 'content'
OUTPUT_PATH = 'output'
DELETE_OUTPUT_DIRECTORY = True

# Feed generation is usually not desired when developing
FEED_DOMAIN = SITEURL
FEED_ALL_RSS = "feed/index.xml"
CATEGORY_FEED_RSS = "feed/category/%s/index.xml"
TAG_FEED_RSS = "feed/category/%s/index.xml"

# Save as URL
ARTICLE_URL = 'page/{slug}/'
ARTICLE_SAVE_AS = 'page/{slug}/index.html'
CATEGORY_URL = 'category/{slug}/'
CATEGORY_SAVE_AS = 'category/{slug}/index.html'
TAGS_SAVE_AS = ''
TAG_SAVE_AS = ''
AUTHOR_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
ARCHIVES_SAVE_AS = ''
CATEGORIES_SAVE_AS = ''

LOG_FILTER = [
    (logging.WARN, 'Empty alt attribute for image {} in {}')
]


SLUG_SUBSTITUTIONS = [
    ("what if?", "what-if"),
    ("novosti proekta","news"),
    ("prochee", "other"),
#("",""),
]

DEFAULT_PAGINATION = False

EXTRA_PATH_METADATA = {
    'extras/robots.txt': {'path': 'robots.txt'},
}

FILES_TO_COPY = (("uploads", "uploads"))

STATIC_PATHS = [
    'uploads',
    'extras',
]


# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = False
READERS={'html':None}


SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}
