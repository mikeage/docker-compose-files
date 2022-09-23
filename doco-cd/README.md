# doco-cd

This stack runs `doco-cd` in polling mode against this repository over SSH.

## Setup

1. Create the host-local bootstrap secret directory:

```bash
mkdir -p /opt/doco-cd/secrets
chmod 700 /opt/doco-cd/secrets
```

2. Put the repo deploy SSH private key at:

```text
/opt/doco-cd/secrets/id_ed25519_doco
```

3. Put the API secret at:

```text
/opt/doco-cd/secrets/api_secret
```

4. Put the Apprise notify URL at:

```text
/opt/doco-cd/secrets/apprise_notify_urls
```

Example content:

```text
mailtos://mikeage.net:2525?user=outgoing&pass=...&smtp=outbound.mikeage.net&from=dococd@mikeage.net&to=dococd-${DOCO_TARGET}@mikeage.net
```

5. Put the SOPS age private key at:

```text
/opt/doco-cd/secrets/sops_age_key.txt
```

6. Use the shared committed `.env` file for the non-secret settings.
7. Set `DOCO_TARGET` when starting the stack on each host.

## Recommended usage

Use the same [compose.yaml](/Users/mikemi/src/docker-compose-files/doco-cd/compose.yaml) and shared [doco-cd/.env](/Users/mikemi/src/docker-compose-files/doco-cd/.env) on all three nodes, and select the host target at runtime: `DOCO_TARGET=$(hostname) docker compose up -d`

This keeps one `doco-cd` stack definition and one shared committed non-secret env file, while keeping bootstrap secrets out of git.

To trigger an immediate poll without waiting for the next interval:

```bash
./poll-now.sh
```

## Notes

- `POLL_INTERVAL` is in seconds. The current value `300` means Git is polled every 5 minutes.
- The `doco-cd` API is enabled with `API_SECRET_FILE` and bound only to `127.0.0.1:8080`.
- Email notifications are sent through the bundled `apprise` sidecar using `APPRISE_NOTIFY_URLS_FILE`.
- SOPS decryption is enabled with `SOPS_AGE_KEY_FILE=/run/secrets/sops_age_key`.
- `APPRISE_NOTIFY_LEVEL=info` means you also get start/in-progress notifications.
- `DOCO_TARGET` must be set in the shell when you run `docker compose`, because it is intentionally not stored in `.env`.
- `DOCO_TARGET` selects one of the repo root deployment files:
  - `.doco-cd.g4-gpu.yaml`
  - `.doco-cd.openmediavault.yaml`
  - `.doco-cd.vm1.yaml`
- No webhook is exposed here. This is polling-only.
- The repo URL is set to the SSH form because this repo is private and you already have a deploy key.
- `/opt/doco-cd/data:/data` is a persistent bind mount for `doco-cd` state on the host.
