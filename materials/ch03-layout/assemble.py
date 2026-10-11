"""Insert the five figure blocks while preserving the reviewed text byte-for-byte."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
BASE = ROOT / "manuscripts/ch03/ch03.md"
TARGET = ROOT / "manuscripts/ch03-layout/ch03.md"
INSERTIONS = [
    ("### 3.1.4 ", "图3-1把领域条件与设计环节联系起来。沿着具体条件检查表示和评价，观察一种知识如何改变其他环节；图中关系是本书教学分析，不是某次真实研发的组织记录。"),
    ("### 3.1.5 ", "图3-2区分发出指令、设备执行与确认返回。跟随指令和反馈的不同方向，检查权限发生在哪一步，以及确认缺失时为什么只能记录为未知。"),
    ("### 3.2.4 ", "图3-3对照表3-6的两组模拟结果。分别读取整体错误、误报与漏报的分母，再比较同一尺度上的比例；拍摄条件标签不代表人的固有类别，也不证明差异的原因。"),
    ("### 3.3.5 ", "图3-4从一个候选主张追溯事实材料、数量与推理、影响对象。检查后的保留、修正、待调查或暂停需要人说明理由；箭头表示检查汇合与处置路径，不表示工具自动作出裁决。"),
    ("### 3.3.9 ", "图3-5将E05的照明条件放在共同时间轴上。图中条带表示每日时长，不指定真实上下课钟点；把统一减少3小时后的可用时长与各室需要对齐，判断该候选能否满足条件。"),
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assemble():
    text = BASE.read_text(encoding="utf-8")
    replacements = [
        {"old": "图3-1（规划）可用一条带有回返箭头的路径呈现", "new": "图3-1用一条带有回返箭头的路径呈现"},
        {"old": "此图尚待后期制作；当前段落已经给出完整文字解释，阅读不依赖图片。", "new": "图中关系可与上述文字逐项核对。"},
    ]
    for replacement in replacements:
        assert text.count(replacement["old"]) == 1
        text = text.replace(replacement["old"], replacement["new"], 1)
    manifest = json.loads((HERE / "figure-manifest.json").read_text())
    assert len(manifest["figures"]) == 5
    blocks = []
    for number, ((anchor, intro), figure) in enumerate(zip(INSERTIONS, manifest["figures"]), 1):
        assert figure["id"] == f"图3-{number}" and figure["status"] == "ready"
        matches = list(re.finditer(r"(?m)^" + re.escape(anchor), text))
        assert len(matches) == 1, anchor
        block = (intro + "\n\n" + f'![{figure["description"]}](../../{figure["file"]})\n\n'
                 + f'**{figure["id"]} {figure["caption"]}**\n\n来源：{figure["source"]}\n\n')
        text = text[:matches[0].start()] + block + text[matches[0].start():]
        blocks.append({"figure": figure["id"], "before": anchor, "inserted_text": block})
    restored = text
    for block in blocks:
        assert restored.count(block["inserted_text"]) == 1
        restored = restored.replace(block["inserted_text"], "", 1)
    for replacement in replacements:
        assert restored.count(replacement["new"]) == 1
        restored = restored.replace(replacement["new"], replacement["old"], 1)
    assert restored.encode() == BASE.read_bytes()
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(text, encoding="utf-8")
    evidence = {"baseline": str(BASE.relative_to(ROOT)), "baseline_sha256": sha(BASE),
                "illustrated_manuscript": str(TARGET.relative_to(ROOT)), "manuscript_sha256": sha(TARGET),
                "baseline_exactly_preserved_after_reversing_declared_changes": True,
                "insertions": blocks, "figure_status_replacements": replacements,
                "tables": [m[0] for m in re.findall(r"(?m)^\*\*(表3-\d+) (.*?)\*\*$", text)]}
    (HERE / "assembly.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"figures": len(blocks), "baseline_bytes_preserved": True}))


if __name__ == "__main__":
    assemble()
