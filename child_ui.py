import streamlit as st
import json
import os
import datetime

# Load chat data from chat.json
def load_chat_data(file_path="output_for_frontend/chat_with_flags.json"):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return []

# Filter messages by sender and exclude nsfw messages
def filter_messages_by_sender(chat_data, sender_number):
    return [
        message for message in chat_data
        if message.get("sender_number") == sender_number and message.get("nsfw") != 1
    ]

# Display a single message
def display_message(message):
    message_type = message.get("message_type")
    if message_type == "textMessage":
        st.text(message.get("message"))
    elif message_type == "imageMessage":
        image_path = message.get("message")
        if os.path.exists(image_path):
            st.image(image_path, caption=message.get("media_caption", ""), use_column_width=True)
        else:
            st.warning(f"Image not found: {image_path}")
    elif message_type == "audioMessage":
        audio_path = message.get("message")
        if os.path.exists(audio_path):
            st.audio(audio_path)
            
            # Find transcription if available
            audio_filename = os.path.basename(audio_path)
            transcription = None
            
            # Check for transcription in the chat data
            chat_data = load_chat_data()
            for msg in chat_data:
                if msg.get("sender") == "user_audio" and msg.get("source") == audio_filename:
                    transcription = msg.get("message")
                    break
            
            if transcription:
                st.success(f"Transcription: {transcription}")
            else:
                st.info("No transcription available")
        else:
            st.warning(f"Audio not found: {audio_path}")
    # Handle transcription messages
    elif message.get("sender") == "user_audio":
        st.text(f"Transcription: {message.get('message', '')}")
        source = message.get("source", "")
        if source:
            st.caption(f"Source: {source}")
            
            # Try to display the audio file if it exists
            audio_path = os.path.join("data", "audio", source)
            if os.path.exists(audio_path):
                st.audio(audio_path)

# Main Streamlit app
def main():
    st.title("WhatsApp Chat Viewer")

    # Load chat data
    chat_data = load_chat_data()

    # Group messages by sender_number and include user_audio as a separate sender
    senders = {message["sender_number"]: message.get("sender", "") 
              for message in chat_data 
              if "sender_number" in message}
    
    # Add virtual sender for transcriptions
    has_transcriptions = any(msg.get("sender") == "user_audio" for msg in chat_data)
    if has_transcriptions:
        senders["transcriptions"] = "Audio Transcriptions"

    # Skip if no valid senders found
    if not senders:
        st.error("No valid sender information found in chat data.")
        return

    # Sidebar for sender list
    st.sidebar.title("Senders")
    selected_sender = st.sidebar.selectbox(
        "Select a sender",
        options=list(senders.keys()),
        format_func=lambda sender_number: f"{senders[sender_number]}" if sender_number != "transcriptions" 
                                         else "Audio Transcriptions"
    )

    # Display messages from the selected sender
    if selected_sender == "transcriptions":
        st.header("Audio Transcriptions")
        # Filter for transcription messages
        messages = [msg for msg in chat_data if msg.get("sender") == "user_audio"]
    else:
        st.header(f"Messages from {senders[selected_sender]} ({selected_sender})")
        messages = filter_messages_by_sender(chat_data, selected_sender)

    for message in messages:
        with st.container():
            if "timestamp" in message:
                ts = message['timestamp']
                dt_local = datetime.datetime.fromtimestamp(ts)
                st.write(f"Timestamp: {dt_local}")
            display_message(message)
            st.markdown("---")

if __name__ == "__main__":
    main()