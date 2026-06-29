from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer
)

import torch
import re

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


DEVANAGARI_TO_TARGET = {
    "Bengali": {
        "अ": "অ", "आ": "আ", "इ": "ই", "ई": "ঈ", "उ": "উ", "ऊ": "ঊ",
        "ऋ": "ঋ", "ॠ": "ৠ", "ऌ": "ঌ", "ॡ": "ৡ", "ए": "এ", "ऐ": "ঐ",
        "ओ": "ও", "औ": "ঔ", "ं": "ং", "ः": "ঃ", "्": "্",
        "ा": "া", "ि": "ি", "ी": "ী", "ु": "ু", "ू": "ূ", "ृ": "ৃ",
        "ॄ": "ৄ", "ॢ": "ৢ", "ॣ": "ৣ", "े": "ে", "ै": "ৈ", "ो": "ো", "ौ": "ৌ",
        "क": "ক", "ख": "খ", "ग": "গ", "घ": "ঘ", "ङ": "ঙ", "च": "চ",
        "छ": "ছ", "ज": "জ", "झ": "ঝ", "ञ": "ঞ", "ट": "ট", "ठ": "ঠ",
        "ड": "ড", "ढ": "ঢ", "ण": "ণ", "त": "ত", "थ": "থ", "द": "দ",
        "ध": "ধ", "न": "ন", "प": "প", "फ": "ফ", "ब": "ব", "भ": "ভ",
        "म": "ম", "य": "য", "र": "র", "ल": "ল", "व": "ব", "श": "শ",
        "ष": "ষ", "स": "স", "ह": "হ", "ळ": "ল",
        "०": "০", "१": "১", "२": "২", "३": "৩", "४": "৪", "५": "৫",
        "६": "৬", "७": "৭", "८": "৮", "९": "৯",
    },
    "Tamil": {
        "अ": "அ", "आ": "ஆ", "इ": "இ", "ई": "ஈ", "उ": "உ", "ऊ": "ஊ",
        "ऋ": "ரு", "ॠ": "ரூ", "ऌ": "லு", "ॡ": "லூ", "ए": "ஏ", "ऐ": "ஐ",
        "ओ": "ஓ", "औ": "ஔ", "ं": "ஂ", "ः": "ஃ", "्": "்",
        "ा": "ா", "ि": "ி", "ी": "ீ", "ु": "ு", "ू": "ூ", "ृ": "ு",
        "ॄ": "ூ", "ॢ": "ு", "ॣ": "ூ", "े": "ே", "ै": "ை", "ो": "ோ", "ौ": "ௌ",
        "क": "க", "ख": "க", "ग": "க", "घ": "க", "ङ": "ங", "च": "ச",
        "छ": "ச", "ज": "ஜ", "झ": "ஜ", "ञ": "ஞ", "ट": "ட", "ठ": "ட",
        "ड": "ட", "ढ": "ட", "ण": "ண", "त": "த", "थ": "த", "द": "த",
        "ध": "த", "न": "ந", "प": "ப", "फ": "ப", "ब": "ப", "भ": "ப",
        "म": "ம", "य": "ய", "र": "ர", "ल": "ல", "व": "வ", "श": "ஷ",
        "ष": "ஷ", "स": "ஸ", "ह": "ஹ", "ळ": "ள",
        "०": "௦", "१": "௧", "२": "௨", "३": "௩", "४": "௪", "५": "௫",
        "६": "௬", "७": "௭", "८": "௮", "९": "௯",
    },
    "Telugu": {
        "अ": "అ", "आ": "ఆ", "इ": "ఇ", "ई": "ఈ", "उ": "ఉ", "ऊ": "ఊ",
        "ऋ": "ృ", "ॠ": "ౠ", "ऌ": "ౢ", "ॡ": "ౣ", "ए": "ఏ", "ऐ": "ఐ",
        "ओ": "ఓ", "औ": "ఔ", "ं": "ం", "ः": "ః", "्": "్",
        "ा": "ా", "ि": "ి", "ी": "ీ", "ु": "ు", "ू": "ూ", "ृ": "ృ",
        "ॄ": "ౄ", "ॢ": "ౢ", "ॣ": "ౣ", "े": "ే", "ै": "ై", "ो": "ో", "ौ": "ౌ",
        "क": "క", "ख": "ఖ", "ग": "గ", "घ": "ఘ", "ङ": "ఙ", "च": "చ",
        "छ": "ఛ", "ज": "జ", "झ": "ఝ", "ञ": "ఞ", "ट": "ట", "ठ": "ఠ",
        "ड": "డ", "ढ": "ఢ", "ण": "ణ", "त": "త", "थ": "థ", "द": "ద",
        "ध": "ధ", "न": "న", "प": "ప", "फ": "ఫ", "ब": "బ", "भ": "భ",
        "म": "మ", "य": "య", "र": "ర", "ल": "ల", "व": "వ", "श": "శ",
        "ष": "ష", "स": "స", "ह": "హ", "ळ": "ళ",
        "०": "౦", "१": "౧", "२": "౨", "३": "౩", "४": "౪", "५": "౫",
        "६": "౬", "७": "౭", "८": "౮", "९": "౯",
    },
    "Gujarati": {
        "अ": "અ", "आ": "આ", "इ": "ઇ", "ई": "ઈ", "उ": "ઉ", "ऊ": "ઊ",
        "ऋ": "ઋ", "ॠ": "ૠ", "ऌ": "ઌ", "ॡ": "ૡ", "ए": "એ", "ऐ": "ઐ",
        "ओ": "ઓ", "औ": "ઔ", "ं": "ં", "ः": "ઃ", "्": "્",
        "ा": "ા", "ि": "િ", "ी": "ી", "ु": "ુ", "ू": "ૂ", "ृ": "ૃ",
        "ॄ": "ૄ", "ॢ": "ૢ", "ॣ": "ૣ", "े": "ે", "ै": "ૈ", "ो": "ો", "ौ": "ૌ",
        "क": "ક", "ख": "ખ", "ग": "ગ", "घ": "ઘ", "ङ": "ઙ", "च": "ચ",
        "छ": "છ", "ज": "જ", "झ": "ઝ", "ञ": "ઞ", "ट": "ટ", "ठ": "ઠ",
        "ड": "ડ", "ढ": "ઢ", "ण": "ણ", "त": "ત", "थ": "થ", "द": "દ",
        "ध": "ધ", "न": "ન", "प": "પ", "फ": "ફ", "ब": "બ", "भ": "ભ",
        "म": "મ", "य": "ય", "र": "ર", "ल": "લ", "व": "વ", "श": "શ",
        "ष": "ષ", "स": "સ", "ह": "હ", "ळ": "ળ",
        "०": "૦", "१": "૧", "२": "૨", "३": "૩", "४": "૪", "५": "૫",
        "६": "૬", "७": "૭", "८": "૮", "९": "૯",
    },
    "Kannada": {
        "अ": "ಅ", "आ": "ಆ", "इ": "ಇ", "ई": "ಈ", "उ": "ಉ", "ऊ": "ಊ",
        "ऋ": "ಋ", "ॠ": "ೠ", "ऌ": "ಌ", "ॡ": "ೡ", "ए": "ಏ", "ऐ": "ಐ",
        "ओ": "ಓ", "औ": "ಔ", "ं": "ಂ", "ः": "ಃ", "्": "್",
        "ा": "ಾ", "ि": "ಿ", "ी": "ೀ", "ु": "ು", "ू": "ೂ", "ृ": "ೃ",
        "ॄ": "ೄ", "ॢ": "ೢ", "ॣ": "ೣ", "े": "ೇ", "ै": "ೈ", "ो": "ೋ", "ौ": "ೌ",
        "क": "ಕ", "ख": "ಖ", "ग": "ಗ", "घ": "ಘ", "ङ": "ಙ", "च": "ಚ",
        "छ": "ಛ", "ज": "ಜ", "झ": "ಝ", "ञ": "ಞ", "ट": "ಟ", "ठ": "ಠ",
        "ड": "ಡ", "ढ": "ಢ", "ण": "ಣ", "त": "ತ", "थ": "ಥ", "द": "ದ",
        "ध": "ಧ", "न": "ನ", "प": "ಪ", "फ": "ಫ", "ब": "ಬ", "भ": "ಭ",
        "म": "ಮ", "य": "ಯ", "र": "ರ", "ल": "ಲ", "व": "ವ", "श": "ಶ",
        "ष": "ಷ", "स": "ಸ", "ह": "ಹ", "ळ": "ಳ",
        "०": "೦", "१": "೧", "२": "೨", "३": "೩", "४": "೪", "५": "೫",
        "६": "೬", "७": "೭", "८": "೮", "९": "೯",
    },
    "Malayalam": {
        "अ": "അ", "आ": "ആ", "इ": "ഇ", "ई": "ഈ", "उ": "ഉ", "ऊ": "ഊ",
        "ऋ": "ൃ", "ॠ": "ൠ", "ऌ": "ൢ", "ॡ": "ൡ", "ए": "ഏ", "ऐ": "ഐ",
        "ओ": "ഓ", "औ": "ഔ", "ं": "ം", "ः": "ഃ", "्": "്",
        "ा": "ാ", "ि": "ി", "ी": "ീ", "ु": "ു", "ू": "ൂ", "ृ": "ൃ",
        "ॄ": "ൄ", "ॢ": "ൢ", "ॣ": "ൣ", "े": "േ", "ै": "ൈ", "ो": "ോ", "ौ": "ൌ",
        "क": "ക", "ख": "ഖ", "ग": "ഗ", "घ": "ഘ", "ङ": "ങ", "च": "ച",
        "छ": "ഛ", "ज": "ജ", "झ": "ഝ", "ञ": "ഞ", "ट": "ട", "ठ": "ഠ",
        "ड": "ഡ", "ढ": "ഢ", "ण": "ണ", "त": "ത", "थ": "ഥ", "द": "ദ",
        "ध": "ധ", "न": "ന", "प": "പ", "फ": "ഫ", "ब": "ബ", "भ": "ഭ",
        "म": "മ", "य": "യ", "र": "ര", "ल": "ല", "व": "വ", "श": "ശ",
        "ष": "ഷ", "स": "സ", "ह": "ഹ", "ळ": "ള",
        "०": "൦", "१": "൧", "२": "൨", "३": "൩", "४": "൪", "५": "൫",
        "६": "൬", "७": "൭", "८": "൮", "९": "൯",
    },
    "Punjabi": {
        "अ": "ਅ", "आ": "ਆ", "इ": "ਇ", "ई": "ਈ", "उ": "ਉ", "ऊ": "ਊ",
        "ऋ": "੠", "ॠ": "੡", "ऌ": "਌", "ॡ": "੡", "ए": "ਏ", "ऐ": "ਐ",
        "ओ": "ਓ", "औ": "ਔ", "ं": "ਂ", "ः": "ਃ", "्": "੍",
        "ा": "ਾ", "ि": "ਿ", "ी": "ੀ", "ु": "ੁ", "ू": "ੂ", "ृ": "੃",
        "ॄ": "੄", "ॢ": "੢", "ॣ": "੣", "े": "ੇ", "ै": "ੈ", "ो": "ੋ", "ौ": "ੌ",
        "क": "ਕ", "ख": "ਖ", "ग": "ਗ", "घ": "ਘ", "ङ": "ਙ", "च": "ਚ",
        "छ": "ਛ", "ज": "ਜ", "झ": "ਝ", "ञ": "ਞ", "ट": "ਟ", "ठ": "ਠ",
        "ड": "ਡ", "ढ": "ਢ", "ण": "ਣ", "त": "ਤ", "थ": "ਥ", "द": "ਦ",
        "ध": "ਧ", "न": "ਨ", "प": "ਪ", "फ": "ਫ", "ब": "ਬ", "भ": "ਭ",
        "म": "ਮ", "य": "ਯ", "र": "ਰ", "ल": "ਲ", "व": "ਵ", "श": "ਸ਼",
        "ष": "ਸ਼", "स": "ਸ", "ह": "ਹ", "ळ": "ਲ",
        "०": "੦", "१": "੧", "२": "੨", "३": "੩", "४": "੪", "५": "੫",
        "६": "੬", "७": "੭", "८": "੮", "९": "੯",
    },
}


def clean_translated_text(text):
    """
    Remove markdown-like artifacts that can leak into the translated summary.
    """
    text = re.sub(r"^\s*#+\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"\*+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_tts_text(text, target_language):
    """
    Convert mixed Devanagari-heavy output into the expected target Indic script.

    This is a best-effort fallback for MMS TTS models, which need native-script
    input to tokenize correctly.
    """
    if target_language in {"Hindi", "Marathi"}:
        return text

    mapping = DEVANAGARI_TO_TARGET.get(target_language)
    if not mapping:
        return text

    return text.translate(str.maketrans(mapping))



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

    text = clean_translated_text(text)

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
        skip_special_tokens=True,
        clean_up_tokenization_spaces=True
    )[0]

    translated_text = clean_translated_text(translated_text)
    translated_text = normalize_tts_text(translated_text, target_language)

    return translated_text
