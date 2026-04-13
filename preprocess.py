import json
import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return text.strip()

def run_preprocessing(input_file="transcript_raw.json",
                      output_file="processed_data.json"):

    with open(input_file, "r") as f:
        segments = json.load(f)

    processed_data = []

    for seg in segments:
        processed_data.append({
            "start": seg["start"],
            "end": seg["end"],
            "clean_text": clean_text(seg["text"]),
            "original_text": seg["text"]
        })

    with open(output_file, "w") as f:
        json.dump(processed_data, f, indent=4)

    return processed_data