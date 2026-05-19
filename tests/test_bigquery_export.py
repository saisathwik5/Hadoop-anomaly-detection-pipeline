from anomaly_pipeline.bigquery_export import build_load_config, write_dry_run_manifest


def test_build_load_config_defaults_to_parquet_append():
    config = build_load_config("project.dataset.table", "gs://bucket/path/*.parquet")

    assert config["source_format"] == "PARQUET"
    assert config["write_disposition"] == "WRITE_APPEND"


def test_write_dry_run_manifest(tmp_path):
    config = build_load_config("project.dataset.table", "gs://bucket/path/*.parquet")
    manifest = tmp_path / "manifest.txt"

    write_dry_run_manifest(config, manifest)

    assert "table=project.dataset.table" in manifest.read_text(encoding="utf-8")
