@echo off
echo ========================================
echo   BUILD EXECUTABLE
echo ========================================
echo.

call .\test_env\Scripts\activate

echo [1/2] Cleaning old build...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo.
echo [2/2] Building executable...
echo This will take 3-5 minutes...
echo.

.\test_env\Scripts\pyinstaller.exe CorrosionRateApp_simple.spec --clean --noconfirm

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo   BUILD SUCCESS!
echo ========================================
echo.
echo Executable: dist\CorrosionRateApp.exe
echo.
dir dist\CorrosionRateApp.exe
echo.
echo To test:
echo   cd dist
echo   CorrosionRateApp.exe
echo   Open browser: http://localhost:5000
echo.
pause

