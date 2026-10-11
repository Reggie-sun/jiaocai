"""Render the seven editable Chapter 1 history figures and print-size proofs."""
from __future__ import annotations

from html import escape
import hashlib
import json
import re
from pathlib import Path
import subprocess
import tempfile

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "materials/ch01-history-layout"
DATA_PATH = HERE / "figure-data.json"
MANIFEST_PATH = HERE / "figure-manifest.json"
OUT = ROOT / "assets/figures/ch01-history-layout"
OUT.mkdir(parents=True, exist_ok=True)

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
    return "".join(text(x, y + index * step, value, size, anchor=anchor,
                        weight=weight, fill=fill)
                   for index, value in enumerate(values))


def box(x: float, y: float, width: float, height: float, *, fill: str = WHITE,
        stroke: str = GRAY, stroke_width: float = 2.0, radius: int = 8,
        dash: str | None = None) -> str:
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
            f'rx="{radius}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{stroke_width}"{dash_attr}/>')


def line(x1: float, y1: float, x2: float, y2: float, *, color: str = GRAY,
         width: float = 2.0, dash: str | None = None, arrow: bool = False) -> str:
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    end_attr = ' marker-end="url(#arrow)"' if arrow else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{color}" stroke-width="{width}" stroke-linecap="round"'
            f'{dash_attr}{end_attr}/>')


def wrap(height: int, title: str, description: str, body: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{VIEW_WIDTH}px" '
            f'height="{height}px" viewBox="0 0 {VIEW_WIDTH} {height}" role="img" '
            'aria-labelledby="title desc">'
            f'<title id="title">{escape(title)}</title>'
            f'<desc id="desc">{escape(description)}</desc>'
            '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="5" '
            'orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L10,5 L0,10 z" '
            f'fill="{BLUE}"/></marker></defs>'
            f'<rect width="{VIEW_WIDTH}" height="{height}" fill="{WHITE}"/>'
            f'<g font-family="{FONT}">{body}</g></svg>')


def fig1(d: dict) -> str:
    body = [
        text(450, 38, "先用目录找线索，再回原卡核对内容", 24, weight="bold"),
        box(22, 71, 255, 114, fill=PALE, stroke=BLUE),
        text(149, 104, "两个查找需要", 23, weight="bold", fill=BLUE),
        text_lines(149, 137, d["query"], 22, step=29),
        line(149, 187, 149, 210, color=BLUE, arrow=True),
        box(22, 218, 255, 262, fill=WHITE),
        text(149, 251, "本次查找用到的字段", 22, weight="bold"),
        text(149, 282, "用途 · 难度 · 卡号", 22),
        text(149, 310, "架位", 22),
        text(149, 345, "两个用途分开筛", 22),
        text(149, 373, "保留入门候选", 22),
        box(43, 386, 213, 48, fill=PALE, stroke=BLUE, radius=6),
        text(149, 417, "K01、K03", 23, weight="bold", fill=BLUE),
        text(149, 455, "具体内容要读原卡", 22, weight="bold"),
        box(315, 71, 563, 409, fill="#FAFBFC", stroke=INK, stroke_width=2.3),
        text(596, 105, "六张原卡的资料范围", 23, weight="bold"),
        box(338, 124, 516, 183, fill=WHITE, stroke=BLUE, stroke_width=2.2),
        text(596, 155, "目录命中的原卡子集", 22, weight="bold", fill=BLUE),
        box(356, 169, 480, 53, fill=PALE, stroke=GRAY, radius=5),
        text(374, 202, "K01", 22, anchor="start", weight="bold"),
        text(438, 202, "采访准备 · 入门 · 架一层左侧", 22, anchor="start"),
        box(356, 234, 480, 53, fill=PALE, stroke=GRAY, radius=5),
        text(374, 267, "K03", 22, anchor="start", weight="bold"),
        text(438, 267, "使用前确认 · 入门 · 架二层左侧", 22, anchor="start"),
        line(278, 334, 326, 334, color=BLUE, arrow=True),
        text(596, 339, "其余卡片：K02 · K04 · K05 · K06", 22),
        box(338, 365, 516, 91, fill=PALE, stroke=BLUE),
        text(596, 399, "读K03原文，才能核对授权范围", 22, weight="bold"),
        text(596, 432, "找到卡片 ≠ 已确认卡片内容", 22, fill=BLUE),
    ]
    return wrap(505, d["caption"], d["description"], "".join(body))


def fig2(d: dict) -> str:
    body = [
        box(25, 34, 850, 56, fill=PALE, stroke=BLUE),
        text(450, 70, d["goal"], 23, weight="bold", fill=BLUE),
    ]
    column_xs = [24, 316, 608]
    col_width = 268
    row_y = [143, 224, 305, 386]
    row_height = 80
    row_names = ["输入", "规则", "输出", "核对"]
    for column, x in zip(d["representations"], column_xs):
        body += [box(x, 105, col_width, 370, fill=WHITE, stroke=INK, stroke_width=2.1),
                 text(x + col_width / 2, 135, column["name"], 24, weight="bold", fill=BLUE)]
        for index, (label, values) in enumerate(zip(row_names, [column["input"], column["rule"], column["output"], column["check"]])):
            y = row_y[index]
            body += [box(x + 10, y, col_width - 20, row_height, fill=PALE if index % 2 == 0 else WHITE,
                         stroke=MID, stroke_width=1.5, radius=4),
                     text(x + 25, y + 31, label, 22, anchor="start", weight="bold"),
                     text_lines(x + 91, y + 21, values, 22, anchor="start", step=25)]
    body += [text(450, 514, "三种表示面对同一目录与目标；结果相同，核对仍不能省略。", 22, weight="bold")]
    return wrap(540, d["caption"], d["description"], "".join(body))


def fig3(d: dict) -> str:
    body = [text(450, 35, "沿时间次序阅读问题、贡献和边界", 23, weight="bold")]
    x0, y0 = 17, 58
    widths = [140, 215, 291, 220]
    headers = ["时间点", "当时的问题", "一项贡献或设想", "需要保留的边界"]
    header_h, row_h = 47, 83
    x = x0
    for width, label in zip(widths, headers):
        body += [box(x, y0, width, header_h, fill=BLUE, stroke=WHITE, stroke_width=1.3, radius=2),
                 text(x + width / 2, y0 + 31, label, 22, weight="bold", fill=WHITE)]
        x += width
    for row_idx, row in enumerate(d["history_rows"]):
        y = y0 + header_h + row_idx * row_h
        x = x0
        year_lines = row["year"] if isinstance(row["year"], list) else [row["year"]]
        cells = [year_lines, row["problem"], row["contribution"], row["limit"]]
        fills = [PALE if row_idx % 2 == 0 else WHITE] * 4
        for col_idx, (width, lines) in enumerate(zip(widths, cells)):
            text_y = y + (49 if len(lines) == 1 else 35) if col_idx == 0 else y + 29
            body += [box(x, y, width, row_h, fill=fills[col_idx], stroke=MID,
                         stroke_width=1.5, radius=1),
                     text_lines(x + (width / 2 if col_idx == 0 else 10), text_y, lines, 22,
                                anchor="middle" if col_idx == 0 else "start",
                                weight="bold" if col_idx == 0 else "normal", step=27,
                                fill=BLUE if col_idx == 0 else INK)]
            x += width
    footer_y = y0 + header_h + len(d["history_rows"]) * row_h + 30
    body += [text(450, footer_y, d["time_note"], 22, weight="bold", fill=BLUE)]
    return wrap(footer_y + 42, d["caption"], d["description"], "".join(body))


def square_path(x: int, y: int, size: int, *, color: str, width: float = 3,
                directed: bool = False, dash: str | None = None) -> str:
    directions = [(x, y + size, x, y), (x, y, x + size, y),
                  (x + size, y, x + size, y + size),
                  (x + size, y + size, x, y + size)]
    return "".join(line(*edge, color=color, width=width, arrow=directed, dash=dash)
                   for edge in directions)


def fig4(d: dict) -> str:
    xs = [18, 310, 602]
    width = 280
    body = [text(450, 39, f"同一任务：{d['task']}；证据对象各不相同", 23, weight="bold")]
    for x, title in zip(xs, ["数学约定", "指令轨迹", "真实移动观察"]):
        body += [box(x, 68, width, 400, fill=WHITE, stroke=INK, stroke_width=2.1),
                 text(x + width / 2, 102, title, 23, weight="bold", fill=BLUE)]

    body += [square_path(110, 132, 90, color=INK, width=3),
             text(158, 252, "理想方形", 22, weight="bold", fill=BLUE),
             text_lines(158, 291, d["ideal_conditions"], 22, step=27),
             line(44, 362, 272, 362, color=MID, width=1.5),
             text_lines(158, 396, ["依据条件作推理", "检查角与闭合关系"], 22, step=30)]

    body += [square_path(405, 132, 90, color=BLUE, width=3.0, directed=True),
             text(450, 252, "按顺序执行", 22, weight="bold", fill=BLUE),
             text_lines(450, 291, ["每段前进相同长度", "每次右转90°，共4次"], 22, step=30),
             line(336, 362, 564, 362, color=MID, width=1.5),
             text_lines(450, 396, ["逐步重演指令", "检查次数、顺序与停止"], 22, step=30)]

    body += [square_path(697, 132, 90, color=GRAY, width=2.4, dash="8 6"),
             text(742, 252, "目标路线：方形", 22, weight="bold"),
             text(742, 282, "实测轨迹：待记录", 22, weight="bold", fill=BLUE)]
    for idx, label in enumerate(d["physical_observations"]):
        y = 320 + (idx // 2) * 40
        col_x = 628 if idx % 2 == 0 else 756
        body += [box(col_x, y - 24, 115, 34, fill=PALE, stroke=MID, stroke_width=1.3, radius=3),
                 text(col_x + 57, y, label, 22)]
    body += [line(628, 390, 856, 390, color=MID, width=1.5),
             text_lines(742, 422, ["需现场观察与测量", "本图没有实测数据"], 22,
                        step=29, weight="bold")]
    return wrap(490, d["caption"], d["description"], "".join(body))


def draw_grid(rows: list[str], x: int, y: int, cell: int, gap: int,
              changed_cell: dict | None = None) -> str:
    body = []
    for r, row in enumerate(rows, 1):
        for c, bit in enumerate(row, 1):
            px, py = x + (c - 1) * (cell + gap), y + (r - 1) * (cell + gap)
            fill = BLUE if bit == "1" else WHITE
            body += [box(px, py, cell, cell, fill=fill, stroke=INK,
                         stroke_width=1.8, radius=1),
                     text(px + cell / 2, py + cell * .69, bit, 22,
                          weight="bold", fill=WHITE if bit == "1" else INK)]
            if changed_cell and r == changed_cell["row"] and c == changed_cell["column"]:
                body += [f'<rect x="{px-2}" y="{py-2}" width="{cell+4}" height="{cell+4}" '
                         f'fill="none" stroke="{BLUE}" stroke-width="3.5"/>']
    return "".join(body)


def fig5(d: dict) -> str:
    cell, gap = 42, 3
    y = 122
    changed = d["changed_cell"]
    body = [text(450, 39, "E05示例：用格子和逐行标记复核局部变化", 23, weight="bold"),
            box(20, 62, 420, 317, fill=WHITE, stroke=INK, stroke_width=2),
            box(460, 62, 420, 317, fill=WHITE, stroke=INK, stroke_width=2),
            text(230, 99, "原始图案", 23, weight="bold", fill=BLUE),
            text(670, 99, "改动后", 23, weight="bold", fill=BLUE),
            draw_grid(d["original_rows"], 53, y, cell, gap, changed),
            draw_grid(d["changed_rows"], 493, y, cell, gap, changed)]
    for x, rows in [(258, d["original_rows"]), (698, d["changed_rows"])]:
        for index, bits in enumerate(rows):
            body.append(text(x, y + index * (cell + gap) + 28, f"r{index+1}  {bits}",
                             22, anchor="start", weight="bold" if index == 2 else "normal",
                             fill=BLUE if index == 2 else INK))
    body += [box(20, 400, 860, 90, fill=PALE, stroke=BLUE, stroke_width=2),
             text(450, 435, "第三行：0110 → 0010", 23, weight="bold"),
             text(450, 470, "只改第3行第2列：1 → 0", 23, weight="bold", fill=BLUE)]
    return wrap(510, d["caption"], d["description"], "".join(body))


def fig6(d: dict) -> str:
    body = [text(450, 36, "可迁移的是组织关系；具体判断随领域改变", 23, weight="bold"),
            box(20, 62, 420, 341, fill=WHITE, stroke=INK, stroke_width=2),
            box(460, 62, 420, 354, fill=WHITE, stroke=INK, stroke_width=2),
            text(230, 98, "源任务：织造格图", 23, weight="bold", fill=BLUE),
            text(670, 98, "目标任务：整理访谈", 23, weight="bold", fill=BLUE)]
    body.append(draw_grid(d["textile_rows"], 69, 126, 34, 3))
    body += [text(270, 146, "1001", 22, anchor="start"),
             text(270, 183, "0110", 22, anchor="start"),
             text(270, 220, "0110", 22, anchor="start"),
             text(270, 257, "1001", 22, anchor="start"),
             line(50, 292, 410, 292, color=MID, width=1.5),
             text_lines(230, 329, ["标记规则固定", "可按格复现并逐格核对"], 22,
                        step=30)]
    record_y = [150, 252, 354]
    for interview, y in zip(d["interviews"], record_y):
        quote = interview["quote"]
        max_content_chars = 13
        line_count = max(1, (len(quote) + max_content_chars - 1) // max_content_chars)
        chunk_size = (len(quote) + line_count - 1) // line_count
        quote_parts = [quote[i:i + chunk_size] for i in range(0, len(quote), chunk_size)]
        if len(quote_parts) == 1:
            quote_lines = [f'“{quote_parts[0]}”']
        else:
            quote_lines = [f'“{quote_parts[0]}', *quote_parts[1:-1], f'{quote_parts[-1]}”']
        body += [box(480, y - 38, 380, 98, fill=PALE, stroke=MID, stroke_width=1.4, radius=4),
                 text(491, y - 8, interview["speaker"], 22, anchor="start", weight="bold", fill=BLUE),
                 text_lines(520, y - 8, quote_lines, 22, anchor="start", step=25),
                 text(495, y + 47, f'时间关系：{interview["time_relation"]}', 22, anchor="start")]
    body += [box(30, 429, 840, 75, fill=PALE, stroke=BLUE, stroke_width=2),
             text(450, 459, "共同关系：把材料组织成一致、可查找的表示", 23, weight="bold", fill=BLUE),
             text(450, 488, "按当前任务核对结果", 22)]
    body += [box(30, 520, 840, 143, fill=WHITE, stroke=INK, stroke_width=2),
             text(450, 552, "两种任务并非完全同构", 23, weight="bold"),
             line(450, 568, 450, 644, color=MID, width=1.5),
             text_lines(235, 594, ["织造：固定0/1规则", "图案可逐格对照"], 22, step=29),
             text_lines(665, 594, ["访谈：时间可能未确认", "保留原句与确定程度"], 22, step=29)]
    return wrap(680, d["caption"], d["description"], "".join(body))


def fig7(d: dict) -> str:
    body = [text(450, 36, "四种并列提问；连线不表示先后或高低", 23, weight="bold")]
    boxes = [
        (20, 70, d["views"][0]), (480, 70, d["views"][1]),
        (20, 485, d["views"][2]), (480, 485, d["views"][3]),
    ]
    center_x, center_y, center_w, center_h = 250, 267, 400, 185
    body += [line(420, 245, center_x + 37, center_y, color=GRAY, width=2.2),
             line(480, 245, center_x + center_w - 37, center_y, color=GRAY, width=2.2),
             line(420, 485, center_x + 37, center_y + center_h, color=GRAY, width=2.2),
             line(480, 485, center_x + center_w - 37, center_y + center_h, color=GRAY, width=2.2)]
    for x, y, item in boxes:
        body += [box(x, y, 400, 174, fill=WHITE, stroke=GRAY, stroke_width=2.1, radius=10),
                 text(x + 200, y + 34, item["name"], 23, weight="bold", fill=BLUE),
                 text_lines(x + 200, y + 76, item["question"], 22, step=30)]
    body += [box(center_x, center_y, center_w, center_h, fill=PALE,
                 stroke=BLUE, stroke_width=2.5, radius=12),
             text(450, 302, "同一标题决定", 23, weight="bold", fill=BLUE),
             text(450, 336, f'原拟：{d["original_title"]}', 22),
             text(450, 370, f'修订示例：{d["revised_title"]}', 22, weight="bold"),
             text(450, 404, "范围：两段模拟个人经历", 22),
             text(450, 435, "加一张空白样表，不代表全体", 22),
             text(450, 689, d["boundary_note"], 22, weight="bold")]
    return wrap(725, d["caption"], d["description"], "".join(body))


BUILDERS = [fig1, fig2, fig3, fig4, fig5, fig6, fig7]


def render_svg(svg_path: Path, png_path: Path, css_height: int) -> dict:
    if not CHROME.is_file():
        raise FileNotFoundError(f"local SVG renderer unavailable: {CHROME}")
    svg = svg_path.read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="ch01-history-figure-") as td:
        tmp = Path(td)
        html = tmp / "figure.html"
        html.write_text(
            '<!doctype html><html><head><meta charset="utf-8"><style>'
            f'html,body{{margin:0;padding:0;width:{VIEW_WIDTH}px;height:{css_height}px;'
            'overflow:hidden;background:#fff}svg{display:block}</style></head><body>' + svg + '</body></html>',
            encoding="utf-8",
        )
        command = [
            str(CHROME), "--headless", "--no-sandbox", "--disable-gpu",
            "--disable-dev-shm-usage", "--hide-scrollbars",
            f"--user-data-dir={tmp / 'profile'}", "--force-device-scale-factor=2.6666666667",
            f"--window-size={VIEW_WIDTH},{css_height}", "--virtual-time-budget=1000",
            f"--screenshot={png_path}", html.as_uri(),
        ]
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
    return {
        "dimensions_px": dimensions,
        "sha256": hashlib.sha256(png_path.read_bytes()).hexdigest(),
        "gray_sha256": hashlib.sha256(gray_path.read_bytes()).hexdigest(),
        "grayscale_png": gray_path,
    }


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    figures = data["figures"]
    if len(figures) != 7 or len({entry["id"] for entry in figures}) != 7:
        raise ValueError("Chapter 1 layout requires seven unique figure records")
    outputs = []
    for item, builder in zip(figures, BUILDERS):
        number = int(item["id"].split("-")[1])
        svg_path = OUT / f"fig1-{number}.svg"
        png_path = OUT / f"fig1-{number}.png"
        svg = builder(item)
        svg_path.write_text(svg, encoding="utf-8")
        font_sizes = [int(size) for size in re.findall(r'font-size="(\d+)px"', svg)]
        if not font_sizes or min(font_sizes) < MIN_FONT_PX:
            raise ValueError(f"minimum SVG font failed for {item['id']}: {font_sizes}")
        height_match = re.search(r'<svg[^>]+height="(\d+)px"', svg)
        if not height_match:
            raise ValueError(f"missing SVG height for {item['id']}")
        exported = render_svg(svg_path, png_path, int(height_match.group(1)))
        outputs.append({
            **{key: value for key, value in item.items() if key != "history_rows" and key not in {
                "query", "directory_fields", "matches", "other_cards", "judgment_note", "goal",
                "representations", "time_note", "task", "ideal_conditions", "instruction",
                "physical_observations", "physical_status", "original_rows", "changed_rows",
                "changed_cell", "encoding", "textile_rows", "interviews", "shared_relation",
                "difference", "original_title", "revised_title", "evidence_scope", "views",
                "boundary_note"}},
            "status": "ready",
            "editable_source": f"assets/figures/ch01-history-layout/fig1-{number}.svg",
            "file": f"assets/figures/ch01-history-layout/fig1-{number}.png",
            "png": f"assets/figures/ch01-history-layout/fig1-{number}.png",
            "grayscale_png": f"assets/figures/ch01-history-layout/fig1-{number}-gray.png",
            "sha256": exported["sha256"],
            "gray_sha256": exported["gray_sha256"],
            "svg_sha256": hashlib.sha256(svg_path.read_bytes()).hexdigest(),
            "insert_width_mm": INSERT_MM,
            "viewbox_width": VIEW_WIDTH,
            "png_ppi_at_insert": PPI,
            "declared_min_label_px": min(font_sizes),
            "min_font_pt_at_insert": MIN_FONT_PT,
            "dimensions_px": exported["dimensions_px"],
            "gray_semantics": "标签、位置、边框、实虚线、格内数字与形状共同承载含义；颜色只是辅助。",
        })
    manifest = {
        "style": data["style"],
        "insert_width_mm": INSERT_MM,
        "png_ppi_at_insert": PPI,
        "min_label_pt_at_insert": MIN_FONT_PT,
        "render_command": "/home/reggie/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python materials/ch01-history-layout/render_figures.py",
        "visual_review": {"status": "pending_actual_image_view", "items": []},
        "figures": outputs,
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8")
    print(json.dumps({
        "figures": len(outputs), "png_width_px": PNG_WIDTH, "ppi_at_insert": PPI,
        "min_font_pt_at_insert": MIN_FONT_PT,
        "sha256": [{"id": item["id"], "png": item["sha256"],
                    "gray": item["gray_sha256"], "svg": item["svg_sha256"]}
                   for item in outputs],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
