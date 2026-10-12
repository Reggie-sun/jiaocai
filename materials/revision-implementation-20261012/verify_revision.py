"""Current-byte, artifact and preservation checks for the authorized revision."""
from pathlib import Path
from zipfile import ZipFile
import hashlib
import importlib.util
import json
import re

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("current_harness", ROOT / "scripts/harness.py")
harness = importlib.util.module_from_spec(spec)
spec.loader.exec_module(harness)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


old = read(HERE / "preservation-before.json")
allowed_changed = {"教材编写现状与目的.md", "harness.json"}
preserved = [name for name, digest in old["tracked"].items() if name not in allowed_changed]
assert all(sha(ROOT / name) == old["tracked"][name] for name in preserved)
foreign = old.get("untracked", old.get("foreign", {}))
if isinstance(foreign, dict):
    assert all(sha(ROOT / name) == digest for name, digest in foreign.items())
inventory = read(ROOT / "materials/revision-feedback-20261012/section-inventory.json")["chapters"]
chapters, cases, total_pages, fresh, inherited = [], [], 0, 0, 0
for n in range(1, 11):
    source = ROOT / f"manuscripts/ch{n:02d}-feedback/ch{n:02d}.md"
    layout = ROOT / f"manuscripts/ch{n:02d}-feedback-layout/ch{n:02d}.md"
    here = ROOT / f"materials/ch{n:02d}-feedback"
    text = source.read_text()
    assert source.read_bytes() == layout.read_bytes()
    sections = re.findall(r"^## (\d+\.\d+ .+)$", text, re.M)
    baseline = [s["section"] + " " + s["title"] for s in inventory[n - 1]["sections"]]
    assert sections == baseline, (n, sections, baseline)
    visible = harness.visible_markdown(text)
    publication_count = len(re.findall(r"[\u4e00-\u9fff]", re.sub(r"https?://\S+", "", visible)))
    harness_count = len(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff\U00020000-\U0003134f]", visible))
    assert 28000 <= publication_count <= 40000, (n, publication_count)
    assert not re.search(r"西南财经|西南财大|西财|本校特色|本校优势|学校名称|校本资源|校本案例", text)
    if n == 9:
        assert "补充提案" in text.splitlines()[0]
    images = harness.image_paths(ROOT, source, visible)
    assert all(p.is_file() for p in images)
    verification = read(here / "layout-verification.json")
    review = read(here / "page-review.json")
    assert verification["checks"] == "PASS"
    assert verification["toc_cache_matches_actual_pages"] is True
    for key, path in (("source_sha256", source),
                      ("docx_sha256", ROOT / f"output/ch{n:02d}-feedback/ch{n:02d}-feedback.docx"),
                      ("pdf_sha256", ROOT / f"output/ch{n:02d}-feedback/ch{n:02d}-feedback.pdf")):
        assert verification[key] == review[key] == sha(path), (n, key)
    assert review["pages"] == verification["pages"]
    assert review["unviewed_final_page_bytes"] == []
    archive = ROOT / review["archive"]
    assert review["archive_sha256"] == sha(archive)
    rows = review["rows"]
    assert [r["page"] for r in rows] == list(range(1, review["pages"] + 1))
    with ZipFile(archive) as z:
        assert z.testzip() is None
        assert len(z.namelist()) == len(rows)
        for r in rows:
            member = r.get("archive_member", r.get("file"))
            assert hashlib.sha256(z.read(member)).hexdigest() == r["sha256"]
    fresh_count = review["fresh_actual_page_observations"] + review.get("parent_actual_page_observations", 0)
    inherited_count = review["inherited_identical_png_pages"]
    assert fresh_count + inherited_count == review["pages"]
    fresh += fresh_count
    inherited += inherited_count
    total_pages += review["pages"]
    if 4 <= n <= 9:
        for section in sections:
            label = section.split(" ", 1)[0]
            chunk = re.split(r"^## \d+\.\d+ ", text.split("## " + section, 1)[1], maxsplit=1, flags=re.M)[0]
            first = re.search(r"^### (\d+\.\d+\.\d+ .+)$", chunk, re.M)
            assert first and first[1].startswith(label + ".1 ")
            following = chunk[first.end():].split("\n### ", 1)[0].strip()
            assert len(following) > 200
            cases.append({"chapter": n, "section": section, "first_subsection": first[1],
                          "first_case_excerpt": following[:700], "status": "Mapped actual text; teaching meaning assessed by independent readers"})
    chapters.append({"chapter": n, "title": text.splitlines()[0][2:], "source": str(source.relative_to(ROOT)),
                     "source_sha256": sha(source), "layout_sha256": sha(layout),
                     "han_characters_approx": publication_count, "harness_han_characters_approx": harness_count,
                     "sections": len(sections), "figures": len(images), "pages": review["pages"],
                     "fresh_actual_observations": fresh_count, "inherited_identical_png_pages": inherited_count,
                     "docx_sha256": review["docx_sha256"], "pdf_sha256": review["pdf_sha256"],
                     "layout_verification_sha256": sha(here / "layout-verification.json"),
                     "page_review_sha256": sha(here / "page-review.json")})
assert sum(c["sections"] for c in chapters) == 48
assert len(cases) == 32
assert sum(c["figures"] for c in chapters) == 62
assert total_pages == 732
for name in ("professional", "teaching"):
    r = read(HERE / f"content-{name}-report.json")
    assert r["blocking_findings_remaining"] == []
    for n, digest in r["final_candidate_sha256"].items():
        assert sha(ROOT / f"manuscripts/ch{int(n):02d}-feedback/ch{int(n):02d}.md") == digest
    assert all(sha(ROOT / p) == digest for p, digest in r["initial_full_read"].items())
record = {"checks": "PASS", "chapters": chapters, "case_positions": cases,
          "count_method": "Remove Markdown comments/fenced code and URL strings; count U+4E00–U+9FFF, including headings/captions/tables/references. Harness count separately uses its native wider Han range without URL removal. Neither equals publisher or Word character counting.",
          "total_han_characters_approx": sum(c["han_characters_approx"] for c in chapters),
          "total_sections": 48, "section_case_positions_ch04_ch09": 32, "total_figures": 62,
          "total_chapter_pages": total_pages, "fresh_actual_page_observations": fresh,
          "inherited_identical_png_pages": inherited, "unviewed_final_page_bytes": [],
          "protected_tracked_files": len(preserved), "protected_foreign_files": len(foreign),
          "allowed_changed_tracked": sorted(allowed_changed), "original_source_docx_and_template_preserved": True,
          "scope": "Parent current-byte/structure/closed-evidence audit; not a replacement for actual content or page reading. Outline QA and package/Harness results are separate records."}
(HERE / "verification.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({k: record[k] for k in ("checks", "total_han_characters_approx", "total_chapter_pages", "fresh_actual_page_observations", "inherited_identical_png_pages", "protected_tracked_files", "protected_foreign_files")}))
