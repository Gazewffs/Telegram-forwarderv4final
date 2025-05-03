# Complete Guide: Running Telegram Message Forwarder 24/7 with Termux and VPS

This guide will walk you through the setup process to run the Telegram Message Forwarder continuously using Termux and a VPS, with step-by-step instructions even if you have no prior experience.

## Table of Contents
1. [Overview](#overview)
2. [Requirements](#requirements)
3. [Setting Up Termux on Your Android Device](#setting-up-termux-on-your-android-device)
4. [Getting a VPS](#getting-a-vps)
5. [Connecting Termux to Your VPS](#connecting-termux-to-your-vps)
6. [Setting Up the Forwarder on Your VPS](#setting-up-the-forwarder-on-your-vps)
7. [Configuring the Forwarder](#configuring-the-forwarder)
8. [Running the Forwarder 24/7](#running-the-forwarder-24-7)
9. [Managing and Updating Your Forwarder](#managing-and-updating-your-forwarder)
10. [Troubleshooting](#troubleshooting)

## Overview
The setup involves connecting your Android device (with Termux) to a VPS, where the forwarder will run continuously. Termux acts as your control center to access and manage the VPS.

## Requirements
- Android smartphone with Termux app installed
- A VPS (Virtual Private Server) running Linux (Ubuntu recommended)
- Telegram account
- Telegram API credentials

## Setting Up Termux on Your Android Device

1. **Install Termux**
   - Download and install Termux from Google Play Store or F-Droid

2. **Update Termux packages**
   ```bash
   pkg update
   pkg upgrade
   ```

3. **Install required tools**
   ```bash
   pkg install openssh python git nano
   ```

## Getting a VPS

1. **Choose a VPS provider**
   - Recommended options: DigitalOcean, Linode, Vultr, or OVH
   - Sign up for an account

2. **Create a VPS**
   - Select Ubuntu 20.04 or 22.04 LTS
   - Choose the cheapest plan ($5-6/month is sufficient)
   - Complete the setup
   - Note your VPS IP address, username (usually 'root'), and password

## Connecting Termux to Your VPS

1. **Connect to VPS via SSH**
   ```bash
   ssh root@YOUR_VPS_IP
   ```
   - Replace `YOUR_VPS_IP` with your actual VPS IP address
   - When prompted, enter your VPS password
   - Accept the fingerprint by typing 'yes' if asked

2. **Set up SSH key authentication (optional but recommended)**
   
   On your Termux:
   ```bash
   # Generate an SSH key
   ssh-keygen -t rsa
   
   # Copy your public key to the VPS
   ssh-copy-id root@YOUR_VPS_IP
   ```

## Setting Up the Forwarder on Your VPS

1. **Install required packages on VPS**
   ```bash
   apt update
   apt upgrade
   apt install python3 python3-pip git screen
   ```

2. **Create a directory for the forwarder**
   ```bash
   mkdir -p /opt/telegram_forwarder
   cd /opt/telegram_forwarder
   ```

3. **Download the forwarder code**
   
   You have two options:
   
   **Option 1**: Download directly from your Replit project
   ```bash
   # Create a ZIP file of the clean version first
   cd /path/to/telegram_forwarder
   zip -r telegram_forwarder.zip *
   
   # On your VPS, create a directory for the forwarder
   mkdir -p /opt/telegram_forwarder
   
   # Upload the ZIP file to your VPS (from your local machine)
   scp telegram_forwarder.zip root@YOUR_VPS_IP:/opt/telegram_forwarder/
   
   # On VPS, unzip the file
   cd /opt/telegram_forwarder
   apt install unzip
   unzip telegram_forwarder.zip
   ```
   
   **Option 2**: Use GitHub (if you've pushed your code to GitHub)
   ```bash
   git clone YOUR_GITHUB_REPO_URL /opt/telegram_forwarder
   cd /opt/telegram_forwarder
   ```

4. **Install Python dependencies**
   ```bash
   pip3 install telethon flask
   ```

## Configuring the Forwarder

1. **Get Telegram API credentials**
   - Visit [my.telegram.org](https://my.telegram.org) and log in
   - Click on "API Development tools"
   - Create a new application
   - Note your API ID and API Hash

2. **Edit the config file**
   ```bash
   nano config.json
   ```
   
   Update the file with your credentials:
   ```json
   {
       "api_id": "YOUR_API_ID",
       "api_hash": "YOUR_API_HASH",
       "source_channel": "SOURCE_CHANNEL_USERNAME_OR_ID",
       "destination_channel": "DESTINATION_CHANNEL_USERNAME_OR_ID",
       "session_string": "",
       "text_filters": [
           "FILTER_TEXT->REPLACEMENT_TEXT"
       ],
       "replacement_image_path": "replacement_image.png",
       "rate_limit_delay": 3,
       "always_replace_media": false,
       "forward_all_messages": true
   }
   ```
   
   - Save the file with Ctrl+O, then Enter, then Ctrl+X

3. **Initialize the forwarder to authenticate with Telegram**
   ```bash
   python3 main.py
   ```
   
   - You'll be prompted to enter your phone number
   - Enter the verification code sent to your Telegram
   - If you have two-factor authentication, enter your password

## Running the Forwarder 24/7

1. **Set up a screen session**
   ```bash
   screen -S telegram_forwarder
   ```

2. **Start the forwarder**
   ```bash
   cd /opt/telegram_forwarder
   python3 main.py
   ```

3. **Detach from the screen session (to keep it running in background)**
   - Press Ctrl+A, then press D
   
4. **Verify the forwarder is running**
   ```bash
   screen -ls
   ```
   You should see your session listed

## Managing and Updating Your Forwarder

1. **Reattach to the screen session**
   ```bash
   screen -r telegram_forwarder
   ```

2. **Stop the forwarder**
   - Reattach to the screen
   - Press Ctrl+C to stop the forwarder
   - Type `exit` to close the screen session

3. **Update the forwarder**
   - Stop the forwarder
   - Pull the latest code if using Git or upload new files
   - Restart the forwarder in a new screen session

4. **Setting up a system service (optional but recommended)**
   ```bash
   nano /etc/systemd/system/telegram-forwarder.service
   ```
   
   Add this content:
   ```
   [Unit]
   Description=Telegram Message Forwarder
   After=network.target
   
   [Service]
   ExecStart=/usr/bin/python3 /opt/telegram_forwarder/main.py
   WorkingDirectory=/opt/telegram_forwarder
   Restart=always
   RestartSec=10
   User=root
   
   [Install]
   WantedBy=multi-user.target
   ```
   
   Enable and start the service:
   ```bash
   systemctl enable telegram-forwarder
   systemctl start telegram-forwarder
   ```
   
   Check status:
   ```bash
   systemctl status telegram-forwarder
   ```

## Troubleshooting

1. **Check the forwarder status**
   ```bash
   screen -r telegram_forwarder
   ```
   or if using systemd:
   ```bash
   systemctl status telegram-forwarder
   journalctl -u telegram-forwarder
   ```

2. **Common issues and solutions**

   - **Authentication fails**: Make sure API credentials are correct and the session string is valid.
   - **Cannot connect to source channel**: Ensure you're a member of the source channel.
   - **VPS connection lost**: Reconnect from Termux with `ssh root@YOUR_VPS_IP`.
   - **Forwarder stops working**: Check VPS resources (memory/CPU) and ensure Python is running.
   - **Error logs**: Add more detailed logging to debug issues.

3. **If the forwarder stops working**
   - Check if the process is still running
   - Restart the service if needed
   - Check system resources with `top` or `htop`

## Advanced Setup Tips

1. **Set up automatic updates**
   ```bash
   crontab -e
   ```
   
   Add:
   ```
   0 3 * * * cd /opt/telegram_forwarder && git pull && systemctl restart telegram-forwarder
   ```
   
   This will update the code daily at 3 AM and restart the service.

2. **Set up login alerts**
   
   Create a notification when someone logs into your VPS:
   ```bash
   nano /etc/ssh/sshrc
   ```
   
   Add:
   ```bash
   IP=$(echo $SSH_CONNECTION | awk '{print $1}')
   DATETIME=$(date)
   echo "SSH login: $USER from $IP at $DATETIME" | mail -s "SSH Login Alert" your-email@example.com
   ```

3. **VPS monitoring**
   
   Install a simple monitoring tool:
   ```bash
   apt install monit
   ```
   
   Configure monit to monitor your forwarder and restart it if it stops:
   ```bash
   nano /etc/monit/conf.d/telegram-forwarder
   ```
   
   Add:
   ```
   check process telegram-forwarder with pidfile /var/run/telegram-forwarder.pid
     start program = "/bin/systemctl start telegram-forwarder"
     stop program = "/bin/systemctl stop telegram-forwarder"
     if not exists then restart
   ```

---

With this setup, your Telegram Message Forwarder will run 24/7 on your VPS, with Termux providing a convenient way to manage it from your Android device. The system is resilient and will automatically restart if there are any issues.