#!/usr/bin/env python3
"""Recalculate chapter examples/exercises and test fail-closed input behavior."""

from __future__ import annotations

import copy
import json
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "materials" / "ch06" / "project"
sys.path.insert(0, str(PROJECT))

from prototype import analyze_dataset  # noqa: E402


DATA_PATH = ROOT / "materials" / "ch06" / "exercise-data.json"
OUTPUT_PATH = ROOT / "materials" / "ch06" / "author-exercise-verification.json"
CENT = Decimal("0.01")


def independent_calculation(zone: dict[str, Any], days: int, price: Decimal) -> dict[str, str]:
    """Recalculate with a separate expression and Decimal arithmetic."""
    count = Decimal(zone["lamp_count"])
    watts = Decimal(str(zone["watts_per_lamp"]))
    base_hours = Decimal(str(zone["baseline_hours_per_day"]))
    candidate_hours = Decimal(str(zone["candidate_hours_per_day"]))
    power_kw = count * watts / Decimal("1000")
    baseline = power_kw * base_hours * Decimal(days)
    candidate = power_kw * candidate_hours * Decimal(days)
    change = baseline - candidate
    cost = change * price
    return {
        "baseline_kwh": _decimal_text(baseline),
        "candidate_kwh": _decimal_text(candidate),
        "signed_change_kwh": _decimal_text(change),
        "simulated_cost_change_cny": format(cost.quantize(CENT, rounding=ROUND_HALF_UP), ".2f"),
        "simulated_cost_change_cny_unrounded": _decimal_text(cost),
    }


def _decimal_text(value: Decimal) -> str:
    text = format(value, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text or "0"


def _assert_fields(actual: dict[str, Any], expected: dict[str, Any], label: str) -> list[str]:
    checked: list[str] = []
    for key, value in expected.items():
        if key == "D_status":
            observed = next(zone["status"] for zone in actual["zones"] if zone["id"] == "D")
        elif key == "D_calculation":
            observed = next(zone["calculation"] for zone in actual["zones"] if zone["id"] == "D")
        elif key in {"status", "calculation"}:
            if key == "status":
                observed = actual["status"]
            else:
                observed = actual["calculation"]
        elif actual.get("calculation") is not None and key in actual["calculation"]:
            observed = actual["calculation"][key]
        else:
            observed = actual.get(key)
        if observed != value:
            raise AssertionError(f"{label}: {key}: expected {value!r}, got {observed!r}")
        checked.append(f"{label}.{key}")
    return checked


def _single_zone(result: dict[str, Any]) -> dict[str, Any]:
    if len(result.get("zones", [])) != 1:
        raise AssertionError("expected exactly one zone")
    return result["zones"][0]


def verify() -> dict[str, Any]:
    with DATA_PATH.open("r", encoding="utf-8") as handle:
        data = json.load(handle, parse_float=Decimal)

    checked_cases: list[dict[str, Any]] = []
    for case_name, case in data["cases"].items():
        input_data = case["input"]
        expected = case["expected"]
        result = analyze_dataset(input_data)
        if "total_signed_change_kwh" in expected:
            checked = _assert_fields(result, expected, case_name)
            zone_values = [z for z in result["zones"] if z["calculation"] is not None]
            independent_total = sum((Decimal(z["calculation"]["signed_change_kwh"]) for z in zone_values), Decimal("0"))
            if _decimal_text(independent_total) != expected["total_signed_change_kwh"]:
                raise AssertionError(f"{case_name}: independent total kWh mismatch")
            price = Decimal(str(input_data["teaching_price_cny_per_kwh"]))
            original_zones = {z["id"]: z for z in input_data["zones"]}
            independent_cost = sum((Decimal(independent_calculation(original_zones[z["id"]], input_data["period_days"], price)["simulated_cost_change_cny_unrounded"]) for z in zone_values), Decimal("0"))
            if format(independent_cost.quantize(CENT, rounding=ROUND_HALF_UP), ".2f") != expected["total_simulated_cost_change_cny"]:
                raise AssertionError(f"{case_name}: independent cost total mismatch")
        else:
            zone_result = _single_zone(result)
            if "status" in expected:
                checked = _assert_fields(zone_result, expected, case_name)
            else:
                checked = []
            calculation = zone_result["calculation"]
            if "calculation" in expected and expected["calculation"] is None and calculation is not None:
                raise AssertionError(f"{case_name}: blocked input unexpectedly calculated")
            if calculation:
                if "calculation" in expected:
                    raise AssertionError(f"{case_name}: expected a blocked calculation")
                for key in ("baseline_kwh", "candidate_kwh", "signed_change_kwh", "simulated_cost_change_cny"):
                    wanted = expected.get(key)
                    if wanted is not None and calculation[key] != wanted:
                        raise AssertionError(f"{case_name}: {key}: expected {wanted}, got {calculation[key]}")
                    if wanted is not None:
                        checked.append(f"{case_name}.{key}")
                independent = independent_calculation(input_data["zones"][0], input_data["period_days"], Decimal(str(input_data["teaching_price_cny_per_kwh"])))
                for key, expected_value in independent.items():
                    if key == "simulated_cost_change_cny_unrounded":
                        continue
                    if calculation[key] != expected_value:
                        raise AssertionError(f"{case_name}: prototype and independent {key} differ")
                    checked.append(f"{case_name}.independent_{key}")

        checked_cases.append({
            "case": case_name,
            "status": result["zones"][0]["status"] if result.get("zones") else result["dataset_status"],
            "checks": checked,
        })

    base = copy.deepcopy(data["cases"]["worked_A_30d"]["input"])
    behavior_checks: list[dict[str, str]] = []

    missing = copy.deepcopy(base)
    del missing["zones"][0]["watts_per_lamp"]
    missing_result = _single_zone(analyze_dataset(missing))
    assert missing_result["status"] == "HOLD_CONFLICT" and missing_result["calculation"] is None
    behavior_checks.append({"case": "missing_watts", "expected": "HOLD_CONFLICT; no calculation", "actual": missing_result["status"]})

    out_of_range = copy.deepcopy(base)
    out_of_range["zones"][0]["candidate_hours_per_day"] = 25
    range_result = _single_zone(analyze_dataset(out_of_range))
    assert range_result["status"] == "HOLD_CONFLICT" and range_result["calculation"] is None
    behavior_checks.append({"case": "hours_over_24", "expected": "HOLD_CONFLICT; no calculation", "actual": range_result["status"]})

    unknown = copy.deepcopy(base)
    unknown["zones"][0]["emergency_lighting_status"] = "unknown"
    unknown_result = _single_zone(analyze_dataset(unknown))
    assert unknown_result["status"] == "HOLD_CONFIRMATION" and unknown_result["calculation"] is None
    behavior_checks.append({"case": "unknown_protection", "expected": "HOLD_CONFIRMATION; no calculation", "actual": unknown_result["status"]})

    for case_name, mutate in (
        ("null_protection", lambda z: z.__setitem__("emergency_lighting_status", None)),
        ("missing_protection", lambda z: z.pop("emergency_lighting_status")),
        ("invalid_protection_string", lambda z: z.__setitem__("emergency_lighting_status", "no")),
        ("boolean_protection", lambda z: z.__setitem__("emergency_lighting_status", False)),
        ("malformed_protection", lambda z: z.__setitem__("emergency_lighting_status", ["confirmed_no"])),
    ):
        malformed_status = copy.deepcopy(base)
        mutate(malformed_status["zones"][0])
        malformed_result = _single_zone(analyze_dataset(malformed_status))
        assert malformed_result["status"] == "HOLD_CONFLICT" and malformed_result["calculation"] is None
        behavior_checks.append({"case": case_name, "expected": "HOLD_CONFLICT; no calculation", "actual": malformed_result["status"]})

    duplicate = copy.deepcopy(base)
    duplicate["zones"].append(copy.deepcopy(duplicate["zones"][0]))
    duplicate_result = analyze_dataset(duplicate)
    assert all(z["status"] == "HOLD_CONFLICT" and z["calculation"] is None for z in duplicate_result["zones"])
    behavior_checks.append({"case": "duplicate_zone_id", "expected": "both rows HOLD_CONFLICT; no calculation", "actual": "both rows HOLD_CONFLICT"})

    changed = copy.deepcopy(base)
    changed["period_days"] = 31
    changed_result = _single_zone(analyze_dataset(changed))["calculation"]
    assert changed_result["signed_change_kwh"] == "40.176"
    behavior_checks.append({"case": "period_change_30_to_31", "expected": "40.176 kWh", "actual": f"{changed_result['signed_change_kwh']} kWh"})

    changed = copy.deepcopy(base)
    changed["teaching_price_cny_per_kwh"] = Decimal("0.70")
    changed_result = _single_zone(analyze_dataset(changed))["calculation"]
    assert changed_result["signed_change_kwh"] == "38.88" and changed_result["simulated_cost_change_cny"] == "27.22"
    behavior_checks.append({"case": "price_change_0.62_to_0.70", "expected": "38.88 kWh; 27.22 CNY", "actual": f"{changed_result['signed_change_kwh']} kWh; {changed_result['simulated_cost_change_cny']} CNY"})

    no_period = copy.deepcopy(base)
    del no_period["period_days"]
    no_period_result = analyze_dataset(no_period)
    assert no_period_result["dataset_status"] == "HOLD_DATASET" and not no_period_result["zones"]
    behavior_checks.append({"case": "missing_dataset_period", "expected": "HOLD_DATASET; no zone calculation", "actual": no_period_result["dataset_status"]})

    return {
        "scope": "本章讲解示例、独立题关键算术、单位/价格变化和fail-closed行为",
        "data_identity": "exercise-data.json; author-created teaching values",
        "calculation_method": "independent Decimal formula: count × W ÷ 1000 × hours/day × days; cost = signed kWh × teaching CNY/kWh",
        "case_count": len(checked_cases),
        "case_results": checked_cases,
        "behavior_check_count": len(behavior_checks),
        "behavior_checks": behavior_checks,
        "status": "PASS",
        "limitations": ["PASS only confirms arithmetic and software behavior for these teaching fixtures.", "It is not a field measurement, real tariff, accessibility/safety evaluation, or teaching-effectiveness assessment."],
    }


def main() -> int:
    result = verify()
    OUTPUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{result['status']}: {result['case_count']} numeric/example cases; {result['behavior_check_count']} behavior checks")
    print(f"wrote {OUTPUT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
