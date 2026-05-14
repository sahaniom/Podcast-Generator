# Podcast Generator - Transcript Modules

This repository contains modules dedicated to extracting and processing transcripts from YouTube videos. The extraction system is designed to automatically gather English transcripts using API fetching or ML-based audio transcription as a fallback.

## Initial Setup

Before running the project, it is recommended to use a Python virtual environment to manage dependencies.

### 1. Create a Virtual Environment
```bash
# Windows
python -m venv venv

# macOS/Linux
python3 -m venv venv
```

### 2. Activate the Virtual Environment
```bash
# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
If you have a `requirements.txt` file:
```bash
pip install -r requirements.txt
```

If you are setting up the dependencies for the first time, you can create the `requirements.txt` file by freezing your current environment:
```bash
pip freeze > requirements.txt
```

## Folder Structure

* **`transcript/`**
  * `transcript_extractor.py`: The core script that retrieves an English transcript for a given YouTube video. It follows a multi-step process:
    1. **Cache Check:** Reuse existing transcript or audio files if they exist locally.
    2. **Captions API:** Attempts to fetch English captions via `youtube_transcript_api`.
    3. **Whisper Fallback:** If captions are unavailable, it downloads the audio using `yt-dlp` and transcribes/translates it locally using the `faster-whisper` AI model.
  * `Audio/`: Directory where downloaded audio files are cached to prevent re-downloads.
  * `Transcript/`: Directory where final transcript `.txt` files are saved with language info.

* **`llm/`**
  * `extractor.py`: Orchestrates the LLM extraction process by chunking text, calling the LLM, and merging results into structured JSON. Includes **resumability support** to pick up from the last processed chunk if interrupted.
  * `ollama_client.py`: Client for interacting with a local Ollama API (using `gemma2:2b`) to generate LLM responses with deterministic settings.
  * `sport_detector.py`: Automatically classifies the sport (e.g., cricket, football) from the transcript to provide context for extraction.
  * `prompts.py`: Contains system prompts used for classification and structured data extraction.

* **`processing/`**
  * `chunking.py`: Utility module for splitting large texts into manageable chunks (default 1200 chars) to stay within LLM context windows.

* **`main.py`**: The main entry point that runs the end-to-end pipeline:
  1. Fetches transcript from YouTube.
  2. Detects the sport.
  3. Efficiently extracts structured data (highlights, moments, scores) using LLM.
  4. Saves results to `main_output.txt`.

* **`youtube_video_transcript/`**
  * `1_get_transcript.py`: A simplified/initial version of the transcript extraction pipeline. It attempts to fetch captions and falls back to audio download and Whisper transcription. Audio files are downloaded directly (usually as `audio.mp3`) and cleaned up immediately after extraction.
  * `2_get_transcript.py`: An enhanced version of the extraction script similar to `transcript_extractor.py`. It caches the downloaded audio into the `youtube_video_transcript/Audio/` directory by video ID to prevent re-downloads, includes translation capabilities, and saves the final transcript to the `youtube_video_transcript/Transcript/` directory.
  * `README.md`: A localized README specifically for this pipeline variant.
  * `Audio/`: Cache directory for audio downloaded by `2_get_transcript.py`.
  * `Transcript/`: Directory where the final `.txt` transcript files (e.g., `MAm0RLQpYas.txt`) are saved by the script.

## Core Dependencies
These modules rely on the following primary Python packages:
- `youtube-transcript-api`: For fetching official/auto-generated captions.
- `yt-dlp`: For downloading audio streams when captions are missing.
- `faster-whisper`: For local, AI-powered transcription and translation of audio files.

## Usage
To run the full pipeline and generate structured sports data from a YouTube video, follow these steps:

### 1. Activate the Virtual Environment
Ensure your environment is active before running the script:
```bash
# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2. Run the Pipeline
Execute the `main.py` script:
```bash
# Run the complete podcast generation pipeline
python main.py
```

The script will fetch the transcript, detect the sport, process it through the LLM, and save the final results to `main_output.txt`.

### 3. Deactivate the Virtual Environment
Once you are finished, you can exit the virtual environment:
```bash
deactivate
```

For individual transcript extraction:
```bash
# Example running the enhanced transcript extractor
python transcript/transcript_extractor.py
```

