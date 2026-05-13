import json
import re
from os import getenv
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

load_dotenv()

OLLAMA_BASE_URL = getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = getenv("OLLAMA_MODEL", "llama3.2")

app = FastAPI(
    title="AI Code Review API",
    description="Review source code locally with FastAPI and Ollama.",
    version="1.0.0",
)


class ReviewRequest(BaseModel):
    language: str = Field(..., min_length=1, max_length=50, example="python")
    code: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        example="try:\n    print('hello')\nexcept:\n    pass",
    )


class ReviewResponse(BaseModel):
    summary: str
    bugs: List[str]
    improvements: List[str]
    score: int


def build_prompt(language: str, code: str) -> str:
    return (
        "You are a professional code reviewer.\n"
        "Analyze the code and return only a valid JSON object with these fields:\n"
        "summary, bugs, improvements, score.\n"
        "Do not write any text outside the JSON.\n"
        "Use arrays for bugs and improvements and an integer score from 0 to 10.\n\n"
        f"Language: {language}\n"
        "Code:\n"
        f"{code.strip()}\n"
    )


def extract_text_from_response(data: Any) -> str:
    if isinstance(data, str):
        return data
    if isinstance(data, dict):
        # FIX: "response" is the key used by Ollama's native /api/generate endpoint
        for key in ("response", "text", "output", "output_text", "content"):
            if key in data and isinstance(data[key], str):
                return data[key]
        if "choices" in data and isinstance(data["choices"], list):
            for choice in data["choices"]:
                text = extract_text_from_response(choice)
                if text:
                    return text
        if "results" in data and isinstance(data["results"], list):
            for result in data["results"]:
                text = extract_text_from_response(result)
                if text:
                    return text
        if "message" in data:
            return extract_text_from_response(data["message"])
    if isinstance(data, list):
        for item in data:
            text = extract_text_from_response(item)
            if text:
                return text
    return ""


def parse_ollama_output(text: str) -> Dict[str, Any]:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        trimmed = text
        start = trimmed.find("{")
        end = trimmed.rfind("}")
        if start != -1 and end != -1 and end > start:
            candidate = trimmed[start : end + 1]
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                pass
    raise ValueError("Could not parse Ollama response as JSON.")


def call_ollama(prompt: str) -> Dict[str, Any]:
    # FIX: Correct Ollama native API endpoint (was /v1/generate which does not exist)
    url = f"{OLLAMA_BASE_URL.rstrip('/')}/api/generate"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        # FIX: Ollama native API uses "options" for inference parameters
        "options": {
            "temperature": 0.2,
            "num_predict": 512,  # FIX: was 250, too low to fit full JSON response
        },
    }

    try:
        response = requests.post(url, json=payload, timeout=60)
    except requests.exceptions.RequestException as error:
        raise HTTPException(
            status_code=503,
            detail=(
                f"Unable to connect to Ollama at {OLLAMA_BASE_URL}. "
                "Make sure Ollama is running locally and the URL is correct."
            ),
        ) from error

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"Ollama returned an error: {response.status_code} - {response.text}",
        )

    result = response.json()
    text = extract_text_from_response(result)
    if not text:
        raise HTTPException(
            status_code=502,
            detail="Ollama returned no text output. Check your model and service status.",
        )

    parsed = parse_ollama_output(text)
    score = 0
    if parsed.get("score") is not None:
        score_match = re.search(r"(\d+)", str(parsed["score"]))
        if score_match:
            score = max(0, min(int(score_match.group(1)), 10))

    return {
        "summary": str(parsed.get("summary", "No summary available.")).strip(),
        "bugs": parsed.get("bugs") if isinstance(parsed.get("bugs"), list) else [],
        "improvements": parsed.get("improvements") if isinstance(parsed.get("improvements"), list) else [],
        "score": score,
    }


@app.get("/")
def health() -> Dict[str, str]:
    return {"status": "ok", "message": "AI Code Review API is running."}


@app.post("/review", response_model=ReviewResponse)
def review_code(request: ReviewRequest) -> Dict[str, Any]:
    prompt = build_prompt(request.language, request.code)
    return call_ollama(prompt)
