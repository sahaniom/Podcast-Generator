from llm.ollama_client import call_ollama
import json

# System prompt for the LLM to generate a podcast script from cricket match data
PODCAST_PROMPT = """
You are an expert sports podcast writer.

Generate an exciting and natural multi-speaker sports podcast conversation.

IMPORTANT RULES:
- Use ONLY these speaker tags:
  [HOST]
  [GUEST]
  [NARRATOR]

- HOST should guide the discussion
- GUEST should provide insights and reactions
- NARRATOR should occasionally provide transitions
- Make the interaction dynamic and conversational
- Keep it engaging and energetic
- Mention important wickets, boundaries, turning points
- Mention the final result
- Avoid repetition
- Do NOT mention every single event
- Create storytelling and emotional momentum
- Keep it around 300-500 words
- Make it sound like a real sports podcast
- Do NOT use markdown
- Do NOT add stage directions

Structured Match Data:
{data}

Generate ONLY the podcast script.
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


