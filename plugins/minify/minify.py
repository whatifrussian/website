"""Preserve the output of the original pelican-minify 0.9 plugin."""

from pathlib import Path
import re

from htmlmin import minify
from pelican import signals


def minify_html(pelican):
    options = pelican.settings.get('MINIFY', {})
    output_path = Path(pelican.settings['OUTPUT_PATH'])
    for path in output_path.rglob('*'):
        if path.suffix not in ('.html', '.htm'):
            continue
        source = path.read_text(encoding='utf-8')
        source = source.replace('&#39;', "'").replace('&#32;', ' ')
        source = re.sub(
            r'href="([^"]*)"',
            lambda match: 'href="{}"'.format(
                re.sub(r'&(?!#?[A-Za-z0-9]+;)', '&amp;', match.group(1))),
            source,
        )
        path.write_text(minify(source, **options), encoding='utf-8')


def register():
    signals.finalized.connect(minify_html)
