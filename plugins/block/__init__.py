from pelican import signals
from pelican.contents import Article
from pelican.generators import ArticlesGenerator
from pelican.writers import Writer
import os
from copy import deepcopy
import logging
import markdown

logger = logging.getLogger(__name__)

PREFIX = "[BLOCK]"

def write_blocked_articles(generator: ArticlesGenerator, writer: Writer):
    for article in generator.articles:
        blocked_country = article.metadata.get('blocked_country')
        blocked_content = article.metadata.get('blocked_content_override')
        logger.debug("%s Processing article %s", PREFIX, article.slug)
        logger.debug("%s Article metadata: %s", PREFIX, article.metadata)

        if not blocked_country or not blocked_content:
            logger.debug("%s No blocked country or content override found for %s", PREFIX, article.slug)
            continue
        
        if not blocked_content.strip().startswith("<"):
            blocked_content = markdown.markdown(blocked_content)

        logger.debug("%s Writing blocked content for %s: %s", PREFIX, article.slug, blocked_content)

        base_dir = os.path.dirname(article.save_as)
        new_filename = "index_{}.html".format(blocked_country)
        alt_save_as = os.path.join(base_dir, new_filename)
        alt_url = os.path.join(os.path.dirname(article.url), new_filename)

        context = generator.context.copy()
        context.update({
            'article': article,
            'content': blocked_content,
            'blocked_country': blocked_country,
        })

        article.blocked_content = blocked_content

        writer.write_file(
            alt_save_as,
            generator.get_template(article.template),
            context,
            article=article,
            category=article.category,
            override_output=True,
            relative_urls=generator.settings.get('RELATIVE_URLS'),
            url=alt_url,
            save_as=alt_save_as,
        )
        


        

def register():
    signals.article_writer_finalized.connect(write_blocked_articles)
