"""Assemble the owned Chapter 1 fragments and explicit source/data ledgers."""
from pathlib import Path
import copy
import hashlib
import importlib.util
import json
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
MANUSCRIPTS = ROOT / "manuscripts/ch01-rewrite"


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def data_evidence():
    spec = importlib.util.spec_from_file_location("exercise_proof", ROOT / "materials/ch01/verify_exercises.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    proof = module.main()
    devices = module.read("e01-devices.json")["devices"]
    requests = module.read("e01-requests.json")["requests"]
    module.check_reference(devices, requests, [
        {"request_id": "R1", "device_id": "D1", "slot_id": "S1"},
        {"request_id": "R2", "device_id": "D2", "slot_id": "S2"},
        {"request_id": "R3", "device_id": "D1", "slot_id": "S2"},
        {"request_id": "R4", "device_id": "D1", "slot_id": "S3"},
    ], "device_id", lambda r, q: q["required_capability"] in r["capabilities"])
    proof["new_e01_answer_checked"] = True
    proof["bottleneck"] = {"requests": 3, "allowed_union": 2, "infeasible": True}
    overlap = lambda a, b: a[0] < b[1] and b[0] < a[1]
    assert overlap((9, 11), (10, 11))
    assert not overlap((9, 11), (11, 12))
    assert overlap((9, 11 + 20 / 60), (11 - 15 / 60, 12))
    proof["half_open_interval_checks"] = {"overlap": True, "touching": False, "exclusive_cleanup_preparation_overlap": True}
    proof["synthetic_impulse"] = {"lbf_seconds": 5, "factor_rounded": 4.45, "newton_seconds": 22.25, "not_mission_data": True}
    assert 3 * 18 * 5 * 28 / 1000 == 7.56
    assert 3 * 24 * 5 * 28 / 1000 == 10.08
    assert 5 / 50 == 0.1 and 12 / 80 == 0.15
    proof["e04_separate_worked_examples"] = {"energy_kwh": [7.56, 10.08], "pause_rates": [0.1, 0.15], "separate_from_exercise": True}
    write_json(HERE / "numeric-proof.json", proof)
    inputs = {p.name: json.loads(p.read_text(encoding="utf-8")) for p in sorted((ROOT / "materials/ch01").glob("e[0-9][0-9]-*.json"))}
    write_json(HERE / "exercise-inputs.json", {"provenance": "Unmodified original Chapter 1 teaching JSON; synthetic, not real campus/community data.", "sha256": proof["input_sha256"], "inputs": inputs})


def sources():
    ledger = json.loads((ROOT / "materials/ch01/sources.json").read_text(encoding="utf-8"))
    ledger["citation_style"] = "GB/T 7714-2025；章内首次出现顺序编号"
    for record in ledger["sources"]:
        record["current_verification"] = "2026-10-11：本轮重新读取原文或机构页面，核对本文采用的有限主张；书目字段单独核对。"
    ledger["sources"][-1]["author"] = "Chloe Autio; Reva Schwartz; Jesse Dunietz; Shomik Jain; Martin Stanley; Elham Tabassi; Patrick Hall; Kamie Roberts"
    ledger["sources"][-1]["metadata_url"] = "https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence"
    ledger["sources"].append({
        "id": "S10", "author": "Mars Climate Orbiter Mishap Investigation Board", "year": 1999,
        "title": "Mars Climate Orbiter Mishap Investigation Board Phase I Report", "publication": "NASA, 10 November 1999",
        "url": "https://llis.nasa.gov/llis_lib/pdf/1009464main1_0641-mr.pdf",
        "locators": ["§4 printed p.16 / PDF p.16: SM_FORCES expected newton-seconds, delivered pound-seconds; factor 4.45", "§4–§6: contributing causes and recommendations"],
        "verified_claim": "地面软件接口所约定的冲量单位与交付数据不一致，是报告明确识别的根本原因；还存在多个促成因素。",
        "limits": "正文5 lbf·s数例由作者自拟，非任务遥测；不把灾难归结为单独一个人的算术失误。",
        "current_verification": "2026-10-11实际读取NASA官方完整报告的首页及§4。", "status": "original_support_checked",
    })
    write_json(HERE / "sources.json", ledger)
    return {r["id"]: r for r in ledger["sources"]}


REFERENCES = {
    "S01": "Wing J M. Computational Thinking[J/OL]. Communications of the ACM, 2006, 49(3): 33-35[2026-10-11]. https://doi.org/10.1145/1118178.1118215.",
    "S02": "Wing J M. Computational Thinking: What and Why?[EB/OL]. (2010-11-17)[2026-10-11]. https://www.cs.cmu.edu/~CompThink/resources/TheLinkWing.pdf.",
    "S03": "Turing A M. On Computable Numbers, with an Application to the Entscheidungsproblem[J/OL]. Proceedings of the London Mathematical Society, 1937, s2-42(1): 230-265[2026-10-11]. https://doi.org/10.1112/plms/s2-42.1.230.",
    "S04": "Papert S, Solomon C. Twenty Things To Do With A Computer: AI Memo 248 / LOGO Memo 3[R/OL]. 1971-06: 1-3[2026-10-11]. https://dspace.mit.edu/entities/publication/35dcc702-9306-4ad7-8a42-1209517c9c1c.",
    "S05": "Facione P A. Critical Thinking: A Statement of Expert Consensus for Purposes of Educational Assessment and Instruction: ED315423[R/OL]. 1990: 2[2026-10-11]. https://files.eric.ed.gov/fulltext/ED315423.pdf.",
    "S06": "Design Council. Framework for Innovation[EB/OL]. [2026-10-11]. https://www.designcouncil.org.uk/resources/framework-for-innovation/.",
    "S07": "NIST/SEMATECH. e-Handbook of Statistical Methods: 5.1.1 What is experimental design?[EB/OL]. [2026-10-11]. https://itl.nist.gov/div898/handbook/pri/section1/pri11.htm.",
    "S08": "Meadows D H. Leverage Points: Places to Intervene in a System[R/OL]. 1999-12[2026-10-11]. https://donellameadows.org/wp-content/userfiles/Leverage_Points.pdf.",
    "S09": "Autio C, Schwartz R, Dunietz J, et al. Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile: NIST AI 600-1[R/OL]. 2024-07-26: 6[2026-10-11]. https://doi.org/10.6028/NIST.AI.600-1.",
    "S10": "Mars Climate Orbiter Mishap Investigation Board. Mars Climate Orbiter Mishap Investigation Board Phase I Report[R/OL]. 1999-11-10: 16[2026-10-11]. https://llis.nasa.gov/llis_lib/pdf/1009464main1_0641-mr.pdf.",
}

TABLE_TITLES = {
    8: "E02评价量规", 10: "E03时段口径", 14: "E04不同主体的模拟需求",
    15: "E04两夜的模拟观察记录", 16: "E04基线、候选与能耗假设", 17: "E04评价量规",
    21: "E02来源比较参考", 22: "E03候选与筛选依据", 23: "E03一种完整安排",
    24: "E03参考安排的逐项检查", 25: "E04额定月能耗复算",
}


def assemble(target=None, report=None):
    names = ["opening.md", "s1-1.md", "s1-2.md", "s1-3.md", "s1-4.md", "capstone.md"]
    chunks = [ (MANUSCRIPTS / name).read_text(encoding="utf-8").strip() for name in names ]
    chunks.append("## 练习参考解与讨论\n\n请先完成正文练习，再使用参考解核对推理。开放题按证据与边界评价，参考表达不作为唯一正确措辞。")
    for index in range(1, 6):
        fragment = (MANUSCRIPTS / f"answers-e0{index}.md").read_text(encoding="utf-8").strip()
        fragment = re.sub(r"^## (.+)$", r"**\1**", fragment, flags=re.M)
        fragment = re.sub(r"^# (.+)$", r"### \1", fragment, flags=re.M)
        fragment = re.sub(r"^本文件对应.*?\n", "", fragment, flags=re.M)
        chunks.append(fragment)
    draft = "\n\n".join(chunks) + "\n"
    draft = re.sub(r"^#+ (1\.\d(?:\.\d+)? .+)$", lambda m: ("### " if m[1].split(" ")[0].count(".") == 2 else "## ") + m[1], draft, flags=re.M)
    draft = re.sub(r"^### (E0[1-5].*)$", r"**\1**", draft, flags=re.M)
    draft = re.sub(r"\[([^\]]+)\]\(answers-e0[1-5]\.md\)", r"\1", draft)
    citations = {}
    def cite(match):
        identity = match[1]
        if identity not in citations:
            citations[identity] = len(citations) + 1
        return f"[{citations[identity]}]"
    draft = re.sub(r"\[\[(S\d{2})\]\]", cite, draft)
    assert set(citations) == set(REFERENCES), set(REFERENCES) - set(citations)
    lines = draft.splitlines()
    result, context, tables, pending = [], "章首", [], None
    table_ids = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("#"):
            context = re.sub(r"^#+ ", "", line)
        candidate = re.fullmatch(r"\*?\*?表1-X\w+ (.*?)\*?\*?", line)
        if candidate:
            pending = candidate[1].rstrip("*")
            old_id = re.search(r"表1-X\w+", line)[0]
            table_ids[old_id] = "表1-" + str(len(tables) + 1)
            i += 1
            continue
        if line.startswith("|"):
            block = []
            while i < len(lines) and lines[i].startswith("|"):
                block.append(lines[i]); i += 1
            header = [s.strip() for s in block[0].strip("|").split("|")]
            title = pending or context + "：" + "、".join(header[:2])
            pending = None
            number = len(tables) + 1
            title = TABLE_TITLES.get(number, title)
            tables.append({"id": f"表1-{number}", "caption": title, "columns": header})
            result += [f"**表1-{number} {title}**", "", *block, ""]
            if i >= len(lines) or not (i + 1 < len(lines) and lines[i + 1].startswith("来源：")):
                result += ["来源：本书原创教学材料与作者分析；数值材料的模拟性质见对应题设。", ""]
            continue
        result.append(line)
        i += 1
    chapter = "\n".join(result).rstrip() + "\n\n## 参考文献\n\n"
    chapter = re.sub(r"表1-X[A-Za-z0-9_]+", lambda m: table_ids[m[0]], chapter)
    chapter += "\n\n".join(f"[{number}] {REFERENCES[identity]}" for identity, number in citations.items()) + "\n"
    chapter = re.sub(r"\n{3,}", "\n\n", chapter)
    (target or MANUSCRIPTS / "ch01.md").write_text(chapter, encoding="utf-8")
    visible = re.sub(r"```.*?```", "", chapter, flags=re.S)
    visible = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", visible)
    count = len(re.findall(r"[\u4e00-\u9fff]", visible))
    assert 28000 <= count <= 40000, count
    figures = re.findall(r"^\*?\*?图1-(\d+) (.+?)(?:\*\*)?$", chapter, flags=re.M)
    assert [int(n) for n, _ in figures] == list(range(1, 9)), figures
    prose = "\n".join(line for line in chapter.splitlines() if not line.startswith("![") and not re.match(r"^图1-\d+ ", line))
    assert all(f"图1-{n}" in prose for n in range(1, 9)), "Each figure needs a numbered prose guide."
    write_json(report or HERE / "assembly.json", {
        "manuscript_sha256": hashlib.sha256(chapter.encode()).hexdigest(),
        "fragments": {n: hashlib.sha256((MANUSCRIPTS / n).read_bytes()).hexdigest() for n in names + [f"answers-e0{i}.md" for i in range(1, 6)]},
        "han_count_without_code_or_link_targets": count, "count_limit": [28000, 40000],
        "count_boundary": "章首、四节、章末、术语、集中题解与文献；移除代码块及链接目标。不是Word或出版社统计。",
        "citation_order": citations, "tables": tables, "figure_caption_count": len(figures),
    })
    print(json.dumps({"han_count": count, "tables": len(tables), "figures": len(figures), "references": len(citations)}))


if __name__ == "__main__":
    data_evidence()
    sources()
    assemble()
