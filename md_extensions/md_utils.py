import re
from markdown.preprocessors import Preprocessor
from markdown.inlinepatterns import Pattern
from markdown.util import AMP_SUBSTITUTE


# To be understanded by Python-Markdown.
def html_entity(html):
    return html.replace('&', AMP_SUBSTITUTE)


# The class allow to change data holds by another preprocessor in the same way
# as TrivialTextPattern changes a text itself. In order to use it extend and
# overwrite 'run' method.
class TrivialPreprocessor(Preprocessor):
    def __init__(self, markdown, RE, repl):
        super(TrivialPreprocessor, self).__init__(markdown)
        self.compiled_re = re.compile(RE)
        self.repl = repl

    def store(self, x):
        return self.markdown.htmlStash.store(x)

    def handleMatch(self, m):
        if callable(self.repl):
            return self.store(self.repl(m))
        return self.store(self.repl)

    def run(self, lines):
        return lines


# The class intended to replace matched text with 'repl' (a string or a
# function) one using temporary key-value storage. The matched text replaced
# here with key corresponding to 'repl' string. The key alters to 'repl' later.
# The class can be added to markdown.inlinePatterns as is (with appropriate
# params).
class TrivialTextPattern(Pattern):
    def __init__(self, markdown, RE, repl):
        super(TrivialTextPattern, self).__init__(RE, markdown)
        self.repl = repl

    def store(self, x):
        return self.markdown.htmlStash.store(x)

    def handleMatch(self, m):
        if callable(self.repl):
            return self.store(self.repl(m))
        return self.store(self.repl)


# Fake preprocessor to make an action when metadata will be available. It leans
# on 'meta' extension. Inherit the class and redefine 'available' method.
class MetadataAction(Preprocessor):
    def run(self, lines):
        self.available(self.markdown.Meta)
        return lines

    def available(self, meta):
        pass
