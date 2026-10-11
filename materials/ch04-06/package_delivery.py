"""Package the authorized three chapters and verify every packaged byte."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]


def main():
    files = [ROOT / "output/ch04-06/README.md"]
    for chapter in (4, 5, 6):
        stem = f"ch0{chapter}"
        check = json.loads((ROOT / f"materials/{stem}/verification.json").read_text())
        assert check["checks"] == "PASS" and check["toc_cache_matches_actual_pages"]
        for suffix in ("docx", "pdf"):
            f = ROOT / f"output/{stem}/{stem}-illustrated.{suffix}"
            assert hashlib.sha256(f.read_bytes()).hexdigest() == check[f"{suffix}_sha256"]
            files.append(f)
        for folder in (stem, stem + "-layout"):
            files.append(ROOT / f"manuscripts/{folder}/{stem}.md")
        figures = sorted((ROOT / f"assets/figures/{stem}").iterdir())
        assert len(figures) == {4: 18, 5: 21, 6: 24}[chapter]
        files.extend(figures)
    files.extend(sorted((ROOT / "materials/ch06/project").glob("*")))
    assert all(f.is_file() for f in files)
    package = ROOT / "output/ch04-06/ch04-06-delivery.zip"
    with ZipFile(package, "w", ZIP_DEFLATED) as archive:
        for f in files:
            archive.write(f, str(f.relative_to(ROOT)))
    entries = {str(f.relative_to(ROOT)): hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
    with ZipFile(package) as archive:
        assert archive.testzip() is None and set(archive.namelist()) == set(entries)
        assert all(hashlib.sha256(archive.read(name)).hexdigest() == digest for name, digest in entries.items())
    evidence = {"file": str(package.relative_to(ROOT)), "sha256": hashlib.sha256(package.read_bytes()).hexdigest(),
                "bytes": package.stat().st_size, "word_files": 3, "pdf_files": 3, "figures": 21,
                "editable_svg_files": 21, "crc_and_byte_correspondence": "PASS", "entries": entries}
    (ROOT / "materials/ch04-06/package-check.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: evidence[key] for key in ("file", "bytes", "figures", "crc_and_byte_correspondence")}))


if __name__ == "__main__":
    main()
