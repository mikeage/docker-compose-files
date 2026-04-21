from __future__ import annotations

from dataclasses import dataclass
from os import environ


@dataclass(frozen=True)
class Settings:
    immich_base_url: str
    immich_api_key: str
    timezone_name: str
    rotation_seconds: int
    output_width: int
    output_height: int
    jpeg_quality: int
    year_overlay: bool

    @classmethod
    def from_env(cls) -> "Settings":
        immich_base_url = environ.get("IMMICH_BASE_URL", "").strip().rstrip("/")
        immich_api_key = environ.get("IMMICH_API_KEY", "").strip()
        timezone_name = environ.get("TIMEZONE", "Asia/Jerusalem").strip()
        rotation_seconds = int(environ.get("ROTATION_SECONDS", "60"))
        output_width = int(environ.get("OUTPUT_WIDTH", "320"))
        output_height = int(environ.get("OUTPUT_HEIGHT", "240"))
        jpeg_quality = int(environ.get("JPEG_QUALITY", "85"))
        year_overlay = environ.get("YEAR_OVERLAY", "true").strip().lower() in {
            "1",
            "true",
            "yes",
            "on",
        }

        if not immich_base_url:
            raise ValueError("IMMICH_BASE_URL is required")
        if not immich_api_key:
            raise ValueError("IMMICH_API_KEY is required")
        if rotation_seconds <= 0:
            raise ValueError("ROTATION_SECONDS must be positive")
        if output_width <= 0 or output_height <= 0:
            raise ValueError("OUTPUT_WIDTH and OUTPUT_HEIGHT must be positive")

        return cls(
            immich_base_url=immich_base_url,
            immich_api_key=immich_api_key,
            timezone_name=timezone_name,
            rotation_seconds=rotation_seconds,
            output_width=output_width,
            output_height=output_height,
            jpeg_quality=jpeg_quality,
            year_overlay=year_overlay,
        )
