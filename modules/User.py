import json
import requests
import vk_api
import os


if str(os.name) == "nt":dir_pref = "\\"
else:dir_pref = "/"

def captcha_handler(captcha):
    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)

def auth_handler():
    key = input("Enter authentication code: ")
    remember_device = True
    return key, remember_device


class User:
    """
        docstring forUser.

        Чтение конфигурации из файла
    """

    def __init__(self, file=rf'config.json'):
        with open(file) as f:data = json.load(f)

        self.user_id = data['user_id']
        self.group_id = data['group_id']
        self.token = data['token']

        self.login = data['login']
        self.passwd= data['password']
        if data['auth_token'] == 1:
            self.vk = vk_api.VkApi(token = self.token)
        else:
            self.vk = vk_api.VkApi(
                                    self.login, self.passwd,
                                    captcha_handler=captcha_handler,
                                    auth_handler = auth_handler,
                                    app_id=6287487)
            self.vk.auth()
        self.v = data['v']


    def picture_send(self, image_to_send, working_directory):
        do = os.getcwd()
        os.chdir(working_directory)
        a = self.vk.method('photos.getWallUploadServer', {'v': self.v})
        b = requests.post(a['upload_url'], files={
                          'photo': open(image_to_send, 'rb')}).json()
        if b['photo'] == '':
            b['photo'] = image_to_send
        c = self.vk.method('photos.saveWallPhoto', {
            'photo': b['photo'], 'server': b['server'], 'hash': b['hash'], 'v': self.v})[0]
        d = f'photo{c["owner_id"]}_{c["id"]}'
        os.chdir(do)
        return d


    def make_post(self, attachments):
        self.post_text = ''
        
        
        self.vk.method('account.setOnline', {'v': self.v})
        id_ = self.vk.method('wall.post', {
                                           'owner_id': -self.group_id,
                                           'message': self.post_text,
                                            'attachments': attachments,
                                            'from_group': 1,
                                            'signed': 0,
                                            'v': self.v})
        
        return id_
    
    def delete_post(self, post_id):
        self.vk.method('account.setOnline', {'v': self.v})
        status = self.vk.method('wall.delete', {
                                           'owner_id': -self.group_id,
                                           'post_id' : post_id,
                                            'v': self.v
                                            })
        return status    



    def groups_getOnTheWallCustom(self, post_id):
        post_ = self.vk.method('wall.getById', {'posts': f'-{self.group_id}_{post_id}','v': self.v})[0]
        return post_