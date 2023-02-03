##CREDIT TO Pacil Coolsonickirby for source code. It has been modified to fit my needs

from __future__ import unicode_literals
import subprocess, re
from Parameters import os, Path


def to_samples(t):
    """Convert a time (format: MM:SS.ms) to samples at a 48000 rate"""
    # Convert time to integer
    return int(t)
    
current_dir = Path(os.getcwd()) / "nus3audio_converter"
temp_dir = current_dir / "tmp"
input_dir = current_dir.parent / "edited_audio"
sox_exe = current_dir / "tools" / "sox" / "sox.exe"
temp_wav = temp_dir / "tmp.wav"
vgmstram_test_exe = current_dir / "tools" / "vgmstream" / "test.exe"
vgaudio_exe = current_dir / "tools" / "VGAudioCli.exe"
lopus = current_dir / "tmp" / "tmp.lopus"
nus3audio = current_dir / "tools" / "nus3audio.exe"
output_dir = current_dir.parent / "final_audio"

def convert_smash_audio():
    try:
        os.mkdir(str(temp_dir = current_dir / "tmp"))
    except:
        pass
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    count = 0
    added_songs  = open("added_songs.txt", "a")
    for x in os.listdir(str(input_dir)):
        print("Converting %s....." % x)

        subprocess.call([str(sox_exe), str(input_dir / x ),"-r", "48000", str(temp_wav)])
        vgmstream_process = subprocess.Popen([str(vgmstram_test_exe), "-m", str(temp_wav)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = vgmstream_process.communicate()
        output = output.decode()
        

        # Convert loop points to samples
        if False:
            start_loop_point = to_samples(start_loop_point)
        else:
            start_loop_point = 0

        if False:
            end_loop_point = to_samples(end_loop_point)
        else:
            end_loop_point = re.search("(?<=stream total samples: )(.*)(?= \()", str(output))[0]

        extension_index = x.index(".")
        new_name = x[0:extension_index] + ".nus3audio"
        subprocess.call([str(vgaudio_exe), str(temp_wav), str(lopus), "-l", "%s-%s" % (start_loop_point, end_loop_point), "--bitrate", "64000", "--CBR", "--opusheader", "namco"])
        subprocess.call([str(nus3audio), "-n", "-A", "Coolsonickirby & Pacil Batch Converter", lopus, "-w", str(output_dir / new_name) ])
        print("Converted %s\n---------------------------------" % x)
        count += 1
        added_songs.write(x + "\n")
    print("Converted All Files")
    added_songs.close()
    return count

if __name__ == "__main__":
    convert_smash_audio()
