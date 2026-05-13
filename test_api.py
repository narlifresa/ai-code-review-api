import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"

CODE_SAMPLE = (
    "try:\n"
    "    print('hello')\n"
    "except:\n"
    "    pass\n"
)


def test_health_check():
    """GET / should return 200 with status ok."""
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    body = response.json()
    assert body.get("status") == "ok"
    assert "message" in body


def test_review_returns_200():
    """POST /review should return 200 for valid input."""
    response = requests.post(
        f"{BASE_URL}/review",
        json={"language": "python", "code": CODE_SAMPLE},
        timeout=60,
    )
    assert response.status_code == 200


def test_review_response_keys():
    """POST /review response must contain all required keys."""
    response = requests.post(
        f"{BASE_URL}/review",
        json={"language": "python", "code": CODE_SAMPLE},
        timeout=60,
    )
    body = response.json()
    assert "summary" in body
    assert "bugs" in body
    assert "improvements" in body
    assert "score" in body


def test_review_field_types():
    """POST /review fields must have correct types."""
    response = requests.post(
        f"{BASE_URL}/review",
        json={"language": "python", "code": CODE_SAMPLE},
        timeout=60,
    )
    body = response.json()
    assert isinstance(body["summary"], str)
    assert isinstance(body["bugs"], list)
    assert isinstance(body["improvements"], list)
    assert isinstance(body["score"], int)


def test_review_score_range():
    """Score must be between 0 and 10 inclusive."""
    response = requests.post(
        f"{BASE_URL}/review",
        json={"language": "python", "code": CODE_SAMPLE},
        timeout=60,
    )
    score = response.json()["score"]
    assert 0 <= score <= 10


def test_review_rejects_empty_code():
    """POST /review should reject empty code with 422."""
    response = requests.post(
        f"{BASE_URL}/review",
        json={"language": "python", "code": ""},
        timeout=10,
    )
    assert response.status_code == 422


def test_review_rejects_empty_language():
    """POST /review should reject empty language with 422."""
    response = requests.post(
        f"{BASE_URL}/review",
        json={"language": "", "code": CODE_SAMPLE},
        timeout=10,
    )
    assert response.status_code == 422
