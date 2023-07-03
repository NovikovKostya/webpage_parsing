import typing as t
from datetime import datetime
from sqlite3 import Connection
from urllib.parse import urlparse

from dateutil.tz import gettz

from src.core.article_data import ArticleData


def add_data_to_db(article_link: str, db_conn: Connection, article_info: ArticleData, version: t.Union[int, float],
                   path_to_archive: str) -> None:
    cur = db_conn.cursor()
    article_resource = f'{urlparse(article_link).scheme}://{urlparse(article_link).netloc}'
    cur.execute('SELECT id FROM article_resource WHERE href = ?', (article_resource,))
    resource_id = cur.fetchone()[0]
    attr_for_db = [article_link,
                   article_info.slug,
                   article_info.dt,
                   resource_id,
                   datetime.now(gettz()).isoformat(' ', 'seconds'),
                   version,
                   path_to_archive]
    cur.execute("""INSERT INTO article_links(
    href, slug, published_dt, article_resource_id, parsed_dt, article_archive_file_version, article_archive_file_path)
    VALUES(?, ?, ?, ?, ?, ?, ?) """, attr_for_db)
    db_conn.commit()
