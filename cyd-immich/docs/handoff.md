# Handoff

This file is the shortest path for a new session to understand the repo state.

## What This Project Is

The project displays Immich `on this day` memories on a `CYD` (`ESP32-2432S028R`) using:

- an ESPHome device config for the CYD
- a small Dockerized Python proxy service

The proxy talks to Immich and renders a final `320x240` baseline JPEG. The CYD only downloads that already-rendered frame.

## Current Deployment Decisions

- Immich URL: `https://immich.mikeage.net`
- Proxy URL: `https://cyd-immich-proxy.internal.mikeage.net`
- Timezone: `Asia/Jerusalem`
- Rotation interval: `60s`
- Overlay: year only
- Asset rules: photos only
- Home Assistant may be used to control the ESPHome backlight entity
- Container orchestration: `docker compose`
- Compose file name: `compose.yaml`
- Secrets currently live in `.env`; the user plans to encrypt that with SOPS after moving repos

## Immich Permissions Required Right Now

The current proxy implementation uses:

- `memory.read`
- `asset.download`

`asset.download` is required because the proxy currently fetches original assets from Immich and resizes them server-side.

## Main Files

- [README.md](../README.md)
- [docs/architecture.md](architecture.md)
- [docs/service-api.md](service-api.md)
- [docs/handoff.md](handoff.md)
- [compose.yaml](../compose.yaml)
- [.env](../.env)
- [esphome/cyd-immich-memories.yaml.example](../esphome/cyd-immich-memories.yaml.example)
- [src/cyd_immich_proxy/main.py](../src/cyd_immich_proxy/main.py)
- [src/cyd_immich_proxy/immich.py](../src/cyd_immich_proxy/immich.py)
- [src/cyd_immich_proxy/config.py](../src/cyd_immich_proxy/config.py)

## What Already Works In The Scaffold

- FastAPI service with:
  - `GET /healthz`
  - `GET /api/v1/displays/{device_id}/current.jpg`
  - `GET /api/v1/displays/{device_id}/slice.jpg`
  - `GET /api/v1/displays/{device_id}/status`
- Daily memory lookup from Immich
- Filtering to `IMAGE` assets
- Downloading original assets
- Server-side cover-crop to `320x240`
- Server-side year overlay
- ETag / Last-Modified response headers
- ESPHome template using `mipi_spi` on `ESPHome 2026.4.1`
- Full-color slice-by-slice rendering for `WROOM` CYD hardware without PSRAM
- Home Assistant-driven backlight control via the exposed ESPHome light entity

## Open Assumptions / Things To Verify On Real Hardware

- Whether the CYD can validate the proxy TLS chain
  - If not, set `http_request.verify_ssl: false` in the ESPHome config
- Whether the common CYD pin mapping in the ESPHome example matches this exact board
- Whether the `320x80` full-color slice pipeline is stable enough on this device

## Known Environment Detail

Local verification succeeded for:

- Python import of the proxy under `uv run -p 3.12`
- YAML parse of the ESPHome config

No live Immich requests or real device compile/flash were performed yet.

## Most Likely Next Steps

1. Move this project to the target repo.
2. Encrypt `.env` with SOPS there.
3. Bring up the proxy with `docker compose up -d --build`.
4. Hit `/healthz` and `/status` manually.
5. Try the ESPHome config against the real CYD.
6. Watch the first slice refresh on-device and confirm it no longer tries to allocate a full `320x240` runtime image.
7. Fix any board-specific pin issues.
8. If the display struggles with HTTPS, relax SSL validation or switch to an internal HTTP endpoint.
