# CYD Monitor Session Notes

Last updated: 2026-04-20
Repo: `/Users/mikemi/src/cyd-monitor`
Primary config: `cyd-monitor.yaml`

## Current Goal
ESP32 CYD dashboard for 5 Linux hosts with robust behavior under temporary network failures.

## User Preferences
- User compiles/uploads manually.
- Assistant should run `esphome config` and `esphome logs` only (no `esphome run`).
- Keep landscape orientation and mirrored setting as currently configured.
- Keep simple, distance-readable UI.

## Current Display Behavior
- Text-only (graphs removed for stability).
- 3-column x 2-row card grid:
  - `vm1` (`vm1.lan`)
  - `g4-gpu` (`g4-gpu.lan`)
  - `omv` (`openmediavault.lan`)
  - `u59` (`u59-proxmox.lan`)
  - `g4-prox` (`g4-proxmox.lan`)
- sixth tile intentionally unused
- Shows `C:` and `L:`.
- Shows `C:XXX` / `L:XXX` after `3` consecutive poll failures.
- Top bar is a 60-second heartbeat ticker (independent of poll timing).
- Active poll indicator is a thick blue frame around the whole host tile.
- No separate status block / legend tile.

## Current Polling/Network Settings
- Poll slot: every `2s`, round-robin (one host per slot).
- Effective per-host cadence: ~10s.
- HTTP timeout: `600ms`.
- Display driver migrated for ESPHome 2026.4.x:
  - `platform: mipi_spi`
  - `model: ESP32-2432S028`
  - `color_depth: 8`
  - `data_rate: 20MHz`
  - `spi` display bus uses only `clk_pin` and `mosi_pin`
- `esp32.cpu_frequency` pinned to `160MHZ` during 2026.4.x migration testing.
- `esp32.framework.advanced` now includes:
  - `minimum_chip_revision: "3.1"`
  - `sram1_as_iram: true`
- Hostnames:
  - `openmediavault.lan`
  - `vm1.lan`
  - `g4-gpu.lan`
  - `u59-proxmox.lan`
  - `g4-proxmox.lan`
- Request header includes `Connection: close`.
- Wi-Fi tweaks:
  - `power_save_mode: NONE`
  - `fast_connect: true`

## Known Runtime Observations
- Repeated transient HTTP failures still occur:
  - `HTTP Request failed ... Code: -1`
  - `ESP_ERR_HTTP_CONNECT`
  - `esp-tls ... select() timeout`
- Recent soak slices showed failures but no immediate watchdog reset in that window.
- Earlier sessions did hit watchdog resets during heavier rendering/network blocking.

## Useful Commands
- Validate config:
  - `esphome config cyd-monitor.yaml`
- Follow logs over API:
  - `esphome logs cyd-monitor.yaml --device cyd-monitor.lan`
- Follow logs over serial:
  - `esphome logs cyd-monitor.yaml --device /dev/cu.usbserial-10`

## Next Debug Steps (if failures persist)
1. Run long soak logs (30+ min) and count:
   - `ESP_ERR_HTTP_CONNECT`
   - `Code: -1`
   - any `task_wdt` or reboot lines.
2. If still noisy, test one change at a time:
   - increase timeout slightly (e.g. `800ms`)
   - poll slot from `2s` to `3s`
   - temporarily force fixed IPs instead of `.lan` hostnames.
3. Keep failure threshold at `3` unless user requests otherwise.
