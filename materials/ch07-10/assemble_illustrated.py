"""Replace agreed figure slots while preserving all other author manuscript bytes."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assemble(chapter):
    original = ROOT / f"manuscripts/ch{chapter:02d}/ch{chapter:02d}.md"
    target = ROOT / f"manuscripts/ch{chapter:02d}-layout/ch{chapter:02d}.md"
    manifest = ROOT / f"materials/ch{chapter:02d}/figure-manifest.json"
    figures = json.loads(manifest.read_text())["figures"]
    source = original.read_text()
    assert "![" not in source
    markers = re.findall(r"<!-- FIGURE:(\d+-\d+) -->", source)
    assert markers == [fig["id"][1:] for fig in figures], markers
    result = source
    substitutions = []
    for fig in figures:
        assert f'**{fig["id"]} {fig["caption"]}**' in source
        assert fig["source"] in source and fig["description"] in source
        marker = f'<!-- FIGURE:{fig["id"][1:]} -->'
        asset = ROOT / fig["file"]
        assert asset.exists() and sha(asset) == fig["sha256"]
        relative = os.path.relpath(asset, target.parent)
        image = f'![{fig["id"]} {fig["caption"]}]({relative})'
        assert source.count(marker) == 1
        result = result.replace(marker, image, 1)
        substitutions.append((marker, image))
    restored = result
    for marker, image in substitutions:
        restored = restored.replace(image, marker, 1)
    assert restored == source
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(result)
    report = {"chapter": chapter, "original": str(original.relative_to(ROOT)),
              "original_sha256": sha(original), "illustrated": str(target.relative_to(ROOT)),
              "illustrated_sha256": sha(target), "manifest_sha256": sha(manifest),
              "figures": len(figures), "original_prose_preserved": True,
              "change": "Only agreed figure comment slots replaced with image objects."}
    (manifest.parent / "assembly.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--chapter", type=int, choices=[7, 8, 9, 10], required=True)
    args = parser.parse_args()
    assemble(args.chapter)
