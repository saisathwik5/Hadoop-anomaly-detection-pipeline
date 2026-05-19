from anomaly_pipeline.validation import (
    completeness_check,
    partition_check,
    referential_integrity_check,
    type_consistency_check,
)


def test_completeness_check_flags_missing_required_values():
    rows = [
        {"transaction_id": "T1", "account_id": "A1"},
        {"transaction_id": "", "account_id": "A2"},
    ]

    result = completeness_check(rows, ["transaction_id", "account_id"])

    assert result.status == "FAIL"
    assert result.failed_count == 1


def test_type_consistency_check_passes_expected_types():
    rows = [{"amount": 10.0}, {"amount": 11.5}]

    result = type_consistency_check(rows, {"amount": float})

    assert result.status == "PASS"


def test_referential_integrity_check_finds_orphan_keys():
    child = [{"account_id": "A1"}, {"account_id": "MISSING"}]
    parent = [{"account_id": "A1"}]

    result = referential_integrity_check(child, parent, "account_id", "account_id")

    assert result.status == "FAIL"
    assert result.failed_count == 1


def test_partition_check_requires_partition_columns():
    rows = [{"txn_date": "2025-02-01"}, {"txn_date": ""}]

    result = partition_check(rows, ["txn_date"])

    assert result.status == "FAIL"
    assert result.failed_count == 1
