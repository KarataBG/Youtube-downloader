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


# from pytube.cli import on_progress


def progress_function(chunk, file_handle, bytes_remaining):
    current = ((int(filesize) - bytes_remaining) / filesize)
    percent = '{0:.1f}'.format(current * 100)
    print(percent)


def download(url, quality):
    global filesize
    video = url.streams.filter(resolution="720p").first()
    print(4)
    mime_type = video.mime_type
    filesize = video.filesize
    title = url.title
    title = title.replace("|", "_").replace("/", "_").replace("\\", "_").replace("?", "").replace(":", "-").replace(
        "*", "").replace("<", "less than").replace(">", "more than").replace("\"", "").replace("&", "and").replace(
        "/", "or")

    videoFile = video.download(output_path=directory,
                               filename=title + ' ' + quality + ' video .' + mime_type.split("/")[1])
    print(5)


vidQualities = [
    "1080p",
    "720p",
    "480p",
    "360p",
]

print("!")
# url = YouTube('https://www.youtube.com/watch?v=nGWTuQUMQpw', on_progress_callback=progress_function)
# url = YouTube('https://www.youtube.com/watch?v=KvMY1uzSC1E', on_progress_callback=progress_function)
url = YouTube('https://www.youtube.com/watch?v=-rfJX6xVwsk', on_progress_callback=progress_function)
# playlist = Playlist("https://www.youtube.com/watch?v=67h-KI4Ngtg&list=PLS6oKYrRmu0BSZ8lQPWb_U9jVuPn573r-&index=10")
# streams = url.streams
print(2)
# videoQuality = "1080p"
directory = filedialog.askdirectory()
directoryLabel = directory
# title = url.title
print(3)
download(url, "1080p")

# filesize = 0
# for vid in playlist.videos:
# for quality in vidQualities:
# print(4)
# t = threading(target=download, args=[vid, "720p"])
# t.start()
# download(vid,"720p")
