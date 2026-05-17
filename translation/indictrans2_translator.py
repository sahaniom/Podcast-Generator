from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer
)

import torch

# High-quality open-source model for English to Indic language translation
MODEL_NAME = "ai4bharat/indictrans2-en-indic-dist-200M"


print("Loading IndicTrans2 model...")

# Load tokenizer and model from Hugging Face
tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True
)

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True
)

# Move model to GPU if available for faster inference
device = "cuda" if torch.cuda.is_available() else "cpu"

model.to(device)

print(f"IndicTrans2 loaded on {device}")


# Mapping of human-readable language names to IndicTrans2 script codes
LANGUAGE_CODES = {
    "Hindi": "hin_Deva",
    "Bengali": "ben_Beng",
    "Tamil": "tam_Taml",
    "Telugu": "tel_Telu",
    "Marathi": "mar_Deva",
    "Gujarati": "guj_Gujr",
    "Kannada": "kan_Knda",
    "Malayalam": "mal_Mlym",
    "Punjabi": "pan_Guru"
}



def translate_to_indic(text, target_language):
    """
    Translates English text into a supported Indic language using IndicTrans2.

    Args:
        text (str): The English text to translate.
        target_language (str): Key from LANGUAGE_CODES (e.g., 'Hindi').

    Returns:
        str: Translated text in the target script.

    Raises:
        ValueError: If the requested language is not in the supported list.
    """

    target_code = LANGUAGE_CODES.get(
        target_language
    )

    if not target_code:
        raise ValueError(
            f"Unsupported language: {target_language}"
        )

    # Tokenize input text and move tensors to target device
    input_text = f"eng_Latn {target_code} {text}"
    batch = tokenizer(
        [input_text],
        return_tensors="pt",
        padding=True,
        truncation=True
    ).to(device)

    # Generate translation using Seq2Seq model
    generated_ids = model.generate(
        **batch,
        max_length=1024
    )

    # Decode the output tokens back into readable text
    translated_text = tokenizer.batch_decode(
        generated_ids,
        skip_special_tokens=True
    )[0]

    return translated_text
