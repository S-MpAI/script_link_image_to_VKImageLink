import os
import time
from modules.ext import NotPostingImages
import random
import requests
import json

username = 'BSNIKChannel'
tn = 'TOKEN'

if str(os.name) == "nt":dir_pref = "\\"
else:dir_pref = "/"

image_exctensions = ['jpeg','jpg','png','gif','tiff']

def information_about_cpu():
    r = requests.get(f'https://www.pythonanywhere.com//api/v0/user/BSNIKChannel/cpu/',headers={'Authorization': f'Token {tn}'}).text
    t = json.loads(r)

    return f'''Общее использование процессора в день (секунды): {round(t["daily_cpu_total_usage_seconds"], 1)}/{t["daily_cpu_limit_seconds"]}
Следующий сброс: {t['next_reset_time'].replace('T',' ')}'''

def prints_in_console():
    a = ''
    r = requests.get(f'https://www.pythonanywhere.com//api/v0/user/{username}/consoles/{int(get_console())}/get_latest_output/',headers={'Authorization': f'Token {tn}'}).text
    r =json.loads(r)

    if r['output'] != '''\r\nPreparing execution environment... OK\r\nSpam, spam, spam, sausage, eggs, spam and spam... OK\r\nLoading Bash interpreter...\u001b[;H\u001b[2J\u001b[0;37m22:03 ~\u001b[0;33m \u001b[1;32m$ \u001b[0;37m\r\u001b[K\u001b[0;37m22:03 ~\u001b[0;33m \u001b[1;32m$ \u001b[0;37m''':
        if '|' in r:
            if 'Время последнего обновления' not in r:
                if '' != r:
                    a = '|' + str(list(r.split('\r'))[-1]).split('|')[-2] + '|' + str(list(r.split('\r'))[-1]).split('|')[-1].replace(' "}', '')
                else:a = 'Консоль в режиме ожидания.'
            else:pass
    else:a = 'Консоль пуста, в режиме ожидания.'
    return a

def get_console():
    r = requests.get(f'https://www.pythonanywhere.com//api/v0/user/{username}/consoles/',headers={'Authorization': f'Token {tn}'}).text
    return json.loads(r)[0]['id']

def get_offset_for_script(sep, length):
    q = 100/sep
    x = q * length / 100
    a = [int(i*x) for i in range(1,sep+1)]
    return a


def set_new_information_in_description(user, s):
    address, name, description, group_id = user.groups_getSettings(user.group_id)
    sep = "-"*15
    if f'{sep}' in str(description):
        description = list(description.split(sep))[0]
        if s == None:
            description_ = description + f'\n\n{sep}\n{information_about_cpu()}'
        else:description_ = description + f'\n\n{sep}\n{s}'
    else:
        if s == None:description_ = description + f'\n\n{sep}\n{information_about_cpu()}'
        else:description_ = description + f'\n\n{sep}\n{s}'
    description_ = description_ + f'\nВремя последнего обновления: {time.strftime("%m.%d.%Y, %H:%M:%S", time.localtime())}\n{prints_in_console()}'
    user.groups_setDescription(group_id, description_)

def set_new_information_on_the_wall(user):
    text = user.groups_getOnTheWall()
    sep = "-"*15
    if f'{sep}' in str(text):
        text = list(text.split(sep))[0]
        text_ = text + f'\n\n{sep}\n{information_about_cpu()}'
    else:
        text_ = text + f'\n\n{sep}\n{information_about_cpu()}'
    user.groups_set_on_the_wall(text_)

def set_new_repost_wall(user, post_id):
       user.send_message('Вышел новый арт в группе!', 'beseda', f'wall-{user.group_id}_{post_id}')


def remove_pictures():
    try:
        os.rmdir('pictures')
    except OSError:
        os.chdir(f'{os.getcwd()}{dir_pref}pictures')
        for entry in os.scandir(os.getcwd()):
            if entry.is_file():
                os.remove(entry.name)




def get_images_in_folder(w_directory):
    pictures = []
    for entry in os.scandir(w_directory):
        if entry.is_file():
            if str(entry.name).split('.')[-1] in image_exctensions:
                    pictures.append(entry.name)

    return pictures


def get_local_ip_address():
    r = requests.get(f'https://api.ipify.org?format=json')
    if r.status_code != 200: return f'ERROR ({r.status_code})'
    return (r.text).split('"')[3]


def check_files(working_dir):
    if os.path.exists(working_dir):
        pictures = []
        print('Нужная папка была найдена.')
        skan = os.scandir(working_dir)
        if len(list(skan)) != 0:
            pictures = get_images_in_folder(working_dir)
            print(f'Количество найденных изображений: {len(pictures)}')
            print(f'{"-"*5}')
            if len(pictures) != 0:return True
            else: return False
        else:
            return False
            # raise NotPostingImages('Нету изображений которые необходимо постить... ')
    else:
        os.mkdir(working_dir)
        print('Нужная папка НЕ была найдена.')
        return False

def get_random_image(working_directory):
    pictures = get_images_in_folder(working_directory)
    picture = random.choice(pictures)

    return picture

if __name__ == '__main__':
    print(f'-{prints_in_console()}-')
