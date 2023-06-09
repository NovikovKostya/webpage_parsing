import os


def create_img_file(tmpdirname, article_info) -> str:
    pic_format = article_info.picture_href[article_info.picture_href.rfind('.') + 1:]
    with open(os.path.join(tmpdirname, f'header_pic.{pic_format}'), 'wb') as img_file:
        img_file.write(article_info.picture_bytes)
    return img_file.name