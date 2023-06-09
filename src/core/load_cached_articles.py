import typing as t
import os


def load_cached_articles(saved_articles_file) -> t.Set[str]:
    if not os.path.exists(saved_articles_file):
        return set()

    with open(saved_articles_file, 'rt', encoding='utf-8') as file:
        return set(line.strip() for line in file.readlines())