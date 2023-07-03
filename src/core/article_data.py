import typing as t
from datetime import datetime

from dateutil.tz import gettz


class ArticleData(t.NamedTuple):
    slug: str
    dt: datetime
    title: str
    text: str
    language: str
    keywords: list
    picture_href: str
    picture_bytes: bytes
    href: str

    def serialize_to_json(self) -> t.Dict[str, t.Any]:
        return {
            'title': self.title,
            'text': self.text,
            'publication_dt': self.dt.isoformat(' ', "seconds"),
            'parsing_dt': datetime.now(gettz()).isoformat(' ', 'seconds'),
            'meta_keywords': self.keywords,
            'language': self.language,
            'href': self.href,
        }
