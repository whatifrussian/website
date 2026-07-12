# -*- coding: utf-8 -*-


from __future__ import unicode_literals
import re
from markdown.extensions import Extension
from markdown.postprocessors import Postprocessor
from markdown.treeprocessors import Treeprocessor
from xml.etree import ElementTree as etree
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
            ['span', 'nobr', [
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
            fn = sup.find("a[@class='footnote-ref']")
            if fn is None:
                continue
            # extract number and body
            id_ = fn.get('href')[1:]
            ref_text = id_[len('fn-'):]
            is_non_number = False
            if not ref_text.isdigit():
                is_non_number = True
                ref_text = '#'
            li = root.find("div[@class='footnote']/ol/li[@id='%s']" % id_)
            is_multipar = len(li.findall('p')) > 1
            # remove backreference
            backref = li[-1].find("./a[@class='footnote-backref']")
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


class ImageMapFootnotePostprocessor(Postprocessor):
    """Restore inline footnotes attached to raw-HTML image maps.

    ``FootnoteExtTreeprocessor`` normally decides whether to emit the closing
    ``ellipsis`` marker by looking for elements after the original ``sup`` in
    its parent. That works for Markdown elements, but not for a raw-HTML
    ``map``. Python-Markdown removes raw HTML into ``htmlStash`` before tree
    processors run and restores it later in its ``raw_html`` postprocessor.
    Consequently, while ``FootnoteExtTreeprocessor`` is running, it sees the
    footnote as the final child of a paragraph: the following map is not an
    ElementTree sibling, ``has_text_after`` is false, and both the closing
    arrow and the empty punctuation anchor are omitted. When raw HTML is
    restored, Markdown 3 also places the map after ``</p>``. Markdown 2 kept
    that map inside the paragraph, which is the DOM expected by the site's
    inline-footnote CSS and JavaScript.

    This cannot be corrected reliably in ``FootnoteExtTreeprocessor`` without
    depending on Python-Markdown's private stash-placeholder format and moving
    opaque placeholder text between ElementTree ``text``/``tail`` fields.
    Such a workaround would be more fragile than waiting until raw HTML has
    been restored. This postprocessor therefore runs after ``raw_html`` (its
    priority is lower), matches an image and map through their standard
    ``usemap``/``name`` relationship, and restores only the legacy relationship
    needed by the footnote widget:

    * the map is moved back inside the image paragraph;
    * the empty ``punctum`` span is restored; and
    * the closing ``ellipsis`` arrow is restored.

    Ordinary footnotes and raw-HTML blocks without a matching image map are
    returned unchanged.
    """

    def run(self, source):
        search_from = 0
        while True:
            map_start = source.find('<map name="', search_from)
            if map_start < 0:
                return source
            name_start = map_start + len('<map name="')
            name_end = source.find('"', name_start)
            name = source[name_start:name_end]
            usemap = source.rfind('usemap="#{}"'.format(name), 0, map_start)
            paragraph_end = source.rfind('</p>', usemap, map_start)
            map_end = source.find('</map>', map_start)
            if usemap < 0 or paragraph_end < 0 or map_end < 0:
                search_from = name_end
                continue

            segment = source[usemap:paragraph_end]
            segment = segment.replace(
                '</sup><span class="ellipsis">',
                '</sup><span class="punctum"></span>'
                '<span class="ellipsis">',
                1,
            )
            final_span = segment.rfind('</span>')
            segment = (segment[:final_span] +
                       '<span class="ellipsis">↳</span>' +
                       segment[final_span:])
            source = (
                source[:usemap] + segment +
                source[paragraph_end + len('</p>'):
                       map_end + len('</map>')] +
                '</p>' + source[map_end + len('</map>'):]
            )
            search_from = map_end + len('</map>')


class FootnoteExtExtension(Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(
            FootnoteExtTreeprocessor(md), 'footnote_ext', 0)
        md.postprocessors.register(
            ImageMapFootnotePostprocessor(md), 'image_map_footnotes', 0)
