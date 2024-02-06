from __future__ import unicode_literals
import re ,os
from pathlib import Path
from yt_dlp import YoutubeDL
import yt_dlp as ydl
from Alerts import Alerts
import sys
# output_path = os.getcwd() + "/url_list"
# file_path = output_path + "/url_list.txt"

ffmpeg_path =  Path(getattr(sys, '_MEIPASS', Path.cwd())) / 'ffmpeg' / 'bin'
output_path = Path(os.getcwd()) / "bot_files"/ "raw_audio"
#Makes the directory for the output of downloads
if not os.path.exists(output_path):
    os.makedirs(output_path)

error_path = Path(os.getcwd()) / "bot_files"/ "error_links"
if not os.path.exists(error_path):
    os.makedirs(error_path)

error_file = error_path / "error.txt"

#ffmpeg
audio_format = YoutubeDL({'format': 'bestaudio',
                                    'outtmpl' : str(output_path / "%(title)s.%(ext)s"), 
                                    'logtostderr': True,
                                    'postprocessors': [{
                                    'key': 'FFmpegExtractAudio',
                                    'preferredcodec': 'mp3',
                                    'preferredquality': '320',
                                     }],
                                    'cachedir': False,
                                    'noplaylist' : True,
                                    'ffmpeg_location': str(ffmpeg_path)
                                    })

def download_song (url):
    #audio_format.cache.remove()
    try:
        print("Downloading ... -", url)
        res = audio_format.extract_info(url)
        print(Alerts.DOWNLOADED, res['title'])
        return True
    except Exception as e:
        print(e)
        error = open(error_file,"a")
        error.write(url + " Invalid Link "+ "\n")
        error.close()
        print(Alerts.WARNING + " FAILED TO PROCESS " + url)
        return False

#writes youtube urls from a message
def download_urls(msg : str):
    msg_split = re.split(' |\n',msg)
    counter = 0
    for x in msg_split:
        if is_youtube(x):
            if(download_song(x)):
                counter = counter + 1

            #url_file.write(x + "\n")
    return counter
    
#Basic eval case and praying no troll url to break
def is_youtube(msg : str):
    return msg.__contains__('https') and msg.__contains__('you')


if __name__ == "__main__":
    download_song("https://youtu.be/e1xCOsgWG0M?si=q7vcdSnJIZjfIKwj")



