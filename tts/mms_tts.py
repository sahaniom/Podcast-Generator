"""
MMS Text-to-Speech (TTS) Module
===============================
This module provides functionality to generate high-quality speech audio from text using 
Facebook's Massively Multilingual Speech (MMS) TTS models. The models are based on the 
VITS (Variational Inference with adversarial learning for end-to-end Text-to-Speech) 
architecture, developed by Meta AI.

Supported Languages:
- Hindi, Tamil, Bengali, Telugu, Marathi, Gujarati, Kannada, Malayalam, Punjabi

Features:
1. Dynamic model loading and caching to save memory and reduce loading overhead.
2. Local CPU/GPU execution leveraging Hugging Face Transformers and PyTorch.
3. Seamless integration with the 'soundfile' library to write output audio waves.
"""

import os
import torch
import soundfile as sf
from transformers import VitsModel, AutoTokenizer

# Mapping of supported human-readable language names to their respective Meta MMS model identifiers on Hugging Face.
# These models are trained specifically for TTS in each respective language.
LANGUAGE_MODELS = {
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

# Global in-memory cache to store instantiated (tokenizer, model) tuples.
# This prevents redundant downloads and reloading of heavy weights across multiple calls.
_loaded_models = {}


def load_model(language):
    """
    Dynamically loads and caches the Hugging Face MMS TTS model and tokenizer 
    for the specified language.

    Parameters:
    -----------
    language : str
        The human-readable name of the language (must be a key in LANGUAGE_MODELS).

    Returns:
    --------
    tuple (AutoTokenizer, VitsModel)
        The loaded and cached tokenizer and model instance.

    Raises:
    -------
    ValueError
        If the requested language is not supported.
    """
    # 1. Validate if the requested language is supported
    if language not in LANGUAGE_MODELS:
        raise ValueError(f"Unsupported language: {language}. Supported options: {list(LANGUAGE_MODELS.keys())}")

    # 2. Check if the model is already loaded in the cache; if not, load it
    if language not in _loaded_models:
        model_name = LANGUAGE_MODELS[language]

        print(f"Loading TTS model for {language}...")
        print(f"Model Identifier: {model_name}")

        # Load the tokenizer and model from Hugging Face Hub (cached locally after first run)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = VitsModel.from_pretrained(model_name)

        # Store in the global cache
        _loaded_models[language] = (tokenizer, model)

    # Return the cached or newly loaded model-tokenizer pair
    return _loaded_models[language]


def generate_tts(text, language, output_path):
    """
    Generates high-quality speech audio from text and saves it as a WAV file.

    Parameters:
    -----------
    text : str
        The input text string to convert to speech.
    language : str
        The target language for the speech generation.
    output_path : str
        The destination file path where the generated WAV file will be saved.

    Returns:
    --------
    str
        The file path of the successfully generated audio.
    """
    # 1. Fetch the corresponding tokenizer and model (utilizing dynamic loading & caching)
    tokenizer, model = load_model(language)

    # 2. Tokenize the input text and format it as PyTorch tensors ("pt")
    inputs = tokenizer(text, return_tensors="pt")

    # 3. Perform model inference. Disabling gradient tracking saves memory and computation time.
    with torch.no_grad():
        output = model(**inputs).waveform

    # 4. Extract and post-process the audio waveform
    # Squeeze: removes dimensions of size 1 (converting from batch/channel shape to flat 1D sequence)
    # CPU: moves the tensor to CPU memory if it was processed on a GPU
    # Numpy: converts the PyTorch tensor to a standard NumPy array for file-writing
    waveform = output.squeeze().cpu().numpy()

    # 5. Ensure the destination directory exists before writing
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 6. Write the raw waveform array to the specified output WAV file
    # Uses the model's native sampling rate configuration (typically 16000Hz or 22050Hz)
    sf.write(
        output_path,
        waveform,
        model.config.sampling_rate
    )

    return output_path
