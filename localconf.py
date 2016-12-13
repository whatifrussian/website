#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import logging
import md_extensions

AUTHOR = 'whatif'
SITENAME = 'Что если?'

TIMEZONE = 'Europe/Moscow'

DEFAULT_LANG = 'ru'

PLUGIN_PATHS = ['plugins']
PLUGINS = ['neighbors', 'sitemap', 'assets', 'minify', 'gzip_cache',
           'preserve_old_feed_items', 'feed_alter_settings']
THEME = 'themes/whatif'
PATH = 'content'
OUTPUT_PATH = 'output'
DELETE_OUTPUT_DIRECTORY = True

MINIFY = {
    'remove_comments': True,
    'remove_all_empty_space': True,
    'remove_optional_attribute_quotes': True,
}

# RSS feeds
FEED_ALL_RSS = 'feed/index.xml'
CATEGORY_FEED_RSS = None
AUTHOR_FEED_RSS = None
TRANSLATION_FEED_RSS = None
TAG_FEED_RSS = None
# Atom feeds
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
TAG_FEED_ATOM = None
# Feeds options
FEED_MAX_ITEMS = 5
RSS_FEED_SUMMARY_ONLY = False

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
    (logging.WARN, 'Empty alt attribute for image %s in %s')
]

TEMPLATE_PAGES = {
    'translations.html': 'translations/index.html',
    '404.html': '404.html',
    'rewrite.html': 'rewrite.map'
}

SLUG_SUBSTITUTIONS = [
    ('what if?', 'what-if'),
    ('novosti proekta', 'news'),
    ('prochee', 'other'),
    # ('',''),
]

DEFAULT_PAGINATION = False

EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/googleb52597a81842d95f.html':
        {'path': 'googleb52597a81842d95f.html'},
    'extra/yandex_7e403715421012c7.txt':
        {'path': 'yandex_7e403715421012c7.txt'},
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
# RELATIVE_URLS = False
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

MARKDOWN = {
    'extensions': [
        'markdown.extensions.meta',
        'markdown.extensions.extra',
        'markdown.extensions.abbr',
        'markdown.extensions.footnotes',
        md_extensions.QuestionExtension(),
        md_extensions.FiguresExtension(),
        md_extensions.FootnoteExtExtension(),
        md_extensions.EscapeExtExtension(),
        md_extensions.TextAlignExtension(),
        md_extensions.MathJaxExtension(),
        md_extensions.SubSuperScriptExtension(),
        md_extensions.ArticleLinksExtension(),
    ],
    'output_format': 'html5',
}


# remove footnotes extension
# remove footnotes_ext extension
# add footnotes extension with UNIQUE_IDS=True
def FEED_ALTER_SETTINGS(settings):
    import six
    from markdown.extensions.footnotes import FootnoteExtension

    markdown_opts = settings['MARKDOWN']
    for ext in list(markdown_opts['extensions']):
        is_str = isinstance(ext, six.string_types)
        if is_str and ext == 'markdown.extensions.footnotes':
            markdown_opts['extensions'].remove(ext)
        elif isinstance(ext, md_extensions.FootnoteExtExtension):
            markdown_opts['extensions'].remove(ext)
    # it's necessary to create instance to get unique_prefix being persistent
    markdown_opts['extensions'].append(FootnoteExtension(UNIQUE_IDS=True))
