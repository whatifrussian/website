from markdown.extensions import Extension
from .md_utils import TrivialTextPattern, MetadataAction


# Markdown extension
# ==================


class MaybeEscapeDollar(MetadataAction):
    def available(self, meta):
        if 'formulas' not in meta or meta['formulas'] != ['False']:
            return
        # ESCAPED_CHARS is class variable, so we copy the list and assing it to
        # the instance to prevent sharing between Markdown instances
        chars = list(self.md.ESCAPED_CHARS)
        chars.append('$')
        self.md.ESCAPED_CHARS = chars


class MathJaxExtension(Extension):
    def extendMarkdown(self, md):
        def repl(match):
            return ''.join(match.group('edge', 'body', 'edge'))

        # '\$' -> '$' when formulas disabled;
        # that needed for consistency: when formulas enabled, MathJax with
        # 'processEscapes: true' will do that
        md.preprocessors.register(
            MaybeEscapeDollar(md), 'maybe_escape_dollar', 26)

        # exclude formulas from processing as a markdown
        MATHJAX_RE = r'(?<!\\)(?P<edge>\$\$?)(?P<body>.+?)(?P=edge)'
        mathJaxPattern = TrivialTextPattern(md, MATHJAX_RE, repl)
        md.inlinePatterns.register(mathJaxPattern, 'mathjax', 181)
