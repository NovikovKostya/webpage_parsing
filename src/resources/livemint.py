import json
import logging

from bs4 import BeautifulSoup
from cfscrape import CloudflareScraper
from dateutil.parser import parse

from src import core

logger = logging.getLogger(__name__)
parser_version = 1.0


@core.check_element_exist
def get_title(soup: BeautifulSoup, article_link: str):
    return soup.find('h1').text


@core.check_element_exist
def get_text(soup: BeautifulSoup, article_link: str):
    return ' '.join([i.text.strip() for i in soup.find('div', class_='mainArea').findAll('p')])


@core.check_element_exist
def get_picture_href(soup: BeautifulSoup, article_link: str):
    return soup.find('span', class_='pos-rel dblock imgmobalignment').find('img').get('src')


@core.check_element_exist
def get_date(soup: BeautifulSoup, article_link: str):
    return parse(soup.find('meta', attrs={'property': 'article:published_time'}).get('content'))


@core.check_element_exist
def get_keywords(soup: BeautifulSoup, article_link: str):
    return soup.find('meta', attrs={'name': 'keywords'}).get('content')


def create_json_file(tmpdir_path: str, article_info: core.ArticleData) -> str:
    with open(f'{tmpdir_path}/data.json', 'w+t', encoding='utf-8') as json_file:
        json.dump(article_info.serialize_to_json(), json_file, indent=4)
    return json_file.name


def get_article_data(scrapper: CloudflareScraper, article_link: str, soup: BeautifulSoup) -> core.ArticleData:
    article_title = get_title(soup, article_link)
    article_text = get_text(soup, article_link)
    article_pic_href = get_picture_href(soup, article_link)
    article_date = get_date(soup, article_link)
    article_keywords = get_keywords(soup, article_link)

    return core.ArticleData(
        slug=article_link[article_link.rfind(str('/')) + 1:article_link.rfind('.')],
        title=article_title,
        dt=article_date,
        text=article_text,
        language='en',
        keywords=article_keywords.split(','),
        picture_href=article_pic_href,
        picture_bytes=scrapper.get(article_pic_href).content if article_pic_href else '',
        href=article_link,
    )


