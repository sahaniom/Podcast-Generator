def chunk_text(text, chunk_size=1200):
    """
    Splits the provided text into smaller chunks of a specific size.

    Args:
        text (str): The input text to be split.
        chunk_size (int): The maximum character length for each chunk. 
                        Defaults to 1200 characters to prevent LLM context window issues.

    Returns:
        list: A list of text strings (chunks).
    """
    chunks = []

    # Iterate through the text and extract slices of 'chunk_size'
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    return chunks
