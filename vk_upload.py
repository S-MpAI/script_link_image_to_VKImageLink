from modules.User import User
import json
user = User()
def vk_uploader(file_name, dir_):
    photo = user.picture_send(file_name, dir_)
    post_id = user.make_post(photo)['post_id']

    data = user.groups_getOnTheWallCustom(post_id)
    link = data['attachments'][0]['photo']['sizes'][-1]['url']
    vk_delete_post(post_id)
    return str(link)

def vk_delete_post(post_id):
    user.delete_post(post_id)