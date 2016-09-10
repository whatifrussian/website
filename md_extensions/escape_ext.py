from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern
from markdown.util import AMP_SUBSTITUTE


# Utility functions
# =================


# To be understanded by Python-Markdown.
def html_entity(html):
    return html.replace('&', AMP_SUBSTITUTE)


# Markdown extension
# ==================


class WhitespacesPattern(Pattern):
    RE = r'(?P<before>.?)\\ (?P<after>.?)'

    def __init__(self):
        super(WhitespacesPattern, self).__init__(self.RE)

    def handleMatch(self, m):
        before = m.group('before')
        after = m.group('after')
        if before.isdigit() and after.isdigit():
            return before + html_entity('&thinsp;') + after
        else:
            return before + html_entity('&nbsp;') + after


class ApostrophesPattern(Pattern):
    RE = r'\\\''

    def __init__(self):
        super(ApostrophesPattern, self).__init__(self.RE)

    def handleMatch(self, m):
        # Modifier Letter Apostrophe
        return html_entity('&#x2bc;')


class EscapeExtExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('whitespaces', WhitespacesPattern(), '<escape')
        md.inlinePatterns.add('apostrophes', ApostrophesPattern(), '<escape')
