import os


def create_html_file(tmpdirname, article_response) -> str:
    with open(os.path.join(tmpdirname, 'article.html'), 'w', encoding='utf-8') as html_file:
        html_file.write(article_response.text)
    return html_file.name