import json
import time
import os
# from tts.mms_tts import generate_tts
from tts.dialogue_tts import generate_dialogue_tts
from audio_processing.podcast_mixer import create_podcast
from config import SUPPORTED_LANGUAGES

from transcript.transcript_extractor import get_transcript, extract_video_id
from llm.extractor import llm_extract
from llm.sport_detector import detect_sport
from generation.podcast_script_generator import (
    generate_podcast_script
)
from translation.translator import translate_script


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


def main(url=None, target_language=None):
    """
    Main entry point for the Podcast Generator pipeline.
    
    This function coordinates the sequential tasks required to turn a YouTube video
    into a synthesized local-language podcast:
      1. Prompt for target language and validate it against supported models.
      2. Check caching rules in reverse order (Translated Script -> English Script -> Full Pipeline).
      3. If no cached script exists:
         - Download/extract the video transcript (with fallback to Whisper transcription).
         - Detect the specific sport for contextual relevance.
         - Clear temporary/debug files from previous extraction attempts.
         - Perform structured info extraction using local LLMs.
         - Generate a dynamic, conversational English podcast script.
         - Save the English script.
      4. Translate the English podcast script using the IndicTrans2 translation module.
      5. Generate high-quality text-to-speech audio using Meta's MMS TTS models.
      6. Display results and output the execution benchmarks.
    """
    # Start tracking total pipeline execution time
    start_time = time.time()

    # Define the default target YouTube video URL
    # url = "https://www.youtube.com/watch?v=MAm0RLQpYas"
    if not url:
        url = input("Enter YouTube URL: ").strip()

    if not target_language:
        target_language = input(
            "Enter target language: "
        ).strip().title()
    video_id = extract_video_id(url)
    
    # Prompt the user to input the desired Indian language for the podcast
    # target_language = input("Enter target language: ").strip().title()

    # Stop execution early if the user selects an unsupported language
    if target_language not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported language: {target_language}")

    # Set up expected file system paths for intermediate and final assets
    en_script_path = os.path.join("scripts", video_id, "english.txt")
    translated_script_path = os.path.join(
        "scripts", video_id, f"{target_language.lower()}.txt")
    audio_output_path = save_audio_path(video_id, target_language)
    final_podcast_path = os.path.join(
        "outputs",
        video_id,
        f"{target_language.lower()}_podcast.wav"
    )

    podcast_script = None
    translated_script = None

    # -------------------------------------------------------------------------
    # REVERSE CACHING LOGIC
    # This prevents running heavy LLM or translation pipelines if work is already done.
    # -------------------------------------------------------------------------
    
    # Check Case A: The translated script already exists.
    # We can load it and skip both English generation and translation.
    if os.path.exists(translated_script_path):
        print(
            f"\n✅ Translated script found for {target_language} at {translated_script_path}")
        with open(translated_script_path, "r", encoding="utf-8") as f:
            translated_script = f.read()

    # Check Case B: The English script exists but translation is missing.
    # We load the English script and proceed directly to translation.
    elif os.path.exists(en_script_path):
        print(f"\n✅ English podcast script found at {en_script_path}")
        with open(en_script_path, "r", encoding="utf-8") as f:
            podcast_script = f.read()
            
    # Check Case C: No scripts exist. We must run the full ingestion & generation pipeline.
    else:
        # Step 1: Ingest transcript (via API or local faster-whisper fallback)
        print("Fetching transcript...")
        transcript = get_transcript(url)

        # -----------------------------
        # STEP 1: SPORT DETECTION
        # Determines if it's cricket, football, etc. to supply context for prompts
        # -----------------------------
        print("\nDetecting sport...")
        sport = detect_sport(transcript)
        print(f"Detected sport: {sport}")

        # Clean up temporary state files left behind by LLM chunking processes
        for f in ["llm_chunk_state.json", "llm_chunk_results.jsonl", "main_output.txt", "debug_llm_output.txt"]:
            if os.path.exists(f):
                os.remove(f)

        # -----------------------------
        # STEP 2: STRUCTURED EXTRACTION
        # Extracts match events, players, scores, and context in structured JSON format
        # -----------------------------
        print("\nExtracting structured data...")
        structured_output = llm_extract(transcript, sport)

        # -----------------------------
        # STEP 3: PODCAST SCRIPT GENERATION
        # Conversational script writing based on structured JSON data
        # -----------------------------
        print("\nGenerating podcast script...")
        podcast_script = generate_podcast_script(structured_output)
        save_script(video_id, "english", podcast_script)
        print(f"✅ English script saved to {en_script_path}")

    # -----------------------------
    # STEP 4: TRANSLATION
    # -----------------------------
    # Translate the English script if the translated version isn't already available
    if not translated_script and podcast_script:
        print(f"\nTranslating to {target_language}...")
        translated_script = translate_script(podcast_script, target_language)
        save_script(video_id, target_language, translated_script)
        print(f"✅ Translated script saved to {translated_script_path}")

    # -----------------------------
    # STEP 5: TEXT-TO-SPEECH (TTS) AUDIO GENERATION
    # -----------------------------
    # Synthesize the finalized local-language podcast audio if it doesn't already exist
    if translated_script:
        if os.path.exists(audio_output_path):
            print(f"\n✅ Audio already exists at: {audio_output_path}")

        else:
            print(f"\nGenerating {target_language} podcast audio...")

            # Run text-to-speech synthesis
            generate_dialogue_tts(
                script=translated_script,
                language=target_language,
                output_path=audio_output_path
            )

            print(f"✅ Audio saved at: {audio_output_path}")

            print("\nCreating final podcast with music...")

            create_podcast(
                voice_path=audio_output_path,

                output_path=final_podcast_path,

                intro_path="assets/intro_music.mp3",

                background_path="assets/background_music.mp3",

                outro_path="assets/outro_music.mp3"
            )

            print(f"✅ Final podcast saved at: {final_podcast_path}")

    # -----------------------------
    # STEP 6: CONSOLE OUTPUT & BENCHMARKING
    # -----------------------------
    # Display the final text output in both English and the target language
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

