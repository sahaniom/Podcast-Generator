"""
This script retrieves an English transcript for a given YouTube video.
It uses a two-step fallback mechanism:
1. It first attempts to fetch English captions (or translate existing ones to English) using the YouTube Transcript API.
2. If captions are unavailable, it automatically downloads the audio via yt-dlp.
3. It then generates and translates a transcript using the local faster-whisper AI model.
4. Finally, it cleans up the downloaded audio file after transcription.
"""

import re
import os
import yt_dlp
from tqdm import tqdm
from faster_whisper import WhisperModel
from youtube_transcript_api import YouTubeTranscriptApi

# ---------- Load model ONCE ----------
model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)


# ---------- Extract video ID ----------
def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    return match.group(1) if match else url


# ---------- Step 1: Try captions ----------
def get_caption_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en']) # type: ignore
        return " ".join([x['text'] for x in transcript])
    except:
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id) # type: ignore
            for t in transcript_list:
                try:
                    translated = t.translate('en').fetch()
                    return " ".join([x['text'] for x in translated])
                except:
                    continue
        except:
            pass
    return None


# ---------- Step 2: Download audio ----------
def download_audio(url, output="audio.mp3"):
    print("⬇️ Downloading audio...")
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output,
        'quiet': True,
        'noplaylist': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl: # type: ignore
        ydl.download([url])

    return output


# ---------- Step 3: Faster-Whisper with progress ----------
def whisper_transcribe(audio_path):
    print("🎙️ Transcribing with faster-whisper...")

    segments, info = model.transcribe(
        audio_path,
        task="translate"
    )

    full_text = []

    # tqdm progress bar
    segments = list(segments)  # convert generator → list to get length
    for seg in tqdm(segments, desc="Transcribing", unit="segment"):
        full_text.append(seg.text)

    return " ".join(full_text)


# ---------- Main Pipeline ----------
def get_transcript(url):
    video_id = extract_video_id(url)
    print(f"🎬 Processing video ID: {video_id}")

    # Step 1: captions
    text = get_caption_transcript(video_id)
    if text:
        print("✅ Used captions")
        return text

    # Step 2: Whisper fallback
    print("⚠️ No captions found, using Whisper...")
    audio_file = download_audio(url)

    text = whisper_transcribe(audio_file)

    # cleanup
    if os.path.exists(audio_file):
        os.remove(audio_file)

    return text


# ---------- Run ----------
if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=MAm0RLQpYas"

    transcript = get_transcript(url)

    print("\n--- TRANSCRIPT ---\n")
    print(transcript)
