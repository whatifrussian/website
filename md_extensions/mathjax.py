from markdown.extensions import Extension
from .md_utils import TrivialTextPattern


# Markdown extension
# ==================


class MathJaxExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        MATHJAX_RE = r'(?<!\\)(?P<edge>\$\$?)(?P<body>.+?)(?P=edge)'
        repl = lambda m: ''.join(m.group('edge', 'body', 'edge'))
        mathJaxPattern = TrivialTextPattern(md, MATHJAX_RE, repl)
        md.inlinePatterns.add('mathjax', mathJaxPattern, '<escape')
