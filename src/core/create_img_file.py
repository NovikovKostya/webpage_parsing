from src.core.article_data import ArticleData


def create_img_file(tmpdir_path: str, article_info: ArticleData) -> str:
    pic_format = article_info.picture_href[article_info.picture_href.rfind('.') + 1:]
    with open(f'{tmpdir_path}/header_pic.{pic_format}', 'wb') as img_file:
        img_file.write(article_info.picture_bytes)
    return img_file.name
