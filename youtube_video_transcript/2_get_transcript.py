"""
This script retrieves an English transcript for a given YouTube video.
It features a two-step extraction process:
1. First, it attempts to fetch explicit or auto-generated captions via the YouTube Transcript API, translating them to English if necessary.
2. If captions are unavailable, it falls back to downloading the audio using yt-dlp (caching it in an 'Audio' directory) and transcribing/translating it locally using the faster-whisper model.
Finally, it saves the extracted transcript, along with language detection info, to a local 'transcript' folder.
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
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id) # type: ignore
        
        # Try to find an English transcript first
        try:
            t = transcript_list.find_transcript(['en'])
            return " ".join([x['text'] for x in t.fetch()]), f"{t.language} ({t.language_code})"
        except:
            pass
        
        # Try to find any other transcript and translate it to English
        for t in transcript_list:
            if t.is_translatable:
                try:
                    translated = t.translate('en')
                    return " ".join([x['text'] for x in translated.fetch()]), f"{t.language} - Translated to English ({t.language_code})"
                except:
                    continue
    except:
        pass
    
    return None, None


# ---------- Step 2: Download audio ----------
def download_audio(url, video_id):
    print("⬇️ Downloading audio...")
    audio_dir = "Audio"
    os.makedirs(audio_dir, exist_ok=True)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(audio_dir, f"{video_id}.%(ext)s"),
        'quiet': True,
        'noplaylist': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl: # type: ignore
        info_dict = ydl.extract_info(url, download=True)
        downloaded_file = ydl.prepare_filename(info_dict)

    return downloaded_file


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

    # Because faster_whisper translates to English when task="translate",
    # the detected language is info.language.
    language_str = f"Auto-detected by Whisper ({info.language})"
    return " ".join(full_text), language_str


# ---------- Main Pipeline ----------
def get_transcript(url):
    video_id = extract_video_id(url)
    print(f"🎬 Processing video ID: {video_id}")

    # Step 1: captions
    text, lang_info = get_caption_transcript(video_id)
    if text:
        print("✅ Used captions")
    else:
        # Step 2: Whisper fallback
        print("⚠️ No captions found, using Whisper...")
        
        # Check for existing audio file
        audio_dir = "Audio"
        os.makedirs(audio_dir, exist_ok=True)
        
        audio_file = None
        for f in os.listdir(audio_dir):
            if f.startswith(f"{video_id}."):
                audio_file = os.path.join(audio_dir, f)
                break
                
        if audio_file:
            print(f"🔄 Found existing audio file: {audio_file}")
        else:
            audio_file = download_audio(url, video_id)

        text, lang_info = whisper_transcribe(audio_file)

    # Step 3: Save to transcript folder
    os.makedirs("Transcript", exist_ok=True)
    output_path = os.path.join("Transcript", f"{video_id}.txt")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"Language: {lang_info}\n\n")
        f.write(text.strip() + "\n")
        
    print(f"💾 Transcript saved to: {output_path}")

    return text


# ---------- Run ----------
if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=MAm0RLQpYas"

    transcript = get_transcript(url)

    print("\n--- TRANSCRIPT ---\n")
    print(transcript)

