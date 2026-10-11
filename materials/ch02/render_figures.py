"""Build the eight editable Chapter 2 teaching figures at print size.

The SVG is the source of truth. PNG exports are 2400 px wide (about 393 ppi
when inserted at the shared 155 mm text width).
"""
from __future__ import annotations

from html import escape
from pathlib import Path
import hashlib
import json
import math
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets/figures/ch02"
OUT.mkdir(parents=True, exist_ok=True)
INK = "#222222"
BLUE = "#1F4E79"
PALE = "#F1F3F5"
WIDTH = 900
INSERT_MM = 155
PNG_WIDTH = 2400
MIN_FONT_PX = 22


def txt(x: float, y: float, value: str, size: int = 24, anchor: str = "middle",
        weight: str = "normal", fill: str = INK) -> str:
    if size < MIN_FONT_PX:
        raise ValueError(f"text below print minimum: {value!r} at {size}px")
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
            f'font-size="{size}" font-weight="{weight}" fill="{fill}">{escape(value)}</text>')


def multiline(x: float, y: float, values: list[str], size: int = 24,
              anchor: str = "middle", weight: str = "normal") -> str:
    return "".join(txt(x, y + 31 * i, value, size, anchor, weight) for i, value in enumerate(values))


def box(x: float, y: float, w: float, h: float, lines: list[str], *, dashed: bool = False,
        fill: str = "white", stroke: str = INK, radius: int = 8,
        size: int = 23, weight: str = "normal") -> str:
    dash = ' stroke-dasharray="9 6"' if dashed else ""
    start = y + h / 2 - (len(lines) - 1) * 15.5 + 8
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="2.5"{dash}/>' +
            multiline(x + w / 2, start, lines, size, weight=weight))


def node(x: float, y: float, label: str, *, settled: bool = False,
         size: int = 24, square: bool = False) -> str:
    if square:
        shape = f'<rect x="{x-34}" y="{y-30}" width="68" height="60" rx="4" fill="white" stroke="{INK}" stroke-width="3" stroke-dasharray="9 5"/>'
    else:
        shape = f'<circle cx="{x}" cy="{y}" r="34" fill="white" stroke="{INK}" stroke-width="3"/>'
        if settled:
            shape += f'<circle cx="{x}" cy="{y}" r="27" fill="none" stroke="{BLUE}" stroke-width="2.5"/>'
    return shape + txt(x, y + 8, label, size, weight="bold")


def line(x1: float, y1: float, x2: float, y2: float, *, arrow: bool = False,
         dashed: bool = False, color: str = BLUE, width: float = 3.0) -> str:
    dash = ' stroke-dasharray="10 7"' if dashed else ""
    marker = ' marker-end="url(#arrow)"' if arrow else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{color}" stroke-width="{width}"{dash}{marker}/>')


def edge(x1: float, y1: float, x2: float, y2: float, label: str,
         lx: float, ly: float, *, arrow: bool = False, dashed: bool = False,
         highlight: bool = False) -> str:
    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy)
    radius = 36
    sx, sy = x1 + dx * radius / length, y1 + dy * radius / length
    ex, ey = x2 - dx * radius / length, y2 - dy * radius / length
    color = BLUE if highlight else INK
    width = 5.0 if highlight else 2.5
    path = line(sx, sy, ex, ey, arrow=arrow, dashed=dashed, color=color, width=width)
    label_width = max(52, len(label) * 23 + 20)
    label_rect = (f'<rect x="{lx-label_width/2}" y="{ly-22}" width="{label_width}" height="30" '
                  f'rx="4" fill="white" stroke="none"/>')
    return path + label_rect + txt(lx, ly, label, 22, fill=color, weight="bold" if highlight else "normal")


def wrap(height: int, content: str, desc: str, figure_id: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{height}" '
            f'viewBox="0 0 900 {height}" role="img" aria-labelledby="title desc">'
            f'<title id="title">{escape(figure_id)}</title><desc id="desc">{escape(desc)}</desc>'
            '<defs><marker id="arrow" markerWidth="8" markerHeight="6" refX="7.5" refY="3" '
            'orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L8,3 L0,6 z" fill="#1F4E79"/></marker>'
            '<pattern id="dots" width="9" height="9" patternUnits="userSpaceOnUse">'
            '<circle cx="2" cy="2" r="1.2" fill="#777777"/></pattern></defs>'
            f'<rect width="900" height="{height}" fill="white"/>'
            '<g font-family="Noto Sans CJK SC, sans-serif">' + content + '</g></svg>')


def make_fig1() -> tuple[int, str, str]:
    p = []
    p += [txt(225, 52, "建筑级：适合粗略定位", 25, weight="bold"),
          txt(675, 52, "入口级：支持通行判断", 25, weight="bold")]
    p += [box(24, 82, 402, 340, [], dashed=True, stroke="#777777"),
          box(474, 82, 402, 340, [], dashed=True, stroke="#777777")]
    # Coarse view: two real entrances are merged and only the shortest approach remains.
    p += [node(90, 230, "西门"), box(239, 183, 160, 94, ["资料中心", "入口已合并"], size=23)]
    p += [edge(126, 230, 239, 230, "3分钟", 182, 210, arrow=True)]
    p += [txt(225, 324, "可答：大致到达建筑", 23), txt(225, 362, "不能答：是否无台阶通行", 23)]
    # Detailed view: N and M are distinct destinations and have different access attributes.
    p += [node(525, 230, "西门"), node(798, 160, "N"), node(798, 300, "M")]
    p += [edge(562, 218, 762, 168, "3分钟", 652, 168, arrow=True)]
    p += [edge(562, 241, 762, 291, "7分钟", 680, 350, arrow=True, highlight=True)]
    p += [line(798, 194, 798, 266, arrow=True),
          txt(846, 222, "外绕", 22, weight="bold"), txt(846, 249, "4分钟", 22)]
    p += [txt(798, 111, "北门：有台阶", 22), txt(798, 355, "南门：无台阶", 22, weight="bold")]
    p += [txt(675, 394, "无台阶任务选M；3分钟路线不合格", 22, weight="bold", fill=BLUE)]
    desc = "同一资料中心在粗略模型中只有一个节点，北门和南门被合并；入口模型保留西门到北门3分钟且有台阶、到南门7分钟且无台阶，以及两门间绕行4分钟。"
    return 455, "两种导览表示及其可回答的问题", wrap(455, "".join(p), desc, "图2-1教学示意")


def make_fig2() -> tuple[int, str, str]:
    p = [txt(450, 47, "普通移动保留服务进度；办理服务才跨层", 25, weight="bold"),
         box(35, 78, 830, 190, [], dashed=True, stroke="#777777"),
         box(35, 305, 830, 170, [], stroke=BLUE),
         txt(58, 108, "s=0：尚未完成服务", 22, anchor="start", weight="bold"),
         txt(58, 335, "s=1：已经完成服务", 22, anchor="start", weight="bold")]
    # Top layer: ordinary moves keep s=0; the direct two-minute arrival cannot
    # satisfy the service-completed destination requirement.
    p += [box(92, 142, 112, 54, ["起点 S,0"], size=22),
          node(486, 174, "P,0", square=True), node(786, 174, "X,0", square=True),
          node(280, 224, "C,0"),
          line(204, 169, 450, 169, arrow=True), txt(328, 151, "总计2分钟", 22, weight="bold"),
          line(522, 174, 746, 174, arrow=True),
          line(194, 189, 246, 213, arrow=True),
          txt(786, 223, "不满足已服务目标", 22, weight="bold")]
    # Cross-layer transition exists only at C when service is completed.
    p += [line(280, 258, 280, 345, arrow=True),
          txt(352, 289, "办理完成：s=0→1", 22, anchor="start", weight="bold", fill=BLUE)]
    # Bottom layer: after the service transition, ordinary movement stays in s=1.
    p += [node(280, 379, "C,1"), node(486, 379, "P,1"), node(786, 379, "X,1"),
          line(314, 379, 450, 379, arrow=True), line(520, 379, 750, 379, arrow=True),
          txt(450, 455, "起点经C办理服务后到P：总计5分钟（含服务；不拆分路段）", 22, weight="bold", fill=BLUE),
          box(80, 502, 740, 89, ["同一地点P的(P,0)与(P,1)必须分别保留",
                                  "目标是(X,1)；不能只因位置相同就合并两种状态"], size=22)]
    desc = "图示两层状态图。普通移动在同一服务进度层内进行；只有在C办理服务时，状态从C,0跨到C,1。上方直接路线到P需2分钟，但出口X,0不满足已服务条件；下方起点经C办理后到P的整段共5分钟，从P到出口的时间未在此示意中给定，最终目标仍为X,1。"
    return 610, "同一位置在不同任务进度下的状态扩展", wrap(610, "".join(p), desc, "图2-2状态扩展示意")


def make_fig3() -> tuple[int, str, str]:
    p = [txt(450, 45, "处理环节由有向边连接；模块实现由边界封装", 24, weight="bold")]
    # This is the chapter's E02 dependency shape, without durations or a critical-path answer.
    coords = {"A": (92, 265), "B": (270, 146), "C": (270, 377),
              "D": (466, 377), "E": (466, 146), "F": (652, 265), "G": (810, 265)}
    specs = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"),
             ("B", "E"), ("D", "F"), ("E", "F"), ("F", "G")]
    labels = {
        "A": ["A", "读入快照"],
        "B": ["B", "节点规范", "map=M1"],
        "C": ["C", "通行规则", "map=M1 / C1"],
        "D": ["D", "计算路线", "需版本兼容"],
        "E": ["E", "生成说明"],
        "F": ["F", "端到端检查"],
        "G": ["G", "发布"],
    }
    dims = {"A": (104, 84), "B": (137, 96), "C": (137, 96), "D": (142, 96),
            "E": (137, 84), "F": (146, 84), "G": (91, 84)}
    for a, b in specs:
        x1, y1 = coords[a]
        x2, y2 = coords[b]
        dx, dy = x2 - x1, y2 - y1
        unit = math.hypot(dx, dy)
        ux, uy = dx / unit, dy / unit
        w1, h1 = dims[a]
        w2, h2 = dims[b]
        off1 = min((w1 / 2) / abs(ux) if ux else float("inf"),
                   (h1 / 2) / abs(uy) if uy else float("inf"))
        off2 = min((w2 / 2) / abs(ux) if ux else float("inf"),
                   (h2 / 2) / abs(uy) if uy else float("inf"))
        p.append(line(x1 + ux * off1, y1 + uy * off1,
                      x2 - ux * off2, y2 - uy * off2, arrow=True))
    for k, (x, y) in coords.items():
        w, h = dims[k]
        p.append(box(x-w/2, y-h/2, w, h, labels[k],
                     dashed=k in ("B", "C", "D", "E"), size=22,
                     stroke=BLUE if k in ("B", "C", "D", "E") else INK))
    p += [txt(466, 477, "B、C向D提供的数据须兼容；箭头表示依赖，不表示执行耗时", 22, weight="bold"),
          txt(466, 514, "虚线边框圈出封装模块；内部实现可变，对外承诺保持可组合", 22)]
    desc = "A读入快照后分支到B节点规范与C通行规则；D计算路线依赖B和C，E说明依赖B；F端到端检查依赖D和E；G发布依赖F。模块虚线框表示封装边界，B与C都标注map=M1，C另标profile=C1，D要求输入版本兼容。图不表示耗时或关键链。"
    return 545, "有向无环依赖图与带版本语义的接口", wrap(545, "".join(p), desc, "图2-3依赖示意")


def make_fig4() -> tuple[int, str, str]:
    p = [txt(450, 46, "规则只在有支持的局部输入范围内使用", 25, weight="bold"),
         # A conceptual boundary, not a learned threshold or confidence region.
         '<path d="M205 305 C180 222 242 127 365 119 C495 92 611 143 635 228 C663 311 594 371 479 380 C359 390 236 373 205 305 Z" '
         'fill="#F1F3F5" stroke="#1F4E79" stroke-width="3" stroke-dasharray="11 7"/>',
         txt(420, 154, "局部观察支持范围", 23, weight="bold", fill=BLUE)]
    p += [line(124, 408, 781, 408, arrow=False, color=INK, width=2.5),
          line(124, 408, 124, 87, arrow=False, color=INK, width=2.5),
          txt(790, 435, "输入特征 a", 22, anchor="end"),
          '<text transform="rotate(-90 62 264)" x="62" y="264" text-anchor="middle" font-family="Noto Sans CJK SC, sans-serif" font-size="22" fill="#222222">输入特征 b</text>']
    # Supported observations (filled circles) and unclassified boundary cases (open circles).
    for x, y in [(270, 274), (321, 221), (355, 310), (416, 254), (464, 335), (517, 222), (557, 286)]:
        p.append(f'<circle cx="{x}" cy="{y}" r="9" fill="{INK}" stroke="{INK}" stroke-width="2"/>')
    for x, y in [(219, 187), (604, 202), (580, 346)]:
        p.append(f'<circle cx="{x}" cy="{y}" r="10" fill="white" stroke="{BLUE}" stroke-width="3"/>')
    for x, y in [(727, 161), (695, 292), (160, 336)]:
        p.append(f'<path d="M{x-9},{y-9} L{x+9},{y+9} M{x+9},{y-9} L{x-9},{y+9}" stroke="{INK}" stroke-width="3"/>')
    p += [txt(236, 190, "边缘待核验", 22, anchor="start", fill=BLUE),
          txt(746, 169, "先复核", 22, anchor="start", weight="bold", fill=BLUE),
          box(182, 447, 536, 78, ["实心点：范围内观察   空心点：边界待核验   ×：范围外", "边界只是教学示意，不是阈值或统计置信区间"], size=22)]
    desc = "概念性的二维输入空间。虚线轮廓表示当前有样本支持的局部范围，实心圆表示该范围内的观察，空心圆表示邻近边界而待核验的样本，叉号表示未观测或例外的范围外位置。轮廓不提供数值阈值或统计置信区间。"
    return 550, "观察样本、规则适用区域与例外边界", wrap(550, "".join(p), desc, "图2-4适用范围示意")


def make_fig5() -> tuple[int, str, str]:
    p = [txt(450, 48, "确定C=5之后：D=7与E=8仍在前沿", 25, weight="bold")]
    coords = {"P": (92, 269), "A": (300, 143), "B": (300, 394), "C": (520, 269), "E": (650, 421), "D": (796, 269)}
    edges = [
        ("P", "A", "2", 195, 178, False), ("P", "B", "3", 191, 363, True),
        ("A", "C", "6", 408, 183, False),
        ("B", "C", "2", 411, 350, True), ("B", "E", "5", 468, 421, False),
        ("C", "D", "2", 657, 252, True), ("E", "D", "3", 735, 364, False),
    ]
    for a, b, label, lx, ly, chosen in edges:
        x1, y1 = coords[a]
        x2, y2 = coords[b]
        p.append(edge(x1, y1, x2, y2, label, lx, ly, arrow=True, highlight=chosen))
    # Route A→D along the top and enter from D's top edge so its arrowhead
    # stays distinct from the C→D arrow entering from the left.
    p.append('<path d="M300 108 C430 88 650 104 796 239" fill="none" stroke="#222222" stroke-width="2.5" marker-end="url(#arrow)"/>')
    p.append(f'<rect x="{554-31}" y="102" width="62" height="30" rx="4" fill="white"/>')
    p.append(txt(554, 124, "11", 22))
    distances = {"P": (92, 218, "0"), "A": (255, 116, "2"), "B": (300, 466, "3"),
                 "C": (520, 218, "5"), "E": (650, 477, "8"), "D": (704, 218, "7")}
    for name, (x, y, distance) in distances.items():
        p.append(txt(x, y, f"距P={distance}", 22, anchor="end" if name == "A" else "middle", weight="bold"))
    for label in ("P", "A", "B", "C"):
        p.append(node(*coords[label], label, settled=True))
    for label in ("E", "D"):
        p.append(node(*coords[label], label, square=True))
    p += [box(53, 518, 794, 72,
              ["双圆：已确定；虚线方框：前沿候选。D=7是当前最小待选距离",
               "下一步取出D并结束；回溯P→B→C→D，路线总时间7分钟"],
              fill=PALE, stroke=BLUE, size=22)]
    desc = "有向边及分钟数为P至A2、P至B3、A至C6、A至D11、B至C2、B至E5、C至D2、E至D3。处理C=5后，P、A、B、C已确定；D=7、E=8仍在前沿，最佳路线为P-B-C-D，总计7。"
    return 610, "路径搜索中的前沿状态与暂定距离", wrap(610, "".join(p), desc, "图2-5算法示例")


def make_fig6() -> tuple[int, str, str]:
    p = [txt(450, 47, "同一批五个请求：时间与覆盖分开看", 25, weight="bold"),
         txt(450, 82, "讲解示例数据；“失败”表示没有合格路线，不计入成功平均", 22)]
    # Header and rows show each paired outcome; all data comes from the paragraph.
    left, top = 83, 126
    colx = [130, 280, 440, 602, 757]
    p += [txt(colx[0], top, "请求", 22, weight="bold"),
          txt(colx[1], top, "基线B", 22, weight="bold"),
          txt(colx[2], top, "候选C", 22, weight="bold"),
          txt(colx[3], top, "配对状态", 22, weight="bold"),
          txt(colx[4], top, "分组", 22, weight="bold")]
    p.append(line(left, 139, 817, 139, color=INK, width=2.5))
    bvals = ["6分", "7分", "8分", "9分", "10分"]
    cvals = ["5分", "6分", "7分", "失败", "失败"]
    for i, (bv, cv) in enumerate(zip(bvals, cvals), start=1):
        y = 181 + (i - 1) * 55
        p.append(txt(colx[0], y, f"R{i}", 23, weight="bold"))
        p.append(txt(colx[1], y, bv, 23))
        p.append(txt(colx[2], y, cv, 23, fill=BLUE if cv != "失败" else INK, weight="bold" if cv != "失败" else "normal"))
        state = "共同成功" if i <= 3 else "仅B成功"
        p.append(txt(colx[3], y, state, 22))
        p.append(txt(colx[4], y, "未提供", 22))
        if i in (4,):
            p.append(line(105, y+28, 790, y+28, color="#777777", width=1.8, dashed=True))
    p += [box(45, 477, 810, 78, ["成功均值：B=(6+7+8+9+10)/5=8分钟；C=(5+6+7)/3=6分钟"], size=22),
          box(45, 574, 390, 77, ["覆盖：B 5/5", "C 3/5"], stroke=BLUE, size=22),
          box(465, 574, 390, 77, ["共同成功R1–R3", "C比B各快1分钟"], size=22),
          txt(450, 690, "本例未提供通行条件分组标签；真实分组需另有数据，不能由图推造", 22, weight="bold")]
    desc = "五个成对请求的基线时间为6、7、8、9、10分钟，候选为5、6、7分钟后两个失败；故成功均值分别为8与6分钟，覆盖率分别为5/5与3/5，共同成功的前三个请求候选各快1分钟。未给分组标签，因此不作分组统计。"
    return 720, "配对比较、覆盖与分组评价", wrap(720, "".join(p), desc, "图2-6讲解示例")


def make_fig7() -> tuple[int, str, str]:
    p = [txt(450, 47, "自动流程必须区分未提交、已确认与结果未知", 25, weight="bold"),
         box(38, 103, 202, 84, ["提交前检查", "判断是否可提交"], size=22),
         box(348, 103, 205, 84, ["提交", "保留原操作ID"], size=22),
         box(658, 103, 204, 84, ["等待权威确认"], fill=PALE, size=22),
         box(34, 238, 218, 84, ["明确拒绝", "确定尚无外部效果"], dashed=True, size=22),
         box(340, 238, 220, 84, ["确认已应用", "结束并记录"], stroke=BLUE, size=22),
         box(650, 238, 220, 108, ["断连或超时", "UNKNOWN", "暂停重试"], dashed=True, stroke=BLUE, size=22)]
    p += [line(240, 145, 348, 145, arrow=True), txt(294, 137, "符合", 22),
          line(553, 145, 658, 145, arrow=True),
          line(139, 187, 139, 238, arrow=True), txt(181, 221, "拒绝", 22),
          line(730, 187, 450, 238, arrow=True),
          line(760, 187, 760, 238, arrow=True, dashed=True), txt(824, 218, "未知", 22, anchor="end"),
          box(338, 369, 224, 77, ["使用原操作ID查询", "权威状态"], dashed=True, size=22),
          line(760, 346, 510, 369, arrow=True, dashed=True)]
    outcomes = [(34, ["确认未执行", "确认无在途请求", "幂等契约允许", "才可有限次同ID重试"]),
                (340, ["确认已应用", "记录外部结果", "结束"]),
                (646, ["仍无法确认", "保持暂停", "不自动重试"])]
    targets = [142, 450, 756]
    for (x, lines), target in zip(outcomes, targets):
        p.append(line(450, 446, target, 490, arrow=True, dashed=lines[0] == "仍无法确认"))
        p.append(box(x, 490, 218, 126, lines,
                     dashed=lines[0] == "仍无法确认", stroke=BLUE if lines[0] == "仍无法确认" else INK, size=22))
    # Only the confirmed-safe branch can loop to the submit step. The connector
    # runs outside every node so it cannot be mistaken for another outcome.
    p.append('<path d="M34 553 H17 V80 H450 V103" fill="none" stroke="#1F4E79" stroke-width="2.5" marker-end="url(#arrow)"/>')
    p += [txt(450, 665, "计时器或暂时查无记录都不能证明未执行；证据不足时继续停留在UNKNOWN", 22, weight="bold")]
    desc = "提交前拒绝表示无外部效果；提交后确认成功则记录结果；断连/超时进入UNKNOWN，先查询原操作ID。查询确认未执行且重试语义安全时才允许同ID重试；查明已执行则结束；仍无法确认时继续暂停。"
    return 690, "自动执行中的检查、确认与未知状态", wrap(690, "".join(p), desc, "图2-7状态示意")


def make_fig8() -> tuple[int, str, str]:
    p = [txt(450, 47, "E06导览图：道路分钟数与通行条件", 25, weight="bold"),
         txt(450, 80, "无箭头＝双向；实线＝无台阶；虚线并标“台阶”＝P—Q", 22)]
    coords = {"G": (80, 340), "P": (300, 160), "Q": (300, 480),
              "C": (540, 340), "D": (620, 160), "X": (820, 340)}
    # Draw exact, undirected edge set. Place the stair edge behind the other links.
    specs = [
        ("G", "P", "2", 185, 232, False), ("G", "Q", "4", 185, 445, False),
        ("P", "Q", "", 300, 340, True), ("P", "C", "3", 418, 216, False),
        ("Q", "C", "2", 450, 374, False), ("P", "D", "5", 460, 137, False),
        ("C", "D", "2", 600, 235, False), ("D", "X", "3", 730, 225, False),
        ("Q", "X", "6", 560, 454, False), ("C", "X", "7", 680, 315, False),
    ]
    for a, b, label, lx, ly, dashed in specs:
        x1, y1 = coords[a]
        x2, y2 = coords[b]
        if label:
            p.append(edge(x1, y1, x2, y2, label, lx, ly, dashed=dashed))
        else:
            # Stair link label sits beside the line; keep the line continuous.
            p.append(line(x1, y1 + 36, x2, y2 - 36, dashed=dashed, color=INK, width=2.5))
    for name, (x, y) in coords.items():
        p.append(node(x, y, name, settled=False))
    p += [txt(420, 347, "1分钟·台阶", 22, weight="bold"),
          box(51, 555, 798, 92, ["状态：(位置, 已服务?)；首次到C服务2分钟，只由0→1一次",
                                   "约束：服务完成≤8分钟；最终到X≤12分钟；台阶profile须先筛边"], size=22)]
    desc = "无向边及分钟数完整列出G-P2、G-Q4、P-Q1台阶、P-C3、Q-C2、P-D5、C-D2、D-X3、Q-X6、C-X7。首次到C服务2分钟，服务完成不晚于8分钟，最终到X不晚于12分钟。"
    return 680, "E06社区导览地图", wrap(680, "".join(p), desc, "图2-8综合练习")


FIGURES = [
    (1, "任务相关的信息取舍", "建筑合并会隐藏入口与通行属性；用粗略定位和无台阶到达任务比较信息是否足够。", make_fig1),
    (2, "位置与服务进度状态", "同一位置P的服务标志不同会改变后续目标判断，路径总时间不擅自拆成未知路段。", make_fig2),
    (3, "依赖关系与模块边界", "有向边描述先后依赖，虚线框描述模块封装，版本字段说明边界组合的兼容约束。", make_fig3),
    (4, "规则适用区域与例外", "概念示意表示局部样本支持、边界待核验和范围外不外推；不提供数值阈值或统计置信区间。", make_fig4),
    (5, "Dijkstra算法前沿", "P-A-B-C-E-D教学有向图的准确权重、处理C之后暂定距离和最短路线。", make_fig5),
    (6, "成对评价与覆盖", "以2.5.1五个请求比较两个方法的成功时间、失败分母和共同成功子集；不伪造分组标签。", make_fig6),
    (7, "有界自动化与UNKNOWN", "确定拒绝、成功确认和提交后未知分别进入不同状态；未知通过原操作ID查证后才能恢复。", make_fig7),
    (8, "综合导览地图", "绘制E06十条无向道路、分钟数、唯一台阶边、C点一次服务与完成/到达时限。", make_fig8),
]


def render(number: int, height: int, svg: str) -> dict:
    source = OUT / f"fig2-{number}.svg"
    target = OUT / f"fig2-{number}.png"
    source.write_text(svg, encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="ch02-figure-") as temporary:
        html = Path(temporary) / "figure.html"
        html.write_text('<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;padding:0;background:white}svg{display:block}</style></head><body>' + svg + '</body></html>', encoding="utf-8")
        result = subprocess.run([
            "/usr/bin/google-chrome", "--headless", "--no-sandbox", "--disable-gpu",
            "--hide-scrollbars", f"--user-data-dir={temporary}/profile",
            "--force-device-scale-factor=2.6666666667", f"--window-size=900,{height}",
            "--virtual-time-budget=1000", f"--screenshot={target}", html.as_uri(),
        ], capture_output=True, text=True, timeout=45)
        if result.returncode or not target.exists():
            raise RuntimeError(f"Chrome failed for figure {number}: {result.stderr[-2000:]}")
    png_data = target.read_bytes()
    png_width, png_height = struct.unpack(">II", png_data[16:24])
    return {"path": str(target.relative_to(ROOT)), "svg_path": str(source.relative_to(ROOT)),
            "png_sha256": hashlib.sha256(png_data).hexdigest(),
            "svg_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "png_bytes": target.stat().st_size, "svg_bytes": source.stat().st_size,
            "png_width_px": png_width, "png_height_px": png_height}


def main() -> None:
    outputs = []
    min_pt = round(MIN_FONT_PX * INSERT_MM * 72 / 25.4 / WIDTH, 2)
    ppi = round(PNG_WIDTH / (INSERT_MM / 25.4))
    for number, use, description, builder in FIGURES:
        height, caption, svg = builder()
        files = render(number, height, svg)
        outputs.append({
            "id": f"图2-{number}", "caption": caption, "instructional_purpose": use,
            "description": description, "source": "本书原创教学示意；图内数据来自章内明确说明的教学模拟情境。",
            "status": "rendered_pending_parent_integration_review",
            "editable_source": files["svg_path"], "png": files["path"],
            "file": files["path"], "sha256": files["png_sha256"],
            "insert_width_mm": INSERT_MM, "viewbox_width": WIDTH,
            "png_ppi_at_insert": round(files["png_width_px"] / (INSERT_MM / 25.4)),
            "declared_min_label_px": MIN_FONT_PX, "min_label_pt_at_insert": min_pt,
            "min_font_pt_at_insert": min_pt,
            "gray_semantics": "关系同时使用节点文字、箭头或实/虚线、圆形/方框与明确说明；结论不只依靠颜色。",
            **files,
        })
    manifest = {
        "style": "textbook-style-v1.0", "insert_width_mm": INSERT_MM,
        "png_ppi_at_insert": ppi, "min_label_pt_at_insert": min_pt,
        "render_command": "python3 materials/ch02/render_figures.py",
        "figures": outputs,
    }
    (ROOT / "materials/ch02/figure-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"figures": len(outputs), "png_ppi": ppi, "min_label_pt": min_pt,
                      "files": [{"id": f["id"], "png_bytes": f["png_bytes"], "sha256": f["png_sha256"]} for f in outputs]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
