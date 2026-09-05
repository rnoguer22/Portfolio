import requests
from config import TELEGRAM_BOT_TOKEN, CHAT_ID



def send_telegram_alert(message):
    # Connect to the telegram API with our bot token
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    # Define the message
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown',
        'disable_notification': False
    }
    try:
        # Send the message
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"Error sending message: {response.text}")
    except Exception as e:
        print(f"Connection error with telegram: {e}")
