"""Package editable chapter delivery and verify every archived byte."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUTPUT = ROOT / "output/revision-feedback-20261012"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    delivery = json.loads((HERE / "harness-delivery.json").read_text())
    assert len(delivery["new_runs"]) == 10
    assert all(r["status"]["runs"][0]["effective_state"] == "accepted" and not r["status"]["stale"]
               for r in delivery["new_runs"].values())
    files = {OUTPUT / "README.md", HERE / "report.md", HERE / "content-adjudication.md",
             HERE / "verification.json", HERE / "content-professional-report.json", HERE / "content-teaching-report.json",
             HERE / "outline-edit.json", HERE / "outline-verification.json", HERE / "outline-page-review.json",
             ROOT / "output/outline-feedback/教材大纲-全国版.docx", ROOT / "output/outline-feedback/教材大纲-全国版.pdf",
             ROOT / "templates/textbook-style-v1.0.dotx"}
    figure_files, figure_count = set(), 0
    for n in range(1,11):
        stem = f"ch{n:02d}"
        check = json.loads((ROOT / f"materials/{stem}-feedback/layout-verification.json").read_text())
        assert check["checks"] == "PASS" and check["toc_cache_matches_actual_pages"]
        for suffix in ("docx", "pdf"):
            path = ROOT / f"output/{stem}-feedback/{stem}-feedback.{suffix}"
            assert sha(path) == check[suffix + "_sha256"]
            files.add(path)
        files.update(ROOT / f"manuscripts/{stem}-feedback{suffix}/{stem}.md" for suffix in ("", "-layout"))
        spec = json.loads((ROOT / f"runs/{stem}-feedback-20261012.spec.json").read_text())
        figure_count += len(spec["figures"])
        for figure in spec["figures"]:
            p = ROOT / figure["file"]
            figure_files.update(x for x in p.parent.glob(p.stem + ".*") if x.is_file())
            figure_files.update(x for x in p.parent.glob(p.stem + "-gray*.png") if x.is_file())
        files.update(ROOT / f"materials/{stem}-feedback/{name}" for name in
                     ("layout-verification.json", "page-review.json", "harness-review.json", "harness-status.json"))
        manifest = ROOT / f"materials/{stem}-feedback/figure-manifest.json"
        if not manifest.is_file():
            manifest = ROOT / ("materials/ch01-03-review/ch01/figure-manifest.json" if n == 1
                               else "materials/ch10/figure-manifest.json")
        files.add(manifest)
    files.update(figure_files)
    files.update(p for p in (ROOT / "materials/ch06/project").glob("*") if p.is_file())
    files.update(p for p in (ROOT / "materials/ch08/practice").glob("*") if p.is_file())
    files.update(p for p in (ROOT / "materials/ch08-feedback/local-workflow").glob("*") if p.is_file())
    files.add(ROOT / "materials/ch08-feedback/workflow-verification.json")
    files.update(ROOT / f"materials/{stem}/{name}" for stem in ("ch01-rewrite", "ch02-progressive")
                 for name in ("exercise-inputs.json", "exercise-verification.json")
                 if (ROOT / f"materials/{stem}/{name}").is_file())
    files.update(ROOT / f"materials/ch{n:02d}/{name}" for n in (3,4,5,6,7,8,9,10)
                 for name in ("exercise-data.json", "author-exercise-verification.json")
                 if (ROOT / f"materials/ch{n:02d}/{name}").is_file())
    assert all(p.is_file() for p in files), [str(p.relative_to(ROOT)) for p in files if not p.is_file()]
    assert figure_count == 62
    assert len([p for p in figure_files if p.suffix == ".svg"]) == 62
    package = OUTPUT / "全国版教材修订包.zip"
    entries = {str(p.relative_to(ROOT)): sha(p) for p in sorted(files)}
    with ZipFile(package, "w", ZIP_DEFLATED) as z:
        for p in sorted(files):
            z.write(p, str(p.relative_to(ROOT)))
    with ZipFile(package) as z:
        assert z.testzip() is None
        assert set(z.namelist()) == set(entries)
        assert all(hashlib.sha256(z.read(name)).hexdigest() == digest for name, digest in entries.items())
    record = {"file": str(package.relative_to(ROOT)), "sha256": sha(package), "bytes": package.stat().st_size,
              "word_files": 11, "pdf_files": 11, "chapter_markdown_files": 20,
              "figures": 62, "editable_svg_files": 62, "figure_assets": len(figure_files),
              "crc_and_byte_correspondence": "PASS", "entries": entries,
              "scope": "Nationwide AI draft delivery. Page PNG archives stay in project evidence, not duplicated in user package; no publishing."}
    (HERE / "package-check.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: record[k] for k in ("file", "bytes", "word_files", "pdf_files", "figures", "crc_and_byte_correspondence")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
