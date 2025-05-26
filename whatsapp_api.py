import requests
import os
import json
from whatsapp_api_client_python import API

import time
import subprocess


# Setup
greenAPI = API.GreenAPI("7105240414", "7248b928fcc34d2699dbf1eefe19ba7d90f78cc1054140c6bb")

os.makedirs('data', exist_ok=True)
os.makedirs('data/audio', exist_ok=True)
os.makedirs('images', exist_ok=True)

# Save parsed message data to a JSON file
def save_to_json(data, filename="data/chat.json"):
    try:
        # Load existing data if the file exists
        if os.path.exists(filename):
            with open(filename, "r") as json_file:
                existing_data = json.load(json_file)
        else:
            existing_data = []

        # Ensure the existing data is a list
        if not isinstance(existing_data, list):
            existing_data = []

        # Append the new message data
        existing_data.append(data)

        # Write the updated data back to the file
        with open(filename, "w") as json_file:
            json.dump(existing_data, json_file, indent=4)

        print(f"Message data appended to {filename}")
    except Exception as e:
        print(f"Failed to append message data to JSON: {e}")

# Helper: Download media file   
def save_media(url, name):
    response = requests.get(url)
    if response.status_code == 200:
        # Supported image formats
        if name.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')):
            with open(f'images/{name}', "wb") as f:
                f.write(response.content)

        # Supported audio formats
        elif name.endswith(('.ogg', '.oga', '.mp3', '.wav', '.flac', '.aac')):
            with open(f'data/audio/{name}', 'wb') as f:
                f.write(response.content)
                
        print(f"{name} downloaded successfully!")
    else:
        print(f"Failed to download {name}. Status code: {response.status_code}")
    return response.status_code

    
# Get the latest notification
url = "https://7105.api.greenapi.com/waInstance7105240414/receiveNotification/7248b928fcc34d2699dbf1eefe19ba7d90f78cc1054140c6bb"

import time
import subprocess
# ...existing imports...

def save_messages_to_json():
    while True:  # Endless loop
        response = requests.get(url)

        try:
            data = response.json()
        except Exception as e:
            print("Failed to parse JSON:", e)
            data = None

        message_data = {}

        if data:
            print("Received message data")

            # Delete notification
            receipt_id = data.get("receiptId")
            if receipt_id:
                delete_url = f"https://7105.api.greenapi.com/waInstance7105240414/deleteNotification/7248b928fcc34d2699dbf1eefe19ba7d90f78cc1054140c6bb/{receipt_id}"
                del_response = requests.delete(delete_url)
                print("Delete response:", del_response.text)

            body = data.get('body', {})
            message_data['timestamp'] = body.get('timestamp')
            message_data['instance_wid'] = body.get('instanceData', {}).get('wid')

            sender = body.get('senderData', {})
            message_data['sender'] = sender.get('senderName')
            message_data['sender_contact_name'] = sender.get('senderContactName')
            message_data['sender_number'] = sender.get('sender')
            message_data['chat_id'] = sender.get('chatId')
            message_data['chat_name'] = sender.get('chatName')

            msg = body.get('messageData', {})
            msg_type = msg.get('typeMessage')
            message_data['message_type'] = msg_type

            # Poll Message
            if msg_type == 'pollMessage':
                poll_data = body.get('pollMessageData', {})
                message_data['poll_caption'] = poll_data.get('name')
                message_data['poll_options'] = [opt.get('optionName') for opt in poll_data.get('options', [])]

            # Image or Audio Message
            elif msg_type in ['imageMessage', 'audioMessage']:
                file_data = msg.get('fileMessageData', {})
                media_url = file_data.get('downloadUrl')
                media_name = file_data.get('fileName')
                if media_url and media_name:
                    save_media(media_url, media_name)
                    folder = 'images' if msg_type == 'imageMessage' else 'data/audio'
                    message_data['message'] = f'{folder}/{media_name}'
                message_data['media_caption'] = file_data.get('caption')
                message_data['media_thumbnail'] = file_data.get('jpegThumbnail')

            # Text Message
            elif msg_type == 'textMessage':
                text_data = msg.get('textMessageData', {})
                message_data['message'] = text_data.get('textMessage')

            # Quoted or Reaction Message
            elif msg_type in ['quotedMessage', 'reactionMessage']:
                extended = msg.get('extendedTextMessageData', {})
                message_data['message'] = extended.get('text')

            print("\nParsed message data:")
            for k, v in message_data.items():
                print(f"{k}: {v}")

            # Save the message data to a JSON file
            save_to_json(message_data)

            # Call backend/main.py
            try:
                subprocess.run(["python", "backend/main.py"], check=True)
                print("backend/main.py executed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to execute backend/main.py: {e}")

        else:
            print("No new data received.")

        # Delay for 2 seconds before the next iteration
        time.sleep(5)


if __name__ == '__main__':    
    save_messages_to_json()