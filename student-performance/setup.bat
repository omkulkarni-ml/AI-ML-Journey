@echo off
echo ====================================
echo Student Performance Predictor Setup
echo ====================================
echo.

cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Python version:
python --version
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Node.js is not installed or not in PATH
    echo Please install Node.js 18+ from https://nodejs.org
    echo Frontend setup will be skipped.
    echo.
)

REM Setup Python virtual environment
echo Setting up Python virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing Python dependencies...
pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)

echo.
echo Setting up environment file...
if not exist "api\.env" (
    copy "api\.env.example" "api\.env"
    echo Environment file created. Please edit api\.env with your settings.
) else (
    echo Environment file already exists.
)

REM Setup frontend if Node.js is available
node --version >nul 2>&1
if errorlevel 0 (
    echo.
    echo Setting up frontend...
    cd frontend
    
    if not exist "node_modules" (
        echo Installing Node.js dependencies...
        npm install
        if errorlevel 1 (
            echo WARNING: Failed to install frontend dependencies
        )
    ) else (
        echo Frontend dependencies already installed.
    )
    
    cd ..
)

echo.
echo ====================================
echo Setup Complete!
echo ====================================
echo.
echo Next steps:
echo.
echo 1. Configure environment variables:
echo    Edit api\.env with your settings
echo.
echo 2. Start the API server:
echo    cd api
echo    python app.py
echo.
echo 3. Start the frontend (in a new terminal):
echo    cd frontend
echo    npm run dev
echo.
echo 4. Open your browser and navigate to:
echo    http://localhost:5173
echo.
echo Default login credentials:
echo    Create a new account at http://localhost:5173/signup
echo.
echo ====================================
pause
