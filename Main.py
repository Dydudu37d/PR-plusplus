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
    exec('from tkinter import messagebox')
    exec(code)
    
