from pelican import signals
import os
import logging
import markdown

logger = logging.getLogger(__name__)

def patch_blocked_override(generator):
    generator.blocked_variants = []

    for article in list(generator.articles):
        blocked_country = article.metadata.get('blocked_country')
        blocked_content = article.metadata.get('blocked_content_override')

        logger.debug("Processing article %s", article.slug)
        logger.debug("Article metadata: %s", article.metadata)

        if not blocked_country or not blocked_content:
            logger.debug("Article %s does not have blocked_country or blocked_content_override metadata.", article.title)
            continue

        logger.debug("Article %s has blocked_country: %s", article.title, blocked_country)

        if not blocked_content.strip().startswith("<"):
            blocked_content = markdown.markdown(blocked_content)

        article.blocked_country = blocked_country
        article.blocked_content_override = blocked_content
        generator.blocked_variants.append(article)

    logger.info("Found %d articles with blocked_country override", len(generator.blocked_variants))


def write_blocked_override(generator, writer):
    for article in getattr(generator, 'blocked_variants', []):
        blocked_country = article.blocked_country
        blocked_content = article.blocked_content_override

        if not blocked_content.strip().startswith("<"):
            blocked_content = markdown.markdown(blocked_content)

        logger.debug("Writing blocked_country variant for %s", article.slug)
        logger.debug("Blocked content: %s", blocked_content)

        # Derive path: 'slug/index_{blocked_country}.html'
        base_dir = os.path.dirname(article.save_as)
        new_filename = "index_{blocked_country}.html".format(blocked_country=blocked_country)
        alt_save_as = os.path.join(base_dir, new_filename)
        alt_url = os.path.join(os.path.dirname(article.url), new_filename)

        logger.info("Writing blocked_country variant for %s to %s", article.slug, alt_save_as)

        context = generator.context.copy()

        context.update({
            'article': article,
            'content': blocked_content,
            'blocked_country': blocked_country,
        })

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
    signals.article_generator_finalized.connect(patch_blocked_override)
    signals.article_writer_finalized.connect(write_blocked_override)
