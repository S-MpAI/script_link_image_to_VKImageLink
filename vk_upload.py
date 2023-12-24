from modules.User import User
import json
user = User()
def vk_uploader(file_name, dir_):
    """
        Загружает изображение на стену пользователя ВКонтакте и возвращает прямую ссылку на него.

        Аргументы:
            file_name (str): Имя файла для загрузки.
            dir_ (str): Директория, в которой находится файл.

        Возвращает:
            str: Прямая ссылка на загруженное изображение.
    """
    photo = user.picture_send(file_name, dir_)
    post_id = user.make_post(photo)['post_id']

    data = user.groups_getOnTheWallCustom(post_id)
    link = data['attachments'][0]['photo']['sizes'][-1]['url']
    vk_delete_post(post_id)
    return str(link)

def vk_delete_post(post_id):
    """
        Удаляет пост пользователя ВКонтакте по указанному идентификатору.

        Аргументы:
            post_id (int): Идентификатор поста.

        Возвращает:
            None
    """
    user.delete_post(post_id)
