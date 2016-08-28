from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from markdown.util import etree

class FiguresTreeprocessor(Treeprocessor):
    @staticmethod
    def wrap_imgs_into_figure(elem):
        for p in (p for p in elem if p.tag == 'p'):
            imgs = [img for img in p if img.tag == 'img']
            if len(imgs) == 1:
                p.tag = 'figure'
                em = etree.SubElement(etree.SubElement(
                    etree.SubElement(p, 'figcaption'), 'div'), 'em')
                em.text = imgs[0].get('title', '')
                imgs[0].set('class', 'illustration')
            elif len(imgs) > 1:
                # figures in row case, processed now by JS
                pass

    def run(self, root):
        # wrap images in footnotes
        for li in root.findall("div[@class='footnote']/ol/li"):
            FiguresTreeprocessor.wrap_imgs_into_figure(li)
        # wrap images in an article
        FiguresTreeprocessor.wrap_imgs_into_figure(root)

class FiguresExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.treeprocessors['figures'] = FiguresTreeprocessor()
