# Structured Output for Chat Safety Analysis

This feature enhances the chat safety analysis system to generate structured JSON output files whenever dangerous content is detected. The analysis results are saved in the `output` directory with timestamped filenames. The system keeps only the most recent analysis file, automatically deleting previous ones.

## Features

- Automatic creation of structured JSON output for detected threats
- Keeps only the most recent analysis file (deletes previous ones)
- Saves results in two formats:
  - Timestamped file (`analysis_result_YYYYMMDD_HHMMSS.json`)
  - Standard file (`latest_analysis.json`) for easier access
- Timestamps in filenames and inside JSON for better tracking
- Detailed analysis saved in multiple formats based on detection type
- Generation of output files only when medium or high risk content is detected

## Detection Types

The system can detect and create structured output for three types of concerning content:

1. **Text Analysis** - Detects grooming or dangerous text patterns in conversations
2. **Image Analysis** - Identifies NSFW (Not Safe For Work) content in images
3. **Final Analysis** - Combined analysis from both text and image scanning

## Output Format

Output files are saved in the `output` directory with two formats:
- Timestamped: `analysis_result_YYYYMMDD_HHMMSS.json`
- Standard: `latest_analysis.json` (always contains the most recent analysis)

The JSON structure varies slightly based on the detection type, but generally includes:

```json
{
  "risk_level": "Medium or High",
  "analysis": "Detailed analysis text explaining the findings",
  "flagged_messages": "List of specific messages that triggered the detection",
  "detection_type": "text_analysis/image_analysis/final_analysis",
  "timestamp": "ISO formatted timestamp",
  
  // For text analysis:
  "chat_excerpt": "Excerpt of the concerning messages",
  
  // For image analysis:
  "nsfw_images": [
    {
      "image_path": "/path/to/image.jpg",
      "nsfw_score": 0.95,
      "is_nsfw": true
    }
  ]
}
```

## How to Test

You can use the `test_structured_output.py` script to test different scenarios:

```bash
# Run with default "low" risk level (no output file generated)
python backend/test_structured_output.py

# Test with "medium" risk level (generates output file)
python backend/test_structured_output.py medium

# Test with "high" risk level (generates output file)
python backend/test_structured_output.py high

# Test image detection (generates output file if NSFW image detected)
python backend/test_structured_output.py image
```

## Integration

The structured output feature is fully integrated with the existing chat analysis system:

- In `main.py`, the system will automatically generate output files when dangerous content is detected
- The output directory is automatically created if it doesn't exist
- The agent will report the location of saved output files in its analysis results 