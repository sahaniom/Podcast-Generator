import re

from translation.indictrans2_translator import (
    translate_to_indic
)


def parse_dialogue(script):
    """
    Extract speaker dialogue blocks.
    """

    pattern = r"\[(HOST|GUEST|NARRATOR)\]\s*(.*?)(?=\[(HOST|GUEST|NARRATOR)\]|$)"

    matches = re.findall(
        pattern,
        script,
        re.DOTALL
    )

    dialogue = []

    for match in matches:

        speaker = match[0]

        text = match[1].strip()

        if text:

            dialogue.append({
                "speaker": speaker,
                "text": text
            })

    return dialogue


def translate_script(script, language):
    """
    Translate dialogue block-by-block.
    """

    dialogue = parse_dialogue(script)

    translated_blocks = []

    for item in dialogue:

        speaker = item["speaker"]
        text = item["text"]

        translated_text = translate_to_indic(
            text,
            language
        )

        translated_blocks.append(
            f"[{speaker}]\n{translated_text}"
        )

    return "\n\n".join(translated_blocks)



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