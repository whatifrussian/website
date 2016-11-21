import os
import copy
from pelican import signals
from pelican.writers import Writer
from pelican.readers import Readers


# The plugin indent to run readers (such as markdown) with different settings
# for main content and RSS/Atom feeds.
#
# Usage: create the following function in Pelican's config file.
#
# def FEED_ALTER_SETTINGS(settings):
#     ... modify settings here ...


CALLBACK_NAME = 'FEED_ALTER_SETTINGS'


class FeedAlterSettingsWriter(Writer):
    def __init__(self, output_path, settings=None):
        super(FeedAlterSettingsWriter, self).__init__(
            output_path, settings=settings)
        # copy and alter settings
        new_settings = copy.deepcopy(self.settings)
        self.settings[CALLBACK_NAME](new_settings)
        # put the new settings into readers
        self.readers = Readers(new_settings)

    def alter_item(self, item):
        # split path to dir and filename
        abspath = os.path.abspath(item.source_path)
        base_path = os.path.dirname(abspath)
        path = os.path.basename(abspath)
        # read content with the new settings
        return self.readers.read_file(base_path=base_path, path=path,
                                      content_class=item.__class__)

    def _add_item_to_the_feed(self, feed, item):
        # sunstitute the item with new one created with the new settings
        item = self.alter_item(item)
        super(FeedAlterSettingsWriter, self)._add_item_to_the_feed(feed, item)


def get_custom_writer(pelican_object):
    has_callback = CALLBACK_NAME in pelican_object.settings
    if has_callback and callable(pelican_object.settings[CALLBACK_NAME]):
        return FeedAlterSettingsWriter
    else:
        return Writer


def register():
    signals.get_writer.connect(get_custom_writer)
