# Chat Analysis with Speech-to-Text

This project analyzes chat conversations, detects potentially unsafe content in both text and images, and now includes speech-to-text functionality.

## Features

- Chat text analysis for concerning patterns and content
- Image NSFW detection
- Speech-to-text conversion from audio files
- Integration of audio transcriptions into chat analysis

## Setup

1. Clone the repository
2. Install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

## Speech-to-Text Functionality

The system now supports automatic transcription of audio files to text using the Whisper model from OpenAI through the faster-whisper library.

### How to Use

1. Place audio files (mp3, wav, m4a, ogg) in the `data/audio` directory
2. Run the main script:

```bash
cd backend
python main.py
```

3. The system will:
   - Detect any audio files in the `data/audio` directory
   - Transcribe them to text using the medium-sized Whisper model
   - Add the transcriptions to the chat.json file
   - Mark processed files to avoid duplicate processing

### Testing Speech-to-Text Separately

You can test the speech-to-text functionality separately:

```bash
cd backend
python test_speech.py [optional_path_to_audio_file]
```

If no audio file is specified, the script will use the first audio file found in the `data/audio` directory.

## Configuration

The speech-to-text functionality can be configured in `speech_to_text.py`:

- `model_size`: "tiny", "base", "small", "medium", "large-v3"
- `language`: Language code (e.g., "en" for English)
- Other parameters for transcription quality and performance 