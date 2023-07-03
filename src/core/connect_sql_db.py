import sqlite3
from sqlite3 import Connection


def connect_sql_db() -> Connection:
    with sqlite3.connect('db.sqlite') as conn:
        cur = conn.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS article_resource(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        href TEXT
        )""")

        cur.execute("""CREATE TABLE IF NOT EXISTS article_links(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        href TEXT,
                        slug TEXT,
                        published_dt TEXT,
                        article_resource_id INTEGER,
                        parsed_dt TEXT,
                        article_archive_file_version REAL,
                        article_archive_file_path TEXT,
                        FOREIGN KEY (article_resource_id) REFERENCES article_resource (id)
        )""")
    return conn
