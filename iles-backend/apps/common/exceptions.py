"""Custom exception handler for consistent error envelopes.

Every error returns:
    {"error": {"code": "...", "detail": "...", "fields": {...}}}

This makes frontend error handling deterministic.
"""
from rest_framework.views import exception_handler


def envelope_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return None

    data = response.data
    code = exc.__class__.__name__

    if isinstance(data, dict):
        if "detail" in data and len(data) == 1:
            envelope = {"error": {"code": code, "detail": str(data["detail"])}}
        else:
            envelope = {
                "error": {
                    "code": code,
                    "detail": "Validation failed.",
                    "fields": data,
                }
            }
    else:
        envelope = {"error": {"code": code, "detail": str(data)}}

    response.data = envelope
    return response
