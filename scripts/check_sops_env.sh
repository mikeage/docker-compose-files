#!/usr/bin/env bash
set -euo pipefail

status=0

for file in "$@"; do
    case "$file" in
        doco-cd/.env)
            continue
            ;;
    esac

    if ! grep -q '^sops_version=' "$file"; then
        echo "SOPS check failed: $file is missing sops metadata (sops_version=...)." >&2
        status=1
        continue
    fi

    if ! grep -Fq 'ENC[' "$file"; then
        echo "SOPS check failed: $file does not appear to contain encrypted values." >&2
        status=1
    fi
done

exit "$status"
