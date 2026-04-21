# CYD Immich Memories

This repo is the starting point for a two-part photo frame built around a `CYD` (`ESP32-2432S028R`) and an `Immich` server.

The current target firmware baseline is `ESPHome 2026.4.1`.

The intended design is:

1. A small Dockerized service runs in the homelab.
2. That service talks to Immich, selects `on this day` memories, fetches source images, and renders a final `320x240` frame for the display.
3. The CYD runs ESPHome and only fetches the already-rendered frame.

That split keeps Immich auth, image selection, resizing, cropping, and overlay logic off the ESP32.

## Why this shape

The current ESPHome docs make the tradeoffs fairly clear:

- `online_image` can download and decode images at runtime, but it only supports `BMP`, `JPEG` and `PNG`, and JPEG support is limited to baseline JPEGs.
- `online_image` requires a fair amount of RAM, and ESPHome explicitly warns that operation without PSRAM is not guaranteed.
- In `ESPHome 2026.4.1`, the safer display direction for this board class is `mipi_spi` rather than the older `ili9xxx` path.

For this project, the safest first version is to have the server do the expensive work and let the CYD act like a thin client.

On the common `WROOM`-based CYD without PSRAM, a full-screen `RGB565`
`online_image` frame can exceed available contiguous heap. The current ESPHome
config therefore keeps full color but fetches the rendered frame in `320x80`
JPEG slices and paints them onto the display one slice at a time.

## Repo Layout

- [docs/architecture.md](docs/architecture.md)
- [docs/service-api.md](docs/service-api.md)
- [docs/handoff.md](docs/handoff.md)
- [esphome/cyd-immich-memories.yaml.example](esphome/cyd-immich-memories.yaml.example)
- [compose.yaml](compose.yaml)

## Current Status

The repo now also contains the first runnable proxy service:

- `compose.yaml`
- `Dockerfile`
- `.env`
- Python app under `src/cyd_immich_proxy/`

Start with [docs/handoff.md](docs/handoff.md) if you open this repo in a fresh session and need the current state quickly.

The parts that still need your confirmation are:

- Final TLS details for the proxy hostname
- Whether you want to keep the common CYD pin mapping as-is
- Whether the `320x80` slice height is stable enough on your actual board

## Required Immich Permissions

For the current implementation, the API key should have:

- `memory.read`
- `asset.download`

The proxy currently fetches original image files from Immich and renders the `320x240` JPEG itself.

## Quick Start

1. Confirm `.env` contains the intended runtime values.
2. Start the proxy with `docker compose up -d --build`.
3. Point the CYD config at `https://cyd-immich-proxy.internal.mikeage.net`.
4. Add `asset.download` to the Immich API key permissions before first use.

## Primary References

- ESPHome `online_image`: <https://esphome.io/components/online_image/>
- ESPHome `http_request`: <https://esphome.io/components/http_request/>
- ESPHome `mipi_spi`: <https://esphome.io/components/display/mipi_spi/>
- ESPHome `ili9xxx`: <https://esphome.io/components/display/ili9xxx/>
- ESPHome `psram`: <https://esphome.io/components/psram/>
- Immich API index: <https://docs.immich.app/api/>
- Immich `searchMemories`: <https://immich.app/docs/api/search-memories>
- Immich `viewAsset`: <https://immich.app/docs/api/view-asset>
- Immich `downloadAsset`: <https://immich.app/docs/api/download-asset>
