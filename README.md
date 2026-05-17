# Podcast Generator - Transcript Modules

This repository contains modules dedicated to extracting and processing transcripts from YouTube videos. The extraction system is designed to automatically gather English transcripts using API fetching or ML-based audio transcription as a fallback.

## Prerequisites

This project uses **Ollama** for local LLM processing (Sport Detection, Data Extraction, and Podcast Generation) and **IndicTrans2** for high-quality translation into Indic languages.

1.  **Install Ollama**: Download and install from [ollama.com](https://ollama.com/).
2.  **Pull the LLM Model**: This project uses `gemma2:2b` by default.
    ```bash
    ollama pull gemma2:2b
    ```
3.  **IndicTrans2 Requirements**: The translation module uses Hugging Face's `transformers`. Ensure you have sufficient disk space for the `indictrans2-en-indic-dist-200M` model (~450MB) and a GPU (optional but recommended) for faster translation.

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

### 4. Hugging Face Authentication
The translation module and some models require Hugging Face authentication. Run the following command and paste your token when prompted:
```bash
hf auth login
```
And then paste the hugging face token.

---

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
  * `translator.py`: A wrapper module that routes translations directly to the **IndicTrans2** translation engine for translating podcast scripts into Indic languages (the alternative local LLM-based translation logic is commented out for reference).
  * `indictrans2_translator.py`: The core translation engine using the `ai4bharat/indictrans2-en-indic-dist-200M` model to support Indic languages like Hindi, Bengali, Tamil, etc.

* **`main.py`**: The main entry point that runs the end-to-end pipeline with **caching and resumability**:
  1. **Reverse Check:** Checks if the translated script for the video already exists in `scripts/{video_id}/{language_lowercase}.txt` (e.g. `hindi.txt`).
  2. **English Check:** If translation is missing, it checks for an existing English script in `scripts/{video_id}/english.txt`.
  3. **Full Pipeline:** If no scripts are found, it fetches the transcript, detects the sport, and extracts structured data.
  4. **Generation & Storage:** Generates and saves the English podcast script and translated versions in structured folders (`scripts/{video_id}/`).

* **`scripts/`** (Generated)
  * `{video_id}/`: A folder for each processed video containing:
    * `english.txt`: The generated English podcast script.
    * `{language_lowercase}.txt`: The translated version of the script (e.g. `hindi.txt`).

* **`youtube_video_transcript/`**
  * `1_get_transcript.py`: A simplified/initial version of the transcript extraction pipeline. It attempts to fetch captions and falls back to audio download and Whisper transcription. Audio files are downloaded directly (usually as `audio.mp3`) and cleaned up immediately after extraction.
  * `2_get_transcript.py`: An enhanced version of the extraction script similar to `transcript_extractor.py`. It caches the downloaded audio into the `youtube_video_transcript/Audio/` directory by video ID to prevent re-downloads, includes translation capabilities, and saves the final transcript to the `youtube_video_transcript/Transcript/` directory.
  * `README.md`: A localized README specifically for this pipeline variant.
  * `Audio/`: Cache directory for audio downloaded by `2_get_transcript.py`.
  * `Transcript/`: Directory where the final `.txt` transcript files (e.g., `MAm0RLQpYas.txt`) are saved by the script.

* **`tts/`**
  * `mms_tts.py`: The Text-to-Speech (TTS) generation engine using Facebook's Massively Multilingual Speech (MMS) models from Hugging Face `transformers` (VITS architecture). It dynamically loads and caches models to generate speech from text in various Indic languages.

* **`test_tts.py`**: A simple verification script to test the local TTS generation pipeline by generating a Hindi audio sample (`audio/test_hindi.wav`).

## Core Dependencies
These modules rely on the following primary Python packages:
- `youtube-transcript-api`: For fetching official/auto-generated captions.
- `yt-dlp`: For downloading audio streams when captions are missing.
- `faster-whisper`: For local, AI-powered transcription and translation of audio files.
- `torch` & `transformers`: For PyTorch tensor operations and downloading/running the VitsModel & AutoTokenizer TTS models.
- `soundfile`: For writing the generated audio waveform to standard `.wav` files.

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
1. Check if the **translated script** (`scripts/{video_id}/{language_lowercase}.txt`) already exists. If yes, it loads it and finishes.
2. If not, check if the **English podcast script** (`scripts/{video_id}/english.txt`) exists. If yes, it skips generation and goes straight to translation.
3. If neither exists, it runs the **full pipeline**: fetching the transcript, detecting the sport, extracting structured data, and then generating both the English and translated scripts.

All results are organized in the `scripts/` folder, structured by YouTube video ID.

### 3. Deactivate the Virtual Environment
Once you are finished, you can exit the virtual environment:
```bash
deactivate
```

### 4. Running Text-to-Speech (TTS) Generation
To synthesize spoken audio from text using local MMS TTS models:
1. Make sure your virtual environment is active.
2. Run the test script to verify the TTS model download, load, and audio synthesis:
   ```bash
   python test_tts.py
   ```
3. The script will dynamically load the Meta MMS model for Hindi, synthesize the audio from a sample Hindi text, and write it to `audio/test_hindi.wav`.

For individual transcript extraction:
```bash
# Example running the enhanced transcript extractor
python transcript/transcript_extractor.py
```

