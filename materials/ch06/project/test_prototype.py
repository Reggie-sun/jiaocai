"""Standard-library tests for the offline chapter prototype."""

import copy
import json
import unittest
from decimal import Decimal
from pathlib import Path

from prototype import analyze_dataset, render_report


HERE = Path(__file__).resolve().parent


def load_input():
    with (HERE / "inputs.json").open(encoding="utf-8") as handle:
        return json.load(handle, parse_float=Decimal)


class PrototypeTests(unittest.TestCase):
    def test_known_zones_and_protected_zone(self):
        result = analyze_dataset(load_input())
        by_id = {zone["id"]: zone for zone in result["zones"]}
        self.assertEqual(by_id["A"]["calculation"]["signed_change_kwh"], "38.88")
        self.assertEqual(by_id["A"]["calculation"]["simulated_cost_change_cny"], "24.11")
        self.assertEqual(by_id["B"]["calculation"]["signed_change_kwh"], "51.84")
        self.assertEqual(by_id["C"]["calculation"]["signed_change_kwh"], "8.64")
        self.assertEqual(by_id["D"]["status"], "HOLD_PROTECTED")
        self.assertIsNone(by_id["D"]["calculation"])
        self.assertEqual(result["total_signed_change_kwh"], "99.36")
        self.assertEqual(result["total_simulated_cost_change_cny"], "61.60")
        self.assertFalse(result["device_controlled"])

    def test_report_preserves_zone_inputs_units_and_sources_for_ready_and_hold(self):
        data = load_input()
        data["zones"][0]["source_note"] = "A区教学来源版本甲"
        data["zones"][3]["source_note"] = "D区保护状态来源版本乙"
        result = analyze_dataset(data)
        by_id = {zone["id"]: zone for zone in result["zones"]}
        self.assertEqual(by_id["A"]["input_snapshot"], data["zones"][0])
        self.assertEqual(by_id["D"]["input_snapshot"], data["zones"][3])

        report = render_report(result)
        self.assertIn("灯具数量：48盏", report)
        self.assertIn("单灯功率：18瓦/盏", report)
        self.assertIn("基线时长：12小时/天", report)
        self.assertIn("候选时长：10.5小时/天", report)
        self.assertIn('应急照明状态："confirmed_no"', report)
        self.assertIn("source_note：A区教学来源版本甲", report)
        self.assertIn("[D] D入口边界区 — HOLD_PROTECTED", report)
        self.assertIn('应急照明状态："confirmed_yes"', report)
        self.assertIn("source_note：D区保护状态来源版本乙", report)

    def test_source_note_changes_reach_report(self):
        data = load_input()
        data["zones"][0]["source_note"] = "更新后的来源说明"
        report = render_report(analyze_dataset(data))
        self.assertIn("source_note：更新后的来源说明", report)

    def test_numeric_contract_accepts_int_float_and_decimal(self):
        data = load_input()
        data["teaching_price_cny_per_kwh"] = Decimal("0.625")
        zone = data["zones"][0]
        zone["watts_per_lamp"] = 18
        zone["baseline_hours_per_day"] = 12.0
        zone["candidate_hours_per_day"] = Decimal("10.5")
        result = analyze_dataset(data)
        self.assertEqual(result["zones"][0]["status"], "READY_FOR_HUMAN_REVIEW")

    def test_numeric_contract_rejects_strings_and_booleans(self):
        fields = (
            "teaching_price_cny_per_kwh",
            "watts_per_lamp",
            "baseline_hours_per_day",
            "candidate_hours_per_day",
        )
        for field in fields:
            for bad_value in ("18", "not-a-number", True, None):
                with self.subTest(field=field, bad_value=bad_value):
                    data = load_input()
                    if field == "teaching_price_cny_per_kwh":
                        data[field] = bad_value
                        result = analyze_dataset(data)
                        self.assertEqual(result["dataset_status"], "HOLD_DATASET")
                        self.assertIsNone(result["total_signed_change_kwh"])
                    else:
                        data["zones"][0][field] = bad_value
                        result = analyze_dataset(data)
                        self.assertEqual(result["zones"][0]["status"], "HOLD_CONFLICT")
                        self.assertIsNone(result["zones"][0]["calculation"])

    def test_fractional_price_is_displayed_exactly_and_reconciles(self):
        data = load_input()
        data["teaching_price_cny_per_kwh"] = Decimal("0.625")
        result = analyze_dataset(data)
        report = render_report(result)
        self.assertEqual(result["teaching_price_cny_per_kwh"], "0.625")
        self.assertEqual(result["total_signed_change_kwh"], "99.36")
        self.assertEqual(result["total_simulated_cost_change_cny"], "62.10")
        self.assertIn("教学模拟价：0.625元/kWh", report)
        self.assertIn("模拟金额差合计：62.10元", report)

    def test_missing_data_does_not_get_filled(self):
        data = load_input()
        del data["zones"][0]["watts_per_lamp"]
        result = analyze_dataset(data)
        zone = result["zones"][0]
        self.assertEqual(zone["status"], "HOLD_CONFLICT")
        self.assertIsNone(zone["calculation"])
        self.assertTrue(any("watts_per_lamp" in issue for issue in zone["issues"]))

    def test_unknown_protection_state_holds(self):
        data = load_input()
        data["zones"][0]["emergency_lighting_status"] = "unknown"
        result = analyze_dataset(data)
        self.assertEqual(result["zones"][0]["status"], "HOLD_CONFIRMATION")
        self.assertIsNone(result["zones"][0]["calculation"])

    def test_null_protection_state_holds_as_conflict(self):
        data = load_input()
        data["zones"][0]["emergency_lighting_status"] = None
        result = analyze_dataset(data)
        self.assertEqual(result["zones"][0]["status"], "HOLD_CONFLICT")
        self.assertIsNone(result["zones"][0]["calculation"])

    def test_missing_protection_state_holds(self):
        data = load_input()
        del data["zones"][0]["emergency_lighting_status"]
        result = analyze_dataset(data)
        self.assertEqual(result["zones"][0]["status"], "HOLD_CONFLICT")
        self.assertIsNone(result["zones"][0]["calculation"])

    def test_invalid_protection_string_holds(self):
        data = load_input()
        data["zones"][0]["emergency_lighting_status"] = "no"
        result = analyze_dataset(data)
        self.assertEqual(result["zones"][0]["status"], "HOLD_CONFLICT")
        self.assertIsNone(result["zones"][0]["calculation"])

    def test_boolean_protection_value_holds(self):
        data = load_input()
        data["zones"][0]["emergency_lighting_status"] = False
        result = analyze_dataset(data)
        self.assertEqual(result["zones"][0]["status"], "HOLD_CONFLICT")
        self.assertIsNone(result["zones"][0]["calculation"])

    def test_conflicting_or_out_of_range_input_holds(self):
        data = load_input()
        data["zones"][0]["lamp_count"] = -1
        result = analyze_dataset(data)
        self.assertEqual(result["zones"][0]["status"], "HOLD_CONFLICT")
        self.assertIsNone(result["zones"][0]["calculation"])

    def test_longer_candidate_is_reported_as_increase(self):
        data = load_input()
        zone = data["zones"][0]
        zone["lamp_count"] = 12
        zone["watts_per_lamp"] = 18
        zone["baseline_hours_per_day"] = 8
        zone["candidate_hours_per_day"] = 9
        result = analyze_dataset(data)
        zone_result = result["zones"][0]
        self.assertEqual(zone_result["status"], "SCENARIO_INCREASE")
        self.assertEqual(zone_result["calculation"]["signed_change_kwh"], "-6.48")
        self.assertEqual(zone_result["calculation"]["simulated_cost_change_cny"], "-4.02")

    def test_days_and_rate_changes_are_separate(self):
        original = analyze_dataset(load_input())
        data = load_input()
        data["period_days"] = 31
        changed_days = analyze_dataset(data)
        self.assertEqual(changed_days["zones"][0]["calculation"]["signed_change_kwh"], "40.176")

        data = load_input()
        data["teaching_price_cny_per_kwh"] = Decimal("0.70")
        changed_price = analyze_dataset(data)
        self.assertEqual(changed_price["zones"][0]["calculation"]["signed_change_kwh"], original["zones"][0]["calculation"]["signed_change_kwh"])
        self.assertEqual(changed_price["zones"][0]["calculation"]["simulated_cost_change_cny"], "27.22")

    def test_invalid_emergency_value_does_not_crash_or_pass(self):
        data = load_input()
        data["zones"][0]["emergency_lighting_status"] = ["confirmed_no"]
        result = analyze_dataset(data)
        self.assertEqual(result["zones"][0]["status"], "HOLD_CONFLICT")
        self.assertIsNone(result["zones"][0]["calculation"])

    def test_duplicate_id_holds_both_rows(self):
        data = load_input()
        duplicate = copy.deepcopy(data["zones"][1])
        duplicate["id"] = "A"
        data["zones"].append(duplicate)
        result = analyze_dataset(data)
        rows = [zone for zone in result["zones"] if zone["id"] == "A"]
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(zone["status"] == "HOLD_CONFLICT" for zone in rows))

    def test_dataset_level_unknowns_hold_every_zone(self):
        data = load_input()
        data["period_days"] = 0
        result = analyze_dataset(data)
        self.assertEqual(result["dataset_status"], "HOLD_DATASET")
        self.assertEqual(result["zones"], [])


if __name__ == "__main__":
    unittest.main()
