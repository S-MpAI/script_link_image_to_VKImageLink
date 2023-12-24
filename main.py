import os
import json
from modules.random_neko_list import imgs, imgs18
from py_upload import upload_to_server
from vk_upload import vk_uploader
from downloader import DDF

w_dir = os.getcwd()

def process_image_links(img_links, access_list, block_list):
    """
    Обрабатывает список изображений, загружая их на сервер VK или PythonAnywhere.

    Аргументы:
        img_links (list): Список ссылок на изображения.
        access_list (list): Список разрешенных расширений изображений.
        block_list (list): Список запрещенных расширений изображений.

    Возвращает:
        list: Список новых ссылок на изображения VK.
    """
    append_ = []
    not_append_ = []
    NewVKLinks = []
    o = 0

    for link in img_links:
        if type(link) == dict:
            pass
        else:
            if link not in ['imgs', 'imgs18']:
                if str(link.split('/')[2]) not in ['i.pinimg.com', 'i.pximg.net']:
                    if 'https://sun' not in str(link):
                        if list(link.split('.'))[-1] in access_list:
                            if not os.path.exists('VK_'):
                                os.mkdir('VK_')
                            os.chdir('VK_')
                            name_file = DDF(link, o)
                            os.chdir(w_dir)
                            link = vk_uploader(name_file, 'VK_')
                            NewVKLinks.append(link)
                        elif list(link.split('.'))[-1] in block_list:
                            if not os.path.exists('PY'):
                                os.mkdir('PY')
                            os.chdir('PY')
                            name_file = DDF(link, o)
                            upload_to_server(name_file)
                            o = o + 1
                            os.chdir(w_dir)
                else:
                    NewVKLinks.append(link)

            if 'imgs' == link:
                append_.append(link)
            if 'imgs18' == link:
                append_.append(link)

    return NewVKLinks

count_imgs = len(imgs)
count_imgs18 = len(imgs18)

NewVKLinks = process_image_links(imgs18, ['jpg', 'png', 'jpeg'], ['mp4', 'gif', 'webm'])
with open("NewVKLinks.json", "w") as outfile:
    json.dump(NewVKLinks, outfile, indent=4)
