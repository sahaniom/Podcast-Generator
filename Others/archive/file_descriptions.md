# Podcast-Generator File Descriptions

This document provides a summary of each file in the `Podcast-Generator` project and its role within the AI-powered football commentary pipeline.

## Core Application
- **[app.py](app.py)**: The main entry point of the project. It uses **Streamlit** to provide a web interface where users can upload audio/video files or provide URLs. It orchestrates the entire pipeline, including downloading media, transcribing audio with `faster-whisper`, running the ML highlight detection, calling Vertex AI for summarization, and generating the final podcast audio using `gTTS`.

## Data Processing & ML
- **[preprocess.py](preprocess.py)**: Contains utility functions to clean raw transcriptions. It lowercases text, removes special characters, and structures the data into a JSON format while preserving timestamps (`start`, `end`).
- **[create_dataset.py](create_dataset.py)**: A script used to prepare training data. It scans preprocessed segments for specific keywords (like "goal", "penalty", "wow") and labels them as highlights (`1`) or non-highlights (`0`).
- **[train_model.py](train_model.py)**: Trains a **Logistic Regression** model using **TF-IDF Vectorization** on the dataset created by `create_dataset.py`. It saves the trained model (`highlight_model.pkl`) and vectorizer (`vectorizer.pkl`) for later use.
- **[ml_highlight.py](ml_highlight.py)**: A helper module that loads the saved ML model and vectorizer. It provides the `predict_highlights` function used by the main app to score and identify highlights in new transcripts.

## AI & Automation
- **[vertex_ai.py](vertex_ai.py)**: Handles the integration with **Google Vertex AI (Gemini 2.0 Flash)**. It takes the text from detected highlights and uses a refined prompt to generate an exciting, coherent sports summary meant for the final podcast.
- **[run_pipeline.py](run_pipeline.py)**: An automation script that builds the environment. It sequentially runs the dataset creation, model training, and then launches the Streamlit application.

## Documentation & Metadata
- **[PROJECT_EXPLANATION.md](PROJECT_EXPLANATION.md)**: Provides a high-level overview of the project architecture, dependencies, and detailed workflow.
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)**: (Currently open) Contains instructions on how to set up the environment and run the project.
- **[temp.txt](temp.txt)**: A temporary file likely used for debugging or short-term storage of text/logs.
