# Motion Detection Security System

This project detects motion using OpenCV and sends an email alert with an image attachment when motion is detected.

## Features
- Real-time motion detection
- Email notification with image
- Automatic image cleanup
- Uses threading for non-blocking email sending

## Requirements
- Python 3.x
- OpenCV
- python-dotenv

## Setup

1. Install dependencies:
   pip install -r requirements.txt

2. Create a .env file and add:
   EMAIL_ADDRESS=your_email
   EMAIL_PASSWORD=your_app_password

3. Run:
   python main.py
