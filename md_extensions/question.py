import re
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from markdown.util import etree
from markdown.blockprocessors import BlockQuoteProcessor


# Utility functions
# =================


def tweak_question(blockquote):
    blockquote.set('class', 'question')
    div = etree.Element('div')
    for child in list(blockquote):
        div.append(child)
        blockquote.remove(child)
    blockquote.append(div)


# Markdown extension
# ==================


# Parse special question blockquote (>>).
class QuestionBlockProcessor(BlockQuoteProcessor):
    RE = re.compile(r'(^|\n)[ ]{0,3}>>[ ]?(.*)')

    def run(self, parent, blocks):
        super(QuestionBlockProcessor, self).run(parent, blocks)
        blockquote = self.lastChild(parent)
        tweak_question(blockquote)


# Fix first regular blockquote (>).
class QuestionTreeprocessor(Treeprocessor):
    def run(self, root):
        blockquote = root.find('blockquote')
        if blockquote is None:
            return None
        if blockquote.get('class') == 'question':
            # It's a blockquote created by QuestionBlockProcessor
            return None
        tweak_question(blockquote)


class QuestionExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.parser.blockprocessors.add(
            'question', QuestionBlockProcessor(md.parser), '<quote')
        md.treeprocessors['question'] = QuestionTreeprocessor()
