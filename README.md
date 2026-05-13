# AI Code Review API

A beginner-friendly FastAPI portfolio project that runs locally with Ollama for AI-powered code review.

## Description

This project provides a clean REST API for reviewing code samples in any language.
It uses FastAPI and a local Ollama model to return a structured review with a summary, bugs, improvements, and a score.

## Features

- `POST /review` endpoint for code review
- Local AI execution through Ollama
- Structured JSON response with `summary`, `bugs`, `improvements`, and `score`
- Error handling when Ollama is unavailable
- Beginner-friendly and ready for local development

## Tech Stack

- Python
- FastAPI
- Ollama
- Requests
- python-dotenv

## Installation (Windows PowerShell)

```powershell
git clone https://github.com/your-username/ai-code-review-api.git
cd ai-code-review-api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

> If you use VS Code, the project includes `.vscode/settings.json` to select the local `.venv` interpreter automatically.

## Ollama Setup

1. Install Ollama: https://ollama.com/
2. Pull the recommended model:

```powershell
ollama pull llama3.2
```

3. Start the Ollama daemon:

```powershell
ollama daemon
```

By default, the API uses `http://127.0.0.1:11434` and model `llama3.2`.

## Environment Variables

Copy `.env.example` to `.env` if you want to override the defaults:

```powershell
copy .env.example .env
```

Available variables:

- `OLLAMA_BASE_URL` - local Ollama URL (default: `http://127.0.0.1:11434`)
- `OLLAMA_MODEL` - model name (default: `llama3.2`)

## Run the FastAPI Server

```powershell
python -m uvicorn main:app --reload
```

Open the docs at:

- `http://127.0.0.1:8000/docs`

## Test with Thunder Client

Create a new request in Thunder Client targeting `http://127.0.0.1:8000/review`.
Use JSON body:

```json
{
  "language": "python",
  "code": "try:\n    print('hello')\nexcept:\n    pass"
}
```

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

- `main.py` - FastAPI application and Ollama integration
- `requirements.txt` - Python dependencies
- `README.md` - project documentation
- `.gitignore` - ignored files and folders
- `.env.example` - example environment configuration
- `test_api.py` - sample API test script

## Future Improvements

- Add automated tests for API behavior
- Support multiple review styles in queries
- Add request validation for language and code length
- Cache repeated reviews for faster response times

## Notes

This project does not use OpenAI, DeepSeek, or Hugging Face. It is designed for local AI review using Ollama only.