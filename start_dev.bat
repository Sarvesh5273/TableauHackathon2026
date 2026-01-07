@echo off
echo 🚀 Starting Hackathon Environment...

:: 1. Start the Flask Server (The Brain)
start "Flask Server" cmd /k "venv\Scripts\activate && python scripts\server.py"

:: 2. Start the Ngrok Tunnel (The Bridge)
:: Note: This will open a window showing your NEW URL.
start "Ngrok Tunnel" cmd /k "ngrok http 5000"

echo ✅ Systems Online.
echo ⚠️  REMINDER: Copy your NEW ngrok URL from the tunnel window!
pause