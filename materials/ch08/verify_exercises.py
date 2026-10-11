#!/usr/bin/env python3
"""Recalculate Chapter 8 schedules and verify exercise text against supplied fixtures."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from collections import Counter
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "materials" / "ch08" / "exercise-data.json"
CHAPTER_PATH = ROOT / "manuscripts" / "ch08" / "ch08.md"
PRACTICE_DIR = ROOT / "materials" / "ch08" / "practice"
OUTPUT_PATH = ROOT / "materials" / "ch08" / "author-exercise-verification.json"
EXPECTED_IDS = [f"E{i:02d}" for i in range(1, 8)]
REQUIRED_EXERCISE_LABELS = ["材料：", "任务：", "成果：", "评价标准："]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def heading_block(text: str, heading_pattern: str) -> str:
    match = re.search(heading_pattern, text, re.M)
    if not match:
        raise AssertionError(f"missing heading matching {heading_pattern!r}")
    end_match = re.search(r"^#{2,3} ", text[match.end():], re.M)
    end = match.end() + end_match.start() if end_match else len(text)
    return text[match.start():end]


def check_exercise_blocks(text: str, expected_ids: list[str]) -> list[dict[str, Any]]:
    closing = text.find("## 参考解与讨论")
    if closing < 0:
        raise AssertionError("chapter is missing the terminal ‘参考解与讨论’ section")

    exercise_results: list[dict[str, Any]] = []
    for exercise_id in expected_ids:
        matches = list(re.finditer(rf"^### {exercise_id}(?:\s|$).*?$", text[:closing], re.M))
        if len(matches) != 1:
            raise AssertionError(f"expected one independent-exercise heading for {exercise_id}; found {len(matches)}")
        next_heading = re.search(r"^### ", text[matches[0].end():closing], re.M)
        end = matches[0].end() + next_heading.start() if next_heading else closing
        block = text[matches[0].start():end]
        missing = [label for label in REQUIRED_EXERCISE_LABELS if label not in block]
        if missing:
            raise AssertionError(f"{exercise_id} is missing required task content: {', '.join(missing)}")
        answer_matches = list(re.finditer(rf"^### {exercise_id} 参考解与讨论\s*$", text[closing:], re.M))
        if len(answer_matches) != 1:
            raise AssertionError(f"{exercise_id} must have exactly one detailed answer after ‘参考解与讨论’")
        exercise_results.append({"id": exercise_id, "task_fields": REQUIRED_EXERCISE_LABELS, "answer_at_end": True})

    answer_ids = re.findall(r"^### (E\d{2}) 参考解与讨论\s*$", text[closing:], re.M)
    if answer_ids != expected_ids:
        raise AssertionError(f"answer IDs/order mismatch: expected {expected_ids}, got {answer_ids}")
    return exercise_results


def check_table_order(text: str) -> list[str]:
    ids = re.findall(r"^\*\*表(8-\d+)\s+", text, re.M)
    expected = [f"8-{i}" for i in range(1, len(ids) + 1)]
    if ids != expected:
        raise AssertionError(f"table numbers are not sequential by first appearance: {ids}")
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if re.match(r"^\*\*表8-\d+\s+", line):
            if index + 1 >= len(lines) or not re.match(r"^\|", lines[index + 1]):
                raise AssertionError(f"table title is not immediately followed by a Markdown table: {line}")
    return ids


def check_schedule(data: dict[str, Any], text: str) -> dict[str, Any]:
    challenge = data["two_week_challenge"]
    schedule = challenge["schedule"]
    days = [item["day"] for item in schedule]
    if days != list(range(1, 15)):
        raise AssertionError(f"schedule must cover days 1–14 in order, got {days}")
    if any(not isinstance(item["minutes"], int) or item["minutes"] < 0 for item in schedule):
        raise AssertionError("each daily duration must be a nonnegative integer number of minutes")

    total = sum(item["minutes"] for item in schedule)
    week_one = sum(item["minutes"] for item in schedule[:7])
    week_two = sum(item["minutes"] for item in schedule[7:])
    budget = challenge["available_minutes"]
    if total != challenge["planned_total_minutes"]:
        raise AssertionError(f"planned minutes mismatch: schedule sums to {total}, declared {challenge['planned_total_minutes']}")
    if total > budget or week_one > challenge["weekly_available_minutes"] or week_two > challenge["weekly_available_minutes"]:
        raise AssertionError("two-week or weekly schedule exceeds the learner's stated time budget")

    checkpoint_days = sorted(item["day"] for item in challenge["checkpoints"])
    if checkpoint_days != [7, 14]:
        raise AssertionError(f"expected checkpoints on days 7 and 14, got {checkpoint_days}")

    manuscript_minutes = {
        int(day): int(minutes)
        for day, minutes in re.findall(r"^\|\s*第(\d+)天\s*\|\s*(\d+)\s*\|", text, re.M)
    }
    expected_minutes = {item["day"]: item["minutes"] for item in schedule}
    if manuscript_minutes != expected_minutes:
        raise AssertionError(f"manuscript schedule does not match data: {manuscript_minutes} != {expected_minutes}")
    missing_tasks = [item["day"] for item in schedule if item["task"] not in text]
    if missing_tasks:
        raise AssertionError(f"manuscript is missing scheduled task descriptions for days: {missing_tasks}")

    checkpoint_cues = {
        7: ["至少四个核心术语", "查看状态和一项差异", "尚未解决的问题写下来", "一个已提交版本", "一项仍未提交的差异"],
        14: ["完成一个新的小变更", "查看历史与差异", "本地练习的边界", "可检验的下一目标"],
    }
    for checkpoint in challenge["checkpoints"]:
        missing_cues = [cue for cue in checkpoint_cues[checkpoint["day"]] if cue not in text]
        if missing_cues:
            raise AssertionError(f"manuscript is missing checkpoint cues for day {checkpoint['day']}: {missing_cues}")

    day7_task = schedule[6]["task"]
    day8_task = schedule[7]["task"]
    if "一个已提交版本" not in day7_task or "未提交的差异" not in day7_task:
        raise AssertionError("day 7 must check one existing commit and one uncommitted diff")
    if "第二次提交" not in day8_task:
        raise AssertionError("day 8 must make the second commit after day 7's uncommitted diff")

    totals_statement = f"第一周合计{week_one}分钟、第二周合计{week_two}分钟、总计{total}分钟"
    if totals_statement not in text:
        raise AssertionError(f"manuscript is missing the independently calculated schedule totals: {totals_statement}")
    if "虚构的填写示例" not in text or "不是实际执行记录" not in text:
        raise AssertionError("the sample learning record must be labeled fictional and not actually executed")

    return {
        "day_count": len(schedule),
        "week_one_minutes": week_one,
        "week_two_minutes": week_two,
        "planned_total_minutes": total,
        "available_minutes": budget,
        "remaining_minutes": budget - total,
        "checkpoint_days": checkpoint_days,
        "day_7_checks_committed_and_uncommitted_state": True,
        "day_8_creates_second_commit": True,
    }


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise AssertionError(f"CSV has no header: {path.relative_to(ROOT)}")
        return list(reader.fieldnames), list(reader)


def check_e03(data: dict[str, Any], text: str) -> dict[str, Any]:
    scenario = data["e03_independent_scenario"]
    task = heading_block(text, r"^### E03 应用训练")
    answer = heading_block(text, r"^### E03 参考解与讨论")
    if any(term in task for term in ("RiverCSV", "preserve_blank")):
        raise AssertionError("E03 task still duplicates the Section 8.3 RiverCSV case")
    task_cues = ["MapleDB", "4.2", "retry_policy", "尚未核实", "命令行参数", "环境变量"]
    answer_cues = ["disabled", "bounded", "最多重试2次", "尚未验证", "最终配置", "幂等"]
    missing_task = [cue for cue in task_cues if cue not in task]
    missing_answer = [cue for cue in answer_cues if cue not in answer]
    if missing_task or missing_answer:
        raise AssertionError(f"E03 independent scenario/answer mismatch: task={missing_task}, answer={missing_answer}")
    if scenario["documented_default_when_omitted"] not in answer:
        raise AssertionError("E03 answer does not state the configured documentation default")
    return {
        "product": scenario["product"],
        "version": scenario["version"],
        "documented_default_when_omitted": scenario["documented_default_when_omitted"],
        "runtime_override_checks": scenario["required_runtime_checks"],
        "answer_separates_documentation_from_runtime": True,
    }


class FixtureHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.labels: list[tuple[str, str]] = []
        self.controls: list[dict[str, str]] = []
        self.forbidden_tags: list[str] = []
        self.external_attributes: list[tuple[str, str]] = []
        self.event_attributes: list[tuple[str, str]] = []
        self.active_label: int | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        if tag == "label":
            self.labels.append((values.get("for", ""), ""))
            self.active_label = len(self.labels) - 1
        if tag in {"input", "textarea"}:
            self.controls.append({"tag": tag, "type": "textarea" if tag == "textarea" else values.get("type", ""), **values})
        if tag in {"script", "link", "img", "iframe", "form", "source", "video", "audio"}:
            self.forbidden_tags.append(tag)
        for key, value in attrs:
            if key in {"src", "href", "action", "formaction"} and value:
                self.external_attributes.append((tag, key))
            if key.lower().startswith("on"):
                self.event_attributes.append((tag, key))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)

    def handle_data(self, data: str) -> None:
        if self.active_label is not None:
            label_id, label_text = self.labels[self.active_label]
            self.labels[self.active_label] = (label_id, label_text + data.strip())

    def handle_endtag(self, tag: str) -> None:
        if tag == "label":
            self.active_label = None


def check_e05(data: dict[str, Any], text: str) -> dict[str, Any]:
    fixture = data["e05_fixtures"]
    html_path = ROOT / fixture["html_path"]
    empty_path = ROOT / fixture["empty_record_path"]
    log_path = ROOT / fixture["observation_log_path"]
    for path in (html_path, empty_path, log_path):
        if not path.is_file():
            raise AssertionError(f"missing E05 fixture: {path.relative_to(ROOT)}")

    html = html_path.read_text(encoding="utf-8")
    parser = FixtureHTMLParser()
    parser.feed(html)
    expected = fixture["fields"]
    expected_labels = [item["label"] for item in expected]
    actual_labels = [label for _, label in parser.labels]
    actual_fields = [
        {key: item.get(key, "") for key in ("id", "name", "type")}
        for item in parser.controls
    ]
    expected_fields = [{key: item[key] for key in ("id", "name", "type")} for item in expected]
    labels_by_id = {label_id for label_id, _ in parser.labels}
    if actual_labels != expected_labels or actual_fields != expected_fields:
        raise AssertionError(f"E05 HTML field order differs: labels={actual_labels}, controls={actual_fields}")
    if labels_by_id != {item["id"] for item in expected}:
        raise AssertionError("E05 HTML labels are not associated with all four controls")
    if parser.forbidden_tags or parser.external_attributes or parser.event_attributes:
        raise AssertionError("E05 HTML is not a standalone offline fixture")
    if ":focus-visible" not in html:
        raise AssertionError("E05 HTML must include a visible keyboard-focus style")

    empty_header, empty_rows = read_csv(empty_path)
    if empty_header != fixture["input_header"] or len(empty_rows) != 1 or any(empty_rows[0].values()):
        raise AssertionError("E05 empty-record CSV must have four matching headers and one blank row")
    log_header, log_rows = read_csv(log_path)
    expected_log_header = ["顺序", "字段标签", "预期顺序", "实际键盘顺序", "焦点是否可见", "观察环境与备注"]
    expected_log_fields = [{"顺序": str(i), "字段标签": label} for i, label in enumerate(expected_labels, start=1)]
    if log_header != expected_log_header or len(log_rows) != 4:
        raise AssertionError("E05 observation log must provide four blank rows for the named fields")
    if [{key: row[key] for key in ("顺序", "字段标签")} for row in log_rows] != expected_log_fields:
        raise AssertionError("E05 observation log field order differs from the HTML fixture")
    if any(row["实际键盘顺序"] or row["焦点是否可见"] or row["观察环境与备注"] for row in log_rows):
        raise AssertionError("E05 fixture must not prefill unobserved browser results")

    task = heading_block(text, r"^### E05 应用训练")
    answer = heading_block(text, r"^### E05 参考解与讨论")
    required_paths = [fixture["html_path"], fixture["empty_record_path"], fixture["observation_log_path"]]
    if any(path not in task for path in required_paths):
        raise AssertionError("E05 task must give all three repository-relative material paths")
    for cue in ("Tab和Shift+Tab", "未观察", "实际浏览器", "每周不超过15分钟"):
        if cue not in task:
            raise AssertionError(f"E05 task is missing the required independent instruction: {cue}")
    for cue in ("源码层面的预期", "没有实际执行浏览器测试", "实际列保持空白", "未观察"):
        if cue not in answer:
            raise AssertionError(f"E05 answer lacks observation boundary: {cue}")
    if re.search(r"我已在.{0,30}浏览器.{0,20}复核|实际第三步.{0,20}看不到", answer):
        raise AssertionError("E05 answer invents a browser observation")

    return {
        "ordered_labels": actual_labels,
        "field_count": len(parser.controls),
        "offline_static_html": True,
        "blank_record_rows": len(empty_rows),
        "blank_observation_rows": len(log_rows),
        "answer_makes_no_browser_execution_claim": True,
    }


def analyze_weather_csv(path: Path, expected: dict[str, Any], semantic_rules: dict[str, Any]) -> dict[str, Any]:
    headers, rows = read_csv(path)
    if headers != expected["headers"]:
        raise AssertionError(f"weather CSV headers differ in {path.name}: {headers}")
    duplicate_keys = [
        {"date": key[0], "station_id": key[1], "count": count}
        for key, count in sorted(Counter((row["date"], row["station_id"]) for row in rows).items())
        if count > 1
    ]
    for row in rows:
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", row["date"]):
            raise AssertionError(f"weather input date is not YYYY-MM-DD in {path.name}: {row['date']}")
        date.fromisoformat(row["date"])
        if not row["station_id"] or not row["temperature_c"] or not row["rainfall_mm"]:
            raise AssertionError(f"weather input contains an unexpected blank cell in {path.name}")
        for field in ("temperature_c", "rainfall_mm"):
            if row[field] != expected["missing_sentinel"]:
                float(row[field])
    missing_by_field = {
        field: sum(row[field] == expected["missing_sentinel"] for row in rows)
        for field in ("temperature_c", "rainfall_mm")
    }
    candidate_values = {
        field: sorted({row[field] for row in rows if row[field] in expected_values})
        for field, expected_values in expected["candidate_values_for_review"].items()
    }
    semantic_mismatch_values = {
        field: sorted({row[field] for row in rows if row[field] != expected["missing_sentinel"] and float(row[field]) < 0})
        for field in semantic_rules["nonnegative_quantity_fields"]
    }
    result = {
        "data_rows": len(rows),
        "duplicate_keys": duplicate_keys,
        "missing_by_field": missing_by_field,
        "candidate_values_for_review": candidate_values,
        "semantic_mismatch_values": semantic_mismatch_values,
    }
    for key, value in result.items():
        if value != expected[key]:
            raise AssertionError(f"weather CSV recalculation differs for {path.name} {key}: {value} != {expected[key]}")
    return result


def check_e07(data: dict[str, Any], text: str) -> dict[str, Any]:
    fixture = data["e07_fixture_expected_facts"]
    paths = data["e07_capstone"]["fixture_paths"]
    baseline_path = ROOT / paths["baseline"]
    transfer_path = ROOT / paths["transfer"]
    dictionary_path = ROOT / paths["dictionary"]
    for path in (baseline_path, transfer_path, dictionary_path):
        if not path.is_file():
            raise AssertionError(f"missing E07 fixture: {path.relative_to(ROOT)}")

    semantic_rules = fixture["semantic_rules"]
    baseline = analyze_weather_csv(baseline_path, {"headers": fixture["headers"], "missing_sentinel": fixture["missing_sentinel"], **fixture["baseline"]}, semantic_rules)
    transfer = analyze_weather_csv(transfer_path, {"headers": fixture["headers"], "missing_sentinel": fixture["missing_sentinel"], **fixture["transfer"]}, semantic_rules)
    dictionary = dictionary_path.read_text(encoding="utf-8")
    dictionary_cues = ["`date`", "`station_id`", "`temperature_c`", "`rainfall_mm`", "YYYY-MM-DD", "摄氏度（°C）", "毫米（mm）", "`NA`", "应为非负值", "不能单独确定冲突原因", "不能决定应如何处理数据", "不得因语义不一致而自动删除或填补原值", "CC0 1.0"]
    missing_dictionary_cues = [cue for cue in dictionary_cues if cue not in dictionary]
    if missing_dictionary_cues:
        raise AssertionError(f"E07 data dictionary is missing schema/license constraints: {missing_dictionary_cues}")
    if any(value in dictionary for value in ("43.8", "-2.0", "88.0", "2026-04-03")):
        raise AssertionError("E07 data dictionary leaks computed answer facts")

    task = heading_block(text, r"^### E07 综合训练")
    answer = heading_block(text, r"^### E07 参考解与讨论")
    if any(path not in task for path in paths.values()):
        raise AssertionError("E07 task must cite baseline, transfer, and dictionary by repository-relative paths")
    if any(Path(path).name not in answer for path in paths.values()):
        raise AssertionError("E07 answer must explain both supplied CSVs and the data dictionary")
    answer_cues = ["6条数据记录", "2026-04-03,ST01", "43.8", "-2.0", "按数量语义应为非负", "与这一字段定义不一致", "核实原始记录、数值编码或字段说明", "不能据此确定", "5条记录", "88.0", "保留原CSV", "不自动删除或填补", "不能自动去重"]
    missing_answer_cues = [cue for cue in answer_cues if cue not in answer]
    if missing_answer_cues:
        raise AssertionError(f"E07 answer is missing recalc/decision boundaries: {missing_answer_cues}")

    return {
        "baseline": baseline,
        "transfer": transfer,
        "dictionary_fields_and_units_checked": ["date: YYYY-MM-DD", "station_id: text", "temperature_c: °C", "rainfall_mm: mm"],
        "missing_sentinel": fixture["missing_sentinel"],
        "semantic_rule_review": {
            "nonnegative_quantity_fields": semantic_rules["nonnegative_quantity_fields"],
            "baseline_negative_rainfall_is_semantic_mismatch": baseline["semantic_mismatch_values"]["rainfall_mm"] == ["-2.0"],
            "cause_and_processing_remain_unresolved": "不能单独确定冲突原因" in dictionary and "不能决定应如何处理数据" in dictionary,
            "raw_value_preserved_without_auto_delete_or_fill": "不得因语义不一致而自动删除或填补原值" in dictionary and "不自动删除或填补原值" in answer,
            "required_follow_up": semantic_rules["required_response"],
        },
        "license_scope": fixture["license"],
        "dictionary_does_not_leak_answer_facts": True,
        "raw_data_preserved": True,
    }


def check_e06_fixture(data: dict[str, Any]) -> dict[str, Any]:
    rows = list(csv.DictReader(data["e06_csv_fixture"].splitlines()))
    facts = data["e06_expected_facts"]
    if len(rows) != facts["data_rows"]:
        raise AssertionError("E06 CSV row count does not match its expected fact")
    ids = [row["record_id"] for row in rows]
    duplicates = sorted({value for value in ids if ids.count(value) > 1})
    empty_scores = sum(row["score"] == "" for row in rows)
    score_91_rows = sum(row["score"] == "91" for row in rows)
    calculated = {"data_rows": len(rows), "duplicate_record_ids": duplicates, "empty_score_rows": empty_scores, "score_91_rows": score_91_rows}
    if calculated != facts:
        raise AssertionError(f"E06 fixture facts differ: {calculated} != {facts}")
    return calculated


def check_capstone_schedule(data: dict[str, Any], text: str) -> dict[str, Any]:
    capstone = data["e07_capstone"]
    days = capstone["schedule_example_days"]
    minutes = capstone["schedule_example_minutes"]
    weekly = capstone["schedule_example_weekly_minutes"]
    if len(days) != len(minutes) or days != sorted(days) or any(day < 1 or day > 14 for day in days):
        raise AssertionError("E07 schedule days and durations are inconsistent")
    task = heading_block(text, r"^### E07 综合训练")
    answer = heading_block(text, r"^### E07 参考解与讨论")
    displayed = [(int(day), int(value)) for day, value in re.findall(r"第(\d+)天(\d+)分钟", answer)]
    expected = list(zip(days, minutes))
    if displayed != expected:
        raise AssertionError(f"E07 answer schedule differs from data: {displayed} != {expected}")
    if "两周内最多投入360分钟" not in task or "每周不超过180分钟" not in task:
        raise AssertionError("E07 task must state the two-week and weekly time budgets")
    total = sum(minutes)
    calculated_weekly = [
        sum(value for day, value in zip(days, minutes) if day <= 7),
        sum(value for day, value in zip(days, minutes) if day > 7),
    ]
    if total != capstone["schedule_example_total_minutes"] or calculated_weekly != weekly:
        raise AssertionError(f"E07 schedule totals differ: daily total={total}, weekly={calculated_weekly}")
    if sum(weekly) != total or len(weekly) != 2 or any(value > capstone["weekly_budget_minutes"] for value in weekly):
        raise AssertionError("E07 schedule exceeds or misstates the weekly budget")
    return {
        "activity_count": len(minutes),
        "week_one_minutes": weekly[0],
        "week_two_minutes": weekly[1],
        "planned_total_minutes": total,
        "two_week_budget_minutes": 360,
        "weekly_budget_minutes": capstone["weekly_budget_minutes"],
        "remaining_minutes": 360 - total,
    }


def verify() -> dict[str, Any]:
    required = [DATA_PATH, CHAPTER_PATH]
    missing = [path for path in required if not path.is_file()]
    if missing:
        names = ", ".join(path.relative_to(ROOT).as_posix() for path in missing)
        raise FileNotFoundError(f"required Chapter 8 authoring inputs are not present yet: {names}")

    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    text = CHAPTER_PATH.read_text(encoding="utf-8")
    if data["independent_exercise_ids"] != EXPECTED_IDS:
        raise AssertionError(f"exercise ID contract mismatch: expected {EXPECTED_IDS}, got {data['independent_exercise_ids']}")

    exercises = check_exercise_blocks(text, EXPECTED_IDS)
    tables = check_table_order(text)
    schedule = check_schedule(data, text)
    e03 = check_e03(data, text)
    e05 = check_e05(data, text)
    e06 = check_e06_fixture(data)
    e07 = check_e07(data, text)
    capstone_schedule = check_capstone_schedule(data, text)
    practice_files = [ROOT / path for path in data["e05_fixtures"].values() if isinstance(path, str) and path.startswith("materials/")]
    practice_files.extend(ROOT / path for path in data["e07_capstone"]["fixture_paths"].values())
    return {
        "status": "PASS",
        "scope": "Chapter 8 exercise blocks and delayed answers, table order, two-week time budget, E03 independent scenario, E05 offline fixtures, and recalculated E06/E07 CSV facts",
        "chapter_sha256": sha256(CHAPTER_PATH),
        "data_sha256": sha256(DATA_PATH),
        "exercise_count": len(exercises),
        "exercises": exercises,
        "table_ids_in_first_appearance_order": tables,
        "two_week_schedule": schedule,
        "e03_independent_scenario": e03,
        "e05_fixture_verification": e05,
        "e06_fixture_recalculation": e06,
        "e07_data_recalculation": e07,
        "e07_capstone_schedule_recalculation": capstone_schedule,
        "practice_file_sha256": {path.relative_to(ROOT).as_posix(): sha256(path) for path in practice_files},
        "limitations": [
            "PASS confirms only the mechanical content and arithmetic checks encoded here.",
            "It does not establish that a learner executed the plan, retained skills, or achieved transfer.",
            "It does not establish actual browser behavior; E05 results require learner execution in a stated environment.",
            "It does not replace independent subject-matter or teaching review.",
        ],
    }


def main() -> int:
    try:
        result = verify()
    except (AssertionError, FileNotFoundError, KeyError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    OUTPUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{result['status']}: {result['exercise_count']} exercises; "
          f"{result['two_week_schedule']['planned_total_minutes']} challenge minutes; "
          f"{result['e06_fixture_recalculation']['data_rows']} E06 rows; "
          f"{result['e07_data_recalculation']['baseline']['data_rows']}+{result['e07_data_recalculation']['transfer']['data_rows']} E07 rows")
    print(f"wrote {OUTPUT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
