@echo off
setlocal

REM Selalu bekerja dari folder skrip ini
cd /d "%~dp0"

echo ========================================
echo   SETUP CORROSION RATE APP
echo ========================================
echo.

REM Buat virtual environment bila belum ada (folder test_env tidak ikut di Git,
REM jadi di komputer baru langkah ini yang menyiapkannya)
if not exist "test_env\Scripts\python.exe" (
    echo [INFO] Virtual environment belum ada, membuat yang baru...
    echo.

    where python >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Python tidak ditemukan di PATH!
        echo.
        echo Install Python 3.8+ dari https://www.python.org/downloads/
        echo dan centang "Add Python to PATH".
        echo.
        pause
        exit /b 1
    )

    python -m venv test_env
    if errorlevel 1 (
        echo.
        echo [ERROR] Gagal membuat virtual environment.
        echo.
        pause
        exit /b 1
    )
) else (
    echo [OK] Virtual environment ditemukan.
)

set "PY=test_env\Scripts\python.exe"

echo.
echo [1/2] Memperbarui pip...
"%PY%" -m pip install --upgrade pip --quiet

echo [2/2] Memasang dependensi ^(2-3 menit^)...
echo.
"%PY%" -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERROR] Sebagian paket gagal dipasang, mencoba tanpa versi terkunci...
    "%PY%" -m pip install flask numpy pandas scikit-learn joblib xgboost waitress
    if errorlevel 1 (
        echo.
        echo [ERROR] Instalasi gagal.
        echo.
        echo         Bila pip menyebut "Microsoft Visual C++ 14.0 or greater is
        echo         required", versi Python di komputer ini tidak punya paket
        echo         siap pakai. Pakai Python 3.11 - 3.13 versi standar ^(bukan
        echo         free-threaded / "t"^), hapus folder test_env, lalu ulangi.
        echo         Selain itu, periksa koneksi internet.
        echo.
        pause
        exit /b 1
    )
)

REM Opsional: kompresi respons. app.py menangani ketiadaannya lewat
REM try/except ImportError, jadi kegagalan di sini tidak menggagalkan setup.
if exist "requirements-optional.txt" (
    "%PY%" -m pip install -r requirements-optional.txt
    if errorlevel 1 echo [INFO] Paket opsional dilewati; aplikasi tetap jalan tanpa kompresi.
)

echo.
echo ========================================
echo   SETUP COMPLETE!
echo ========================================
echo.
echo Jalankan aplikasi dengan: RUN_APP.bat
echo.
pause
