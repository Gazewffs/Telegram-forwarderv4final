#!/bin/bash

# Simple installation script for Telegram Message Forwarder
# This script will set up the environment and install required dependencies

echo "======================================"
echo "Telegram Message Forwarder Installation"
echo "======================================"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
  echo "Please run as root or with sudo"
  exit 1
fi

# Update system packages
echo "[1/5] Updating system packages..."
apt update && apt upgrade -y

# Install required system dependencies
echo "[2/5] Installing required system packages..."
apt install -y python3 python3-pip python3-venv screen git

# Create virtual environment
echo "[3/5] Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "[4/5] Installing Python dependencies..."
pip install -r requirements.txt

# Setup as a service
echo "[5/5] Setting up service..."
cat > /etc/systemd/system/telegram-forwarder.service << EOF
[Unit]
Description=Telegram Message Forwarder
After=network.target

[Service]
ExecStart=$(pwd)/venv/bin/python3 $(pwd)/main.py
WorkingDirectory=$(pwd)
Restart=always
RestartSec=10
User=root

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload

echo "======================================"
echo "Installation complete!"
echo ""
echo "Next steps:"
echo "1. Edit config.json with your Telegram API credentials"
echo "2. Run 'python3 main.py' to authenticate with Telegram"
echo "3. Start the service: systemctl start telegram-forwarder"
echo "4. Enable autostart: systemctl enable telegram-forwarder"
echo ""
echo "To check status: systemctl status telegram-forwarder"
echo "To view logs: journalctl -u telegram-forwarder"
echo "======================================"