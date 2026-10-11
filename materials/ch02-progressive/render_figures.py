"""Build editable Chapter 2 progression figures and print-size PNG derivatives.

Concept diagrams are authored as text-editable SVG. The comparison chart is
drawn from the chapter's fixed teaching data with Matplotlib. PNG files are
rendered at 2400 px wide for the 155 mm shared text width; grayscale copies
are retained for a print-legibility check.
"""
from __future__ import annotations

from html import escape
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets/figures/ch02-progressive"
OUT.mkdir(parents=True, exist_ok=True)
MANIFEST = ROOT / "materials/ch02-progressive/figure-manifest.json"

INK = "#222222"
BLUE = "#1F4E79"
GRAY = "#676767"
PALE = "#EEF1F4"
WHITE = "#FFFFFF"
FONT = "Noto Sans CJK SC, sans-serif"
VIEW_WIDTH = 900
INSERT_MM = 155
PNG_WIDTH = 2400
MIN_FONT_PX = 22
PPI = round(PNG_WIDTH / (INSERT_MM / 25.4))
MIN_FONT_PT = round(MIN_FONT_PX * INSERT_MM * 72 / 25.4 / VIEW_WIDTH, 2)
CHROME = Path("/usr/bin/google-chrome")


def t(x: float, y: float, value: str, size: int = 22, *, anchor: str = "middle",
      weight: str = "normal", fill: str = INK, opacity: float = 1.0) -> str:
    if size < MIN_FONT_PX:
        raise ValueError(f"text below print minimum: {value!r} at {size}px")
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{FONT}" '
            f'font-size="{size}px" font-weight="{weight}" fill="{fill}" '
            f'fill-opacity="{opacity}">{escape(value)}</text>')


def lines(x: float, y: float, values: list[str], size: int = 22, *,
          anchor: str = "middle", weight: str = "normal", fill: str = INK,
          step: int = 31) -> str:
    return "".join(t(x, y + step * i, value, size, anchor=anchor, weight=weight, fill=fill)
                   for i, value in enumerate(values))


def panel(x: float, y: float, w: float, h: float, *, fill: str = WHITE,
          stroke: str = GRAY, dashed: bool = False, radius: int = 10,
          stroke_width: float = 2.5) -> str:
    dash = ' stroke-dasharray="9 7"' if dashed else ""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"{dash}/>')


def circle(x: float, y: float, label: str, *, r: int = 35,
           stroke: str = INK, fill: str = WHITE, weight: str = "bold",
           double: bool = False) -> str:
    out = f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
    if double:
        out += f'<circle cx="{x}" cy="{y}" r="{r-7}" fill="none" stroke="{BLUE}" stroke-width="2.5"/>'
    return out + t(x, y + 8, label, 24, weight=weight)


def arrow(x1: float, y1: float, x2: float, y2: float, *, dashed: bool = False,
          color: str = BLUE, width: float = 3.0, marker: bool = True) -> str:
    dash = ' stroke-dasharray="10 7"' if dashed else ""
    end = ' marker-end="url(#arrow)"' if marker else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{color}" stroke-width="{width}"{dash}{end}/>')


def path(d: str, *, color: str = BLUE, width: float = 3.0,
         dashed: bool = False, marker: bool = True) -> str:
    dash = ' stroke-dasharray="10 7"' if dashed else ""
    end = ' marker-end="url(#arrow)"' if marker else ""
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"'
            f'{dash}{end}/>')


def edge(x1: float, y1: float, x2: float, y2: float, label: str = "", *,
         lx: float | None = None, ly: float | None = None, directed: bool = False,
         dashed: bool = False, highlight: bool = False, curve: str | None = None) -> str:
    dx, dy = x2 - x1, y2 - y1
    dist = math.hypot(dx, dy)
    radius = 36
    sx, sy = x1 + dx * radius / dist, y1 + dy * radius / dist
    ex, ey = x2 - dx * radius / dist, y2 - dy * radius / dist
    color = BLUE if highlight else INK
    width = 5.0 if highlight else 2.7
    if curve:
        shape = path(curve, color=color, width=width, dashed=dashed, marker=directed)
    else:
        shape = arrow(sx, sy, ex, ey, dashed=dashed, color=color,
                      width=width, marker=directed)
    if not label:
        return shape
    label_width = max(46, len(label) * 23 + 16)
    lx = (sx + ex) / 2 if lx is None else lx
    ly = (sy + ey) / 2 if ly is None else ly
    plate = (f'<rect x="{lx-label_width/2}" y="{ly-21}" width="{label_width}" height="29" '
             f'rx="3" fill="{WHITE}" stroke="none"/>')
    return shape + plate + t(lx, ly, label, 22, fill=color,
                              weight="bold" if highlight else "normal")


def wrap(height: int, title: str, desc: str, body: str) -> str:
    # The accessible title/description are metadata only; no chapter number or
    # visible figure caption is baked into the artwork.
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{VIEW_WIDTH}px" height="{height}px" '
            f'viewBox="0 0 {VIEW_WIDTH} {height}" role="img" aria-labelledby="title desc">'
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>'
            '<defs><marker id="arrow" markerWidth="9" markerHeight="7" refX="8" refY="3.5" '
            'orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L9,3.5 L0,7 z" fill="#1F4E79"/></marker>'
            '<pattern id="hatch" width="10" height="10" patternUnits="userSpaceOnUse">'
            '<path d="M-2,2 L2,-2 M0,10 L10,0 M8,12 L12,8" stroke="#676767" stroke-width="1.5"/>'
            f'</pattern></defs><rect width="900" height="{height}" fill="white"/>'
            f'<g font-family="{FONT}">{body}</g></svg>')


def fig1() -> str:
    body = []
    # Three distinct visual roles: original evidence, facts extracted from it,
    # and questions that the text does not settle.
    body += [panel(24, 54, 270, 316, fill=PALE, stroke=GRAY),
             t(159, 91, "模拟通知原文", 24, weight="bold")]
    body += lines(48, 139, [
        "周五下午，设计楼301",
        "举行海报工作坊。",
        "13:50签到，14:00开场，",
        "15:30结束。",
        "西侧电梯可到三层。",
    ], 22, anchor="start", step=39)
    body += [arrow(294, 210, 329, 210, color=BLUE, width=3)]
    body += [panel(330, 54, 274, 316, stroke=BLUE),
             t(467, 91, "可直接记录", 24, weight="bold", fill=BLUE)]
    fact_rows = [
        ("✓", "日期：周五"),
        ("✓", "签到：13:50"),
        ("✓", "地点：设计楼301"),
        ("✓", "电梯：到三层"),
    ]
    for i, (mark, label) in enumerate(fact_rows):
        y = 145 + i * 54
        body += [circle(367, y-5, mark, r=16, stroke=BLUE, weight="bold"),
                 t(397, y+3, label, 22, anchor="start")]
    body += [path("M604 207 C623 207 626 207 644 207", color=GRAY, width=2.5, dashed=True),
             panel(646, 54, 230, 316, dashed=True, stroke=GRAY),
             t(761, 91, "仍需核验", 24, weight="bold")]
    body += [panel(670, 119, 182, 64, fill=PALE, stroke=GRAY),
             lines(761, 145, ["“整段无台阶", "可到达”"], 22, weight="bold", step=27)]
    body += [t(761, 221, "通知未说明", 22, weight="bold", fill=BLUE),
             lines(674, 259, ["入口→电梯", "电梯→房间", "有电梯 ≠", "整段路线可达"],
                   22, anchor="start", step=31)]
    body += [t(450, 414, "把“未提供”保留下来，不能把空白补成肯定事实。", 22, weight="bold")]
    return wrap(445, "通知中可记录事实与尚缺证据", "左侧为模拟通知。中间列只保留通知明确给出的事实；右侧列出整段无台阶通行承诺仍缺少的入口到电梯、以及电梯到房间连接信息。", "".join(body))


def fig2() -> str:
    body = []
    # The pixel patch, response maps and task output use different encodings;
    # the note explicitly limits the familiar layer-by-layer illustration.
    x0, y0, cell, gap = 56, 135, 29, 5
    vals = [
        [0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 0, 0, 1, 0],
        [0, 0, 1, 1, 0], [0, 1, 1, 1, 0],
    ]
    for r, row in enumerate(vals):
        for c, v in enumerate(row):
            fill = PALE if not v else "#B7C1CA"
            body.append(f'<rect x="{x0+c*(cell+gap)}" y="{y0+r*(cell+gap)}" width="{cell}" height="{cell}" fill="{fill}" stroke="{GRAY}" stroke-width="1.5"/>')
    body += [t(145, 105, "输入局部", 24, weight="bold"),
             lines(145, 343, ["像素亮暗", "按位置排列"], 22)]
    body += [arrow(264, 214, 305, 214, width=3)]

    # Early feature response: the same step-like patch appears as local edges.
    body += [panel(312, 126, 160, 184, fill=WHITE, stroke=GRAY)]
    for i, (x1, y1, x2, y2) in enumerate([
        (338, 163, 385, 163), (394, 163, 440, 163),
        (338, 207, 338, 248), (382, 207, 426, 207),
        (426, 207, 426, 250), (360, 251, 405, 251),
    ]):
        body.append(arrow(x1, y1, x2, y2, color=BLUE if i % 2 == 0 else INK,
                          width=3, marker=False))
    body += [t(392, 105, "局部响应", 24, weight="bold"),
             lines(392, 343, ["可能对边缘、", "方向敏感"], 22)]
    body += [arrow(473, 214, 516, 214, width=3)]

    # Later feature combinations are intentionally named as possible responses,
    # not stable human-readable concepts.
    body += [panel(524, 126, 160, 184, fill=PALE, stroke=BLUE)]
    body += [path("M550 258 L550 220 L580 220 L580 183 L610 183 L610 153 L650 153",
                  color=BLUE, width=6, marker=False),
             path("M550 268 L650 268", color=GRAY, width=2.5, dashed=True, marker=False),
             t(604, 105, "组合响应", 24, weight="bold"),
             lines(604, 343, ["可形成纹理或", "局部形状模式"], 22)]
    body += [arrow(686, 214, 726, 214, width=3)]

    body += [panel(735, 126, 145, 184, stroke=GRAY),
             t(807, 105, "任务输出", 24, weight="bold")]
    body += [panel(752, 158, 111, 48, fill=PALE, stroke=GRAY),
             t(807, 190, "候选类别", 22),
             panel(752, 221, 111, 48, fill=WHITE, stroke=BLUE, dashed=True),
             t(807, 253, "任务分数", 22),
             lines(807, 343, ["随任务目标", "计算结果"], 22)]
    body += [panel(48, 392, 804, 66, fill=PALE, stroke=GRAY),
             t(450, 419, "分层图只是帮助理解的可能路径；真实响应不保证对应固定、可命名的现实概念。", 22, weight="bold"),
             t(450, 446, "模型学到什么取决于数据、标签、网络结构和训练目标。", 22)]
    return wrap(480, "卷积网络从局部输入形成任务表示的概念示意", "图示以台阶形局部图像为例，从像素局部、可能的边缘响应、组合响应到任务输出。它不是任何真实模型的激活图，也不声称网络层与人类概念一一对应。", "".join(body))


def fig3() -> str:
    body = []
    body += [t(450, 43, "任务箭头表示先后依赖；下方使用同一小时刻度", 22, weight="bold")]
    # A small DAG above a common-scale schedule avoids conflating dependency
    # with elapsed time.
    coords = {"T1": (175, 130), "T2": (175, 236), "T3": (448, 130), "T4": (725, 183)}
    boxes = {"T1": ["T1  确认文本", "1小时"],
             "T2": ["T2  预约空间", "2小时"],
             "T3": ["T3  制作打印稿", "2小时"],
             "T4": ["T4  安装检查", "1小时"]}
    for start, end in [("T1", "T3"), ("T2", "T4"), ("T3", "T4")]:
        x1, y1 = coords[start]
        x2, y2 = coords[end]
        body.append(arrow(x1+79, y1, x2-79, y2, width=3))
    for key, (x, y) in coords.items():
        body += [panel(x-80, y-39, 160, 78,
                       fill=PALE if key in ("T1", "T2") else WHITE,
                       stroke=BLUE if key in ("T1", "T2") else INK),
                 lines(x, y-4, boxes[key], 22, weight="bold", step=31)]
    body += [t(450, 300, "只看逻辑依赖时，T1与T2可以同时开始；现实仍要检查人手和场地。", 22)]

    # One horizontal axis serves every task bar.
    x_start, x_end = 178, 832
    for tick in range(5):
        x = x_start + tick * (x_end-x_start) / 4
        body += [arrow(x, 340, x, 520, color="#A0A0A0", width=1.8, marker=False),
                 t(x, 331, f"{tick}h", 22, weight="bold")]
    body += [t(43, 385, "T1", 22, anchor="start", weight="bold"),
             t(43, 426, "T2", 22, anchor="start", weight="bold"),
             t(43, 467, "T3", 22, anchor="start", weight="bold"),
             t(43, 508, "T4", 22, anchor="start", weight="bold")]
    scale = (x_end - x_start) / 4
    bars = [("T1", 0, 1, 385), ("T2", 0, 2, 426), ("T3", 1, 3, 467), ("T4", 3, 4, 508)]
    for label, start, end, y in bars:
        x = x_start + start*scale
        w = (end-start)*scale
        fill = BLUE if label in ("T1", "T3") else PALE
        stroke = BLUE if label in ("T1", "T3") else INK
        body += [f'<rect x="{x}" y="{y-25}" width="{w}" height="30" rx="3" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>',
                 t(x+w/2, y-3, f"{end-start}h", 22, weight="bold", fill=WHITE if label in ("T1", "T3") else INK)]
    body += [t(505, 563, "最早在第4小时完成；不是把四项时长相加成6小时。", 22, weight="bold")]
    return wrap(590, "依赖关系与最早任务时间线", "T1确认文本耗时1小时，T2预约空间耗时2小时；T3依赖T1、耗时2小时；T4依赖T2和T3、耗时1小时。时间线使用统一的0至4小时刻度，逻辑上并行不保证现实资源一定允许并行。", "".join(body))


def fig4() -> str:
    body = []
    body += [t(450, 40, "以当前记录为例：先形成Q，再与可用位置的K逐一匹配", 22, weight="bold")]
    # Three positions share the same horizontal alignment to make the K/V
    # association visible. Varying connector width is only qualitative.
    xs = [180, 450, 720]
    labels = ["此前位置1", "此前位置2", "当前位置"]
    for x, label in zip(xs, labels):
        body += [panel(x-92, 69, 184, 53, fill=PALE if x != 720 else WHITE,
                       stroke=BLUE if x == 720 else GRAY, dashed=x == 720),
                 t(x, 103, label, 22, weight="bold")]
    body += [panel(642, 145, 156, 52, stroke=BLUE),
             t(720, 179, "查询 Q", 24, weight="bold", fill=BLUE)]
    for x in xs:
        body.append(arrow(720, 197, x, 223, color=BLUE, width=2.7))
    for x, i in zip(xs, range(1, 4)):
        body += [panel(x-77, 222, 154, 52, fill=PALE, stroke=GRAY),
                 t(x, 256, f"键 K{i}", 24, weight="bold"),
                 arrow(x, 274, x, 300, width=2.7),
                 panel(x-65, 301, 130, 49, stroke=GRAY),
                 t(x, 333, f"权重 α{i}", 22)]
    body += [t(450, 383, "Q与每个K的匹配共同决定权重", 22, weight="bold")]
    for x, i in zip(xs, range(1, 4)):
        body += [panel(x-67, 400, 134, 50, fill=PALE, stroke=GRAY),
                 t(x, 433, f"值 V{i}", 24, weight="bold")]
    body += [path("M180 453 C180 480 280 481 355 491", color=GRAY, width=2.3),
             path("M450 453 L450 491", color=BLUE, width=4.0),
             path("M720 453 C720 480 620 481 545 491", color=GRAY, width=2.3),
             panel(345, 485, 210, 54, fill=PALE, stroke=BLUE),
             t(450, 520, "加权汇总：Σ αᵢVᵢ", 22, weight="bold", fill=BLUE)]
    body += [arrow(450, 540, 450, 565, width=2.7),
             panel(321, 565, 258, 47, stroke=INK),
             t(450, 596, "当前位置的新表示", 22, weight="bold"),
             lines(450, 647, ["连线粗细仅作权重示意，不含实测数值。", "预测时只能汇总当时允许访问的位置；权重不是因果解释。"], 22, step=29)]
    return wrap(710, "自注意力中查询、键和值的概念关系", "当前位置形成查询Q，与可用位置各自的键K匹配后形成权重；对应的值V按权重汇总成当前位置的新表示。图中没有真实权重数值，预测任务必须按任务设置限制可访问的时间位置。", "".join(body))


def fig5() -> str:
    body = []
    body += [t(450, 43, "多方在本地训练；协调方只接收模型更新并汇总", 22, weight="bold")]
    centers = [165, 450, 735]
    names = ["机构A", "机构B", "机构C"]
    for x, name, idx in zip(centers, names, range(1, 4)):
        body += [panel(x-122, 76, 244, 232, fill=PALE, stroke=GRAY, dashed=True),
                 t(x, 108, name, 24, weight="bold")]
        # A stack of records visually remains inside the institutional boundary.
        for j in range(3):
            body.append(f'<rect x="{x-56+j*7}" y="{114+j*10}" width="112" height="32" rx="4" fill="{WHITE}" stroke="{INK}" stroke-width="2"/>')
        body += [t(x, 194, "本地原始记录", 22, weight="bold"),
                 arrow(x, 204, x, 222, color=INK, width=2.5),
                 panel(x-85, 224, 170, 54, stroke=BLUE),
                 t(x, 259, "本地训练", 22, weight="bold", fill=BLUE)]
    # Separate upload cards keep update labels away from the converging arrows.
    for x, i in zip(centers, range(1, 4)):
        body += [panel(x-86, 322, 172, 42, fill=WHITE, stroke=BLUE, radius=6),
                 t(x, 350, f"上传更新 Δθ{i}", 22, weight="bold", fill=BLUE)]
    for x, i in zip(centers, range(1, 4)):
        body.append(arrow(x, 364, 450, 410, color=BLUE, width=3.3))
    body += [panel(333, 412, 234, 72, fill=WHITE, stroke=BLUE),
             lines(450, 443, ["协调方聚合", "形成汇总模型"], 22, weight="bold", fill=BLUE, step=27)]
    # A separate lower row makes the return direction distinct from uploads.
    body += [path("M450 484 L450 491", color=GRAY, width=2.5, dashed=True, marker=False),
             panel(344, 491, 212, 38, fill=WHITE, stroke=GRAY, radius=5, stroke_width=1.4),
             t(450, 517, "返回汇总模型 θₜ₊₁", 22, weight="bold", fill=BLUE),
             path("M450 529 L450 540", color=GRAY, width=2.5, dashed=True, marker=False),
             path("M165 540 L735 540", color=GRAY, width=2.5, dashed=True, marker=False)]
    for x in centers:
        body.append(path(f"M{x} 540 L{x} 553", color=GRAY, width=2.5, dashed=True, marker=True))
    for x, name in zip(centers, names):
        body += [panel(x-112, 555, 224, 48, fill=PALE, stroke=GRAY),
                 t(x, 586, f"{name}继续使用或训练", 22, weight="bold")]
    body += [panel(45, 617, 810, 70, fill=WHITE, stroke=GRAY),
             lines(450, 646, ["原始记录留在本地 ≠ 自动隐私保护。更新仍可能泄露信息，", "还需明确授权、可见范围与额外保护机制。"], 22, step=28)]
    return wrap(705, "联邦学习的数据与更新流向", "三个机构各自保留原始记录并进行本地训练；模型更新流向协调方聚合，汇总模型再返回机构。图说明数据流转方式，不代表更新天然安全或隐私风险已经消除。", "".join(body))


def fig6() -> str:
    body = []
    # Current section 2.4's exact directed example (five locations, eight edges).
    coords = {"P": (82, 269), "A": (250, 145), "B": (250, 399),
              "C": (430, 269), "D": (550, 269)}
    body += [t(315, 43, "有向边上的分钟数", 22, weight="bold")]
    body += [
        edge(*coords["P"], *coords["A"], "2", lx=151, ly=183, directed=True, highlight=True),
        edge(*coords["P"], *coords["B"], "5", lx=151, ly=357, directed=True),
        edge(*coords["A"], *coords["B"], "1", lx=278, ly=270, directed=True, highlight=True),
        edge(*coords["A"], *coords["C"], "6", lx=355, ly=172, directed=True),
        edge(*coords["A"], *coords["D"], "11", lx=439, ly=91, directed=True,
             curve="M280 117 C350 54 466 54 523 233"),
        edge(*coords["B"], *coords["C"], "1", lx=352, ly=354, directed=True, highlight=True),
        edge(*coords["B"], *coords["D"], "5", lx=439, ly=443, directed=True,
             curve="M280 425 C350 488 466 488 523 305"),
        edge(*coords["C"], *coords["D"], "2", lx=490, ly=240, directed=True, highlight=True),
    ]
    for label, (x, y) in coords.items():
        body.append(circle(x, y, label, r=32, stroke=BLUE if label in {"P", "A", "B", "C", "D"} else INK))
    body += [t(315, 525, "较粗蓝线：一条6分钟路线 P→A→B→C→D", 22, weight="bold", fill=BLUE)]
    # A second panel records only the values needed to reproduce the worked trace.
    body += [panel(600, 67, 278, 455, fill=PALE, stroke=GRAY),
             t(739, 104, "逐轮更新", 24, weight="bold")]
    trace = [
        ("处理P", "A=2，B=5"),
        ("处理A", "B=3，C=8，D=13"),
        ("处理B", "C=4，D=8"),
        ("处理C", "D=6"),
    ]
    for i, (step, value) in enumerate(trace):
        y = 157 + i*78
        body += [t(628, y, step, 22, anchor="start", weight="bold"),
                 t(628, y+31, value, 22, anchor="start"),
                 arrow(628, y+44, 850, y+44, color="#A0A0A0", width=1.4, marker=False)]
    body += [lines(739, 473, ["到D后沿前驱回溯", "P→A→B→C→D"], 22, weight="bold", step=29)]
    return wrap(570, "固定道路时间下的Dijkstra手算示例", "当前正文中的五节点有向图含八条边：P-A2、P-B5、A-B1、A-C6、A-D11、B-C1、B-D5、C-D2。右侧列出依次处理P、A、B、C时的距离更新，最终得到P-A-B-C-D，总时间6分钟。", "".join(body))


def fig7_svg(path_out: Path) -> None:
    # Exact values from section 2.5's four paired simulated requests.
    # Four cases: B completes V1,V2,V3 at 12,10,14 min; C completes V1,V2
    # at 8,9 min. V4 fails for both. Means below are computed from these rows.
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    import numpy as np

    b = np.array([12, 10, 14], dtype=float)
    c = np.array([8, 9], dtype=float)
    b_common = np.array([12, 10], dtype=float)
    c_common = np.array([8, 9], dtype=float)
    means = [b.mean(), c.mean(), b_common.mean(), c_common.mean()]
    assert means == [12.0, 8.5, 11.0, 8.5]
    font_match = subprocess.run(
        ["fc-match", "-f", "%{file}", FONT.split(",")[0]],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    if not font_match or not Path(font_match).is_file():
        raise RuntimeError("Noto Sans CJK SC is not available")
    font_manager.fontManager.addfont(font_match)
    font_name = font_manager.FontProperties(fname=font_match).get_name()

    # 16.5 pt source text scales to 10.74 pt when the 900 CSS px artwork is
    # inserted at 155 mm. Keep SVG text as text, not outlined glyph paths.
    rc = {
        "font.family": font_name,
        "font.size": 16.5,
        "axes.labelsize": 16.5,
        "xtick.labelsize": 16.5,
        "ytick.labelsize": 16.5,
        "svg.fonttype": "none",
        "axes.edgecolor": INK,
        "text.color": INK,
        "axes.labelcolor": INK,
        "xtick.color": INK,
        "ytick.color": INK,
        "figure.facecolor": WHITE,
        "axes.facecolor": WHITE,
        "savefig.facecolor": WHITE,
        "svg.hashsalt": "textbook-ch02-fig2-7-v1",
    }
    with mpl.rc_context(rc):
        fig, (ax_cover, ax_time) = plt.subplots(
            2, 1, figsize=(9.375, 6.2), layout="constrained",
            gridspec_kw={"height_ratios": [0.9, 2.0]},
        )
        # Coverage uses its own count scale and an explicit shared denominator.
        y = np.array([1, 0])
        cover = [3, 2]
        bars = ax_cover.barh(y, cover, color=[BLUE, "#B7C1CA"], edgecolor=INK,
                             linewidth=1.5, height=0.52)
        bars[1].set_hatch("///")
        ax_cover.set_yticks(y, ["方案B", "方案C"])
        ax_cover.set_xlim(0, 4.55)
        ax_cover.set_xticks([0, 1, 2, 3, 4])
        ax_cover.set_xlabel("完成请求数（共4个）")
        ax_cover.grid(axis="x", color="#B8B8B8", linewidth=0.7, linestyle=":")
        ax_cover.set_axisbelow(True)
        ax_cover.spines[["top", "right", "left"]].set_visible(False)
        ax_cover.tick_params(axis="y", length=0)
        for yi, v in zip(y, cover):
            ax_cover.text(v + 0.10, yi, f"{v}/4", va="center", ha="left",
                          fontsize=16.5, color=INK)

        # The time plot shows both all-success and common-success averages on
        # one zero-based minute axis, with the sample membership stated in labels.
        y2 = [3, 2, 1, 0]
        vals = [means[0], means[1], means[2], means[3]]
        colors = [BLUE, "#B7C1CA", BLUE, "#B7C1CA"]
        labels = [
            "成功均值 B（V1–V3）",
            "成功均值 C（V1–V2）",
            "共同成功 B（V1、V2）",
            "共同成功 C（V1、V2）",
        ]
        bars2 = ax_time.barh(y2, vals, color=colors, edgecolor=INK,
                             linewidth=1.4, height=0.58)
        for j in (1, 3):
            bars2[j].set_hatch("///")
        ax_time.set_yticks(y2, labels)
        ax_time.set_xlim(0, 15.2)
        ax_time.set_xticks([0, 5, 10, 15])
        ax_time.set_xlabel("平均耗时（分钟；只对完成请求求均值）")
        ax_time.grid(axis="x", color="#B8B8B8", linewidth=0.7, linestyle=":")
        ax_time.set_axisbelow(True)
        ax_time.spines[["top", "right", "left"]].set_visible(False)
        ax_time.tick_params(axis="y", length=0)
        for yi, v in zip(y2, vals):
            ax_time.text(v + 0.18, yi, f"{v:g}", va="center", ha="left",
                         fontsize=16.5, color=INK)
        fig.suptitle("未完成不是0分钟；比较方案时还要同时看覆盖率。",
                     fontsize=16.5, color=INK)
        fig.savefig(path_out, format="svg", bbox_inches=None, metadata={
            "Title": "四个模拟请求的覆盖与平均耗时比较",
            "Description": "B完成V1至V3，平均12分钟；C完成V1和V2，平均8.5分钟。共同完成的V1、V2上，B平均11分钟、C平均8.5分钟；覆盖分别为3/4与2/4。",
            "Date": None,
        })
        plt.close(fig)


def fig8() -> str:
    body = []
    coords = {"G": (88, 279), "P": (300, 130), "Q": (300, 422),
              "C": (520, 279), "D": (623, 121), "X": (818, 279)}
    # Ten exact undirected links from the capstone material. Only P-Q is a
    # stair segment, shown with a dashed line and a direct text label.
    links = [
        ("G", "P", "2", 190, 186, False), ("G", "Q", "4", 190, 369, False),
        ("P", "Q", "1·台阶", 300, 279, True), ("P", "C", "3", 416, 176, False),
        ("Q", "C", "2", 416, 380, False), ("P", "D", "5", 472, 113, False),
        ("C", "D", "2", 583, 180, False), ("D", "X", "3", 730, 180, False),
        ("Q", "X", "6", 560, 394, False), ("C", "X", "7", 680, 255, False),
    ]
    body += [t(450, 43, "无箭头表示双向；数字为道路分钟数", 22, weight="bold")]
    for a, b, label, lx, ly, dashed in links:
        body.append(edge(*coords[a], *coords[b], label, lx=lx, ly=ly,
                         dashed=dashed, directed=False))
    for key, (x, y) in coords.items():
        body.append(circle(x, y, key, r=34, stroke=BLUE if key == "C" else INK,
                           double=(key == "C")))
    body += [panel(44, 502, 812, 82, fill=PALE, stroke=GRAY),
             lines(450, 534, ["C点首次参访服务2分钟（只计一次）；服务完成≤8分钟，最终到X≤12分钟。",
                              "无障碍方案先排除P—Q台阶边；基础地图没有图中未列出的道路。"], 22, weight="bold", step=29)]
    return wrap(605, "E06确认道路和服务条件", "六个地点G、P、Q、C、D、X之间的十条双向道路及分钟数：G-P2、G-Q4、P-Q1（台阶）、P-C3、Q-C2、P-D5、C-D2、D-X3、Q-X6、C-X7。C点首次参访服务耗时2分钟且只计一次；题目另给完成与到达时限。", "".join(body))


FIGURES = [
    {
        "number": 1, "caption": "通知事实、记录与未知信息",
        "purpose": "辨认哪些字段能从来源直接记录，以及哪些承诺仍缺少证据。",
        "description": "对照模拟通知的原文事实与仍未说明的无台阶路线连接信息；电梯可达三层不能单独证明整段路线可达。",
        "source": "本书原创教学示意；通知内容为模拟。",
        "builder": fig1,
    },
    {
        "number": 2, "caption": "卷积网络的局部与组合响应示意",
        "purpose": "帮助理解局部图像信息如何经过多层组合进入任务输出，同时限制层级类比的含义。",
        "description": "以台阶形局部图像说明像素、可能的局部边缘响应、组合响应和任务输出；并明确真实网络不会保证每层对应固定现实概念。",
        "source": "本书原创概念示意；非真实模型激活图或实测结果。",
        "builder": fig2,
    },
    {
        "number": 3, "caption": "微型展板任务的依赖与时间安排",
        "purpose": "在一条共同时间轴上看出T1/T2可逻辑并行、T3/T4的依赖与最早4小时完成。",
        "description": "T1需1小时，T2需2小时，T3需2小时且依赖T1，T4需1小时且依赖T2和T3；在资源允许时最早第4小时完成。",
        "source": "本书原创教学示例；时间和任务均为模拟。",
        "builder": fig3,
    },
    {
        "number": 4, "caption": "自注意力中查询、键和值的关系",
        "purpose": "按查询匹配、权重形成、值汇总的次序解释注意力机制，并提示时间可见范围。",
        "description": "当前位置形成Q，与可访问位置的K逐一匹配并形成权重，再按权重合并对应V，生成当前位置的新表示；连线权重没有实测数值。",
        "source": "本书原创概念示意；无实测权重。",
        "builder": fig4,
    },
    {
        "number": 5, "caption": "联邦学习中的本地数据与模型更新",
        "purpose": "区分原始记录的本地保留、更新上传和汇总模型返回，并标出隐私边界。",
        "description": "三个机构各自在本地记录上训练并发送模型更新给协调方，聚合结果返回各机构；更新仍可能泄露信息，流程本身不构成隐私保证。",
        "source": "本书原创系统示意；不表示任何真实机构部署。",
        "builder": fig5,
    },
    {
        "number": 6, "caption": "Dijkstra逐轮更新与最短路线",
        "purpose": "把正文的有向道路、距离更新和6分钟回溯路线放在一幅图中检查。",
        "description": "当前正文的八条有向边为P-A2、P-B5、A-B1、A-C6、A-D11、B-C1、B-D5、C-D2；最短路线为P-A-B-C-D，6分钟。",
        "source": "本书原创教学示例；分钟数是固定模拟值。",
        "builder": fig6,
    },
    {
        "number": 7, "caption": "四个模拟请求的完成情况与耗时比较",
        "purpose": "并列检查覆盖和成功耗时，并区分全体成功请求与共同成功子集。",
        "description": "四个请求中B完成3个（V1、V2、V3，均值12分钟），C完成2个（V1、V2，均值8.5分钟）；只在共同成功的V1、V2上，B均值11分钟、C均值8.5分钟。",
        "source": "本书原创教学示例；四个请求为2.5节的模拟数据，不代表实地服务性能。",
        "matplotlib": True,
    },
    {
        "number": 8, "caption": "E06校园导览模拟地图",
        "purpose": "提供综合练习中可直接核对的确认道路、通行条件和任务限制。",
        "description": "图示六个地点和十条双向道路；P-Q为唯一含台阶边，C点首次服务2分钟且只计一次，服务完成不晚于第8分钟、抵达X不晚于第12分钟。",
        "source": "本书原创教学模拟；道路、方向、时间和条件依照章末E06材料绘制。",
        "builder": fig8,
    },
]


def export_png(svg_path: Path, target: Path, css_height: int) -> dict:
    if not CHROME.exists():
        raise FileNotFoundError(f"expected local renderer is unavailable: {CHROME}")
    svg = svg_path.read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="ch02-progressive-figure-") as temp_name:
        temp = Path(temp_name)
        html = temp / "figure.html"
        html.write_text(
            '<!doctype html><html><head><meta charset="utf-8"><style>'
            'html,body{margin:0;padding:0;width:900px;height:' + str(css_height) +
            'px;overflow:hidden;background:#fff}svg{display:block}</style></head><body>' +
            svg + '</body></html>',
            encoding="utf-8",
        )
        cmd = [
            str(CHROME), "--headless", "--no-sandbox", "--disable-gpu",
            "--disable-dev-shm-usage", "--hide-scrollbars",
            f"--user-data-dir={temp / 'profile'}", "--force-device-scale-factor=2.6666666667",
            f"--window-size=900,{css_height}", "--virtual-time-budget=1000",
            f"--screenshot={target}", html.as_uri(),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=45)
        if result.returncode or not target.exists():
            raise RuntimeError(f"Chrome failed for {svg_path.name}: {result.stderr[-2000:]}")
    from PIL import Image, ImageOps
    with Image.open(target) as image:
        color = image.convert("RGB")
        if color.width != PNG_WIDTH:
            raise RuntimeError(f"unexpected PNG width for {target.name}: {color.width}")
        color.save(target, format="PNG", dpi=(PPI, PPI), optimize=True)
        gray_path = target.with_name(target.stem + "-gray.png")
        ImageOps.grayscale(color).save(gray_path, format="PNG", dpi=(PPI, PPI), optimize=True)
        dims = {"width_px": color.width, "height_px": color.height}
    return {
        "color_png": target,
        "gray_png": gray_path,
        "dimensions_px": dims,
        "png_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
        "gray_sha256": hashlib.sha256(gray_path.read_bytes()).hexdigest(),
    }


def main() -> None:
    outputs = []
    for spec in FIGURES:
        number = spec["number"]
        svg_path = OUT / f"fig2-{number}.svg"
        png_path = OUT / f"fig2-{number}.png"
        if spec.get("matplotlib"):
            fig7_svg(svg_path)
            css_height = round(6.2 * 96)
        else:
            svg = spec["builder"]()
            svg_path.write_text(svg, encoding="utf-8")
            match = re.search(r'<svg[^>]+height="(\d+)px"', svg)
            if not match:
                raise ValueError(f"missing SVG height for figure {number}")
            css_height = int(match.group(1))
            font_sizes = [int(v) for v in re.findall(r'font-size="(\d+)px"', svg)]
            if not font_sizes or min(font_sizes) < MIN_FONT_PX:
                raise ValueError(f"minimum SVG label size failed for figure {number}")
        exported = export_png(svg_path, png_path, css_height)
        svg_hash = hashlib.sha256(svg_path.read_bytes()).hexdigest()
        outputs.append({
            "id": f"图2-{number}",
            "caption": spec["caption"],
            "instructional_purpose": spec["purpose"],
            "description": spec["description"],
            "source": spec["source"],
            "status": "ready",
            "editable_source": str(svg_path.relative_to(ROOT)),
            "file": str(png_path.relative_to(ROOT)),
            "png": str(png_path.relative_to(ROOT)),
            "grayscale_png": str(exported["gray_png"].relative_to(ROOT)),
            "sha256": exported["png_sha256"],
            "gray_sha256": exported["gray_sha256"],
            "svg_sha256": svg_hash,
            "insert_width_mm": INSERT_MM,
            "viewbox_width": VIEW_WIDTH,
            "png_ppi_at_insert": PPI,
            "declared_min_label_px": MIN_FONT_PX,
            "min_font_pt_at_insert": MIN_FONT_PT,
            "dimensions_px": exported["dimensions_px"],
            "gray_semantics": "文字标签、位置、边框、箭头、实/虚线、纹理或线宽共同编码；灰度PNG已导出供检查。",
        })
    manifest = {
        "style": "textbook-style-v1.0",
        "insert_width_mm": INSERT_MM,
        "png_ppi_at_insert": PPI,
        "min_label_pt_at_insert": MIN_FONT_PT,
        "render_command": "python materials/ch02-progressive/render_figures.py",
        "figures": outputs,
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
    print(json.dumps({
        "figures": len(outputs), "png_width_px": PNG_WIDTH, "ppi_at_insert": PPI,
        "min_label_pt_at_insert": MIN_FONT_PT,
        "hashes": [{"id": f["id"], "png": f["sha256"], "svg": f["svg_sha256"],
                    "gray": f["gray_sha256"]} for f in outputs],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
