import typing as t

import feedparser


def get_article_links_from_rss(rss_url: str) -> t.Set[str]:
    return set(entry.link for entry in feedparser.parse(rss_url).entries)
