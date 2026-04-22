# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "PyYAML>=6.0",
# ]
# ///

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
VAR_PATTERN = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)(?:(?::?[-+?])[^}]*)?\}")


def discover_compose_files() -> list[Path]:
    return sorted(ROOT.glob("**/compose.yaml")) + sorted(ROOT.glob("**/compose.yml"))


def placeholder_for(var_name: str) -> str:
    if var_name == "HOSTNAME":
        return "ci-host"
    if var_name.endswith("_PORT"):
        return "1234"
    if any(token in var_name for token in ("DIR", "FILE", "LOCATION", "PATH")):
        return "/tmp/ci"
    return "ci-placeholder"


def strip_env_files(compose_text: str) -> str:
    parsed = yaml.safe_load(compose_text)
    if not isinstance(parsed, dict):
        raise ValueError("compose file did not parse to a mapping")

    services = parsed.get("services", {})
    if isinstance(services, dict):
        for service in services.values():
            if isinstance(service, dict):
                service.pop("env_file", None)

    return yaml.safe_dump(parsed, sort_keys=False)


def build_env(compose_text: str) -> dict[str, str]:
    env = os.environ.copy()
    env.setdefault("COMPOSE_PROJECT_NAME", "ci")

    for var_name in sorted(set(VAR_PATTERN.findall(compose_text))):
        env.setdefault(var_name, placeholder_for(var_name))

    return env


def validate_compose_file(compose_file: Path) -> None:
    compose_text = compose_file.read_text()
    sanitized_compose = strip_env_files(compose_text)
    env = build_env(compose_text)

    with tempfile.NamedTemporaryFile(
        "w",
        suffix=".ci.compose.yaml",
        prefix=f"{compose_file.stem}.",
        dir=compose_file.parent,
        delete=False,
    ) as tmp_file:
        tmp_file.write(sanitized_compose)
        tmp_path = Path(tmp_file.name)

    try:
        subprocess.run(
            ["docker", "compose", "-f", tmp_path.name, "config", "-q"],
            cwd=compose_file.parent,
            env=env,
            check=True,
        )
    finally:
        tmp_path.unlink(missing_ok=True)

    print(f"validated {compose_file.relative_to(ROOT)}")


def main() -> int:
    compose_files = discover_compose_files()
    if not compose_files:
        print("no compose files found", file=sys.stderr)
        return 1

    for compose_file in compose_files:
        validate_compose_file(compose_file)

    print(f"validated {len(compose_files)} compose files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
