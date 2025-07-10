from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

class Prompt(BaseModel):
    prompt: str
    max_tokens: int = 256

@app.post("/generate")
def generate_text(prompt: Prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "deepseek-r1",
            "prompt": prompt.prompt,
            "stream": False
        }
    )
    data = response.json()

    # Extract and clean the response
    if isinstance(data.get("response"), str):
        cleaned = data["response"]
        
        # Remove <think>...</think> section if it exists
        if "<think>" in cleaned and "</think>" in cleaned:
            cleaned = cleaned.split("</think>")[-1]

        # Remove all newline characters and extra whitespace
        cleaned = cleaned.replace("\n", " ").strip()

        return {"response": cleaned}
    else:
        return {"error": "Unexpected response format", "raw": data}
