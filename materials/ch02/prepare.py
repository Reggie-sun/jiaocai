"""Assemble Chapter 2; reuse the existing authoring conventions without changing owners."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
MANUSCRIPTS = ROOT / "manuscripts/ch02"
NAMES = ["opening.md", *[f"s2-{i}.md" for i in range(1, 6)], "capstone.md"]
TABLE_TITLES = [
    "E01有向道路与通行条件", "流程阶段与模块边界的不同观察角度",
    "E02交付环节与依赖", "模式的不同表示及其边界", "E03模拟观察记录",
    "六节点示例的有向道路", "六节点示例的Dijkstra推演", "E04有向道路",
    "E05固定请求上的路线结果", "E06模拟参访地图的道路",
    "E02各环节的最早开始与完成", "E03规则在开发集与测试集上的指标",
    "E04的Dijkstra逐轮距离记录",
]


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def assemble():
    chunks = [(MANUSCRIPTS / name).read_text(encoding="utf-8").strip() for name in NAMES]
    chunks.append("## 参考解与讨论\n\n先独立完成正文练习，再核对以下推演。开放题按证据、推理和适用边界评价；合理的不同表达与设计可以成立。")
    answers = [f"answers-e0{i}.md" for i in range(1, 7)]
    for name in answers:
        fragment = (MANUSCRIPTS / name).read_text(encoding="utf-8").strip()
        identity = re.search(r"E0[1-6]", name)[0] if re.search(r"E0[1-6]", name) else name[8:11].upper()
        fragment = re.sub(r"^#{1,3} .*?\n", f"**{identity}参考解与讨论**\n", fragment, count=1)
        chunks.append(fragment)
    draft = "\n\n".join(chunks) + "\n"
    ledger = json.loads((HERE / "sources.json").read_text(encoding="utf-8"))
    references = {r["id"]: r["reference"] for r in ledger["sources"]}
    citations = {}
    def cite(match):
        identity = match[1]
        if identity not in citations:
            citations[identity] = len(citations) + 1
        return f"[{citations[identity]}]"
    draft = re.sub(r"\[\[(S\d{2})\]\]", cite, draft)
    assert set(citations) == set(references), set(references) - set(citations)
    lines = draft.splitlines()
    result, tables, old_ids = [], [], {}
    i = 0
    while i < len(lines):
        line = lines[i]
        provisional = re.fullmatch(r"\*?\*?表2-X\w+ (.*?)\*?\*?", line)
        if provisional:
            old_ids[re.search(r"表2-X\w+", line)[0]] = f"表2-{len(tables) + 1}"
            i += 1
            continue
        if line.startswith("|"):
            block = []
            while i < len(lines) and lines[i].startswith("|"):
                block.append(lines[i]); i += 1
            assert len(block) > 1
            if not re.fullmatch(r"[| :\-]+", block[1]):
                block.insert(1, "|" + "---|" * (len(block[0].split("|")) - 2))
            number = len(tables) + 1
            title = TABLE_TITLES[number - 1]
            header = [s.strip() for s in block[0].strip("|").split("|")]
            tables.append({"id": f"表2-{number}", "caption": title, "columns": header})
            result += [f"**表2-{number} {title}**", "", *block, ""]
            j = i
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j >= len(lines) or not lines[j].startswith("来源："):
                result += ["来源：本书原创教学材料与作者推演；模拟数值的条件见对应题设。", ""]
            continue
        result.append(line)
        i += 1
    chapter = "\n".join(result).rstrip() + "\n\n## 参考文献\n\n"
    chapter = re.sub(r"表2-X[A-Za-z0-9_]+", lambda m: old_ids[m[0]], chapter)
    chapter += "\n\n".join(f"[{number}] {references[identity]}" for identity, number in citations.items()) + "\n"
    chapter = re.sub(r"\n{3,}", "\n\n", chapter)
    target = MANUSCRIPTS / "ch02.md"
    target.write_text(chapter, encoding="utf-8")
    visible = re.sub(r"```.*?```", "", chapter, flags=re.S)
    visible = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", visible)
    count = len(re.findall(r"[\u4e00-\u9fff]", visible))
    assert 28000 <= count <= 40000, count
    figures = re.findall(r"^\*?\*?图2-(\d+) (.+?)(?:\*\*)?$", chapter, flags=re.M)
    assert [int(n) for n, _ in figures] == list(range(1, 9)), figures
    assert len(tables) == len(TABLE_TITLES)
    assert not re.search(r"\[\[S\d+\]\]|表2-X|TODO|TBD", chapter)
    write_json(HERE / "assembly.json", {
        "manuscript_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
        "fragments": {n: hashlib.sha256((MANUSCRIPTS / n).read_bytes()).hexdigest() for n in NAMES + answers},
        "han_count_without_code_or_link_targets": count,
        "count_boundary": "章首、五节、综合训练、回顾、术语、六份题解、文献；移除代码块和链接目标。",
        "citation_order": citations, "tables": tables,
        "figure_caption_count": len(figures), "exercise_count": 6,
    })
    print(json.dumps({"han_count": count, "tables": len(tables), "figures": len(figures), "references": len(citations)}))


if __name__ == "__main__":
    assemble()
