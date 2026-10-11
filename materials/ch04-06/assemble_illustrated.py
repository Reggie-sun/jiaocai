"""Insert final figure objects without changing the author's prose."""
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
    original = ROOT / f"manuscripts/ch0{chapter}/ch0{chapter}.md"
    destination = ROOT / f"manuscripts/ch0{chapter}-layout/ch0{chapter}.md"
    manifest = ROOT / f"materials/ch0{chapter}/figure-manifest.json"
    source = original.read_text()
    figures = json.loads(manifest.read_text())["figures"]
    assert "![" not in source, "Author source must not already contain image objects"
    result, inserted = source, []
    for fig in figures:
        pattern = rf"^(?:\*\*)?{re.escape(fig['id'])} {re.escape(fig['caption'])}(?:\*\*)?$"
        matches = list(re.finditer(pattern, result, flags=re.M))
        assert len(matches) == 1, (fig["id"], len(matches))
        image_path = os.path.relpath(ROOT / fig['file'], destination.parent)
        assert (destination.parent / image_path).resolve() == (ROOT / fig['file']).resolve()
        image = f"![{fig['id']} {fig['caption']}]({image_path})\n\n"
        result = result[:matches[0].start()] + image + result[matches[0].start():]
        inserted.append(image)
    restored = result
    for image in inserted:
        restored = restored.replace(image, "", 1)
    assert restored == source, "Insertion must preserve every original character"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(result)
    report = {"chapter": chapter, "original": str(original.relative_to(ROOT)), "original_sha256": sha(original), "illustrated": str(destination.relative_to(ROOT)), "illustrated_sha256": sha(destination), "manifest_sha256": sha(manifest), "figures": len(figures), "original_prose_preserved": True, "change": "Only image Markdown objects inserted directly above original figure captions."}
    (ROOT / f"materials/ch0{chapter}/assembly.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--chapter", type=int, required=True)
    assemble(parser.parse_args().chapter)
