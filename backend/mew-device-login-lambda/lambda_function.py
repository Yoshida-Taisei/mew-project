import base64
import json

import boto3
from jose import jwt

from backend.shared.config import load_config
from backend.shared.http import cors_headers, error_response, get_header


_DDB_TABLE_NAME = "mew-line-device"
_DDB_LINE_ID_TEMP = "temp_id"
_NONCE_ADD_KEY = "12345678"


def lambda_handler(event, context):
    
    cfg = load_config()
    origin = get_header(event, "origin")

    auth = get_header(event, "authorization") or get_header(event, "Authorization")
    if not auth:
        return error_response(
            status_code=401,
            message="Unauthorized: Authorization header is required",
            origin=origin,
            allowed_origins=cfg.allowed_origins,
        )

    device_id = _get_device_id_from_jwt(auth)
    nonce_bytes = _generate_nonce(device_id)
    nonce_payload = {"nonce": nonce_bytes.decode("utf-8")}
    
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(_DDB_TABLE_NAME)
    _put_temp_nonce(table, device_id, nonce_bytes)
    
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": cors_headers(origin, cfg.allowed_origins),
        "body": json.dumps(nonce_payload, ensure_ascii=False),
    }


def _get_device_id_from_jwt(id_token: str) -> str:
    token = id_token.strip()
    if token.lower().startswith("bearer "):
        token = token[7:].strip()
    payload = jwt.get_unverified_claims(token)
    return payload["cognito:username"]


def _put_temp_nonce(dynamo_table, device_id: str, nonce: bytes) -> None:
    dynamo_table.put_item(
        Item={
            "DeviceID": device_id,
            "LINEID": _DDB_LINE_ID_TEMP,
            "nonce": nonce,
        }
    )


def _generate_nonce(device_id: str) -> bytes:
    return base64.b64encode((device_id + _NONCE_ADD_KEY).encode("utf-8"))