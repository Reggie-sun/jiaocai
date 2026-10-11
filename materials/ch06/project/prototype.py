#!/usr/bin/env python3
"""Offline teaching prototype for transparent lighting-scenario estimates."""

from __future__ import annotations

import json
import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
from typing import Any


TWO_PLACES = Decimal("0.01")
VALID_EMERGENCY_STATES = {"confirmed_yes", "confirmed_no", "unknown"}
ZONE_FIELDS = (
    "id",
    "name",
    "lamp_count",
    "watts_per_lamp",
    "baseline_hours_per_day",
    "candidate_hours_per_day",
    "emergency_lighting_status",
    "source_note",
)


def _decimal(value: Any, field: str) -> Decimal:
    """Accept numeric values, but never coerce quoted JSON strings or booleans."""
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        raise ValueError(f"{field}必须是有限数值")
    try:
        number = value if isinstance(value, Decimal) else Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError(f"{field}必须是有限数值") from None
    if not number.is_finite():
        raise ValueError(f"{field}必须是有限数值")
    return number


def _decimal_text(number: Decimal) -> str:
    text = format(number, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text or "0"


def _input_value(snapshot: dict[str, Any], field: str) -> str:
    if field not in snapshot:
        return "缺失"
    value = snapshot[field]
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, Decimal):
        return format(value, "f")
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), default=str)


def _display(number: Decimal, places: int = 3) -> str:
    quantum = Decimal(1).scaleb(-places)
    value = number.quantize(quantum, rounding=ROUND_HALF_UP)
    text = format(value, "f").rstrip("0").rstrip(".")
    return text or "0"


def _money(number: Decimal) -> str:
    return format(number.quantize(TWO_PLACES, rounding=ROUND_HALF_UP), ".2f")


def _dataset_hold(message: str) -> dict[str, Any]:
    return {
        "dataset_status": "HOLD_DATASET",
        "dataset_issues": [message],
        "zones": [],
        "computed_scope": "没有分区完成计算",
        "total_signed_change_kwh": None,
        "total_simulated_cost_change_cny": None,
        "human_decision_required": True,
        "device_controlled": False,
    }


def analyze_dataset(data: Any) -> dict[str, Any]:
    """Validate local teaching input and return estimates or explicit hold states."""
    if not isinstance(data, dict):
        return _dataset_hold("文件顶层必须是JSON对象")

    try:
        period = data["period_days"]
        if isinstance(period, bool) or not isinstance(period, int) or period <= 0:
            raise ValueError("period_days必须是正整数")
        price = _decimal(data["teaching_price_cny_per_kwh"], "teaching_price_cny_per_kwh")
        if price < 0:
            raise ValueError("教学模拟价格不得为负数")
        price_note = data["teaching_price_note"]
        if not isinstance(price_note, str) or not price_note.strip():
            raise ValueError("缺少教学模拟价格说明")
        zones = data["zones"]
        if not isinstance(zones, list) or not zones:
            raise ValueError("zones必须是非空列表")
    except KeyError as exc:
        return _dataset_hold(f"缺少顶层必需字段：{exc.args[0]}")
    except ValueError as exc:
        return _dataset_hold(str(exc))

    id_counts: dict[str, int] = {}
    for zone in zones:
        if isinstance(zone, dict):
            zone_id = zone.get("id")
            if isinstance(zone_id, str) and zone_id.strip():
                id_counts[zone_id.strip()] = id_counts.get(zone_id.strip(), 0) + 1

    results: list[dict[str, Any]] = []
    computed_energy = Decimal("0")
    computed_cost = Decimal("0")
    computed_count = 0

    for index, zone in enumerate(zones, start=1):
        if not isinstance(zone, dict):
            results.append({
                "id": f"row-{index}",
                "name": f"第{index}行",
                "status": "HOLD_CONFLICT",
                "issues": ["分区记录必须是JSON对象"],
                "calculation": None,
                "input_snapshot": zone,
            })
            continue

        input_snapshot = dict(zone)
        zone_id = zone.get("id", "").strip() if isinstance(zone.get("id"), str) else f"row-{index}"
        name = zone.get("name") if isinstance(zone.get("name"), str) else zone_id
        issues = [f"缺少必需字段：{field}" for field in ZONE_FIELDS if field not in zone]
        if not isinstance(zone.get("id"), str) or not zone.get("id", "").strip():
            issues.append("id必须是非空字符串")
        if not isinstance(zone.get("name"), str) or not zone.get("name", "").strip():
            issues.append("name必须是非空字符串")
        if isinstance(zone.get("id"), str) and id_counts.get(zone_id, 0) > 1:
            issues.append(f"区域编号重复：{zone_id}")
        if not isinstance(zone.get("source_note"), str) or not zone.get("source_note", "").strip():
            issues.append("source_note为空；需补充来源状态")

        numeric: dict[str, Decimal] = {}
        if "lamp_count" in zone:
            count = zone["lamp_count"]
            if isinstance(count, bool) or not isinstance(count, int) or count <= 0:
                issues.append("lamp_count必须是正整数")
            else:
                numeric["lamp_count"] = Decimal(count)
        for field in ("watts_per_lamp", "baseline_hours_per_day", "candidate_hours_per_day"):
            if field in zone:
                try:
                    numeric[field] = _decimal(zone[field], field)
                except ValueError as exc:
                    issues.append(str(exc))

        if "watts_per_lamp" in numeric and numeric["watts_per_lamp"] <= 0:
            issues.append("watts_per_lamp必须大于0")
        for field in ("baseline_hours_per_day", "candidate_hours_per_day"):
            if field in numeric and not Decimal("0") <= numeric[field] <= Decimal("24"):
                issues.append(f"{field}必须在0至24小时/天之间")

        emergency = zone.get("emergency_lighting_status")
        if "emergency_lighting_status" in zone and (
            not isinstance(emergency, str) or emergency not in VALID_EMERGENCY_STATES
        ):
            issues.append("emergency_lighting_status只能是confirmed_yes、confirmed_no或unknown")

        if issues:
            results.append({"id": zone_id, "name": name, "status": "HOLD_CONFLICT", "issues": issues, "calculation": None, "input_snapshot": input_snapshot})
            continue

        if emergency == "unknown":
            results.append({
                "id": zone_id,
                "name": name,
                "status": "HOLD_CONFIRMATION",
                "issues": ["应急照明状态未知；暂停确定建议，需人工确认"],
                "calculation": None,
                "input_snapshot": input_snapshot,
            })
            continue
        if emergency == "confirmed_yes":
            results.append({
                "id": zone_id,
                "name": name,
                "status": "HOLD_PROTECTED",
                "issues": ["分区标记为包含应急照明；不计算可调整建议"],
                "calculation": None,
                "input_snapshot": input_snapshot,
            })
            continue

        count = numeric["lamp_count"]
        watts = numeric["watts_per_lamp"]
        baseline_hours = numeric["baseline_hours_per_day"]
        candidate_hours = numeric["candidate_hours_per_day"]
        power_kw = count * watts / Decimal("1000")
        baseline_kwh = power_kw * baseline_hours * period
        candidate_kwh = power_kw * candidate_hours * period
        signed_change_kwh = baseline_kwh - candidate_kwh
        cost_change = signed_change_kwh * price

        if candidate_hours < baseline_hours:
            status = "READY_FOR_HUMAN_REVIEW"
            note = "候选时长较短；这是教学情景估算，需人工复核后才能讨论"
        elif candidate_hours > baseline_hours:
            status = "SCENARIO_INCREASE"
            note = "候选时长较长；显示情景增加，不标记为节能建议"
        else:
            status = "SCENARIO_NO_CHANGE"
            note = "候选与基线时长相同；情景没有电量差"

        calculation = {
            "total_power_kw": _display(power_kw),
            "baseline_kwh": _display(baseline_kwh),
            "candidate_kwh": _display(candidate_kwh),
            "signed_change_kwh": _display(signed_change_kwh),
            "simulated_cost_change_cny": _money(cost_change),
            "price_note": price_note,
        }
        results.append({"id": zone_id, "name": name, "status": status, "issues": [note], "calculation": calculation, "input_snapshot": input_snapshot})
        computed_energy += signed_change_kwh
        computed_cost += cost_change
        computed_count += 1

    return {
        "dataset_status": "READY_WITH_REVIEW_ITEMS" if any(z["status"].startswith("HOLD") for z in results) else "READY_FOR_HUMAN_REVIEW",
        "dataset_issues": [],
        "period_days": period,
        "teaching_price_cny_per_kwh": _decimal_text(price),
        "teaching_price_note": price_note,
        "zones": results,
        "computed_scope": f"只汇总{computed_count}个通过检查的教学分区；待确认、冲突或保护分区未计入，不代表校园总量",
        "total_signed_change_kwh": _display(computed_energy) if computed_count else None,
        "total_simulated_cost_change_cny": _money(computed_cost) if computed_count else None,
        "human_decision_required": True,
        "device_controlled": False,
    }


def render_report(result: dict[str, Any]) -> str:
    lines = ["校园共享学习空间照明建议原型（离线教学模拟）", f"数据集状态：{result['dataset_status']}"]
    if result.get("dataset_issues"):
        lines.extend(f"- 数据集问题：{issue}" for issue in result["dataset_issues"])
    else:
        lines.append(f"比较期：{result['period_days']}天；教学模拟价：{result['teaching_price_cny_per_kwh']}元/kWh")
        lines.append(f"价格说明：{result['teaching_price_note']}")
        for zone in result["zones"]:
            lines.append(f"\n[{zone['id']}] {zone['name']} — {zone['status']}")
            snapshot = zone["input_snapshot"]
            if isinstance(snapshot, dict):
                lines.append(
                    "  输入项（保留原值与单位）："
                    f"灯具数量：{_input_value(snapshot, 'lamp_count')}盏；"
                    f"单灯功率：{_input_value(snapshot, 'watts_per_lamp')}瓦/盏；"
                    f"基线时长：{_input_value(snapshot, 'baseline_hours_per_day')}小时/天；"
                    f"候选时长：{_input_value(snapshot, 'candidate_hours_per_day')}小时/天；"
                    f"应急照明状态：{_input_value(snapshot, 'emergency_lighting_status')}"
                )
                source_note = snapshot.get("source_note")
                if isinstance(source_note, str):
                    source_display = source_note
                else:
                    source_display = _input_value(snapshot, "source_note")
                lines.append(f"  source_note：{source_display}")
            for issue in zone["issues"]:
                lines.append(f"  状态说明：{issue}")
            calculation = zone["calculation"]
            if calculation:
                lines.append(f"  总功率：{calculation['total_power_kw']} kW")
                lines.append(f"  基线/候选：{calculation['baseline_kwh']} / {calculation['candidate_kwh']} kWh")
                lines.append(f"  基线减候选：{calculation['signed_change_kwh']} kWh")
                lines.append(f"  模拟金额差：{calculation['simulated_cost_change_cny']}元")
        lines.append(f"\n汇总范围：{result['computed_scope']}")
        lines.append(f"通过检查分区的基线减候选电量合计：{result['total_signed_change_kwh']} kWh")
        lines.append(f"通过检查分区的模拟金额差合计：{result['total_simulated_cost_change_cny']}元")
    lines.append("人工决定：必须复核输入来源、空间条件和责任边界。")
    lines.append("设备控制：否；本原型不联网、不连接传感器或灯具、不执行操作。")
    lines.append("教学数据：本文件中的数值均为自拟示例，不是现场调查或实际账单。")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if len(argv) > 2 or (len(argv) == 2 and argv[1] in {"-h", "--help"}):
        print("用法：python3 prototype.py [inputs.json]")
        return 0 if len(argv) == 2 else 2
    path = Path(argv[1]) if len(argv) == 2 else Path("inputs.json")
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle, parse_float=Decimal)
    except FileNotFoundError:
        print(f"找不到本地输入文件：{path}", file=sys.stderr)
        return 2
    except (OSError, json.JSONDecodeError) as exc:
        print(f"无法读取JSON输入：{exc}", file=sys.stderr)
        return 2

    result = analyze_dataset(data)
    print(render_report(result))
    return 0 if result["dataset_status"] != "HOLD_DATASET" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
