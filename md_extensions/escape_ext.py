import re

from markdown.extensions import Extension
from markdown.postprocessors import Postprocessor
from markdown.preprocessors import Preprocessor
from markdown.treeprocessors import Treeprocessor
from .md_utils import TrivialPreprocessor, TrivialTextPattern, html_entity


# Markdown extension
# ==================


class AbbrTitlePreprocessor(TrivialPreprocessor):
    def run(self, lines):
        for k, v in self.md.inlinePatterns._data.items():
            if not k.startswith('abbr-'):
                continue
            v.title = self.compiled_re.sub(self.handleMatch, v.title)
        return lines


class ReferenceTitlePreprocessor(TrivialPreprocessor):
    def run(self, lines):
        new_ref = {}
        for k, v in self.md.references.items():
            url, title = v
            if title:
                new_title = self.compiled_re.sub(self.handleMatch, title)
                new_ref[k] = (url, new_title)
            else:
                new_ref[k] = v
        self.md.references = new_ref
        return lines


class QuotedTitlePreprocessor(Preprocessor):
    pattern = re.compile(r'''(\]\([^\n]*?")'([^\n]*?)'("\))''')

    def run(self, lines):
        result = []
        for line in lines:
            line = self.pattern.sub(r'\1&#39;\2&#39;\3', line)
            line = line.replace('] (/', '](/')
            line = line.replace(' " :', ' "&#32;:')
            if line.startswith('[^') and line.endswith(' '):
                # Protect the existing trailing space; do not add a second
                # one. Markdown 3 otherwise trims it before parsing the note.
                line = line[:-1] + '&#32;'
            if result and result[-1].endswith(']') and line.startswith('(/'):
                result[-1] += line
                continue
            result.append(line)
        return result


class ReferenceTitleTreeprocessor(Treeprocessor):
    def run(self, root):
        for elem in root.iter():
            for name, value in elem.attrib.items():
                # Keep the legacy entity spelling, not merely the equivalent
                # Unicode character. Besides making old/new output stable,
                # &nbsp; makes the typographic intent visible in HTML diffs.
                value = re.sub(
                    r'(?<=\d)\\ (?=\d)', html_entity('&thinsp;'), value)
                value = value.replace(r'\ ', html_entity('&nbsp;'))
                value = value.replace(r"\'", html_entity('&#x2bc;'))
                elem.set(name, value)


class LegacyEntityPostprocessor(Postprocessor):
    """Undo compatibility entities needed only while parsing Markdown.

    Modern Markdown interprets apostrophe-delimited text inside an image title
    differently from the old release. QuotedTitlePreprocessor protects those
    apostrophes until parsing is complete; the old renderer emitted them as
    literal characters, so restore that representation in the final fragment.
    """

    def run(self, text):
        return text.replace('&#39;', "'").replace('&#32;', ' ')


class EscapeExtExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(
            QuotedTitlePreprocessor(md), 'quoted_titles', 28)
        processors = [
            (md.preprocessors, AbbrTitlePreprocessor, 11),
            (md.preprocessors, ReferenceTitlePreprocessor, 11),
            (md.inlinePatterns, TrivialTextPattern, 161),
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
            if cls is not TrivialTextPattern:
                patterns_local = list(reversed(patterns))
            for prefix, re, repl in patterns_local:
                name = prefix + cls_name
                inst = cls(md, re, repl)
                parsers.register(inst, name, order)

        md.treeprocessors.register(
            ReferenceTitleTreeprocessor(md), 'reference_titles', 1)
        md.postprocessors.register(
            LegacyEntityPostprocessor(md), 'legacy_entities', 0)
