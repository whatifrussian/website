# -*- coding: utf-8 -*-


from __future__ import unicode_literals
import re
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from markdown.util import etree
from markdown.extensions.footnotes import NBSP_PLACEHOLDER
from .etree_utils import replace_element_inplace, create_etree, \
    remove_suffix, add_suffix
from .md_utils import html_entity
from .six_mini import string_types


# Utility functions
# =================


NON_NUMBER_BODY_SUFFIX = [
    html_entity('&nbsp;') + '— ',
    ('em', 'Прим. пер.'),
]


def non_number_footnote_add_suffix(elem):
    for s in NON_NUMBER_BODY_SUFFIX:
        if isinstance(s, string_types):
            add_suffix(elem, s)
        elif isinstance(s, tuple) and len(s) == 2:
            etree.SubElement(elem, s[0]).text = s[1]
        else:
            raise NameError('non_number_footnote_add_suffix: bad input')


def tweak_footnote(place_to, ref_text, li, punctum, is_multipar,
                   has_text_after, is_non_number):
    refbody = etree.Element('span')
    refbody_cls = 'refbody' + (' refbody_wide' if is_multipar else '')
    refbody.set('class', refbody_cls)

    # Having block element inside inline one is invalid.
    # p, figure, figcaption, div -> span.p, span.figure, etc
    refbody.text = li.text
    for i, child in enumerate(li):
        # block -> inline
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
        # remove &nbsp; at end of last </p>
        if i == len(li) - 1:
            remove_suffix(child, NBSP_PLACEHOLDER)
            if is_non_number:
                non_number_footnote_add_suffix(child)
        # ready and go
        refbody.append(child)

    fn_tree = \
        ['span', 'ref', [
            ['nobr', '', [
                ['sup', 'refnum', [
                    ['span', 'bracket', '['],
                    ['span', '', ref_text],
                    ['span', 'bracket', ']'],
                    ['b', '', '']]],
                ['span', 'punctum', punctum] if punctum is not None else [],
                ['span', 'ellipsis', '\u21b2']]],
            refbody,
            ['span', 'ellipsis', '\u21b3'] if has_text_after else []]]
    replace_element_inplace(place_to, create_etree(fn_tree))


# Markdown extension
# ==================


class FootnoteExtTreeprocessor(Treeprocessor):
    def run(self, root):
        # TODO: use precapculated child-parent map?
        def get_sup_parent(root, id_):
            for maybe_parent in root.findall('.//*[sup]'):
                if maybe_parent.find("./sup[@id='%s']" % id_):
                    return maybe_parent
            return None

        sups = root.findall('.//sup[@id]')
        for sup in sups:
            fn = sup.find("a[@rel='footnote']")
            if fn is None:
                continue
            # extract number and body
            id_ = fn.get('href')[1:]
            ref_text = id_[len('fn:'):]
            is_non_number = False
            if not ref_text.isdigit():
                is_non_number = True
                ref_text = '#'
            li = root.find("div[@class='footnote']/ol/li[@id='%s']" % id_)
            is_multipar = len(li.findall('p')) > 1
            # remove backreference
            backref = li[-1].find("./a[@rev='footnote']")
            if backref is not None:
                li[-1].remove(backref)
            # modify footnote
            punctum = None
            siblings = list(get_sup_parent(root, sup.get('id')))
            has_text_after = siblings.index(sup) < len(siblings) - 1
            if sup.tail is not None:
                m = re.match(
                    r'^(?P<punctum>[,;:.)]*)(?P<rest>.*)$', sup.tail,
                    re.DOTALL)
                punctum = m.group('punctum')
                rest = m.group('rest')
                sup.tail = rest if rest != '' else None
                has_text_after = has_text_after or sup.tail is not None
            tweak_footnote(sup, ref_text, li, punctum, is_multipar,
                           has_text_after, is_non_number)
        footnotes_div = root.find("div[@class='footnote']")
        if footnotes_div is not None:
            root.remove(footnotes_div)


class FootnoteExtExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.treeprocessors['footnote_ext'] = FootnoteExtTreeprocessor()
