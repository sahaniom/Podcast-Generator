import json
import time
import os

from transcript.transcript_extractor import get_transcript
from llm.extractor import llm_extract
from llm.sport_detector import detect_sport


def main():
    """
    Main entry point for the Podcast Generator pipeline.
    """

    start_time = time.time()

    url = "https://www.youtube.com/watch?v=MAm0RLQpYas"

    # Fetch the transcript for the given YouTube URL
    print("Fetching transcript...")
    transcript = get_transcript(url)

    # -----------------------------
    # STEP 1: SPORT DETECTION
    # -----------------------------
    # Analyze the transcript to identify which sport is being discussed
    print("\nDetecting sport...")
    sport = detect_sport(transcript)

    print(f"Detected sport: {sport}")

    # Clean up state files from previous runs to ensure fresh data
    if os.path.exists("llm_chunk_state.json"):
        os.remove("llm_chunk_state.json")

    if os.path.exists("llm_chunk_results.jsonl"):
        os.remove("llm_chunk_results.jsonl")
    
    if os.path.exists("main_output.txt"):
        os.remove("main_output.txt")
    
    if os.path.exists("debug_llm_output.txt"):
        os.remove("debug_llm_output.txt")

    # -----------------------------
    # STEP 2: STRUCTURED EXTRACTION
    # -----------------------------
    # Use LLM to extract highlights, statistics, and key moments from the transcript
    print("\nExtracting structured data...")
    structured_output = llm_extract(transcript, sport)

    print("\n--- STRUCTURED OUTPUT ---\n")

    output_json = json.dumps(structured_output, indent=4)
    print(output_json)

    end_time = time.time()
    total_time = end_time - start_time
    time_message = f"\nTotal execution time: {total_time:.2f} seconds"

    print(time_message)

    # Persist the final structured JSON and timing info to a text file
    with open("main_output.txt", "w", encoding="utf-8") as f:
        f.write("--- STRUCTURED OUTPUT ---\n\n")
        f.write(output_json)
        f.write("\n" + time_message)

    print(f"\n💾 Output saved to: main_output.txt")


if __name__ == "__main__":
    main()
