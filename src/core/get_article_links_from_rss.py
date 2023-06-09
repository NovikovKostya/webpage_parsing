import feedparser
import typing as t


def get_article_links_from_rss(rss_url) -> t.List[str]:
    return [entry.link for entry in feedparser.parse(rss_url).entries]