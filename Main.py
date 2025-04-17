from typing import *
from os import *

keyword = {
    "prln":"print",
    "return":"return",
    "//":"#",
    "func":"def",
    "run":"exec",
    "load":"import",
}

def start(code):
    for key in keyword:
        code = code.replace(key, keyword[key])
        #if "msgbox" in key:
            #os.system('mshta vbscript:msgbox('提示内容1',1,'提示窗口1')(window.close)')
    exec(code)
    
