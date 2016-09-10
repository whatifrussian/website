import sys
from markdown.util import etree


PY3 = sys.version_info > (3,)


def replace_element(parent, old, new):
    idx = list(parent).index(old)
    parent.remove(old)
    parent.insert(idx, new)
    new.text = old.text
    new.tail = old.tail


def replace_element_inplace(old, new):
    old_tail = old.tail
    old.clear()
    old.tag = new.tag
    old.text = new.text
    old.tail = old_tail
    old.attrib = new.attrib
    for child in new:
        old.append(child)


def create_etree(in_tree):
    tag = lambda l: l[0]
    cls = lambda l: l[1]
    sub = lambda l: l[2]
    def set_class(elem, val):
        if val != '':
            elem.set('class', val)
    # `isinstance(x, etree.Element)` doesn't work well in Python 2
    def isElementInstance(x):
        elementType = type(etree.Element(None))
        return isinstance(x, elementType)

    if isElementInstance(in_tree):
        return in_tree
    if in_tree == []:
        return None
    elem = etree.Element(tag(in_tree))
    set_class(elem, cls(in_tree))
    subel = sub(in_tree)
    if isElementInstance(subel):
        elem.append(subel)
    elif isinstance(subel, str if PY3 else basestring):
        elem.text = subel
    elif isinstance(subel, list):
        for s in subel:
            new_elem = create_etree(s)
            if new_elem is not None:
                elem.append(new_elem)
    else:
        raise NameError('create_etree: bad input')
    return elem


def remove_suffix(elem, suffix):
    if len(elem) == 0:
        text = elem.text
    else:
        text = elem[-1].tail

    if text.endswith(suffix):
        text = text[:-len(suffix)]
        if len(elem) == 0:
            elem.text = text
        else:
            elem[-1].tail = text
