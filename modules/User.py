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
# from user_functions import *
def captcha_handler(captcha):
    """ При возникновении капчи вызывается эта функция и ей передается объект
        капчи. Через метод get_url можно получить ссылку на изображение.
        Через метод try_again можно попытаться отправить запрос с кодом капчи
    """

    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()

    # Пробуем снова отправить запрос с капчей
    return captcha.try_again(key)

def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция.
    """

    # Код двухфакторной аутентификации
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device
token = 'vk1.a.nM5nelhJ3Pz_5xxZiOHewLGZgwvhbQVdNGc92CAC8eYUwuMpdSZ9Q8j4Cn-8sXOQwufKAz0nDKh9i93xVWKyONNoYl4uBw4hDYJzFcaf9VwAee3x3fKwxEgGK0v8QO7qJj8PWCIoxWBHapzJeevvrNwPeEd2SBRNLtE-Z4bxM3JimERdry-XfKA_uEZMQ1WVgK5zcUsprux5MxUN4-0zcQ'
token_I = 'vk1.a.KEUma3WGK5BSfWeRk1Ie8JGsoX6gJU2_18zX344bQKvwpnWU1BoikZHSoL92Yk9yl9FeEwcupAXQ3q8O0fDiaIlVhWapz6uCnMSOZ6K53fHHV_0PQ40wd8029Q08aUFfBLOmH7Q82QuC7-LuhfqcWWNxzhc2wgsACxjah3QbhDrzkXyBboU141iYA2D42DxMf-dOseqlLgHHYg1e7bZMow'
tiken_ = 'https://oauth.vk.com/blank.html#access_token=vk1.a.KEUma3WGK5BSfWeRk1Ie8JGsoX6gJU2_18zX344bQKvwpnWU1BoikZHSoL92Yk9yl9FeEwcupAXQ3q8O0fDiaIlVhWapz6uCnMSOZ6K53fHHV_0PQ40wd8029Q08aUFfBLOmH7Q82QuC7-LuhfqcWWNxzhc2wgsACxjah3QbhDrzkXyBboU141iYA2D42DxMf-dOseqlLgHHYg1e7bZMow&expires_in=0&user_id=435600030&email=malayski51@gmail.com'


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
        self.token = data['token_osnova']
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
        # self.vk = vk_api.VkApi(token = 'vk1.a.26MUxXY_g2LYCKd8tO3eCoshh66FmNXvI1Rip1g9gaShmPX0ilLxxX8-Yj6BJY4e1YFphHBCtX4duDxxxCwuSr4V3gzX-W26Z2GSLSF7VS7iMNLV-O94kmklQaDGWrCz17ptWWJpWO7ev3OatYC85AcLceRodvp2FWR8oxF07TokW-htO4nDj7rTL-YR2m64nok0xx3MwRFY8l57uzmksQ') # group_my
        # self.vk = vk_api.VkApi(token = 'vk1.a.ToI3W7kyz30Dj3fkkDMdOh8Jrc64-TGY6uHZBH3HKHUN0jUU4cxTW8lAMXjLcAOIn2L83JMNIWFRn7D29qW2aBA5Wz3kj0Jy7lWbeigidzfRCxoQaYtyPTGhhUe8zdtMjC0v6LbGr5YwNWx7zI90olF_uT1eDYNoyaZZyyAimR2GLNwaUOUBWj1VTSZDlxFt2OxOqma_wcnuReNttlm8LQ') # group_not_my
        # self.vk = vk_api.VkApi(token = 'vk1.a.mqVZu_zfhmCe2z49gVRNvCCo6X_GIyxVGTs7XepImnZHVmNirjBhtuqm8dttt-f537LNbzI5Yac27SqSbGyb03LV95jzsy9CQh0GaG91goEzKD7bKQPPKfB-TWtN1JbO2nOp4YA7JhQZTZTV_lIpiwS0wTGwCZBL9-H37I24EsUKsOfvDUF_E-usElOU7PzJtfO3D-wB-45bjOjgC2GPhg') # user
        # self.vk = vk_api.VkApi(token = 'vk1.a.7nz5gbKAIAex0GvTXHyhiDdPRJSzPdidh3JmZjyT1E2wDba_WtvDuwMaYhAp8_cy92Lr2w1V9IivdRkiq2xuW0RgjUJGrAA92retWu-6ToVcVoh6wZ2hIjiFjb_3a0qKoh4BivEjNN_zy-r_Ti2SgShnw6iV4wmSRZEBQV2T1wv_eurgQTMG9387IckK4kxDHYVSaIIBodWNd8efTbAAtQ') # user + messages
        self.v = data['v']

    """
        Добавить в друзья все заявки
    """

    def add_all_to_friends(self):
        for request_to_friends in self.vk.method('friends.getRequests', {'out': 0, 'v': self.v})['items']:
            try:
                self.vk.method('friends.add', {
                               'user_id': request_to_friends, 'v': self.v})
            except:
                pass

    """
        Отписаться от всех заявок
    """

    def friends_deny_request(self):
        for request_to_friends in self.vk.method('friends.getRequests', {'out': 1, 'v': self.v})['items']:
            try:
                self.vk.method('friends.delete', {
                               'user_id': request_to_friends, 'v': self.v})
            except:
                pass

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

    """
        Репост последнего поста из группы
        (если есть закреп - то предпоследнего)
    """

    def repost_last_post(self):
        post = self.vk.method(
            'wall.get', {'owner_id': -self.group_id, 'count': 1, 'filter': 'owner', 'v': self.v})['items'][0]
        if 'is_pinned' in post:
            post = self.vk.method('wall.get', {
                                  'owner_id': -self.group_id, 'offset': 1, 'count': 1, 'filter': 'owner', 'v': self.v})['items'][0]
        owner_id = post['owner_id']
        post_id = post['id']
        self.vk.method('wall.repost', {
                       'object': f'wall{owner_id}_{post_id}', 'v': self.v})
        return post_id

    """
        Проверка наличия идентификатора поста в базе данных
    """

    def check_in_db(self, id):
        conn = sqlite3.connect("posts.db")
        cursor = conn.cursor()
        try:
            cursor.execute('CREATE TABLE posts (id text)')
        except:
            pass
        sql = "SELECT * FROM posts WHERE id=?"
        cursor.execute(sql, [(id)])
        res = cursor.fetchall()
        if res:
            return 1
        else:
            return 0

    """
        Добавление идентификатора поста в базу данных
    """

    def add_in_db(self, id):
        conn = sqlite3.connect("posts.db")
        cursor = conn.cursor()
        try:
            cursor.execute("""CREATE TABLE posts (id text)""")
        except:
            pass
        cursor.execute("""INSERT INTO posts (id) VALUES (?)""", (id,))
        conn.commit()
        return 0

    """
        Добавление водяного знака
    """

    def add_watermark(self, img):
        picture = Image.open(img)
        watermark = Image.open(self.watermark_img).convert("RGBA")
        width, height = watermark.size
        picture.paste(watermark, (0, 0, width, height),  watermark)
        picture.save(img)

    """
        Получает случайный пост со стены группы из списка
    """

    def get_random_post(self):
        while True:
            donor_id = random.choice(self.donors)
            count = self.vk.method(
                'wall.get', {'owner_id': donor_id, 'v': self.v})['count']
            post = self.vk.method('wall.get', {'owner_id': donor_id, 'offset': random.randint(
                2, count - 1), 'count': 1, 'filter': 'owner', 'v': self.v})['items'][0]
            donor_post_id = post['id']
            text = post['text'].lower()
            if any(word in text for word in self.stop_words):
                continue
            if post['marked_as_ads']:
                continue
            if self.sqlog:
                if self.check_in_db(f'{donor_id}_{donor_post_id}'):
                    continue
            attachments = ''
            for attachment in post['attachments']:
                if attachment['type'] == 'photo':
                    photo = attachment['photo']
                    url = photo['sizes'][-1]['url']
                    file = url.split('/')[-1]
                    urllib.request.urlretrieve(url, file)
                    if self.watermark:
                        self.add_watermark(file)
                    attachments += self.picture_send(file) + ','
                    os.remove(file)
                if attachment['type'] == 'audio':
                    audio = attachment['audio']
                    attachments += f'audio{audio["owner_id"]}_{audio["id"]},'
                if attachment['type'] == 'audio_playlist':
                    audio_playlist = attachment['audio_playlist']
                    attachments += f'audio_playlist{audio_playlist["owner_id"]}_{audio_playlist["id"]},'
                if attachment['type'] == 'video':
                    video = attachment['video']
                    attachments += f'video{video["owner_id"]}_{video["id"]},'
                if attachment['type'] == 'doc':
                    doc = attachment['doc']
                    attachments += f'doc{doc["owner_id"]}_{doc["id"]},'
            if not attachments:
                continue
            break
        return {'donor_id': donor_id, 'donor_post_id': donor_post_id, 'attachments': attachments, 'text': text}

    """
        Пост в группу
    """

    def make_post(self, attachments):
        self.post_text = ''#str(random.choice(["Тут должен быть текст, но его забыли сюда вставить.", "" ]))

        self.vk.method('account.setOnline', {'v': self.v})
        id_ = self.vk.method('wall.post', {
                                           'owner_id': -self.group_id,
                                           'message': self.post_text, #+ f'\n\n\nИсточник: @club{abs(donor_id)}({donor})',
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

    def groups_getSettings(self, group_id):
        group_id = self.group_id
        groups_Settings = self.vk.method('groups.getSettings', {'group_id': group_id,'v': self.v})
        groups_Settings['description'] = str(groups_Settings['description']).encode('unicode-escape').decode('unicode-escape')
        description = str(groups_Settings['description']).encode('unicode-escape').decode('unicode-escape')
        name = str(groups_Settings['title']).encode('unicode-escape').decode('unicode-escape')
        address = groups_Settings['address']
        return address, name, description, group_id

    def groups_getOnTheWallCustom(self, post_id):
        post_ = self.vk.method('wall.getById', {'posts': f'-{self.group_id}_{post_id}','v': self.v})[0]
        return post_
        


    def groups_getOnTheWall(self):
        post_ = self.vk.method('wall.getById', {'posts': f'-{self.group_id}_{22}','v': self.v})[0]
        post_['text'] = str(post_['text']).encode('unicode-escape').decode('unicode-escape')
        oss_ = os.getcwd()
        os.chdir(f'modules{dir_pref}jsons{dir_pref}')
        with open("groups_getOnTheWall.json", "w") as outfile:json.dump(post_, outfile, indent=4)
        os.chdir(oss_)
        return post_['text']  
    




    def groups_setDescription(self, group_id, description):
        self.vk.method('groups.edit', {'group_id': group_id,'v': self.v, 'description': description})
        # print(groups_Settings)

    def account_getAppPermissions(self, user_id):

        ass_ = self.vk.method('account.getAppPermissions', {'user_id': user_id,'v': self.v})
        print(ass_)

    def send_message(self, message, type_ch, attachment = None):
        # baseda = 136
        # logs__ = 135
        if type_ch == 'beseda':
            chat_id = 2000000136
        else:
            if type_ch == 'logs':
                chat_id = 2000000135
        # chat_id = self.vk.method("messages.searchConversations", {"q": 'База Неко | Логи', "count": 1})['items'][0]['peer']['id']
        # chat_id = self.vk.messages.searchConversations(q='База Неко | Логи', count=1)['items'][0]['peer']['local_id']
        # print(chat_id)
        if attachment != None:
            self.vk.method("messages.send", {"peer_id": chat_id, "message": message, "attachment": attachment, "random_id": 0})
        else:
            # self.vk.method("messages.send", {"peer_id": id, "message": message, "random_id": 0})
            self.vk.method("messages.send", {"peer_id": chat_id, "message": message, "attachment": attachment, "random_id": random.randint(-3254672,32546547)})

    def set_status(self, status):
        self.vk.method("status.set", {"text": status, 'group_id': self.group_id})

    def groups_set_on_the_wall(self, info):
        self.vk.method('wall.edit', {'owner_id': f'-{self.group_id}',
                                     'post_id': 22,
                                     'v': self.v,
                                     'message': info,
                                     'friends_only': 0,
                                     'attachments': []})

    def repost_wall(self, post_id):
        self.send_message('Вышел новый арт в группе!', 'beseda', f'wall-{self.group_id}_{post_id}')

    def account_getProfileInfo(self):
        q = self.vk.method('account.getProfileInfo', {'v': self.v})
        oss_ = os.getcwd()
        
        os.chdir(f'modules{dir_pref}jsons{dir_pref}')
        with open("account_getProfileInfo.json", "w") as outfile:json.dump(q, outfile, indent=4)
        os.chdir(oss_)
        if q['verification_status'] == 'verified': q['verification_status'] = "✅ (verified)"
        else:q['verification_status'] = "❌ (not verified)"
        return [q['id'], q['first_name'], q['last_name'], q['screen_name'], q['status'], q['verification_status']]
        print(q)

    def notifications_get(self):
        q = self.vk.method('notifications.get', {'v': self.v,
                                                 'count': 2})
        oss_ = os.getcwd()
        os.chdir(f'modules{dir_pref}jsons{dir_pref}')
        with open(f"notifications_get.json", "w") as outfile:json.dump(q, outfile, indent=4)
        os.chdir(oss_)
        print(q)
        pass


    def notifications_sendMessage(self):
        q = self.vk_servise_auth.method('notifications.sendMessage',
                                                 {'v': self.v,
                                                  'user_ids': 435600030,
                                                 'message': 'Типо тестовое сооющение в уведомлениях',
                                                 'group_id': 223280125,
                                                 'fragment': 'vk.com/app123456#LOL'})
        print(q)

    def secure_checkToken(self):
        q = self.vk_servise_auth.method('secure.checkToken',
                                                 {'v': self.v,
                                                  'token': self.servise_auth_token})
        print(q)

    def secure_sendSMSNotification(self):
        q = self.vk_servise_auth.method('secure.sendSMSNotification',
                                                 {'v': self.v,
                                                  'user_id': 435600030,
                                                  'message': 'This message has been sent successfully to the server and will be sent to the server again in the next 24 hours.'})
        print(q)

