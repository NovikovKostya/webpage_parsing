import importlib
import logging
import typing as t
from urllib.parse import urlparse

from src.core.connect_sql_db import connect_sql_db
from src.core.parse_resource import parse_resource

logger = logging.getLogger(__name__)


def parse_rss_feeds(feeds: t.List[str]) -> None:
    conn = connect_sql_db()
    cur = conn.cursor()
    for feed in feeds:
        resource_url = f'{urlparse(feed).scheme}://{urlparse(feed).netloc}'
        cur.execute('SELECT href FROM article_resource WHERE href = ?', (resource_url,))
        if not cur.fetchone():
            cur.execute('INSERT INTO article_resource (href) VALUES (?)', (resource_url,))
            conn.commit()
        try:
            if resource_url.count('.') == 2:
                resource_name = resource_url[resource_url.find('.') + 1:resource_url.rfind('.')]
            else:
                resource_name = resource_url[:resource_url.rfind('.')]
            module = importlib.import_module(f'src.resources.{resource_name}')
            parse_resource(module, feed, resource_name, conn)
        except ModuleNotFoundError:
            logger.info(f'There is no option to parse data from this resource: {feed}')
            continue
    conn.close()
