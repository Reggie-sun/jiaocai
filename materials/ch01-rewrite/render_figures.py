"""Render this chapter's editable diagrams at the shared print baseline."""
from pathlib import Path
from html import escape
import hashlib
import json
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets/figures/ch01-rewrite"
OUT.mkdir(parents=True, exist_ok=True)
INK, BLUE = "#222222", "#1F4E79"


def text(x, y, value, size=24, anchor="middle"):
    return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}">{escape(value)}</text>'


def box(x, y, width, lines, dashed=False):
    height = 40 + 36 * len(lines)
    parts = [f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="5" fill="white" stroke="{INK}" stroke-width="2"' + (' stroke-dasharray="8 5"' if dashed else '') + '/>']
    parts += [text(x + width / 2, y + 36 + i * 36, s) for i, s in enumerate(lines)]
    return "".join(parts)


def line(x1, y1, x2, y2, arrow=True, dashed=False):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{BLUE}" stroke-width="2.5"' + (' marker-end="url(#arrow)"' if arrow else '') + (' stroke-dasharray="7 5"' if dashed else '') + '/>'


def save(number, title, height, parts, description):
    svg = '<svg xmlns="http://www.w3.org/2000/svg" width="900" height="%s" viewBox="0 0 900 %s">' % (height, height)
    svg += '<defs><marker id="arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8" fill="#1F4E79"/></marker></defs>'
    svg += '<rect width="900" height="100%" fill="white"/><g font-family="Noto Sans CJK SC" fill="#222222">' + "".join(parts) + '</g></svg>'
    source = OUT / f"fig1-{number}.svg"
    target = OUT / f"fig1-{number}.png"
    source.write_text(svg, encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="ch01-figure-") as temporary:
        html = Path(temporary) / "figure.html"
        html.write_text('<html><head><style>html,body{margin:0;padding:0}</style></head><body>'+svg+'</body></html>', encoding="utf-8")
        result = subprocess.run([
            "/usr/bin/google-chrome", "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
            f"--user-data-dir={temporary}/profile", "--force-device-scale-factor=2.6666666667",
            f"--window-size=900,{height}", "--virtual-time-budget=1000", f"--screenshot={target}", html.as_uri(),
        ], capture_output=True, text=True, timeout=45)
        if result.returncode or not target.exists():
            raise RuntimeError(result.stderr[-2000:])
    return {"id": f"图1-{number}", "caption": title, "file": str(target.relative_to(ROOT)), "editable_source": str(source.relative_to(ROOT)), "source": "本书原创教学图；模拟数据及作者教学分析。", "description": description, "status": "pending_visual_review", "viewbox_width": 900, "min_font_px": 24, "insert_width_mm": 155, "min_font_pt_at_insert": round(24 * (155 / 25.4 * 72) / 900, 2), "ppi_at_insert": round(2400 / (155 / 25.4)), "sha256": hashlib.sha256(target.read_bytes()).hexdigest(), "svg_sha256": hashlib.sha256(source.read_bytes()).hexdigest()}


figures = []
figures.append(save(1, "需求如何变成可检查的规则", 355, [
    box(20, 30, 250, ["口头要求", "都借到、早点、公平"]),
    box(325, 30, 250, ["对象与关系", "请求、设备、时段"]),
    box(630, 30, 250, ["逐项检查", "归属、开放、占用"]),
    line(270, 80, 320, 80), line(575, 80, 625, 80),
    box(190, 220, 520, ["公平口径仍待确认", "结构化不能替代事实与价值确认"], True),
], "口头需求分成对象与可检查关系，公平标准独立保留为待确认。"))

parts = [text(190, 34, "三项请求"), text(650, 34, "允许的位置"), box(455, 48, 290, ["b", "c"], True), box(760, 240, 115, ["d"])]
for i in range(3):
    y = 90 + 80 * i
    parts += [box(65, y - 30, 170, [f"T{i+1}"]), line(235, y + 5, 530, 85, False), line(235, y + 5, 530, 125, False)]
parts += [text(580, 222, "允许位置并集：2"), text(450, 340, "3项请求争用2个位置；d没有允许关系")]
figures.append(save(2, "局部候选与全局瓶颈", 385, parts, "三项请求各连到b/c，d存在但不可达；请求数三大于并集位置数二。"))

parts = [box(305, 25, 290, ["实际检查", "失败证据是什么？"]), box(20, 205, 260, ["候选违反约束", "修正选择与回退"]), box(320, 205, 260, ["模型看不见冲突", "修改表示与规则"]), box(620, 205, 260, ["条件缺失或无解", "核实或协商条件"])]
parts += [line(380, 137, 150, 200), line(450, 137, 450, 200), line(520, 137, 750, 200), text(450, 360, "修改后重查受影响的全部结论")]
figures.append(save(3, "从检查证据返回选择、表示与条件", 400, parts, "检查证据按错误类型分别返回选择、模型和需求，修改后重新检查。"))

parts = [box(20, 40, 270, ["图灵", "1936收到／宣读", "1937出版", "配置与计算边界"]), box(315, 40, 270, ["Papert与Solomon", "1971", "程序探索的", "教育设计"]), box(610, 40, 270, ["Wing", "2006／2010", "通用能力与", "问题表述"]), text(450, 290, "横向排列表示年代先后，不表示直接影响"), text(450, 335, "比较问题、贡献与证据；不补造传承箭头")]
figures.append(save(4, "思想节点、贡献与证据", 380, parts, "三个思想节点按时间排列，不以影响箭头暗示未经支持的因果传承。"))

parts = [box(40, 30, 300, ["旧设备模型", "请求→设备时段", "功能与唯一占用"]), box(560, 30, 300, ["新场地模型", "请求→场地时段", "时间与唯一占用"]), line(340, 90, 555, 90), text(450, 65, "结构对应"), box(180, 240, 540, ["重建允许关系：人数≤容量", "所需设施⊆可用设施；核对资源身份"]), line(705, 145, 600, 235)]
figures.append(save(5, "结构迁移与新增条件", 385, parts, "单位置互斥结构可对应，人数、设施和身份语义须重新核查。"))

parts = [text(210, 40, "同一场地的时间区间"), text(450, 410, "半开区间端点相接不重叠；独占准备／清理计入占用")]
for index, (label, intervals) in enumerate([
    ("重叠", [(9, 11, "A [9,11)"), (10, 11, "B [10,11)")]),
    ("相接", [(9, 11, "A [9,11)"), (11, 12, "B [11,12)")]),
    ("清理与准备", [(9, 11 + 20/60, "A至11:20"), (10.75, 12, "B从10:45")]),
]):
    y = 80 + 108 * index
    parts += [text(22, y + 35, label, anchor="start")]
    for j, (s, e, label2) in enumerate(intervals):
        x, w = 245 + (s - 9) * 150, (e - s) * 150
        parts += [f'<rect x="{x}" y="{y+j*42}" width="{w}" height="34" fill="white" stroke="{INK}" stroke-width="2"' + (' stroke-dasharray="7 4"' if j else '') + '/>', text(x+w/2, y+25+j*42, label2)]
figures.append(save(6, "连续占用、端点相接与准备清理", 450, parts, "重叠与相接按半开区间区分；第三组加入20分钟清理和15分钟准备后冲突。"))

parts = []
for i, (name, question) in enumerate([("计算", "规则与重复检查"), ("数学", "单位与数量关系"), ("实证", "比较与实际观测"), ("批判", "主张与替代解释"), ("设计", "用户任务与原型"), ("系统", "边界、反馈与时延")]):
    col, row = i % 2, i // 2
    parts += [box(30+col*450, 25+row*132, 390, [name, question])]
parts += [text(450, 447, "同一问题需要互补证据；各视角不构成互斥分类")]
figures.append(save(7, "不同思维视角需要的证据", 490, parts, "六种思维视角分别提出不同问题与证据要求，可以对同一任务共同使用。"))

parts = [box(290, 20, 320, ["数字服务任务", "目标、输入与边界"]), box(35, 205, 355, ["模型内检查", "时间、资格、唯一占用", "当前数据能否安排？"]), box(510, 205, 355, ["现实证据", "实际时长、服务体验", "模型是否足以解释？"]), line(340, 132, 210, 200), line(560, 132, 690, 200), text(450, 400, "两种证据各有范围；新观察可以改变模型")]
figures.append(save(8, "综合任务的模型检验与现实证据", 445, parts, "模型合格安排与现实服务证据分成两条路径，任何一条通过不替另一条验收。"))

(OUT / "manifest.json").write_text(json.dumps({"style": "textbook-style-v1.0", "figures": figures}, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"figures": len(figures), "ppi": 393, "minimum_label_pt": 11.72}))
