# 🎙️ AI Multilingual Podcast Generator — Overall Architecture

Your project evolved into a full AI-driven multimedia pipeline.

At a high level:

```text id="h9x2vk"
YouTube Video
    ↓
Transcript Extraction
    ↓
Structured Match Understanding
    ↓
LLM Podcast Script Generation
    ↓
Multi-Speaker Dialogue Formatting
    ↓
Multilingual Translation
    ↓
Dialogue-Aware TTS
    ↓
Audio Stitching
    ↓
Podcast Music Mixing
    ↓
Final Podcast Output
    ↓
Streamlit UI
```

---

# 🧠 1. Input Layer

## Purpose

Accept a YouTube video URL from:

* terminal (`main.py`)
* Streamlit UI (`app.py`)

---

## Components

### 📄 `app.py`

Handles:

* YouTube URL input
* language selection
* audio playback
* downloads

Built using:
Streamlit

---

### 📄 `main.py`

Acts as:

# 🎯 central orchestration controller

Responsibilities:

* cache checking
* pipeline execution
* coordination between modules

---

# 🎥 2. Transcript Ingestion Layer

## Purpose

Convert YouTube video into raw textual transcript.

---

## Components

### 📄 `transcript/transcript_extractor.py`

Responsibilities:

* extract video ID
* fetch transcript
* fallback transcription if subtitles unavailable

Pipeline:

```text id="m8v4tw"
YouTube URL
    ↓
Transcript API / Whisper fallback
    ↓
Raw Transcript
```

---

# 🏅 3. Sports Understanding Layer

## Purpose

Understand:

* which sport
* what happened
* important match events

---

## Components

### 📄 `llm/sport_detector.py`

Uses LLM classification to detect:

* cricket
* football
* tennis
  etc.

---

### 📄 `llm/extractor.py`

Transforms:

```text id="g5r1zx"
unstructured commentary
```

into:

```text id="t2p8wy"
structured match knowledge
```

like:

* wickets
* boundaries
* turning points
* players
* match result

---

# ✍️ 4. Podcast Script Generation Layer

## Purpose

Transform structured sports data into:

# 🎙️ conversational podcast dialogue

---

## Components

### 📄 `generation/podcast_script_generator.py`

Uses LLM prompting to generate:

* HOST dialogue
* GUEST dialogue
* NARRATOR transitions

Output example:

```text id="p6x2km"
[HOST]
Welcome back...

[GUEST]
What a game that was...
```

This layer creates:

# 🧠 storytelling intelligence

---

# 🌍 5. Translation Layer

## Purpose

Convert English dialogue into multilingual podcast scripts.

---

## Components

### 📄 `translation/translator.py`

Responsibilities:

* dialogue parsing
* block-by-block translation
* speaker preservation

Critical improvement:

```text id="s7w4ny"
dialogue-aware translation
```

instead of:

```text id="w1q8tv"
whole-script translation
```

which massively improved quality.

---

### 📄 `translation/indictrans2_translator.py`

Uses:
AI4Bharat IndicTrans2

For:

```text id="d4m6kp"
English → Indic language translation
```

Supported languages:

* Hindi
* Bengali
* Tamil
* Telugu
* Marathi
* Gujarati
* Kannada
* Malayalam
* Punjabi

---

# 🔊 6. Text-to-Speech Layer

## Purpose

Convert translated dialogue into natural speech audio.

---

## Components

### 📄 `tts/mms_tts.py`

Core multilingual TTS engine.

Uses:
Meta MMS TTS models.

Responsibilities:

* language model loading
* chunk splitting
* sentence-level synthesis
* audio merging
* model caching

---

## Important Feature

### ✅ Chunked TTS

Instead of:

```text id="h4v7zp"
whole script → one synthesis
```

you implemented:

```text id="x2n8tr"
sentence chunking
    ↓
individual WAV generation
    ↓
audio stitching
```

which improved:

* stability
* pacing
* memory usage

---

# 👥 7. Dialogue-Aware Audio Layer

## Purpose

Handle:

* speaker parsing
* multi-speaker orchestration
* future voice styling

---

## Components

### 📄 `tts/dialogue_tts.py`

Responsibilities:

* parse `[HOST]`
* parse `[GUEST]`
* parse `[NARRATOR]`
* remove tags before speech
* generate sequential dialogue audio

This created:

# 🧠 speaker-aware synthesis architecture

---

# 🎧 8. Audio Post-Processing Layer

## Purpose

Transform plain narration into:

# 🎙️ real podcast experience

---

## Components

### 📄 `audio_processing/podcast_mixer.py`

Responsibilities:

* intro music
* background music
* outro music
* fades
* volume balancing
* final export

Built using:
Pydub

---

# 🗂️ 9. File Management & Caching Layer

## Purpose

Avoid expensive recomputation.

---

## Features

Your pipeline intelligently caches:

* English scripts
* translated scripts
* synthesized audio
* final podcast outputs

Example:

```text id="m7r5vq"
scripts/<video_id>/
audio/<video_id>/
outputs/<video_id>/
```

This significantly improves:

* performance
* developer workflow
* scalability

---

# ⚙️ 10. Configuration Layer

## Components

### 📄 `config.py`

Centralizes:

* supported languages
* music paths
* durations
* audio configs

This improved:

# 🧠 maintainability

---

# 🖥️ 11. Frontend Layer

## Components

### 📄 `app.py`

Provides:

* web interface
* audio playback
* download support

Users can:

```text id="b6v1qw"
Paste URL
    ↓
Select language
    ↓
Generate podcast
    ↓
Listen/download
```

---

# 🏗️ Final System Architecture

```text id="k8m3tr"
                ┌─────────────────────┐
                │   Streamlit UI      │
                └─────────┬───────────┘
                          ↓
                ┌─────────────────────┐
                │      main.py        │
                │ Pipeline Controller │
                └─────────┬───────────┘
                          ↓
        ┌─────────────────────────────────┐
        │ Transcript Extraction Layer     │
        └─────────────────────────────────┘
                          ↓
        ┌─────────────────────────────────┐
        │ Sport Detection + Extraction    │
        └─────────────────────────────────┘
                          ↓
        ┌─────────────────────────────────┐
        │ Podcast Script Generation       │
        └─────────────────────────────────┘
                          ↓
        ┌─────────────────────────────────┐
        │ Dialogue-Aware Translation      │
        └─────────────────────────────────┘
                          ↓
        ┌─────────────────────────────────┐
        │ Dialogue-Aware TTS              │
        └─────────────────────────────────┘
                          ↓
        ┌─────────────────────────────────┐
        │ Audio Mixing & Enhancement      │
        └─────────────────────────────────┘
                          ↓
                ┌─────────────────────┐
                │ Final Podcast WAV   │
                └─────────────────────┘
```

---

# 🚀 Biggest Technical Strengths

Your project demonstrates:

* modular AI system design
* multilingual NLP
* speech synthesis orchestration
* LLM pipeline engineering
* audio processing
* caching architecture
* UI integration

This is far beyond a basic “LLM app.”
