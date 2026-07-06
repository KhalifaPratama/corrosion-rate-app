@echo off
echo ========================================
echo   SETUP CORROSION RATE APP
echo ========================================
echo.

REM Check if virtual environment exists
if exist "test_env\Scripts\python.exe" (
    echo [OK] Virtual environment found!
    echo.
    echo [1/2] Activating virtual environment...
    call .\test_env\Scripts\activate
    echo.
    
    echo [2/2] Installing/Updating dependencies...
    echo This may take 2-3 minutes...
    echo.
    python -m pip install --upgrade pip --quiet
    pip install -r readme\requirements.txt
    
    if errorlevel 1 (
        echo.
        echo [ERROR] Failed to install some packages
        echo Trying alternative method...
        pip install flask numpy pandas scikit-learn joblib category-encoders
    )
    
    echo.
    echo ========================================
    echo   SETUP COMPLETE!
    echo ========================================
    echo.
    echo Ready to run! Execute:
    echo   RUN_APP.bat
    echo.
) else (
    echo [INFO] Virtual environment not found.
    echo Creating new virtual environment...
    echo.
    
    REM Try to find Python
    where python >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Python not found in PATH!
        echo.
        echo Please install Python 3.8+ from:
        echo https://www.python.org/downloads/
        echo.
        echo Make sure to check "Add Python to PATH"
        echo.
        pause
        exit /b 1
    )
    
    echo [1/3] Creating virtual environment...
    python -m venv test_env
    
    echo [2/3] Activating virtual environment...
    call .\test_env\Scripts\activate
    
    echo [3/3] Installing dependencies...
    python -m pip install --upgrade pip --quiet
    pip install -r readme\requirements.txt
    
    echo.
    echo ========================================
    echo   SETUP COMPLETE!
    echo ========================================
    echo.
    echo Ready to run! Execute:
    echo   RUN_APP.bat
    echo.
)

pause
