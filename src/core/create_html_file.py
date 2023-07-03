def create_html_file(tmpdir_path: str, article_html: str) -> str:
    with open(f'{tmpdir_path}/article.html', 'w', encoding='utf-8') as html_file:
        html_file.write(article_html)
    return html_file.name
