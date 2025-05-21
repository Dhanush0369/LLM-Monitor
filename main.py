# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# Auto-instrument for Prometheus metrics
Instrumentator().instrument(app).expose(app)

class Prompt(BaseModel):
    text: str

@app.post("/generate")
def generate_text(prompt: Prompt):
    api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
    headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}
    
    try:
        response = requests.post(api_url, headers=headers, json={"inputs": prompt.text})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
