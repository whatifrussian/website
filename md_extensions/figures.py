from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from markdown.util import etree
from .etree_utils import replace_element


# Utility functions
# =================


def create_figure(img, non_imgs=[]):
    img.set('class', 'illustration')
    figure = etree.Element('figure')
    figure.append(img)
    em = etree.SubElement(etree.SubElement(
        etree.SubElement(figure, 'figcaption'), 'div'), 'em')
    em.text = img.get('title', '')
    if len(non_imgs) > 0:
        figure.extend(non_imgs)
    return figure


def wrap_imgs_into_figure(elem):
    for p in (p for p in elem if p.tag == 'p'):
        imgs = [img for img in p if img.tag == 'img']
        if len(imgs) == 1:
            non_imgs = [e for e in p if e not in imgs]
            figure = create_figure(imgs[0], non_imgs)
            replace_element(elem, p, figure)
        elif len(imgs) > 1:
            p.tag = 'figure'
            p.set('class', 'figure_wide')
            for img in imgs:
                figure = create_figure(img)
                replace_element(p, img, figure)


# Markdown extension
# ==================


class FiguresTreeprocessor(Treeprocessor):
    def run(self, root):
        # wrap images in footnotes
        for li in root.findall("div[@class='footnote']/ol/li"):
            wrap_imgs_into_figure(li)
        # wrap images in an article
        wrap_imgs_into_figure(root)

class FiguresExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.treeprocessors['figures'] = FiguresTreeprocessor()
