#!/usr/bin/env python3
"""Focused numeric and structural checks for Chapter 10 exercises."""

from __future__ import annotations

import hashlib
import itertools
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANUSCRIPT = ROOT / "manuscripts/ch10/ch10.md"
PARTS = [
    ROOT / "manuscripts/ch10/opening.md",
    ROOT / "manuscripts/ch10/s10-1.md",
    ROOT / "manuscripts/ch10/s10-2.md",
    ROOT / "manuscripts/ch10/s10-3.md",
    ROOT / "manuscripts/ch10/closing.md",
]
DATA_PATH = ROOT / "materials/ch10/exercise-data.json"
REPORT_PATH = ROOT / "materials/ch10/author-exercise-verification.json"


def fail(message: str) -> None:
    raise AssertionError(message)


def han_count(text: str) -> int:
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`[^`]*`", "", text)
    text = re.sub(r"https?://\S+", "", text)
    return len(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]", text))


def validate_plan(
    name: str,
    assignments: dict,
    reviews: list,
    tasks: dict,
    skills: dict,
    capacities: dict,
    required_review_hours: int,
) -> dict:
    assigned = [task for task_list in assignments.values() for task in task_list]
    if sorted(assigned) != sorted(tasks):
        fail(f"{name}: every current task must be assigned exactly once")

    task_owners = {
        task: member
        for member, task_list in assignments.items()
        for task in task_list
    }
    review_by_owner: dict[tuple[str, str], str] = {}
    review_hours = {member: 0 for member in capacities}
    for item in reviews:
        key = (item["task"], item["assigned_to"])
        if key in review_by_owner:
            fail(f"{name}: duplicate peer review for {key}")
        if task_owners.get(item["task"]) != item["assigned_to"]:
            fail(f"{name}: peer review does not match the task owner")
        reviewer = item["reviewer"]
        if reviewer == item["assigned_to"]:
            fail(f"{name}: a member cannot review their own task")
        if skills[item["task"]][reviewer] != 2:
            fail(f"{name}: peer reviewer must have skill value 2")
        if item["included_in_task_estimate"]:
            fail(f"{name}: the stated peer review is extra to the work-package estimate")
        if item["duration_hours"] != required_review_hours:
            fail(f"{name}: skill-1 review duration differs from the exercise rule")
        review_by_owner[key] = reviewer
        review_hours[reviewer] += item["duration_hours"]

    task_owner_hours = {}
    total_loads = {}
    remaining = {}
    for member, task_list in assignments.items():
        task_owner_hours[member] = sum(tasks[task] for task in task_list)
        total_loads[member] = task_owner_hours[member] + review_hours[member]
        remaining[member] = capacities[member] - total_loads[member]
        if remaining[member] < 0:
            fail(f"{name}: {member} exceeds stated weekly capacity")
        for task in task_list:
            skill = skills[task][member]
            if skill == 0:
                fail(f"{name}: {member} is not eligible for {task}")
            if skill == 1 and (task, member) not in review_by_owner:
                fail(f"{name}: {task} assigned at skill value 1 needs a named peer reviewer")

    if set(total_loads) != set(capacities):
        fail(f"{name}: capacity data must cover every team member")
    return {
        "task_owner_hours": task_owner_hours,
        "peer_review_hours": review_hours,
        "total_loads": total_loads,
        "remaining_hours": remaining,
        "team_total_hours": sum(total_loads.values()),
    }


def has_feasible_assignment(
    tasks: dict,
    skills: dict,
    capacities: dict,
    review_hours: int,
) -> bool:
    members = list(capacities)
    options = {
        task: [member for member in members if skills[task][member] > 0]
        for task in tasks
    }
    if any(not candidates for candidates in options.values()):
        return False

    task_names = list(tasks)
    for owners in itertools.product(*(options[task] for task in task_names)):
        owner_by_task = dict(zip(task_names, owners))
        eligible_reviewers = {}
        for task, owner in owner_by_task.items():
            if skills[task][owner] == 1:
                eligible_reviewers[task] = [
                    reviewer for reviewer in members
                    if reviewer != owner and skills[task][reviewer] == 2
                ]
                if not eligible_reviewers[task]:
                    break
        else:
            review_tasks = list(eligible_reviewers)
            reviewer_options = [eligible_reviewers[task] for task in review_tasks]
            review_choices = itertools.product(*reviewer_options) if review_tasks else [()]
            for reviewers in review_choices:
                loads = {member: 0 for member in members}
                for task, owner in owner_by_task.items():
                    loads[owner] += tasks[task]
                for reviewer in reviewers:
                    loads[reviewer] += review_hours
                if all(loads[member] <= capacities[member] for member in members):
                    return True
    return False


def main() -> int:
    data = json.loads(DATA_PATH.read_text())
    if data["chapter"] != "ch10":
        fail("exercise data must identify ch10")

    parts_text = "\n\n".join(path.read_text().strip() for path in PARTS) + "\n"
    manuscript = MANUSCRIPT.read_text()
    if manuscript != parts_text:
        fail("ch10.md is stale relative to opening, section, or closing files")

    section_titles = [
        "10.1 技术背景下的领导力内涵：愿景、影响力、赋能他人、决策力、沟通力，协作能力。聆听，欣赏，客观表达。",
        "10.2 在项目团队中展现领导力：目标设定、任务分配、冲突调解、激励成员。",
        "10.3 技术责任与伦理：在跨界应用中思考技术的边界与社会影响。",
    ]
    positions = []
    for title in section_titles:
        if manuscript.count(title) != 1:
            fail(f"required original section title missing or duplicated: {title}")
        positions.append(manuscript.index(title))
    if positions != sorted(positions):
        fail("sections are not in the required order")

    closing_order = [
        "## 章末综合训练",
        "## 本章回顾",
        "## 关键术语",
        "## 参考解与讨论",
        "## 参考文献",
    ]
    close_positions = [manuscript.index(item) for item in closing_order]
    if close_positions != sorted(close_positions):
        fail("chapter close components are not in required order")

    for exercise_id in ("E01", "E02", "E03", "E04"):
        if manuscript.count(f"练习 {exercise_id}") != 1:
            fail(f"exercise prompt missing or duplicated: {exercise_id}")
        if manuscript.count(f"### {exercise_id} 参考解与讨论") != 1:
            fail(f"detailed answer missing or duplicated: {exercise_id}")
    for concept_text in (
        "团队成员共同持有的一种信念",
        "它是团队层面的共同信念",
        "团队成员共同持有的信念，即在团队中提出问题",
    ):
        if concept_text not in manuscript:
            fail(f"psychological-safety definition lost its team-level shared-belief boundary: {concept_text}")

    table_numbers = [int(n) for n in re.findall(r"^\*\*表10-(\d+)\s+", manuscript, re.M)]
    if table_numbers != list(range(1, 14)):
        fail(f"table captions must be sequential 10-1 through 10-13; got {table_numbers}")
    table_checks = 0
    lines = manuscript.splitlines()
    for index, line in enumerate(lines):
        if re.match(r"^\*\*表10-\d+\s+", line):
            next_line = index + 1
            while next_line < len(lines) and not lines[next_line].strip():
                next_line += 1
            if next_line >= len(lines) or not lines[next_line].startswith("|"):
                fail(f"table caption is not followed by a Markdown grid: {line}")
            grid = []
            while next_line < len(lines) and lines[next_line].startswith("|"):
                grid.append([cell.strip() for cell in lines[next_line].strip().strip("|").split("|")])
                next_line += 1
            widths = {len(row) for row in grid}
            if len(widths) != 1 or len(grid) < 3:
                fail(f"table is not rectangular or lacks a body row: {line}")
            table_checks += 1

    figure_ids = re.findall(r"^<!-- FIGURE:(10-\d+) -->$", manuscript, re.M)
    if figure_ids != ["10-1", "10-2", "10-3", "10-4"]:
        fail(f"figure markers must be unique and sequential 10-1 through 10-4; got {figure_ids}")
    for figure_id in figure_ids:
        marker = f"<!-- FIGURE:{figure_id} -->"
        caption = re.search(
            rf"^{re.escape(marker)}\n\*\*图{re.escape(figure_id)}\s+.+\*\*$",
            manuscript,
            re.M,
        )
        if not caption:
            fail(f"figure marker must be followed immediately by its caption: {figure_id}")

    reference_index = manuscript.index("## 参考文献")
    references = manuscript[reference_index:]
    if [int(n) for n in re.findall(r"^\[(\d+)\]", references, re.M)] != [1, 2, 3, 4]:
        fail("bibliography numbering must be sequential [1] through [4]")
    for number in range(1, 5):
        if f"[{number}]" not in manuscript[:reference_index]:
            fail(f"bibliography item [{number}] is not cited in the chapter body")

    e02 = data["e02"]
    if sum(e02["task_hours"].values()) != e02["total_task_hours"]:
        fail("E02 total work-package hours do not match input")
    if e02["capacity_hours"]["小叶"] != 7 or e02["exercise_variant"]["capacity_hours"]["小叶"] != 4:
        fail("E02 baseline and exam-week capacity scenarios must remain separate at 7 and 4 hours")
    for expected_capacity_text in ("小叶提出自己有七小时可用于本项目", "你目前有七小时"):
        if expected_capacity_text not in manuscript:
            fail(f"E02 original case capacity does not match the seven-hour matrix: {expected_capacity_text}")
    if "小叶提出自己只有六小时可用于本项目" in manuscript or "你目前只有六小时" in manuscript:
        fail("E02 original case still contains a six-hour capacity that conflicts with the matrix")
    if "能依据技能要求、个人容量和额外复核要求说明完整方案是否可行及理由" not in manuscript:
        fail("E02 evaluation criteria must not disclose the infeasibility result")
    if "完整工作包方案为何在个人容量与必要复核约束下不可行" in manuscript:
        fail("E02 evaluation criteria prematurely disclose the infeasibility result")
    worked_results = {}
    for name, solution in e02["worked_examples"].items():
        result = validate_plan(
            name,
            solution["assignments"],
            solution["peer_reviews"],
            e02["task_hours"],
            e02["skill_matrix"],
            e02["capacity_hours"],
            e02["skill1_peer_review_hours"],
        )
        if result["total_loads"] != e02["expected_worked_loads"][name]:
            fail(f"{name}: computed member loads differ from the worked example")
        if result["remaining_hours"] != e02["expected_worked_remaining_hours"][name]:
            fail(f"{name}: computed remaining capacity differs from the worked example")
        if result["team_total_hours"] != e02["expected_worked_total_hours"][name]:
            fail(f"{name}: team workload including reviews differs from the worked example")
        worked_results[name] = result

    variant = e02["exercise_variant"]
    variant_result = validate_plan(
        "E02 independent variant",
        variant["assignments"],
        variant["peer_reviews"],
        variant["task_hours"],
        variant["skill_matrix"],
        variant["capacity_hours"],
        variant["skill1_peer_review_hours"],
    )
    if variant_result["total_loads"] != variant["expected_loads"]:
        fail("E02 independent variant member loads differ from the expected answer")
    if variant_result["remaining_hours"] != variant["expected_remaining_hours"]:
        fail("E02 independent variant remaining capacity differs from the expected answer")
    if variant_result["team_total_hours"] != variant["expected_total_hours"]:
        fail("E02 independent variant workload differs from the expected answer")
    full_scope = e02["full_scope_feasibility"]
    full_scope_feasible = has_feasible_assignment(
        e02["task_hours"],
        e02["skill_matrix"],
        full_scope["capacity_hours"],
        e02["skill1_peer_review_hours"],
    )
    if full_scope_feasible != full_scope["expected_feasible"]:
        fail("E02 full-scope feasibility result differs from exhaustive assignment check")
    branch = full_scope["infeasibility_branch"]
    branch_loads = {member: 0 for member in full_scope["capacity_hours"]}
    branch_owners = {}
    for member, task_list in branch["pre_T4_assignments"].items():
        for task in task_list:
            if task in branch_owners or e02["skill_matrix"][task][member] == 0:
                fail(f"E02 infeasibility branch has a duplicate or ineligible task owner: {task}")
            branch_owners[task] = member
            branch_loads[member] += e02["task_hours"][task]
    for item in branch["pre_T4_peer_reviews"]:
        if branch_owners.get(item["task"]) != item["assigned_to"]:
            fail("E02 infeasibility branch review does not match its task owner")
        if item["reviewer"] == item["assigned_to"] or e02["skill_matrix"][item["task"]][item["reviewer"]] != 2:
            fail("E02 infeasibility branch review lacks an eligible independent reviewer")
        branch_loads[item["reviewer"]] += e02["skill1_peer_review_hours"]
    if branch_loads != branch["expected_pre_T4_loads"]:
        fail("E02 infeasibility branch pre-T4 loads do not recompute from owners and reviews")
    next_task = branch["next_task"]
    next_owner = branch["next_owner"]
    next_reviewer = branch["next_reviewer"]
    if e02["skill_matrix"][next_task][next_owner] != 1:
        fail("E02 infeasibility branch next task must need peer review")
    if next_owner == next_reviewer or e02["skill_matrix"][next_task][next_reviewer] != 2:
        fail("E02 infeasibility branch next reviewer must be a different skill-2 member")
    branch_after = dict(branch_loads)
    branch_after[next_owner] += e02["task_hours"][next_task]
    branch_after[next_reviewer] += e02["skill1_peer_review_hours"]
    if branch_after != branch["expected_after_T4_and_review_loads"]:
        fail("E02 infeasibility branch post-T4 loads do not recompute from the task and review")
    if branch_after[next_owner] > full_scope["capacity_hours"][next_owner]:
        fail("E02 infeasibility branch incorrectly claims the task owner exceeds capacity")
    if branch_after[next_reviewer] <= full_scope["capacity_hours"][next_reviewer]:
        fail("E02 infeasibility branch reviewer must exceed the stated capacity")
    if sum(variant["optional_deferred_task_hours"].values()) != 2:
        fail("E02 scope change must defer the stated two-hour optional task")
    if variant["task_hours"]["T2a"] + variant["optional_deferred_task_hours"]["T2b"] != e02["task_hours"]["T2"]:
        fail("E02 split scope must equal the original T2 estimate")
    if not variant["deferred_scope_authorized_by_course_lead"]:
        fail("E02 variant may defer T2b only when the course lead authorized the scope change")
    for criterion in variant["minimum_acceptance"]:
        if criterion not in manuscript:
            fail(f"E02 variant no longer states the original acceptance criterion: {criterion}")
    for expected_text in (
        "小叶本周最多只能投入4小时",
        "T2a（4小时）",
        "T2b（2小时）",
        "课程负责人此前确认的原始最低验收条件",
        "两段复核各占复核者1小时",
        "均不包含在相应工作包估计中",
        "周三15:00前",
        "15:00—16:00",
        "周五10:00前",
        "10:00—11:00",
        "共24小时",
        "口头指导或导师在场不自动提升技能值",
    ):
        if expected_text not in manuscript:
            fail(f"E02 prompt or worked example lost a changed constraint: {expected_text}")
    for arithmetic in (
        "4+4+1=9小时",
        "共24小时",
        "5+4=9小时，剩余10−9=1小时",
        "剩余4−4=0小时",
        "剩余9−7=2小时",
        "剩余9−9=0小时",
        "小叶尚有3小时；T3需4小时",
        "小叶以技能值1承担时，3小时任务会使她从1小时增至4小时，仍在4小时容量内",
        "小陈已负荷9小时，复核后为10小时，超过9小时容量",
        "没有合规的逐人分配",
        "总负荷为9+4+7=20小时",
    ):
        if arithmetic not in manuscript:
            fail(f"E02 written answer does not show independently checked arithmetic: {arithmetic}")

    e03 = data["e03"]
    for expected_text in ("六条虚构活动说明", "三种虚构路线提示", "只有一周维护时间"):
        if expected_text not in manuscript:
            fail(f"E03 prompt no longer states its supplied condition: {expected_text}")
    if e03["conditions"]["external_trial_permission"] or e03["conditions"]["external_service_data_handling_known"]:
        fail("E03 scenario must retain its stated authorization and service uncertainty")
    if e03["conditions"]["accessibility_routes_professionally_verified"] or e03["conditions"]["real_student_data_in_pack"]:
        fail("E03 scenario assumptions changed; review the exercise data and answer")
    rubric = data["portfolio_rubric"]
    if rubric["dimensions"] * rubric["maximum_per_dimension"] != rubric["maximum_total"]:
        fail("portfolio rubric maximum-total arithmetic is inconsistent")
    if "最高24分" not in manuscript:
        fail("portfolio rubric total in manuscript differs from exercise data")

    e03_answer_start = manuscript.index("### E03 参考解与讨论")
    e03_answer_end = manuscript.index("### E04 参考解与讨论", e03_answer_start)
    e03_answer = manuscript[e03_answer_start:e03_answer_end]
    proposed_risk_records = {}
    for function in ("GOVERN", "MAP", "MEASURE", "MANAGE"):
        line = next((item for item in e03_answer.splitlines() if item.startswith(f"- **{function}**：")), None)
        if line is None:
            fail(f"E03 proposed risk record is missing: {function}")
        for field in ("拟议责任主体", "检查问题：", "暂停条件："):
            if field not in line:
                fail(f"E03 {function} record lacks {field}")
        proposed_risk_records[function] = True
    for boundary in ("不是已获批准的任命", "这些检查尚未执行，不能写成实测通过", "合成资料情境"):
        if boundary not in e03_answer:
            fail(f"E03 proposed risk records lost their simulation boundary: {boundary}")

    count = han_count(manuscript)
    if not 28000 <= count <= 40000:
        fail(f"Han-character count outside chapter requirement: {count}")

    result = {
        "chapter": "ch10",
        "verified_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "scope": "numeric recalculation and manuscript structure only; not a teaching, source, figure, or human acceptance review",
        "status": "PASS",
        "checks": [
            "opening/section/closing files exactly match the assembled manuscript",
            "required section titles and chapter close components appear in order",
            "E01-E04 each have an independent prompt and a detailed chapter-end answer",
            "all 13 sequential table captions introduce rectangular Markdown grids",
            "four unique sequential figure markers immediately introduce matching captions",
            "four sequential bibliography items are cited in the chapter body",
            "E02 worked examples and independent variant recompute task, review, capacity, and scope arithmetic; exhaustive search and a focused T4 branch check full-scope infeasibility",
            "psychological safety is described as a team-level shared belief; individual experience is only a clue",
            "E03 simulated scenario conditions and E04 rubric total match exercise data",
            "Han-character count is within the 28,000–40,000 chapter range after code/URL removal",
        ],
        "E02": {
            "original_work_package_hours": e02["total_task_hours"],
            "worked_examples": worked_results,
            "independent_variant": variant_result,
            "full_scope_feasible_under_new_capacity_and_review_rule": full_scope_feasible,
            "full_scope_infeasibility_branch": {
                "pre_T4_loads": branch_loads,
                "after_T4_and_required_review_loads": branch_after,
                "owner_fits_capacity": branch_after[next_owner] <= full_scope["capacity_hours"][next_owner],
                "reviewer_exceeds_capacity": branch_after[next_reviewer] > full_scope["capacity_hours"][next_reviewer],
            },
            "skill1_peer_review_hours": e02["skill1_peer_review_hours"],
            "deferred_optional_hours": sum(variant["optional_deferred_task_hours"].values()),
        },
        "E03": {
            "synthetic_activity_descriptions": e03["synthetic_activity_descriptions"],
            "synthetic_route_prompts": e03["synthetic_route_prompts"],
            "maintenance_weeks": e03["maintenance_weeks"],
            "external_trial_permission": e03["conditions"]["external_trial_permission"],
            "accessibility_routes_professionally_verified": e03["conditions"]["accessibility_routes_professionally_verified"],
            "proposed_risk_record_functions": list(proposed_risk_records),
        },
        "E04_rubric_maximum_total": rubric["maximum_total"],
        "table_count": table_checks,
        "figure_ids": figure_ids,
        "manuscript_han_count_excluding_fenced_code_inline_code_and_urls": count,
        "inputs": {
            "manuscript": {
                "path": str(MANUSCRIPT.relative_to(ROOT)),
                "sha256": hashlib.sha256(MANUSCRIPT.read_bytes()).hexdigest(),
            },
            "exercise_data": {
                "path": str(DATA_PATH.relative_to(ROOT)),
                "sha256": hashlib.sha256(DATA_PATH.read_bytes()).hexdigest(),
            },
            "verifier": {
                "path": str(Path(__file__).relative_to(ROOT)),
                "sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            },
        },
    }
    REPORT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(f"PASS: {count} Han characters; {table_checks} rectangular tables; {len(figure_ids)} figure markers; E02 arithmetic verified")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, OSError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
