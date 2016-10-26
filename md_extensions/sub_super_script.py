from markdown.extensions import Extension
from markdown.inlinepatterns import SimpleTagPattern


# Markdown extension
# ==================


class SubSuperScriptExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        patterns = md.inlinePatterns
        # H_{2}O and E=mc^{2}
        SUBSCRIPT_RE = r'(_)\{([^}]+)\}'
        SUPERSCRIPT_RE = r'(\^)\{([^}]+)\}'
        patterns['subscript'] = SimpleTagPattern(SUBSCRIPT_RE, 'sub')
        patterns['superscript'] = SimpleTagPattern(SUPERSCRIPT_RE, 'sup')
