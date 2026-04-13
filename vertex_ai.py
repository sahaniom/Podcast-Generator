from google import genai
# 🔑 Replace with your API key
genai.configure(api_key="AIzaSyBIB9V62vC0hHJ_-7qENx0c6KGcICnwuYY")

def generate_summary_vertex(text):

    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""
    You are a sports commentator AI.

    Summarize the following football commentary into an exciting podcast-style summary.
    Highlight key moments like goals, penalties, and important plays.

    Commentary:
    {text}
    """

    response = model.generate_content(prompt)

    return response.text