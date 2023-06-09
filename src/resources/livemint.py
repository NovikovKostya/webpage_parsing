import json
import logging
import os
import tempfile
import typing as t
from datetime import datetime

import cfscrape
from bs4 import BeautifulSoup
from dateutil.parser import parse
from dateutil.tz import gettz

from src import core

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG, datefmt='%I:%M:%S')

RSS_FILE_URL = 'https://www.livemint.com/rss/news'

PARSED_ARTICLES_DIR = os.path.join('data', 'parse_livemint')
os.makedirs(PARSED_ARTICLES_DIR, exist_ok=True)

ALREADY_LOADED_ARTICLES_DB_FILE = os.path.join(PARSED_ARTICLES_DIR, 'list_of_articles.txt')


class ArticleData(t.NamedTuple):
    slug: str
    dt: datetime
    title: str
    text: str
    keywords: list
    picture_href: str
    picture_bytes: bytes
    href: str


@core.check_element_exist
def get_title(soup, article_link):
    return soup.find('h1').text


@core.check_element_exist
def get_text(soup, article_link):
    return ' '.join([i.text.strip() for i in soup.find('div', class_='mainArea').findAll('p')])


@core.check_element_exist
def get_picture_href(soup, article_link):
    return soup.find('span', class_='pos-rel dblock imgmobalignment').find('img').get('src')


@core.check_element_exist
def get_date(soup, article_link):
    return parse(soup.find('meta', attrs={'property': 'article:published_time'}).get('content'))


@core.check_element_exist
def get_keywords(soup, article_link):
    return soup.find('meta', attrs={'name': 'keywords'}).get('content')


def create_json_file(tmpdirname, article_info) -> str:
    with open(os.path.join(tmpdirname, 'data.json'), 'w+t', encoding='utf-8') as json_file:
        json.dump({
            'title': article_info.title,
            'text': article_info.text,
            'publication_dt': article_info.dt.isoformat(' ', "seconds"),
            'parsing_dt': datetime.now(gettz()).isoformat(' ', 'seconds'),
            'meta_keywords': article_info.keywords,
            'href': article_info.href,
        }, json_file, indent=4)
    return json_file.name


def get_article_data(scrapper, article_link, soup: BeautifulSoup) -> ArticleData:
    article_title = get_title(soup, article_link)
    article_text = get_text(soup, article_link)
    article_pic_href = get_picture_href(soup, article_link)
    article_date = get_date(soup, article_link)
    article_keywords = get_keywords(soup, article_link)

    return ArticleData(
        slug=article_link[article_link.rfind(str('/')) + 1:article_link.rfind('.')],
        title=article_title,
        dt=article_date,
        text=article_text,
        keywords=article_keywords.split(','),
        picture_href=article_pic_href,
        picture_bytes=scrapper.get(article_pic_href).content if article_pic_href else '',
        href=article_link,
    )

def parsing(rss_file_url) -> None:
    all_article_links = core.get_article_links_from_rss(rss_file_url)
    old_article_links = core.load_cached_articles(ALREADY_LOADED_ARTICLES_DB_FILE)
    new_article_links = set(filter(lambda x: x not in old_article_links, all_article_links))
    successfully_saved_links = set()
    logger.info(f'Count articles for parsing: {len(new_article_links)}')
    scrapper = cfscrape.create_scraper()

    try:
        for article_link in new_article_links:
            logger.info(f'Process article "{article_link}"')
            article_response = scrapper.get(article_link)
            if not core.check_article_status_code(article_response):
                logger.error(f'{article_link} response status code not 2xx')
                continue

            soup = BeautifulSoup(article_response.text, 'lxml')
            article_info = get_article_data(scrapper, article_link, soup)

            files_to_archive = []
            with tempfile.TemporaryDirectory() as tmpdirname:
                files_to_archive.append(core.create_html_file(tmpdirname, article_response))
                files_to_archive.append(create_json_file(tmpdirname, article_info))
                if article_info.picture_bytes:
                    files_to_archive.append(core.create_img_file(tmpdirname, article_info))

                core.archive_files(PARSED_ARTICLES_DIR, article_info.slug, files_to_archive)
                successfully_saved_links.add(article_link)

        core.save_cached_articles(ALREADY_LOADED_ARTICLES_DB_FILE, old_article_links.union(successfully_saved_links))
        logger.info(f'Count articles for saving: {len(successfully_saved_links)}')
    except KeyboardInterrupt:
        core.save_cached_articles(ALREADY_LOADED_ARTICLES_DB_FILE, old_article_links.union(successfully_saved_links))
        logger.info(f'Keyboard interrupt.Count articles for saving: {len(successfully_saved_links)}')
