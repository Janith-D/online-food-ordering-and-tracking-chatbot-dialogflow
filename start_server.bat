@echo off
REM Food Ordering Chatbot - Windows Startup Script

echo ================================================
echo Food Ordering Chatbot - Backend Server
echo ================================================
echo.

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment not found. Using global Python.
)

REM Check if .env file exists
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and configure your database settings.
    echo.
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo.
    echo Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo Starting FastAPI server...
echo Server will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py

pause
