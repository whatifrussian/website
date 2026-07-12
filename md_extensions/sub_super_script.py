from markdown.extensions import Extension
from markdown.inlinepatterns import SimpleTagPattern


# Markdown extension
# ==================


class SubSuperScriptExtension(Extension):
    def extendMarkdown(self, md):
        patterns = md.inlinePatterns
        # H_{2}O and E=mc^{2}
        SUBSCRIPT_RE = r'(_)\{([^}]+)\}'
        SUPERSCRIPT_RE = r'(\^)\{([^}]+)\}'
        patterns.register(SimpleTagPattern(SUBSCRIPT_RE, 'sub'),
                          'subscript', 0)
        patterns.register(SimpleTagPattern(SUPERSCRIPT_RE, 'sup'),
                          'superscript', 0)
