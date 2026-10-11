"""Package the checked PDF, editable diagrams and exact page evidence."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUTPUT = ROOT / "output/ch03-layout"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def page_archive(snapshot, destination, selected=None):
    rows = snapshot["pages"]
    if selected is not None:
        rows = [row for row in rows if row["page"] in selected]
    with ZipFile(destination, "w", ZIP_DEFLATED) as archive:
        for row in rows:
            source = Path(row["file"])
            assert sha(source) == row["sha256"]
            archive.write(source, f'page-{row["page"]}.png')
    with ZipFile(destination) as archive:
        assert len(archive.namelist()) == len(rows)
        for row in rows:
            assert hashlib.sha256(archive.read(f'page-{row["page"]}.png')).hexdigest() == row["sha256"]
    return {"file": str(destination.relative_to(ROOT)), "sha256": sha(destination), "pages": len(rows)}


def main():
    layout = json.loads((HERE / "layout-final.json").read_text())
    final = json.loads((HERE / "page-snapshot-final.json").read_text())
    assert layout["checks"] == "PASS" and layout["toc_cache_matches_actual_pages"]
    assert final["pdf_sha256"] == layout["pdf_sha256"]
    pdf = OUTPUT / "第三章-计算思维与人工智能素养.pdf"
    assert sha(Path(final["pdf"])) == final["pdf_sha256"]
    shutil.copyfile(final["pdf"], pdf)
    assert sha(pdf) == layout["pdf_sha256"]
    assert sha(OUTPUT / "第三章-计算思维与人工智能素养.docx") == layout["docx_sha256"]
    manifest = json.loads((HERE / "figure-manifest.json").read_text())
    package = OUTPUT / "第三章-五幅教学图.zip"
    with ZipFile(package, "w", ZIP_DEFLATED) as archive:
        for figure in manifest["figures"]:
            assert figure["status"] == "ready"
            for key, digest in [("editable_source", "svg_sha256"), ("file", "sha256"), ("grayscale_png", "gray_sha256")]:
                path = ROOT / figure[key]
                assert sha(path) == figure[digest]
                archive.write(path, path.name)
        archive.write(HERE / "figure-data.json", "figure-data.json")
        lines = ["# Chapter 3 Teaching Figures", "", "五幅原创教学图；每幅含可编辑SVG、2400px彩图及灰度PNG。", "", "155mm插入宽度约393ppi，最小文字约10.74pt。修改图义或数据后须重新导出并核对正文。", ""]
        lines += [f'- {figure["id"]} {figure["caption"]}。来源：{figure["source"]}' for figure in manifest["figures"]]
        archive.writestr("README.md", "\n".join(lines) + "\n")
    with ZipFile(package) as archive:
        for figure in manifest["figures"]:
            for key, digest in [("editable_source", "svg_sha256"), ("file", "sha256"), ("grayscale_png", "gray_sha256")]:
                assert hashlib.sha256(archive.read(Path(figure[key]).name)).hexdigest() == figure[digest]
    snapshots = HERE / "snapshots"
    records = [page_archive(final, snapshots / "final-pages.zip")]
    records.append(page_archive(json.loads((HERE / "page-snapshot-r2.json").read_text()), snapshots / "prior-pages-r2.zip"))
    records.append(page_archive(json.loads((HERE / "page-snapshot-r4.json").read_text()), snapshots / "targeted-pages-r4.zip", [50, 59]))
    old = json.loads((HERE / "page-snapshot-r2.json").read_text())
    assert sha(Path(old["pdf"])) == old["pdf_sha256"]
    shutil.copyfile(old["pdf"], snapshots / "page-review-r2.pdf")
    files = [pdf, OUTPUT / "第三章-计算思维与人工智能素养.docx", package]
    (HERE / "package-check.json").write_text(json.dumps({"checks": "PASS", "deliverables": [{"file": str(path.relative_to(ROOT)), "sha256": sha(path), "bytes": path.stat().st_size} for path in files], "page_archives": records}, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
