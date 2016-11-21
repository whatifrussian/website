import feedgenerator
from pelican import signals
from pelican import writers


# This temporary Pelican plugin created with intention to save IDs of RSS/Atom
# items for articles published before we moved to Pelican 3.7, which has new
# IDs format. It can be safely removed when 5 pages/articles will generated
# using Pelican 3.7.


def get_tag_uri_new(url, date):
    tags_new_format = {
        'tag:chtoes.li,2016-10-24:/speedup-and-feedback/',
        'tag:chtoes.li,2016-10-24:/flood-death-valley/',
        'tag:chtoes.li,2016-07-27:/sun-bug/',
        'tag:chtoes.li,2016-05-30:/tatooine-rainbow/',
        'tag:chtoes.li,2016-04-18:/pizza-bird/',
    }
    tag = feedgenerator.get_tag_uri(url, date)
    if tag in tags_new_format:
        tag = tag.replace('/', '', 1)
    return tag


def patch_get_tag_uri(pelican_object):
    writers.__dict__['get_tag_uri'] = get_tag_uri_new


def register():
    signals.initialized.connect(patch_get_tag_uri)
