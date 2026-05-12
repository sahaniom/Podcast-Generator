import requests

# URL for the local Ollama API
OLLAMA_URL = "http://localhost:11434/api/generate"

# The LLM model to use for generation
MODEL_NAME = "qwen3.5:2b"


def call_ollama(prompt):
    """
    Makes a POST request to the local Ollama API to generate a response for the given prompt.
    Returns the generated response text.
    """
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "temperature": 0
            }
        )

        print("STATUS CODE:", response.status_code)

        # Raise an exception if the request failed
        response.raise_for_status()

        data = response.json()

        # Return the actual text response from the model
        return data["response"]

    except requests.exceptions.RequestException as e:
        print("Ollama Request Failed")
        print(e)
        
        # Log the response content if available for debugging
        if response is not None:
            print(response.text)

        raise

