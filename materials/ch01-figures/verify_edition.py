"""Verify the figure-only edition against its delivered source and DOCX."""
from pathlib import Path
from zipfile import ZipFile
import argparse
import copy
import hashlib
import json
import re

from docx import Document
from lxml import etree
from PIL import Image
from pypdf import PdfReader
import pdfplumber

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OLD_SOURCE = ROOT / "manuscripts/ch01-rewrite/ch01.md"
SOURCE = ROOT / "manuscripts/ch01-figures/ch01.md"
OLD_DOCX = ROOT / "output/ch01/第一章-计算思维.docx"
DOCX = ROOT / "output/ch01/第一章-计算思维-教学图新版.docx"
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
      "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
      "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def norm(text):
    return re.sub(r"\s+|\u2060|\u200b", "", text)


def normalized_document(xml):
    """Only drawing extent/description and cached PAGEREF digits may differ."""
    xml = copy.deepcopy(xml)
    for drawing in xml.findall(".//wp:inline", NS):
        for extent in (drawing.find("wp:extent", NS), drawing.find(".//a:xfrm/a:ext", NS)):
            extent.set("cx", "0"); extent.set("cy", "0")
        drawing.find("wp:docPr", NS).set("descr", "FIGURE")
    for paragraph in xml.findall(".//w:p", NS):
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
                if re.search(r"PAGEREF section_\d+", stack[-1]["code"]):
                    node.text = "PAGE"
    return etree.tostring(xml, method="c14n")


def inspect(pdf_path, output, toc_output):
    assert SOURCE.read_text().replace("assets/figures/ch01-figures/", "assets/figures/ch01-rewrite/") == OLD_SOURCE.read_text()
    assert len(re.findall(r"assets/figures/ch01-figures/fig1-[1-8]\.png", SOURCE.read_text())) == 8
    manifest = json.loads((ROOT / "assets/figures/ch01-figures/manifest.json").read_text())
    build = json.loads((HERE / "build.json").read_text())
    with ZipFile(OLD_DOCX) as old, ZipFile(DOCX) as new:
        assert old.namelist() == new.namelist()
        changed = [name for name in old.namelist() if old.read(name) != new.read(name)]
        assert sorted(changed) == build["changed_parts"] and len(changed) == 9
        old_xml = etree.fromstring(old.read("word/document.xml"))
        xml = etree.fromstring(new.read("word/document.xml"))
        assert normalized_document(old_xml) == normalized_document(xml)
        assert len(xml.findall(".//w:tbl", NS)) == 26
        assert [etree.tostring(t) for t in old_xml.findall(".//w:tbl", NS)] == [etree.tostring(t) for t in xml.findall(".//w:tbl", NS)]
        relations = {n.get("Id"): n.get("Target") for n in etree.fromstring(new.read("word/_rels/document.xml.rels"))}
        for shape, figure in zip(Document(DOCX).inline_shapes, manifest["figures"]):
            drawing = shape._inline
            path = ROOT / figure["file"]
            assert abs(shape.width.mm - 155) < .05
            target = relations[drawing.find(".//a:blip", NS).get(f"{{{NS['r']}}}embed")]
            assert new.read("word/" + target) == path.read_bytes()
            assert sha(path) == figure["sha256"]
            assert sha(ROOT / figure["editable_source"]) == figure["editable_source_sha256"]
            with Image.open(path) as image:
                assert image.width / (shape.width.mm / 25.4) >= 300
                assert abs(shape.height.mm - 155 * image.height / image.width) < .05
            assert figure["min_font_pt_at_insert"] >= 10.5
        instructions = xml.xpath("//w:instrText/text()", namespaces=NS)
        bookmarks = xml.xpath("//w:bookmarkStart/@w:name", namespaces=NS)
        refs = [re.search(r"(?:PAGE)?REF\s+(\w+)", code)[1] for code in instructions if re.search(r"(?:PAGE)?REF ", code)]
        assert all(target in bookmarks for target in refs)
        assert len(xml.findall(".//wp:inline", NS)) == 8
    protected = json.loads((HERE / "protected-source-sha256.json").read_text())
    assert all(sha(ROOT / name) == value for name, value in protected.items())
    fonts = set()
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        for obj in page["/Resources"]["/Font"].values():
            font = obj.get_object()
            for descendant in font.get("/DescendantFonts", [obj]):
                descriptor = descendant.get_object()["/FontDescriptor"].get_object()
                assert any(key in descriptor for key in ("/FontFile", "/FontFile2", "/FontFile3"))
                fonts.add(str(descriptor["/FontName"]))
    heading_pages, caption_pages, extents = {}, {}, []
    with pdfplumber.open(pdf_path) as pdf:
        for number, page in enumerate(pdf.pages, 1):
            text = norm("".join(c["text"] for c in page.chars))
            assert all(-.5 <= c["x0"] and c["x1"] <= page.width + .5 and -.5 <= c["top"] and c["bottom"] <= page.height + .5 for c in page.chars)
            assert not any(error in text for error in ("Error!", "错误!", "未找到引用", "Reference source not found"))
            footer = page.crop((0, page.height - 60, page.width, page.height)).extract_text().strip()
            assert footer == str(number), (number, footer)
            body = [c for c in page.chars if 70 < c["top"] < page.height - 70]
            extents.append({"page": number, "body_top": round(min(c["top"] for c in body), 1), "body_bottom": round(max(c["bottom"] for c in body), 1)})
            if number > 3:
                for heading in build["toc_headings"]:
                    if heading not in heading_pages and norm(heading) in text:
                        heading_pages[heading] = number
            for figure in manifest["figures"]:
                caption = figure["id"] + figure["caption"]
                if norm(caption) in text:
                    caption_pages[figure["id"]] = number
        assert len(heading_pages) == 9 and len(caption_pages) == 8
    result = {"checks": "PASS", "source_sha256": sha(SOURCE), "docx_sha256": sha(DOCX), "pdf_sha256": sha(pdf_path),
              "pages": len(reader.pages), "text_and_all_other_ooxml_unchanged": True,
              "changed_docx_parts": changed, "tables_exactly_preserved": 26, "figures_embedded_exactly": 8,
              "reference_fields": len(refs), "toc_pages": heading_pages, "caption_pages": caption_pages,
              "toc_cache_matches_actual_pages": build["toc_cached_pages"] == heading_pages,
              "all_fonts_embedded": sorted(fonts), "protected_files_unchanged": len(protected), "page_extents": extents,
              "boundary": "Executable correspondence and layout checks; actual viewing is recorded separately. Word native updates, classroom trial and paper printing not evaluated."}
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    if toc_output:
        toc_output.write_text(json.dumps(heading_pages, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("checks", "pages", "toc_cache_matches_actual_pages", "caption_pages", "protected_files_unchanged")}, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--toc-output", type=Path)
    args = parser.parse_args()
    inspect(args.pdf, args.output, args.toc_output)
