from __future__ import unicode_literals
import re ,os
from Parameters import Path, re, os
from yt_dlp import YoutubeDL

# output_path = os.getcwd() + "/url_list"
# file_path = output_path + "/url_list.txt"


output_path = Path(os.getcwd()) / "audio_list"
#Makes the directory for the output of downloads
if not os.path.exists(output_path):
    os.makedirs(output_path)

error_path = Path(os.getcwd()) / "error_links"
if not os.path.exists(error_path):
    os.makedirs(error_path)

error_file = error_path / "error.txt"

#ffmpeg
audio_format = YoutubeDL({'format': 'bestaudio',
                                    'outtmpl' : str(output_path / "%(title)s.%(ext)s"), 
                                    'postprocessors': [{
                                    'key': 'FFmpegExtractAudio',
                                    'preferredcodec': 'mp3',
                                    'preferredquality': '320'
                                     }],
                                    'cachedir': False,
                                    'noplaylist' : True})

def download_song (url):
    #audio_format.cache.remove()
    try:
        audio_format.extract_info(url)
    except:
        error = open(error_file,"a")
        error.write(url + " Invalid Link "+ "\n")
        error.close()
        print("Invalid link: " + url)

#writes youtube urls from a message
def download_urls(msg : str):
    msg_split = re.split(' |\n',msg)
    for x in msg_split:
        if is_youtube(x):
            download_song(x)
            #url_file.write(x + "\n")
    
    
#Basic eval case and praying no troll url to break
def is_youtube(msg : str):
    return msg.__contains__('https') and msg.__contains__('you')


if __name__ == "__main__":
    download_song("httpsyouman")



