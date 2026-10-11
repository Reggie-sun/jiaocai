"""Use the proven document builder with this delivery's chapter inputs."""
from pathlib import Path
import argparse
import importlib.util
import hashlib
import json
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("previous_builder", ROOT / "materials/ch04-06/build_docx.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)

# Preserve compact citations and consume journal-name emphasis without splitting
# existing bold text, code spans, or URLs.
original_inline = builder.inline
INLINE_TOKENS = re.compile(
    r"(\*\*.*?\*\*|`[^`]+`|https?://[^\s。；，]+|"
    r"(?<![\w*])\*(?!\*)[^*\n]+\*(?![\w*])|\[\d+(?:[-–,，]\d+)+\])"
)


def inline_with_ranges(paragraph, value, refs=True):
    for token in INLINE_TOKENS.split(value):
        if refs and re.fullmatch(r"\[\d+(?:[-–,，]\d+)+\]", token):
            paragraph.add_run("\u2060")
            paragraph.add_run(token).font.superscript = True
            paragraph.add_run("\u2060")
        elif re.fullmatch(r"\*(?!\*)[^*\n]+\*", token):
            paragraph.add_run(token[1:-1]).italic = True
        else:
            original_inline(paragraph, token, refs)


builder.inline = inline_with_ranges

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--chapter", type=int, choices=[7, 8, 9, 10], required=True)
    p.add_argument("--source", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--toc-pages", type=Path)
    args = p.parse_args()
    builder.CHAPTER = args.chapter
    builder.HERE = ROOT / f"materials/ch{args.chapter:02d}"
    builder.SOURCE = args.source.resolve()
    builder.TITLE = builder.SOURCE.read_text().splitlines()[0][2:]
    builder.OUTPUT = args.output.resolve()
    builder.build(json.loads(args.toc_pages.read_text()) if args.toc_pages else {})
    if args.chapter == 9:
        # Keep the observed figure and list introductions with their next
        # paragraph; preserve all text.
        doc = builder.Document(builder.OUTPUT)
        changed = []
        for index, paragraph in enumerate(doc.paragraphs):
            if paragraph.text == "来源：作者原创（教学结构图）。" and index == 53:
                paragraph.paragraph_format.keep_with_next = True
                doc.paragraphs[index + 1].paragraph_format.keep_together = True
                changed.append(index)
            elif paragraph.text == "交付物：":
                paragraph.paragraph_format.keep_with_next = True
                changed.append(index)
            elif paragraph.text == "分歧至少可能发生在四个层面：":
                paragraph.paragraph_format.keep_with_next = True
                changed.append(index)
        assert changed == [53, 145, 299], changed
        doc.save(builder.OUTPUT)
        evidence = json.loads((builder.HERE / "build.json").read_text())
        evidence["docx_sha256"] = hashlib.sha256(builder.OUTPUT.read_bytes()).hexdigest()
        evidence["pagination_corrections"] = {"CH09-PAGE-001": 53, "CH09-PAGE-002": 299, "CH09-PAGE-003": 145}
        (builder.HERE / "build.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n")
