#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")"

set -a
source ./.env
set +a

DOCO_TARGET="${DOCO_TARGET:-$(hostname)}"
API_SECRET="$(< /opt/doco-cd/secrets/api_secret)"

curl \
    --fail \
    --show-error \
    --silent \
    --request POST \
    --url 'http://127.0.0.1:8070/v1/api/poll/run?wait=true' \
    --header "content-type: application/json" \
    --header "x-api-key: ${API_SECRET}" \
    --data @- <<EOF
[
  {
    "url": "${REPO_URL}",
    "reference": "${REPO_REFERENCE}",
    "target": "${DOCO_TARGET}"
  }
]
EOF
