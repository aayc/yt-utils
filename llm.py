import json
import os
import re
import google.generativeai as genai

def unwrap_md_json(text: str) -> str:
    """Return the first block of JSON code in the text. If no JSON is found, return the original text."""

    if '```json' in text.lower():
        text = re.split('```json', text, flags=re.IGNORECASE)[1]
        if '```' in text:
            text = text.split('```')[0]
    return text.strip()

def gemini_qa(question: str, context: str, model: str = "gemini-1.5-flash") -> str:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel(model)
    
    prompt = f"""# Lecture transcript

{context}

###

Based on the above context, answer the following question: {question}"""
    
    response = model.generate_content(prompt)
    return response.text

def gemini_open_ended(question: str, model: str = "gemini-1.5-flash") -> str:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel(model)
    chat = model.start_chat()
    response = chat.send_message(question)
    return response.text


def gemini_flashcards(text: str, model: str = "gemini-1.5-pro") -> list[dict[str, str]]:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel(model)
    
    prompt = f"""Given the text of this lecture, create flashcards in a question and answer format for studying later on Anki.
Format the response as a list of JSON objects with 'question' and 'answer' fields.
Text: {text}

Return your response as a JSON array of objects, like this:

```json
[
    {{"question": <question>, "answer": <answer>}},
    {{"question": <question>, "answer": <answer>}}
]
```"""
    
    response = model.generate_content(prompt)
    try:
        flashcards = json.loads(unwrap_md_json(response.text))
        assert isinstance(flashcards, list), "Flashcards are not a list"
        assert all(isinstance(card, dict) and 'question' in card and 'answer' in card for card in flashcards), "Flashcards are not dictionaries with 'question' and 'answer' fields"
        return flashcards
    except:
        return None