"""Statistical process control anomaly detection."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, pstdev


@dataclass(frozen=True)
class Anomaly:
    entity_id: str
    metric_name: str
    metric_value: float
    score: float
    rule: str


def zscore_anomalies(
    observations: dict[str, float],
    metric_name: str,
    threshold: float = 3.0,
) -> list[Anomaly]:
    """Flag observations whose z-score exceeds the threshold."""
    values = list(observations.values())
    if len(values) < 2:
        return []

    avg = mean(values)
    stddev = pstdev(values)
    if stddev == 0:
        return []

    anomalies: list[Anomaly] = []
    for entity_id, value in observations.items():
        score = abs((value - avg) / stddev)
        if score >= threshold:
            anomalies.append(
                Anomaly(
                    entity_id=entity_id,
                    metric_name=metric_name,
                    metric_value=value,
                    score=round(score, 4),
                    rule="zscore",
                )
            )
    return anomalies


def control_limit_anomalies(
    observations: dict[str, float],
    metric_name: str,
    lower_limit: float,
    upper_limit: float,
) -> list[Anomaly]:
    """Flag observations outside configured control limits."""
    anomalies = []
    for entity_id, value in observations.items():
        if value < lower_limit or value > upper_limit:
            distance = min(abs(value - lower_limit), abs(value - upper_limit))
            anomalies.append(
                Anomaly(
                    entity_id=entity_id,
                    metric_name=metric_name,
                    metric_value=value,
                    score=round(distance, 4),
                    rule="control_limit",
                )
            )
    return anomalies
