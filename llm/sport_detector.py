from llm.ollama_client import call_ollama


# Prompt template for classifying the sport being discussed in a transcript.
# Ensures the model returns a single, parseable word from a predefined list.
SPORT_PROMPT = """
Detect the sport from this transcript.

Return ONLY one word.

Possible sports:
- cricket
- football
- basketball
- badminton

Transcript:
{transcript}
"""


def detect_sport(transcript):
    """
    Analyzes a sample of the transcript to detect which sport is being played/discussed.
    Uses the first 1500 characters of the transcript for efficient classification.

    Args:
        transcript (str): The full or partial transcript text.

    Returns:
        str: The detected sport in lowercase (e.g., 'cricket', 'football').
    """
    sample = transcript[:1500]

    prompt = SPORT_PROMPT.format(transcript=sample)

    response = call_ollama(prompt)

    return response.strip().lower()
