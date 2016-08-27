from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor

class FiguresTreeprocessor(Treeprocessor):
    def run(self, root):
        for img in root.findall('p/img'):
            img.set('class', 'illustration')

class FiguresExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.treeprocessors['figures'] = FiguresTreeprocessor()
