import json
import time
import os
from pydub import AudioSegment
from tts.mms_tts import generate_tts
from tts.dialogue_tts import generate_dialogue_tts
from audio_processing.podcast_mixer import create_podcast
from config import SUPPORTED_LANGUAGES

from transcript.transcript_extractor import get_transcript, extract_video_id
from llm.extractor import llm_extract
from llm.sport_detector import detect_sport
from llm.summary_generator import generate_summary
from generation.podcast_script_generator import (
    generate_podcast_script
)
from translation.translator import translate_script
from translation.indictrans2_translator import translate_to_indic

SUMMARY_PHRASES = {
    "English": "Summary of the match",
    "Hindi": "मैच का सारांश",
    "Tamil": "ஆட்டத்தின் சுருக்கம்",
    "Telugu": "మ్యాచ్ సారాంశం",
    "Marathi": "सामन्याचा सारांश",
    "Gujarati": "મેचનો સારાંશ",
    "Kannada": "ಪಂದ್ಯದ ಸಾರಾಂಶ",
    "Malayalam": "മത്സരത്തിന്റെ സംഗ്രഹം",
    "Punjabi": "ਮੈਚ ਦਾ ਸਾਰ",
    "Bengali": "ম্যাচের সারসংক্ষেপ"
}


def save_script(video_id, language, content):
    """
    Saves the generated or translated script to a language-specific file inside a video-specific folder.

    Parameters:
    ----------
    video_id : str
        The unique YouTube video identifier (extracted from the URL).
    language : str
        The language of the script (e.g., 'english', 'hindi').
    content : str
        The text content of the script to save.

    Returns:
    -------
    str
        The absolute or relative file path where the script was written.
    """
    # Create the directory structure under 'scripts/{video_id}' if it does not already exist
    folder_path = os.path.join("scripts", video_id)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)

    # Save the script content as a lowercase language text file (e.g., 'scripts/MAm0RLQpYas/hindi.txt')
    file_path = os.path.join(folder_path, f"{language.lower()}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return file_path


def save_audio_path(video_id, language):
    """
    Constructs and returns the standard target audio output path for a specific language and video ID.
    If the parent directory doesn't exist, it creates it.

    Parameters:
    ----------
    video_id : str
        The unique YouTube video identifier.
    language : str
        The language of the synthesized audio (e.g., 'Hindi', 'Tamil').

    Returns:
    -------
    str
        The relative file path where the synthesized audio file should be saved (e.g., 'audio/MAm0RLQpYas/hindi.wav').
    """
    # Create the directory structure under 'audio/{video_id}' if it doesn't exist
    folder_path = os.path.join("audio", video_id)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)

    # Return the target WAV file path
    return os.path.join(
        folder_path,
        f"{language.lower()}.wav"
    )


def save_summary_audio_path(video_id, language):
    """
    Returns the cached summary audio output path for a specific language and video ID.
    """
    folder_path = os.path.join("audio", video_id)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)

    return os.path.join(
        folder_path,
        f"summary_{language.lower()}.wav"
    )


def generate_summary_only(url=None, target_language=None):
    """
    Generate only the summary text for the selected language.
    Returns the summary text so the UI can display it separately from the podcast.
    """
    if not url:
        url = input("Enter YouTube URL: ").strip()

    if not target_language:
        target_language = input("Enter target language: ").strip().title()

    video_id = extract_video_id(url)

    if target_language not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported language: {target_language}")

    summary_en_path = os.path.join("scripts", video_id, "summary_english.txt")
    summary_translated_path = os.path.join(
        "scripts", video_id, f"summary_{target_language.lower()}.txt"
    )

    translated_summary_script = None

    if target_language == "English":
        if os.path.exists(summary_en_path):
            with open(summary_en_path, "r", encoding="utf-8") as f:
                translated_summary_script = f.read()
        else:
            transcript = get_transcript(url)
            sport = detect_sport(transcript)
            translated_summary_script = generate_summary(transcript, sport)
            os.makedirs(os.path.dirname(summary_en_path), exist_ok=True)
            with open(summary_en_path, "w", encoding="utf-8") as f:
                f.write(translated_summary_script)
            print(f"✅ English summary saved to {summary_en_path}")
    else:
        if os.path.exists(summary_translated_path):
            with open(summary_translated_path, "r", encoding="utf-8") as f:
                translated_summary_script = f.read()
        elif os.path.exists(summary_en_path):
            with open(summary_en_path, "r", encoding="utf-8") as f:
                summary_script = f.read()
            translated_summary_script = translate_to_indic(
                summary_script,
                target_language
            )
            os.makedirs(os.path.dirname(summary_translated_path), exist_ok=True)
            with open(summary_translated_path, "w", encoding="utf-8") as f:
                f.write(translated_summary_script)
            print(f"✅ Translated summary saved to {summary_translated_path}")
        else:
            transcript = get_transcript(url)
            sport = detect_sport(transcript)
            summary_script = generate_summary(transcript, sport)
            os.makedirs(os.path.dirname(summary_en_path), exist_ok=True)
            with open(summary_en_path, "w", encoding="utf-8") as f:
                f.write(summary_script)
            print(f"✅ English summary saved to {summary_en_path}")

            translated_summary_script = translate_to_indic(
                summary_script,
                target_language
            )
            with open(summary_translated_path, "w", encoding="utf-8") as f:
                f.write(translated_summary_script)
            print(f"✅ Translated summary saved to {summary_translated_path}")

    print(f"\n--- {target_language.upper()} SUMMARY ---\n")
    print(translated_summary_script)

    return translated_summary_script


def generate_summary_audio(url=None, target_language=None):
    """
    Generate or load the summary text, synthesize summary audio, and return its path.
    """
    if not url:
        url = input("Enter YouTube URL: ").strip()

    if not target_language:
        target_language = input("Enter target language: ").strip().title()

    video_id = extract_video_id(url)

    summary_audio_path = save_summary_audio_path(video_id, target_language)

    if not os.path.exists(summary_audio_path):
        summary_text = generate_summary_only(url=url, target_language=target_language)
        summary_phrase = SUMMARY_PHRASES.get(target_language, "Summary of the match")
        full_summary_text = f"{summary_phrase}. {summary_text}"

        print(f"\nGenerating {target_language} summary audio...")
        generate_tts(
            text=full_summary_text,
            language=target_language,
            output_path=summary_audio_path
        )
        print(f"✅ Summary audio saved at: {summary_audio_path}")
    else:
        print(f"✅ Summary audio already exists at: {summary_audio_path}")

    return summary_audio_path


def combine_summary_and_podcast(summary_audio_path, podcast_audio_path, output_path):
    """
    Combines the summary audio and the podcast audio with a short pause in between.
    """
    print(f"\nCombining summary and podcast audio...")
    summary_audio = AudioSegment.from_wav(summary_audio_path)
    podcast_audio = AudioSegment.from_wav(podcast_audio_path)
    
    # 1 second pause between summary and podcast
    pause = AudioSegment.silent(duration=1000)
    
    combined = summary_audio + pause + podcast_audio
    
    combined.export(output_path, format="wav")
    print(f"✅ Combined final output saved at: {output_path}")


def main(url=None, target_language=None):
    """
    Main entry point for podcast generation.
    Returns the final podcast audio path with intro, background, and outro music.
    """
    start_time = time.time()

    if not url:
        url = input("Enter YouTube URL: ").strip()

    if not target_language:
        target_language = input("Enter target language: ").strip().title()

    video_id = extract_video_id(url)

    if target_language not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported language: {target_language}")

    en_script_path = os.path.join("scripts", video_id, "english.txt")
    translated_script_path = os.path.join(
        "scripts", video_id, f"{target_language.lower()}.txt"
    )
    audio_output_path = save_audio_path(video_id, target_language)
    final_podcast_path = os.path.join(
        "outputs",
        video_id,
        f"{target_language.lower()}_podcast.wav"
    )

    podcast_script = None
    translated_script = None

    if os.path.exists(translated_script_path):
        print(
            f"\n✅ Translated script found for {target_language} at {translated_script_path}"
        )
        with open(translated_script_path, "r", encoding="utf-8") as f:
            translated_script = f.read()
    elif os.path.exists(en_script_path):
        print(f"\n✅ English podcast script found at {en_script_path}")
        with open(en_script_path, "r", encoding="utf-8") as f:
            podcast_script = f.read()

    if not translated_script and not podcast_script:
        print("Fetching transcript...")
        transcript = get_transcript(url)

        print("\nDetecting sport...")
        sport = detect_sport(transcript)
        print(f"Detected sport: {sport}")

        for file_name in [
            "llm_chunk_state.json",
            "llm_chunk_results.jsonl",
            "main_output.txt",
            "debug_llm_output.txt",
        ]:
            if os.path.exists(file_name):
                os.remove(file_name)

        print("\nExtracting structured data...")
        structured_output = llm_extract(transcript, sport)

        print("\nGenerating podcast script...")
        podcast_script = generate_podcast_script(structured_output)
        save_script(video_id, "english", podcast_script)
        print(f"✅ English script saved to {en_script_path}")

    if target_language == "English":
        if podcast_script:
            translated_script = podcast_script
        else:
            with open(en_script_path, "r", encoding="utf-8") as f:
                translated_script = f.read()
        print("\nSkipping translation for English.")
    elif not translated_script and podcast_script:
        print(f"\nTranslating script to {target_language}...")
        translated_script = translate_script(
            podcast_script,
            target_language
        )
        save_script(video_id, target_language, translated_script)
        print(f"✅ Translated script saved to {translated_script_path}")

    if translated_script:
        if not os.path.exists(audio_output_path):
            print(f"\nGenerating {target_language} podcast audio...")
            generate_dialogue_tts(
                script=translated_script,
                language=target_language,
                output_path=audio_output_path
            )
            print(f"✅ Audio saved at: {audio_output_path}")
        else:
            print(f"\n✅ Audio already exists at: {audio_output_path}")

        if not os.path.exists(final_podcast_path):
            print("\nCreating final podcast with music...")
            create_podcast(
                voice_path=audio_output_path,
                output_path=final_podcast_path,
                intro_path="assets/intro_music.mp3",
                background_path="assets/background_music.mp3",
                outro_path="assets/outro_music.mp3"
            )
            print(f"✅ Final podcast saved at: {final_podcast_path}")
        else:
            print(f"✅ Final podcast already exists at: {final_podcast_path}")

    if podcast_script:
        print("\n--- PODCAST SCRIPT (EN) ---\n")
        print(podcast_script)

    if translated_script:
        print(f"\n--- {target_language.upper()} PODCAST ---\n")
        print(translated_script)

    end_time = time.time()
    print(f"\nTotal execution time: {end_time - start_time:.2f} seconds")

    return final_podcast_path


if __name__ == "__main__":
    main()

