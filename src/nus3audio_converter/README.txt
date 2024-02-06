To convert your audio files to NUS3Audio files, put the audio files in the input folder and run one of the convert scripts. The converted files will be in the output folder.

If you're on Windows, you'll want to run the ones that end in ".exe". Otherwise, you'll have to install Python and run the ".py" files using Python.

The standard convert file will ask you for loop points in MM:SS.ms format for each file. There's no hard limit on how many digits you can have of minutes, seconds, or milliseconds.

convert (no loop) won't loop the files. They'll just play once, and that's it.

convert (start to end) will loop the files from the start to the end. Naturally, it won't ask you for loop points.

convert (samples) will ask for the loop points in samples instead of seconds. You can specify the sampling rate, but if you don't, the program will auto-detect it for you.

If prompted for the starting loop point, and you leave it blank, it'll just use the beginning of the song. Likewise, the end of the song will be used for the ending loop point if you leave that blank (just like smashultimatetools).

If find any bugs or have any feature requests, message Pacil on Gamebanana or on the modding Discord.

This batch NUS3Audio Converter was made by Pacil and Coolsonickirby. Please credit them if you use it.