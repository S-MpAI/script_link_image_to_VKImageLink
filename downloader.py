import json
from urllib.request import HTTPError
import urllib.request
import http
import os
from time import sleep

black = "\033[30m"
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
violet = "\033[35m"
turquoise = "\033[36m"
white = "\033[37m"
st = "\033[37"




if str(os.name) == "nt":dir_pref = "\\"
else:dir_pref = "/"

def download(workingdirectory, file='data.json'):
    """
    Загружает изображения из JSON-файла и сохраняет успешно загруженные изображения в указанной директории.

    Args:
        workingdirectory (str): Рабочая директория для сохранения изображений.
        file (str): Имя JSON-файла с данными. По умолчанию: 'data.json'.
    """
    with open(file) as f:data = json.load(f)

    o = os.getcwd()
    if not os.path.exists(workingdirectory):
      os.mkdir(workingdirectory)
    os.chdir(workingdirectory)
    DDF(data)
    os.chdir(o)




def download_function(url, name_file):
  """
    Пытается загрузить файл по указанному URL и обрабатывает различные ошибки.

    Args:
        url (str): URL для загрузки файла.
        name_file (str): Имя файла для сохранения.

    Returns:
        str: Статус операции (код HTTP, ошибки и т. д.).
  """
  url = url.replace(" ", "%20")

  if "?size=" in url:
    ind = url.find("?size=")
  else:
    if "?extra=" in url:
      ind = url.find("?extra=")
    else:
      ind = len(url)

  print('\r', end='')

  try:
    urllib.request.urlretrieve(str(url), name_file)

    print(f"{green}[+] 200: {blue}{name_file}{white}  URL: {url[0:ind]}")
    status = '200'

  except HTTPError as err_code:
    print(f"{red}[-] {red}{err_code.code}: {blue}{name_file}{white}  URL: {url[0:ind]}")
    status = f'{err_code.code}'
  except urllib.error.URLError as err_code:
    if "[WinError 10054]" in str(err_code):
      print(f"{red}[-] {red}522: {blue}{name_file}{white}  URL: {url[0:ind]}")
      status = f'522'

    elif "[Errno 99]" in str(err_code):
      print(f"{red}[-] {red}524: {blue}{name_file}{white}  URL: {url[0:ind]}")
      status = f'524'

    elif "[SSL: WRONG_VERSION_NUMBER]" in str(err_code):
      print(f"{red}[-] {red}526: {blue}{name_file}{white}  URL: {url[0:ind]}")
      status = f'526'

    elif "[Errno 11001]" in str(err_code):
      print(f"{red}[-] {red}101: {blue}{name_file}{white}  URL: {url[0:ind]}")
      status = f'101'

    elif "[WinError 10060]" in str(err_code):
      print(f"{red}[-] {red}524: {blue}{name_file}{white}  URL: {url[0:ind]}")
      status = f'524'    

    elif "[Errno 104]" in str(err_code):
      print(f"{red}[-] {red}524: {blue}{name_file}{white}  URL: {url[0:ind]}")
      status = f'524' 

    elif "<urlopen error retrieval incomplete:" in str(err_code):
      print(f"{violet}[?] 103: {blue}{name_file}{white}  URL: {url[0:ind]}")
      status = f'103' 
    
    elif '[Errno 11002]' in str(err_code):
      err_code = str(err_code).replace('<','').replace('>','').replace('urlopen error ','')
      print(f"{red}[-] {red}524 [{err_code}]: {blue}{name_file}{white}  URL: {url[0:ind]}")
      status = f'524'
    elif '[Errno 11004]' in str(err_code):
      err_code = str(err_code).replace('<','').replace('>','').replace('urlopen error ','')
      print(f"{red}[-] {red}524 [{err_code}]: {blue}{name_file}{white}  URL: {url[0:ind]}")
      status = f'524'
    elif '[WinError 10013]' in str(err_code):
      err_code = str(err_code).replace('<','').replace('>','').replace('urlopen error ','')
      print(f"{red}[-] {red}403 [{err_code}]: {blue}{name_file}{white}  URL: {url[0:ind]}")
      status = f'403'
    
    elif '[WinError 10053] Программа на вашем хост-компьютере разорвала установленное подключение' in str(err_code):
        status = f'1'
      

    else:
      # print(err_code)
      print('\r', end='')
      err_code = str(err_code).replace('<','').replace('>','').replace('urlopen error ','')
      print(f"{violet}[?] ___ ({err_code}): {blue}{name_file}{white}  URL: {url[0:ind]}")
      status = f'___ ({err_code})'

  except http.client.RemoteDisconnected:
    print(f"{violet}[-] {violet}101: {blue}{name_file}{white}  URL: {url[0:ind]}")
    status = f'101'

  except ConnectionResetError:
    print(f"{violet}[-] {violet}101: {blue}{name_file}{white}  URL: {url[0:ind]}")
    status = f'101'

  except ValueError as err:
    print(f"{violet}[?] 102: {blue}{name_file}{white}  URL: {url[0:ind]}")
    status = f'102'

  # except Exception as err:
  #   print(f"{violet}[?] ___  ({err_code}): {blue}{name_file}{white}  URL: {url[0:ind]}")
  #   status = f'___ ({err_code})'

  return status



def DDF(url, i):
      """
    Обрабатывает URL, определяет расширение файла, создает уникальное имя файла и пытается загрузить файл.

    Args:
        url (str): URL для загрузки файла.
        i (int): Уникальный индекс.

    Returns:
        str: Имя успешно загруженного файла.
      """
      zn = url
      
      if zn !='imgs18':
       if zn !='imgs':
        try:
            url = list(zn.keys())[0]
            exten = zn[f"{list(zn.keys())[0]}"]
        except AttributeError:
            url = zn
            if "mp4" in url:
              exten = f".mp4"
            else:
              if "gif" in url:
                exten = f".gif"
              else:
                if "jpg" in url:
                  exten = f".jpg"
                else:
                  if "webp" in url:
                    exten = f".webp"
                  else:
                    if "webm" in url:
                      exten = f".webm"
                    else:
                      exten = f".png"


        name_file = f"{i}{exten}"
        # name_file = zn
        url = zn
        for _ in range(5):
            while not os.path.exists(name_file):
              try:
                status = (download_function(url, name_file))


                if status != "200":
                    if status == '103':
                        sleep(5)
                        status = (download_function(url, name_file))
                        if status != "200":
                          break
                    elif status == '403':
                      
                      while status != '200':
                        status = (download_function(url, name_file))
                      
                        
                    else:
                      break
                else:pass
              except Exception as err_:
                break
      return name_file

if __name__ == "__main__":
    download(f'{os.getcwd()}{dir_pref}pictures')
