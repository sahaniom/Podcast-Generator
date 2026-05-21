# AI Football Commentary Processor - Project Documentation

This project is an AI-powered pipeline designed to process football commentary from various sources (audio, video, or URLs), identify key match highlights using Machine Learning, generate an exciting summary using Google Vertex AI (Gemini), and finally convert that summary into a podcast-style audio file.

## Project Structure Overview

The project is organized into several Python scripts, each handling a specific part of the pipeline:

### 1. Web Application (`app.py`)
This is the main entry point and user interface built with **Streamlit**.
- **Inputs**: Supports audio/video file uploads and URLs (YouTube/Direct links).
- **Processing**:
    - **Downloads**: Uses `yt-dlp` for video/audio downloads.
    - **Transcription**: Uses `faster-whisper` for high-performance speech-to-text.
    - **Integration**: Orchestrates the flow between preprocessing, ML highlight detection, Vertex AI summarization, and Text-to-Speech (TTS).
    - **Audio/Video Tools**: Uses `ffmpeg` for format conversions and audio extraction.

### 2. Data Preprocessing (`preprocess.py`)
Handles the cleaning and structuring of transcribed text.
- **Cleaning**: Lowercases text and removes non-alphanumeric characters using regex.
- **Structuring**: Maps original segments to their "cleaned" versions while preserving timestamps (`start`, `end`).

### 3. Machine Learning Pipeline
The project includes a custom ML model to detect "highlights" based on commentary text.
- **`create_dataset.py`**: A script to label data. It marks segments as highlights (label `1`) if they contain specific keywords like "goal", "penalty", or "amazing".
- **`train_model.py`**: Trains a **Logistic Regression** model using **TF-IDF Vectorization** to classify text as a highlight or not.
- **`ml_highlight.py`**: A helper script used by the app to load the saved model (`highlight_model.pkl`) and vectorizer (`vectorizer.pkl`) to predict highlights in new transcripts.

### 4. Vertex AI Integration (`vertex_ai.py`)
Utilizes Google's **Gemini 2.0 Flash** model to transform raw highlight text into a coherent, "exciting" sports summary. It acts as the "creative brain" of the podcast.

### 5. Pipeline Automation (`run_pipeline.py`)
A utility script that automates the entire setup:
1. Runs `create_dataset.py` to prepare the data.
2. Runs `train_model.py` to build the highlight detection model.
3. Launches the `streamlit` application.

## Detailed Workflow

1.  **Ingestion**: User provides a football match video/audio.
2.  **Conversion**: The system extracts/converts the audio to a 16kHz WAV format (optimized for Whisper).
3.  **Transcription**: `faster-whisper` generates a timestamped transcript.
4.  **Highlight Detection**: The trained ML model analyzes each segment and scores it. The top 5 highest-scoring "highlights" (e.g., goals, saves) are selected.
5.  **Summarization**: These highlights are sent to Google Gemini with a sports-specific prompt.
6.  **Audio Output**: The summary is converted to speech using `gTTS` (Google Text-to-Speech) and presented as a playable podcast in the UI.

## Key Dependencies
- `streamlit`: For the Web UI.
- `faster-whisper`: For Speech-to-Text.
- `google-genai`: For accessing Gemini models.
- `scikit-learn`: For the highlight detection ML model.
- `gTTS`: For generating the final podcast audio.
- `ffmpeg` & `yt-dlp`: For media processing and downloading.

## How to Run
Typically, you would run the entire project using:
```bash
python run_pipeline.py
```

*(Note: Ensure you have your Google API key configured in `app.py` or environment variables before running.)*
