from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time
from typing import Any
from zoneinfo import ZoneInfo

import httpx

from cyd_immich_proxy.config import Settings


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


@dataclass(frozen=True)
class MemoryAsset:
    asset_id: str
    year: int | None
    captured_at: datetime | None
    city: str | None
    country: str | None
    original_file_name: str | None

    @property
    def place_label(self) -> str | None:
        if self.city and self.country:
            return f"{self.city}, {self.country}"
        return self.city or self.country


class ImmichClient:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._client = httpx.AsyncClient(
            base_url=settings.immich_base_url,
            headers={"x-api-key": settings.immich_api_key},
            follow_redirects=True,
            timeout=30.0,
        )
        self._timezone = ZoneInfo(settings.timezone_name)

    async def close(self) -> None:
        await self._client.aclose()

    async def fetch_memory_assets(self, target_date: date) -> list[MemoryAsset]:
        query_time = datetime.combine(target_date, time.min, tzinfo=self._timezone)
        response = await self._client.get(
            "/api/memories",
            params={
                "type": "on_this_day",
                "for": query_time.isoformat(),
            },
        )
        response.raise_for_status()

        payload = response.json()
        assets: list[MemoryAsset] = []
        seen: set[str] = set()
        for memory in payload:
            for asset_payload in memory.get("assets", []):
                asset = self._parse_asset(asset_payload)
                if asset is None or asset.asset_id in seen:
                    continue
                seen.add(asset.asset_id)
                assets.append(asset)
        return assets

    async def download_original(self, asset_id: str) -> bytes:
        response = await self._client.get(f"/api/assets/{asset_id}/original")
        response.raise_for_status()
        return response.content

    def _parse_asset(self, payload: dict[str, Any]) -> MemoryAsset | None:
        if payload.get("type") != "IMAGE":
            return None

        asset_id = payload.get("id")
        if not asset_id:
            return None

        captured_at = (
            _parse_datetime(payload.get("localDateTime"))
            or _parse_datetime(payload.get("dateTimeOriginal"))
            or _parse_datetime(payload.get("fileCreatedAt"))
            or _parse_datetime(payload.get("createdAt"))
        )
        year = captured_at.year if captured_at else None

        city = payload.get("city")
        country = payload.get("country")
        original_file_name = payload.get("originalFileName")

        exif_info = payload.get("exifInfo")
        if isinstance(exif_info, dict):
            city = city or exif_info.get("city")
            country = country or exif_info.get("country")

        return MemoryAsset(
            asset_id=asset_id,
            year=year,
            captured_at=captured_at,
            city=city,
            country=country,
            original_file_name=original_file_name,
        )
