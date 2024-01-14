import os
import json
import time

from modules.classes import Config, Startclass



C = Config()
S = Startclass(C)
print(f'''┌{"―"*15} Start:''')

S.start()
        
print(f'''└{"―"*15}''')


