import json
import requests

from backend.shared.config import load_config
from backend.shared.http import cors_headers, error_response, get_header


def lambda_handler(event, context):
    
    cfg = load_config()
    origin = get_header(event, "origin")

    try:
        access_token = event["access_token"]
    except Exception:
        return error_response(
            status_code=400,
            message="Bad Request: access_token is required",
            origin=origin,
            allowed_origins=cfg.allowed_origins,
        )
    
    if not _validate_access_token(access_token, cfg.line_channel_id):
        return error_response(
            status_code=401,
            message="Access token validation failed",
            origin=origin,
            allowed_origins=cfg.allowed_origins,
        )

    user_id = _get_user_id(access_token)
    link_token = _get_link_token(cfg.line_channel_access_token, user_id)
    
    return {
        "statusCode": 200,
        "headers": cors_headers(origin, cfg.allowed_origins),
        "body": link_token,
    }


def _validate_access_token(access_token: str, expected_channel_id: str) -> bool:
    response = requests.get(
        "https://api.line.me/oauth2/v2.1/verify",
        params={"access_token": access_token},
        timeout=10,
    )
    client_id = response.json().get("client_id")
    return bool(client_id) and client_id == expected_channel_id

def _get_user_id(access_token: str) -> str:
    response = requests.get(
        "https://api.line.me/v2/profile",
        headers={"Authorization": "Bearer " + access_token},
        timeout=10,
    )
    return response.json()["userId"]

def _get_link_token(channel_access_token: str, user_id: str) -> dict:
    response = requests.post(
        f"https://api.line.me/v2/bot/user/{user_id}/linkToken",
        headers={"Authorization": "Bearer " + channel_access_token},
        timeout=10,
    )
    return response.json()