@echo off

REM Check if the application's Python script is running and kill it
tasklist /FI "IMAGENAME eq python.exe" /NH /FO CSV | findstr /R /C:"main.py" > nul
if errorlevel 1 (
    echo Application not running, starting it now...
) else (
    echo Killing existing application instance...
    for /f "tokens=2 delims=," %%i in ('tasklist /NH /FO CSV /FI "IMAGENAME eq python.exe" ^| findstr /R /C:"main.py"') do taskkill /F /PID %%i
)
SET PYTHONPATH=%PYTHONPATH%;f:\cloud\worktoy\src

REM Start the application
python main.py

exit
