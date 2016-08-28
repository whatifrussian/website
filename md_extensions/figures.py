from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from markdown.util import etree

class FiguresTreeprocessor(Treeprocessor):
    @staticmethod
    def wrap_imgs_into_figure(elem):
        def add_figcaption(elem, title):
            em = etree.SubElement(etree.SubElement(
                etree.SubElement(elem, 'figcaption'), 'div'), 'em')
            em.text = title

        for p in (p for p in elem if p.tag == 'p'):
            imgs = [img for img in p if img.tag == 'img']
            if len(imgs) == 1:
                p.tag = 'figure'
                img = imgs[0]
                add_figcaption(p, img.get('title', ''))
                img.set('class', 'illustration')
            elif len(imgs) > 1:
                p.tag = 'figure'
                p.set('class', 'figure_wide')
                for img in imgs:
                    figure = etree.SubElement(p, 'figure')
                    p.remove(img)
                    figure.append(img)
                    add_figcaption(figure, img.get('title', ''))
                    img.set('class', 'illustration')

    def run(self, root):
        # wrap images in footnotes
        for li in root.findall("div[@class='footnote']/ol/li"):
            FiguresTreeprocessor.wrap_imgs_into_figure(li)
        # wrap images in an article
        FiguresTreeprocessor.wrap_imgs_into_figure(root)

class FiguresExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.treeprocessors['figures'] = FiguresTreeprocessor()
