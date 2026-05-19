from anomaly_pipeline.anomaly import control_limit_anomalies, zscore_anomalies


def test_control_limit_anomalies_flags_out_of_bounds_values():
    observations = {"A100": 100.0, "A200": 125.0, "A300": 10000.0}

    anomalies = control_limit_anomalies(observations, "daily_total", 0.0, 1000.0)

    assert len(anomalies) == 1
    assert anomalies[0].entity_id == "A300"
    assert anomalies[0].rule == "control_limit"


def test_zscore_anomalies_flags_extreme_observation():
    observations = {
        "A100": 100.0,
        "A200": 101.0,
        "A300": 102.0,
        "A400": 5000.0,
    }

    anomalies = zscore_anomalies(observations, "daily_total", threshold=1.5)

    assert len(anomalies) == 1
    assert anomalies[0].entity_id == "A400"
