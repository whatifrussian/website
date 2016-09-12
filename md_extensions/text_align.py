import re
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from markdown.util import etree


# Markdown extension
# ==================


class TextAlignTreeprocessor(Treeprocessor):
    BEGIN_CRE = re.compile(r'^ *--> *(.*)$')
    END_CRE = re.compile(r'^(.*?) *<-- *$')
    COMMON_CRE = re.compile(r'^ *--> *(.*?) *<-- *$')

    def tweak_paragraph(self, p):
        has_childs = len(p) > 0
        if has_childs:
            begin_m = self.BEGIN_CRE.match(p.text or '')
            end_m = self.END_CRE.match(p[-1].tail or '')
            if not (begin_m and end_m):
                return
            p.text = begin_m.group(1)
            p[-1].tail = end_m.group(1)
        else:
            common_m = self.COMMON_CRE.match(p.text or '')
            if not common_m:
                return
            p.text = common_m.group(1)
        cls = p.get('class', '')
        p.set('class', (cls + ' center').lstrip(' '))

    def run(self, root):
        for p in root.findall('.//p'):
            self.tweak_paragraph(p)
        for p in root.findall(".//span[@class='p']"):
            self.tweak_paragraph(p)


class TextAlignExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.treeprocessors['text_align'] = TextAlignTreeprocessor()
