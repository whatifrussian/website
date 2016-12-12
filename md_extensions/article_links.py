from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor


# Lean on the 'meta' extension.
class ArticleLinksTreeprocessor(Treeprocessor):
    def run(self, root):
        meta = self.markdown.Meta
        if 'category' not in meta or meta['category'] != ['What If?']:
            return None
        links = root.findall('.//a[@href]')
        for link in links:
            if not link.get('href').startswith('#'):
                link.set('target', '_blank')


class ArticleLinksExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.treeprocessors['article_links'] = ArticleLinksTreeprocessor(md)
