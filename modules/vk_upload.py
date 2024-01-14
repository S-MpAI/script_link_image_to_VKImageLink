from modules.User import User
import vk_api
import traceback
user = User()
def vk_uploader(file_name, dir_):
    try:
        photo = user.picture_send(file_name, dir_)
        post_id = user.make_post(photo)['post_id']

        data = user.groups_getOnTheWallCustom(post_id)
        link = data['attachments'][0]['photo']['sizes'][-1]['url']
        vk_delete_post(post_id)
        return str(link), ''
    except vk_api.exceptions.ApiError as e:
        print(traceback.format_exc())
        e = str(e)
        if 'no access_token passed' in e:
            e = 'Access token не введен!'
        return 'Err', e
    except Exception as e:
        print(traceback.format_exc())
        return 'Err', str(e)

def vk_delete_post(post_id):
    user.delete_post(post_id)
    # vk1.a.NJB_DhCrrd512s6NEnl35PvWdBzLF5X3ta9MOodkSboQpf5sSkMIWOn4_a-lUpzE8INnqbjIGzITUX5UU8t5yH3stSL1IdvINh4KGh80-hNbfJKVpEmeUk3HWFRi26ssB-DGlHAEuyOUNgPckMq7IkZMVYDBfBpGMZBzBuezmkPrQOtCm8ag2VW6bB0XD9db0j_ufJEun3vVCqX4l5Ny-Q