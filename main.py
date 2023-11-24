import os
import json
from modules.random_neko_list import imgs, imgs18
from py_upload import upload_to_server
from vk_upload import vk_uploader
from downloader import DDF

w_dir = os.getcwd()


# e = 'https://i.pximg.net/img-original/img/2023/07/28/20/01/40/110314318_p0.jpg'
# print(e.split('/')[2])
# raise ImportError('I')

print(f'''
Count Imgs: {len(imgs)}
Count Imgs18: {len(imgs18)}
''')



append_ = []
not_append_ = []

access_image_list = ['jpg', 'png', 'jpeg']
block__image_list = ['mp4', 'gif', 'webm']
NewVKLinks = []

o = 0
for link in imgs18:
    if type(link) == dict:pass
    else:
        if link not in ['imgs', 'imgs18']:

            if str(link.split('/')[2]) not in  ['i.pinimg.com','i.pximg.net']:
                if 'https://sun' not in str(link):
                    # print(str(link.split('/')[2]))

                    if list(link.split('.'))[-1] in access_image_list:
                        if not os.path.exists('VK_'):
                            os.mkdir('VK_')
                        os.chdir('VK_')
                        name_file = DDF(link, o)
                        os.chdir(w_dir)
                        link = vk_uploader(name_file, 'VK_') 
                        NewVKLinks.append(link)

                    elif list(link.split('.'))[-1] in block__image_list:
                        if not os.path.exists('PY'):os.mkdir('PY')
                        os.chdir('PY')
                        name_file = DDF(link, o)
                        # print(os.getcwd())
                        
                        upload_to_server(name_file)
                    o = o + 1
                    os.chdir(w_dir)
                else:
                    NewVKLinks.append(link)
                    pass
        
        
        if 'imgs' == link: append_.append(link)
        if 'imgs18' == link: append_.append(link)

        



# [print(_) for _ in not_append_]
# print('\t\n')
# [print(_) for _ in append_]


# # for link in append_:
# if not os.path.exists('VK_'):
#     os.mkdir('VK_')
# os.chdir('VK_')
# DDF(append_)

# os.chdir(w_dir)

# if not os.path.exists('PY'):os.mkdir('PY')
# os.chdir('PY')
# DDF(not_append_)

# os.chdir(w_dir)


# for file in os.scandir('VK_'):
#     link = vk_uploader(file.name, 'VK_') 
#     NewVKLinks.append(link)

with open("NewVKLinks.json", "w") as outfile:
  json.dump(NewVKLinks, outfile, indent=4)