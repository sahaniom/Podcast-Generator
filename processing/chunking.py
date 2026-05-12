def chunk_text(text, chunk_size=3000):
    """
    Splits the provided text into smaller chunks of a specific size.
    This is useful for processing large transcripts with LLMs that have token limits.
    """
    chunks = []

    # Iterate through the text and extract slices of 'chunk_size'
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    return chunks
