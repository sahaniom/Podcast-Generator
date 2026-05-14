# Prompt designed to guide the LLM in extracting structured data from noisy transcripts.
# It enforces strict JSON output and provides a blueprint for the expected fields.

EXTRACTION_PROMPT = """
You are an expert cricket commentary analyzer.

Tasks:
1. Fix transcription/ASR mistakes
2. Remove repeated commentary
3. Extract ONLY important cricket events
4. Do NOT hallucinate
5. If no event exists, return empty events

Valid event types:
- WICKET
- FOUR
- SIX
- RUN
- CATCH
- LBW

Output STRICT JSON ONLY.

Format:

{{
  "sport": "cricket",
  "teams": [],
  "events": [
    {{
      "type": "",
      "description": ""
    }}
  ],
  "score_summary": "",
  "result": ""
}}

Transcript:
{transcript}
"""