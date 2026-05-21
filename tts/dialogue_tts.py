import re
import os
import shutil

from pydub import AudioSegment

from tts.mms_tts import generate_tts


def parse_dialogue(script):
    """
    Extract structured speaker dialogue blocks.
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

        # Remove accidental leftover tags
        text = re.sub(r"\[.*?\]", "", text).strip()

        if text:

            dialogue.append({
                "speaker": speaker,
                "text": text
            })

    return dialogue


def merge_dialogue_audio(dialogue_items, output_path):
    """
    Merge styled dialogue audio.
    """

    combined = AudioSegment.empty()

    pause = AudioSegment.silent(duration=500)

    for item in dialogue_items:

        speaker = item["speaker"]

        audio = AudioSegment.from_wav(
            item["file"]
        )

        # Apply voice style
        audio = apply_speaker_style(
            audio,
            speaker
        )

        combined += audio + pause

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    combined.export(
        output_path,
        format="wav"
    )


def apply_speaker_style(audio, speaker):
    """
    Apply lightweight voice styling
    to simulate different speakers.
    """

    if speaker == "HOST":

        # Slightly louder + faster
        audio = audio + 2
        audio = audio.speedup(playback_speed=1.05)

    elif speaker == "GUEST":

        # Slightly softer
        audio = audio - 1

    elif speaker == "NARRATOR":

        # Slower and calmer
        audio = audio.speedup(playback_speed=0.95)

    return audio


def generate_dialogue_tts(
    script,
    language,
    output_path
):
    """
    Generate multi-speaker dialogue audio.
    """

    dialogue = parse_dialogue(script)

    temp_dir = "temp_dialogue_audio"

    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

    os.makedirs(temp_dir, exist_ok=True)

    generated_files = []

    print(f"\nGenerating dialogue audio...")

    for idx, item in enumerate(dialogue):

        speaker = item["speaker"]
        text = item["text"]

        chunk_path = os.path.join(
            temp_dir,
            f"{idx}_{speaker.lower()}.wav"
        )

        print(f"\nSpeaker: {speaker}")
        print(f"Generating segment {idx + 1}/{len(dialogue)}")

        generate_tts(
            text=text,
            language=language,
            output_path=chunk_path
        )

        generated_files.append({
            "speaker": speaker,
            "file": chunk_path
        })

    print("\nMerging dialogue audio...")

    merge_dialogue_audio(
        generated_files,
        output_path
    )

    shutil.rmtree(temp_dir)

    return output_path

