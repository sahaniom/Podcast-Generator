# Podcast Generator - Transcript Modules

This repository contains modules dedicated to extracting and processing transcripts from YouTube videos. The extraction system is designed to automatically gather English transcripts using API fetching or ML-based audio transcription as a fallback.

## Folder Structure

* **`transcript/`**
  * `transcript_extractor.py`: The core script that retrieves an English transcript for a given YouTube video. It follows a multi-step process:
    1. **Cache Check:** Reuse existing transcript or audio files if they exist locally.
    2. **Captions API:** Attempts to fetch English captions via `youtube_transcript_api`.
    3. **Whisper Fallback:** If captions are unavailable, it downloads the audio using `yt-dlp` and transcribes/translates it locally using the `faster-whisper` AI model.
  * `Audio/`: Directory where downloaded audio files are cached to prevent re-downloads.
  * `Transcript/`: Directory where final transcript `.txt` files are saved with language info.

* **`llm/`**
  * `extractor.py`: Orchestrates the LLM extraction process by chunking text, calling the LLM, and merging results into structured JSON.
  * `ollama_client.py`: Client for interacting with a local Ollama API (using `qwen3.5:2b`) to generate LLM responses.
  * `prompts.py`: Contains the system prompt used for structured data extraction from sports transcripts.

* **`processing/`**
  * `chunking.py`: Utility module for splitting large texts into manageable chunks to stay within LLM token limits.
    - Initially chunk size is 3000, but it seems too large for 2B model, so it has been reduced to 1200.

* **`main.py`**: The main entry point to run the full pipeline, from fetching a YouTube transcript to outputting structured JSON data.

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
- `tqdm`: For displaying progress bars during the Whisper transcription process.

## Usage
To extract a transcript, you can run the primary extractor script or the numbered scripts. By default, the scripts are configured to process a specific video URL in the `__main__` execution block.

```bash
# Example running the enhanced transcript extractor
python transcript/transcript_extractor.py
```
