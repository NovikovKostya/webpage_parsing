import logging
import os
import tempfile
from sqlite3 import Connection

import cfscrape
import feedparser
from bs4 import BeautifulSoup

from src import core

logger = logging.getLogger(__name__)


def parse_resource(module, feed_url: str, resource_name: str, db_conn: Connection) -> None:
    section_name = ''.join([i for i in feedparser.parse(feed_url).feed.title.lower() if i.isalpha()])
    parsed_articles_dir = os.path.join('data', f'parse_{resource_name}', section_name)
    os.makedirs(parsed_articles_dir, exist_ok=True)

    all_article_links = core.get_article_links_from_rss(feed_url)
    old_article_links = core.load_cached_articles(db_conn)
    new_article_links = all_article_links.difference(old_article_links)
    logger.info(f'Count articles for parsing from {resource_name} section {section_name}: {len(new_article_links)}')
    scrapper = cfscrape.create_scraper()

    try:
        for article_link in new_article_links:
            logger.info(f'Process article "{article_link}"')
            article_response = scrapper.get(article_link)
            try:
                article_response.raise_for_status()
            except Exception as e:
                logger.error(e)
                continue

            soup = BeautifulSoup(article_response.text, 'lxml')
            article_info = module.get_article_data(scrapper, article_link, soup)
            parser_version = module.parser_version

            files_to_archive = []
            with tempfile.TemporaryDirectory() as tmpdirname:
                tmpdir_path = os.path.join(tmpdirname)
                files_to_archive.append(core.create_html_file(tmpdir_path, article_response.text))
                files_to_archive.append(module.create_json_file(tmpdir_path, article_info))
                if article_info.picture_bytes:
                    files_to_archive.append(core.create_img_file(tmpdir_path, article_info))

                core.archive_files(parsed_articles_dir, article_info.slug, files_to_archive)
                core.add_data_to_db(article_link, db_conn, article_info, parser_version, parsed_articles_dir)
    except KeyboardInterrupt:
        logger.info(f'Keyboard interrupt. Stop parsing process')
