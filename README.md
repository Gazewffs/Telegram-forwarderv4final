# Telegram Message Forwarder

A robust Python-based Telegram message forwarding system with advanced channel resolution, media replacement, and intelligent filtering capabilities.

## Features

- Forward messages from channels where forwarding is disabled
- Replace images with custom replacement images (specifically images with captions)
- Apply text filters to modify message content
- Run 24/7 on VPS or through Termux
- Web interface for easy management and monitoring
- Message tracking to avoid duplicates
- Rate limiting to avoid API restrictions

## Files in this Package

- `main.py` - Main entry point for running the forwarder
- `app.py` - Web interface using Flask
- `forwarder.py` - Core message forwarding functionality
- `config.py` - Configuration handling
- `db_handler.py` - Database management for message tracking
- `filter_manager.py` - Text filtering functionality
- `config.json` - Configuration file (edit with your credentials)
- `replacement_image.png` - The image used to replace captioned images
- `complete_guide.md` - Detailed guide for 24/7 deployment on VPS via Termux
- `setup_guide.md` - Additional setup information
- `requirements.txt` - Required Python packages
- `install.sh` - Installation script for Linux/VPS

## Quick Start

1. Install Python 3.7 or higher
2. Install dependencies: `pip install -r requirements.txt`
3. Edit `config.json` with your API credentials and channel information
4. Run the forwarder: `python main.py`

## Documentation

See the following files for detailed guides:

- `complete_guide.md` - Step-by-step instructions for setting up on VPS with Termux
- `setup_guide.md` - Additional detailed setup information

## Running 24/7

For continuous operation, we recommend:

1. Setting up on a VPS with Linux
2. Managing via Termux from your Android device
3. Using screen or systemd service for persistent operation

Follow the detailed instructions in `complete_guide.md` for the full setup process.

## Customizing

- **Text Filters**: Edit the `text_filters` array in `config.json`
- **Replacement Image**: Replace `replacement_image.png` with your own image
- **Rate Limiting**: Adjust `rate_limit_delay` in `config.json` to avoid API restrictions

## License

This project is licensed under the MIT License