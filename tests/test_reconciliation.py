from anomaly_pipeline.anomaly import Anomaly
from anomaly_pipeline.reconciliation import anomaly_alert, should_page, validation_alert
from anomaly_pipeline.validation import ValidationResult


def test_validation_alert_escalates_failed_check():
    result = ValidationResult("referential_integrity", "FAIL", 12, "account_id->account_id")

    alert = validation_alert(result)

    assert alert["severity"] == "HIGH"
    assert should_page(alert, failed_count_threshold=10) is True


def test_anomaly_alert_contains_metric_context():
    anomaly = Anomaly("A100", "daily_total", 12000.0, 4.2, "zscore")

    alert = anomaly_alert(anomaly)

    assert alert["alert_type"] == "anomaly"
    assert alert["metric_name"] == "daily_total"
    assert alert["score"] == 4.2
