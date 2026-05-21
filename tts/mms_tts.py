import os
import re
import shutil
import torch
import soundfile as sf

from pydub import AudioSegment
from transformers import VitsModel, AutoTokenizer

# Mapping of supported natural languages to Meta's MMS (Massively Multilingual Speech)
# pre-trained VITS Text-to-Speech model identifiers hosted on Hugging Face.
LANGUAGE_MODELS = {
    "English": "facebook/mms-tts-eng",
    "Hindi": "facebook/mms-tts-hin",
    "Tamil": "facebook/mms-tts-tam",
    "Bengali": "facebook/mms-tts-ben",
    "Telugu": "facebook/mms-tts-tel",
    "Marathi": "facebook/mms-tts-mar",
    "Gujarati": "facebook/mms-tts-guj",
    "Kannada": "facebook/mms-tts-kan",
    "Malayalam": "facebook/mms-tts-mal",
    "Punjabi": "facebook/mms-tts-pan"
}

# In-memory dictionary cache to prevent re-instantiating heavy tokenizer and model pairs 
# on successive synthesis requests during a single execution.
_loaded_models = {}


def load_model(language):
    """
    Loads and caches the Hugging Face Tokenizer and VitsModel for the specified target language.

    Parameters:
    ----------
    language : str
        The name of the target language (e.g., 'Hindi', 'Tamil').

    Returns:
    -------
    tuple (AutoTokenizer, VitsModel)
        The loaded tokenizer and TTS model instances.
    """
    if language not in LANGUAGE_MODELS:
        raise ValueError(f"Unsupported language: {language}")

    # Check if the model is already in our in-memory cache to save startup/GPU time
    if language not in _loaded_models:
        model_name = LANGUAGE_MODELS[language]

        print(f"\nLoading TTS model for {language}...")
        print(f"Model: {model_name}")

        # Instantiate tokenizer and VITS architecture TTS model from Hugging Face
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = VitsModel.from_pretrained(model_name)

        # Store in cache
        _loaded_models[language] = (tokenizer, model)

    return _loaded_models[language]


def split_text_into_chunks(text):
    """
    Splits a large input text block into a list of sentence-level chunks to keep
    the TTS model context clean and avoid input length limits.
    
    The splitter handles standard English terminal punctuation (., !, ?) as well 
    as the Devanagari full stop/danda (।).

    Parameters:
    ----------
    text : str
        The full text to split.

    Returns:
    -------
    list of str
        A list of cleaned sentence chunks.
    """
    # Regex split pattern utilizing positive lookbehind for sentence terminal marks:
    # (?<=[।.!?]) checks for danda, period, exclamation, or question mark, followed by spaces.
    sentences = re.split(r'(?<=[।.!?])\s+', text)

    cleaned = []
    for sentence in sentences:
        sentence = sentence.strip()
        # Keep only non-empty string chunks
        if sentence:
            cleaned.append(sentence)

    return cleaned


def generate_single_chunk(text, tokenizer, model, output_path):
    """
    Synthesizes speech for a single text sentence chunk and saves it as a WAV file.

    Parameters:
    ----------
    text : str
        A single sentence of text to synthesize.
    tokenizer : AutoTokenizer
        The tokenizer corresponding to the loaded language model.
    model : VitsModel
        The loaded VitsModel instance.
    output_path : str
        The path where the temporary WAV chunk should be written.
    """
    # Tokenize the input string into standard PyTorch tensors
    inputs = tokenizer(text, return_tensors="pt")

    # Disable gradient computation for faster inference and lower memory usage
    with torch.no_grad():
        output = model(**inputs).waveform

    # Squeeze extra dimensions, pull the array from GPU (if applicable) to CPU, and convert to NumPy
    waveform = output.squeeze().cpu().numpy()

    # Save waveform as a standard audio file using soundfile at the model's target sampling rate (usually 16000Hz or 22050Hz)
    sf.write(
        output_path,
        waveform,
        model.config.sampling_rate
    )


def merge_audio_files(chunk_files, final_output_path):
    """
    Stitches multiple small sentence WAV chunks together, inserting a realistic 
    conversational pause between sentences.

    Parameters:
    ----------
    chunk_files : list of str
        Ordered list of file paths pointing to temporary audio chunks.
    final_output_path : str
        Target file path for the full merged audio file.
    """
    # Initialize an empty PyDub AudioSegment container
    combined = AudioSegment.empty()

    # Create a 400ms silent audio segment to simulate natural spacing between sentences
    pause = AudioSegment.silent(duration=400)

    # Append each WAV file along with the pause segment
    for chunk in chunk_files:
        audio = AudioSegment.from_wav(chunk)
        combined += audio + pause

    # Export the final compiled audio output
    combined.export(final_output_path, format="wav")


def generate_tts(text, language, output_path):
    """
    High-level orchestration API that generates high-quality multi-lingual 
    text-to-speech audio for an entire script.

    The execution flow is as follows:
      1. Load or fetch tokenizer & model for target language.
      2. Split the script into sentence chunks.
      3. Clean and prepare a temporary directory.
      4. Synthesize WAV files for each chunk sequentially.
      5. Stitch/Merge the temporary WAV files with 400ms inter-sentence pauses.
      6. Clean up temporary directories and save the merged file.

    Parameters:
    ----------
    text : str
        The script text content (e.g., translated Hindi script).
    language : str
        The target language name matching the supported set.
    output_path : str
        The destination file path where the final WAV should be saved.

    Returns:
    -------
    str
        The final audio output path.
    """
    # Load required model and tokenizer (from cache if already retrieved)
    tokenizer, model = load_model(language)

    # Segment text into single-sentence chunks
    chunks = split_text_into_chunks(text)

    # Define path for temporary file processing
    temp_dir = "temp_tts_chunks"

    # Reset the temp directory if it exists to ensure a clean run
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

    os.makedirs(temp_dir, exist_ok=True)

    chunk_files = []

    print(f"\nGenerating {len(chunks)} audio chunks...")

    # Synthesize each individual text segment
    for idx, chunk in enumerate(chunks):
        chunk_path = os.path.join(
            temp_dir,
            f"chunk_{idx}.wav"
        )

        print(f"Generating chunk {idx + 1}/{len(chunks)}")

        generate_single_chunk(
            chunk,
            tokenizer,
            model,
            chunk_path
        )

        chunk_files.append(chunk_path)

    # Ensure output parent directory is available
    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    print("\nMerging audio chunks...")

    # Merge individual sentences with natural gaps
    merge_audio_files(
        chunk_files,
        output_path
    )

    # Clean up the intermediate working directory
    shutil.rmtree(temp_dir)

    return output_path

