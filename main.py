import json
import time
import os

from transcript.transcript_extractor import get_transcript, extract_video_id
from llm.extractor import llm_extract
from llm.sport_detector import detect_sport
from generation.podcast_script_generator import (
    generate_podcast_script
)
from translation.translator import translate_script

def save_script(video_id, language, content):
    """Saves the script to a language-specific file inside a video-specific folder."""
    folder_path = os.path.join("scripts", video_id)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)
    
    file_path = os.path.join(folder_path, f"{language.lower()}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return file_path

def main():
    """
    Main entry point for the Podcast Generator pipeline.
    """

    start_time = time.time()

    url = "https://www.youtube.com/watch?v=MAm0RLQpYas"
    video_id = extract_video_id(url)
    target_language = "Hindi"

    # Define paths for check
    en_script_path = os.path.join("scripts", video_id, "english.txt")
    translated_script_path = os.path.join("scripts", video_id, f"{target_language.lower()}.txt")

    podcast_script = None
    translated_script = None

    # Reverse Order Check Logic
    if os.path.exists(translated_script_path):
        print(f"\n✅ Translated script found for {target_language} at {translated_script_path}")
        with open(translated_script_path, "r", encoding="utf-8") as f:
            translated_script = f.read()
    
    elif os.path.exists(en_script_path):
        print(f"\n✅ English podcast script found at {en_script_path}")
        with open(en_script_path, "r", encoding="utf-8") as f:
            podcast_script = f.read()
    else:
        # Full Pipeline Execution
        print("Fetching transcript...")
        transcript = get_transcript(url)

        # -----------------------------
        # STEP 1: SPORT DETECTION
        # -----------------------------
        print("\nDetecting sport...")
        sport = detect_sport(transcript)
        print(f"Detected sport: {sport}")

        # Clean up temporary state files
        for f in ["llm_chunk_state.json", "llm_chunk_results.jsonl", "main_output.txt", "debug_llm_output.txt"]:
            if os.path.exists(f): os.remove(f)

        # -----------------------------
        # STEP 2: STRUCTURED EXTRACTION
        # -----------------------------
        print("\nExtracting structured data...")
        structured_output = llm_extract(transcript, sport)

        # -----------------------------
        # STEP 3: PODCAST SCRIPT GENERATION
        # -----------------------------
        print("\nGenerating podcast script...")
        podcast_script = generate_podcast_script(structured_output)
        save_script(video_id, "english", podcast_script)
        print(f"✅ English script saved to {en_script_path}")

    # Step 4: Translation (if not already found)
    if not translated_script and podcast_script:
        print(f"\nTranslating to {target_language}...")
        translated_script = translate_script(podcast_script, target_language)
        save_script(video_id, target_language, translated_script)
        print(f"✅ Translated script saved to {translated_script_path}")

    # Output to console
    if podcast_script:
        print("\n--- PODCAST SCRIPT (EN) ---\n")
        print(podcast_script)
    
    if translated_script:
        print(f"\n--- {target_language.upper()} PODCAST ---\n")
        print(translated_script)

    end_time = time.time()
    print(f"\nTotal execution time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
