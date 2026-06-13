import re
from llm.ollama_client import call_ollama

# System prompt to generate a concise summary from the transcript
SUMMARY_PROMPT = """
You are an expert sports commentator.
Based on the following transcript of a {sport} match, generate a detailed summary of the match.

IMPORTANT RULES:
- Write all numbers and scores as words in English (e.g., write 'three' instead of '3', 'ten' instead of '10', 'one hundred forty-six' instead of '146').
- Do NOT use numeric digits under any circumstances.
- Do not include any metadata, intro, JSON, markdown formatting, or stage directions. Return ONLY the plain text summary.

Transcript:
{transcript}
"""

def convert_numbers_to_words(text):
    """
    Finds numeric digits (both integers and decimals) in the text and converts them to words.
    E.g. 146 -> "one hundred forty six", 19.1 -> "nineteen point one".
    """
    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", 
            "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    
    def int_to_words(num):
        if num == 0:
            return "zero"
        words = []
        if num >= 100:
            words.append(ones[num // 100] + " hundred")
            num %= 100
        if num >= 20:
            words.append(tens[num // 10])
            num %= 10
        if num > 0:
            words.append(ones[num])
        return " ".join(w for w in words if w)

    def replace_match(match):
        num_str = match.group(0)
        if '.' in num_str:
            parts = num_str.split('.')
            try:
                left = int_to_words(int(parts[0]))
                right_digits = []
                for digit in parts[1]:
                    d = int(digit)
                    if d == 0:
                        right_digits.append("zero")
                    else:
                        right_digits.append(ones[d])
                right = " ".join(right_digits)
                return f"{left} point {right}"
            except (ValueError, IndexError):
                return num_str
        else:
            try:
                num = int(num_str)
                if num < 1000:
                    return int_to_words(num)
                return num_str
            except ValueError:
                return num_str

    # Match float numbers (e.g. 19.1) or integers (e.g. 146)
    return re.sub(r'\b\d+(?:\.\d+)?\b', replace_match, text)


def generate_summary(transcript, sport):
    """
    Generates a concise summary of the match based on the transcript.
    Truncates long transcripts to avoid context length issues in the local LLM.
    Ensures all numbers are represented as words.
    """
    # Truncate to a safe maximum length of 15000 characters
    max_chars = 15000
    truncated_transcript = transcript
    if len(transcript) > max_chars:
        truncated_transcript = transcript[:max_chars] + "..."

    prompt = SUMMARY_PROMPT.format(
        sport=sport,
        transcript=truncated_transcript
    )
    
    print("\nCalling summary generation LLM...")
    response = call_ollama(prompt).strip()
    
    # Post-process to guarantee numbers are in words
    processed_response = convert_numbers_to_words(response)
    
    print(f"Original LLM Summary: {response}")
    print(f"Processed Summary (no digits): {processed_response}")
    
    return processed_response
