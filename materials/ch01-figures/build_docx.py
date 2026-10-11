"""Replace eight illustrations in the delivered DOCX, preserving its native styles/fields."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import argparse
import hashlib
import json
import re

from lxml import etree
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OLD = ROOT / "output/ch01/第一章-计算思维.docx"
OUT = ROOT / "output/ch01/第一章-计算思维-教学图新版.docx"
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
      "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
      "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}


def update_toc(body, pages, headings):
    changed = []
    for paragraph in body.findall(".//w:p", NS):
        stack = []
        for node in paragraph.iter():
            if node.tag == f"{{{NS['w']}}}fldChar":
                kind = node.get(f"{{{NS['w']}}}fldCharType")
                if kind == "begin":
                    stack.append({"code": "", "result": False})
                elif kind == "separate" and stack:
                    stack[-1]["result"] = True
                elif kind == "end" and stack:
                    stack.pop()
            elif node.tag == f"{{{NS['w']}}}instrText" and stack:
                stack[-1]["code"] += node.text or ""
            elif node.tag == f"{{{NS['w']}}}t" and stack and stack[-1]["result"]:
                match = re.search(r"PAGEREF section_(\d+)", stack[-1]["code"])
                if match:
                    index = int(match[1])
                    node.text = str(pages[headings[index]])
                    changed.append(index)
    assert sorted(changed) == list(range(len(headings))), changed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--toc-pages", type=Path)
    args = parser.parse_args()
    manifest = json.loads((ROOT / "assets/figures/ch01-figures/manifest.json").read_text())
    original_build = json.loads((ROOT / "materials/ch01-rewrite/build.json").read_text())
    pages = json.loads(args.toc_pages.read_text()) if args.toc_pages else original_build["toc_cached_pages"]
    with ZipFile(OLD) as original:
        document = etree.fromstring(original.read("word/document.xml"))
        relationships = etree.fromstring(original.read("word/_rels/document.xml.rels"))
        targets = {n.get("Id"): n.get("Target") for n in relationships}
        drawings = document.findall(".//wp:inline", NS)
        assert len(drawings) == len(manifest["figures"]) == 8
        replacements = {}
        for drawing, figure in zip(drawings, manifest["figures"]):
            path = ROOT / figure["file"]
            target = targets[drawing.find(".//a:blip", NS).get(f"{{{NS['r']}}}embed")]
            assert target.startswith("media/") and target.endswith(".png"), target
            assert "word/" + target not in replacements
            replacements["word/" + target] = path.read_bytes()
            with Image.open(path) as image:
                width = 155 * 36000
                height = round(width * image.height / image.width)
            drawing.find("wp:extent", NS).set("cx", str(width))
            drawing.find("wp:extent", NS).set("cy", str(height))
            extent = drawing.find(".//a:xfrm/a:ext", NS)
            extent.set("cx", str(width)); extent.set("cy", str(height))
            drawing.find("wp:docPr", NS).set("descr", figure["description"])
        update_toc(document, pages, original_build["toc_headings"])
        replacements["word/document.xml"] = etree.tostring(document, xml_declaration=True, encoding="UTF-8", standalone=True)
        OUT.parent.mkdir(parents=True, exist_ok=True)
        with ZipFile(OUT, "w", ZIP_DEFLATED) as output:
            for item in original.infolist():
                output.writestr(item, replacements.get(item.filename, original.read(item.filename)))
    report = {"base_docx": str(OLD.relative_to(ROOT)), "base_sha256": hashlib.sha256(OLD.read_bytes()).hexdigest(),
              "docx_sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(), "style": "textbook-style-v1.0",
              "changed_parts": sorted(replacements), "toc_cached_pages": pages,
              "toc_headings": original_build["toc_headings"],
              "method": "Reuse delivered template-based DOCX; replace eight PNG media/extent/alt descriptions and current PAGEREF cache only. Native styles, numbering, captions, refs and all other text/parts preserved.",
              "word_native_execution": "NOT_EVALUATED"}
    (HERE / "build.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"output": str(OUT), "figures": 8}))


if __name__ == "__main__":
    main()
