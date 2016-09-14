from markdown.util import AMP_SUBSTITUTE


# To be understanded by Python-Markdown.
def html_entity(html):
    return html.replace('&', AMP_SUBSTITUTE)
