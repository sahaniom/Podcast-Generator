import streamlit as st
import subprocess
import requests
import json
import os
from faster_whisper import WhisperModel
from gtts import gTTS
from preprocess import run_preprocessing

# ✅ ML MODEL
from ml_highlight import predict_highlights

# ✅ Vertex AI SDK
from google import genai

# 🔐 SAFE API KEY (USE ENV VARIABLE)
client = genai.Client(api_key="AIzaSyBIB9V62vC0hHJ_-7qENx0c6KGcICnwuYY")

st.title("⚽ AI Football Commentary Processor")

# ---------------------- INPUT SECTION ----------------------
input_type = st.selectbox(
    "Choose Input Type",
    ["Upload Audio", "Upload Video", "Audio URL", "Video URL"],
)

uploaded_file = None
audio_url = None
video_url = None

if input_type in ["Upload Audio", "Upload Video"]:
    uploaded_file = st.file_uploader("Upload File")

elif input_type == "Audio URL":
    audio_url = st.text_input("Enter Audio URL (MP3/WAV)")

elif input_type == "Video URL":
    video_url = st.text_input("Enter Video URL")

# ---------------------- HELPER FUNCTIONS ----------------------

def download_video(url):
    try:
        subprocess.run([
            "yt-dlp",
            "--cookies-from-browser", "chrome",   # ✅ FIXED YOUTUBE ISSUE
            "-x", "--audio-format", "mp3",
            "-o", "input_audio.mp3",
            url
        ], check=True)
        return "input_audio.mp3"
    except subprocess.CalledProcessError:
        st.error("❌ Video download failed (Try login to YouTube in Chrome)")
        return None


def download_audio(url):
    try:
        if url.lower().endswith((".mp3", ".wav", ".m4a")):
            out = "input_audio.mp3"
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(out, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            return out
        else:
            return download_video(url)
    except Exception as e:
        st.error(f"Audio download failed: {e}")
        return None


def extract_audio(video_path):
    audio_path = "extracted_audio.mp3"
    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", video_path,
            "-vn", "-acodec", "mp3",
            audio_path
        ], check=True)
        return audio_path
    except subprocess.CalledProcessError:
        st.error("Audio extraction failed")
        return None


def convert_to_wav(audio_path):
    wav_path = "processed.wav"
    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", audio_path,
            "-ar", "16000", "-ac", "1",
            wav_path
        ], check=True)
        return wav_path
    except subprocess.CalledProcessError:
        st.error("Audio conversion failed")
        return None


# ---------------------- AI LOGIC ----------------------

def transcribe_audio(audio_path):
    model = WhisperModel("base")
    segments, _ = model.transcribe(audio_path)

    data = []
    for segment in segments:
        data.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text
        })
    return data


# ✅ Vertex AI Summary (FIXED)
def generate_summary_vertex(text):

    text = text[:4000]  # reduce tokens → avoid quota

    prompt = f"""
    You are an expert football commentator.

    Create an exciting short podcast-style summary.
    Focus only on key highlights like goals, saves, penalties.

    Commentary:
    {text}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        try:
            return response.text
        except:
            return response.candidates[0].content.parts[0].text

    except Exception as e:
        return f"❌ Vertex AI Error: {str(e)}"


def generate_podcast(summary):
    tts = gTTS(summary)
    output = "podcast.mp3"
    tts.save(output)
    return output


# ---------------------- PROCESS BUTTON ----------------------

if st.button("Process"):

    # ---------------- INPUT HANDLING ----------------
    if uploaded_file:
        file_path = uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        if input_type == "Upload Video":
            audio_path = extract_audio(file_path)
        else:
            audio_path = file_path

    elif audio_url:
        audio_path = download_audio(audio_url)

    elif video_url:
        audio_path = download_video(video_url)

    else:
        st.error("Please provide input")
        st.stop()

    if not audio_path:
        st.stop()

    wav_path = convert_to_wav(audio_path)

    if not wav_path:
        st.stop()

    # ---------------- STT ----------------
    st.info("Transcribing...")
    segments = transcribe_audio(wav_path)

    # ---------------- SAVE RAW ----------------
    with open("transcript_raw.json", "w") as f:
        json.dump(segments, f, indent=4)

    # ---------------- PREPROCESS ----------------
    processed_data = run_preprocessing()
    segments = processed_data

    # ---------------- TRANSCRIPT ----------------
    full_text = " ".join([s["original_text"] for s in segments])

    st.subheader("📜 Transcript")
    st.write(full_text)

    # ---------------- ML HIGHLIGHTS ----------------
    scored_segments = predict_highlights(segments)

    top_highlights = [s for s in scored_segments if s["label"] == 1]
    top_highlights = sorted(top_highlights, key=lambda x: x["score"], reverse=True)[:5]

    st.subheader("⭐ ML Highlights")

    for h in top_highlights:
        st.write(f"⏱ {round(h['start'],1)}s - {round(h['end'],1)}s")
        st.write(f"📝 {h['original_text']}")
        st.write(f"🔥 Score: {round(h['score'], 3)}")
        st.write("---")

    # ---------------- SUMMARY USING HIGHLIGHTS ----------------
    highlight_text = " ".join([h["original_text"] for h in top_highlights])

    with st.spinner("Generating AI Summary using Vertex AI..."):
        summary = generate_summary_vertex(highlight_text)

    st.subheader("📝 AI Summary (Vertex AI)")
    st.write(summary)

    # ---------------- PODCAST ----------------
    podcast_file = generate_podcast(summary)

    st.subheader("🎧 Podcast")
    st.audio(podcast_file)

    st.success("Processing Complete!")