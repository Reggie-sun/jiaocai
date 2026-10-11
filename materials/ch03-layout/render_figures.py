"""Render the five editable Chapter 3 teaching figures and print-size PNGs."""
from __future__ import annotations

from html import escape
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "materials/ch03-layout"
DATA_PATH = HERE / "figure-data.json"
MANIFEST_PATH = HERE / "figure-manifest.json"
EXPORT_PATH = HERE / "figure-export.json"
SOURCE_PATH = ROOT / "manuscripts/ch03/ch03.md"
OUT = ROOT / "assets/figures/ch03-layout"

INK = "#202326"
BLUE = "#1F4E79"
GRAY = "#555B61"
MID = "#D7DCE1"
PALE = "#F0F2F4"
WHITE = "#FFFFFF"
FONT = "Noto Sans CJK SC, sans-serif"
VIEW_WIDTH = 900
PNG_WIDTH = 2400
INSERT_MM = 155
MIN_FONT_PX = 22
MIN_STROKE_PX = 2
PPI = round(PNG_WIDTH / (INSERT_MM / 25.4))
MIN_FONT_PT = round(MIN_FONT_PX * INSERT_MM * 72 / 25.4 / VIEW_WIDTH, 2)
CHROME = Path("/usr/bin/google-chrome")


def text(x: float, y: float, value: str, size: int = 22, *, anchor: str = "middle",
         weight: str = "normal", fill: str = INK) -> str:
    if size < MIN_FONT_PX:
        raise ValueError(f"SVG text is below print-size minimum: {value!r} ({size}px)")
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
            f'font-family="{FONT}" font-size="{size}px" font-weight="{weight}" '
            f'fill="{fill}">{escape(value)}</text>')


def text_lines(x: float, y: float, values: list[str], size: int = 22, *,
               anchor: str = "middle", weight: str = "normal", fill: str = INK,
               step: int = 29) -> str:
    return "".join(text(x, y + i * step, value, size, anchor=anchor,
                       weight=weight, fill=fill) for i, value in enumerate(values))


def box(x: float, y: float, width: float, height: float, *, fill: str = WHITE,
        stroke: str = GRAY, stroke_width: float = 2, radius: int = 8,
        dash: str | None = None) -> str:
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
            f'rx="{radius}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{stroke_width}"{dash_attr}/>')


def line(x1: float, y1: float, x2: float, y2: float, *, color: str = GRAY,
         width: float = 2, dash: str | None = None, arrow: bool = False) -> str:
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    end_attr = ' marker-end="url(#arrow)"' if arrow else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{color}" stroke-width="{width}" stroke-linecap="round"'
            f'{dash_attr}{end_attr}/>')


def path(d: str, *, color: str = GRAY, width: float = 2,
         dash: str | None = None, arrow: bool = False) -> str:
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    end_attr = ' marker-end="url(#arrow)"' if arrow else ""
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-linejoin="round"{dash_attr}{end_attr}/>')


def svg_doc(height: int, caption: str, description: str, body: str) -> str:
    defs = (
        '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="5" '
        'orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L10,5 L0,10 z" '
        f'fill="{BLUE}"/></marker>'
        '<pattern id="teaching" width="10" height="10" patternUnits="userSpaceOnUse">'
        f'<rect width="10" height="10" fill="{PALE}"/>'
        f'<path d="M0 10 L10 0" stroke="{BLUE}" stroke-width="2"/></pattern>'
        '<pattern id="extra" width="10" height="10" patternUnits="userSpaceOnUse">'
        f'<rect width="10" height="10" fill="{WHITE}"/>'
        f'<path d="M0 10 L10 0 M0 0 L10 10" stroke="{GRAY}" stroke-width="2"/>'
        '</pattern></defs>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{VIEW_WIDTH}px" '
            f'height="{height}px" viewBox="0 0 {VIEW_WIDTH} {height}" role="img" '
            'aria-labelledby="title desc">'
            f'<title id="title">{escape(caption)}</title>'
            f'<desc id="desc">{escape(description)}</desc>{defs}'
            f'<rect width="{VIEW_WIDTH}" height="{height}" fill="{WHITE}"/>'
            f'<g font-family="{FONT}">{body}</g></svg>')


def figure_1(item: dict) -> str:
    body = [text(450, 38, f'同一服务目标：{item["goal"]}', 24, weight="bold")]
    stage_x = [25, 245, 465, 685]
    for i, stage in enumerate(item["stages"]):
        x = stage_x[i]
        body += [box(x, 65, 190, 103, fill=PALE if i in (0, 3) else WHITE,
                     stroke=BLUE if i in (0, 3) else GRAY),
                 text(x + 95, 101, stage["name"], 26, weight="bold", fill=BLUE),
                 text_lines(x + 95, 130, stage["question"], 22, step=25)]
        if i < 3:
            body.append(line(x + 194, 116, stage_x[i + 1] - 5, 116,
                             color=BLUE, arrow=True))
    body += [path("M780 176 V222 H120 V176", color=BLUE, arrow=True),
             line(340, 222, 340, 176, color=BLUE, arrow=True),
             text(450, 258, "测试和使用反馈可回到目标与表示", 22, weight="bold", fill=BLUE)]

    positions = [(20, 286), (315, 286), (610, 286), (165, 440), (460, 440)]
    for domain, (x, y) in zip(item["domains"], positions):
        body += [box(x, y, 270, 138, fill=WHITE, stroke=GRAY),
                 text(x + 16, y + 31, domain["name"], 24, anchor="start",
                      weight="bold", fill=BLUE),
                 text(x + 16, y + 62, f'环节：{domain["affects"].replace(" · ", "/")}',
                      22, anchor="start", weight="bold"),
                 text_lines(x + 16, y + 95, domain["lines"], 22,
                            anchor="start", step=28)]
    body += [text(450, 633, item["nonexclusive_note"], 22, weight="bold")]
    return svg_doc(670, item["caption"], item["description"], "".join(body))


def figure_2(item: dict) -> str:
    body = []
    actors = [(135, item["actors"][0]), (420, item["actors"][1]),
              (710, item["actors"][2])]
    for x, actor in actors:
        body += [box(x - 105, 40, 210, 48, fill=PALE, stroke=BLUE),
                 text(x, 72, actor, 23, weight="bold", fill=BLUE),
                 line(x, 96, x, 465, color=MID, dash="6 7")]

    body += [text(278, 129, f'① {item["steps"][0]}', 22, weight="bold"),
             line(145, 150, 408, 150, color=BLUE, arrow=True),
             text(565, 204, f'② {item["steps"][1]}', 22, weight="bold"),
             line(430, 225, 698, 225, color=BLUE, arrow=True),
             box(600, 262, 220, 78, fill=PALE, stroke=BLUE),
             text_lines(710, 293, ["③ 设备接收指令", "并执行动作"], 22,
                        weight="bold", fill=BLUE, step=30),
             text(565, 367, f'④ {item["steps"][3]}', 22, weight="bold"),
             line(700, 387, 432, 387, color=BLUE, arrow=True),
             text(278, 432, f'⑤ {item["steps"][4]}', 22, weight="bold"),
             line(408, 452, 145, 452, color=BLUE, arrow=True)]

    body += [path("M420 468 V493 H260 V516", color=GRAY, dash="7 7", arrow=True),
             box(160, 515, 520, 70, fill=WHITE, stroke=GRAY, dash="7 6"),
             text(420, 545, "若超时或离线，没有设备回传", 22, weight="bold"),
             text(420, 575, "当前状态未知", 22, weight="bold", fill=BLUE),
             text(450, 625, "未确认 ≠ 已成功；不能把“已发送”写成“已关闭”。",
                  22, weight="bold")]
    return svg_doc(650, item["caption"], item["description"], "".join(body))


def fraction(group: dict, metric: dict) -> tuple[int, int]:
    if metric["name"] == "误报率":
        return group["fp"], group["fp"] + group["tn"]
    if metric["name"] == "漏报率":
        return group["fn"], group["tp"] + group["fn"]
    return group["fn"] + group["fp"], group["tp"] + group["fn"] + group["fp"] + group["tn"]


def figure_3(item: dict) -> str:
    body = [text(450, 36, "教学模拟；A/B表示拍摄条件，不代表固有类别", 22, weight="bold")]
    panel_xs = [20, 470]
    for group, x in zip(item["groups"], panel_xs):
        body += [box(x, 55, 410, 240, fill=WHITE, stroke=GRAY),
                 text(x + 205, 88, f'{group["name"]} · {group["condition"]}',
                      23, weight="bold", fill=BLUE),
                 text(x + 197.5, 119, "判同一人", 22, weight="bold"),
                 text(x + 332.5, 119, "判不同人", 22, weight="bold"),
                 text(x + 68, 163, "实为同一", 22, weight="bold"),
                 text(x + 68, 229, "实为不同", 22, weight="bold")]
        cell_data = [(x + 135, 132, f'TP {group["tp"]}'),
                     (x + 270, 132, f'FN {group["fn"]}'),
                     (x + 135, 198, f'FP {group["fp"]}'),
                     (x + 270, 198, f'TN {group["tn"]}')]
        fills = [PALE, WHITE, WHITE, PALE]
        for (cx, cy, label), fill in zip(cell_data, fills):
            body += [box(cx, cy, 125, 58, fill=fill, stroke=GRAY, radius=4),
                     text(cx + 62.5, cy + 36, label, 22, weight="bold")]

    body += [text(450, 333, "三类比例使用共同的0–100%刻度", 23, weight="bold"),
             text(393, 375, "组A", 22, weight="bold", fill=BLUE),
             text(693, 375, "组B", 22, weight="bold", fill=BLUE)]
    bar_xs = [320, 620]
    bar_width = 145
    for x in bar_xs:
        for tick, label in zip([x, x + bar_width / 2, x + bar_width], ["0%", "50%", "100%"]):
            body += [line(tick, 414, tick, 428, color=GRAY),
                     text(tick, 403, label, 22)]
        body.append(line(x, 421, x + bar_width, 421, color=GRAY))

    row_y = [463, 555, 647]
    groups = item["groups"]
    for metric, y in zip(item["metrics"], row_y):
        body += [text(26, y + 28, metric["name"], 23, anchor="start", weight="bold"),
                 text(26, y + 58, metric["fraction"], 22, anchor="start")]
        for group, x in zip(groups, bar_xs):
            numerator, denominator = fraction(group, metric)
            ratio = numerator / denominator
            fill_width = bar_width * ratio
            body.append(box(x, y + 23, bar_width, 22, fill=PALE, stroke=GRAY, radius=2))
            if fill_width > 0:
                body.append(f'<rect x="{x}" y="{y + 23}" width="{fill_width}" height="22" '
                            f'rx="2" fill="{BLUE}" stroke="{BLUE}" stroke-width="2"/>')
            body.append(text(x + bar_width + 12, y + 42,
                             f'{round(ratio * 100)}% ({numerator}/{denominator})',
                             22, anchor="start", weight="bold"))
    body += [text(450, 739, "误报 / 漏报分母各为2；整体错分分母为4。", 22, weight="bold")]
    return svg_doc(760, item["caption"], item["description"], "".join(body))


def figure_4(item: dict) -> str:
    body = [box(300, 30, 300, 76, fill=PALE, stroke=BLUE),
            text(450, 77, item["claim"], 24, weight="bold", fill=BLUE)]
    check_xs = [20, 310, 600]
    for check, x in zip(item["checks"], check_xs):
        body += [box(x, 162, 280, 142, fill=WHITE, stroke=GRAY),
                 text(x + 140, 198, check["name"], 23, weight="bold", fill=BLUE),
                 text_lines(x + 18, 239, check["questions"], 22,
                            anchor="start", step=30)]
        body.append(line(450, 106, x + 140, 156, color=GRAY, arrow=True))

    body += [box(220, 357, 460, 88, fill=PALE, stroke=BLUE),
             text(450, 392, item["judgment"], 23, weight="bold", fill=BLUE),
             text(450, 425, "三类检查结果汇合后再选处置", 22)]
    for x in [160, 450, 740]:
        body.append(line(x, 304, 450, 336, color=GRAY))
    body.append(line(450, 336, 450, 350, color=BLUE, arrow=True))

    action_xs = [15, 237, 459, 681]
    trunk = path("M450 445 V466 H117 H783", color=BLUE)
    body.append(trunk)
    for action, x in zip(item["dispositions"], action_xs):
        body += [line(x + 102, 466, x + 102, 481, color=BLUE, arrow=True),
                 box(x, 482, 204, 119, fill=WHITE, stroke=GRAY),
                 text(x + 102, 515, action["name"], 24, weight="bold", fill=BLUE),
                 text_lines(x + 102, 549, [action["condition"][:8], action["condition"][8:]],
                            22, step=29)]
    body += [text(450, 642, item["human_judgment_note"], 22, weight="bold")]
    body += [text(450, 678, "图示路径辅助推理，不自动裁定主张可靠与否。", 22)]
    return svg_doc(700, item["caption"], item["description"], "".join(body))


def figure_5(item: dict) -> str:
    plot_x, plot_width = 300, 550
    scale = plot_width / 8
    body = [text(450, 38, "共同时间尺度：0–8小时/日", 24, weight="bold"),
            text(450, 72, "斜纹为教学需要；交叉纹为额外准备与清场0.5小时。", 22)]
    axis_y = 112
    body.append(line(plot_x, axis_y, plot_x + plot_width, axis_y, color=INK))
    for hour in range(9):
        x = plot_x + hour * scale
        body += [line(x, axis_y - 7, x, axis_y + 8, color=INK),
                 text(x, axis_y - 14, str(hour), 22)]

    candidate_hours = item["rooms"][0]["original_hours"] - item["candidate_reduction_hours"]
    for index, room in enumerate(item["rooms"]):
        y = 143 + index * 127
        teaching_end = plot_x + room["teaching_hours"] * scale
        extra_end = teaching_end + room["extra_hours"] * scale
        candidate_end = plot_x + candidate_hours * scale
        body += [line(20, y + 111, 875, y + 111, color=MID),
                 text(24, y + 28, f'教室 {room["name"]}', 23,
                      anchor="start", weight="bold", fill=BLUE),
                 text(24, y + 60, f'教学 {room["teaching_hours"]} h', 22, anchor="start"),
                 text(24, y + 91, "准备/清场 0.5 h", 22, anchor="start")]
        body += [box(plot_x, y + 2, plot_width, 30, fill=PALE, stroke=GRAY, radius=2),
                 text(plot_x + plot_width / 2, y + 25, "原亮灯 8 h", 22, weight="bold"),
                 f'<rect x="{plot_x}" y="{y + 36}" width="{room["teaching_hours"] * scale}" '
                 f'height="23" fill="url(#teaching)" stroke="{BLUE}" stroke-width="2"/>',
                 f'<rect x="{teaching_end}" y="{y + 36}" width="{room["extra_hours"] * scale}" '
                 f'height="23" fill="url(#extra)" stroke="{GRAY}" stroke-width="2"/>',
                 f'<rect x="{plot_x}" y="{y + 72}" width="{candidate_hours * scale}" '
                 f'height="25" fill="{BLUE}" stroke="{BLUE}" stroke-width="2"/>',
                 text(plot_x + candidate_hours * scale / 2, y + 93,
                      f'统一候选 {candidate_hours} h', 22, weight="bold", fill=WHITE)]
    body += [text(450, 680, "按每间教室的分段需求检查候选时间。", 22, weight="bold")]
    return svg_doc(710, item["caption"], item["description"], "".join(body))


BUILDERS = [figure_1, figure_2, figure_3, figure_4, figure_5]


def validate_data(data: dict) -> None:
    figures = data.get("figures", [])
    if len(figures) != 5 or [item.get("id") for item in figures] != [
            "图3-1", "图3-2", "图3-3", "图3-4", "图3-5"]:
        raise ValueError("Chapter 3 layout requires five ordered figure records")
    source = SOURCE_PATH.read_text(encoding="utf-8")
    f3 = figures[2]
    table_rows = re.findall(
        r'^\| (组[AB]) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+)／(\d+) \|$',
        source, re.M)
    actual_rows = [(g["name"], str(g["tp"]), str(g["fn"]), str(g["fp"]), str(g["tn"]),
                    str(g["fn"] + g["fp"]), "4") for g in f3["groups"]]
    if table_rows != actual_rows:
        raise ValueError(f"Figure 3-3 data differs from manuscript table 3-6: {table_rows}")
    for group in f3["groups"]:
        if group["tp"] + group["fn"] != 2 or group["fp"] + group["tn"] != 2:
            raise ValueError(f"Figure 3-3 denominators differ from table 3-6: {group}")

    f5 = figures[4]
    room_rows = re.findall(
        r'^\| ([ABCD]) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (0\.5) \|$',
        source, re.M)
    actual_rooms = [(r["name"], str(r["original_hours"]), str(r["teaching_hours"]), "0.5")
                    for r in f5["rooms"]]
    expected_rooms = [(row[0], row[3], row[4], row[5]) for row in room_rows]
    if expected_rooms != actual_rooms or len(room_rows) != 4:
        raise ValueError(f"Figure 3-5 room data differs from manuscript table 3-8: {room_rows}")
    if "每间每天统一少开三小时" not in source or f5["candidate_reduction_hours"] != 3:
        raise ValueError("Figure 3-5 candidate reduction differs from E05")
    candidate_hours = f5["rooms"][0]["original_hours"] - f5["candidate_reduction_hours"]
    if candidate_hours != 5 or any(r["original_hours"] - f5["candidate_reduction_hours"] != candidate_hours
                                   for r in f5["rooms"]):
        raise ValueError("Figure 3-5 must show a common five-hour candidate")


def validate_svg(svg: str, svg_path: Path) -> int:
    root = ET.fromstring(svg)
    if root.attrib.get("viewBox", "").split()[:2] != ["0", "0"]:
        raise ValueError(f"Invalid SVG viewBox: {svg_path}")
    font_sizes = [int(size) for size in re.findall(r'font-size="(\d+)px"', svg)]
    if not font_sizes or min(font_sizes) < MIN_FONT_PX:
        raise ValueError(f"Minimum SVG font failed for {svg_path.name}: {font_sizes}")
    stroke_sizes = [float(size) for size in re.findall(r'stroke-width="([\d.]+)"', svg)]
    if stroke_sizes and min(stroke_sizes) < MIN_STROKE_PX:
        raise ValueError(f"Minimum SVG line width failed for {svg_path.name}: {stroke_sizes}")
    return min(font_sizes)


def render_svg(svg_path: Path, png_path: Path, css_height: int) -> dict:
    if not CHROME.is_file():
        raise FileNotFoundError(f"local SVG renderer unavailable: {CHROME}")
    svg = svg_path.read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="ch03-layout-figure-") as td:
        tmp = Path(td)
        html_path = tmp / "figure.html"
        html_path.write_text(
            '<!doctype html><html><head><meta charset="utf-8"><style>'
            f'html,body{{margin:0;padding:0;width:{VIEW_WIDTH}px;height:{css_height}px;'
            'overflow:hidden;background:#fff}svg{display:block}</style></head><body>' + svg + '</body></html>',
            encoding="utf-8")
        command = [str(CHROME), "--headless", "--no-sandbox", "--disable-gpu",
                   "--disable-dev-shm-usage", "--hide-scrollbars",
                   f"--user-data-dir={tmp / 'profile'}", "--force-device-scale-factor=2.6666666667",
                   f"--window-size={VIEW_WIDTH},{css_height}", "--virtual-time-budget=1000",
                   f"--screenshot={png_path}", html_path.as_uri()]
        result = subprocess.run(command, capture_output=True, text=True, timeout=45)
        if result.returncode or not png_path.is_file():
            raise RuntimeError(f"SVG export failed for {svg_path.name}: {result.stderr[-1500:]}")
    with Image.open(png_path) as source:
        color = source.convert("RGB")
        if color.width != PNG_WIDTH:
            raise RuntimeError(f"Unexpected image width for {png_path}: {color.width}")
        color.save(png_path, format="PNG", dpi=(PPI, PPI), optimize=True)
        gray_path = png_path.with_name(png_path.stem + "-gray.png")
        ImageOps.grayscale(color).save(gray_path, format="PNG", dpi=(PPI, PPI), optimize=True)
        dimensions = {"width_px": color.width, "height_px": color.height}
    return {"dimensions_px": dimensions,
            "sha256": hashlib.sha256(png_path.read_bytes()).hexdigest(),
            "gray_sha256": hashlib.sha256(gray_path.read_bytes()).hexdigest(),
            "grayscale_png": gray_path}


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    validate_data(data)
    OUT.mkdir(parents=True, exist_ok=True)
    outputs = []
    export_records = []
    for item, builder in zip(data["figures"], BUILDERS):
        number = int(item["id"].split("-")[1])
        svg_path = OUT / f"fig3-{number}.svg"
        png_path = OUT / f"fig3-{number}.png"
        svg = builder(item)
        svg_path.write_text(svg, encoding="utf-8")
        min_font = validate_svg(svg, svg_path)
        height_match = re.search(r'<svg[^>]+height="(\d+)px"', svg)
        if not height_match:
            raise ValueError(f"Missing SVG height for {item['id']}")
        rendered = render_svg(svg_path, png_path, int(height_match.group(1)))
        output = {
            **{key: value for key, value in item.items()
               if key not in {"stages", "domains", "actors", "steps", "unknown", "groups",
                              "metrics", "scale", "checks", "judgment", "dispositions",
                              "human_judgment_note", "goal", "feedback", "nonexclusive_note",
                              "candidate_reduction_hours", "rooms", "student_prompt", "claim"}},
            "status": "rendered",
            "editable_source": f"assets/figures/ch03-layout/fig3-{number}.svg",
            "file": f"assets/figures/ch03-layout/fig3-{number}.png",
            "png": f"assets/figures/ch03-layout/fig3-{number}.png",
            "grayscale_png": f"assets/figures/ch03-layout/fig3-{number}-gray.png",
            "sha256": rendered["sha256"],
            "gray_sha256": rendered["gray_sha256"],
            "svg_sha256": hashlib.sha256(svg_path.read_bytes()).hexdigest(),
            "insert_width_mm": INSERT_MM,
            "viewbox_width": VIEW_WIDTH,
            "png_ppi_at_insert": PPI,
            "declared_min_label_px": min_font,
            "min_font_pt_at_insert": MIN_FONT_PT,
            "min_label_pt_at_insert": MIN_FONT_PT,
            "dimensions_px": rendered["dimensions_px"],
            "gray_semantics": "标签、位置、边框、图案、计数和共同刻度承载含义；颜色只是辅助。"
        }
        outputs.append(output)
        export_records.append({
            "id": item["id"],
            "svg": output["editable_source"],
            "png": output["png"],
            "grayscale_png": output["grayscale_png"],
            "dimensions_px": output["dimensions_px"],
            "png_ppi_at_insert": PPI,
            "sha256": output["sha256"],
            "gray_sha256": output["gray_sha256"],
            "svg_sha256": output["svg_sha256"]
        })

    manifest = {
        "style": data["style"],
        "insert_width_mm": INSERT_MM,
        "png_ppi_at_insert": PPI,
        "min_label_pt_at_insert": MIN_FONT_PT,
        "render_command": "/home/reggie/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python materials/ch03-layout/render_figures.py",
        "visual_review": {"status": "pending_actual_image_view", "items": []},
        "figures": outputs
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8")
    export = {
        "renderer": str(CHROME),
        "render_engine": "Chrome headless SVG screenshot at 900 CSS px, exported to 2400 px",
        "style": data["style"],
        "insert_width_mm": INSERT_MM,
        "png_ppi_at_insert": PPI,
        "minimum_label_pt_at_insert": MIN_FONT_PT,
        "outputs": export_records
    }
    EXPORT_PATH.write_text(json.dumps(export, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(json.dumps({"figures": len(outputs), "png_width_px": PNG_WIDTH,
                      "ppi_at_insert": PPI, "min_font_pt_at_insert": MIN_FONT_PT,
                      "outputs": [{"id": item["id"], "png": item["sha256"],
                                  "gray": item["gray_sha256"], "svg": item["svg_sha256"]}
                                 for item in outputs]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
