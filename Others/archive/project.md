# Major Project Progress Report  
## Automated Sports Highlight Extraction and Multilingual Podcast Generation Using Hybrid AI  

**Student Name:** Om Sahani  
**Roll Number:** (Your Roll Number)  
**Organization:** National Informatics Centre (NIC)  
**Duration:** 6 Months  
**Total Sprints:** 5  

---

# Sprint 0 – System Design & Planning (January 2026)

## 1. Overview
Sprint 0 focused on designing the complete system architecture, defining the AI workflow pipeline, selecting appropriate technologies, and preparing the development environment. No core implementation was done in this phase; instead, foundational planning and research were completed.

## 2. Objectives
- Finalize system architecture
- Define AI workflow pipeline
- Design custom highlight scoring algorithm
- Select Speech-to-Text, LLM, and TTS services
- Define evaluation metrics (ROUGE, BERTScore)
- Set up repository structure
- Prepare implementation roadmap

## 3. Completed Work
- Designed high-level architecture (Ingestion Layer, Highlight Engine, AI Layer, Output Layer)
- Defined pipeline: Audio → STT → Segmentation → Scoring → LLM → TTS
- Designed highlight scoring formula
- Finalized technology stack (Python, Google STT, Vertex AI, TTS)
- Designed transcript storage structure
- Prepared sprint backlog for Sprint 1

## 4. Key Achievements
- Completed professional system architecture
- Designed proprietary highlight detection logic
- Established research evaluation framework

## 5. Challenges
- Designing fair scoring weights
- Handling LLM hallucination risk
- Selecting evaluation metrics

## 6. Outcome
Project foundation established and ready for implementation.

---

# Sprint 1 – Core Pipeline Implementation (February 2026)

## 1. Overview
Sprint 1 focused on building the working core pipeline from audio input to highlight generation.

## 2. Objectives
- Integrate Speech-to-Text API
- Implement transcript segmentation
- Develop keyword scoring module
- Implement sentiment analysis
- Combine scoring formula
- Extract top highlight segments

## 3. Completed Work
- Successfully converted audio commentary to timestamped transcript
- Implemented transcript segmentation logic
- Developed keyword-based scoring module
- Integrated sentiment polarity scoring
- Added punctuation-based excitement scoring
- Combined weighted moment_score formula
- Extracted Top 5 highlight segments

## 4. Key Achievements
- Working highlight detection engine
- Custom scoring algorithm operational
- Reduced dependency on LLM for event detection

## 5. Challenges
- Handling noisy transcripts
- Fine-tuning scoring weights
- Managing timestamp alignment

## 6. Outcome
Functional highlight extraction system completed.

---

# Sprint 2 – LLM Integration & Podcast Generation (March 2026)

## 1. Overview
Sprint 2 focused on integrating Generative AI for summary creation and converting summaries into podcast audio.

## 2. Objectives
- Integrate Vertex AI (Gemini)
- Design structured prompt templates
- Implement hallucination control rules
- Integrate Text-to-Speech
- Generate podcast output

## 3. Completed Work
- Connected highlight segments to LLM
- Generated grounded highlight summaries
- Implemented timestamp citation enforcement
- Developed verification layer to prevent hallucinations
- Integrated Google Text-to-Speech
- Generated final podcast audio (.mp3)

## 4. Key Achievements
- Fully automated Audio → Podcast pipeline
- Reduced hallucinated events via verification logic
- Generated natural-sounding podcast narration

## 5. Challenges
- Prompt engineering optimization
- Managing API latency
- Ensuring factual grounding

## 6. Outcome
End-to-end AI-powered podcast generation completed.

---

# Sprint 3 – Evaluation & Research Metrics (April 2026)

## 1. Overview
Sprint 3 focused on transforming the project into a research-grade system by implementing evaluation metrics and comparison analysis.

## 2. Objectives
- Implement ROUGE evaluation
- Implement BERTScore evaluation
- Compare baseline vs hybrid model
- Conduct human evaluation study
- Generate performance graphs

## 3. Completed Work
- Compared keyword-only baseline with hybrid scoring model
- Calculated ROUGE scores
- Computed BERTScore similarity
- Collected human ratings (accuracy, clarity, excitement)
- Generated performance comparison graphs

## 4. Key Achievements
- Demonstrated improvement over baseline model
- Validated system accuracy scientifically
- Strengthened academic contribution

## 5. Challenges
- Creating ground truth highlights
- Interpreting evaluation results

## 6. Outcome
Project upgraded to research-level quality.

---

# Sprint 4 – Advanced Features & Multilingual Support (May 2026)

## 1. Overview
Sprint 4 focused on adding advanced features to enhance system scalability and innovation.

## 2. Objectives
- Implement speaker diarization
- Add multilingual support (Hindi, Marathi)
- Implement translation pipeline
- Improve UI / dashboard visualization
- Optimize scoring engine

## 3. Completed Work
- Added speaker labels in transcript
- Implemented Hindi speech-to-text processing
- Integrated translation API
- Generated multilingual podcast summaries
- Developed dashboard with highlight timeline graph

## 4. Key Achievements
- Multilingual podcast generation
- Improved transcript clarity with diarization
- Enhanced visualization of highlight scores

## 5. Challenges
- Handling mixed-language commentary
- Speaker boundary accuracy

## 6. Outcome
Project completed with advanced AI capabilities.

---

# Final Conclusion

Over the 6-month duration, the project evolved from architectural planning to a fully functional AI-powered sports highlight extraction and podcast generation system. The system integrates custom scoring algorithms, Generative AI, multilingual processing, and research-based evaluation metrics.

The hybrid approach (custom highlight detection + LLM summarization + verification layer) ensures both performance efficiency and factual accuracy, making the system suitable for real-world media automation applications.

---

# Future Scope

- Real-time streaming highlight detection
- Integration with live sports APIs
- Mobile application deployment
- Advanced prosody-based excitement detection
- Deployment as scalable microservices

---

# Technology Stack

- Python
- Google Speech-to-Text API
- Vertex AI (Gemini)
- Google Text-to-Speech
- Pandas, NLP libraries
- Firestore / Cloud Storage
- React / Flask (Dashboard)

---

# Research Contribution

- Custom weighted highlight scoring model
- Hybrid AI architecture
- Hallucination verification layer
- Multilingual podcast generation
- Comparative evaluation using ROUGE and BERTScore