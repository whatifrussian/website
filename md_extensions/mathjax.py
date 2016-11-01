from markdown.extensions import Extension
from .md_utils import TrivialTextPattern


# Markdown extension
# ==================


class MathJaxExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        def repl(match):
            return ''.join(match.group('edge', 'body', 'edge'))

        # exclude formulas from processing as a markdown
        MATHJAX_RE = r'(?<!\\)(?P<edge>\$\$?)(?P<body>.+?)(?P=edge)'
        mathJaxPattern = TrivialTextPattern(md, MATHJAX_RE, repl)
        md.inlinePatterns.add('mathjax', mathJaxPattern, '<escape')
