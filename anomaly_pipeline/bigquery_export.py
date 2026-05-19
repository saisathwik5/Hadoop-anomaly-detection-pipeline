"""BigQuery export helpers."""

from __future__ import annotations

from pathlib import Path


def build_load_config(
    table: str, source_uri: str, source_format: str = "PARQUET"
) -> dict[str, str]:
    """Return a serializable load-job config for tests and dry runs."""
    return {
        "table": table,
        "source_uri": source_uri,
        "source_format": source_format,
        "write_disposition": "WRITE_APPEND",
    }


def write_dry_run_manifest(config: dict[str, str], output_path: str | Path) -> None:
    """Write a local manifest that documents the intended BigQuery load."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"{key}={value}" for key, value in sorted(config.items())]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
