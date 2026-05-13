[README.md](https://github.com/user-attachments/files/27693066/README.md)
# AI Code Review API

A beginner-friendly FastAPI portfolio project that runs locally with Ollama for AI-powered code review.

## Description

This project provides a clean REST API for reviewing code samples in any language.
It uses FastAPI and a local Ollama model to return a structured review with a summary, bugs, improvements, and a score.

## Features

- `POST /review` endpoint for code review
- `GET /` health check endpoint
- Local AI execution through Ollama (`/api/generate`)
- Structured JSON response with `summary`, `bugs`, `improvements`, and `score`
- Input validation (language: max 50 chars, code: max 10,000 chars)
- Error handling when Ollama is unavailable
- Beginner-friendly and ready for local development

## Tech Stack

- Python
- FastAPI
- Ollama
- Requests
- python-dotenv
- pytest

## Installation (Windows PowerShell)

```powershell
git clone https://github.com/narlifresa/ai-code-review-api.git
cd ai-code-review-api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Installation (macOS / Linux)

```bash
git clone https://github.com/narlifresa/ai-code-review-api.git
cd ai-code-review-api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ollama Setup

1. Install Ollama: https://ollama.com/
2. Pull the recommended model:

```bash
ollama pull llama3.2
```

3. Start the Ollama daemon:

```bash
ollama serve
```

By default, the API connects to `http://127.0.0.1:11434` using model `llama3.2`.

## Environment Variables

Copy `.env.example` to `.env` if you want to override the defaults:

```powershell
copy .env.example .env   # Windows
cp .env.example .env     # macOS / Linux
```

Available variables:

- `OLLAMA_BASE_URL` — Ollama server URL (default: `http://127.0.0.1:11434`)
- `OLLAMA_MODEL` — model name (default: `llama3.2`)

## Run the FastAPI Server

```bash
python -m uvicorn main:app --reload
```

Open the interactive docs at:

- `http://127.0.0.1:8000/docs`

## Run Tests

```bash
pytest test_api.py -v
```

> Make sure both the FastAPI server and Ollama are running before executing tests.

## Example Request

```json
{
  "language": "python",
  "code": "try:\n    print('hello')\nexcept:\n    pass"
}
```

## Example Response

```json
{
  "summary": "The code runs but uses a broad exception handler.",
  "bugs": [
    "Bare except can hide real errors."
  ],
  "improvements": [
    "Use except Exception as e instead of bare except.",
    "Add meaningful error handling."
  ],
  "score": 6
}
```

## Project Structure

- `main.py` — FastAPI application and Ollama integration
- `test_api.py` — pytest test suite
- `requirements.txt` — Python dependencies
- `README.md` — project documentation
- `.gitignore` — ignored files and folders
- `.env.example` — example environment configuration

## Future Improvements

- Support multiple review styles (security-focused, performance-focused, etc.)
- Cache repeated reviews for faster response times
- Add request rate limiting
- Dockerize the project for easier deployment

## Notes

This project does not use OpenAI, DeepSeek, or Hugging Face. It is designed for local AI review using Ollama only. The API communicates with Ollama via the native `/api/generate` endpoint.
