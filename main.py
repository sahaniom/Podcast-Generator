import json

from transcript.transcript_extractor import get_transcript
from llm.extractor import llm_extract


def main():
    """
    Main entry point for the Podcast Generator pipeline.
    It fetches a transcript from a YouTube URL and uses an LLM to extract structured sports data.
    """
    url = "https://www.youtube.com/watch?v=MAm0RLQpYas"

    print("Fetching transcript...")
    # Extract the transcript for the specified video URL
    transcript = get_transcript(url)

    print("Extracting structured data...")
    # Use LLM-based extraction to convert transcript into structured JSON
    structured_output = llm_extract(transcript)

    print("\n--- STRUCTURED OUTPUT ---\n")

    # Display the final structured data in a pretty-printed JSON format
    print(json.dumps(structured_output, indent=4))


if __name__ == "__main__":
    main()