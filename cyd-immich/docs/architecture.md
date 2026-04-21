# Architecture

## Goal

Build a `CYD` wall or desk display that rotates through Immich `on this day` memories with minimal logic on the ESP32.

This design is being aimed at `ESPHome 2026.4.1`.

## Working Assumptions

- The display hardware is a `ESP32-2432S028R` / CYD class board with a `320x240` TFT.
- The board family is based on the classic `ESP32-WROOM` according to the Makerfabs Sunton page, so memory is materially tighter than on newer `ESP32-S3 + PSRAM` display boards.
- The display should not talk to Immich directly.
- A separate service running in Docker is acceptable.

## Constraints Confirmed From Current Docs

## ESPHome image path

- `online_image` downloads and decodes images at runtime.
- Supported formats are `BMP`, `JPEG`, and `PNG`.
- JPEG support is baseline-only.
- ESPHome warns that `online_image` needs a fair amount of RAM and may not be reliable without PSRAM.
- `online_image` supports HTTP caching via `ETag` and `Last-Modified`.

## ESPHome display path

- `ili9xxx` still supports `ILI9341`, but the docs say it has been made redundant by `mipi_spi` and may be removed in a future release.
- For a new config on `ESPHome 2026.4.1`, `mipi_spi` should be treated as the baseline driver.

## Immich API path

- Immich exposes a `searchMemories` endpoint with `type=on_this_day`.
- That endpoint requires the `memory.read` permission.
- Immich also exposes asset-view and asset-download endpoints that can supply image content to the proxy service.

## Recommended System Shape

## 1. Server-side service

The service should own:

- Immich authentication
- Daily memory lookup
- Asset filtering
- Orientation-aware crop/fit decisions
- Downscaling to `320x240`
- Text overlay rendering
- HTTP cache headers for the device

The device should never need to know Immich asset IDs or hold an Immich API key.

## 2. Device-side ESPHome

The CYD should own:

- Wi-Fi connectivity
- Display init
- Polling a single JPEG endpoint
- Rendering the downloaded image
- Home Assistant can control the exposed ESPHome backlight light entity

That keeps the firmware simple and lowers the risk that image decode or JSON parsing becomes the unstable part of the system.

## Data Flow

1. At startup, the service asks Immich for `on_this_day` memories for the current date.
2. The service extracts candidate image assets and ignores unsupported items such as videos in the first version.
3. The service fetches the original asset from Immich.
4. The service renders a final `320x240` baseline JPEG for the CYD.
5. The CYD fetches either `current.jpg` or smaller rendered `slice.jpg` segments with `online_image`.
6. When the service rotates to the next memory, it returns a new `ETag` so ESPHome refreshes its cache.

## Why Server-Rendered Frames Are The Best First Version

This project could be built in two broad ways.

## Option A: device fetches metadata plus raw image

Pros:

- More flexibility on-device

Cons:

- More HTTP requests from the ESP32
- More parsing and state on the ESP32
- More RAM pressure
- More room for display-specific bugs

## Option B: device fetches one already-rendered JPEG

Pros:

- Simplest ESPHome config
- Best fit for constrained RAM
- Server controls crop, typography, and fallback behavior
- Easy to cache and debug

Cons:

- Overlay layout lives on the server
- Interactive UI later will need a slightly richer contract

For the first cut, `Option B` is the pragmatic choice.

## Rendering Rules I’d Start With

- Target output: `320x240`
- Format: baseline `JPEG`
- Keep one frame in landscape orientation only
- Use cover-crop rather than letterboxing by default
- Burn a small footer or header with:
  - month/day
  - original year
  - optional city or album hint
- Filter out:
  - videos
  - motion photos
  - assets without usable preview/download path
- Prefer image assets that are already roughly landscape when multiple candidates exist

## Service Responsibilities In More Detail

## Daily cache

The service should cache the day’s memory list so it does not hit Immich on every display poll.

Suggested behavior:

- Refresh the memory list at midnight local time.
- Keep a shorter retry interval if the list fetch fails.
- Preserve the last good rendered frame if Immich is temporarily unavailable.

## Rotation

The service should own rotation timing so multiple displays can stay consistent if desired.

Suggested behavior:

- Global default: `30s` per frame
- Deterministic rotation based on wall clock time rather than per-request random choice

For your current target, the first implementation uses `60s` rotation.

That lets the device keep polling a stable endpoint like `current.jpg`.

## Caching

The service should return:

- `ETag`
- `Last-Modified`
- `Cache-Control: no-cache`

That matches ESPHome’s documented HTTP caching support and avoids downloading unchanged frames unnecessarily.

## Risks

## 1. CYD memory headroom

The biggest technical risk is that runtime image fetch/decode on the CYD may still be tight even with server-rendered images. If that happens, the first levers to pull are:

- use exact-size `320x240` server output
- keep `online_image` at `RGB565`
- fetch the frame as smaller vertical slices rather than a single full-screen image
- reduce `buffer_size`
- keep only a single active image in memory

On the current `ESP32-WROOM` CYD baseline, the chosen workaround is to keep
full color and have the proxy expose rendered `320x80` slices. The device then
downloads, paints, and releases each slice in sequence instead of allocating a
single `320x240` runtime image.

If that still proves flaky, the fallback is leaving ESPHome and using a small custom firmware with tighter control over buffers.

## 2. Immich API churn

Immich changes quickly. The official docs explicitly note active development. The service should isolate all Immich-specific logic behind a small client layer so API changes do not affect the ESPHome side.

## 3. Board-to-board CYD variation

Pin mappings and small hardware details can vary. The current ESPHome example is intentionally a template until we confirm your exact board’s working pins.

## Milestones

1. Confirm the exact CYD pin mapping and test-card config.
2. Bring up a static JPEG from a tiny local web service.
3. Implement the Docker service with a placeholder frame.
4. Add Immich memory lookup.
5. Add server-side rendering and cropping.
