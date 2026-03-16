def validate_consultation_response(response: str) -> bool:
    return bool(response and response.strip())
