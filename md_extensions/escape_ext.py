import re
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.inlinepatterns import Pattern


# Markdown extension
# ==================


class TrivialPreprocessor(Preprocessor):
    def __init__(self, markdown, RE, repl):
        super(TrivialPreprocessor, self).__init__(markdown)
        self.compiled_re = re.compile(RE)
        self.repl = repl

    def store(self, x):
        return self.markdown.htmlStash.store(x)

    def handleMatch(self, m):
        return self.store(self.repl)


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
            if v[1]:
                t = v[1]
                new_title = self.compiled_re.sub(self.handleMatch, v[1])
                new_ref[k] = (v[0], new_title)
            else:
                new_ref[k] = v
        self.markdown.references = new_ref
        return lines


class TrivialTextPattern(Pattern):
    def __init__(self, markdown, RE, repl):
        super(TrivialTextPattern, self).__init__(RE, markdown)
        self.repl = repl

    def store(self, x):
        return self.markdown.htmlStash.store(x)

    def handleMatch(self, m):
        return self.store(self.repl)


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
            add = lambda name, re, repl: parsers.add(
                name, cls(md, re, repl), order)
            cls_name = cls.__name__
            # odict.add() adds in reverse order when '>smth' used
            patterns_local = patterns
            if order.startswith('>'):
                patterns_local = list(reversed(patterns))
            for prefix, re, repl in patterns_local:
                add(prefix + cls_name, re, repl)
