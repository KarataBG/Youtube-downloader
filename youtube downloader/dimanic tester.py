import os
import sys
import time
from threading import Thread as threading
from tkinter import OptionMenu
from tkinter import Button
from tkinter import Label
from tkinter import Message
from tkinter import Tk
from tkinter import StringVar
from tkinter import NONE
from tkinter import Entry
from tkinter import filedialog
from tkinter import ttk
# from queue import Queue
from time import sleep, perf_counter

from pytube import YouTube
from pytube import Playlist

from textwrap import wrap

root = Tk()

resolutions = [
    '4320p',
    '2160p',
    '1440p',
    '1080p',
    '720p',
    '480p',
    '360p'
]
types = [
    'video/webm',
    'video/mp4'
]


def cock(res, type):
    print(f"Imame resoluciq {res}; Tip{type}")
    # print(index)
    # print(f"Imame resoluciq {resolutions[int(index)]}; Tip{type}")


def pr():
    print(2)


class D:
    def __init__(self):
        print("ABC")


index = 0
filesize = 3000000000
for res in resolutions:
    for type in types:
        # string = streams.filter(resolution=res, mime_type=type).first()
        #
        # if string is None:
        #     continue
        # print(string)

        # but = Button(root, text="Избери", command=lambda: cock(res, type))
        but = Button(root, text="Избери", command=lambda k=res, j=type, d=D(): cock(k, j))
        but.grid(row=index, column=1)

        lab = Label(root,
                    text=f"{res} {type.split('/')[1]} {filesize / 1024 / 1024 :.2f} MB")
        lab.grid(row=index, column=0)

        index += 1

root.mainloop()
