import json
import os
import re
import time

from llm.prompts import EXTRACTION_PROMPT
from llm.ollama_client import call_ollama
from processing.chunking import chunk_text


CHUNK_RESULTS_PATH = "llm_chunk_results.jsonl"
CHUNK_STATE_PATH = "llm_chunk_state.json"


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


def extract_from_chunk(chunk, sport):
    """
    Cleans transcript chunk using sport-aware LLM cleaner
    before structured extraction.
    """

    print("\nOriginal chunk:\n", chunk[:200], "...\n")

    # ----------------------------------------
    # STEP 2: STRUCTURED EXTRACTION
    # ----------------------------------------
    prompt = EXTRACTION_PROMPT.format(
        transcript=chunk,
        sport=sport
    )

    print("Calling extraction LLM...")

    response = call_ollama(prompt)

    # Save extraction response
    with open(
        "debug_llm_output.txt",
        "a",
        encoding="utf-8"
    ) as f:

        f.write("CLEANED CHUNK:\n")
        f.write(chunk)

        f.write("\n\nEXTRACTION OUTPUT:\n")
        f.write(response)

        f.write(
            "\n\n======================================================\n\n"
        )

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
        for team in r.get("teams", []):
            if isinstance(team, str):
                teams.add(team.strip())

            elif isinstance(team, dict):
                name = team.get("name")

                if isinstance(name, str):
                    teams.add(name.strip())

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


def load_chunk_state():
    if not os.path.exists(CHUNK_STATE_PATH):
        return 0

    try:
        with open(CHUNK_STATE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return int(data.get("processed_count", 0))
    except Exception:
        return 0


def save_chunk_state(processed_count):
    with open(CHUNK_STATE_PATH, "w", encoding="utf-8") as f:
        json.dump({"processed_count": processed_count}, f)


def load_previous_results(processed_count):
    if processed_count <= 0 or not os.path.exists(CHUNK_RESULTS_PATH):
        return []

    results = []
    with open(CHUNK_RESULTS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except Exception:
                continue

            parsed = record.get("parsed")
            if parsed:
                results.append(parsed)

    return results


def llm_extract(transcript, sport):
    """
    Orchestrates the LLM extraction process:
    1. Chunks the transcript into smaller pieces.
    2. Sequentially extracts structured data from each chunk using the LLM.
    3. Merges the results into a single totalized JSON object.
    """
    print("Chunking transcript...")
    chunks = chunk_text(transcript)

    processed_count = load_chunk_state()
    results = load_previous_results(processed_count)

    if processed_count > 0:
        print(f"Resuming from chunk {processed_count + 1} of {len(chunks)}")

    print("Extracting structured data from chunks...")
    print(f"Total chunks to process: {len(chunks)}\n")
    for i, chunk in enumerate(chunks, 1):
        if i <= processed_count:
            continue

        chunk_start = time.time()
        parsed = extract_from_chunk(chunk, sport)
        chunk_end = time.time()

        if parsed:
            results.append(parsed)

        # Append a record for each processed chunk for resumability.
        with open(CHUNK_RESULTS_PATH, "a", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    {
                        "chunk_index": i,
                        "parsed": parsed,
                        "processed_at": time.time()
                    }
                )
            )
            f.write("\n")

        processed_count = i
        save_chunk_state(processed_count)
        
        print(f"Chunk {i} processed in {chunk_end - chunk_start:.2f} seconds")

    print("Merging results...")
    return merge_results(results)
