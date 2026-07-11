"""Keep feedgenerator 1.x XML serialization on modern Pelican."""

from pathlib import Path
import re

from pelican import signals


def preserve_legacy_feeds(pelican):
    output = Path(pelican.settings['OUTPUT_PATH'])

    rss_path = output / pelican.settings['FEED_ALL_RSS']
    rss = rss_path.read_text(encoding='utf-8')
    rss = rss.replace(' xmlns:atom="http://www.w3.org/2005/Atom"', '')
    rss = re.sub(r'<atom:link [^>]*/>', '', rss)
    rss = rss.replace('<description/>', '<description></description>')
    rss_path.write_text(rss, encoding='utf-8')

    atom_path = output / pelican.settings['FEED_ALL_ATOM']
    atom = atom_path.read_text(encoding='utf-8')
    atom = re.sub(r'<link ([^>]*)/>', r'<link \1></link>', atom)
    atom = atom.replace(
        '</updated><entry>',
        '</updated><subtitle></subtitle><entry>',
        1,
    )
    atom = re.sub(r'<category term="[^"]*"/>', '', atom)
    atom_path.write_text(atom, encoding='utf-8')


def register():
    signals.finalized.connect(preserve_legacy_feeds)
