import json
import re
import time

from llm.prompts import EXTRACTION_PROMPT
from llm.ollama_client import call_ollama
from processing.chunking import chunk_text


def extract_json(text):
    """
    Extracts the first valid JSON object found in the given text using a recursive regex.
    The regex handles nested curly braces to better isolate complete JSON objects.
    Splits multiple potential JSON objects and returns the first one that parses correctly.
    """
    matches = re.findall(r"\{(?:[^{}]|(?:\{[^{}]*\}))*\}", text, re.DOTALL)

    for match in matches:
        try:
            return json.loads(match)
        except:
            continue

    return None


def extract_from_chunk(chunk):
    """
    Uses the LLM to extract structured data from a single chunk of text.
    The chunk is injected into the EXTRACTION_PROMPT and sent to Ollama.
    Logs the raw LLM response to 'debug_llm_output.txt' for analysis.
    """
    print("\nExtracting from chunk:\n", chunk[:200], "...\n")
    prompt = EXTRACTION_PROMPT.format(transcript=chunk)

    print("Calling LLM...")
    response = call_ollama(prompt)

    # Log raw output for debugging JSON extraction issues
    with open("debug_llm_output.txt", "a", encoding="utf-8") as f:
        f.write(response)
        f.write("\n\n======================================================\n\n")

    print("Extracted response:\n", response, "\n")
    return extract_json(response)


def merge_results(results):
    """
    Merges multiple extraction results into a single structured output.
    Aggregates sport, teams, events, score summary, and result.
    Validates event structure and deduplicates teams across chunks.
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

        # Filter and validate event objects from current chunk
        for event in r.get("events", []):
            if isinstance(event, dict):
                if "type" in event and "description" in event:
                    final["events"].append(event)

        # Take the most recent score summary and result as they are likely the final state
        if r.get("score_summary"):
            final["score_summary"] = r["score_summary"]

        if r.get("result"):
            final["result"] = r["result"]

    final["teams"] = list(teams)

    return final


def llm_extract(transcript):
    """
    Orchestrates the LLM extraction process:
    1. Chunks the transcript into smaller pieces.
    2. Sequentially extracts structured data from each chunk using the LLM.
    3. Merges the results into a single totalized JSON object.
    """
    print("Chunking transcript...")
    chunks = chunk_text(transcript)

    results = []

    print("Extracting structured data from chunks...")
    print(f"Total chunks to process: {len(chunks)}\n")
    for i, chunk in enumerate(chunks, 1):
        chunk_start = time.time()
        parsed = extract_from_chunk(chunk)
        chunk_end = time.time()

        if parsed:
            results.append(parsed)
        
        print(f"Chunk {i} processed in {chunk_end - chunk_start:.2f} seconds")

    print("Merging results...")
    return merge_results(results)
