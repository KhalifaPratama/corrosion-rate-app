@echo off
setlocal
cls

REM ==========================================================================
REM  SETUP_AND_RUN.bat
REM  Untuk komputer yang BELUM punya virtual environment (mis. hasil git clone
REM  di device baru - folder test_env tidak ikut di Git).
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

REM Satu baris Python yang dipakai berulang untuk menolak interpreter yang
REM tidak layak: exit code 1 bila build free-threaded (Py_GIL_DISABLED), yaitu
REM varian yang hampir tidak punya wheel siap pakai sehingga pip memaksa
REM compile dari source dan menuntut Visual C++ Build Tools.
set "CEKPY=import sysconfig,sys; sys.exit(1 if sysconfig.get_config_var('Py_GIL_DISABLED') else 0)"

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

REM -------- 1. Siapkan virtual environment --------
if not exist "%VPY%" goto pilih_python

REM Venv yang sudah ada belum tentu layak. Venv gagal dari percobaan sebelumnya
REM tetap tertinggal di disk, dan tanpa pemeriksaan ini script akan memakainya
REM lagi sehingga error yang sama terulang walau Python-nya sudah diperbaiki.
"%VPY%" -c "%CEKPY%" >nul 2>&1
if not errorlevel 1 goto venv_siap

echo [1/3] Virtual environment lama tidak layak pakai, dibuat ulang...
echo       ^(interpreternya rusak atau build free-threaded^)
echo.
rmdir /s /q "%VENV%"
if exist "%VPY%" (
    echo [ERROR] Gagal menghapus folder "%VENV%".
    echo         Tutup semua jendela/terminal yang memakainya, lalu ulangi.
    echo.
    pause
    exit /b 1
)

:pilih_python
echo [1/3] Menyiapkan virtual environment "%VENV%"...

REM Utamakan launcher "py" dengan versi eksplisit: "py -3" mengambil versi
REM TERBARU yang terpasang, dan itu bisa saja build free-threaded yang
REM dependensinya tidak bisa dipasang tanpa compiler.
set "BOOT="
call :coba "py -3.13"
call :coba "py -3.12"
call :coba "py -3.11"
call :coba "py -3"
call :coba "python"
if defined BOOT goto buat_venv

echo.
echo [ERROR] Tidak ada Python yang cocok di komputer ini.
echo.
echo         Yang dibutuhkan: Python 3.11 - 3.13 versi standar.
echo.
echo         1. Unduh dari https://www.python.org/downloads/
echo         2. Saat instalasi centang "Add Python to PATH", dan JANGAN
echo            centang opsi free-threaded / "no GIL" ^(3.14t dan sejenisnya
echo            belum punya paket siap pakai untuk aplikasi ini^)
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

REM %VPY% sengaja tidak dikutip: for /f salah mengurai kutip bersarang dan
REM hasilnya jadi kosong. Aman karena path-nya relatif dan tanpa spasi.
set "PYVER=?"
for /f "delims=" %%v in ('%VPY% -c "import sys; print(sys.version.split()[0])" 2^>nul') do set "PYVER=%%v"
echo [2/3] Memasang dependensi untuk Python %PYVER%.
echo       Butuh koneksi internet, sekitar 2-5 menit...
echo.
"%VPY%" -m pip install --upgrade pip --quiet
"%VPY%" -m pip install -r requirements.txt
if errorlevel 1 goto deps_gagal

REM Paket opsional dipasang terpisah dan kegagalannya sengaja tidak fatal:
REM app.py sudah menangani ketiadaannya lewat try/except ImportError.
if not exist "requirements-optional.txt" goto deps_ok
"%VPY%" -m pip install -r requirements-optional.txt
if errorlevel 1 echo       [INFO] Paket opsional dilewati; aplikasi tetap jalan tanpa kompresi.
goto deps_ok

:deps_gagal
echo.
echo [ERROR] Instalasi dependensi gagal ^(Python %PYVER%^).
echo.
echo         Periksa pesan pip di atas:
echo.
echo         - Ada "Microsoft Visual C++ 14.0 or greater is required"?
echo           Berarti versi Python ini tidak punya paket siap pakai dan pip
echo           mencoba meng-compile sendiri. Solusinya BUKAN memasang
echo           compiler, melainkan memakai Python 3.11 - 3.13 versi standar
echo           ^(bukan free-threaded / "t"^): install dari python.org, hapus
echo           folder "%VENV%", lalu jalankan file ini lagi.
echo.
echo         - Ada "Could not find a version" atau timeout?
echo           Kemungkinan koneksi internet atau proxy. Ulangi setelah
echo           koneksi stabil.
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
exit /b %ERRORLEVEL%

REM -------- Subrutin: terima kandidat interpreter bila layak --------
REM Kandidat pertama yang lolos dipakai; sisanya dilewati tanpa dieksekusi.
:coba
if defined BOOT goto :eof
%~1 -c "%CEKPY%" >nul 2>&1
if errorlevel 1 goto :eof
set "BOOT=%~1"
goto :eof
