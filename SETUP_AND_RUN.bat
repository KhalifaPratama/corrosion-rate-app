@echo off
setlocal
cls

REM ==========================================================================
REM  SETUP_AND_RUN.bat
REM  Untuk komputer yang BELUM punya virtual environment (mis. hasil git clone
REM  di device baru — folder test_env tidak ikut di Git).
REM  Sekali klik: buat venv -> pasang dependensi -> jalankan aplikasi.
REM  Aman dijalankan berulang: kalau venv & dependensi sudah ada, langsung run.
REM ==========================================================================

REM Selalu bekerja dari folder skrip ini, bukan folder tempat cmd dibuka
cd /d "%~dp0"

REM Konsol Windows default (code page 437) tidak bisa menampilkan emoji pada
REM pesan startup app.py; tanpa ini prosesnya bisa mati sebelum server jalan.
chcp 65001 >nul
set PYTHONIOENCODING=utf-8

set "VENV=test_env"
set "VPY=%VENV%\Scripts\python.exe"
set "MARK=%VENV%\.deps_installed"

echo ========================================
echo   CORROSION RATE APP - SETUP ^& RUN
echo ========================================
echo.

if not exist "requirements.txt" (
    echo [ERROR] requirements.txt tidak ada di folder ini:
    echo         %CD%
    echo.
    echo         Pastikan file .bat ini berada di folder project yang sama
    echo         dengan app.py dan requirements.txt.
    echo.
    pause
    exit /b 1
)

if exist "%VPY%" goto venv_siap

REM -------- 1. Buat virtual environment --------
echo [1/3] Virtual environment belum ada, membuat "%VENV%"...

REM Utamakan launcher "py" karena "python" di Windows sering hanya stub
REM Microsoft Store yang tidak bisa dipakai.
set "BOOT="
py -3 -c "import sys" >nul 2>&1
if not errorlevel 1 set "BOOT=py -3"
if defined BOOT goto buat_venv

python -c "import sys" >nul 2>&1
if not errorlevel 1 set "BOOT=python"
if defined BOOT goto buat_venv

echo.
echo [ERROR] Python tidak ditemukan di komputer ini.
echo.
echo         1. Install Python 3.8+ dari https://www.python.org/downloads/
echo         2. Saat instalasi, centang "Add Python to PATH"
echo         3. Tutup jendela ini, lalu jalankan file ini lagi
echo.
pause
exit /b 1

:buat_venv
echo       Memakai interpreter: %BOOT%
%BOOT% -m venv "%VENV%"
if errorlevel 1 (
    echo.
    echo [ERROR] Gagal membuat virtual environment.
    echo         Coba jalankan manual untuk melihat pesan aslinya:
    echo         %BOOT% -m venv %VENV%
    echo.
    pause
    exit /b 1
)
echo       Selesai.
goto pasang_deps

:venv_siap
echo [1/3] Virtual environment sudah ada: %VENV%

:pasang_deps
REM -------- 2. Pasang dependensi (dilewati bila sudah pernah sukses) --------
if exist "%MARK%" (
    echo [2/3] Dependensi sudah terpasang, dilewati.
    goto jalankan
)

echo [2/3] Memasang dependensi. Butuh koneksi internet, sekitar 2-5 menit...
echo.
"%VPY%" -m pip install --upgrade pip --quiet
"%VPY%" -m pip install -r requirements.txt
if not errorlevel 1 goto deps_ok

echo.
echo [WARN] Versi terkunci di requirements.txt gagal dipasang.
echo        Mencoba lagi tanpa penguncian versi...
echo.
"%VPY%" -m pip install flask flask-compress numpy pandas scikit-learn joblib category-encoders xgboost waitress
if not errorlevel 1 goto deps_ok

echo.
echo [ERROR] Instalasi dependensi gagal.
echo         Periksa koneksi internet, lalu jalankan file ini lagi.
echo.
pause
exit /b 1

:deps_ok
echo ok> "%MARK%"
echo.
echo       Dependensi terpasang.

:jalankan
REM -------- 3. Jalankan aplikasi --------
"%VPY%" -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Dependensi tidak lengkap di venv ini.
    echo         Hapus folder "%VENV%" lalu jalankan file ini lagi.
    echo.
    pause
    exit /b 1
)

REM Port bisa diganti dari luar, mis. "set FLASK_PORT=8080" sebelum menjalankan
if not defined FLASK_PORT set "FLASK_PORT=5000"

echo.
echo [3/3] Menjalankan server...
echo.
echo       Buka di browser : http://localhost:%FLASK_PORT%
echo       Menghentikan    : Ctrl+C
echo.

"%VPY%" app.py

REM Jendela sengaja tidak langsung tertutup, supaya pesan error tetap terbaca
echo.
echo [INFO] Server berhenti dengan exit code %ERRORLEVEL%.
pause
