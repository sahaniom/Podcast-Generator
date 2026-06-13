# 🎙️ Detailed Architecture — AI Multilingual Podcast Generator

```text id="p8m4tx"
┌──────────────────────────────────────────────────────────────────────────┐
│                         STREAMLIT WEB UI                                │
│                              app.py                                     │
│--------------------------------------------------------------------------│
│ • Accepts YouTube URL                                                    │
│ • Language Selection                                                     │
│ • Starts Podcast Generation Pipeline                                     │
│ • Audio Playback                                                         │
│ • Podcast Download                                                       │
└───────────────────────────────┬──────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                     PIPELINE ORCHESTRATOR                               │
│                              main.py                                    │
│--------------------------------------------------------------------------│
│ Responsibilities:                                                        │
│ • Input validation                                                       │
│ • Reverse caching logic                                                  │
│ • Coordinates all AI modules                                             │
│ • Handles podcast + summary generation flow                              │
│ • Executes translation + TTS + mixing                                    │
│ • Merges spoken summary with the final mixed podcast                     │
│ • Returns final podcast path                                             │
└───────────────────────────────┬──────────────────────────────────────────┘
                                │
                ┌───────────────┴────────────────┐
                ▼                                ▼

┌──────────────────────────────┐    ┌──────────────────────────────┐
│      FILE CACHE LAYER        │    │        CONFIGURATION         │
│------------------------------------------------------------------│
│ scripts/<video_id>/          │    │ config.py                    │
│ audio/<video_id>/            │    │------------------------------│
│ outputs/<video_id>/          │    │ • Supported languages        │
│                              │    │ • Music paths                │
│ • Caches podcast scripts     │    │ • Audio configs              │
│ • Caches summary scripts     │    │ • Constants                  │
│ • Caches summary audio       │    │                              │
│ • Prevents recomputation     │    │ main.py                      │
│ • Stores intermediate files  │    │ • Language-specific          │
│                              │    │   spoken summary phrases     │
└──────────────────────────────┘    └──────────────────────────────┘


══════════════════════════════════════════════════════════════════════════════
1️⃣ TRANSCRIPT INGESTION LAYER
══════════════════════════════════════════════════════════════════════════════

                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                    transcript/transcript_extractor.py                   │
│--------------------------------------------------------------------------│
│ INPUT: YouTube URL                                                       │
│                                                                          │
│ Responsibilities:                                                        │
│ • Extract YouTube Video ID                                               │
│ • Fetch transcript via transcript APIs                                   │
│ • Fallback transcription if subtitles unavailable                        │
│                                                                          │
│ OUTPUT: Raw transcript text                                              │
└──────────────────────────────────────────────────────────────────────────┘


══════════════════════════════════════════════════════════════════════════════
2️⃣ SPORTS UNDERSTANDING LAYER
══════════════════════════════════════════════════════════════════════════════

                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                      llm/sport_detector.py                              │
│--------------------------------------------------------------------------│
│ INPUT: Transcript                                                        │
│                                                                          │
│ Uses LLM to classify:                                                    │
│ • Cricket                                                                │
│ • Football                                                               │
│ • Tennis                                                                 │
│ etc.                                                                     │
│                                                                          │
│ OUTPUT: Detected sport                                                   │
└──────────────────────────────────────────────────────────────────────────┘


                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                         llm/extractor.py                                │
│--------------------------------------------------------------------------│
│ INPUT: Transcript + Sport Context                                        │
│                                                                          │
│ Responsibilities:                                                        │
│ • Extract wickets                                                        │
│ • Extract boundaries                                                     │
│ • Detect turning points                                                  │
│ • Extract players                                                        │
│ • Extract scores                                                         │
│ • Extract final result                                                   │
│                                                                          │
│ Uses structured LLM prompting                                            │
│                                                                          │
│ OUTPUT: Structured sports JSON                                           │
└──────────────────────────────────────────────────────────────────────────┘


══════════════════════════════════════════════════════════════════════════════
3️⃣ SUMMARY GENERATION LAYER
══════════════════════════════════════════════════════════════════════════════

                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                    llm/summary_generator.py                             │
│--------------------------------------------------------------------------│
│ INPUT: Transcript + Sport Context                                        │
│                                                                          │
│ Responsibilities:                                                        │
│ • Generate a short match recap using a dedicated LLM prompt              │
│ • Truncate very long transcripts before summary generation               │
│ • Convert numeric digits into spoken English words                       │
│ • Return plain text suitable for translation and TTS                     │
│                                                                          │
│ OUTPUT: English summary text                                             │
└──────────────────────────────────────────────────────────────────────────┘


══════════════════════════════════════════════════════════════════════════════
4️⃣ PODCAST SCRIPT GENERATION LAYER
══════════════════════════════════════════════════════════════════════════════

                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│             generation/podcast_script_generator.py                      │
│--------------------------------------------------------------------------│
│ INPUT: Structured sports data                                            │
│                                                                          │
│ Responsibilities:                                                        │
│ • Generate podcast storytelling                                          │
│ • Create conversational dialogue                                         │
│ • Add excitement/emotion                                                 │
│ • Create HOST/GUEST/NARRATOR interactions                                │
│                                                                          │
│ Uses LLM prompting                                                       │
│                                                                          │
│ OUTPUT:                                                                  │
│                                                                          │
│ [HOST]                                                                   │
│ Welcome back...                                                          │
│                                                                          │
│ [GUEST]                                                                  │
│ What a match...                                                          │
│                                                                          │
│ [NARRATOR]                                                               │
│ The momentum shifted...                                                  │
└──────────────────────────────────────────────────────────────────────────┘


══════════════════════════════════════════════════════════════════════════════
5️⃣ MULTILINGUAL TRANSLATION LAYER
══════════════════════════════════════════════════════════════════════════════

                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                    translation/translator.py                            │
│--------------------------------------------------------------------------│
│ INPUT: English podcast dialogue                                          │
│                                                                          │
│ Responsibilities:                                                        │
│ • Parse speaker dialogue blocks                                          │
│ • Translate each dialogue separately                                     │
│ • Preserve speaker structure                                             │
│                                                                          │
│ CRITICAL DESIGN:                                                         │
│ • Block-by-block translation                                             │
│   instead of whole-script translation                                    │
│                                                                          │
│ OUTPUT: Multilingual dialogue script                                     │
└──────────────────────────────────────────────────────────────────────────┘


                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│            translation/indictrans2_translator.py                        │
│--------------------------------------------------------------------------│
│ Uses AI4Bharat IndicTrans2                                               │
│                                                                          │
│ Also handles:                                                            │
│ • summary translation for non-English target languages                   │
│                                                                          │
│ Supported Languages:                                                     │
│ • Hindi                                                                  │
│ • Tamil                                                                  │
│ • Bengali                                                                │
│ • Telugu                                                                 │
│ • Marathi                                                                │
│ • Gujarati                                                               │
│ • Kannada                                                                │
│ • Malayalam                                                              │
│ • Punjabi                                                                │
│ • English                                                                │
│                                                                          │
│ OUTPUT: High-quality Indic translations                                  │
└──────────────────────────────────────────────────────────────────────────┘


══════════════════════════════════════════════════════════════════════════════
6️⃣ DIALOGUE-AWARE TTS LAYER
══════════════════════════════════════════════════════════════════════════════

                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                      tts/dialogue_tts.py                                │
│--------------------------------------------------------------------------│
│ INPUT: Multilingual dialogue script                                      │
│                                                                          │
│ Responsibilities:                                                        │
│ • Parse [HOST]/[GUEST]/[NARRATOR]                                        │
│ • Remove metadata tags before TTS                                        │
│ • Generate speaker-specific chunks                                       │
│ • Apply lightweight voice styling                                        │
│                                                                          │
│ Speaker Simulation:                                                      │
│ • HOST → energetic                                                       │
│ • GUEST → softer                                                         │
│ • NARRATOR → calmer/slower                                               │
│                                                                          │
│ OUTPUT: Speaker-aware dialogue audio                                     │
└──────────────────────────────────────────────────────────────────────────┘


                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                          tts/mms_tts.py                                 │
│--------------------------------------------------------------------------│
│ Uses Meta MMS TTS                                                        │
│                                                                          │
│ Responsibilities:                                                        │
│ • Load multilingual TTS models                                           │
│ • Sentence chunking                                                      │
│ • Chunk-level synthesis                                                  │
│ • Audio stitching                                                        │
│ • Model caching                                                          │
│                                                                          │
│ Supported Models:                                                        │
│ • facebook/mms-tts-eng                                                   │
│ • facebook/mms-tts-hin                                                   │
│ • facebook/mms-tts-tam                                                   │
│ • etc.                                                                   │
│                                                                          │
│ OUTPUT: Natural speech WAV files                                         │
└──────────────────────────────────────────────────────────────────────────┘


══════════════════════════════════════════════════════════════════════════════
7️⃣ AUDIO POST-PROCESSING LAYER
══════════════════════════════════════════════════════════════════════════════

                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│               audio_processing/podcast_mixer.py                         │
│--------------------------------------------------------------------------│
│ INPUT: Dialogue audio                                                    │
│                                                                          │
│ Responsibilities:                                                        │
│ • Add intro music                                                        │
│ • Add background ambience                                                │
│ • Add outro music                                                        │
│ • Fade in/out                                                            │
│ • Volume balancing                                                       │
│ • Create podcast body before summary merge                               │
│                                                                          │
│ Uses Pydub audio processing                                              │
│                                                                          │
│ OUTPUT: Mixed podcast body WAV                                           │
└──────────────────────────────────────────────────────────────────────────┘


                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                    main.py audio merge stage                            │
│--------------------------------------------------------------------------│
│ INPUT: Summary WAV + Mixed podcast body WAV                              │
│                                                                          │
│ Responsibilities:                                                        │
│ • Prefix the spoken summary before the main podcast                      │
│ • Insert a short silent pause between both segments                      │
│ • Export the final combined podcast file                                 │
│                                                                          │
│ OUTPUT: Final cinematic podcast                                          │
└──────────────────────────────────────────────────────────────────────────┘


══════════════════════════════════════════════════════════════════════════════
8️⃣ FINAL OUTPUT LAYER
══════════════════════════════════════════════════════════════════════════════

                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                           OUTPUTS                                       │
│--------------------------------------------------------------------------│
│ scripts/<video_id>/english.txt                                           │
│ scripts/<video_id>/summary_english.txt                                   │
│ scripts/<video_id>/hindi.txt                                             │
│ scripts/<video_id>/summary_hindi.txt                                     │
│                                                                          │
│ audio/<video_id>/hindi.wav                                               │
│ audio/<video_id>/summary_hindi.wav                                       │
│                                                                          │
│ outputs/<video_id>/hindi_podcast.wav                                     │
│                                                                          │
│ Streamlit UI Playback                                                    │
│ Downloadable Podcast                                                     │
└──────────────────────────────────────────────────────────────────────────┘
```
