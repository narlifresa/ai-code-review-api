import requests

BASE_URL = "http://127.0.0.1:8000"


def test_api():
    print("=" * 60)
    print("AI Code Review API - Test Suite")
    print("=" * 60)
    print()

    print("Testing GET /...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except requests.exceptions.RequestException as error:
        print(f"ERROR: Could not connect to API. {error}")
        return

    print()
    print("Testing POST /review...")
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

    try:
        response = requests.post(
            f"{BASE_URL}/review",
            json=payload,
            timeout=30,
        )
        print(f"Status: {response.status_code}")
        print(f"Body: {response.json()}")
    except requests.exceptions.Timeout:
        print("ERROR: Request timed out. Is the FastAPI server running?")
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to API. Is the server running?")
    except Exception as error:
        print(f"ERROR: {error}")

    print()
    print("✅ Test script finished.")