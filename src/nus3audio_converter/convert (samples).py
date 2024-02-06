import os, subprocess, re, shutil


def to_48kHz(sample, rate):
    """Convert a sample at a given sample rate to samples at a 48000 rate"""
    return round(sample * (48000 / rate))


try:
    os.mkdir("tmp")
except:
    pass

for x in os.listdir("./input"):
    # Get the sample rate
    sample_rate = input("Sample rate in Hz (leave blank to auto-detect): ")
    if not sample_rate:
        sample_rate = subprocess.Popen(["./tools/sox/sox.exe", "--i", "-r", "./input/%s" % x], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]

    sample_rate = int(sample_rate)
    
    start_loop_point = int(input("Starting loop point for %s (format: samples): " % x))
    end_loop_point = int(input("Ending loop point for %s (format: samples): " % x))
    print("Converting %s....." % x)

    
    subprocess.call(["./tools/sox/sox.exe", "./input/%s" % x, "-r", "48000", "./tmp/tmp.wav"])
    vgmstream_process = subprocess.Popen(["./tools/vgmstream/test.exe", "-m", "./tmp/tmp.wav"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = vgmstream_process.communicate()
    output = output.decode()

    # Convert loop points to samples
    if start_loop_point:
        start_loop_point = to_48kHz(start_loop_point, sample_rate)
    else:
        start_loop_point = 0

    if end_loop_point:
        end_loop_point = to_48kHz(end_loop_point, sample_rate)
    else:
        end_loop_point = re.search("(?<=stream total samples: )(.*)(?= \()", output)[0]

    subprocess.call(["./tools/VGAudioCli.exe", "./tmp/tmp.wav", "./tmp/tmp.lopus", "-l", "%s-%s" % (start_loop_point, end_loop_point), "--bitrate", "64000", "--CBR", "--opusheader", "namco"])
    subprocess.call(["./tools/nus3audio.exe", "-n", "-A", "Coolsonickirby & Pacil Batch Converter", "./tmp/tmp.lopus", "-w", "./output/%s.nus3audio" % os.path.splitext(x)[0]])
    print("Converted %s\n---------------------------------" % x)
