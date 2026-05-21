# Setup and Execution Guide

Follow these steps to set up the virtual environment and run the Podcast Generator project.

## 1. Create Virtual Environment

Open your terminal in the project root directory and run:

```powershell
# Create the virtual environment
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\Activate.ps1
```

## 2. Install Dependencies

Once the virtual environment is activated, install the required packages:

```powershell
pip install streamlit faster-whisper gtts scikit-learn joblib google-genai requests yt-dlp python-dotenv
```

> **Note:** Ensure you have `ffmpeg` installed on your system as it is required for audio/video processing.

## 3. Configure API Key

1. Copy the `.env.example` file to create a `.env` file:
   ```powershell
   copy .env.example .env
   ```
2. Open the `.env` file and replace `your_api_key_here` with your actual Google AI API key.

## 4. Run the Project

The main entry point is a Streamlit web application. To start it, run:

```powershell
streamlit run app.py
```

## Additional Scripts

If you need to train the highlight detection model:

1. **Create Dataset**: `python create_dataset.py`
2. **Train Model**: `python train_model.py`
