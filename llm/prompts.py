# Prompt designed to guide the LLM in extracting structured data from noisy transcripts.
# It enforces strict JSON output and provides a blueprint for the expected fields.

EXTRACTION_PROMPT = """
You are an information extraction system.

Your task:
Convert the sports transcript into STRICT JSON.

RULES:
- Output ONLY JSON
- No markdown
- No explanations
- No bullet points
- No extra text
- Do not hallucinate
- If information is missing, use empty string or empty list
- Event types must be UPPERCASE
- Keep descriptions short

VALID EVENT TYPES:
WICKET
FOUR
SIX
GOAL
FOUL
BOUNDARY
OUT
RUN
CATCH

JSON FORMAT:

{{
  "sport": "",
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