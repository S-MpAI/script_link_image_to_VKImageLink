import unicodedata
import urllib.request
from PIL import Image
import random
import sqlite3
import json
import requests
import vk_api
import os


if str(os.name) == "nt":dir_pref = "\\"
else:dir_pref = "/"


def captcha_handler(captcha):
    """ При возникновении капчи вызывается эта функция и ей передается объект
        капчи. Через метод get_url можно получить ссылку на изображение.
        Через метод try_again можно попытаться отправить запрос с кодом капчи
    """

    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()

    return captcha.try_again(key)

def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция.
    """

    # Код двухфакторной аутентификации
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device

class User:
    """
        docstring forUser.

        Чтение конфигурации из файла
    """

    def __init__(self, file=rf'modules{dir_pref}config.json'):
        with open(file) as f:
            data = json.load(f)

        self.user_id = data['user_id']
        self.group_id = data['group_id']
        self.post_text = data['post_text']
        self.donors = data['donors']
        self.stop_words = data['stop_words']
        self.add_friends = data['add_friends']
        self.del_requests = data['del_requests']
        self.repost = data['repost']
        self.watermark = data['watermark']
        self.watermark_img = data['watermark_img']
        self.time_to_start_script = data['time_to_start_script']
        self.time_sleep = int(data['time_sleep'])
        self.sqlog = data['sqlog']
        self.token = data['token']
        self.servise_auth_token= data['service']

        self.login = data['login']
        self.passwd= data['password']
        if data['auth_token'] == 1:
            self.vk = vk_api.VkApi(token = self.token) # user + messages
        else:
            self.vk = vk_api.VkApi(
                                    self.login, self.passwd,
                                    captcha_handler=captcha_handler,
                                    auth_handler = auth_handler,
                                    app_id=2685278) #all - 6287487, my - 2685278
            self.vk.auth()
        self.vk_servise_auth = vk_api.VkApi(token = self.servise_auth_token)
        self.v = data['v']



    """
        Загрузка изображения на сервер и получение объекта photo
    """

    def picture_send(self, image_to_send, working_directory):
        do = os.getcwd()
        os.chdir(working_directory)
        a = self.vk.method('photos.getWallUploadServer', {'v': self.v})
        b = requests.post(a['upload_url'], files={
                          'photo': open(image_to_send, 'rb')}).json()
        c = self.vk.method('photos.saveWallPhoto', {
            'photo': b['photo'], 'server': b['server'], 'hash': b['hash'], 'v': self.v})[0]
        d = f'photo{c["owner_id"]}_{c["id"]}'
        os.chdir(do)
        return d
