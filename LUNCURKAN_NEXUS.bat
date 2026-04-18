@echo off
title N.E.X.U.S AI Launcher
echo ======================================================
echo       N.E.X.U.S GPT AI - DOCKER REPOSITORY
echo ======================================================
echo 1. Memeriksa ketersediaan Docker...
where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Docker tidak terdeteksi! Silakan install Docker Desktop.
    pause
    exit
)

echo 2. Menjalankan Container (Background Mode)...
docker-compose up -d --build

echo 3. Menunggu Server (5 detik)...
timeout /t 5 /nobreak >nul

echo 4. Membuka Dashboard Terpusat di Browser...
start "" "http://localhost:8888/index.html"

echo ======================================================
echo [SESI AKTIF] Database tersimpan di server/nexus_gpt.db
echo Tekan tombol apa saja untuk mematikan server...
echo ======================================================
pause
docker-compose down
exit
