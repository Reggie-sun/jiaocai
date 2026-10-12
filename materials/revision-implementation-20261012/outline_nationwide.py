"""Preserve the original outline package while replacing school-dependent text."""
from pathlib import Path
from zipfile import ZipFile
from copy import copy
from lxml import etree
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "AI时代的计算思维--跨界创新与终身学习能力培养-教材大纲.docx"
OUTPUT = ROOT / "output/outline-feedback/教材大纲-全国版.docx"
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
REPLACEMENTS = [
    ("依托行业院校特色资源", "结合不同学科与行业的开放案例资源"),
    ("“一校一行”特色鲜明", "跨领域案例覆盖广泛"),
    ("深度融入本校优势行业", "深度融入不同领域"),
    ("本校行业特色案例", "不同领域的行业案例"),
    ("本校特色融入：", "跨领域资源融入："),
    ("阐明本课程如何利用本校（[学校名称]）在[行业领域，如：交通运输、能源电力、现代农业、金融科技等]的优势资源进行教学。",
     "阐明本课程如何利用交通运输、能源电力、现代农业、金融科技等不同领域的公开案例与可用资源进行教学，面向全国学生安排可完成的学习路径。"),
    ("【本校特色案例】", "【跨领域案例】"),
    ("西财延伸讨论", "延伸讨论"),
    ("[本校特色行业/校园生活]", "相关行业或校园生活"),
    ("[本校特色行业]", "相关行业"),
    ("[本校特色领域]", "真实问题"),
    ("本校特色行业", "相关行业"),
    ("本校优势行业", "不同领域"),
    ("突出“行业院校特色”落地：", "落实跨领域案例："),
    ("明确、具体地融入本校的优势行业", "明确、具体地融入不同领域知识"),
    ("这是区别于通用课程的核心。", "案例选择应与计算思维及跨界创新的学习目标相对应。"),
    ("结合本校特色的", "结合真实问题的"),
    ("强化本校行业特色融合", "强化跨领域知识融合"),
    ("本校特色案例", "跨领域案例"),
    ("本校特色场景", "跨领域应用场景"),
    ("强化本校特色", "强化跨领域应用"),
    ("直接嵌入本校行业资源（如农业院校→智慧农业案例，交通院校→智能交通项目）", "结合可获得的行业案例资源（如智慧农业、智能交通），根据问题与学习条件选择项目"),
    ("校本案例库：提前建设本校行业交叉案例", "跨领域案例库：提前整理不同领域的交叉案例"),
    ("利用本校实验室/云计算资源支持项目开发。", "根据可用设备和网络条件选择本地工具或适合的计算资源支持项目开发，保留无需专属实验室的基础完成路径。"),
    ("本校行业基因深度渗透——从案例、项目到评审，全程体现“一校一行”", "跨领域知识贯穿应用——从案例、项目到评审，结合不同学科与行业的问题条件"),
]


def replace_span(nodes, start, end, new):
    cursor = 0
    inserted = False
    for node in nodes:
        text = node.text or ""
        stop = cursor + len(text)
        if cursor < end and stop > start:
            left, right = max(0, start - cursor), min(len(text), end - cursor)
            node.text = text[:left] + (new if not inserted else "") + text[right:]
            node.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
            inserted = True
        cursor = stop
    assert inserted


with ZipFile(SOURCE) as archive:
    xml = etree.fromstring(archive.read("word/document.xml"))
    changes = []
    paragraphs = xml.xpath("//w:p", namespaces=NS)
    original = ["".join(p.xpath(".//w:t/text()", namespaces=NS)) for p in paragraphs]
    for index, paragraph in enumerate(paragraphs):
        nodes = paragraph.xpath(".//w:t", namespaces=NS)
        before = "".join(n.text or "" for n in nodes)
        for old, new in REPLACEMENTS:
            text = "".join(n.text or "" for n in nodes)
            starts = [m.start() for m in re.finditer(re.escape(old), text)]
            for start in reversed(starts):
                replace_span(nodes, start, start + len(old), new)
        after = "".join(n.text or "" for n in nodes)
        if before != after:
            changes.append({"paragraph_including_tables": index, "before": before, "after": after})
        assert not re.search("本校|西财|学校名称|行业院校|一校一行|校本", after), after
    fixed_tables = []
    for index, table in enumerate(xml.xpath("//w:tbl", namespaces=NS)):
        table_properties = table.find("w:tblPr", NS)
        floating = table_properties.find("w:tblpPr", NS)
        if floating is not None:
            table_properties.remove(floating)
        for row in table.findall("w:tr", NS):
            row_properties = row.find("w:trPr", NS)
            if row_properties is None:
                row_properties = etree.Element("{" + NS["w"] + "}trPr")
                row.insert(0, row_properties)
            if row_properties.find("w:cantSplit", NS) is None:
                etree.SubElement(row_properties, "{" + NS["w"] + "}cantSplit")
        first = table.find("w:tr", NS)
        if first is not None:
            properties = first.find("w:trPr", NS)
            if properties is None:
                properties = etree.Element("{" + NS["w"] + "}trPr")
                first.insert(0, properties)
            if properties.find("w:tblHeader", NS) is None:
                etree.SubElement(properties, "{" + NS["w"] + "}tblHeader")
            for paragraph in first.xpath(".//w:p", namespaces=NS):
                properties = paragraph.find("w:pPr", NS)
                if properties is None:
                    properties = etree.Element("{" + NS["w"] + "}pPr")
                    paragraph.insert(0, properties)
                if properties.find("w:keepNext", NS) is None:
                    etree.SubElement(properties, "{" + NS["w"] + "}keepNext")
            fixed_tables.append(index)
            if index in (2, 4):
                previous = table.getprevious()
                while previous is not None and previous.tag == "{" + NS["w"] + "}p":
                    properties = previous.find("w:pPr", NS)
                    if properties is None:
                        properties = etree.Element("{" + NS["w"] + "}pPr")
                        previous.insert(0, properties)
                    if properties.find("w:keepNext", NS) is None:
                        etree.SubElement(properties, "{" + NS["w"] + "}keepNext")
                    if previous.xpath(".//w:t/text()", namespaces=NS):
                        break
                    previous = previous.getprevious()
    assert len(fixed_tables) == 5
    OUTPUT.parent.mkdir(exist_ok=True, parents=True)
    with ZipFile(OUTPUT, "w") as result:
        for info in archive.infolist():
            result.writestr(copy(info), etree.tostring(xml, xml_declaration=True, encoding="UTF-8", standalone=True)
                           if info.filename == "word/document.xml" else archive.read(info.filename))
    with ZipFile(OUTPUT) as result:
        assert result.testzip() is None
        assert all(result.read(name) == archive.read(name) for name in archive.namelist() if name != "word/document.xml")
        final = etree.fromstring(result.read("word/document.xml")).xpath("//w:p", namespaces=NS)
        changed = {c["paragraph_including_tables"] for c in changes}
        assert len(final) == len(original)
        assert all("".join(p.xpath(".//w:t/text()", namespaces=NS)) == original[i]
                   for i, p in enumerate(final) if i not in changed)
record = {"source": str(SOURCE.relative_to(ROOT)), "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
          "output": str(OUTPUT.relative_to(ROOT)), "output_sha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
          "changes": changes, "unchanged_paragraphs_byte_text_identical": len(original) - len(changes),
          "other_package_parts_byte_identical": True,
          "layout_correction": {"tables": fixed_tables, "finding": "Orphaned headers in r1; r3 floating-table PDF export lost rows and split the final assessment row", "change": "Make five tables inline, repeat headers, prevent row splitting and keep headers/two titles with following rows; no text changed."},
          "scope": "School-dependent positioning and resource assumptions only; original outline retained. General instructions, titles/order except school placeholder, tables and other text preserved. Historical course-hours inconsistency remains unresolved."}
(ROOT / "materials/revision-implementation-20261012/outline-edit.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"changed_paragraphs": len(changes), "preserved_paragraphs": len(original) - len(changes)}, ensure_ascii=False))
