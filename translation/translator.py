from llm.ollama_client import call_ollama

# Prompt template for translating podcast scripts while preserving tone and emotion
TRANSLATION_PROMPT = """
Translate the following sports podcast script into {language}.

RULES:
- Keep commentary tone natural
- Keep excitement and emotion
- Do NOT summarize
- Preserve meaning
- Make it sound like a real sports commentator

Podcast Script:
{script}

Return ONLY translated text.
"""


def translate_script(script, language):
    """
    Translates a podcast script into a target language using LLM.
    
    Args:
        script (str): The original podcast script text.
        language (str): The target language for translation (e.g., 'Hindi', 'Spanish').
        
    Returns:
        str: The translated podcast script.
    """

    prompt = TRANSLATION_PROMPT.format(
        script=script,
        language=language
    )

    # Call LLM client to perform the translation
    response = call_ollama(prompt)

    return response.strip()