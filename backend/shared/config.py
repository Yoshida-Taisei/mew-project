import os
from dataclasses import dataclass
from typing import List


def _split_csv(value: str) -> List[str]:
    return [v.strip() for v in (value or "").split(",") if v.strip()]


@dataclass(frozen=True)
class AppConfig:
    line_channel_access_token: str
    line_channel_id: str
    allowed_origins: List[str]
    aws_region: str


def load_config() -> AppConfig:
    return AppConfig(
        line_channel_access_token=os.environ.get("LINE_CHANNEL_ACCESS_TOKEN", ""),
        line_channel_id=os.environ.get("LINE_CHANNEL_ID", ""),
        allowed_origins=_split_csv(os.environ.get("ALLOWED_ORIGINS", "")),
        aws_region=os.environ.get("AWS_REGION", "ap-northeast-1"),
    )

