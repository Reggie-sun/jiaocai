"""Register closed current chapter evidence through the existing Harness CLI."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def invoke(*args):
    result = subprocess.run(["python3", "-B", "scripts/harness.py", *args], cwd=ROOT,
                            text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    return json.loads(result.stdout)


before = json.loads((ROOT / "harness.json").read_text())
assert len(before["runs"]) == 18, "One-time delivery entry; do not duplicate existing new runs"
shared = [
    "specs/revision-feedback.spec.md", "plans/revision-feedback.plan.md",
    "specs/authoring-quality.spec.md", "skills/textbook-authoring/SKILL.md",
    "skills/textbook-authoring/references/teaching-figures.md",
    "templates/textbook-style-v1.0.dotx", "materials/style-pilot/report.md",
]
shared += [str((HERE / name).relative_to(ROOT)) for name in (
    "content-adjudication.md", "content-professional-report.json", "content-teaching-report.json",
    "content-corrections.json", "verification.json", "source-receipt-check.json", "source-report.json",
    "source-receipt.json", "source-inspect.json", "source-task.json", "source-run.json",
    "notion-offline-primary.txt", "siyuan-pricing-primary.txt", "mit-ocw-primary.txt", "source-claims.txt",
    "outline-edit.json", "outline-verification.json", "outline-page-review.json", "outline-final-pages.zip",
    "delivery.py", "render_batch.py", "outline_nationwide.py", "runtime.json", "harness-tests.json",
    "ch06-project-tests.log", "ch06-project-output.txt",
)]
shared += ["output/outline-feedback/教材大纲-全国版.docx", "output/outline-feedback/教材大纲-全国版.pdf"]
reports = {}
for n in range(1, 11):
    stem = f"ch{n:02d}"
    old_spec = ROOT / f"runs/{stem}-{'crossreview' if n <= 3 else 'layout'}.spec.json"
    spec = json.loads(old_spec.read_text())
    source = ROOT / f"manuscripts/{stem}-feedback-layout/{stem}.md"
    body = source.read_text()
    spec["title"] = body.splitlines()[0][2:]
    spec["manuscript"] = str(source.relative_to(ROOT))
    spec["stage"] = "draft"
    # Existing required-content/figure contracts are preserved; the new Chapter6
    # title is intentionally generalized without changing its PBL section roles.
    assert all(item in body for item in spec["required_content"])
    materials = set(shared)
    materials.add(f"specs/{stem}.spec.md")
    materials.add(f"plans/{stem}.plan.md")
    materials.add(f"manuscripts/{stem}-feedback/{stem}.md")
    materials.add(f"output/{stem}-feedback/{stem}-feedback.docx")
    materials.add(f"output/{stem}-feedback/{stem}-feedback.pdf")
    # Chapter evidence is already closed; review/status files generated below
    # remain outside the input snapshot to avoid circular mutable proofs.
    for path in (ROOT / f"materials/{stem}-feedback").rglob("*"):
        if path.is_file():
            materials.add(str(path.relative_to(ROOT)))
    for fig in spec["figures"]:
        figure = ROOT / fig["file"]
        materials.update(str(p.relative_to(ROOT)) for p in figure.parent.glob(figure.stem + ".*"))
        materials.update(str(p.relative_to(ROOT)) for p in figure.parent.glob(figure.stem + "-gray*.png"))
    if n in (1, 3):
        materials.update("materials/ch01-03-review/" + p for p in (
            "professional-r2-recovery.json", "professional-receipt-check-r2-recovery.json", "teaching-r1.md", "teaching-r2.md", "adjudication.md", "candidate-r2.json", "candidate-r3.json"))
        materials.add(f"materials/ch01-03-review/{stem}/page-review.json")
    elif n == 10:
        materials.update(str(p.relative_to(ROOT)) for p in (ROOT / "materials/ch10").glob("content-*.md"))
        materials.add("materials/ch10/page-review.json")
    if n == 2:
        materials.update("materials/ch02-progressive/" + p for p in ("exercise-inputs.json", "exercise-verification.json", "verify_exercises.py"))
    if n in (4, 5, 6):
        materials.update(f"materials/{stem}/" + p for p in ("exercise-data.json", "author-exercise-verification.json", "verify_exercises.py"))
    if n == 6:
        materials.update(str(p.relative_to(ROOT)) for p in (ROOT / "materials/ch06/project").glob("*") if p.is_file())
    if n in (7, 8, 9, 10):
        materials.update(str(p.relative_to(ROOT)) for p in (ROOT / f"materials/{stem}").glob("*exercise*.json") if p.is_file())
    if n == 8:
        materials.update(str(p.relative_to(ROOT)) for p in (ROOT / "materials/ch08/practice").glob("*") if p.is_file())
    spec["materials"] = sorted(materials)
    assert all((ROOT / p).is_file() for p in spec["materials"])
    spec["todos"] = [
        "全国版完整图文AI初稿，chapter/draft；真实教师/学生试读、课堂试教与出版社审定尚未开展。",
        "Microsoft Word原生域刷新与实体打印未执行；改变分页或更新域后重新核对目录和页面。",
        "第八章品牌账号/移动端/全国网络可用性与学生学习成效未验证；本机五文件流程不等于品牌实操或教学效果。",
    ]
    if n == 9:
        spec["todos"].append("第九章题名与结构继续是补充提案，未获目录确认。")
    run_id = f"{stem}-feedback-20261012"
    path = ROOT / f"runs/{run_id}.spec.json"
    path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n")
    started = invoke("start", "--id", run_id, "--spec", str(path.relative_to(ROOT)))
    checked = invoke("check", "--id", run_id)
    template = invoke("review-template", "--id", run_id)
    # Parent's five-dimensional current-snapshot adjudication. The independent
    # readers' actual ranges are preserved in separate pinned records.
    template["reviewer"] = "Codex Parent /root；当前证据汇总自审，独立AI会话与继承范围见content-adjudication"
    template["review_kind"] = "ai_self"
    template["reviewed_at"] = datetime.now(timezone.utc).isoformat()
    notes = {
        "teaching": "按当前Skill/增量Spec核对全国定位、原纲角色、基础路径和独立案例；七个变化章全文首审+定向闭合见专业/教学两个真实会话封存报告；第一/三/十章旧审读只按字节等价或明确小改继承。未声称学生/课堂验收。",
        "sources": "第二章原纲与三版全文mapping及一手论文逐项记录；第八章官方页面当前核对与受管来源窄审receipt已验证；模拟与真实边界由专业会话实际审读。其余未变出处沿用已核验原记录，不以品牌可访问推断全国可用。",
        "exercises": "实际独立内容审读及数值复算；第四章E07–10与集中参考解、E07口径/E08停止条件、第5章独立提示和第9章权重已实际复查闭合；第6章原型/测试实际运行，第8章UTF-8/CSV/TSV最小本地流程已演练。题号、数据和答案的当前排版检查通过。",
        "figures": "本轮62幅已有教学图语义未变；当前路径/来源/模板尺寸/图嵌入和全部表格对应检查PASS；当前章page-review绑定PNG归档，每个最终页实际观察或严格PNG同字节继承，无未观察新页。Word原生域与打印未测试。",
        "consistency": "当前源/图文稿相同，48节原题/顺序和第四至九章32个首小节位置核对；当前Word/PDF源码哈希、目录缓存/实际页、所有页图CRC/SHA一致；新增语义finding均已闭合，Parent保留第9章补充提案身份及旧run失效历史。",
    }
    for kind, text in notes.items():
        template["checks"][kind] = {"status": "pass", "notes": f"第{n}章：" + text}
    review_file = ROOT / f"materials/{stem}-feedback/harness-review.json"
    review_file.write_text(json.dumps(template, ensure_ascii=False, indent=2) + "\n")
    reviewed = invoke("review", "--id", run_id, "--evidence", str(review_file.relative_to(ROOT)))
    accepted = invoke("accept", "--id", run_id)
    status = invoke("status", "--id", run_id)
    reports[run_id] = {"start": started, "check": checked, "review": reviewed, "accept": accepted, "status": status}
    (ROOT / f"materials/{stem}-feedback/harness-status.json").write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"run": run_id, "status": status}, ensure_ascii=False), flush=True)
after = json.loads((ROOT / "harness.json").read_text())
assert after["policy"] == before["policy"] and after["runs"][:18] == before["runs"]
assert len(after["runs"]) == 28
(HERE / "harness-delivery.json").write_text(json.dumps({"new_runs": reports, "previous_18_run_records_preserved": True,
    "policy_unchanged": True, "engine_sha256": sha(ROOT / "scripts/harness.py"), "review_kind": "ai_self", "stage": "chapter/draft"}, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"new_accepted_runs": 10, "old_records_preserved": True}))
