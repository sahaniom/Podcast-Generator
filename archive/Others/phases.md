Good — now you’re doing it the right way: **plan first, then build**.
Since your scope is now **multi-sport + multi-language + podcast**, we need a clean, modular pipeline.

I’ll give you a **practical, implementation-ready roadmap** (not just theory).

---

# 🧠 FINAL SYSTEM ARCHITECTURE (What you are building)

```text
YouTube → Transcript → LLM Structuring → Rules → Podcast Script → TTS → UI
```

---

# 🚀 STEP-BY-STEP IMPLEMENTATION PLAN

We’ll divide this into **6 phases** so you don’t get overwhelmed.

---

# 🧩 PHASE 1 — Your Current Code (✅ DONE)

✔ Transcript extraction (captions + Whisper fallback)
✔ English normalization via Whisper (`task="translate"`)

👉 Output:

```text
Raw English Transcript
```

---

# 🔥 PHASE 2 — LLM STRUCTURED EXTRACTION (MOST IMPORTANT)

### 🎯 Goal:

Convert messy transcript → **structured JSON**

---

## What this step should do:

* Detect sport (cricket / football / etc.)
* Extract teams
* Extract key events
* Extract score summary
* Extract result

---

## Output format (fix this early):

```json
{
  "sport": "cricket",
  "teams": ["India", "Pakistan"],
  "events": [
    {"type": "WICKET", "description": "..."},
    {"type": "SIX", "description": "..."}
  ],
  "score_summary": "...",
  "result": "India won..."
}
```

---

## ⚠️ Critical Design Rule:

👉 This JSON becomes your **single source of truth**

---

## Implementation tasks:

* [ ] Setup Ollama
* [ ] Write extraction prompt
* [ ] Handle long transcripts (chunking)
* [ ] Merge chunk outputs

---

# 🧩 PHASE 3 — RULE-BASED POST PROCESSING

Now rules become **simple and powerful**

---

## What rules should do:

* Normalize event types (SIX, GOAL, THREE_POINTER)
* Clean duplicate events
* Standardize scores

---

## Example:

```python
if data["sport"] == "cricket":
    normalize_cricket_events(data)
elif data["sport"] == "football":
    normalize_football_events(data)
```

---

## Tasks:

* [ ] Create sport-wise rule modules
* [ ] Keep rules minimal (don’t over-engineer)

---

# 🧠 PHASE 4 — PODCAST SCRIPT GENERATION (LLM)

### 🎯 Goal:

Convert structured data → **human-like narration**

---

## Input:

```json
structured_data
```

## Output:

```text
"Welcome to the thrilling final between India and Pakistan..."
```

---

## Key Features:

* Storytelling
* Emotion
* Flow

---

## Tasks:

* [ ] Create prompt for storytelling
* [ ] Add tone control (excited, neutral, dramatic)
* [ ] Keep it deterministic (temperature=0.3–0.5)

---

# 🌍 PHASE 5 — MULTI-LANGUAGE SUPPORT

### 🎯 Goal:

Generate podcast in **user-selected language**

---

## IMPORTANT DESIGN:

👉 Do NOT translate transcript
👉 Only translate final script

---

## Flow:

```text
Structured Data → LLM → Hindi Script
```

---

## Example prompt:

```text
Generate a Hindi podcast script from this match data.
Keep player names unchanged.
Translate narration only.
```

---

## Tasks:

* [ ] Add language parameter
* [ ] Test Hindi output first
* [ ] Then expand to Tamil, Telugu, etc.

---

# 🔊 PHASE 6 — TEXT TO SPEECH (TTS)

### 🎯 Goal:

Convert script → audio

---

## Options:

### Local:

* Coqui TTS
* Piper

### Online:

* Google TTS (easier, but needs internet)

---

## Tasks:

* [ ] Choose TTS engine
* [ ] Map language → voice
* [ ] Generate `.wav` or `.mp3`

---

# 🖥️ PHASE 7 — OUTPUT (UI / CLI)

### Output should include:

* 📄 Text (podcast script)
* 🔊 Audio file

---

## Tasks:

* [ ] Save script file
* [ ] Save audio file
* [ ] Optional: simple web UI later

---

# ⚙️ OPTIONAL PHASE 8 — LANGCHAIN (LATER)

Use LangChain only when:

* multiple chains grow
* prompts become complex
* you want modular pipelines

👉 Not needed in initial version

---

# 🧠 FINAL PIPELINE (CODE LEVEL)

```python
def pipeline(url, language="en"):
    transcript = get_transcript(url)

    structured = llm_extract(transcript)        # Phase 2
    structured = apply_rules(structured)        # Phase 3

    script = llm_generate(structured, language) # Phase 4 + 5
    audio = tts_generate(script, language)      # Phase 6

    return script, audio
```

---

# ⚠️ COMMON MISTAKES TO AVOID

### ❌ Don’t:

* Write heavy rules for raw text
* Translate early
* Skip structured step

### ✅ Do:

* Convert text → JSON early
* Keep rules minimal
* Let LLM handle language

---

# 🎯 DEVELOPMENT ORDER (VERY IMPORTANT)

Follow this order strictly:

1. ✅ Transcript (done)
2. 🔥 LLM → structured JSON (**next step**)
3. Rules on JSON
4. Podcast script (English)
5. Add Hindi
6. Add TTS
7. Add more sports

---

# 🚀 What Next?

👉 Next step is **PHASE 2 (most critical)**

If you want, I’ll help you:

* Write **perfect LLM extraction prompt**
* Implement **Ollama integration**
* Handle **chunking + merging correctly**

Just say: *“let’s implement phase 2”* 👍
