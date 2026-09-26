@echo off
title Cache Cleaner Launcher
echo ========================================================
echo  Cache Cleaner - Pro Developer & System Suite
echo ========================================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [HATA] Python bulunamadi! Lutfen Python'in yuklu ve PATH'e ekli oldugundan emin olun.
    pause
    exit /b 1
)

echo Bagimliliklar kontrol ediliyor...
pip install -r requirements.txt --quiet

echo Uygulama baslatiliyor...
python main.py

if errorlevel 1 (
    echo.
    echo [UYARI] Uygulama sonlandirildi.
    pause
)
