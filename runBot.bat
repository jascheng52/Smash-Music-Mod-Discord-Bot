:: Check for Python Installation
python --version 2>NUL
if errorlevel 1 goto errorNoPython

:: Set the path to the directory containing ffmpeg
set "ffmpeg_path=%~dp0ffmpeg\bin"

:: Add the ffmpeg directory to the system PATH
set "PATH=%ffmpeg_path%;%PATH%"

:: Reaching here means Python is installed.
:: Execute stuff...
echo Installing Dependencies...
::python -m pip install -r .\src\requirements.txt
python -m pip install pedalboard
python -m pip install Unidecode
python -m pip install pykakasi
python -m pip install tkcalendar
python -m pip install yt-dlp
python -m pip install -U nextcord[speed]


cd src
python botGui.py  
if errorlevel 1 goto errorRunning
:: Once done, exit the batch file -- skips executing the errorNoPython section
goto:eof

:errorNoPython
echo.
echo Error^: Python not installed or added to PATH variables
echo Press any key to close the window...
pause >nul
goto:eof

:errorRunning
echo.
echo Error^: Error Running Bot
echo Press any key to close the window...
pause >nul
goto:eof

