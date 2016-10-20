#!/usr/bin/env python


import os
import re
import sys
from itertools import count


def process_md_file(filepath):
    def get_next_label():
        nonlocal next_try_label_int
        for i in count(start=next_try_label_int, step=1):
            cur = str(i)
            if cur in booked_labels:
                continue
            next_try_label_int = i + 1
            booked_labels.append(cur)
            return cur

    def repl(m):
        has_inline_links = True
        label = get_next_label()
        text = m.group('text')
        url = m.group('url')
        title = m.group('title')
        if title:
            stash.append('[{label}]: {url} "{title}"'.format_map(locals()))
        else:
            stash.append('[{label}]: {url}'.format_map(locals()))
        return '[{text}][{label}]'.format(text=text, label=label)

    # reference_link_use_re = r'(?<!!)\[[^\[\]]+\]\[\d+\]'
    reference_link_def_re = r'^\[(?P<label>[^\^\[\]]+)\]: .*$'
    inline_link_re = r'(?<!!)' + \
        r'\[' + \
        r'(?P<text>[^\[\]]+)' + \
        r'\]' + \
        r'\(' + \
        r'(?P<url>[^\(\)"]+)' + \
        r'(?: +"(?P<title>[^"]+)")?' + \
        r'\)'

    with open(filepath, 'r') as f:
        content = f.read()

    next_try_label_int = 1
    booked_labels = re.findall(reference_link_def_re, content, re.U | re.M)
    has_reference_links = len(booked_labels) > 0
    has_inline_links = False
    stash = []

    content = re.sub(inline_link_re, repl, content, re.U | re.M)

    if has_reference_links and has_inline_links:
        print('WARNING: {filepath} has both reference and inline links'
              .format(filepath=filepath), file=sys.stderr)

    # pop stash
    content = content.rstrip('\n')
    for s in stash:
        content += '\n\n' + s
    # one newline at end
    content += '\n'

    with open(filepath, 'w') as f:
        f.write(content)


base_dir = os.path.dirname(os.path.abspath(__file__))
content_dir = os.path.join(base_dir, 'content')

for category_dirname in os.listdir(content_dir):
    category_dir = os.path.join(content_dir, category_dirname)
    if not os.path.isdir(category_dir):
        continue
    for filename in os.listdir(category_dir):
        filepath = os.path.join(category_dir, filename)
        if os.path.isfile(filepath) and filename.endswith('.md'):
            process_md_file(filepath)
