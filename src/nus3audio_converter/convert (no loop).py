import os, subprocess, re, shutil

try:
    os.mkdir("tmp")
except:
    pass

for x in os.listdir("./input"):
    print("Converting %s....." % x)
    
    subprocess.call(["./tools/sox/sox.exe", "./input/%s" % x, "-r", "48000", "./tmp/tmp.wav"])
    vgmstream_process = subprocess.Popen(["./tools/vgmstream/test.exe", "-m", "./tmp/tmp.wav"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = vgmstream_process.communicate()
    output = output.decode()
    total_streams = re.search("(?<=stream total samples: )(.*)(?= \()", output)[0]
    subprocess.call(["./tools/VGAudioCli.exe", "./tmp/tmp.wav", "./tmp/tmp.lopus", "--bitrate", "64000", "--CBR", "--opusheader", "namco"])
    subprocess.call(["./tools/nus3audio.exe", "-n", "-A", "Coolsonickirby Batch Converter", "./tmp/tmp.lopus", "-w", "./output/%s.nus3audio" % os.path.splitext(x)[0]])
    print("Converted %s\n---------------------------------" % x)
