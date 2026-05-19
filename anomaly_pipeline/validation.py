"""Data quality validation for transactional ELT pipelines."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class ValidationResult:
    check_name: str
    status: str
    failed_count: int
    details: str


def completeness_check(
    rows: list[dict[str, object]], required_columns: Iterable[str]
) -> ValidationResult:
    """Validate that required columns are non-null."""
    columns = list(required_columns)
    failed = [
        row for row in rows if any(row.get(column_name) in (None, "") for column_name in columns)
    ]
    return ValidationResult(
        check_name="completeness",
        status="PASS" if not failed else "FAIL",
        failed_count=len(failed),
        details=f"required_columns={','.join(columns)}",
    )


def type_consistency_check(
    rows: list[dict[str, object]],
    expected_types: dict[str, type],
) -> ValidationResult:
    """Validate Python-level types for local tests and pre-Spark checks."""
    failed_count = 0
    for row in rows:
        for column_name, expected_type in expected_types.items():
            value = row.get(column_name)
            if value is not None and not isinstance(value, expected_type):
                failed_count += 1
                break

    return ValidationResult(
        check_name="type_consistency",
        status="PASS" if failed_count == 0 else "FAIL",
        failed_count=failed_count,
        details=f"checked_columns={','.join(expected_types)}",
    )


def referential_integrity_check(
    child_rows: list[dict[str, object]],
    parent_rows: list[dict[str, object]],
    child_key: str,
    parent_key: str,
) -> ValidationResult:
    """Validate that all child keys exist in the parent dataset."""
    parent_values = {row[parent_key] for row in parent_rows}
    failed = [row for row in child_rows if row.get(child_key) not in parent_values]
    return ValidationResult(
        check_name="referential_integrity",
        status="PASS" if not failed else "FAIL",
        failed_count=len(failed),
        details=f"{child_key}->{parent_key}",
    )


def partition_check(
    rows: list[dict[str, object]], partition_columns: Iterable[str]
) -> ValidationResult:
    """Validate that partition columns are present and populated."""
    columns = list(partition_columns)
    failed = [
        row
        for row in rows
        if any(column_name not in row or row[column_name] in (None, "") for column_name in columns)
    ]
    return ValidationResult(
        check_name="partition_check",
        status="PASS" if not failed else "FAIL",
        failed_count=len(failed),
        details=f"partition_columns={','.join(columns)}",
    )
