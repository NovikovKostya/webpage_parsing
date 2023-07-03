import json
import logging
import typing as t

import pytz
from bs4 import BeautifulSoup
from cfscrape import CloudflareScraper
from dateutil.parser import parse

from src import core

logger = logging.getLogger(__name__)
parser_version = 1.0

def remove_tag(*args: t.List) -> None:
    for arg in args:
        for tag in arg:
            tag.decompose()


@core.check_element_exist
def get_title(soup: BeautifulSoup, article_link: str):
    return soup.find('h1').text


@core.check_element_exist
def get_text(soup: BeautifulSoup, article_link: str):
    return ''.join(soup.find('div', class_='WYSIWYG articlePage').findAll(string=True)).strip()


@core.check_element_exist
def get_picture_href(soup: BeautifulSoup, article_link: str):
    return soup.find('div', class_='WYSIWYG articlePage').find('img').get('src')


@core.check_element_exist
def get_language(soup: BeautifulSoup, article_link: str):
    return soup.find('meta', attrs={'http-equiv': 'content-language'}).get('content')


@core.check_element_exist
def get_date(soup: BeautifulSoup, article_link: str):
    pub_date = ''
    for i in soup.select('#leftColumn > div:nth-child(6) > span:nth-child(1)'):
        pub_date = parse(' '.join(i.text.split(' ')[1:-1])).replace(tzinfo=pytz.timezone('EST'))
    return pub_date


def create_json_file(tmpdir_path: str, article_info: core.ArticleData) -> str:
    with open(f'{tmpdir_path}/data.json', 'w+t', encoding='utf-8') as json_file:
        json.dump(article_info.serialize_to_json(), json_file, indent=4)
    return json_file.name


def get_article_data(scrapper: CloudflareScraper, article_link: str, soup: BeautifulSoup) -> core.ArticleData:
    article_title = get_title(soup, article_link)
    remove_tag(soup.find('div', class_='WYSIWYG articlePage').findAll('script'),
               soup.findAll('div', class_='relatedInstrumentsWrapper'),
               soup.find('div', class_='imgCarousel').findAll('span'))
    article_text = get_text(soup, article_link)
    article_pic_href = get_picture_href(soup, article_link)
    article_language = get_language(soup, article_link)
    article_date = get_date(soup, article_link)

    return core.ArticleData(
        slug=article_link[article_link.rfind(str('/')) + 1:],
        title=article_title,
        dt=article_date,
        text=article_text,
        language=article_language,
        keywords=[],
        picture_href=article_pic_href,
        picture_bytes=scrapper.get(article_pic_href).content if article_pic_href else '',
        href=article_link,
    )


