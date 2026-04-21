# Service API

This is the proposed device-facing contract for the homelab service.

The key design choice is that the CYD should fetch a fully rendered frame, not raw Immich assets plus metadata.

## Public Device Endpoints

## `GET /api/v1/displays/{device_id}/current.jpg`

Returns the current frame for the given display profile.

Response:

- `200 OK`
- `Content-Type: image/jpeg`
- Body: baseline JPEG, already rendered to the target display size

Expected headers:

- `ETag`
- `Last-Modified`
- `Cache-Control: no-cache`

Notes:

- The service owns frame rotation.
- The same URL remains stable while the content changes over time.
- ESPHome can use HTTP cache validation instead of downloading a new body every time.

## `GET /api/v1/displays/{device_id}/slice.jpg?top={top}&height={height}`

Returns a vertically cropped slice of the current rendered frame.

Response:

- `200 OK`
- `Content-Type: image/jpeg`
- Body: baseline JPEG for the requested slice

Expected headers:

- `ETag`
- `Last-Modified`
- `Cache-Control: no-cache`

Notes:

- This exists for non-PSRAM `ESP32-WROOM` CYD boards that cannot reliably hold a
  full `320x240 RGB565` runtime image in RAM.
- The proxy still owns all cropping and rendering; the device only requests a
  smaller already-rendered piece of the current frame.
- `top` must be inside the frame and `height` must be positive.

## `GET /api/v1/displays/{device_id}/status`

Returns debug metadata for the currently selected frame.

Example response:

```json
{
  "device_id": "cyd-living-room",
  "date": "2026-04-21",
  "rotation_seconds": 60,
  "memory_type": "on_this_day",
  "asset_id": "immich-asset-id",
  "year": 2019,
  "place": "Jerusalem",
  "source": "immich",
  "image_width": 320,
  "image_height": 240,
  "etag": "\"f6c1f5f5\""
}
```

This endpoint is for debugging and future UI expansion. The first ESPHome version does not need to call it.

## Suggested Service Configuration

Environment variables:

- `IMMICH_BASE_URL`
- `IMMICH_API_KEY`
- `TIMEZONE`
- `ROTATION_SECONDS`
- `OUTPUT_WIDTH`
- `OUTPUT_HEIGHT`
- `JPEG_QUALITY`
- `YEAR_OVERLAY`

Optional per-device settings:

- output size
- overlay enabled/disabled
- crop mode
- rotation interval
- timezone override

## Internal Immich Responsibilities

The public service contract above should hide all Immich-specific details. Internally, the service will need to:

- search Immich memories for `type=on_this_day`
- extract candidate `IMAGE` assets
- fetch the original asset
- render the final frame

That indirection is deliberate. It lets the ESPHome side stay stable even if Immich endpoint details change.

## Rendering Contract

The server should return frames that already satisfy the device constraints:

- exact output size: `320x240`
- baseline `JPEG`
- optional server-side text overlay
- visually safe crop for portrait or landscape source images

For low-memory clients, the server may additionally expose pre-cropped vertical
slices from that same rendered frame.

The CYD should never need to resize, crop, or compose images on its own.

## Required Immich Permissions

The current implementation uses:

- `memory.read`
- `asset.download`

`asset.download` is needed because the proxy fetches `/api/assets/{id}/original` and does the final resize itself.
