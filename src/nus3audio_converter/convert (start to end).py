import os, subprocess, re, shutil


def to_samples(t):
    """Convert a time (format: MM:SS.ms) to samples at a 48000 rate"""
    # Convert time to integer
    return int(t)
    


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

    # Convert loop points to samples
    if False:
        start_loop_point = to_samples(start_loop_point)
    else:
        start_loop_point = 0

    if False:
        end_loop_point = to_samples(end_loop_point)
    else:
        end_loop_point = re.search("(?<=stream total samples: )(.*)(?= \()", output)[0]

    subprocess.call(["./tools/VGAudioCli.exe", "./tmp/tmp.wav", "./tmp/tmp.lopus", "-l", "%s-%s" % (start_loop_point, end_loop_point), "--bitrate", "64000", "--CBR", "--opusheader", "namco"])
    subprocess.call(["./tools/nus3audio.exe", "-n", "-A", "Coolsonickirby & Pacil Batch Converter", "./tmp/tmp.lopus", "-w", "./output/%s.nus3audio" % os.path.splitext(x)[0]])
    print("Converted %s\n---------------------------------" % x)
