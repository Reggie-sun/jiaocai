#!/usr/bin/env python3
"""Recalculate Chapter 4's original numerical teaching examples."""

from __future__ import annotations

import json
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "exercise-data.json"
OUTPUT_PATH = ROOT / "author-exercise-verification.json"


def percent(numerator: int, denominator: int, places: int = 6) -> float:
    value = Decimal(numerator) * Decimal(100) / Decimal(denominator)
    quantum = Decimal(1).scaleb(-places)
    return float(value.quantize(quantum, rounding=ROUND_HALF_UP))


def weighted(scores: list[int], weights: list[float]) -> float:
    total = sum(Decimal(score) * Decimal(str(weight)) for score, weight in zip(scores, weights))
    return float(total.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP))


def close(actual: float, expected: float, *, tolerance: float = 0.00001) -> bool:
    return abs(actual - expected) <= tolerance


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    checked: list[dict[str, object]] = []

    def record(name: str, actual: object, expected: object) -> None:
        if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
            passed = close(float(actual), float(expected))
        else:
            passed = actual == expected
        checked.append({"id": name, "actual": actual, "expected": expected, "status": "PASS" if passed else "FAIL"})
        if not passed:
            raise AssertionError(f"{name}: expected {expected!r}, got {actual!r}")

    ex = data["examples"]
    demo = ex["s4_1_demo"]
    record("s4_1_demo_percent", percent(demo["numerator"], demo["denominator"], 1), demo["expected_percent"])

    groups = ex["s4_2_confounded_groups"]
    for key, values in groups.items():
        record(f"{key}_percent", percent(values["passed"], values["total"], 1), values["expected_percent"])

    matrix = ex["s4_2_screening_matrix"]
    record("s4_2_screening_total", matrix["tp"] + matrix["fn"] + matrix["fp"] + matrix["tn"], matrix["total"])
    record("s4_2_screening_recall_percent", percent(matrix["tp"], matrix["tp"] + matrix["fn"], 1), 80.0)
    record("s4_2_screening_false_positive_rate_percent", percent(matrix["fp"], matrix["fp"] + matrix["tn"], 1), 15.0)
    record("s4_2_screening_accuracy_percent", percent(matrix["tp"] + matrix["tn"], matrix["total"], 1), 84.4)
    record("s4_2_screening_precision_percent", percent(matrix["tp"], matrix["tp"] + matrix["fp"], 1), 42.1)

    time_change = ex["s4_2_time_change_minutes"]
    record("s4_2_absolute_time_decrease", time_change["before"] - time_change["after"], time_change["expected_absolute_decrease"])
    record("s4_2_relative_time_decrease_percent", percent(time_change["before"] - time_change["after"], time_change["before"], 6), time_change["expected_relative_percent"])

    sensitivity = ex["s4_3_weight_sensitivity"]
    for group_name, weights_key, expected_key in [
        ("protection", "protection_weights", "expected_protection_scores"),
        ("access", "access_weights", "expected_access_scores"),
    ]:
        for option, scores in sensitivity["scores"].items():
            actual = weighted(scores, sensitivity[weights_key])
            record(f"s4_3_{group_name}_{option}", actual, sensitivity[expected_key][option])

    exercises = data["exercises"]
    e02 = exercises["E02_classifier"]
    record("E02_confusion_total", e02["tp"] + e02["fn"] + e02["fp"] + e02["tn"], e02["total"])
    e02_results = {
        "recall": percent(e02["tp"], e02["tp"] + e02["fn"], 1),
        "false_positive_rate": percent(e02["fp"], e02["fp"] + e02["tn"], 1),
        "precision": percent(e02["tp"], e02["tp"] + e02["fp"], 2),
        "accuracy": percent(e02["tp"] + e02["tn"], e02["total"], 1),
    }
    for name, actual in e02_results.items():
        record(f"E02_{name}_percent", actual, e02["expected_percent"][name])

    e03 = exercises["E03_reminder_groups"]
    for key, values in e03.items():
        record(f"E03_{key}_percent", percent(values.get("passed", values.get("numerator")), values.get("total", values.get("denominator")), 1), values["expected_percent"])

    e04 = exercises["E04_weight_sensitivity"]
    for group_name, weights_key, expected_key in [
        ("A", "group_A_weights", "expected_group_A_scores"),
        ("B", "group_B_weights", "expected_group_B_scores"),
    ]:
        for option, scores in e04["scores"].items():
            record(f"E04_group_{group_name}_{option}", weighted(scores, e04[weights_key]), e04[expected_key][option])

    e06 = exercises["E06_demo_images"]
    record("E06_demo_percent", percent(e06["correct"], e06["total"], 1), e06["expected_percent"])

    result = {
        "chapter": 4,
        "verified_on": date.today().isoformat(),
        "script": "materials/ch04/verify_exercises.py",
        "input": "materials/ch04/exercise-data.json",
        "data_status": "original teaching simulations; not real institutional or model performance data",
        "checks_run": len(checked),
        "status": "PASS",
        "checks": checked,
    }
    OUTPUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
