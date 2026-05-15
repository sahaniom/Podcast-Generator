# Podcast Generator - Transcript Modules

This repository contains modules dedicated to extracting and processing transcripts from YouTube videos. The extraction system is designed to automatically gather English transcripts using API fetching or ML-based audio transcription as a fallback.

## Prerequisites

This project uses **Ollama** for local LLM processing (Sport Detection, Data Extraction, Podcast Generation, and Translation).

1.  **Install Ollama**: Download and install from [ollama.com](https://ollama.com/).
2.  **Pull and Run the Model**: This project uses `gemma2:2b` by default. Run the following in your terminal:
    ```bash
    ollama run gemma2:2b
    ```
    > It will automatically pull the model if you don't have it locally. Ensure you have a stable internet connection for the initial setup.
3.  **Run Ollama**: Ensure the Ollama server is running. On Windows, it usually runs as a tray icon, or you can run `ollama serve` in a separate terminal.

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

* **`generation/`**
  * `podcast_script_generator.py`: Module that transforms structured match data into a natural, conversational podcast-style narration script using the LLM.

* **`translation/`**
  * `translator.py`: Module for translating the generated podcast script into target languages while maintaining the original tone and excitement.

* **`main.py`**: The main entry point that runs the end-to-end pipeline with **caching and resumability**:
  1. **Reverse Check:** Checks if the translated script for the video already exists in `scripts/{video_id}/{language}.txt`.
  2. **English Check:** If translation is missing, it checks for an existing English script in `scripts/{video_id}/english.txt`.
  3. **Full Pipeline:** If no scripts are found, it fetches the transcript, detects the sport, and extracts structured data.
  4. **Generation & Storage:** Generates and saves the English podcast script and translated versions in structured folders (`scripts/{video_id}/`).

* **`scripts/`** (Generated)
  * `{video_id}/`: A folder for each processed video containing:
    * `english.txt`: The generated English podcast script.
    * `{language}.txt`: The translated version of the script.

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

The script will follow a **reverse-check logic**:
1. Check if the **translated script** (`scripts/{video_id}/{language}.txt`) already exists. If yes, it loads it and finishes.
2. If not, check if the **English podcast script** (`scripts/{video_id}/english.txt`) exists. If yes, it skips generation and goes straight to translation.
3. If neither exists, it runs the **full pipeline**: fetching the transcript, detecting the sport, extracting structured data, and then generating both the English and translated scripts.

All results are organized in the `scripts/` folder, structured by YouTube video ID.

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

