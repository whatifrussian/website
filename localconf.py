#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import logging

AUTHOR = u'whatif'
SITENAME = u'Что если?'
 
TIMEZONE = 'Europe/Moscow'

DEFAULT_LANG = u'ru'

PLUGIN_PATH = "plugins"
PLUGINS = ["neighbors", "sitemap"]
THEME = "themes/whatif"
PATH = 'content'
OUTPUT_PATH = 'output'
DELETE_OUTPUT_DIRECTORY = True

# Feed generation is usually not desired when developing
FEED_ALL_RSS = "feed/index.xml"
CATEGORY_FEED_RSS = "feed/category/%s/index.xml"
TAG_FEED_RSS = "feed/category/%s/index.xml"
FEED_MAX_ITEMS = 5

# Save as URL
ARTICLE_URL = '{slug}/'
ARTICLE_SAVE_AS = '{slug}/index.html'
CATEGORY_URL = '{slug}/'
CATEGORY_SAVE_AS = '{slug}/index.html'
TAGS_SAVE_AS = ''
TAG_SAVE_AS = ''
AUTHOR_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
ARCHIVES_SAVE_AS = ''
CATEGORIES_SAVE_AS = ''

LOG_FILTER = [
    (logging.WARN, 'Empty alt attribute for image {} in {}')
]

TEMPLATE_PAGES = {
    'translations.html': 'translations/index.html',
    '404.html': '404.html',
    'rewrite.html': 'rewrite.map'
    }

SLUG_SUBSTITUTIONS = [
    ("what if?", "what-if"),
    ("novosti proekta","news"),
    ("prochee", "other"),
#("",""),
]

DEFAULT_PAGINATION = False

EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/googleb52597a81842d95f.html': {'path': 'googleb52597a81842d95f.html'},
    'extra/yandex_7e403715421012c7.txt': {'path': 'yandex_7e403715421012c7.txt'},
}

FILES_TO_COPY = (
            ("uploads", "uploads")
            )

STATIC_PATHS = [
    'uploads',
    'extra/robots.txt',
    'extra/googleb52597a81842d95f.html',
    'extra/yandex_7e403715421012c7.txt'
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

MD_EXTENSIONS = (['extra', 'abbr', 'footnotes'])
