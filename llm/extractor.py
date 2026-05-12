import json
import re

from llm.prompts import EXTRACTION_PROMPT
from llm.ollama_client import call_ollama
from processing.chunking import chunk_text


def extract_json(text):
    """
    Extracts the first valid JSON object found in the given text.
    Uses regex to find the content between curly braces.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            return None

    return None


def extract_from_chunk(chunk):
    """
    Uses the LLM to extract structured data from a single chunk of text.
    The chunk is injected into the EXTRACTION_PROMPT and sent to Ollama.
    """
    print("\nExtracting from chunk:\n", chunk[:200], "...\n")
    prompt = EXTRACTION_PROMPT.format(transcript=chunk)

    print("Calling LLM...")
    response = call_ollama(prompt)

    print("Extracted response:\n", response, "\n")
    return extract_json(response)


def merge_results(results):
    """
    Merges multiple extraction results into a single structured output.
    Aggregates sport, teams, events, score summary, and result.
    """
    final = {
        "sport": "",
        "teams": [],
        "events": [],
        "score_summary": "",
        "result": ""
    }

    teams = set()

    for r in results:
        if not r:
            continue

        # If sport is not set, take it from the current result
        if not final["sport"] and r.get("sport"):
            final["sport"] = r["sport"]

        # Merge teams using a set to deduplicate
        teams.update(r.get("teams", []))

        # Combine all events
        final["events"].extend(r.get("events", []))

        # Take the most recent score summary and result
        if r.get("score_summary"):
            final["score_summary"] = r["score_summary"]

        if r.get("result"):
            final["result"] = r["result"]

    final["teams"] = list(teams)

    return final


def llm_extract(transcript):
    """
    Orchestrates the LLM extraction process:
    1. Chunks the transcript.
    2. Extracts data from each chunk.
    3. Merges the results into a single JSON object.
    """
    print("Chunking transcript...")
    chunks = chunk_text(transcript)

    results = []

    print("Extracting structured data from chunks...")
    print(f"Total chunks to process: {len(chunks)}\n")
    for chunk in chunks:
        parsed = extract_from_chunk(chunk)

        if parsed:
            results.append(parsed)

    print("Merging results...")
    return merge_results(results)
