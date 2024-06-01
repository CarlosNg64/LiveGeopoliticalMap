import os
from datetime import datetime, timedelta
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel, MessageMediaPhoto, MessageMediaDocument
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Replace 'API_ID', 'API_HASH', 'PHONE_NUMBER', and 'CHAT_ID'
api_id = '21950531'
api_hash = '77ddc817506d749b2e4611e644984eaa'
phone_number = '+17874663738'
chat_id = 'https://t.me/BellumActaNews'  # This can be the username or ID of the chat

# Specify the directories for saving text and media files
text_file_path = r'c:\Users\oneto\Documents\GitHub\LiveGeopoliticalMap\telegram_chat.txt'
media_dir = r'c:\Users\oneto\Documents\GitHub\LiveGeopoliticalMap\media'

# Create the media directory if it doesn't exist
os.makedirs(media_dir, exist_ok=True)

# Create the client and connect
client = TelegramClient('session_name', api_id, api_hash)
client.connect()

# If not already authorized, send the code
if not client.is_user_authorized():
    client.send_code_request(phone_number)
    client.sign_in(phone_number, input('Enter the code: '))

# Get the chat history
async def get_chat_history():
    chat = await client.get_entity(chat_id)
    if isinstance(chat, PeerChannel):
        peer = PeerChannel(chat.id)
    else:
        peer = chat

    messages = []
    offset_id = 0
    limit = 100  # Number of messages to retrieve per request

    while True:
        history = await client(GetHistoryRequest(
            peer=peer,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))

        if not history.messages:
            break

        messages.extend(history.messages)
        offset_id = history.messages[-1].id

    return messages

# Filter messages by date range
def filter_messages_by_date_range(messages, start_date, end_date):
    filtered_messages = []
    for message in messages:
        message_date = message.date.replace(tzinfo=None)
        if start_date <= message_date <= end_date:
            filtered_messages.append(message)
    
    return filtered_messages

# Save the filtered chat history to a text file and download media
async def save_filtered_messages_to_file(start_day, start_month, start_year, end_day, end_month, end_year):
    messages = await get_chat_history()
    
    # Create datetime objects for the start and end dates
    start_date = datetime(start_year, start_month, start_day)
    end_date = datetime(end_year, end_month, end_day) + timedelta(days=1) - timedelta(seconds=1)
    
    # Filter messages by the specified date range
    filtered_messages = filter_messages_by_date_range(messages, start_date, end_date)
    
    # Reverse the messages to be in descending order
    filtered_messages.reverse()
    
    with open(text_file_path, 'w', encoding='utf-8') as file:
        for message in filtered_messages:
            if message.message:
                file.write(message.message + '\n')
                file.write('%%%%%%%%%%%%%%%\n')  # Add delimiter between messages
            
            # Check if the message contains media
            if message.media:
                logging.info('Found media in message ID %s', message.id)
                try:
                    if isinstance(message.media, (MessageMediaPhoto, MessageMediaDocument)):
                        # Download media (photo or document)
                        media_path = await client.download_media(message, file=media_dir)
                        logging.info('Media downloaded to %s', media_path)
                        file.write(f'Media: {media_path}\n')
                        file.write('%%%%%%%%%%%%%%%\n')
                    else:
                        logging.info('Media type %s is not supported for download.', type(message.media))
                except Exception as e:
                    logging.error('Failed to download media: %s', e)

# Run the async functions with specified date range
start_day = 30
start_month = 5
start_year = 2024
end_day = 1
end_month = 6
end_year = 2024

with client:
    client.loop.run_until_complete(save_filtered_messages_to_file(start_day, start_month, start_year, end_day, end_month, end_year))

logging.info('Messages and media saved to %s', text_file_path)
