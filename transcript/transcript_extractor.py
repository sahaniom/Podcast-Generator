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
    """
    Extracts the unique 11-character YouTube video ID from a variety of URL formats
    or returns the input if it's already an ID.
    """
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    return match.group(1) if match else url


# ---------- Step 1: Try captions ----------
def get_caption_transcript(video_id):
    """
    Attempts to retrieve transcripts via the YouTube Transcript API.
    Prioritizes English ('en'), but will fallback to translating any available 
    language to English if the original is not in English.
    """
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
    """
    Downloads the best available audio stream using yt-dlp and saves it 
    as an audio file named after the video ID in the 'Audio' directory.
    """
    print("⬇️ Downloading audio...")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    audio_dir = os.path.join(script_dir, "Audio")
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
    """
    Transcribes the provided audio file using the faster-whisper ML model.
    The task is set to 'translate' to ensure the output is always in English.
    Uses tqdm to show a segment-by-segment progress bar.
    """
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
    """
    The core orchestration function for transcript retrieval:
    1. Checks if a local transcript already exists.
    2. Checks if an audio file already exists (skipping download).
    3. Attempts to fetch API captions.
    4. Falls back to Audio Download + Whisper Transcription.
    5. Saves the final result to the 'Transcript' directory.
    """
    video_id = extract_video_id(url)
    print(f"🎬 Processing video ID: {video_id}")

    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Check 1: Existing transcript
    transcript_dir = os.path.join(script_dir, "Transcript")
    existing_transcript_path = os.path.join(transcript_dir, f"{video_id}.txt")
    
    if os.path.exists(existing_transcript_path):
        print(f"🔄 Found existing transcript file: {existing_transcript_path}")
        with open(existing_transcript_path, "r", encoding="utf-8") as f:
            return f.read()

    # Check 2: Existing audio
    audio_dir = os.path.join(script_dir, "Audio")
    os.makedirs(audio_dir, exist_ok=True)
    
    audio_file = None
    for f in os.listdir(audio_dir):
        if f.startswith(f"{video_id}."):
            audio_file = os.path.join(audio_dir, f)
            break
            
    if audio_file:
        print(f"🔄 Found existing audio file: {audio_file}")
        print("🎙️ Proceeding directly to Whisper transcription...")
        text, lang_info = whisper_transcribe(audio_file)
    else:
        # Step 1: captions
        text, lang_info = get_caption_transcript(video_id)
        if text:
            print("✅ Used captions")
        else:
            # Step 2: Whisper fallback (Download & Transcribe)
            print("⚠️ No captions found, downloading and using Whisper...")
            audio_file = download_audio(url, video_id)
            text, lang_info = whisper_transcribe(audio_file)

    # Step 3: Save to transcript folder
    os.makedirs(transcript_dir, exist_ok=True)
    output_path = os.path.join(transcript_dir, f"{video_id}.txt")
    
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

