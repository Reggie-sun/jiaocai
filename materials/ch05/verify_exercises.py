#!/usr/bin/env python3
"""Recalculate Chapter 5 teaching matrices and check exercise/figure/table coverage."""
from __future__ import annotations

import json
import hashlib
import re
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHAPTER = ROOT / "manuscripts" / "ch05"
MATERIALS = ROOT / "materials" / "ch05"
DATA_PATH = MATERIALS / "exercise-data.json"
REPORT_PATH = MATERIALS / "author-exercise-verification.json"


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def han_count(text: str) -> int:
    text = re.sub(r"(?m)^```.*?^```\s*", "", text, flags=re.S)
    text = re.sub(r"https?://[^\s)]+", "", text)
    return len(re.findall(r"[\u3400-\u9fff]", text))


def recalculate(matrix: dict) -> dict[str, str]:
    weights = [Decimal(row["weight"]) for row in matrix["criteria"]]
    if sum(weights) != Decimal("1"):
        raise ValueError(f"weights sum to {sum(weights)}, expected 1")
    totals: dict[str, str] = {}
    for candidate, scores in matrix["scores"].items():
        if len(scores) != len(weights):
            raise ValueError(f"{candidate} has {len(scores)} scores for {len(weights)} criteria")
        if any(not 1 <= score <= 5 for score in scores):
            raise ValueError(f"{candidate} score outside 1-5")
        total = sum(weight * Decimal(score) for weight, score in zip(weights, scores))
        totals[candidate] = f"{total:.2f}"
    if totals != matrix["expected_totals"]:
        raise ValueError(f"expected {matrix['expected_totals']}, recalculated {totals}")
    return totals


def read_matrix_table(text: str, table_id: int) -> dict:
    caption = re.search(rf"(?m)^表5-{table_id}\s+[^\n]*\n\n", text)
    if not caption:
        raise ValueError(f"missing table 5-{table_id}")
    lines = text[caption.end():].splitlines()
    table_lines = []
    for line in lines:
        if not line.startswith("|"):
            break
        table_lines.append(line)
    if len(table_lines) < 4:
        raise ValueError(f"table 5-{table_id} is incomplete")
    rows = [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in table_lines]
    candidates = [re.match(r"([A-D])", cell) for cell in rows[0][1:]]
    if any(match is None for match in candidates):
        raise ValueError(f"table 5-{table_id} candidate headers must identify A-D")
    candidate_names = [match.group(1) for match in candidates if match]
    weights = []
    scores = {name: [] for name in candidate_names}
    rendered_totals = {}
    for row in rows[2:]:
        label = row[0]
        if "总分" in label:
            rendered_totals = {name: row[index + 1] for index, name in enumerate(candidate_names)}
            continue
        weight_match = re.search(r"[（(](0\.\d+)[）)]", label)
        if not weight_match:
            raise ValueError(f"table 5-{table_id} row missing numeric weight: {label}")
        weights.append(weight_match.group(1))
        for index, name in enumerate(candidate_names):
            scores[name].append(int(row[index + 1]))
    return {"weights": weights, "scores": scores, "rendered_totals": rendered_totals}


def main() -> int:
    inputs = json.loads(load_text(DATA_PATH))
    opening = load_text(CHAPTER / "opening.md")
    sections = [load_text(CHAPTER / f"s5-{n}.md") for n in range(1, 8)]
    closing = load_text(CHAPTER / "closing.md")
    manuscript = "\n\n".join([opening.rstrip(), *[part.rstrip() for part in sections], closing.rstrip()]) + "\n"
    chapter_path = CHAPTER / "ch05.md"
    if chapter_path.exists() and load_text(chapter_path) != manuscript:
        raise ValueError("ch05.md differs from ordered section components")

    matrices = {
        "worked_example_table_5_2": recalculate(inputs["worked_example_table_5_2"]),
        "exercise_E01_table_5_3": recalculate(inputs["exercise_E01_table_5_3"]),
    }
    for table_id, key in [(2, "worked_example_table_5_2"), (3, "exercise_E01_table_5_3")]:
        rendered = read_matrix_table(manuscript, table_id)
        source = inputs[key]
        source_weights = [row["weight"] for row in source["criteria"]]
        if rendered["weights"] != source_weights or rendered["scores"] != source["scores"]:
            raise ValueError(f"table 5-{table_id} values differ from exercise-data.json")
        if rendered["rendered_totals"] and rendered["rendered_totals"] != source["expected_totals"]:
            raise ValueError(f"table 5-{table_id} displayed totals differ from recalculated totals")
    for total in ["3.80", "2.35", "3.75", "2.80"]:
        if total not in closing:
            raise ValueError(f"E01 reference answer missing recalculated total {total}")

    exercise = inputs["exercise_E01_table_5_3"]
    if exercise["hard_constraints"][0] != "without_mouse_for_key_tasks":
        raise ValueError("E01 first hard constraint must remain the no-mouse condition")
    if "keyboard" in exercise["candidate_assessment"]["B"].lower() or "voice interaction" not in exercise["candidate_assessment"]["B"]:
        raise ValueError("E01 B assessment must not equate no-mouse access with keyboard-only access")

    exercise_ids = re.findall(r"(?m)^E(\d{2})", manuscript)
    exercise_ids.extend(re.findall(r"(?m)^### E(\d{2}) 综合任务", manuscript))
    seen_exercises = sorted(set(exercise_ids))
    expected_exercises = [f"{number:02d}" for number in range(1, 9)]
    if seen_exercises != expected_exercises:
        raise ValueError(f"exercise IDs {seen_exercises}, expected {expected_exercises}")
    answer_ids = re.findall(r"(?m)^### E(\d{2})参考解与讨论\s*$", closing)
    if answer_ids != expected_exercises:
        raise ValueError(f"answer IDs {answer_ids}, expected {expected_exercises}")
    if "E02独立作答限定在卡B、卡C或卡D" not in manuscript or "卡A只作为本节的先行示范" not in manuscript:
        raise ValueError("E02 must separate its card-A demonstration from its independent B-D task")
    for required in ["卡B可问", "卡C可问", "卡D可问"]:
        if required not in closing:
            raise ValueError(f"E02 answer missing independent-card analysis: {required}")
    for required in ["权威资源状态", "页面版本和渲染时间", "同一资源ID", "结论应保留为未知"]:
        if required not in manuscript:
            raise ValueError(f"E02 answer/example missing evidence check: {required}")
    for required in ["从随机初始化开始训练", "代码或工程流程复用", "迁移学习"]:
        if required not in manuscript:
            raise ValueError(f"transfer-learning boundary missing: {required}")

    table_ids = [int(value) for value in re.findall(r"(?m)^表5-(\d+)\s+", manuscript)]
    if table_ids != list(range(1, 9)):
        raise ValueError(f"table captions {table_ids}, expected 1..8 in order")
    for table_id in table_ids:
        caption = re.search(rf"(?m)^表5-{table_id}\s+[^\n]*\n\n(?=\|)", manuscript)
        if not caption:
            raise ValueError(f"table 5-{table_id} caption is not on a separate line before the table")

    figure_data = json.loads(load_text(MATERIALS / "author-figures.json"))
    figure_ids = [figure["id"] for figure in figure_data["figures"]]
    expected_figure_ids = [f"fig5-{number}" for number in range(1, 8)]
    if figure_ids != expected_figure_ids:
        raise ValueError(f"figure plan IDs {figure_ids}, expected {expected_figure_ids}")
    for number in range(1, 8):
        if not re.search(rf"(?m)^图5-{number}\s+[^\n]+$", manuscript):
            raise ValueError(f"missing figure title placeholder 5-{number}")
        if not re.search(rf"(?s)^图5-{number}\s+[^\n]+\n\n来源：[^\n]+\n\n", manuscript, re.M):
            raise ValueError(f"figure 5-{number} needs a source and reading cue")

    reference_ids = [int(value) for value in re.findall(r"(?m)^\[(\d+)\]", closing)]
    if reference_ids != list(range(1, 15)):
        raise ValueError(f"reference numbering {reference_ids}, expected 1..14")

    body = manuscript.split("## 参考文献", 1)[0]
    first_use_order = list(dict.fromkeys(re.findall(r"\[(\d+)\]", body)))
    expected_first_use = [str(number) for number in range(1, 15)]
    if first_use_order != expected_first_use:
        raise ValueError(f"first citation order {first_use_order}, expected {expected_first_use}")
    source_register = load_text(MATERIALS / "author-sources.md")
    register_ids = [int(value) for value in re.findall(r"(?m)^- \*\*\[(\d+)\]", source_register)]
    if register_ids != list(range(1, 15)):
        raise ValueError(f"source-map numbering {register_ids}, expected 1..14")

    def reference_urls(text: str) -> dict[int, str]:
        refs: dict[int, str] = {}
        for line in text.splitlines():
            match = re.match(r"^\[(\d+)\]\s+", line)
            if not match:
                continue
            urls = re.findall(r"https?://\S+", line)
            if len(urls) != 1:
                raise ValueError(f"reference {match.group(1)} must have exactly one bare URL")
            refs[int(match.group(1))] = urls[0].rstrip(".,")
        return refs

    chapter_refs = reference_urls(closing)
    register_refs = reference_urls(source_register.split("## References", 1)[1])
    if chapter_refs != register_refs:
        raise ValueError("chapter bibliography URLs differ from author source register")

    count = han_count(manuscript)
    if count < 28000:
        raise ValueError(f"chapter Han character count {count} is below 28000")
    report = {
        "chapter": "ch05",
        "verification": "PASS",
        "method": "Python Decimal weighted-sum recomputation; structural checks over the chapter components",
        "han_character_count_excluding_urls_and_code": count,
        "target_range": [31000, 35000],
        "minimum": 28000,
        "matrices": matrices,
        "exercise_ids": [f"E{number}" for number in expected_exercises],
        "answer_ids": [f"E{number}" for number in answer_ids],
        "table_ids_in_order": table_ids,
        "figure_ids_in_order": figure_ids,
        "reference_ids_in_order": reference_ids,
        "citation_first_use_order": [int(value) for value in first_use_order],
        "source_register_numbering": register_ids,
        "chapter_bibliography_matches_source_register_urls": True,
        "chapter_sha256": hashlib.sha256(chapter_path.read_bytes()).hexdigest() if chapter_path.exists() else None,
        "chapter_file_matches_components": chapter_path.exists() and load_text(chapter_path) == manuscript,
    }
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
