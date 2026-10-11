"""Rebuild all eight local exports; leave the previous chapter and pilots intact."""
from pathlib import Path
import argparse
import importlib.util
import json
import subprocess

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def export(source, binary):
    # The corrected diagnostic figure was exported to its content bounds; others use the page.
    size = "diagram" if source.stem == "fig1-3" else "page"
    for fmt in ("png", "svg", "pdf"):
        command = ["xvfb-run", "-a", str(binary), "-x", "-f", fmt,
                   "--size", size, "--border", "0", "-o", str(source.with_suffix("." + fmt)),
                   str(source), "--disable-gpu", "--no-sandbox"]
        if fmt == "png":
            command += ["--width", "2441", "--border", "0"]
        if fmt == "svg":
            command += ["--embed-svg-images"]
        if fmt == "pdf" and size == "page":
            command += ["--crop"]
        subprocess.run(command, check=True, capture_output=True, timeout=90)
    if size == "diagram":
        with Image.open(source.with_suffix(".png")) as image:
            rgb = image.convert("RGB")
            dpi = rgb.width / (155 / 25.4)
            rgb.save(source.with_suffix(".png"), dpi=(dpi, dpi))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=ROOT / "assets/figures/ch01-figures")
    parser.add_argument("--drawio", type=Path,
                        default=Path.home() / ".local/share/jiaocai-tools/drawio-32.4.1/opt/drawio/drawio")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    relations = module(HERE / "render_relations.py", "chapter_relations")
    relations.OUT = args.output_dir
    for build in (relations.fig1_1, relations.fig1_3, relations.fig1_5, relations.fig1_7, relations.fig1_8):
        source = build()
        subprocess.run(["python3", str(ROOT / "skills/drawio-skill/scripts/validate.py"),
                        str(source), "--strict", "--json"], check=True, capture_output=True)
        export(source, args.drawio)
    # Reuse the verified graph/interval renderer with this edition's data and output directory.
    pilot = module(ROOT / "materials/teaching-figures-pilot/build_figures.py", "verified_pilot")
    data = json.loads((HERE / "data.json").read_text())
    pilot.graph(args.output_dir, data, args.drawio)
    pilot.intervals(args.output_dir, data)
    for path in list(args.output_dir.glob("*candidate*")):
        path.rename(path.with_name(path.name.replace("-candidate", "")))
    timeline = module(HERE / "render_timeline.py", "chapter_timeline")
    timeline.OUT = args.output_dir
    timeline.main()
    for number in range(1, 9):
        png = args.output_dir / f"fig1-{number}.png"
        with Image.open(png) as image:
            image.convert("L").save(png.with_name(png.stem + "-grayscale.png"))
    print(json.dumps({"figures": 8, "output": str(args.output_dir)}))


if __name__ == "__main__":
    main()
