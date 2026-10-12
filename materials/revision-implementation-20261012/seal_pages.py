"""Archive actual reader observations after checking the reader's PNG manifest."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
OBSERVED = {
    2: (86, "pages-r2", "/root/content_professional", "d93b909878b9edaf69c21201dfb2cd51dd4e4e3a039831213659a4fe7c772dd1"),
    4: (74, "pages-r1", "/root/content_teaching", "4a0d49effc84fc7ea5be498b4ce35e1a2cdfc01796d75db346437bb3f8f92c4b"),
    5: (72, "pages-r1", "/root/content_teaching", "05d779e57a47dd27756ed5fa02c94e02178de68aed7b451d12b9301992cb00b4"),
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


for n, (count, directory, observer, expected) in OBSERVED.items():
    here = ROOT / f"materials/ch{n:02d}-feedback"
    pages = here / directory
    pdf = ROOT / f"output/ch{n:02d}-feedback/ch{n:02d}-feedback.pdf"
    assert sha(pages / pdf.name) == sha(pdf)
    manifest = "".join(f"page-{p}.png\t{sha(pages / f'page-{p}.png')}\n" for p in range(1, count + 1))
    assert hashlib.sha256(manifest.encode("ascii")).hexdigest() == expected
    archive = here / "final-pages.zip"
    with ZipFile(archive, "w", ZIP_DEFLATED) as out:
        for p in range(1, count + 1):
            out.write(pages / f"page-{p}.png", f"page-{p}.png")
    with ZipFile(archive) as saved:
        assert saved.testzip() is None
        assert len(saved.namelist()) == count
        assert all(hashlib.sha256(saved.read(f"page-{p}.png")).hexdigest() == sha(pages / f"page-{p}.png") for p in range(1, count + 1))
    record = {
        "chapter": n,
        "source_sha256": sha(ROOT / f"manuscripts/ch{n:02d}-feedback/ch{n:02d}.md"),
        "docx_sha256": sha(ROOT / f"output/ch{n:02d}-feedback/ch{n:02d}-feedback.docx"),
        "pdf_sha256": sha(pdf),
        "pages": count,
        "archive": str(archive.relative_to(ROOT)),
        "archive_sha256": sha(archive),
        "png_manifest_sha256": expected,
        "fresh_actual_page_observations": count,
        "inherited_identical_png_pages": 0,
        "unviewed_final_page_bytes": [],
        "rows": [{"page": p, "sha256": sha(pages / f"page-{p}.png"), "archive_member": f"page-{p}.png",
                  "observation": {"actual_view": True, "detail": "original", "observer": observer,
                                  "manifest_sha256": expected, "finding": None,
                                  "observation": "Reader reported actual individual view_image reading of every frozen page; Parent checked reported manifest and source/output bindings."}}
                 for p in range(1, count + 1)],
        "limits": "Actual rendered-image observations reported by named reader, sealed by Parent. Word-native refresh, physical print and teacher/student acceptance untested.",
    }
    (here / "page-review.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"chapter": n, "pages": count, "archive_sha256": sha(archive)}))
