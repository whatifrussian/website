import re
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from .md_utils import html_entity


# Markdown extension
# ==================


class EscapeExtPreprocessor(Preprocessor):
    def __init__(self):
        self.compiled_re = re.compile(self.RE, re.DOTALL | re.UNICODE)

    def run(self, lines):
        new_lines = []
        for line in lines:
            callback = lambda m: self.handleMatch(m)
            new_lines.append(re.sub(self.compiled_re, callback, line))
        return new_lines


class WhitespacesPreprocessor(EscapeExtPreprocessor):
    RE = r'(?P<before>.?)\\ (?P<after>.?)'

    def handleMatch(self, m):
        before = m.group('before')
        after = m.group('after')
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
