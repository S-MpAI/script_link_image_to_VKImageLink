import os
import json
import time
import traceback
# try:
#     from modules.random_neko_list import imgs, imgs18
#     data = imgs + imgs18
# except:
#     with open('data.json', "r+") as f:data = json.load(f)

# if os.path.exists('config.json'):
#     with open('data.json', "r+") as f:data = json.load(f)
#     already_donload = data.get('already_donload')
# else:
#     already_donload = 0
from modules.py_upload import upload_to_server
from modules.vk_upload import vk_uploader
from modules.downloader import DDF

w_dir = os.getcwd()




VK_folder    = 'VK_'
Other_folder = 'PY_'


append_ = []
not_append_ = []

access_image_list = ['jpg', 'png', 'jpeg']
block__image_list = ['mp4', 'gif', 'webm']
NewVKLinks = []

o = 0

# try:
#     for link in data:
        
#         if type(link) == dict:pass
#         else:
#             if link not in ['imgs', 'imgs18']:

#                 if str(link.split('/')[2]) not in  ['i.pinimg.com','i.pximg.net']:
#                     if 'https://sun' not in str(link):
#                         # print(str(link.split('/')[2]))

#                         if list(link.split('.'))[-1] in access_image_list:
#                             if not os.path.exists(VK_folder):
#                                 os.mkdir(VK_folder)
#                             os.chdir(VK_folder)
#                             name_file = DDF(link, o)
#                             per_link = link
                            
#                             os.chdir(w_dir)
#                             link = vk_uploader(name_file, VK_folder) 
#                             NewVKLinks.append(link)
                            
#                             print(f'''
# ├{"―"*10} NEXT LINK:
# ┊ Pervious LINK: {per_link}
# ┊ VK link: {link}
# ''')

#                         elif list(link.split('.'))[-1] in block__image_list:
#                             if not os.path.exists(Other_folder):os.mkdir(Other_folder)
#                             os.chdir(Other_folder)
#                             name_file = DDF(link, o)
#                             # print(os.getcwd())
                            
#                             upload_to_server(name_file)
#                             print(f'''
# ├{"―"*10} NEXT LINK:
# ┊ Pervious LINK: {per_link}
# ┊ UPLOADED TO SERVER
# ''')
#                         o = o + 1
#                         os.chdir(w_dir)
#                     else:
#                         NewVKLinks.append(link)
#                         pass
            
            
#             if 'imgs' == link: append_.append(link)
#             if 'imgs18' == link: append_.append(link)
        
#         time.sleep(10)
#     with open("NewVKLinks.json", "w") as outfile:json.dump(NewVKLinks, outfile, indent=4)
# except:
#     with open("NewVKLinks.json", "w") as outfile:json.dump(NewVKLinks, outfile, indent=4)

        
# print(f'''└{"―"*15}''')

class Config():
    def __init__(self, config_file = 'config.json'):
        if os.path.exists(config_file):
            with open(config_file, "r+") as f:config = json.load(f)
            self.already_download = config.get('already_donload')
        else:
            self.already_download = 0
        
        print(f'''
Already download: {True if self.already_download else False}''')
        
    def get_links(self):
        if os.path.exists('data.json'):
            with open('data.json', "r+") as f:data = json.load(f)
            print('Links from data.json file')
            return data
        else:
            try:
                from modules.random_neko_list import imgs, imgs18
                print('Links from  random_neko_links.py file')
                return imgs + imgs18
            except:
                print('Not Found Links')
                return []
    
    def get_info(self):
        return self.already_download
            


class Startclass():
    def __init__(self, C):
        self.C = C
        self.o = 0
    def start(self):
        self.sort()
    
    def sort(self):
        if self.C.get_info():
            # print('Уже загружено')
            self.already_downloaded()
            
            # self.not_downloaded()
        else:
            # print('Нужно загрузить')
            self.all_data = self.C.get_links()
            self.not_downloaded()
    
    def not_downloaded(self):
        o = self.o
        try:
            for link in self.data_link:
                
                if type(link) == dict:pass
                else:
                    if link not in ['imgs', 'imgs18']:

                        if str(link.split('/')[2]) not in  ['i.pinimg.com','i.pximg.net']:
                            if 'https://sun' not in str(link):
                                # print(str(link.split('/')[2]))

                                if list(link.split('.'))[-1] in access_image_list:
                                    if not os.path.exists(VK_folder):
                                        os.mkdir(VK_folder)
                                    os.chdir(VK_folder)
                                    name_file = DDF(link, o)
                                    per_link = link
                                    
                                    os.chdir(w_dir)
                                    link = vk_uploader(name_file, VK_folder) 
                                    NewVKLinks.append(link)
                                    
                                    print(f'''├{"―"*10} NEXT LINK:\n┊ Pervious LINK: {per_link}\n┊ VK link: {link}''')

                                elif list(link.split('.'))[-1] in block__image_list:
                                    if not os.path.exists(Other_folder):os.mkdir(Other_folder)
                                    os.chdir(Other_folder)
                                    name_file = DDF(link, o)
                                    # print(os.getcwd())
                                    
                                    upload_to_server(name_file)
                                    print(f'''├{"―"*10} NEXT LINK:\n┊ Pervious LINK: {per_link}\n┊ UPLOADED TO SERVER''')
                                o = o + 1
                                os.chdir(w_dir)
                            else:
                                NewVKLinks.append(link)
                                pass
                    
                    
                    if 'imgs' == link: append_.append(link)
                    if 'imgs18' == link: append_.append(link)
                
                time.sleep(10)
            with open("NewVKLinks.json", "w") as outfile:json.dump(NewVKLinks, outfile, indent=4)
        except:
            with open("NewVKLinks.json", "w") as outfile:json.dump(NewVKLinks, outfile, indent=4)
            
            
    def test(self):
        for file in os.listdir('data'):
            print(file)
            
            
    def already_downloaded(self):
        o = self.o
        try:
            for file_name in os.listdir('data'):
                # print(file_name)
                
                link = file_name
                
                if type(link) == dict:pass
                else:
                    if link not in ['imgs', 'imgs18']:

                        # if str(link.split('/')[2]) not in  ['i.pinimg.com','i.pximg.net']:
                            # if 'https://sun' not in str(link):
                                # print(str(link.split('/')[2]))

                                if list(link.split('.'))[-1] in access_image_list:
                                    
                                    # if not os.path.exists(VK_folder):os.mkdir(VK_folder)
                                    os.chdir('data')
                                    name_file = link
                                    
                                    
                                    os.chdir(w_dir)
                                    link, err = vk_uploader(name_file, 'data') 
                                    if link != 'Err':
                                        NewVKLinks.append(link)
                                        print(f'''├{"―"*10} NEXT LINK:\n┊ File: {name_file}\n┊ VK link: {link}''')
                                    else:
                                        print(f'''├{"―"*10} NEXT LINK:\n┊ Error\n┊ File: {name_file}\n┊ Message: {err}''')
                                    
                                    time.sleep(10)   

                                elif list(link.split('.'))[-1] in block__image_list:
                                    # if not os.path.exists(Other_folder):os.mkdir(Other_folder)
                                    # os.chdir(Other_folder)
                                    # name_file = DDF(link, o)
                                    link = 'None'
                                    name_file = file_name
                                    os.chdir('data')
                                    upload_to_server(name_file, False)
                                    print(f'''├{"―"*10} NEXT LINK:\n┊ File: {name_file}\n┊ UPLOADED TO SERVER''')
                                    time.sleep(5)
                                o = o + 1
                                os.chdir(w_dir)
                
                # if (link != 'Err') or (link == 'None'):time.sleep(10)
                # else:pass
            with open("NewVKLinks.json", "w") as outfile:json.dump(NewVKLinks, outfile, indent=4)
        except Exception as e:
            print(traceback.format_exc())
            print("Error creating newVKLinks.json file : " + str(e))
            
            with open("NewVKLinks.json", "w") as outfile:json.dump(NewVKLinks, outfile, indent=4)
            

if __name__ == "__main__":
    S = Startclass()
    S.test()