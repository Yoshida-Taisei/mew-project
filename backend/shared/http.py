import json
from typing import Any, Dict, Iterable, Optional


def _normalize_origin(origin: Optional[str]) -> str:
    return (origin or "").strip()


def cors_headers(origin: Optional[str], allowed_origins: Iterable[str]) -> Dict[str, str]:
    origin_n = _normalize_origin(origin)
    allowed = {o.strip() for o in allowed_origins if o and o.strip()}
    allow_origin = origin_n if origin_n and origin_n in allowed else "*"

    return {
        "Content-Type": "application/json; charset=utf-8",
        "Access-Control-Allow-Origin": allow_origin,
        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
        "Access-Control-Allow-Methods": "OPTIONS,GET,POST",
    }


def get_header(event: Dict[str, Any], name: str) -> Optional[str]:
    headers = event.get("headers") or {}
    if not isinstance(headers, dict):
        return None
    for k, v in headers.items():
        if isinstance(k, str) and k.lower() == name.lower():
            return v
    return None


def json_response(
    *,
    status_code: int = 200,
    body: Any = None,
    headers: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    return {
        "statusCode": int(status_code),
        "headers": headers or {"Content-Type": "application/json; charset=utf-8"},
        "body": json.dumps(body, ensure_ascii=False),
    }


def error_response(
    *,
    status_code: int,
    message: str,
    origin: Optional[str] = None,
    allowed_origins: Iterable[str] = (),
    details: Any = None,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {"message": message}
    if details is not None:
        payload["details"] = details
    return json_response(
        status_code=status_code,
        body=payload,
        headers=cors_headers(origin, allowed_origins),
    )

