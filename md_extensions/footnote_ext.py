from __future__ import unicode_literals
import re
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from markdown.util import etree
from .etree_utils import replace_element_inplace, create_etree


# Utility functions
# =================


def tweak_footnote(place_to, num, li, punctum, is_multipar):
    refbody = etree.Element('span')
    refbody_cls = 'refbody' + (' refbody_wide' if is_multipar else '')
    refbody.set('class', refbody_cls)

    # Having block element inside inline one is invalid.
    # p -> span.p
    # figure -> span.figure
    # figcaption -> span.figcaption
    # div -> span.div
    refbody.text = li.text
    for child in li:
        if child.tag == 'p':
            child.tag = 'span'
            child.set('class', 'p')
        elif child.tag == 'figure':
            child.tag = 'span'
            child.set('class', 'figure')
            cap = child.find('figcaption')
            cap.tag = 'span'
            cap.set('class', 'figcaption')
            div = cap.find('div')
            div.tag = 'span'
            div.set('class', 'div')
        refbody.append(child)

    fn_tree = \
    ['span', 'ref', [
        ['nobr', '', [
            ['sup', 'refnum', [
                ['span', 'bracket', '['],
                ['span', '', num],
                ['span', 'bracket', ']'],
                ['b', '', '']]],
            ['span', 'punctum', punctum] if punctum is not None else [],
            ['span', 'ellipsis', '\u21b2']]],
        refbody,
        ['span', 'ellipsis', '\u21b3']]]
    replace_element_inplace(place_to, create_etree(fn_tree))


# Markdown extension
# ==================


class FootnoteExtTreeprocessor(Treeprocessor):
    def run(self, root):
        sups = root.findall('.//sup[@id]')
        for sup in sups:
            fn = sup.find("a[@rel='footnote']")
            if fn is None:
                continue
            # extract number and body
            num = fn.text
            id_ = fn.get('href')[1:]
            li = root.find("div[@class='footnote']/ol/li[@id='%s']" % id_)
            is_multipar = len(li.findall('p')) > 1
            # remove backreference
            backref = li[-1].find("./a[@rev='footnote']")
            if backref is not None:
                li[-1].remove(backref)
            # modify footnote
            punctum = None
            if sup.tail is not None:
                m = re.match(
                    r'^(?P<punctum>[,;:.)]*)(?P<rest>.*)$', sup.tail,
                    re.DOTALL)
                punctum = m.group('punctum')
                sup.tail = m.group('rest')
            tweak_footnote(sup, num, li, punctum, is_multipar)
        footnotes_div = root.find("div[@class='footnote']")
        if footnotes_div is not None:
            root.remove(footnotes_div)


class FootnoteExtExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.treeprocessors['footnote_ext'] = FootnoteExtTreeprocessor()
