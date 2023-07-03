import typing as t
from sqlite3 import Connection


def load_cached_articles(db_conn: Connection) -> t.Set[str]:
    cur = db_conn.cursor()
    cur.execute('SELECT href FROM article_links')
    article_links_from_db = cur.fetchall()
    return set(link[0] for link in article_links_from_db)
