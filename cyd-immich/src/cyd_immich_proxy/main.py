from __future__ import annotations

import asyncio
import hashlib
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import UTC, date, datetime
from io import BytesIO
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from PIL import Image, ImageDraw, ImageFont, ImageOps, UnidentifiedImageError
from pillow_heif import register_heif_opener

from cyd_immich_proxy.config import Settings
from cyd_immich_proxy.immich import ImmichClient, MemoryAsset

register_heif_opener()

FONT_CANDIDATES = (
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    Path("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf"),
)


@dataclass(frozen=True)
class Frame:
    body: bytes
    etag: str
    last_modified: str
    metadata: dict[str, Any]


@dataclass
class DailyMemoryState:
    date_key: str
    assets: list[MemoryAsset]


class ProxyService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._timezone = ZoneInfo(settings.timezone_name)
        self._immich = ImmichClient(settings)
        self._lock = asyncio.Lock()
        self._daily_state: DailyMemoryState | None = None
        self._frame_cache: dict[str, Frame] = {}
        self._frame_slice_cache: dict[tuple[str, int, int], Frame] = {}

    async def close(self) -> None:
        await self._immich.close()

    async def get_current_frame(self, device_id: str) -> Frame:
        now_local = datetime.now(self._timezone)
        state = await self._get_daily_state(now_local.date())

        if not state.assets:
            return self._render_placeholder(
                title="No memories today",
                subtitle=now_local.strftime("%b %d"),
            )

        selected_index = await self._get_selected_index(state, now_local)
        for attempt in range(len(state.assets)):
            asset = state.assets[(selected_index + attempt) % len(state.assets)]
            cached = self._frame_cache.get(asset.asset_id)
            if cached is not None:
                return cached

            try:
                source_bytes = await self._immich.download_original(asset.asset_id)
                frame = self._render_asset(asset, source_bytes)
            except Exception:
                continue

            self._frame_cache[asset.asset_id] = frame
            return frame

        return self._render_placeholder(
            title="Unable to render memories",
            subtitle=now_local.strftime("%b %d"),
        )

    async def get_status(self, device_id: str) -> dict[str, Any]:
        frame = await self.get_current_frame(device_id)
        return {
            "device_id": device_id,
            "timezone": self.settings.timezone_name,
            "rotation_seconds": self.settings.rotation_seconds,
            "etag": frame.etag,
            **frame.metadata,
        }

    async def get_current_frame_slice(
        self,
        device_id: str,
        top: int,
        height: int,
    ) -> Frame:
        if top < 0:
            raise ValueError("top must be non-negative")
        if height <= 0:
            raise ValueError("height must be positive")
        if top >= self.settings.output_height:
            raise ValueError("top must be inside the frame height")

        frame = await self.get_current_frame(device_id)
        slice_height = min(height, self.settings.output_height - top)
        if top == 0 and slice_height == self.settings.output_height:
            return frame

        cache_key = (frame.etag, top, slice_height)
        cached = self._frame_slice_cache.get(cache_key)
        if cached is not None:
            return cached

        with Image.open(BytesIO(frame.body)) as image:
            image = image.convert("RGB")
            slice_image = image.crop(
                (0, top, self.settings.output_width, top + slice_height)
            )

        buffer = BytesIO()
        slice_image.save(
            buffer,
            format="JPEG",
            quality=self.settings.jpeg_quality,
            optimize=True,
            progressive=False,
        )
        body = buffer.getvalue()
        slice_frame = Frame(
            body=body,
            etag=f"\"{hashlib.sha1(body).hexdigest()}\"",
            last_modified=frame.last_modified,
            metadata={
                **frame.metadata,
                "image_height": slice_height,
                "slice_top": top,
            },
        )
        self._frame_slice_cache[cache_key] = slice_frame
        return slice_frame

    async def _get_daily_state(self, today: date) -> DailyMemoryState:
        date_key = today.isoformat()
        async with self._lock:
            if self._daily_state and self._daily_state.date_key == date_key:
                return self._daily_state

        assets = await self._immich.fetch_memory_assets(today)
        new_state = DailyMemoryState(date_key=date_key, assets=assets)
        async with self._lock:
            if self._daily_state is None or self._daily_state.date_key != date_key:
                self._daily_state = new_state
                self._frame_cache.clear()
                self._frame_slice_cache.clear()
            return self._daily_state

    async def _get_selected_index(
        self,
        state: DailyMemoryState,
        now_local: datetime,
    ) -> int:
        seconds_since_midnight = (
            now_local.hour * 3600 + now_local.minute * 60 + now_local.second
        )
        rotation_slot = seconds_since_midnight // self.settings.rotation_seconds
        return rotation_slot % len(state.assets)

    def _render_asset(self, asset: MemoryAsset, source_bytes: bytes) -> Frame:
        try:
            with Image.open(BytesIO(source_bytes)) as image:
                image = ImageOps.exif_transpose(image)
                image = image.convert("RGB")
                frame_image = self._cover_crop(
                    image, self.settings.output_width, self.settings.output_height
                )
        except (UnidentifiedImageError, OSError) as exc:
            raise ValueError(f"Unsupported image for asset {asset.asset_id}") from exc

        if self.settings.year_overlay and asset.year:
            self._draw_year_overlay(frame_image, str(asset.year))

        buffer = BytesIO()
        frame_image.save(
            buffer,
            format="JPEG",
            quality=self.settings.jpeg_quality,
            optimize=True,
            progressive=False,
        )
        body = buffer.getvalue()
        etag = f"\"{hashlib.sha1(body).hexdigest()}\""
        last_modified = self._last_modified_from_asset(asset)
        return Frame(
            body=body,
            etag=etag,
            last_modified=last_modified,
            metadata={
                "source": "immich",
                "date": datetime.now(self._timezone).date().isoformat(),
                "memory_type": "on_this_day",
                "asset_id": asset.asset_id,
                "year": asset.year,
                "place": asset.place_label,
                "original_file_name": asset.original_file_name,
                "image_width": self.settings.output_width,
                "image_height": self.settings.output_height,
            },
        )

    def _render_placeholder(self, title: str, subtitle: str | None) -> Frame:
        image = Image.new(
            "RGB",
            (self.settings.output_width, self.settings.output_height),
            color=(18, 22, 29),
        )
        draw = ImageDraw.Draw(image)
        title_font = self._load_font(24)
        subtitle_font = self._load_font(16)

        title_box = draw.textbbox((0, 0), title, font=title_font)
        title_x = (self.settings.output_width - (title_box[2] - title_box[0])) // 2
        title_y = self.settings.output_height // 2 - 24
        draw.text((title_x, title_y), title, fill=(240, 240, 240), font=title_font)

        if subtitle:
            subtitle_box = draw.textbbox((0, 0), subtitle, font=subtitle_font)
            subtitle_x = (
                self.settings.output_width - (subtitle_box[2] - subtitle_box[0])
            ) // 2
            draw.text(
                (subtitle_x, title_y + 34),
                subtitle,
                fill=(176, 184, 194),
                font=subtitle_font,
            )

        buffer = BytesIO()
        image.save(
            buffer,
            format="JPEG",
            quality=self.settings.jpeg_quality,
            optimize=True,
            progressive=False,
        )
        body = buffer.getvalue()
        etag = f"\"{hashlib.sha1(body).hexdigest()}\""
        now_http = datetime.now(UTC).strftime("%a, %d %b %Y %H:%M:%S GMT")
        return Frame(
            body=body,
            etag=etag,
            last_modified=now_http,
            metadata={
                "source": "placeholder",
                "date": datetime.now(self._timezone).date().isoformat(),
                "memory_type": "on_this_day",
                "asset_id": None,
                "year": None,
                "place": None,
                "original_file_name": None,
                "image_width": self.settings.output_width,
                "image_height": self.settings.output_height,
            },
        )

    def _cover_crop(self, image: Image.Image, width: int, height: int) -> Image.Image:
        src_w, src_h = image.size
        scale = max(width / src_w, height / src_h)
        resized = image.resize(
            (max(1, round(src_w * scale)), max(1, round(src_h * scale))),
            Image.Resampling.LANCZOS,
        )

        left = max(0, (resized.width - width) // 2)
        top = max(0, (resized.height - height) // 2)
        return resized.crop((left, top, left + width, top + height))

    def _draw_year_overlay(self, image: Image.Image, year_text: str) -> None:
        draw = ImageDraw.Draw(image, "RGBA")
        font = self._load_font(28)
        text_box = draw.textbbox((0, 0), year_text, font=font)
        text_width = text_box[2] - text_box[0]
        text_height = text_box[3] - text_box[1]

        padding_x = 14
        padding_y = 8
        margin = 12
        box_left = image.width - text_width - padding_x * 2 - margin
        box_top = margin
        box_right = image.width - margin
        box_bottom = box_top + text_height + padding_y * 2

        draw.rounded_rectangle(
            (box_left, box_top, box_right, box_bottom),
            radius=12,
            fill=(18, 22, 29, 180),
        )
        draw.text(
            (box_left + padding_x, box_top + padding_y - text_box[1]),
            year_text,
            font=font,
            fill=(255, 255, 255, 255),
        )

    def _load_font(self, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
        for candidate in FONT_CANDIDATES:
            if candidate.exists():
                return ImageFont.truetype(str(candidate), size=size)
        return ImageFont.load_default()

    def _last_modified_from_asset(self, asset: MemoryAsset) -> str:
        source_time = asset.captured_at or datetime.now(UTC)
        if source_time.tzinfo is None:
            source_time = source_time.replace(tzinfo=self._timezone)
        return source_time.astimezone(UTC).strftime("%a, %d %b %Y %H:%M:%S GMT")


def _response_headers(frame: Frame) -> dict[str, str]:
    return {
        "Cache-Control": "no-cache",
        "ETag": frame.etag,
        "Last-Modified": frame.last_modified,
    }


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings.from_env()
    service = ProxyService(settings)
    app.state.service = service
    yield
    await service.close()


app = FastAPI(
    title="CYD Immich Proxy",
    version="0.1.0",
    lifespan=lifespan,
)


def _service(request: Request) -> ProxyService:
    return request.app.state.service


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/v1/displays/{device_id}/current.jpg")
async def current_image(device_id: str, request: Request) -> Response:
    service = _service(request)
    frame = await service.get_current_frame(device_id)
    if request.headers.get("if-none-match") == frame.etag:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED, headers=_response_headers(frame))
    return Response(
        content=frame.body,
        media_type="image/jpeg",
        headers=_response_headers(frame),
    )


@app.get("/api/v1/displays/{device_id}/slice.jpg")
async def current_image_slice(
    device_id: str,
    request: Request,
    top: int,
    height: int,
) -> Response:
    service = _service(request)
    try:
        frame = await service.get_current_frame_slice(device_id, top=top, height=height)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if request.headers.get("if-none-match") == frame.etag:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED, headers=_response_headers(frame))
    return Response(
        content=frame.body,
        media_type="image/jpeg",
        headers=_response_headers(frame),
    )


@app.get("/api/v1/displays/{device_id}/status")
async def status_endpoint(device_id: str, request: Request) -> JSONResponse:
    service = _service(request)
    return JSONResponse(await service.get_status(device_id))

