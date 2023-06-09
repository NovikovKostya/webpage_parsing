def check_article_status_code(article_response) -> bool:
    return article_response.status_code // 100 == 2