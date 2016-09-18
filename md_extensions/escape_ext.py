import re
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.inlinepatterns import BACKTICK_RE
from .md_utils import html_entity


# Markdown extension
# ==================


class EscapeExtPreprocessor(Preprocessor):
    def __init__(self):
        full_re = '(%s|%s)' % (BACKTICK_RE, self.RE)
        self.compiled_full_re = re.compile(full_re, re.DOTALL | re.UNICODE)

    def run(self, lines):
        def callback(m):
            # detect and skip `block code`
            text = m.group(0)
            if text[0] == r'`' and text[0] == text[-1]:
                return m.group(0)
            return self.handleMatch(m)
        new_lines = []
        for line in lines:
            new_lines.append(re.sub(self.compiled_full_re, callback, line))
        return new_lines


class WhitespacesPreprocessor(EscapeExtPreprocessor):
    RE = r'(?P<before>^|[^\\])\\ (?P<after>.?)'

    def handleMatch(self, m):
        before = m.group('before') or ''
        after = m.group('after') or ''
        if before.isdigit() and after.isdigit():
            return before + html_entity('&thinsp;') + after
        else:
            return before + html_entity('&nbsp;') + after


class ApostrophesPreprocessor(EscapeExtPreprocessor):
    RE = r'\\\''

    def handleMatch(self, m):
        # Modifier Letter Apostrophe
        return html_entity('&#x2bc;')


class EscapeExtExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        pps = md.preprocessors
        order = '<html_block' if 'html_block' in pps.keys() else '<reference'
        pps.add('whitespaces', WhitespacesPreprocessor(), order)
        pps.add('apostrophes', ApostrophesPreprocessor(), order)
