from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern
from markdown.util import AMP_SUBSTITUTE


# Markdown extension
# ==================


class WhitespacesPattern(Pattern):
    RE = r'(?P<before>.?)\\ (?P<after>.?)'

    def __init__(self):
        super(WhitespacesPattern, self).__init__(self.RE)

    def handleMatch(self, m):
        escape = lambda html: html.replace('&', AMP_SUBSTITUTE)
        before = m.group('before')
        after = m.group('after')
        if before.isdigit() and after.isdigit():
            return before + escape('&thinsp;') + after
        else:
            return before + escape('&nbsp;') + after


class EscapeExtExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('whitespaces', WhitespacesPattern(), '<escape')
