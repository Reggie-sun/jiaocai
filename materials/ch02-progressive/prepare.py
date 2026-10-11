"""Assemble the progressive edition with chapter-local citation/caption order."""
from pathlib import Path
import hashlib
import json
import re
import argparse

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
MANUSCRIPTS = ROOT / "manuscripts/ch02-progressive"
NAMES = ["opening.md", *[f"s2-{i}.md" for i in range(1, 6)], "capstone.md"]
ANSWERS = [f"answers-e0{i}.md" for i in range(1, 7)]


def assemble(draft=False):
    chunks = [(MANUSCRIPTS / n).read_text().strip() for n in NAMES]
    chunks.append("## 参考解与讨论\n\n先独立完成正文练习，再按ID定位参考解。基础、应用与拓展分别核对；开放题依据材料、推理和适用范围评价，合理的不同方案可以成立。")
    for n in ANSWERS:
        s = (MANUSCRIPTS / n).read_text().strip()
        identity = n[8:11].upper()
        s = re.sub(r"^#{1,3} .*?\n", f"**{identity}参考解与讨论**\n", s, count=1)
        chunks.append(s)
    chapter = "\n\n".join(chunks) + "\n"
    ledger = json.loads((HERE / "sources.json").read_text())
    refs = {x["id"]: x["reference"] for x in ledger["sources"]}
    citations = {}

    def cite(m):
        identity = m[1]
        assert identity in refs, identity
        if identity not in citations:
            citations[identity] = len(citations) + 1
        return f"[{citations[identity]}]"

    chapter = re.sub(r"\[\[(S\d{2})\]\]", cite, chapter)
    lines = chapter.splitlines()
    result, tables, mapping = [], [], {}
    pending = None
    i = 0
    while i < len(lines):
        line = lines[i]
        caption = re.fullmatch(r"(?:\*\*)?(表2-X[A-Za-z0-9_]+) (.*?)(?:\*\*)?", line)
        if caption:
            assert pending is None, pending
            pending = (caption[1], caption[2])
            i += 1
            continue
        if line.startswith("|"):
            assert pending, f"Table needs explicit caption near {line}"
            number = len(tables) + 1
            old, title = pending
            assert old not in mapping, old
            mapping[old] = f"表2-{number}"
            pending = None
            block = []
            while i < len(lines) and lines[i].startswith("|"):
                block.append(lines[i]); i += 1
            assert re.fullmatch(r"[| :\-]+", block[1])
            tables.append({"id": f"表2-{number}", "caption": title,
                           "columns": [x.strip() for x in block[0].strip("|").split("|")]})
            result += [f"**表2-{number} {title}**", "", *block, ""]
            j = i
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j == len(lines) or not lines[j].startswith("来源："):
                result += ["来源：本书原创教学模拟与作者推演；条件见对应示例或题设。", ""]
            continue
        result.append(line); i += 1
    assert pending is None
    chapter = "\n".join(result)
    chapter = re.sub(r"表2-X[A-Za-z0-9_]+", lambda m: mapping[m[0]], chapter)
    chapter += "\n\n## 参考文献\n\n" + "\n\n".join(
        f"[{n}] {refs[sid]}" for sid, n in citations.items()) + "\n"
    chapter = re.sub(r"\n{3,}", "\n\n", chapter)
    visible = re.sub(r"```.*?```", "", chapter, flags=re.S)
    visible = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", visible)
    count = len(re.findall(r"[\u4e00-\u9fff]", visible))
    assert 28000 <= count <= 40000, count
    figures = re.findall(r"^\*?\*?图2-(\d+) (.+?)(?:\*\*)?$", chapter, flags=re.M)
    if not draft:
        manifest = json.loads((HERE / "figure-manifest.json").read_text())
        assert [int(n) for n, _ in figures] == list(range(1, len(manifest["figures"]) + 1))
    assert not re.search(r"\[\[S\d+\]\]|表2-X|TODO|TBD", chapter)
    target = MANUSCRIPTS / "ch02.md"
    target.write_text(chapter)
    record = {"manuscript_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
              "fragments": {n: hashlib.sha256((MANUSCRIPTS / n).read_bytes()).hexdigest() for n in NAMES + ANSWERS},
              "han_count_without_code_or_link_targets": count,
              "count_boundary": "章首、五节、章末及集中解答与参考文献；排除代码和链接目标，非Word或出版字数。",
              "citation_order": citations, "uncited_inventory_sources": sorted(set(refs) - set(citations)),
              "tables": tables, "figure_caption_count": len(figures), "exercise_count": 6,
              "draft_before_figures": draft}
    (HERE / "assembly.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"han_count": count, "tables": len(tables), "figures": len(figures), "references": len(citations)}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--draft", action="store_true")
    assemble(parser.parse_args().draft)
