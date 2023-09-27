import os
import sys
from threading import Thread as threading
from tkinter import Button
from tkinter import Label
from tkinter import Tk
from tkinter import StringVar
from tkinter import Entry
from tkinter import filedialog


from pytube import YouTube
from pytube import Playlist

from moviepy.editor import *
import moviepy

from textwrap import wrap

# from pytube.cli import on_progress

# sys.path.append(r'C:\ffmpeg\bin')


# направи проверка дали файла го има да не тегли всеки път
# довърши подметодите и направи накрая да показва какво и къде е свалено може и прогрес линия
# ако има начин без бутон а директно от менюто да има онклик
# да проверявам дали вече има песента изтеглена защото аз свалям името + видео/аудио така че да провери дали го има youtube.title; има но не проверява дали е правилно изтеглена

# цялото чакане е в рекодирането на webm в mp3 намери начин да е по бързо; оправено от нишки
# направи нишки; тикче

# при грешка остават временните файлове
# ако е под 720п да не тегли аудио
# нишковаото да бъде опашка от 15 при аудио 3 при малки и средни видеа 1 при дълги видеа
# да се оправи зацепването на главната нишка при теглене
# ако в името на автора има забранени символи
# при ниска резолюция на видеото тегли грешен вид и няма правилен кодек
# [webm @ 00000259c6d3ddc0] Only VP8 or VP9 or AV1 video and Vorbis or Opus audio and WebVTT subtitles are supported for WebM.
# Could not write header for output file #0 (incorrect codec parameters ?): Invalid argument
# Error initializing output stream 0:1 --
# динамично да проверява дали сваля твърде много или обработва твърде много и да увеличава или намалява броя позволени нишки
# да изкарва повече информация преди повреме и след тегленето
# при избирането на качество при преминаване от подробно към друго или да изтрие дошлите менюта или го направи да ги показва всичките опции да може да се изберат на куп
# Направи менюто по-хубаво
# Като цяло трябва да има много повече проверки
#
#
# При динамичното създаване като променлива остава само последното задаване на променливи vid и audio качество
# Или масив от качествата или масив с класове видеото със своите променливи като качество линк стрийм и тн
#
# Threadnumber е тежко зле не че е твърде зле ама е зле че само намалява
# Направи код за когато няма качество
#
# Докато тегли видео/а да блокира бутоните (работи за индив видео) но да има бутон който да спре тегленето веднага и след текущото видео
# Ако няма избраното аудио от плейлист да изтегли една категория надолу
# Не тегли възрастово ограничени видеа сигурно трябва ютуб акаунт бисквити или нещо
#
#
# Ако е избрал видео/лист, но избере нов то да премахне списъка с опции за теглене и име/брой видеа

class Panel:
    startingOptionCheck = True
    choiceOneCheck = True
    workingWithPlaylist = False
    threadNumber = 0
    urlVault = ""
    changedUrl = True
    playlistLength = 0
    currentPlaylistLength = 0
    isDownloading = False

    def startingOption(self):
        # print(self.URL)
        self.directory = filedialog.askdirectory()
        self.directoryLabel.config(text=self.directory)

        if self.entryURL.get() == "":
            self.reportLabel.config(text="Въведи youtube линк")
            return

        if self.urlVault != self.entryURL.get():
            xx = threading(target=self.define(), daemon=True)
            xx.start()

    def define(self):
        if self.entryURL.get().__contains__("playlist?list") or self.entryURL.get().__contains__("&list"):

            self.workingWithPlaylist = True
        else:
            self.workingWithPlaylist = False

        if self.workingWithPlaylist:
            # xx = threading(target=self.definePlaylist, daemon=True)
            # xx.start()
            self.definePlaylist()
        if not self.workingWithPlaylist:
            # xx = threading(target=self.defineStreams, daemon=True)
            # xx.start()
            self.defineStreams()

        self.resetStreams()

    def resetStreams(self):
        for obj in self.labels:
            obj.destroy()

        for obj in self.buttons:
            obj.destroy()

        self.labels = []
        self.buttons = []

        # self.progressLabel.config(text="")

    def defineYoutube(self):
        self.url = YouTube(self.entryURL.get(), on_progress_callback=self.progress_function,
                           on_complete_callback=self.complete_function)
        # self.url.bypass_age_gate()

    def definePlaylist(self):
        self.continueButton.config(text="Връзката не е осъществена")
        print("Starting streams")

        self.playlist = Playlist(self.entryURL.get())
        print("Got playlist")
        # self.playlistStreams = [a.streams for a in self.playlist.videos]
        self.streams = self.playlist.videos[1].streams

        self.continueButton.config(text="Избери")
        self.changedUrl = True
        self.urlVault = self.entryURL.get()
        splitedString = ""
        n  = 32
        for index in range(0, len(self.url.title), n):
            splitedString+=(self.url.title[index : index + n]) + "\n"
        self.sizeLabel.config(text="Заглавие:\n" + str(splitedString))
        self.currentPlaylistLength = 0
        self.playlistLength = self.playlist.length
        self.progressLabel.config(text=f"{self.playlistLength} броя")
        print("Got streams")

        # print(self.playlistStreams)

    def defineStreams(self):
        self.continueButton.config(text="Връзката не е осъществена")
        print("Starting streams")
        self.defineYoutube()
        print(self.url)
        self.streams = self.url.streams
        self.continueButton.config(text="Избери")
        self.changedUrl = True
        self.urlVault = self.entryURL.get()
        splitedString = ""
        n  = 32
        for index in range(0, len(self.url.title), n):
            splitedString+=(self.url.title[index : index + n]) + "\n"
        self.sizeLabel.config(text="Заглавие:\n" + str(splitedString))
        print("Got streams")


    labels = []
    buttons = []

    def choiceOne(self):
        if not self.entryURL.get().strip():
            self.reportLabel.config(text="Не е въведен URL")
            return
        if not self.directory:
            self.reportLabel.config(text="Няма избрана директория")
            return

        if self.changedUrl:
            self.resetStreams()

            if not self.workingWithPlaylist:
                if self.streams is None:
                    x = threading(target=self.define(), daemon=True)
                    x.start()
                    x.join()
                for string in self.streams.filter(type="audio").order_by("abr").desc():
                    but = Button(self.root, text="Избери",
                                 command=lambda mime=string.mime_type, abr=string.abr:
                                 self.downloadQuickVideo(True, False, "", mime, abr))
                    but.grid(row=self.index, column=1)
                    lab = Label(self.root,
                                text=f"{string.abr} {string.mime_type.split('/')[1]} {string.filesize / 1024 / 1024 :.2f} MB")
                    lab.grid(row=self.index, column=0)

                    self.index += 1

                    self.labels.append(lab)
                    self.buttons.append(but)
                resolutions = [
                    '4320p',
                    '2160p',
                    '1440p',
                    '1080p',
                    '720p',
                    '480p',
                    '360p',
                    '240p',
                    '144p'
                ]
                types = [
                    'video/webm',
                    'video/mp4'
                ]
                for res in resolutions:
                    for type in types:
                        try:
                            string = self.streams.filter(resolution=res, mime_type=type).first()

                            if string is None:
                                continue
                            but = Button(self.root, text="Избери",
                                         command=lambda res1=res, type1=type:
                                         self.downloadQuickVideo(False, False, res1, type1, ""))
                            but.grid(row=self.index, column=1)

                            lab = Label(self.root,
                                        text=f"{res} {type.split('/')[1]} {string.filesize / 1024 / 1024 :.2f} MB")
                            lab.grid(row=self.index, column=0)

                            self.index += 1

                            self.labels.append(lab)
                            self.buttons.append(but)
                        except KeyError as e:
                            self.errorLabel.config(
                                text=self.errorLabel.cget("text") + f"Проблем {e} с видео {string.title} \n")
            if self.workingWithPlaylist:
                # for string in self.playlistStreams[0].filter(type="audio").order_by("abr").desc():
                # for string in self.playlist.videos[0].streams.filter(type="audio").order_by("abr").desc():
                for string in self.streams.filter(type="audio").order_by("abr").desc():
                    but = Button(self.root, text="Избери",
                                 command=lambda mime=string.mime_type, abr=string.abr:
                                 self.downloadQuickVideo(True, False, "", mime, abr))
                    but.grid(row=self.index, column=1)
                    lab = Label(self.root,
                                text=f"{string.abr} {string.mime_type.split('/')[1]} mp3")
                    lab.grid(row=self.index, column=0)
                    self.index += 1

                    self.labels.append(lab)
                    self.buttons.append(but)
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
                for res in resolutions:
                    for type in types:
                        # string = self.playlistStreams[0].filter(resolution=res, mime_type=type).first()
                        # string = self.playlist.videos[0].streams.filter(resolution=res, mime_type=type).first()
                        string = self.streams.filter(resolution=res, mime_type=type).first()

                        if string is None:
                            continue
                        but = Button(self.root, text="Избери",
                                     command=lambda res1=res, type1=type:
                                     self.downloadQuickVideo(False, False, res1, type1, ""))
                        but.grid(row=self.index, column=1)

                        lab = Label(self.root,
                                    text=f"{res} {type.split('/')[1]}")
                        lab.grid(row=self.index, column=0)

                        self.index += 1

                        self.labels.append(lab)
                        self.buttons.append(but)
            self.urlVault = self.entryURL.get()
            self.changedUrl = False

    def downloadPlaylist(self, audioOnly: bool, maxQuality: bool, videoQuality: str, mime_type: str,
                         audioQuality: str):
        threads = []
        queue = 2
        usecase = self.playlist.videos[0].length
        if audioOnly or usecase < 60 * 3:
            queue = 4
        if usecase < 60 * 5:
            queue = 2
        if usecase > 60 * 30:
            queue = 1
        if usecase > 60 * 50:
            queue = 1
        if videoQuality == "1440p" or videoQuality == "2160p":
            queue = 1
        queue = 16
        self.threadNumber = 0
        for vid in self.playlist.videos:
            # vid.register_on_progress_callback(self.progress_function)
            while True:
                print(f"threads {queue - self.threadNumber}")
                if self.threadNumber < queue:
                    # if len(threads) > 1:
                    #     threads[0].join()
                    self.threadNumber += 1
                    t = threading(target=self.download,
                                  args=[audioOnly, maxQuality, videoQuality, mime_type, audioQuality, vid,
                                        vid.title])
                    threads.append(t)
                    t.start()
                    break
                sleep(0.05)
        for thread in threads:
            thread.join()

    def downloadQuickVideo(self, audioOnly: bool, maxQuality: bool, videoQuality: str, mime_type: str,
                           audioQuality: str):
        if self.isDownloading:
            print("В момента се тегли от youtube")
            return
        if not self.isDownloading:
            self.isDownloading = True
            self.currentPlaylistLength = 0
            if self.workingWithPlaylist:
                downloadPlaylistThread = threading(target=self.downloadPlaylist,
                                                   args=[audioOnly, maxQuality, videoQuality, mime_type, audioQuality])
                downloadPlaylistThread.start()
            else:
                title = self.url.streams[0].title

                # if len(self.entryName.get()) != 0:
                # title = self.entryName.get()
                # self.download(audioOnly, maxQuality, videoQuality, audioQuality, mime_type, self.url, title) https://www.youtube.com/watch?v=4t8kK030b9o
                # print(audioOnly, maxQuality, videoQuality, audioQuality, mime_type, self.url, title)
                t = threading(target=self.download,
                              args=[audioOnly, maxQuality, videoQuality, mime_type, audioQuality, self.url, title])
                t.start()


    def download(self, audioOnly: bool, maxQuality: bool, videoQuality: str, mime_type: str, audioQuality: str,
                 url: YouTube, title: str):
        # print(audioOnly, maxQuality, videoQuality, audioQuality,"N", mime_type,"N",self.url, title ,"   LLLLLLLLL")
        # print(f"audioO {audioOnly} vidO {maxQuality} vidQ {videoQuality} audioQ {audioQuality} mime {mime_type} ")
        # print(audioQuality + "SEconds time")
        print(self.directory + url.author)
        title = title + f" author- {url.author}"
        title = title.replace("|", "_").replace("/", "_").replace("\\", "_").replace("?", "").replace(":", "-").replace(
            "*", "").replace("<", "less than").replace(">", "more than").replace("\"", "").replace("&", "and").replace(
            "/", "or")

        # Когато тегли да провери ако е само звук или под 720p директно да свали без комбиниране
        # Рестарта който прави бутона избери да се прави автоматично след спиране на нишките
        # ще води до по-малко грешки

        # Виж как да подаваш стрийм че така може да е по бързо

        # audioOutput = self.directory + '/' + title + " author- " + url.author + ' audio.mp3'
        audioOutput = self.directory + '/' + title + '.mp3'
        # if not audioOnly:
        videoOutput = self.directory + '/' + title + " ." + mime_type.split("/")[1]

        if mime_type.split("/")[0] == "audio":
            # измисли начин да проверява имаето без ебавката от преименуването // някак да взима youtube id
            # оправи възникването на грешка на нишките зацикля програмата след приключване на нишките
            # error handling при raise exceptions.AgeRestrictedError(self.video_id)
            # pytube.exceptions.AgeRestrictedError: jKZzU1iiLWw is age restricted, and can't be accessed without logging in.
            # Сега се случва при age restricted
            if os.path.exists(audioOutput):
                print("Съществува аудиото " + url.title)
                # print(f"Self thread {self.threadNumber}")
                txt = self.reportLabel.cget("text")
                self.reportLabel.config(text=f""
                # f"{txt} "
                f"Съществува аудиото {url.title} +\n")
                self.threadNumber -= 1
                self.countPlaylist()
                self.isDownloading = False
                return
        if mime_type.split("/")[0] == "video":
            if os.path.exists(videoOutput):
                print("Съществува видеото" + url.title)
                self.reportLabel.config(text=f"Съществува видеото {url.title}")
                self.threadNumber -= 1
                self.countPlaylist()
                self.isDownloading = False
                return
        if audioOnly:
            if maxQuality:
                audio = url.streams.filter(only_audio=True, abr=audioQuality).first()
            else:
                audio = url.streams.filter(only_audio=True).order_by('abr').last()
                print(audio)
                if not audio:
                    audio = url.streams.filter(only_audio=True).first()
            self.filesize = audio.filesize
            print("Заглавие " + title)
            print(audio.bitrate)
            audioFile = audio.download(output_path=self.directory, filename=title + ".mp3")
            # audioFile = audio.download(output_path=self.directory, skip_existing=True)

            # os.system(
            #     f'cmd /c "ffmpeg -hide_banner -loglevel error -i "{audioFile}" -vn -ab {audio.abr.split("b")[0]} -ar 48000 -y "{audioOutput}" "')
            # f'cmd /c "ffmpeg -hide_banner -loglevel error -i "{audioFile}" -vn -y "{audioOutput}" "')
            # os.remove(audioFile)

        #     mp3conv320 () {
        # INFILE=$1
        # ffmpeg -i “$INFILE” -vn -ab 320k -ar 44100 -loglevel 48 “${INFILE%.*}.mp3”
        # }

        if not audioOnly:

            if maxQuality:
                video = url.streams.order_by('resolution').last()
            else:
                print(videoQuality)
                print(mime_type)
                print(url)
                video = url.streams.filter(mime_type=mime_type, resolution=videoQuality).first()
                print(video)
            if not video:
                video = url.streams.filter(mime_type=mime_type).first()
                if not video:
                    video = url.streams.get_highest_resolution()
                    videoOutput = self.directory + '/' + title + " ." + video.mime_type.split("/")[1]
                    if not video:
                        self.errorLabel.config(
                            text=self.errorLabel.cget("text") + f" Няма информация за видеото {title}")
                        print("Nqma качеството")
                        self.threadNumber -= 1
                        self.countPlaylist()
                        self.isDownloading = False
                        return
            # @#%Jimmy@#%Neutron@#%boy(boi) genius invents super speed;Ray Sipe;Comedy;Parody author- raysipeladygaga video .webm
            # self.filesize = video.filesize
            # print(mime_type + "AAAAAAAAAAAAA")

            # if videoQuality == "144p" or videoQuality == "240p" or videoQuality == "360p" or videoQuality == "480p" or videoQuality == "720p":
            #     video.download(output_path=self.directory, filename=videoOutput)
            # else:

            audio = url.streams.filter(only_audio=True).order_by('abr').last()
            self.filesize = audio.filesize
            # audioFile = audio.download(output_path=self.directory, filename=title + ' audio.mp3')
            audioFile = audio.download(output_path=self.directory, filename=title + ' audio')

            self.filesize = video.filesize
            # videoFile = video.download(output_path=self.directory,filename=title + ' video .' + mime_type.split("/")[1])
            videoFile = video.download(output_path=self.directory, filename=title + ' video')

            #videoclip = VideoFileClip(videoFile)
            #audioclip = AudioFileClip(audioFile)
            try:
                acodec = "copy"
                if mime_type.split("/")[1] == "mp4":
                    acodec = "aac"
                elif mime_type.split("/")[1] == "webm":
                    acodec = "copy"

                moviepy.video.io.ffmpeg_tools.ffmpeg_merge_video_audio(
                    videoFile, audioFile, videoOutput, vcodec='copy',
                    acodec=acodec,
                    ffmpeg_output=False,
                    logger=None)

                # final_clip = videoclip.set_audio(audioclip)
                # final_clip.write_videofile(videoOutput)
                # try:
                #   os.system(f'cmd /c "ffmpeg -hide_banner -loglevel error -y -i "{videoFile}" -i "{audioFile}" -c copy "{videoOutput}" "')
                # except Exception:
                # os.remove(videoOutput)

                os.remove(audioFile)
                os.remove(videoFile)
            except:
                os.remove(audioFile)
                os.remove(videoFile)

        self.threadNumber -= 1
        self.countPlaylist()
        self.isDownloading = False

    def countPlaylist(self):
        if self.workingWithPlaylist:
            self.currentPlaylistLength += 1
            self.progressLabel.config(text=f"{self.currentPlaylistLength} ot {self.playlistLength} videa/audio")

    def reset(self):
        self.root.destroy()
        self.root = Panel()

    def progress_function(self, chunk, file_handle, bytes_remaining):
        current = ((int(self.filesize) - bytes_remaining) / self.filesize)
        percent = '{0:.1f}'.format(current * 100)
        print(percent)
        # self.sizeLabel.config(text=self.filesize)
        self.progressLabel.config(text=percent)

    def complete_function(self, needs3vars, fundrequires3vars):
        self.progressLabel.config(text="Приключи изтеглянето")

    def __init__(self):
        self.playlistStreams = None
        self.streams = None
        self.url = None
        self.filesize = None
        self.playlist = None
        self.directory = None
        self.label = None
        self.root = Tk()
        self.clickedBarzo = StringVar()
        self.clickedPalno = StringVar()
        self.clicked = StringVar()

        self.root.geometry("400x900")

        self.index = 0

        Label(self.root, text="URL").grid(row=self.index, column=0, columnspan=2)
        self.index += 1
        entry_text = StringVar()
        self.entryURL = Entry(self.root, width=50, textvariable=entry_text)
        self.entryURL.grid(row=self.index, column=0, columnspan=2)
        self.index += 1

        Label(self.root, text="File Name (optional)").grid(row=self.index, column=0, columnspan=2)
        self.index += 1
        self.entryName = Entry(self.root, width=50)
        self.entryName.grid(row=self.index, column=0, columnspan=2)
        self.index += 1

        Button(self.root, text="Избиране на директория", command=self.startingOption).grid(row=self.index, column=0,
                                                                                           columnspan=2)
        self.index += 1
        self.directoryLabel = Label(self.root, text="Избрана директория")
        self.directoryLabel.grid(row=self.index, column=0, columnspan=2)
        self.index += 1

        Button(self.root, text="reset", command=self.reset).grid(row=self.index, column=0)
        self.index += 1
        self.progressLabel = Label(self.root, text="Ред за прогрес")
        self.progressLabel.grid(row=self.index, column=0, columnspan=12)

        self.index += 1
        self.reportLabel = Label(self.root, text="Ред за отчет")
        self.reportLabel.grid(row=self.index, column=0, columnspan=12)

        self.index += 1
        self.sizeLabel = Label(self.root, text="Sizing")
        self.sizeLabel.grid(row=self.index, column=0, columnspan=2)
        self.index += 1
        self.errorLabel = Label(self.root, text="Error List")
        self.errorLabel.grid(row=self.index, column=0)
        self.index += 1

        self.continueButton = Button(self.root, text="Връзката не е заредена", command=self.continueButton)
        self.continueButton.grid(row=self.index, column=0, columnspan=2)

        self.index += 1

        self.label = Label(self.root, text=" ")
        self.label.grid(row=self.index, column=0)
        self.index += 1

        # Execute tkinter
        self.root.mainloop()

    def continueButton(self):
        # print(self.urlVault)
        # print(self.entryURL.get())
        if self.urlVault != self.entryURL.get():
            # self.define()
            t = threading(target=self.define(), daemon=True).start()

        t = threading(target=self.choiceOne(), daemon=True).start()
        # self.choiceOne()
        # return


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
