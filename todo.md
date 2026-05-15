- [ ] In UI there should be two options: from URL and by uploading Audio file.
    - Mentor at NIC wanted something to be used for office purpose, and whisper is open source locally downloaded so no data is shared.
    - And maybe we can do something about it, think, like what extra features we can add. like additional preprocessing we are doing in games like counting no. of sixes and all.

- [ ] While deploying add youtube cookies to download audio from youtube using yt_dlp.

- [ ] Check Ollama initial setup in README.md (Ollama serve and other commands)

- [ ] Languages to translate in:
    - Hindi
    - Tamil
    - Bengali
    - Marathi
    - Telugu
    - Kannada
    - Malayalam
    - Gujarati
    - Punjabi

# Project Checkpoints

- [x] **Phase 1: Rule-Based Model**
    - Create model using the current rule-based approach.
    > Result not as expected
- [x] **Phase 2: Machine Learning Model**
    - Transition to using Machine Learning for highlight detection.
- [x] **Phase 3: Hybrid Approach**
    - Combine rule-based logic with ML for improved accuracy.
- [x] **Phase 4: Comparison & Final Selection**
    - Compare results from Rule-Based, ML, and Hybrid models.
    - Evaluate performance manually and using LLM-based assessment.
    - Select the best approach for production.

    > ML model is better without any extra rule. Those things are handles by LLM.
    > There is no need of training model as it is not required in this step.

# For PPT and report:

   Why Your Current main.py Is Actually Good

You already implemented:

caching
reusable scripts
reverse-order loading
video-specific storage
separation of concerns

Those are genuinely good software-engineering decisions.

Especially this logic:

translated exists?
↓
english exists?
↓
otherwise run full pipeline

That’s production-style thinking.

---
---
---

