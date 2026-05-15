from llm.ollama_client import call_ollama
import json

# System prompt for the LLM to generate a podcast script from cricket match data
PODCAST_PROMPT = """
You are an exciting sports podcast narrator.

Generate a natural podcast-style match summary.

RULES:
- Make it engaging and conversational
- Keep the flow natural
- Mention important wickets, boundaries, turning points
- Mention final result
- Avoid repetition
- Do NOT mention every single event
- Create storytelling
- Keep it around 300-500 words
- Use energetic sports commentary style

Structured Match Data:
{data}

Generate ONLY the podcast narration text.
"""


def generate_podcast_script(data):
    """
    Generates a podcast narration script based on structured match data.
    
    Args:
        data (dict): Structured match events and summary data.
        
    Returns:
        str: The generated podcast script text.
    """

    json_data = json.dumps(
        data,
        indent=2
    )

    prompt = PODCAST_PROMPT.format(
        data=json_data
    )

    # Call the Ollama LLM client to generate the script
    response = call_ollama(prompt)

    return response.strip()


