import os
import time
import requests
import shutil

from colorama import Fore, Back, Style

g = Fore.GREEN
r = Fore.RED
b = Fore.BLUE
y = Fore.YELLOW
s = Style.RESET_ALL



username = 'XXYmda3'
token = '50d72b841f3dc14d406a32c1f258d49fdccb6771'
path = f'/home/{username}/'

class ResponseCodeError(Exception):
  """
    Пользовательское исключение для обработки неожиданных кодов ответа во время запросов к API.

    Атрибуты:
        message (str): Опциональное сообщение об ошибке, связанное с исключением.
  """
  def __init__(self, *args):
    if args:self.message = args[0]
    else:self.message = None

  def __str__(self):
    if self.message:return self.message
    else:return "ResponseCodeError has been raised"


def upload_to_server(filename):
                """
    Загружает файл на сервер PythonAnywhere.

    Аргументы:
        filename (str): Имя файла для загрузки.

    Исключения:
        ResponseCodeError: Если код состояния ответа не равен 201 или 200.
                """
                file_name = filename
                w_dir = os.getcwd()
                shutil.copy(f'{w_dir}/{file_name}', f'{w_dir}/content')
                # os.chdir('')
                file = open('content', '+rb')
                get_request(file, file_name)
                time.sleep(5)
                # os.remove('content')
                os.chdir(w_dir)


           


def get_request(file, file_name):
    """
    Выполняет POST-запрос для загрузки файла на сервер PythonAnywhere.

    Аргументы:
        file: Объект файла для загрузки.
        file_name (str): Имя файла.

    Исключения:
        ResponseCodeError: Если код состояния ответа не равен 201 или 200.
    """
    m = f'/api/v0/user/{username}/files/path{path}'
    response = requests.post(f'https://www.pythonanywhere.com/{m}/{file_name}', files={'content': file}, headers={'Authorization': 'Token ' + token})
    # print(response.status_code, response.text)
    if response.status_code == 201:
        print(f'{g}[+] The file named {b}{file_name}{g} was successfully {y}uploaded{g} to the server {b}{username}{g}.{s}')
    elif response.status_code == 200:
        print(f'{g}[+] The file named {b}{file_name}{g} was successfully {y}rewritten{g} to the server {b}{username}{g}.{s}')
    else:
        raise ResponseCodeError(f'[{response.status_code}] Error: {response.text}')


if __name__ == '__main__':
   upload_to_server()
