from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from markdown.util import etree


# Markdown extension
# ==================


class QuestionTreeprocessor(Treeprocessor):
    def run(self, root):
        blockquote = root.find("blockquote")
        if blockquote is None:
            return None
        blockquote.set('class', 'question')
        div = etree.Element('div')
        for child in list(blockquote):
            div.append(child)
            blockquote.remove(child)
        blockquote.append(div)


class QuestionExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.treeprocessors['question'] = QuestionTreeprocessor()
