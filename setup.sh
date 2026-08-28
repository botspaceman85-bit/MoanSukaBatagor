#!/bin/bash

echo "🔥 CHAOS TOOLKIT INSTALLER - KAISAR KING'S ⚡️"
echo "============================================"

# Update package
sudo apt update

# Install Python3 & pip
sudo apt install python3 python3-pip -y

# Install dependensi
pip3 install -r requirements.txt

# Buat direktori logs
mkdir -p logs

# Set permission
chmod +x *.py

echo "✅ INSTALLASI SELESAI!"
echo "Jalankan: python3 run_chaos.py"