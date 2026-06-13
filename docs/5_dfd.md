# 🎯 DFDs (Data Flow Diagrams) for AI Multilingual Podcast Generator

Below are:

* Level 0 DFD
* Level 1 DFD
* Level 2 DFD

using:

# ✅ Mermaid diagrams

You can directly use these in:

* README
* documentation
* reports
* presentations

---

# ✅ Level 0 DFD (Context Diagram)

Shows the system as a single black-box process.

```mermaid
flowchart TD

    User[User]
    YouTube[YouTube Video]
    System[AI Multilingual Podcast Generator]
    Output[Generated Podcast Audio with Spoken Summary]

    User -->|Enter URL & Language| System
    YouTube -->|Transcript Data| System
    System -->|Summary Audio + Podcast Audio + Script| Output
```

---

# ✅ Level 1 DFD

Breaks the system into major modules.

```mermaid
flowchart TD

    User[User]

    A[Transcript Extraction]
    B[Sport Detection & Structured Extraction]
    C[Summary Generation]
    D[Podcast Script Generation]
    E[Translation Engine]
    F[Dialogue-aware TTS]
    G[Podcast Audio Mixer]
    H[Summary TTS and Final Merge]
    I[Final Podcast Output]

    User -->|YouTube URL + Language| A

    A -->|Transcript| B

    B -->|Transcript + Sport Context| C

    B -->|Structured Sports Data| D

    C -->|Summary Text| E
    D -->|English Podcast Script| E

    E -->|Translated Summary + Dialogue Script| F

    F -->|Summary Audio + Dialogue Audio| G
    G -->|Mixed Podcast Body| H
    H -->|Final Podcast WAV| I
```

---

# ✅ Level 2 DFD (Detailed Internal Workflow)

This shows detailed internal architecture and module interaction.

```mermaid
flowchart TD

    %% USER INPUT
    U[User]
    UI[Streamlit UI]

    %% MAIN ORCHESTRATOR
    M[main.py Orchestrator]

    %% TRANSCRIPT LAYER
    T1[Transcript Extractor]
    T2[Video ID Extractor]

    %% LLM LAYER
    S1[Sport Detector]
    S3[Summary Generator]
    S2[Structured Match Extractor]

    %% GENERATION
    G1[Podcast Script Generator]

    %% TRANSLATION
    TR1[Dialogue Parser]
    TR2[IndicTrans2 Translator]

    %% TTS
    TT1[Dialogue TTS Engine]
    TT2[MMS-TTS Models]
    TT3[Chunk Audio Generator]
    TT4[Audio Stitcher]

    %% AUDIO PROCESSING
    A1[Podcast Mixer]
    A2[Background Music]
    A3[Intro/Outro Audio]
    A4[Summary + Podcast Merger]

    %% OUTPUT
    O1[Generated Podcast WAV]
    O2[Download & Playback]

    %% FLOW
    U --> UI

    UI --> M

    M --> T2
    T2 --> T1

    T1 --> S1
    S1 --> S3
    S1 --> S2

    S3 --> TR2
    S2 --> G1

    G1 --> TR1
    TR1 --> TR2

    TR2 --> TT1

    TT1 --> TT2
    TT2 --> TT3
    TT3 --> TT4

    TT4 --> A1
    TT4 --> A4

    A2 --> A1
    A3 --> A1

    A1 --> A4

    A4 --> O1

    O1 --> O2
```

---

# ✅ Level 2 DFD (With Storage/Caching)

This version includes:

* scripts cache
* summary cache
* audio cache
* outputs

```mermaid
flowchart TD

    %% USER
    U[User]

    %% UI
    UI[Streamlit UI]

    %% MAIN
    M[Pipeline Orchestrator]

    %% STORAGE
    SCRIPTS[(Scripts Cache)]
    SUMMARY[(Summary Cache)]
    AUDIO[(Audio Cache)]
    OUTPUTS[(Podcast Outputs)]

    %% PROCESSING
    T[Transcript Extraction]
    LLM[LLM Processing]
    SUM[Summary Generation]
    GEN[Podcast Script Generation]
    TRANS[Translation Engine]
    TTS[TTS Synthesis]
    MIX[Podcast Audio Mixing]
    MERGE[Final Summary and Podcast Merge]

    %% FLOW
    U --> UI

    UI --> M

    M --> T

    T --> LLM

    LLM --> SUM
    LLM --> GEN

    SUM --> SUMMARY
    GEN --> SCRIPTS

    SUMMARY --> TRANS
    SCRIPTS --> TRANS

    TRANS --> AUDIO

    AUDIO --> TTS

    TTS --> MIX
    TTS --> MERGE
    MIX --> MERGE

    MERGE --> OUTPUTS

    OUTPUTS --> UI
```

---

# ✅ Component Architecture Diagram

This is useful for:

* GitHub README
* presentations
* software architecture explanation

```mermaid
graph TD

    subgraph Frontend
        A[Streamlit UI]
    end

    subgraph Core Pipeline
        B[main.py]
    end

    subgraph NLP Layer
        C[Transcript Extraction]
        D[Sport Detection]
        E[Structured Extraction]
        F[Summary Generator]
        G[Podcast Script Generator]
        H[Translation Engine]
    end

    subgraph Speech Layer
        I[Dialogue TTS]
        J[MMS-TTS Models]
    end

    subgraph Audio Layer
        K[Podcast Mixer]
        L[Summary and Podcast Merger]
    end

    subgraph Storage
        M[(Scripts)]
        N[(Summaries)]
        O[(Audio)]
        P[(Outputs)]
    end

    A --> B

    B --> C
    C --> D
    D --> E
    D --> F
    E --> G
    F --> H
    G --> H

    H --> I
    I --> J

    J --> K
    J --> L
    K --> L

    F --> N
    G --> M
    I --> O
    L --> P
```

---

# ✅ Best Recommendation

For:

## 📄 README

use:

* Component Architecture Diagram
* Level 1 DFD

For:

## 📄 Report / Documentation

use:

* Level 0
* Level 1
* Level 2

For:

## 📄 PPT Presentation

use:

* Level 0
* Component Architecture

Those are the cleanest visually.
