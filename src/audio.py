from __future__ import unicode_literals
import pedalboard, re, sys
from Parameters import Path, os
from pedalboard import io , Compressor, Gain
from pedalboard.io import AudioFile
from downloadYou import error_file
from unidecode import unidecode 
from Alerts import Alerts
import pykakasi


def has_japanese_or_chinese(text):
    japanese_pattern = re.compile(u'[\u3040-\u309F\u30A0-\u30FF\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF]+')

    chinese_pattern = re.compile(u'[\u4E00-\u9FFF]+')

    return bool(japanese_pattern.search(text)) or bool(chinese_pattern.search(text))


trans_init = pykakasi.kakasi()
def convert_jp(text):
    trans = trans_init.convert(text)
    trans_string = ""
    for part in trans:
        if(part['hepburn'] == ''):
            trans_string = trans_string+part['orig']
            pass
        trans_string = trans_string + ' '+ part['hepburn']
    return trans_string

# dir  = Path(os.getcwd() )
# destS = Path("audio_list/Sen no Kiseki III OST (First Volume) - Sword of Biting Gale.mp3")
# destS = dir / destS
# destF = Path("audio_list/Sen no Kiseki III OST (First Volume) - Sword of Biting GaleF.mp3")
# destF = dir / destF
base_audio = Path(os.getcwd()) / "bot_files"/ "raw_audio"
edited_audio = Path(os.getcwd()) / "bot_files"/ "compressed_audio"
need_rename = Path(os.getcwd()) / "bot_files"/ "need_rename"
renameFile = need_rename / "rename_file.txt"


if not os.path.exists(edited_audio):
    os.makedirs(edited_audio)

if not os.path.exists(need_rename):
    os.makedirs(need_rename)

#Base setting could be tweeked better to work for most file, no peaking please prayage
threshold = -30
ratio = 3
attack_ms = 200
release_ms = 1000
gain_db = 14


compress = Compressor(threshold_db = threshold, ratio = ratio, 
                        attack_ms = attack_ms, release_ms = release_ms)
gain = Gain(gain_db = gain_db)

board = pedalboard.Pedalboard([compress, gain])

def edit_audio():
    for file in os.listdir(base_audio):
        try:
            print("Compressing... " + file)
            file_path = base_audio / file

            with AudioFile(str(file_path),"r") as f:
                audio = f.read(f.frames)
                samplerate = f.samplerate
            newSound = board(audio,samplerate)

            index_extension = file.rindex(".")
            file_stem_name = file[0:index_extension]
            new_path = edited_audio / file
            #Checks for japanese characters and translates
            #Note other non-ascii characters is moved to rename folder
            if not file_stem_name.isascii():
                #translate adds a space after for some reason after extension .
                if(has_japanese_or_chinese(file_stem_name)):
                    file_stem_name = convert_jp(file_stem_name)
                file_stem_name = unidecode(file_stem_name)
                #Check file for original name
                rename = open(renameFile, "a", encoding='utf8')
                rename.write(file + " ---> " + file_stem_name + "\n")
                rename.close()
                #non allowed window file characters
                file_stem_name = re.sub(r'[\\/*?:"<>|]',"",file_stem_name) 
                new_path = edited_audio / file_stem_name
                
            with AudioFile(str(new_path) +'.mp3',"w", samplerate, newSound.shape[0]) as f:
                f.write(newSound)
            print(Alerts.COMPRESSED, "with name", file_stem_name)
        except Exception as e:
            print(e)
            try:
                error = open(error_file,"a")
                error.write(file + " could not open need rename "+ "\n")
                error.close()
            except:
                print('Unable to write ' + file + " to error file") 
    print("Compressed Songs Completed")

# if __name__ == "__main__":
#     edit_audio()




