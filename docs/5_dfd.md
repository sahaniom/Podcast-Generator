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
    Output[Generated Podcast Audio]

    User -->|Enter URL & Language| System
    YouTube -->|Transcript Data| System
    System -->|Podcast Audio + Script| Output
```

---

# ✅ Level 1 DFD

Breaks the system into major modules.

```mermaid
flowchart TD

    User[User]

    A[Transcript Extraction]
    B[Sport Detection & Structured Extraction]
    C[Podcast Script Generation]
    D[Translation Engine]
    E[Dialogue-aware TTS]
    F[Podcast Audio Mixer]
    G[Final Podcast Output]

    User -->|YouTube URL + Language| A

    A -->|Transcript| B

    B -->|Structured Sports Data| C

    C -->|English Podcast Script| D

    D -->|Translated Dialogue Script| E

    E -->|Speech Audio| F

    F -->|Mixed Podcast Audio| G
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

    %% OUTPUT
    O1[Generated Podcast WAV]
    O2[Download & Playback]

    %% FLOW
    U --> UI

    UI --> M

    M --> T2
    T2 --> T1

    T1 --> S1
    S1 --> S2

    S2 --> G1

    G1 --> TR1
    TR1 --> TR2

    TR2 --> TT1

    TT1 --> TT2
    TT2 --> TT3
    TT3 --> TT4

    TT4 --> A1

    A2 --> A1
    A3 --> A1

    A1 --> O1

    O1 --> O2
```

---

# ✅ Level 2 DFD (With Storage/Caching)

This version includes:

* scripts cache
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
    AUDIO[(Audio Cache)]
    OUTPUTS[(Podcast Outputs)]

    %% PROCESSING
    T[Transcript Extraction]
    LLM[LLM Processing]
    GEN[Podcast Script Generation]
    TRANS[Translation Engine]
    TTS[TTS Synthesis]
    MIX[Podcast Audio Mixing]

    %% FLOW
    U --> UI

    UI --> M

    M --> T

    T --> LLM

    LLM --> GEN

    GEN --> SCRIPTS

    SCRIPTS --> TRANS

    TRANS --> AUDIO

    AUDIO --> TTS

    TTS --> MIX

    MIX --> OUTPUTS

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
        F[Podcast Script Generator]
        G[Translation Engine]
    end

    subgraph Speech Layer
        H[Dialogue TTS]
        I[MMS-TTS Models]
    end

    subgraph Audio Layer
        J[Podcast Mixer]
        K[Music Processing]
    end

    subgraph Storage
        L[(Scripts)]
        M[(Audio)]
        N[(Outputs)]
    end

    A --> B

    B --> C
    C --> D
    D --> E
    E --> F
    F --> G

    G --> H
    H --> I

    I --> J
    J --> K

    F --> L
    H --> M
    J --> N
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
