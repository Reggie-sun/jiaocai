"""Focused semantic, print and source-preservation evidence for the two samples."""
from pathlib import Path
from itertools import product
from zipfile import ZipFile
import hashlib
import json
import re
import xml.etree.ElementTree as ET

from PIL import Image
import pypdf

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
FIG=ROOT/"assets/figures/teaching-pilot"


def main():
    data=json.loads((HERE/"data.json").read_text())
    baseline=json.loads((HERE/"protected-source-sha256.json").read_text())
    changed=[p for p,h in baseline.items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
    assert not changed,changed
    edges={(n.attrib["source"],n.attrib["target"]) for n in ET.parse(FIG/"fig1-2-candidate.drawio").iter("mxCell") if n.get("edge")=="1"}
    expected={(r,p) for r,positions in data["bottleneck"]["allowed"].items() for p in positions}
    assert edges==expected==set(product(["T1","T2","T3"],["b","c"]))
    assert not any("d" in pair for pair in edges)
    assignments=list(product(*[data["bottleneck"]["allowed"][r] for r in ["T1","T2","T3"]]))
    feasible=[a for a in assignments if len(set(a))==3]
    assert len(assignments)==8 and not feasible
    assert data["bottleneck"]["capacity_per_position"]==1
    intervals=[]
    for case in data["intervals"]["cases"]:
        a=case.get("effective_A",case["A"])
        b=case.get("effective_B",case["B"])
        start,end=max(a[0],b[0]),min(a[1],b[1])
        overlap=[start,end] if start<end else None
        assert overlap==case["expected_overlap"]
        intervals.append({"id":case["id"],"overlap_minutes":max(0,end-start),"overlap":overlap})
    assert [x["overlap_minutes"] for x in intervals]==[60,0,35]
    assert data["intervals"]["cases"][2]["effective_A"]==[540,680]
    assert data["intervals"]["cases"][2]["effective_B"]==[645,720]
    expanded=data["intervals"]["cases"][2]
    assert expanded["effective_A"][1]==expanded["A"][1]+expanded["A_cleanup_minutes"]
    assert expanded["effective_B"][0]==expanded["B"][0]-expanded["B_preparation_minutes"]
    for figure in json.loads((FIG/"manifest.json").read_text())["figures"]:
        for path,sha in figure["files"].items():
            assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha,path
    images=[]
    for number in (2,6):
        p=FIG/f"fig1-{number}-candidate.png"
        with Image.open(p) as im:
            im.load()
            ppi=im.width/(155/25.4)
            assert ppi>=300
            if im.mode=="RGBA":assert im.getchannel("A").getextrema()==(255,255)
            images.append({"figure":number,"pixels":im.size,"ppi_at_155mm":round(ppi,2),"sha256":hashlib.sha256(p.read_bytes()).hexdigest()})
    graph=ET.parse(FIG/"fig1-2-candidate.svg").getroot()
    graph_width=float(graph.attrib["viewBox"].split()[2])
    graph_source=(FIG/"fig1-2-candidate.svg").read_text()
    graph_font_sizes=[float(x) for x in re.findall(r"font-size: ([0-9.]+)px",graph_source)]
    minimum_graph_pt=min(graph_font_sizes)*155/25.4*72/graph_width
    assert minimum_graph_pt>=10.5
    time_svg=(FIG/"fig1-6-candidate.svg").read_text()
    assert "Noto Sans CJK SC" in time_svg
    assert "foreignObject" not in time_svg
    width_pt=float(re.search(r'width="([0-9.]+)pt"',time_svg)[1])
    assert abs(width_pt-155/25.4*72)<.01
    # Matplotlib viewBox units equal the pt width, retaining 10.5 pt at insertion.
    sizes=[float(v) for v in re.findall(r"font-size: ([0-9.]+)px",time_svg)]
    assert sizes and min(sizes)>=10.5
    docx=ROOT/"output/teaching-figures-pilot/教学图对照试排.docx"
    with ZipFile(docx) as z:
        body=ET.fromstring(z.read("word/document.xml"))
        ns={"w":"http://schemas.openxmlformats.org/wordprocessingml/2006/main","wp":"http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"}
        widths=[int(n.get("cx")) for n in body.findall(".//wp:extent",ns)]
        assert widths==[155*36000]*4
        instructions=[n.text or "" for n in body.findall(".//w:instrText",ns)]
        assert sum("SEQ Figure" in n for n in instructions)==4
        assert sum("REF " in n for n in instructions)==4
        styles_hash=hashlib.sha256(z.read("word/styles.xml")).hexdigest()
    with ZipFile(ROOT/"templates/textbook-style-v1.0.dotx") as z:
        assert styles_hash==hashlib.sha256(z.read("word/styles.xml")).hexdigest()
    pdf=ROOT/"output/teaching-figures-pilot/教学图对照试排.pdf"
    pages=pypdf.PdfReader(pdf).pages
    assert len(pages)==4,len(pages)
    for index,(number,label) in enumerate([(2,"原图"),(2,"独立候选"),(6,"原图"),(6,"独立候选")]):
        text=pages[index].extract_text()
        assert f"图1-{number}" in text.replace(" ","")
        assert label in text
        assert "来源" in text
    report={"protected_files":len(baseline),"protected_changed":changed,"allowed_edges":sorted(edges),"candidate_combinations":len(assignments),"feasible_assignments":len(feasible),"intervals":intervals,"images":images,"graph_min_text_pt_at_155mm":round(minimum_graph_pt,2),"time_min_text_pt_at_155mm":min(sizes),"graph_svg_foreignObject":"foreignObject" in graph_source,"graph_edit_owner":".drawio; Word uses PNG rather than foreignObject SVG","docx_images_width_mm":155,"docx_styles_identical_to_dotx":True,"native_captions":4,"native_refs":4,"pdf_pages":4,"visual_review":"separate actual Parent observation in report.md; this script does not establish visual/teaching acceptance"}
    (HERE/"verification.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(report,ensure_ascii=False))


if __name__=="__main__":main()
