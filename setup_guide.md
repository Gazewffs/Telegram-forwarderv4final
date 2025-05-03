# Telegram Message Forwarding System Setup Guide

This document provides step-by-step instructions for setting up and running the Telegram message forwarding system on a VPS connected to Termux. This system allows you to forward messages from a source Telegram channel (where forwarding might be disabled) to another channel, with the ability to replace images and filter text.

## Table of Contents
1. [Requirements](#requirements)
2. [Getting Telegram API Credentials](#getting-telegram-api-credentials)
3. [Initial Setup on Your PC/Laptop](#initial-setup-on-your-pclaptop)
4. [Setting Up on a VPS](#setting-up-on-a-vps)
5. [Initial Setup on Termux](#initial-setup-on-termux)
6. [Configuring the Forwarder](#configuring-the-forwarder)
7. [Running the Forwarder](#running-the-forwarder)
8. [Running 24/7 on VPS](#running-24-7-on-vps)
9. [Text Filtering Options](#text-filtering-options)
10. [Troubleshooting](#troubleshooting)

## Requirements

- Telegram account
- PC/Laptop OR an Android device with Termux app installed
- VPS running Linux (Ubuntu/Debian recommended) for 24/7 operation
- Python 3.7 or higher

## Getting Telegram API Credentials

1. Visit [my.telegram.org](https://my.telegram.org) and log in with your phone number
2. Click on "API Development tools"
3. Create a new application:
   - App title: Your choice (e.g., "Message Forwarder")
   - Short name: Your choice (e.g., "forwarder")
   - Platform: Desktop
   - Description: "Personal message forwarding tool"
4. Click "Create Application"
5. Note down your **API ID** and **API Hash** - you will need these later

## Initial Setup on Your PC/Laptop

Follow these steps if you're setting up on a PC or laptop first:

1. Clone the repository or download the code:
   ```
   git clone https://github.com/yourusername/telegram-forwarder.git
   cd telegram-forwarder
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
   
3. Run the web interface:
   ```
   python app.py
   ```

4. Open your browser and go to `http://localhost:5000` to access the configuration interface

## Setting Up on a VPS

For 24/7 operation, you'll need to set up the forwarder on a VPS:

1. Connect to your VPS via SSH:
   ```
   ssh username@your-vps-ip
   ```

2. Install Python and required packages:
   ```
   sudo apt update
   sudo apt install -y python3 python3-pip git screen
   ```

3. Clone the repository:
   ```
   git clone https://github.com/yourusername/telegram-forwarder.git
   cd telegram-forwarder
   ```

4. Install the required dependencies:
   ```
   pip3 install -r requirements.txt
   ```

5. Create a configuration file:
   ```
   nano config.json
   ```
   
   Add your configuration (or use the web interface later):
   ```json
   {
     "api_id": "YOUR_API_ID",
     "api_hash": "YOUR_API_HASH",
     "source_channel": "SOURCE_CHANNEL_USERNAME_OR_ID",
     "destination_channel": "DESTINATION_CHANNEL_USERNAME_OR_ID",
     "text_filters": ["text to filter", "/regex pattern/"],
     "rate_limit_delay": 3
   }
   ```

6. Run the web interface (optional, for easier configuration):
   ```
   python3 app.py
   ```
   
   If your VPS has a firewall, ensure port 5000 is open or use SSH port forwarding.

## Initial Setup on Termux

For Android users who want to run the forwarder on their phone via Termux:

1. Install Termux from the Google Play Store or F-Droid
2. Open Termux and update packages:
   ```
   pkg update && pkg upgrade -y
   ```

3. Install necessary packages:
   ```
   pkg install python openssh git -y
   ```

4. Clone the repository:
   ```
   git clone https://github.com/yourusername/telegram-forwarder.git
   cd telegram-forwarder
   ```

5. Install the required Python packages:
   ```
   pip install telethon flask
   ```

6. Run the forwarder:
   ```
   python app.py
   ```
   
7. Access the web interface by opening a browser and navigating to `http://localhost:5000`

## Configuring the Forwarder

Through the web interface:

1. Enter your Telegram API ID and API Hash
2. Enter the source channel username or ID (where you want to get messages from)
3. Enter the destination channel username or ID (where you want to forward messages to)
4. Add any text filters you want to apply to messages
5. Click "Save Configuration"
6. Click "Start Forwarder" to begin forwarding messages

On first start, you'll need to authenticate with Telegram:
1. Enter your phone number when prompted
2. Enter the authentication code sent to your Telegram account
3. If you have two-factor authentication enabled, enter your password

## Running the Forwarder

### Starting the Forwarder
1. Through the web interface: Click the "Start Forwarder" button
2. Through the command line: Run `python main.py`

### Stopping the Forwarder
1. Through the web interface: Click the "Stop Forwarder" button
2. Through the command line: Press Ctrl+C

## Running 24/7 on VPS

To keep the forwarder running after you disconnect from your VPS:

### Using Screen (recommended)
```
screen -S forwarder
python main.py
```
Then press Ctrl+A followed by D to detach from the screen.

To reconnect later:
```
screen -r forwarder
```

### Using nohup
```
nohup python main.py > forwarder.log 2>&1 &
```

This will run the forwarder in the background and save the output to forwarder.log.

### Setting up as a Systemd Service (Advanced)

1. Create a service file:
   ```
   sudo nano /etc/systemd/system/telegram-forwarder.service
   ```

2. Add the following content (replace paths as needed):
   ```
   [Unit]
   Description=Telegram Message Forwarder
   After=network.target

   [Service]
   Type=simple
   User=YOUR_USERNAME
   WorkingDirectory=/path/to/telegram-forwarder
   ExecStart=/usr/bin/python3 /path/to/telegram-forwarder/main.py
   Restart=on-failure

   [Install]
   WantedBy=multi-user.target
   ```

3. Enable and start the service:
   ```
   sudo systemctl enable telegram-forwarder
   sudo systemctl start telegram-forwarder
   ```

4. Check the status:
   ```
   sudo systemctl status telegram-forwarder
   ```

## Text Filtering Options

The forwarder supports several types of text filters:

1. **Simple Text Removal**:
   ```
   "text_filters": ["Text to remove", "@username"]
   ```
   This will remove the specified text from all messages.

2. **Regex Pattern Matching**:
   ```
   "text_filters": ["/pattern to match/", "/\\d{10}/"]
   ```
   This will remove text matching the regex patterns. In the example, the second pattern removes all 10-digit numbers.

3. **Text Replacement**:
   ```
   "text_filters": ["original->replacement", "Buy Now->Purchase"]
   ```
   This will replace occurrences of "original" with "replacement". In the example, "Buy Now" becomes "Purchase".

4. **Regex Replacement**:
   ```
   "text_filters": ["/pattern/->replacement", "/https?:\\/\\/\\S+/->"]
   ```
   This replaces text matching the regex pattern with the specified replacement. In the example, all URLs are removed.

## Troubleshooting

### Common Issues

1. **Authentication Issues**:
   - Make sure your API ID and API Hash are correct
   - Check that your account is not limited or banned by Telegram
   - Try removing the session file and authenticating again

2. **Channel Access Issues**:
   - Ensure your account is a member of both the source and destination channels
   - For private channels, use the channel ID instead of the username
   - Make sure you have permission to post in the destination channel

3. **Message Forwarding Issues**:
   - Check the logs for errors
   - Make sure the forwarder is running
   - Verify that your message filters aren't removing too much content

4. **Rate Limiting**:
   - If you're seeing FloodWaitError messages, increase the rate_limit_delay value
   - Consider using multiple accounts if you need to forward many messages

### Getting Help

If you encounter issues:
1. Check the logs for errors
2. Try running the forwarder in debug mode: `python main.py --debug`
3. Look for similar issues in the GitHub repository