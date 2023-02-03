from __future__ import unicode_literals
import pedalboard, re, cutlet
from Parameters import Path, os
from pedalboard import io , Compressor, Gain
from pedalboard.io import AudioFile
from downloadYou import error_file
from unidecode import unidecode 
# dir  = Path(os.getcwd() )
# destS = Path("audio_list/Sen no Kiseki III OST (First Volume) - Sword of Biting Gale.mp3")
# destS = dir / destS
# destF = Path("audio_list/Sen no Kiseki III OST (First Volume) - Sword of Biting GaleF.mp3")
# destF = dir / destF
base_audio = Path(os.getcwd())  / "audio_list"
edited_audio = Path(os.getcwd()) / "edited_audio"
need_rename = Path(os.getcwd()) / "need_rename"
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
gain_db = 13

jp_translate = cutlet.Cutlet()

compress = Compressor(threshold_db = threshold, ratio = ratio, 
                        attack_ms = attack_ms, release_ms = release_ms)
gain = Gain(gain_db = gain_db)

board = pedalboard.Pedalboard([compress, gain])

def edit_audio():
    for file in os.listdir(base_audio):
        try:
            print("Compressing " + file)
            file_path = base_audio / file

            with AudioFile(str(file_path),"r") as f:
                audio = f.read(f.frames)
                samplerate = f.samplerate
            newSound = board(audio,samplerate)
            #Checks for japanese characters and translates
            #Note other non-ascii characters is moved to rename folder
            if not file.isascii():
                #translate adds a space after for some reason after extension .
                index_extension = file.rindex(".")
                trans_name = jp_translate.romaji(file[0:index_extension], title = True)
                #Incase japanese coversion does not fix decodes to asciii but could lose name
                #Check file for original name
                if not trans_name.isascii() or "?" in trans_name:
                    asciiName = unidecode(file)
                    rename = open(renameFile, "a")
                    rename.write("Original Name: " + file + " --> New Name: " + asciiName + "\n")
                    rename.close()
                    new_path = edited_audio / asciiName
                else:
                    #Cutlet for some reason converts valid characters such as ／ into a / which makes it not longer a valid file path, 
                    #trying to remove most but it is not exhaustive
                    trans_name = re.sub(r'[\\/*?:"<>|]'," ",trans_name)
                    new_path = edited_audio / (trans_name +file[index_extension:])      
            else:
                new_path = edited_audio / file
            with AudioFile(str(new_path),"w", samplerate, newSound.shape[0]) as f:
                f.write(newSound)
            print("Compress Success at " + str(new_path))
        except Exception as e:
            print(e)
            try:
                error = open(error_file,"a")
                error.write(file + " could not open need rename "+ "\n")
                error.close()
            except:
                print('Unable to write ' + file + " to error file") 
    print("Compressed Songs Completed")

if __name__ == "__main__":
    edit_audio()




