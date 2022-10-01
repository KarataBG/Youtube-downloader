import os
import sys
import threading
from tkinter import *
from tkinter import filedialog

from pytube import YouTube
from pytube import Playlist
from pytube.cli import on_progress

sys.path.append(r'C:\ffmpeg\bin')


# направи проверка дали файла го има да не тегли всеки път
# довърши подметодите и направи накрая да показва какво и къде е свалено може и прогрес линия
# ако има начин без бутон а директно от менюто да има онклик
# да проверявам дали вече има песента изтеглена защото аз свалям името + видео/аудио така че да провери дали го има youtube.title

# цялото чакане е в рекодирането на webm в mp3 намери начин да е по бързо
# направи нишки

class Panel:
    startingOptionCheck = True
    choiceOneCheck = True
    workingWithPlaylist = False

    def startingOption(self):
        self.URL = self.entryURL.get()
        # print(self.URL)
        if self.URL.__contains__("playlist?list") or self.URL.__contains__("&list"):
            self.workingWithPlaylist = True

        self.directory = filedialog.askdirectory()
        self.directoryLabel.config(text=self.directory)
        if self.startingOptionCheck:
            options = [
                "max quality video",
                "max quality audio",
                "all options",
                "1080p"
            ]

            # self.clicked.set("избирай и цъквай бутона")
            self.clicked.set("1080p")

            OptionMenu(self.root, self.clicked, *options).pack()

            Button(self.root, text="Продължи", command=self.choiceOne).pack()

            self.label = Label(self.root, text=" ")
            self.label.pack()
            self.startingOptionCheck = False

    def choiceOne(self):
        if self.choiceOneCheck:
            self.label.config(text=self.clicked.get())
            if self.clicked.get() == "max quality video":
                self.downloadQuickVideo(False, True, "", "")
            if self.clicked.get() == "max quality audio":
                self.downloadQuickVideo(True, True, "", "")
            elif self.clicked.get() == "all options":
                optionsPalno = [
                    "2160p",
                    "1440p",
                    "1080p",
                    "720p",
                    "480p",
                    "360p",
                    "160kbps",
                    "128kbps",
                    "70kbps"
                ]
                drop = OptionMenu(self.root, self.clickedPalno, *optionsPalno)
                drop.pack()
                Button(self.root, text="Подробен избор", command=self.choiceOfPalno).pack()
            elif self.clicked.get() == "1080p":
                self.downloadQuickVideo(False, False, "1080p", "")
            self.choiceOneCheck = False

    URL = NONE

    def choiceOfPalno(self):
        self.URL = self.entryURL.get()

        # print(self.URL)
        self.label.config(text=self.clickedPalno.get())
        if self.clickedPalno.get().__contains__("kbps"):
            # self.downloadQuickVideo(True, False, "", self.clickedPalno.get())
            threading.Thread(target=self.downloadQuickVideo(True, False, "", self.clickedPalno.get()),
                             daemon=True).start()

        elif self.clickedPalno.get().endswith("p"):
            # self.downloadQuickVideo(False, False, self.clickedPalno.get(), "")
            threading.Thread(target=self.downloadQuickVideo(False, False, self.clickedPalno.get(), ""),
                             daemon=True).start()

    def downloadQuickVideo(self, audioOnly: bool, maxQuality: bool, videoQuality: str, audioQuality: str):
        if self.workingWithPlaylist:
            # print(self.URL)
            self.playlist = Playlist(self.URL)
            # print(self.playlist.videos)
            for vid in self.playlist.videos:
                vid.register_on_progress_callback(self.progress_function)

                # self.download(audioOnly, maxQuality, videoQuality, audioQuality, vid, vid.title)
                threading.Thread(
                    target=self.download(audioOnly, maxQuality, videoQuality, audioQuality, vid, vid.title),
                    daemon=True).start()
        else:
            url = YouTube(self.URL, on_progress_callback=on_progress)
            title = url.title
            if len(self.entryName.get()) != 0:
                title = self.entryName.get()
            # self.download(audioOnly, maxQuality, videoQuality, audioQuality, url, title)
            threading.Thread(target=self.download(audioOnly, maxQuality, videoQuality, audioQuality, url, title),
                             daemon=True).start()

    def download(self, audioOnly: bool, maxQuality: bool, videoQuality: str, audioQuality: str, url: YouTube,
                 title: str):

        title = title.replace("|", "").replace("/", "").replace("\\", "").replace("?", "").replace(":", "").replace(
            "*", "").replace("<", "").replace(">", "").replace("\"", "").replace("&", "and")

        audioOutput = self.directory + '/' + title + " author- " + url.author + '.mp3'
        videoOutput = self.directory + '/' + title + " author- " + url.author + '.webm'

        # print(url.streams.filter(only_audio=True))
        if audioOnly:

            if os.path.exists(self.directory + '/' + title + " author- " + url.author + '.mp3'):
                print(self.directory + '/' + title + " author- " + url.author + '.mp3')
                print("Съществува" + url.title)
                return

            if maxQuality:
                audio = url.streams.filter(only_audio=True).order_by('abr').last()
            else:
                audio = url.streams.filter(only_audio=True, abr=audioQuality).first()
            self.filesize = audio.filesize
            audioFile = audio.download(output_path=self.directory, filename=title + ' audio.webm')

            os.system(f'cmd /c "ffmpeg -i "{audioFile}" -vn -ab 160k -ar 48000 -y "{audioOutput}"     "')
            os.remove(audioFile)

        elif not audioOnly:
            if os.path.exists(self.directory + '/' + title + " author- " + url.author + '.webm'):
                print("Съществува" + url.title)
                return
            if os.path.exists(self.directory + '/' + title + " author- " + url.author + '.mp4'):
                print("Съществува" + url.title)
                return
            audio = url.streams.filter(only_audio=True).order_by('abr').last()
            self.filesize = audio.filesize
            audioFile = audio.download(output_path=self.directory, filename=title + ' audio.webm')

            if maxQuality:
                video = url.streams.order_by('resolution').last()
            else:
                video = url.streams.filter(mime_type="video/webm", resolution=videoQuality).first()

            self.filesize = video.filesize
            videoFile = video.download(output_path=self.directory, filename=title + ' video .webm')

            # self.wtfNotAudio(videoFile, audioFile, videoOutput)
            threading.Thread(target=self.wtfNotAudio(videoFile, audioFile, videoOutput), daemon=True).start()

    def wtfNotAudio(self, videoFile, audioFile, videoOutput):
        os.system(f'cmd /c "ffmpeg -y -i "{videoFile}" -i "{audioFile}" -c copy "{videoOutput}" "')
        os.remove(audioFile)
        os.remove(videoFile)

    def reset(self):
        self.root.destroy()
        self.root = Panel()

    def progress_function(self, chunk, file_handle, bytes_remaining):
        # print(self.filesize)
        # print(str(bytes_remaining) + "TTTTTTTTTTTT")
        current = ((int(self.filesize) - bytes_remaining) / self.filesize)
        percent = ('{0:.1f}').format(current * 100)
        progress = int(50 * current)
        status = '█' * progress + '-' * (50 - progress)
        print(percent)
        self.sizeLabel = self.filesize
        self.reportLabel = progress

    def __init__(self):
        # self.entryURL = None
        self.filesize = None
        self.playlist = None
        self.directory = None
        self.label = None
        self.root = Tk()
        self.clickedBarzo = StringVar()
        self.clickedPalno = StringVar()
        self.clicked = StringVar()

        self.root.geometry("300x800")

        Label(self.root, text="URL").pack()
        entry_text = StringVar()
        self.entryURL = Entry(self.root, width=50, textvariable=entry_text)
        entry_text.set("https://www.youtube.com/watch?v=mVTCxn5rJ50&list=PLS6oKYrRmu0BSZ8lQPWb_U9jVuPn573r-&index=9")
        self.entryURL.pack()

        Label(self.root, text="File Name").pack()
        self.entryName = Entry(self.root, width=50)
        self.entryName.pack()

        Button(self.root, text="Избиране на директория", command=self.startingOption).pack()
        self.directoryLabel = Label(self.root, text="Chosen directory")
        self.directoryLabel.pack()

        Button(self.root, text="reset", command=self.reset).pack()
        self.reportLabel = Label(self.root, text="Reports")
        self.reportLabel.pack()
        self.sizeLabel = Label(self.root, text="Reports")
        self.sizeLabel.pack()

        # Execute tkinter
        self.root.mainloop()


if __name__ == '__main__':
    # directory = 'X:\\my python program YouTube download directory'

    Panel()

    # URL = input("Дай линка")
    # url = YouTube(URL)
    # title = url.title
    #
    # b = url.streams.get_highest_resolution()
    # print(url.streams)
    # exit()
    # lesnaVersiq = input("barza versiq True/False").capitalize()
    #
    # if lesnaVersiq:
    #     choise = input("video ili mp3")
    #     if choise == "video":
    #         print()
    #         # a = url.streams.order_by("resolution").last()
    #         # b = url.streams.filter(only_audio=True).order_by('abr').last()
    #     if choise == "mp3":
    #         a = url.streams.filter(only_audio=True).order_by('abr').last()
    # elif not lesnaVersiq:
    #     resolution = input("resoluciq 1080p 720p 480p 360p musica")
    #     if resolution == "musica":
    #         resolutionMusic = input()
    #
    # audio = url.streams.filter(only_audio=True).order_by('abr').last()
    # print(audio)
    # audioFile = audio.download(output_path=directory, filename=title + ' audio.webm')
    # video = url.streams.filter(resolution='1080p', mime_type='video/webm').first()
    # videoFile = video.download(output_path=directory, filename=title + 'video .webm')
    # print(videoFile)
    # print(audioFile)
    #
    # a = directory + '\\' + title + '.webm'
    # print(a)
    #
    # os.system(f'cmd /c "ffmpeg -y -i "{videoFile}" -i "{audioFile}" -c copy  {a} "')
    # os.remove(audioFile)  # audio faila
    # os.remove(videoFile)

# postVideo = videoFile
# postAudio = audioFile

# cancer = ffmpeg.output(postVideo, postAudio, directory + "\\" + "the final solution.webm")
# cancer = ffmpeg.filter(postAudio, '')
# cancer.run()
# print(postVideo)
# playlist = Playlist(URL)

# 137 1080p mp4 248 1080p webm           itag

# os.rename(audioFile, video.title + ' audio.webm')

# videoAt1080 = video.streams.filter(mime_type='video/webm', resolution='1080p').first()
# videoAt1080 = video.streams.filter(mime_type='video/webm', resolution='1080p')
# videoStream = video.streams.get_by_resolution('1080p')
# videoStream = videoAt1080.get_by_resolution('1080p')
# print(videoStream)
# print("AAAAAAAAA")
# print(video.captions)

# postVideo = ffmpeg.input(directory)

# ffmpeg.concat(postVideo, postAudio, v=1, a=1).output('X:\\my python program youtube download directory\\AI Day 2!!!! What to expect! audio 333333.webm').run()
# ffmpeg.output(postAudio, postVideo, 'out.mp4').run()

# os.system(f'cmd /c "ffmpeg -i "{videoFile}" -i "{audioFile}" -c:v copy -c:a aac output.mp4"')

# postVideo = ffmpeg.input(directory + "//" + title + '.webm')
# postAudio = ffmpeg.input(directory + "//" + title + ' audio.webm')

# postVideo = ffmpeg.input('X:\\my python program youtube download directory\\AI Day 2!!!! What to expect!.webm')
# postAudio = ffmpeg.input('X:\\my python program youtube download directory\\AI Day 2!!!! What to expect! audio.webm')
# postVideo = ffmpeg.input(videoFile)
# postAudio = ffmpeg.input(audioFile)

# print(directory +'//' + url.title + '.webm')
# print(directory +'//' + url.title + ' audio .webm')
