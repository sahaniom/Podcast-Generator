from llm.ollama_client import call_ollama


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
    sample = transcript[:1500]

    prompt = SPORT_PROMPT.format(transcript=sample)

    response = call_ollama(prompt)

    return response.strip().lower()