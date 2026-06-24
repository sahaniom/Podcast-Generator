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
    System[0.0 AI Multilingual Podcast Generator]
    Summary[Generated Summary Audio]
    Output[Generated Podcast Audio]

    User -->|Enter URL & Language| System
    YouTube -->|Transcript Data| System
    System -->|Summary Audio| Summary
    System -->|Podcast Audio| Output
```

---

# ✅ Level 1 DFD

Breaks the system into major modules.

```mermaid
flowchart TD

    User[User]

    A[1.0 Transcript Extraction]
    B[2.0 Sport Detection & Structured Extraction]
    C[3.0 Summary Generation]
    D[4.0 Podcast Script Generation]
    E[5.0 Podcast Translation Engine]
    F[6.0 Dialogue-aware TTS]
    G[7.0 Podcast Audio Mixer]
    H[8.0 Summary Translation and TTS]
    I[9.0 Final Podcast Output]
    J[9.1 Summary Audio Output]

    User -->|YouTube URL + Language| A

    A -->|Transcript| B

    B -->|Transcript + Sport Context| C

    B -->|Structured Sports Data| D

    D -->|English Podcast Script| E

    E -->|Translated Dialogue Script| F

    F -->|Dialogue Audio| G
    G -->|Mixed Podcast Body| I
    C -->|Summary Text| H
    H -->|Translated Summary Audio| J
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
    M[0.0 main.py Orchestrator]

    %% TRANSCRIPT LAYER
    T1[1.1 Transcript Extractor]
    T2[1.2 Video ID Extractor]

    %% LLM LAYER
    S1[2.1 Sport Detector]
    S3[3.1 Summary Generator]
    S2[2.2 Structured Match Extractor]

    %% GENERATION
    G1[4.1 Podcast Script Generator]

    %% TRANSLATION
    TR1[5.1 Dialogue Parser]
    TR2[5.2 Podcast IndicTrans2 Translator]
    TR3[8.1 Summary Translator]

    %% TTS
    TT1[6.1 Dialogue TTS Engine]
    TT2[6.2 MMS-TTS Models]
    TT3[6.3 Chunk Audio Generator]
    TT4[6.4 Audio Stitcher]
    TT5[8.2 Summary TTS Engine]

    %% AUDIO PROCESSING
    A1[7.1 Podcast Mixer]
    A2[7.2 Background Music]
    A3[7.3 Intro/Outro Audio]
    A4[8.1 Summary Audio Output]

    %% OUTPUT
    O1[9.1 Generated Podcast WAV]
    O2[9.2 Download & Playback]

    %% FLOW
    U --> UI

    UI --> M

    M --> T2
    T2 --> T1

    T1 --> S1
    S1 --> S3
    S1 --> S2

    S2 --> G1

    G1 --> TR1
    TR1 --> TR2

    TR2 --> TT1

    S3 --> TR3
    TR3 --> TT5

    TT1 --> TT2
    TT2 --> TT3
    TT3 --> TT4

    TT4 --> A4
    TT5 --> A4

    TT4 --> A1

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
    M[0.0 Pipeline Orchestrator]

    %% STORAGE
    SCRIPTS[(4.0 Scripts Cache)]
    SUMMARY[(3.0 Summary Cache)]
    AUDIO[(6.0 Audio Cache)]
    OUTPUTS[(9.0 Podcast Outputs)]

    %% PROCESSING
    T[1.0 Transcript Extraction]
    LLM[2.0 LLM Processing]
    SUM[3.0 Summary Generation]
    GEN[4.0 Podcast Script Generation]
    TRANS[5.0 Translation Engine]
    TTS[6.0 TTS Synthesis]
    MIX[7.0 Podcast Audio Mixing]
    SUMA[8.0 Summary Audio Synthesis]

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
    SUMMARY --> SUMA

    SUMA --> OUTPUTS
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
        A[0.0 Streamlit UI]
    end

    subgraph Core Pipeline
        B[0.0 main.py]
    end

    subgraph NLP Layer
        C[1.0 Transcript Extraction]
        D[2.0 Sport Detection]
        E[2.1 Structured Extraction]
        F[3.0 Summary Generator]
        G[4.0 Podcast Script Generator]
        H[5.0 Translation Engine]
    end

    subgraph Speech Layer
        I[6.0 Dialogue TTS]
        J[6.1 MMS-TTS Models]
    end

    subgraph Audio Layer
        K[7.0 Podcast Mixer]
        L[8.0 Summary Audio Output]
    end

    subgraph Storage
        M[(4.0 Scripts)]
        N[(3.0 Summaries)]
        O[(6.0 Audio)]
        P[(9.0 Outputs)]
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

# ✅ Use-Case Diagram

This diagram shows the main user interactions with the system.

```mermaid
flowchart LR

    User([User])
    System[[AI Multilingual Podcast Generator]]

    UC1((Enter YouTube URL))
    UC2((Select Language))
    UC3((Generate Summary Audio))
    UC4((Generate Podcast Audio))
    UC5((Download Summary))
    UC6((Play Summary))
    UC7((Play Podcast))
    UC8((Download Podcast))

    User --> UC1
    User --> UC2
    User --> UC3
    User --> UC4
    UC5 --> User
    UC6 --> User
    UC7 --> User
    UC8 --> User

    UC1 --> System
    UC2 --> System
    UC3 --> System
    UC4 --> System
    System --> UC5
    System --> UC6
    System --> UC7
    System --> UC8
```

# ✅ Class Diagram

This class diagram shows the primary modules and their relationships.

```mermaid
classDiagram
    class StreamlitUI {
        +generate_summary_button()
        +generate_podcast_button()
    }
    class Orchestrator {
        +main(url, lang)
        +generate_summary_only(url, lang)
    }
    class TranscriptExtractor
    class SportDetector
    class SummaryGenerator
    class PodcastScriptGenerator
    class Translator
    class DialogueTTS
    class MMSTTS
    class PodcastMixer

    StreamlitUI --> Orchestrator
    Orchestrator --> TranscriptExtractor
    TranscriptExtractor --> SportDetector
    SportDetector --> SummaryGenerator
    SportDetector --> PodcastScriptGenerator
    PodcastScriptGenerator --> Translator
    Translator --> DialogueTTS
    Translator --> MMSTTS
    DialogueTTS --> PodcastMixer
    MMSTTS --> PodcastMixer
```

---

# ✅ Sequence Diagrams

Two primary flows are shown: Summary generation and Podcast generation.

## Generate Summary (user flow)

```mermaid
sequenceDiagram
    participant User
    participant UI as Streamlit UI
    participant Orch as main.py Orchestrator
    participant TE as TranscriptExtractor
    participant SD as SportDetector
    participant SG as SummaryGenerator
    participant TR as Translator
    participant TTS as MMSTTS
    participant Storage as Audio Cache

    User->>UI: Click "Generate Summary"
    UI->>Orch: generate_summary_only(url, lang)
    Orch->>TE: get_transcript(url)
    TE->>SD: detect_sport(transcript)
    SD->>SG: generate_summary(transcript, sport)
    SG->>TR: translate(summary, target_lang) (if needed)
    TR->>TTS: synthesize(summary_translated)
    TTS->>Storage: save summary_{lang}.wav
    Storage-->>UI: return summary_audio_path
    UI-->>User: play/download summary WAV
```

## Generate Podcast (user flow)

```mermaid
sequenceDiagram
    participant User
    participant UI as Streamlit UI
    participant Orch as main.py Orchestrator
    participant TE as TranscriptExtractor
    participant SD as SportDetector
    participant PS as PodcastScriptGenerator
    participant TR as Translator
    participant DTTS as DialogueTTS
    participant Mixer as PodcastMixer
    participant Outputs as Outputs

    User->>UI: Click "Generate Podcast"
    UI->>Orch: main(url, lang)
    Orch->>TE: get_transcript(url)
    TE->>SD: detect_sport(transcript)
    SD->>PS: generate_script(structured_data)
    PS->>TR: translate(script, target_lang)
    TR->>DTTS: synthesize_dialogue(translated_script)
    DTTS->>Mixer: provide voice tracks
    Mixer->>Outputs: mix intro/bg/outro -> final WAV
    Outputs-->>UI: return podcast path
    UI-->>User: play/download podcast WAV
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
