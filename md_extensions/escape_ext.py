from markdown.extensions import Extension
from .md_utils import TrivialPreprocessor, TrivialTextPattern


# Markdown extension
# ==================


class AbbrTitlePreprocessor(TrivialPreprocessor):
    def run(self, lines):
        for k, v in self.markdown.inlinePatterns.items():
            if not k.startswith('abbr-'):
                continue
            v.title = self.compiled_re.sub(self.handleMatch, v.title)
        return lines


class ReferenceTitlePreprocessor(TrivialPreprocessor):
    def run(self, lines):
        new_ref = {}
        for k, v in self.markdown.references.items():
            url, title = v
            if title:
                new_title = self.compiled_re.sub(self.handleMatch, title)
                new_ref[k] = (url, new_title)
            else:
                new_ref[k] = v
        self.markdown.references = new_ref
        return lines


class EscapeExtExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        processors = [
            (md.preprocessors, AbbrTitlePreprocessor, '>abbr'),
            (md.preprocessors, ReferenceTitlePreprocessor, '>reference'),
            (md.inlinePatterns, TrivialTextPattern, '<link'),
        ]

        # Thin space processing should be before non-breaking space, because of
        # nbsp regexp matched some cases of thinsp.
        patterns = [
            ('thinsp-', r'(?<=[0-9])\\ (?=[0-9])', '&thinsp;'),
            ('nbsp-', r'(?<!\\)\\ ', '&nbsp;'),
            # Modifier Letter Apostrophe
            ('apostrophe-', r'(?<!\\)\\\'', '&#x2bc;'),
        ]

        for parsers, cls, order in processors:
            cls_name = cls.__name__
            # odict.add() adds in reverse order when '>smth' used
            patterns_local = patterns
            if order.startswith('>'):
                patterns_local = list(reversed(patterns))
            for prefix, re, repl in patterns_local:
                name = prefix + cls_name
                inst = cls(md, re, repl)
                parsers.add(name, inst, order)
