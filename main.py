import json
import time

from transcript.transcript_extractor import get_transcript
from llm.extractor import llm_extract


def main():
    """
    Main entry point for the Podcast Generator pipeline.
    It fetches a transcript from a YouTube URL and uses an LLM to extract structured sports data.
    """
    start_time = time.time()
    url = "https://www.youtube.com/watch?v=MAm0RLQpYas"

    print("Fetching transcript...")
    # Extract the transcript for the specified video URL
    transcript = get_transcript(url)

    print("Extracting structured data...")
    # Use LLM-based extraction to convert transcript into structured JSON
    structured_output = llm_extract(transcript)

    print("\n--- STRUCTURED OUTPUT ---\n")

    # Display the final structured data in a pretty-printed JSON format
    output_json = json.dumps(structured_output, indent=4)
    print(output_json)

    end_time = time.time()
    total_time = end_time - start_time
    time_message = f"\nTotal execution time: {total_time:.2f} seconds"
    print(time_message)

    # Write the output and execution time to a local file
    with open("main_output.txt", "w", encoding="utf-8") as f:
        f.write("--- STRUCTURED OUTPUT ---\n\n")
        f.write(output_json)
        f.write("\n" + time_message)
    print(f"\n💾 Output saved to: main_output.txt")


if __name__ == "__main__":
    main()