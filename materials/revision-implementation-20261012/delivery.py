"""Bind the existing textbook adapter to this revision's owned paths."""
from pathlib import Path
import argparse
import importlib.util
import json
import re
import shutil
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
MANIFEST = {1: "ch01-03-review/ch01", 2: "ch02-progressive",
            3: "ch01-03-review/ch03", **{n: f"ch{n:02d}" for n in range(4, 11)}}


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build(n, pages):
    here = ROOT / f"materials/ch{n:02d}-feedback"
    source = ROOT / f"manuscripts/ch{n:02d}-feedback-layout/ch{n:02d}.md"
    output = ROOT / f"output/ch{n:02d}-feedback/ch{n:02d}-feedback.docx"
    shutil.copyfile(ROOT / "materials" / MANIFEST[n] / "figure-manifest.json",
                    here / "figure-manifest.json")
    if n in (2, 3):
        original = "ch02-progressive" if n == 2 else "ch03-layout"
        builder = load(f"materials/{original}/build_docx.py", "feedback_builder")
        builder.MANUSCRIPT = source
    else:
        adapter = load("materials/ch07-10/build_docx.py", "feedback_builder")
        builder = adapter.builder
    builder.CHAPTER, builder.HERE = n, here
    builder.SOURCE, builder.OUTPUT = source, output
    builder.TITLE = source.read_text().splitlines()[0][2:]
    # Preserve the proven line break for the unusually long original title.
    if n == 2:
        heading = builder.style.numbered_heading

        def balanced_heading(doc, label, text):
            if label == "2.3":
                text = text.replace("：深度学习", "：\n深度学习", 1)
            return heading(doc, label, text)

        builder.style.numbered_heading = balanced_heading
    builder.build(pages)
    if n in (2, 3):
        from docx import Document
        import hashlib
        # Keep the existing unnumbered lead-in labels with their following text.
        labels = set(re.findall(r"^### (?!E\d{2}|\d+\.\d+)(.+)$", source.read_text(), re.M))
        doc = Document(output)
        for paragraph in doc.paragraphs:
            if paragraph.text in labels:
                paragraph.paragraph_format.keep_with_next = True
            if n == 2 and paragraph._p.xpath(".//w:drawing"):
                # Match the later accepted adapters: a character indent must
                # also be reset, otherwise Word's inherited firstLineChars wins.
                from docx.shared import Pt
                from docx.oxml.ns import qn
                paragraph.paragraph_format.first_line_indent = Pt(0)
                paragraph._p.get_or_add_pPr().find(qn("w:ind")).set(qn("w:firstLineChars"), "0")
                for drawing in paragraph._p.xpath(".//wp:inline"):
                    for edge in ("T", "B", "L", "R"):
                        drawing.set("dist" + edge, "0")
        doc.save(output)
        path = here / "build.json"
        evidence = json.loads(path.read_text())
        evidence["manuscript"] = str(source.relative_to(ROOT))
        evidence["docx_sha256"] = hashlib.sha256(output.read_bytes()).hexdigest()
        evidence["unnumbered_lead_ins_keep_with_next"] = sorted(labels)
        path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n")


def verify(n, pdf, toc):
    # Reuse checks; only routing and chapter-count assumptions change.
    path = ROOT / "materials/ch07-10/verify_delivery.py"
    code = path.read_text().replace('f"materials/ch{chapter:02d}"',
                                    'f"materials/ch{chapter:02d}-feedback"')
    code = code.replace('{7: 5, 8: 6, 9: 5, 10: 3}',
                        '{1: 4, 2: 5, 3: 4, 4: 4, 5: 7, 6: 5, 7: 5, 8: 6, 9: 5, 10: 3}')
    code = code.replace('assert not any(re.search(r"(?:fig|tbl)[123]_", code) for code in codes)',
                        'assert all(not re.search(r"(?:fig|tbl)(\\d+)_", code) or int(re.search(r"(?:fig|tbl)(\\d+)_", code)[1]) == chapter for code in codes)')
    code = code.replace('r"^### (E\\d{2}) 参考解与讨论\\s*$"',
                        'r"^(?:### |\\*\\*)(E\\d{2})\\s*参考解与讨论(?:：.*|\\*\\*)?$"')
    # The existing first three chapters use bold lead-ins for these two labels.
    code = code.replace('assert f"## {name}" in source',
                        'assert f"## {name}" in source or (name in ("学习目标", "学习路线") and f"**{name}**" in source)')
    namespace = {"__name__": "feedback_checks", "__file__": str(path)}
    exec(compile(code, str(path), "exec"), namespace)
    here = ROOT / f"materials/ch{n:02d}-feedback"
    namespace["inspect"](n, ROOT / f"output/ch{n:02d}-feedback/ch{n:02d}-feedback.docx",
                         pdf, here / "layout-verification.json", toc)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("operation", choices=("build", "verify"))
    parser.add_argument("chapter", type=int, choices=range(1, 11))
    parser.add_argument("--toc", type=Path)
    parser.add_argument("--pdf", type=Path)
    args = parser.parse_args()
    if args.operation == "build":
        build(args.chapter, json.loads(args.toc.read_text()) if args.toc else {})
    else:
        assert args.pdf
        verify(args.chapter, args.pdf, args.toc)
