#!/usr/bin/env python3
"""Recompute Chapter 9 numeric exercises and check bounded structure claims."""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHAPTER = ROOT / "manuscripts/ch09/ch09.md"
PARTS = [
    ROOT / "manuscripts/ch09/opening.md",
    ROOT / "manuscripts/ch09/s9-1.md",
    ROOT / "manuscripts/ch09/s9-2.md",
    ROOT / "manuscripts/ch09/s9-3.md",
    ROOT / "manuscripts/ch09/s9-4.md",
    ROOT / "manuscripts/ch09/s9-5.md",
    ROOT / "manuscripts/ch09/closing.md",
]
DATA_PATH = ROOT / "materials/ch09/exercise-data.json"
REPORT_PATH = ROOT / "materials/ch09/author-exercise-verification.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def han_count(text: str) -> int:
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`[^`]*`", "", text)
    text = re.sub(r"https?://\S+", "", text)
    return sum("\u3400" <= c <= "\u4dbf" or "\u4e00" <= c <= "\u9fff" or "\uf900" <= c <= "\ufaff" for c in text)


def table_after(text: str, marker: str) -> list[list[str]]:
    pos = text.find(marker)
    if pos < 0:
        raise AssertionError(f"missing table marker: {marker}")
    lines = text[pos:].splitlines()
    table_lines: list[str] = []
    started = False
    for line in lines:
        if line.strip().startswith("|"):
            started = True
            table_lines.append(line.strip())
        elif started:
            break
    rows: list[list[str]] = []
    for line in table_lines:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if cells and all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells):
            continue
        rows.append(cells)
    return rows


def row_values(rows: list[list[str]], first_col: str) -> list[str]:
    for row in rows[1:]:
        if row and row[0] == first_col:
            return row
    raise AssertionError(f"missing table row: {first_col}")


def verify() -> dict:
    data = json.loads(DATA_PATH.read_text())
    text = CHAPTER.read_text()
    checks: list[str] = []
    expected_chapter = "\n\n".join(part.read_text().strip() for part in PARTS) + "\n"
    assert text == expected_chapter, "assembled chapter is stale relative to its source parts"
    checks.append("assembled chapter exactly matches opening, section, and closing source files")

    # E01: recompute the earliest schedule by topological relaxation.
    durations = data["E01"]["duration_days"]
    predecessors = data["E01"]["predecessors"]
    starts: dict[str, int] = {}
    finishes: dict[str, int] = {}
    paths: dict[str, list[list[str]]] = {}
    remaining = set(durations)
    while remaining:
        ready = sorted(task for task in remaining if all(dep in finishes for dep in predecessors[task]))
        if not ready:
            raise AssertionError("E01 dependency graph contains a cycle or unknown predecessor")
        for task in ready:
            start = max((finishes[dep] for dep in predecessors[task]), default=0)
            starts[task] = start
            finishes[task] = start + durations[task]
            critical_parents = [dep for dep in predecessors[task] if finishes[dep] == start]
            paths[task] = (
                [path + [task] for dep in critical_parents for path in paths[dep]]
                if critical_parents else [[task]]
            )
            remaining.remove(task)
    duration = max(finishes.values())
    critical_paths = sorted(
        path for task in durations if finishes[task] == duration for path in paths[task]
    )
    expected = data["E01"]
    assert starts == expected["expected_earliest_start"], (starts, expected["expected_earliest_start"])
    assert finishes == expected["expected_earliest_finish"], (finishes, expected["expected_earliest_finish"])
    assert duration == expected["expected_duration"]
    assert critical_paths == expected["expected_critical_paths"], (critical_paths, expected["expected_critical_paths"])
    assert data["E01"]["duration_days"]["B"] == 1
    input_rows = table_after(text, "| 任务 | 工作内容 | 估计工作日 | 前置任务 |")
    input_durations = {row[0]: int(row[2]) for row in input_rows[1:]}
    assert input_durations == durations, (input_durations, durations)
    input_predecessors = {
        row[0]: re.findall(r"[A-F]", row[3]) if row[3] != "无" else []
        for row in input_rows[1:]
    }
    assert input_predecessors == predecessors, (input_predecessors, predecessors)
    answer_rows = table_after(text, "| 任务 | 最早开始 | 最早结束 | 计算依据 |")
    answer_times = {}
    for row in answer_rows[1:]:
        start = int(re.search(r"\d+", row[1]).group())
        finish = int(re.search(r"\d+", row[2]).group())
        answer_times[row[0]] = (start, finish)
    assert answer_times == {task: (starts[task], finishes[task]) for task in starts}, answer_times
    assert "八个工作日的期限是否可行" in text and "达到理论下限" in text
    assert "并列关键路径" in text and "没有缓冲" in text
    assert "表9-3 E01 更新后的成果展任务清单" in text
    checks.extend(["E01 updated dependency graph is acyclic and recomputed schedule matches input/answer tables", "E01 two critical paths and zero-buffer 8-day boundary match answer text"])

    # E03: recompute the weighted totals and apply the newly stated hard constraint.
    e03 = data["E03"]
    rows = table_after(text, "| 判断项 | 权重 | 静态作品集 | 互动网页 | 嵌入式问答 |")
    scoring_rows = [row for row in rows[1:] if row[0].startswith(("按期完成", "无网络时", "后续更新"))]
    weights = [int(row[1]) for row in scoring_rows]
    assert weights == e03["weights"], weights
    candidates = list(e03["candidates"])
    scores_by_candidate = {name: [] for name in candidates}
    for row in scoring_rows:
        for i, name in enumerate(candidates, start=2):
            scores_by_candidate[name].append(int(row[i]))
    assert scores_by_candidate == e03["candidates"], scores_by_candidate
    totals = {name: sum(w * score for w, score in zip(weights, scores)) for name, scores in scores_by_candidate.items()}
    assert totals == e03["expected_weighted_totals"], totals
    total_row = row_values(rows, "加权合计，仅用于模拟比较")
    assert {name: int(total_row[i]) for i, name in enumerate(candidates, start=2)} == totals
    behavior_test = e03["offline_behavior_test"]
    feasible = [name for name in candidates if behavior_test["results"][name]["passed"]]
    assert feasible == e03["expected_feasible_candidates_after_constraint"], feasible
    assert e03["offline_hard_constraint"] is True
    assert "为硬约束" in text and "静态作品集" in text and "偏好" in text
    assert all(
        term in text
        for term in (
            "清空浏览器缓存",
            "断开Wi-Fi并冷启动",
            "找到指定项目卡并核对来源状态",
            "静态作品集从本地包启动，三张卡及状态标记均显示",
            "互动网页只显示空白框架，页面脚本不在离线包中",
            "嵌入式问答界面打开，但查询依赖远程服务",
            "只显示空白框架",
            "网络不可用",
        )
    )
    assert "minimum_offline_score" not in e03 and "offline_scores" not in e03
    assert all(str(value) in text for value in totals.values())
    assert "1分只是作者设置的偏好分，不是失败证据" in text
    assert "唯一通过的候选" in text
    checks.extend(["E03 weighted candidate scores match table and answer", "E03 offline hard-constraint filter leaves only the feasible candidate"])

    # Structural checks prevent silent loss while remaining explicit about their scope.
    section_titles = ["## 9.1 共同目标与可理解的技术表达", "## 9.2 分工、依赖与资源协调", "## 9.3 聆听、反馈与冲突处理", "## 9.4 团队决策：证据、责任与调整", "## 9.5 技术领导力：支持他人与共同复盘"]
    positions = [text.find(title) for title in section_titles]
    assert all(pos >= 0 for pos in positions) and positions == sorted(positions)
    closing_titles = ["## 章末综合训练", "## 本章回顾", "## 关键术语", "## 参考解与讨论", "## 参考文献"]
    closing_positions = [text.find(title) for title in closing_titles]
    assert all(pos >= 0 for pos in closing_positions) and closing_positions == sorted(closing_positions)
    assert "（补充提案）" in text
    markers = re.findall(r"<!-- FIGURE:(9-\d+) -->", text)
    assert markers == [f"9-{i}" for i in range(1, 6)], markers
    captions = re.findall(r"^\*\*表(9-\d+) [^*]+\*\*$", text, re.M)
    assert captions == [f"9-{i}" for i in range(1, 8)], captions
    for exercise in ("E01", "E02", "E03", "E04", "E05"):
        assert f"练习 {exercise}" in text
        assert f"### {exercise} 参考解与讨论" in text
    e04_start = text.index("### E04 参考解与讨论")
    e04_end = text.index("### E05 参考解与讨论", e04_start)
    e04_answer = text[e04_start:e04_end]
    assert "丙可能已经改了网页" not in e04_answer
    for required_step in (
        "拟议的复盘流程",
        "记录者逐项读回原始发言支持的决定、条件和责任分工",
        "相关成员确认",
        "会后",
        "复核者",
        "状态升级",
        "责任改写",
        "下次会议",
        "题面没有指定",
    ):
        assert required_step in e04_answer, f"E04 retrospective example lacks: {required_step}"
    checks.append("E04 answer removes the cross-exercise action cue and proposes a bounded read-back, confirmation, and follow-up review without inventing assigned roles")
    e05_start = text.index("### E05 参考解与讨论")
    e05_end = text.index("## 参考文献", e05_start)
    e05_answer = text[e05_start:e05_end]
    for deliverable in (
        "**一、共同目标说明**",
        "**二、任务图与交接卡**",
        "**三、决策记录**",
        "**四、更正后的会议摘要**",
        "**五、复盘示例与迁移**",
    ):
        assert deliverable in e05_answer, f"E05 answer lacks required worked deliverable: {deliverable}"
    for grounded_example in (
        "E02与E04是两组各自独立的模拟发言",
        "8个工作日",
        "静态作品集19、互动网页14、嵌入式问答12",
        "公开链接尚未确认",
        "不是E02或E04已经作出的团队决定",
        "不声称有真实项目已经运行",
    ):
        assert grounded_example in e05_answer, f"E05 example is missing a required evidence boundary: {grounded_example}"
    assert 28000 <= han_count(text) <= 40000, han_count(text)
    checks.extend(["chapter sections and closing components appear in required order", "supplement label, five unique figures, seven sequential numbered tables, and E01–E05 answer coverage present", "E05 reference route covers all five deliverables and stays within the simulated evidence", "Han-character count meets the 28,000–40,000 range after code/URL removal"])

    report = {
        "chapter": "ch09",
        "verified_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "scope": "numeric recalculation and manuscript structure only; not a teaching, source, figure, or human acceptance review",
        "status": "PASS",
        "checks": checks,
        "E01": {
            "earliest_start_day_zero_based": starts,
            "earliest_finish_day_zero_based": finishes,
            "critical_paths": critical_paths,
            "minimum_duration_days": duration,
            "deadline_days": expected["deadline_days"],
            "deadline_feasible": duration <= expected["deadline_days"],
            "buffer_days": expected["deadline_days"] - duration
        },
        "E03": {
            "weighted_totals": totals,
            "offline_behavior_test": behavior_test,
            "feasible_after_offline_hard_constraint": feasible
        },
        "manuscript_han_count_excluding_fenced_code_inline_code_and_urls": han_count(text),
        "inputs": {
            "manuscript": {"path": "manuscripts/ch09/ch09.md", "sha256": sha256(CHAPTER)},
            "exercise_data": {"path": "materials/ch09/exercise-data.json", "sha256": sha256(DATA_PATH)},
            "verifier": {"path": "materials/ch09/verify_exercises.py", "sha256": sha256(Path(__file__).resolve())}
        }
    }
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    return report


if __name__ == "__main__":
    result = verify()
    print(json.dumps(result, ensure_ascii=False, indent=2))
