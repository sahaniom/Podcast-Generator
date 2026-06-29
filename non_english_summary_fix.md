# Non-English Summary Fix

## Problem
The summary generation path was producing translated text for Bengali and other Indic languages, but the text was not always in the native script expected by the MMS TTS models.

For `WwSyB8yo2XI`, the Bengali summary cache contained mixed Devanagari/native-script output. MMS TTS for Bengali could not tokenize that text correctly, so every sentence chunk became `torch.Size([1, 0])` and the summary audio path failed.

The podcast branch had the same underlying issue for non-English output, because it also depended on the same translated text before TTS.

## Changes Made
### 1. Normalized translated text before TTS
Updated `translation/indictrans2_translator.py` to:
- strip stray markdown artifacts like `#` and `*`
- apply a best-effort native-script normalization for Indic outputs
- keep Hindi and Marathi unchanged

This made the translated text usable by the MMS tokenizer.

### 2. Normalized cached and newly generated scripts in orchestration
Updated `main.py` to:
- normalize every loaded or newly translated summary/podcast script before audio synthesis
- rewrite non-English cached script files after normalization
- self-heal stale cached summary/podcast text on reruns

### 3. Validated the fix
Re-ran the Bengali summary and podcast paths for `WwSyB8yo2XI` and confirmed:
- Bengali summary text now tokenizes with non-zero input length
- Bengali summary audio is generated successfully
- Bengali podcast audio also completes successfully

## Result
Non-English summary generation now works reliably for the affected Indic languages instead of failing at the TTS step.
