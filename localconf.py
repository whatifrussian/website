#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
# Currently not used, see below.
#import logging

AUTHOR = 'whatif'
SITENAME = 'Что если?'

TIMEZONE = 'Europe/Moscow'

DEFAULT_LANG = 'ru'

PLUGIN_PATHS = [ "plugins" ]
PLUGINS = ["neighbors", "sitemap", 'assets', 'minify', 'gzip_cache']
THEME = "themes/whatif"
PATH = 'content'
OUTPUT_PATH = 'output'
DELETE_OUTPUT_DIRECTORY = True


MINIFY = {
    'remove_comments': True,
    'remove_all_empty_space': True,
    'remove_optional_attribute_quotes': True,
}

# RSS feeds
FEED_ALL_RSS = "feed/index.xml"
CATEGORY_FEED_RSS = "feed/category/%s/index.xml"
AUTHOR_FEED_RSS = None
TRANSLATION_FEED_RSS = None
TAG_FEED_RSS = None
# Atom feeds
FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = "feeds/%s.atom.xml"
AUTHOR_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
TAG_FEED_ATOM = None
# Feeds options
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

# Currently that isn’t not working, see
# https://github.com/getpelican/pelican/issues/1594
#LOG_FILTER = [
#    (logging.WARN, 'Empty alt attribute for image %s in %s')
#]

TEMPLATE_PAGES = {
    'translations.html': 'translations/index.html',
    '404.html': '404.html',
    'rewrite.html': 'rewrite.map'
}

SLUG_SUBSTITUTIONS = [
    ("what if?", "what-if"),
    ("novosti proekta", "news"),
    ("prochee", "other"),
    #("",""),
]

DEFAULT_PAGINATION = False

EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/googleb52597a81842d95f.html': {'path': 'googleb52597a81842d95f.html'},
    'extra/yandex_7e403715421012c7.txt': {'path': 'yandex_7e403715421012c7.txt'},
    'extra/manifest.json': {'path': 'manifest.json'},
}

STATIC_PATHS = [
    'uploads',
    'extra/robots.txt',
    'extra/googleb52597a81842d95f.html',
    'extra/yandex_7e403715421012c7.txt',
    'extra/manifest.json'
]

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = False
READERS = {'html': None}

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

from md_extensions.question import QuestionExtension
from md_extensions.figures import FiguresExtension
from md_extensions.footnote_ext import FootnoteExtExtension
from md_extensions.escape_ext import EscapeExtExtension
from md_extensions.text_align import TextAlignExtension
from md_extensions.mathjax import MathJaxExtension
from md_extensions.sub_super_script import SubSuperScriptExtension
from md_extensions.article_links import ArticleLinksExtension

MD_EXTENSIONS = ([
    'meta',
    'extra',
    'abbr',
    'footnotes',
    QuestionExtension(),
    FiguresExtension(),
    FootnoteExtExtension(),
    EscapeExtExtension(),
    TextAlignExtension(),
    MathJaxExtension(),
    SubSuperScriptExtension(),
    ArticleLinksExtension(),
])
