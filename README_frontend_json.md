# Frontend-Ready JSON with NSFW Flags

This feature enhances the chat safety analysis system to create a frontend-ready JSON file with NSFW flags for each message. The output is saved in a single file in the `output_for_frontend` directory.

## Features

- Creates a JSON file in the same format as chat.json but with an additional "nsfw" flag
- Flags dangerous messages with nsfw=1, safe messages with nsfw=0
- Maintains a single file that's continuously updated, not creating multiple files
- Preserves all the original fields from the source chat.json
- Detects both text-based and image-based NSFW content

## Output Format

The output file is saved in the `output_for_frontend` directory as `chat_with_flags.json`. It follows the exact same format as the original chat.json file but with an additional field:

```json
[
  {
    "timestamp": 1746928799,
    "instance_wid": "905063665714@c.us",
    "sender": "user",
    "sender_contact_name": "",
    "sender_number": "998904214104@c.us",
    "chat_id": "998904214104@c.us",
    "chat_name": "username",
    "message_type": "textMessage",
    "message": "Hello, how are you?",
    "nsfw": 0  // This message is safe
  },
  {
    "timestamp": 1746930550,
    "instance_wid": "905063665714@c.us",
    "sender": "user",
    "sender_contact_name": "",
    "sender_number": "998904214104@c.us",
    "chat_id": "998904214104@c.us",
    "chat_name": "username",
    "message_type": "textMessage",
    "message": "inappropriate or dangerous content",
    "nsfw": 1  // This message is flagged as dangerous
  }
]
```

## Integration with Your Frontend

To use this data in your frontend application:

1. Read the `output_for_frontend/chat_with_flags.json` file
2. Use the "nsfw" field to display warnings or apply special styling to dangerous messages
3. The file is continuously updated as new messages are analyzed

## How It Works

1. Chat messages are analyzed by the AI safety agent
2. When dangerous content is detected in a message, it's flagged with nsfw=1
3. The system maintains a single JSON file that's updated incrementally
4. Messages are matched by content, sender, and timestamp to avoid duplicates
5. Both text analysis and image analysis results contribute to the nsfw flag

## Testing

You can use the `test_structured_output.py` script to test the frontend JSON functionality:

```bash
# Test with high risk level to see examples of flagged messages
python backend/test_structured_output.py high
```

The test script will show statistics about the created frontend JSON file, including the number of safe and unsafe messages. 