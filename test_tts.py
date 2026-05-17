"""
MMS Text-to-Speech (TTS) Testing Script
=======================================
This script is used to verify and test the functionality of the local MMS TTS generation module.
It feeds a sample Hindi text to the generator, loads the Hindi model dynamically, and outputs 
a high-quality synthesized speech WAV file.

Prerequisites:
--------------
Make sure the required dependencies are installed:
- PyTorch (torch)
- Transformers (transformers)
- SoundFile (soundfile)

Usage:
------
Run this script directly from the project root:
    python test_tts.py
"""

from tts.mms_tts import generate_tts

# 1. Define sample text in the target language (Hindi in this case)
sample_text = """
नमस्कार दोस्तों।
आज हम आर्टिफिशियल इंटेलिजेंस और पॉडकास्ट जनरेशन के बारे में बात करेंगे।
"""

# 2. Define the output file path for the generated WAV audio
output_file = "audio/test_hindi.wav"

# 3. Call the TTS generator function
# This will:
# - Dynamically load the 'facebook/mms-tts-hin' model and tokenizer.
# - Convert Hindi Devanagari text to PyTorch tensor tokens.
# - Synthesize the waveform using the VITS generative network.
# - Write the waveform as a WAV file to the 'audio/' directory.
generate_tts(
    text=sample_text,
    language="Hindi",
    output_path=output_file
)

# 4. Print confirmation message upon successful completion
print(f"Audio generated successfully: {output_file}")