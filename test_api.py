import requests

BASE_URL = "http://127.0.0.1:8000"


def test_health_endpoint():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data.get("status") == "ok"
    assert "message" in data


def test_review_endpoint_returns_expected_structure():
    code_sample = (
        "try:\n"
        "    print('hello')\n"
        "except:\n"
        "    pass\n"
    )
    payload = {
        "language": "python",
        "code": code_sample,
    }

    response = requests.post(
        f"{BASE_URL}/review",
        json=payload,
        timeout=30,
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert set(data.keys()) == {"summary", "bugs", "improvements", "score"}
    assert isinstance(data["summary"], str)
    assert isinstance(data["bugs"], list)
    assert isinstance(data["improvements"], list)
    assert isinstance(data["score"], int)
    assert 0 <= data["score"] <= 10