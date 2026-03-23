@echo off
REM Personal Assistant Chatbot - Web Version
REM Installs dependencies and starts the web server

echo.
echo ================================
echo   Personal Assistant Chatbot
echo   Web Version
echo ================================
echo.

cd /d "%~dp0"

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Start the web server
echo.
echo Starting web server...
echo.
python app.py

pause
