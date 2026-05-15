from translation.indictrans2_translator import (
    translate_to_indic
)


def translate_script(script, language):
    """
    Translates a podcast script into a target Indic language.
    
    This function acts as a wrapper for the IndicTrans2 translator,
    allowing the main pipeline to remain agnostic of the underlying 
    translation engine.

    Args:
        script (str): The English podcast script content.
        language (str): Destination Indic language (e.g., 'Hindi', 'Gujarati').

    Returns:
        str: The translated script text.
    """
    return translate_to_indic(
        script,
        language
    )


# * Following code is using Ollama LLM models for translation either Gemma2:2b or Qwen3.5:2b, but now we are using IndicTrans2 for translation. So this file is not being used currently, but we are keeping it for future reference if needed.
'''
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
'''