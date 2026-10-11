"""Reuse the three accepted adapters/checks for this bounded textual revision."""
import argparse
import difflib
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OLD = {1: "ch01-history-layout", 2: "ch02-progressive", 3: "ch03-layout"}
NAMES = {1: "第一章-计算思维-跨章审校版", 2: "第二章-AI时代计算思维的重构-跨章审校版",
         3: "第三章-计算思维与人工智能素养-跨章审校版"}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare(n):
    folder = HERE / f"ch0{n}"
    folder.mkdir(exist_ok=True)
    old = ROOT / "materials" / OLD[n]
    for name in ("figure-manifest.json", "template-parts.json", "assembly.json"):
        if (old / name).exists():
            shutil.copyfile(old / name, folder / name)
    baseline = HERE / "snapshots" / f"ch0{n}-baseline.md"
    candidate = ROOT / "manuscripts/ch01-03-review" / f"ch0{n}.md"
    a, b = baseline.read_text().splitlines(True), candidate.read_text().splitlines(True)
    replacements = []
    for group in difflib.SequenceMatcher(None, a, b, autojunk=False).get_grouped_opcodes(3):
        first, last = group[0], group[-1]
        replacements.append({"old": "".join(a[first[1]:last[2]]), "new": "".join(b[first[3]:last[4]])})
    (folder / "declared-changes.json").write_text(json.dumps({"baseline": str(baseline.relative_to(ROOT)),
        "baseline_sha256": sha(baseline), "source_sha256": sha(candidate),
        "replacements": replacements}, ensure_ascii=False, indent=2) + "\n")


def verify_delta(n):
    record = json.loads((HERE / f"ch0{n}/declared-changes.json").read_text())
    baseline = ROOT / record["baseline"]
    candidate = ROOT / "manuscripts/ch01-03-review" / f"ch0{n}.md"
    assert sha(baseline) == record["baseline_sha256"]
    assert sha(candidate) == record["source_sha256"]
    restored = candidate.read_text()
    for change in reversed(record["replacements"]):
        assert restored.count(change["new"]) == 1
        restored = restored.replace(change["new"], change["old"], 1)
    assert restored.encode() == baseline.read_bytes()


def load(n, kind):
    file = ROOT / "materials" / OLD[n] / f"{kind}.py"
    module_spec = importlib.util.spec_from_file_location(f"chapter{n}_{kind}", file)
    module = importlib.util.module_from_spec(module_spec)
    if kind == "verify_layout":
        code = file.read_text()
        if n in (1, 3):
            start = code.index('    assembly = json.loads(')
            end = code.index('    doc = Document(DOCX)', start)
            code = code[:start] + '    verify_delta()\n    assembly = {"figure_status_replacements": []}\n' + code[end:]
            code = code.replace('"baseline_prose_byte_identical": True', '"declared_changes_reversed_to_baseline": True')
            code = code.replace('"baseline_prose_exact_after_reversing_declared_changes": True', '"declared_changes_reversed_to_baseline": True')
        else:
            start = code.index('    protected = json.loads(')
            end = code.index('    reader = PdfReader', start)
            code = code[:start] + '    verify_delta()\n    protected = json.loads((HERE.parent / "protected-files.json").read_text())\n    concurrent = {}\n    assert all(sha(ROOT / name) == value for name, value in protected.items())\n' + code[end:]
        exec(compile(code, str(file), "exec"), module.__dict__)
        module.verify_delta = lambda: verify_delta(n)
    else:
        module_spec.loader.exec_module(module)
        if n == 2:
            original_heading = module.style.numbered_heading

            def balanced_heading(doc, label, text):
                if label == "2.3":
                    text = text.replace("：深度学习", "：\n深度学习", 1)
                return original_heading(doc, label, text)

            module.style.numbered_heading = balanced_heading
    module.HERE = HERE / f"ch0{n}"
    module.SOURCE = module.MANUSCRIPT = ROOT / "manuscripts/ch01-03-review" / f"ch0{n}.md"
    module.OUTPUT = module.DOCX = ROOT / "output/ch01-03-review" / (NAMES[n] + ".docx")
    return module


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("operation", choices=("prepare", "build", "verify"))
    parser.add_argument("chapter", type=int, choices=(1, 2, 3))
    parser.add_argument("--pdf", type=Path)
    parser.add_argument("--toc", type=Path)
    args = parser.parse_args()
    if args.operation == "prepare":
        prepare(args.chapter)
        verify_delta(args.chapter)
    elif args.operation == "build":
        load(args.chapter, "build_docx").build(json.loads(args.toc.read_text()) if args.toc else {})
    else:
        assert args.pdf
        load(args.chapter, "verify_layout").inspect(args.pdf, HERE / f"ch0{args.chapter}/layout-verification.json", args.toc)
