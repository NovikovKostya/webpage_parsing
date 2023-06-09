import typing as t


def save_cached_articles(saved_articles_file, links: t.Set[str]) -> None:
    with open(saved_articles_file, 'wt', encoding='utf-8') as file:
        file.writelines(f'{i}\n' for i in sorted(links))