"""Reconciliation alert generation."""

from __future__ import annotations

from datetime import datetime, timezone

from anomaly_pipeline.anomaly import Anomaly
from anomaly_pipeline.validation import ValidationResult


def validation_alert(result: ValidationResult, severity: str = "HIGH") -> dict[str, object]:
    """Create a monitoring-friendly alert from a failed validation result."""
    return {
        "alert_type": "validation",
        "check_name": result.check_name,
        "severity": severity if result.status == "FAIL" else "INFO",
        "failed_count": result.failed_count,
        "details": result.details,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def anomaly_alert(anomaly: Anomaly, severity: str = "MEDIUM") -> dict[str, object]:
    """Create a monitoring-friendly alert from an anomaly record."""
    return {
        "alert_type": "anomaly",
        "entity_id": anomaly.entity_id,
        "metric_name": anomaly.metric_name,
        "metric_value": anomaly.metric_value,
        "score": anomaly.score,
        "rule": anomaly.rule,
        "severity": severity,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def should_page(alert: dict[str, object], failed_count_threshold: int = 10) -> bool:
    """Decide whether an alert should page based on severity and volume."""
    return (
        alert.get("severity") == "HIGH"
        and int(alert.get("failed_count", 0)) >= failed_count_threshold
    )
