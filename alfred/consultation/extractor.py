def extract_learning(response: str) -> dict:
    return {"response": response.strip(), "insights": [line.strip() for line in response.splitlines() if line.strip()][:5]}
