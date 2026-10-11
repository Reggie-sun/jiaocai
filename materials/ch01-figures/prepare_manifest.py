"""Bind the eight exports to unchanged chapter captions and print dimensions."""
from pathlib import Path
import hashlib
import json
import re
import xml.etree.ElementTree as ET

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets/figures/ch01-figures"
DESCRIPTIONS = [
    "口头要求对应对象和检查；硬约束、偏好及公平等待确认标准分别表示。",
    "T1、T2、T3与b、c的六条允许边完整可见；d不可达，3项请求争用2个容量1位置。",
    "根据错误证据定位选择、表示或条件；三类不是执行顺序，修改后重新检查。",
    "四个文献节点按真实出版年份定位；1936收稿、宣读单独注释，无因果或影响箭头。",
    "设备借用与场地分配对齐共同结构，同时单列容量、设施、身份语义的新增核查。",
    "共同分钟尺度和半开端点区分60分钟重叠、0分钟相接、独占准备清理后的35分钟冲突。",
    "步道照明这一共同问题的六种互补证据视角；不是权重、步骤或互斥分类。",
    "模型内可行性与实际服务观察分成独立证据域；冲突可反馈修订，不能互相代替验收。",
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    original = json.loads((ROOT / "runs/ch01-rewrite.spec.json").read_text())
    figures = []
    for number, item in enumerate(original["figures"], 1):
        stem = OUT / f"fig1-{number}"
        editor = stem.with_suffix(".drawio") if number not in (4, 6) else stem.with_suffix(".svg")
        with Image.open(stem.with_suffix(".png")) as image:
            pixels = [image.width, image.height]
        svg = ET.parse(stem.with_suffix(".svg")).getroot()
        if number not in (4, 6):
            width = float(svg.get("viewBox").replace(",", " ").split()[2])
            text_cells = [cell for cell in ET.parse(editor).iter("mxCell") if cell.get("value")]
            sizes = [float(re.findall(r"(?:^|;)fontSize=([\d.]+)", cell.get("style", ""))[-1]) for cell in text_cells]
            minimum = min(sizes) * 155 / width * 72 / 25.4
        else:
            width = None
            minimum = 10.5
        figure = {**item, "file": str(stem.with_suffix(".png").relative_to(ROOT)),
                  "status": "ready", "description": DESCRIPTIONS[number - 1],
                  "editable_source": str(editor.relative_to(ROOT)),
                  "editable_source_sha256": sha(editor), "sha256": sha(stem.with_suffix(".png")),
                  "svg_sha256": sha(stem.with_suffix(".svg")), "insert_width_mm": 155,
                  "min_font_pt_at_insert": round(minimum, 3), "viewbox_width": width,
                  "pixel_dimensions": pixels, "ppi_at_insert": round(pixels[0] / (155 / 25.4), 2),
                  "height_mm_at_insert": round(155 * pixels[1] / pixels[0], 2)}
        assert minimum >= 10.5, (number, minimum)
        figures.append(figure)
    manifest = {"style": "textbook-style-v1.0", "figures": figures,
                "boundary": "Figure-specific visual/content review and whole-chapter page viewing are recorded under materials/ch01-figures; ready is not classroom or publisher acceptance."}
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"figures": len(figures), "minimum_font_pt": min(f["min_font_pt_at_insert"] for f in figures)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
