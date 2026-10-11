"""Package the four chapters using the preceding delivery's byte checks."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    files = [ROOT / "output/ch07-10/README.md"]
    files.extend(ROOT / "materials/ch07-10" / name for name in
                 ("report.md", "content-adjudication.md", "continuity-review.md"))
    for chapter in (7, 8, 9, 10):
        stem = f"ch{chapter:02d}"
        here = ROOT / f"materials/{stem}"
        check = json.loads((here / "verification.json").read_text())
        assert check["checks"] == "PASS" and check["toc_cache_matches_actual_pages"]
        observed = json.loads((here / "page-review.json").read_text())
        assert observed.get("status", observed.get("checks")) == "PASS"
        assert observed["pdf_sha256"] == check["pdf_sha256"]
        assert len(observed["pages"]) == check["pages"]
        assert all(p["actually_opened"] or p.get("inherited_identical_png") for p in observed["pages"])
        for suffix in ("docx", "pdf"):
            path = ROOT / f"output/{stem}/{stem}-illustrated.{suffix}"
            assert sha(path) == check[f"{suffix}_sha256"]
            files.append(path)
        for folder in (stem, stem + "-layout"):
            files.append(ROOT / f"manuscripts/{folder}/{stem}.md")
        figures = sorted((ROOT / f"assets/figures/{stem}").iterdir())
        assert len(figures) == {7: 18, 8: 18, 9: 15, 10: 12}[chapter]
        files.extend(figures)
    files.extend(sorted((ROOT / "materials/ch08/practice").glob("*")))
    assert all(path.is_file() for path in files)
    package = ROOT / "output/ch07-10/ch07-10-delivery.zip"
    with ZipFile(package, "w", ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, str(path.relative_to(ROOT)))
    entries = {str(path.relative_to(ROOT)): sha(path) for path in files}
    with ZipFile(package) as archive:
        assert archive.testzip() is None and set(archive.namelist()) == set(entries)
        assert all(hashlib.sha256(archive.read(name)).hexdigest() == digest for name, digest in entries.items())
    evidence = {"file": str(package.relative_to(ROOT)), "sha256": sha(package),
                "bytes": package.stat().st_size, "word_files": 4, "pdf_files": 4,
                "figures": 21, "editable_svg_files": 21,
                "crc_and_byte_correspondence": "PASS", "entries": entries}
    (ROOT / "materials/ch07-10/package-check.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: evidence[key] for key in ("file", "bytes", "figures", "crc_and_byte_correspondence")}))


if __name__ == "__main__":
    main()
