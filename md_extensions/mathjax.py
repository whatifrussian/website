import re
from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern
from markdown.treeprocessors import Treeprocessor
from markdown.util import etree, AtomicString
from .etree_utils import unbox_text_element


# Markdown extension
# ==================


class MathJaxPattern(Pattern):
    RE = r'(?<!\\)(?P<edge>\$\$?)(?P<body>.+?)(?P=edge)'

    def __init__(self):
        super(MathJaxPattern, self).__init__(self.RE)

    def handleMatch(self, m):
        span = etree.Element('span')
        span.set('class', 'mathjax')
        text = m.group('edge') + m.group('body') + m.group('edge')
        span.text = AtomicString(text)
        return span


# Expands <span class="mathjax"/> into just text
class MathJaxTreeprocessor(Treeprocessor):
    def run(self, root):
        unbox_text_element(root, 'span', 'mathjax')


class MathJaxExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('mathjax', MathJaxPattern(), '<escape')
        md.treeprocessors['mathjax'] = MathJaxTreeprocessor()
