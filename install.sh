#!/bin/bash
# INSTALL OTOMATIS
# @makloYapitpp for NityDizz

clear
echo "🔥 INSTALLING SPAM OTP TOOLS..."
echo "================================"

# Update
pkg update && pkg upgrade -y

# Install Python
pkg install python git -y

# Install Library
pip install requests

# Buat Proxy
cat > proxies.txt << 'EOF'
103.85.23.42:8080
103.85.23.43:8080
103.152.112.120:8080
103.153.233.19:8080
103.149.162.210:8080
EOF

echo ""
echo "✅ INSTALL SELESAI!"
echo "🚀 RUN: python otp_spam.py"
echo "PENGUASA Monzap