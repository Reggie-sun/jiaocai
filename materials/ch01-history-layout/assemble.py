"""Insert only the seven reviewed figure blocks into the retained text edition."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
BASE = ROOT / "manuscripts/ch01-history/ch01.md"
TARGET = ROOT / "manuscripts/ch01-history-layout/ch01.md"
INSERTIONS = [
    ("### 1.1.2 ", "图1-1把目录线索、原卡和内容判断分开。顺着编号找到K01、K03后，仍需阅读原文，才能判断它们是否回答了具体问题。"),
    ("### 1.1.4 ", "图1-2对照同一查找目标的三种表示与执行方式。换用表格或程序，目标、用途条件和返回标题与架位的要求仍要说清楚。"),
    ("### 1.2.8 ", "图1-3按各自的问题联系几个历史节点。图中位置仅用于组织阅读，不表示时间距离、完整计算史或单一路线的因果关系。"),
    ("### 1.2.9 ", "图1-4将三类检查并列。纸面方形的条件、执行者走过的指令步骤和真实移动的观察证据，需要分别说明，不能相互替代。"),
    ("### 1.3.2 ", "图1-5把原创简化图案与逐行标记对应起来，并另示E05采用的变化：只改动第3行第2列。它与前文的0100错读例子不同，可以同时在格子和行标记中核对这一个差异。"),
    ("### 1.3.6 ", "图1-6呈现迁移中可以保留的表示关系与必须重审的领域条件。把织造中的0/1规则用于访谈整理时，不能把语义判断也当成确定的机械动作。"),
    ("### 1.4.4 ", "图1-7让四种视角围绕同一拟标题相互补充。它们共同影响标题、材料范围与核对方式，各自提出的检查不能被其他视角代替。"),
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assemble():
    original = BASE.read_text()
    text = original
    manifest = json.loads((HERE / "figure-manifest.json").read_text())
    blocks = []
    for number, ((anchor, intro), figure) in enumerate(zip(INSERTIONS, manifest["figures"]), 1):
        assert figure["id"] == f"图1-{number}" and figure["status"] == "ready"
        match = re.search(r"(?m)^" + re.escape(anchor), text)
        assert match is not None and len(re.findall(r"(?m)^" + re.escape(anchor), text)) == 1
        block = (intro + "\n\n" + f'![{figure["description"]}](../../{figure["file"]})\n\n'
                 + f'**{figure["id"]} {figure["caption"]}**\n\n来源：{figure["source"]}\n\n')
        text = text[:match.start()] + block + text[match.start():]
        blocks.append({"figure": figure["id"], "before": anchor, "inserted_text": block})
    restored = text
    for block in blocks:
        assert restored.count(block["inserted_text"]) == 1
        restored = restored.replace(block["inserted_text"], "", 1)
    assert restored.encode() == BASE.read_bytes()
    TARGET.write_text(text)
    evidence = {"baseline": str(BASE.relative_to(ROOT)), "baseline_sha256": sha(BASE),
                "illustrated_manuscript": str(TARGET.relative_to(ROOT)), "manuscript_sha256": sha(TARGET),
                "baseline_exactly_preserved_after_removing_insertions": True, "insertions": blocks,
                "tables": [m[0] for m in re.findall(r"(?m)^\*\*(表1-\d+) (.*?)\*\*$", text)]}
    (HERE / "assembly.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"figures": len(blocks), "baseline_bytes_preserved": True}, ensure_ascii=False))


if __name__ == "__main__":
    assemble()
