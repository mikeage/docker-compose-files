#!/bin/bash
set -euo pipefail

RCFILE="${RCFILE:-/config/getmailrc}"
INTERVAL="${INTERVAL:-300}"
GETMAILDIR="${GETMAILDIR:-/state/getmaildir}"

mkdir -p "${GETMAILDIR}"

_term() {
  echo "getmail: received stop signal, exiting..."
  exit 0
}

trap _term TERM INT

echo "getmail: starting loop with rcfile=${RCFILE} getmaildir=${GETMAILDIR} interval=${INTERVAL}s"

while true; do
  /usr/bin/getmail --getmaildir "${GETMAILDIR}" --rcfile "${RCFILE}" \
    || echo "getmail: run failed (will retry)"

  # sleep in 1s increments so SIGTERM is handled immediately
  for ((i=0; i<INTERVAL; i++)); do
    sleep 1
  done
done
