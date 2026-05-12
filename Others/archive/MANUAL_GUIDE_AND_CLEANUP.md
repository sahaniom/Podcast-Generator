# Manual Execution and Recommendations

If you choose to run the project files individually rather than using the `run_pipeline.py` script, follow the execution order below. This document also highlights files that are either redundant or could be removed to clean up the workspace.

## 1. Manual Execution Order
To ensure all dependencies (like the ML model) are ready for the web application, run the scripts in this sequence:

1.  **[preprocess.py](preprocess.py)**
    - **Action**: Cleans the raw transcription.
    - **Requirement**: A valid `transcript_raw.json` must exist.
2.  **[create_dataset.py](create_dataset.py)**
    - **Action**: Uses the cleaned text to label highlights and creates `training_data.json`.
3.  **[train_model.py](train_model.py)**
    - **Action**: Trains the Logistic Regression model and saves `highlight_model.pkl` and `vectorizer.pkl`.
4.  **[app.py](app.py)**
    - **Action**: Starts the UI. 
    - **Command**: `streamlit run app.py`

---

## 2. Unnecessary Files
The following files are not required for the pipeline to function and can be safely removed or consolidated:

### Redundant Files
- **[temp.txt](temp.txt)**: Contains a snippet of a VS Code environment warning. It is not code and serves no functional purpose in the project.
- **[vertex_ai.py](vertex_ai.py)**: While this contains the logic for Gemini integration, the same logic is already implemented directly inside **[app.py](app.py)**. Unless this is intended for future modularity, it is currently a duplicate.

### Documentation Cleanup
- **Others/** (Folder): This directory contains older or duplicate versions of the documentation found in the root. 
    - Specifically, `Others/project.md` is superseded by the root [PROJECT_EXPLANATION.md](PROJECT_EXPLANATION.md) and [file_descriptions.md](file_descriptions.md).
