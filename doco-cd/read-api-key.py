# /// script
# requires-python = ">=3.10"
# dependencies = ["PyYAML>=6.0,<7"]
# ///
"""Read the first API key from doco-cd's plaintext YAML key list."""

import sys
from pathlib import Path

import yaml


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("Usage: read-api-key.py API_KEYS_FILE")

    try:
        keys = yaml.safe_load(Path(sys.argv[1]).read_text())
    except (OSError, UnicodeError, yaml.YAMLError):
        # YAML parser errors can include secret values, so keep the message generic.
        sys.exit("Could not read API keys: expected a readable plaintext YAML file")

    if not isinstance(keys, list) or not keys or not isinstance(keys[0], dict):
        sys.exit("API keys file must contain a nonempty list of key entries")

    key = keys[0].get("key")
    if not isinstance(key, str) or not key or key != key.strip() or any(
        ord(char) < 32 or ord(char) == 127 for char in key
    ):
        sys.exit("The first API key must be a nonempty, valid HTTP header value")

    print(key)


if __name__ == "__main__":
    main()
