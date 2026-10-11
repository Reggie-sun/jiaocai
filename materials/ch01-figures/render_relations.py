"""Create the editable draw.io sources for Chapter 1 figures 1, 3, 5, 7 and 8."""

from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets/figures/ch01-figures"
INK = "#222222"
BLUE = "#1F4E79"
PALE = "#E8EFF5"
MUTED = "#D5D8DC"
FONT = "Noto Sans CJK SC"


class Diagram:
    def __init__(self, number, height):
        self.number = number
        self.height = height
        self.root = ET.Element("mxfile", {"host": "drawio", "version": "32.4.1", "type": "device"})
        page = ET.SubElement(self.root, "diagram", {"id": f"ch01-fig1-{number}", "name": "Page-1"})
        model = ET.SubElement(
            page,
            "mxGraphModel",
            {
                "dx": "900", "dy": str(height), "grid": "1", "gridSize": "10",
                "guides": "1", "tooltips": "1", "connect": "1", "arrows": "1",
                "fold": "1", "page": "1", "pageScale": "1", "pageWidth": "900",
                "pageHeight": str(height), "background": "#FFFFFF", "math": "0", "shadow": "0",
            },
        )
        self.cells = ET.SubElement(model, "root")
        ET.SubElement(self.cells, "mxCell", {"id": "0"})
        ET.SubElement(self.cells, "mxCell", {"id": "1", "parent": "0"})
        self.next_id = 2

    def shape(self, x, y, w, h, label, style, *, font_size=24, bold=False, connectable=True):
        cell_id = str(self.next_id)
        self.next_id += 1
        full_style = (
            f"fontFamily={FONT};fontSize={font_size};fontColor={INK};"
            + ("fontStyle=1;" if bold else "")
            + style
            + ("connectable=0;" if not connectable else "")
        )
        cell = ET.SubElement(
            self.cells,
            "mxCell",
            {
                "id": cell_id, "value": label.replace("\n", "\uE000"),
                "style": full_style, "vertex": "1", "parent": "1",
            },
        )
        ET.SubElement(cell, "mxGeometry", {"x": str(x), "y": str(y), "width": str(w), "height": str(h), "as": "geometry"})
        return cell_id

    def text(self, x, y, w, h, label, *, size=24, bold=False, color=INK, align="center"):
        return self.shape(
            x, y, w, h, label,
            f"text;html=1;strokeColor=none;fillColor=none;align={align};verticalAlign=middle;whiteSpace=wrap;fontColor={color};",
            font_size=size, bold=bold, connectable=False,
        )

    def line(self, x1, y1, x2, y2, *, color=BLUE, width=2, dashed=False, arrow=False, waypoints=()):
        cell = ET.SubElement(
            self.cells,
            "mxCell",
            {
                "id": str(self.next_id),
                "value": "",
                "style": (
                    "edgeStyle=none;html=1;rounded=0;"
                    f"strokeColor={color};strokeWidth={width};"
                    + ("dashed=1;dashPattern=6 5;" if dashed else "")
                    + ("endArrow=classic;endFill=1;" if arrow else "endArrow=none;startArrow=none;")
                ),
                "edge": "1", "parent": "1",
            },
        )
        self.next_id += 1
        geometry = ET.SubElement(cell, "mxGeometry", {"relative": "1", "as": "geometry"})
        ET.SubElement(geometry, "mxPoint", {"x": str(x1), "y": str(y1), "as": "sourcePoint"})
        for x, y in waypoints:
            ET.SubElement(ET.SubElement(geometry, "Array", {"as": "points"}), "mxPoint", {"x": str(x), "y": str(y)})
        ET.SubElement(geometry, "mxPoint", {"x": str(x2), "y": str(y2), "as": "targetPoint"})

    def outline(self, x, y, w, h, *, color=INK, width=2):
        self.line(x, y, x + w, y, color=color, width=width)
        self.line(x + w, y, x + w, y + h, color=color, width=width)
        self.line(x + w, y + h, x, y + h, color=color, width=width)
        self.line(x, y + h, x, y, color=color, width=width)

    def save(self):
        OUT.mkdir(parents=True, exist_ok=True)
        target = OUT / f"fig1-{self.number}.drawio"
        ET.indent(self.root, space="  ")
        data = ET.tostring(self.root, encoding="utf-8", xml_declaration=True)
        # Preserve explicit draw.io line breaks while letting ElementTree escape XML text.
        target.write_bytes(data.replace("\uE000".encode("utf-8"), b"&#xa;"))
        return target


def fig1_1():
    d = Diagram(1, 650)
    d.text(40, 24, 235, 48, "口头表达", size=25, bold=True, color=BLUE)
    d.text(315, 24, 170, 48, "判断类别", size=25, bold=True, color=BLUE)
    d.text(545, 24, 315, 48, "字段与检查", size=25, bold=True, color=BLUE)
    rows = [
        ("都借到", "硬约束", "每条请求恰好安排一次", "solid"),
        ("设备功能满足；\n双方时段均可用", "硬约束", "所需功能匹配\n设备与请求均允许该时段", "solid"),
        ("同一时刻不能\n借给两组", "硬约束", "设备身份 × 时段\n同一位置至多一组", "solid"),
        ("尽量早点", "偏好", "硬约束满足后\n按完成时段先后比较", "round"),
        ("分配公平", "待确认", "先约定公平口径\n再确认由谁判断", "dashed"),
    ]
    for i, (phrase, kind, rule, treatment) in enumerate(rows):
        y = 82 + i * 96
        d.line(40, y + 87, 860, y + 87, color=MUTED, width=1)
        d.text(52, y + 3, 218, 78, phrase, size=24, bold=True)
        if treatment == "solid":
            style = f"rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor={INK};strokeWidth=2;"
        elif treatment == "round":
            style = f"ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor={BLUE};strokeWidth=2;"
        else:
            style = f"rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor={INK};strokeWidth=2;dashed=1;dashPattern=5 4;"
        d.shape(320, y + 11, 160, 60, kind, style, font_size=24, bold=True)
        d.line(275, y + 41, 310, y + 41, color=BLUE, width=2, arrow=True)
        d.line(490, y + 41, 530, y + 41, color=BLUE, width=2, arrow=True, dashed=treatment == "dashed")
        d.text(545, y, 315, 80, rule, size=24)
    d.text(80, 594, 740, 30, "偏好可排序；未知口径须保留为未知", size=24, bold=True)
    return d.save()


def fig1_3():
    d = Diagram(3, 660)
    d.text(25, 22, 270, 58, "检查证据", size=26, bold=True, color=BLUE)
    d.text(315, 22, 270, 58, "失效来源", size=26, bold=True, color=BLUE)
    d.text(610, 22, 265, 58, "回到哪里修改", size=26, bold=True, color=BLUE)
    lanes = [
        ("所选安排\n重复占用", "本次选择\n或程序状态", "换位 / 回退"),
        ("真实冲突\n没有被表示", "模型关系\n或占用规则不足", "补全表示 / 规则"),
        ("全部合法选择\n已穷尽仍无解", "输入条件缺失\n或当前实例无解", "核实条件 / 协商"),
    ]
    for i, (evidence, cause, target) in enumerate(lanes):
        y = 108 + i * 156
        # Each horizontal lane is a separate diagnosis path, rather than a shared sequence.
        d.shape(38, y, 248, 104, evidence,
                f"rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor={INK};strokeWidth=2;", font_size=25, bold=True)
        d.shape(326, y, 248, 104, cause,
                f"rounded=0;whiteSpace=wrap;html=1;fillColor={PALE};strokeColor={BLUE};strokeWidth=2;", font_size=24)
        d.shape(615, y, 248, 104, target,
                f"rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor={INK};strokeWidth=2;", font_size=24, bold=True)
        d.line(288, y + 52, 317, y + 52, arrow=True)
        d.line(576, y + 52, 605, y + 52, arrow=True)
    d.line(38, 584, 863, 584, color=INK, width=2)
    d.text(80, 595, 740, 44, "三条独立返回路径；改动后重查受影响的候选与结论", size=24, bold=True)
    return d.save()


def fig1_5():
    d = Diagram(5, 710)
    d.text(46, 20, 340, 52, "设备借用：E01", size=26, bold=True, color=BLUE)
    d.text(514, 20, 340, 52, "场地活动：E03", size=26, bold=True, color=BLUE)
    d.text(387, 20, 126, 52, "角色映射", size=24, bold=True)
    rows = [
        ("请求集合 R", "活动集合 Q"),
        ("位置：设备 × 时段", "位置：场地 × 时段"),
        ("允许关系 A", "允许关系 A′"),
        ("同一设备时段\n至多一个请求", "同一场地时段\n至多一项活动"),
    ]
    for i, (old, new) in enumerate(rows):
        y = 86 + i * 88
        d.shape(50, y, 338, 64, old,
                f"rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor={INK};strokeWidth=2;", font_size=24)
        d.shape(512, y, 338, 64, new,
                f"rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor={INK};strokeWidth=2;", font_size=24)
        d.line(397, y + 32, 503, y + 32, color=BLUE, width=2, arrow=True)
    d.text(65, 454, 770, 43, "新增筛选条件", size=25, bold=True, color=BLUE)
    d.shape(50, 504, 385, 78, "参加人数 ≤ 场地容量",
            f"rounded=1;whiteSpace=wrap;html=1;fillColor={PALE};strokeColor={BLUE};strokeWidth=2;", font_size=24, bold=True)
    d.shape(465, 504, 385, 78, "所需设施 ⊆ 可用设施",
            f"rounded=1;whiteSpace=wrap;html=1;fillColor={PALE};strokeColor={BLUE};strokeWidth=2;", font_size=24, bold=True)
    d.line(242, 476, 242, 496, arrow=True)
    d.line(657, 476, 657, 496, arrow=True)
    d.text(68, 603, 764, 80, "还须复核资源身份与冲突口径。结构对应只支持逐项检查，\n不推出全部可行解等价。", size=24, bold=True)
    return d.save()


def fig1_7():
    d = Diagram(7, 740)
    nodes = [
        ("计算", "规则能否检查条件？", "输入 / 约束", 30, 25),
        ("数学", "数量与单位一致？", "量纲 / 算术", 600, 25),
        ("实证", "现场表现如何？", "观测 / 比较", 30, 282),
        ("批判", "证据是否还有别解？", "来源 / 替代解释", 600, 282),
        ("设计", "用户的任务是什么？", "任务 / 原型", 30, 535),
        ("系统", "影响会传到哪里？", "边界 / 反馈\n时延", 600, 535),
    ]
    # Equal-size spokes attach all six perspectives to one shared question; no arrow encodes sequence or rank.
    spokes = [
        ((414, 312), (255, 175)), ((486, 312), (645, 175)),
        ((375, 350), (300, 350)), ((525, 350), (600, 350)),
        ((414, 388), (255, 535)), ((486, 388), (645, 535)),
    ]
    for title, question, evidence, x, y in nodes:
        d.text(x + 8, y + 3, 254, 34, title, size=25, bold=True, color=BLUE)
        d.text(x + 8, y + 38, 254, 50, question, size=24)
        d.text(x + 8, y + 89, 254, 56, evidence, size=24, bold=True)
    d.shape(375, 310, 150, 76, "步道照明\n同一问题",
            f"ellipse;whiteSpace=wrap;html=1;fillColor={PALE};strokeColor={BLUE};strokeWidth=2;", font_size=24, bold=True)
    # Create every vertex before edges; free-standing connectors otherwise start a shifted export origin.
    for _, _, _, x, y in nodes:
        d.outline(x, y, 270, 150, color=INK, width=2)
    for start, end in spokes:
        d.line(*start, *end, color=BLUE, width=2)
    d.text(90, 700, 720, 30, "六种并列视角可共同使用；不表示权重、顺序或因果", size=24, bold=True)
    return d.save()


def fig1_8():
    d = Diagram(8, 715)
    d.shape(282, 20, 336, 72, "综合任务\n目标、输入与边界",
            f"rounded=1;whiteSpace=wrap;html=1;fillColor={PALE};strokeColor={BLUE};strokeWidth=2;", font_size=24, bold=True)
    # A shared context branches into two evidence domains with different acceptance scopes.
    d.line(450, 92, 450, 112, color=BLUE, width=2)
    d.line(222, 112, 678, 112, color=BLUE, width=2)
    d.line(222, 112, 222, 127, color=BLUE, width=2, arrow=True)
    d.line(678, 112, 678, 127, color=BLUE, width=2, arrow=True)
    d.outline(28, 132, 390, 374, color=INK, width=2)
    d.outline(482, 132, 390, 374, color=INK, width=2)
    d.text(48, 145, 350, 52, "模型内检查", size=27, bold=True, color=BLUE)
    d.text(502, 145, 350, 52, "现实证据", size=27, bold=True, color=BLUE)
    d.shape(55, 213, 336, 72, "资格 · 时段 · 唯一占用",
            f"rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor={INK};strokeWidth=2;", font_size=24)
    d.shape(55, 314, 336, 84, "逐项复核\n当前数据能否安排？",
            f"rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor={BLUE};strokeWidth=2;", font_size=24)
    d.shape(55, 425, 336, 62, "结论范围：这组输入的可行性",
            f"rounded=0;whiteSpace=wrap;html=1;fillColor={PALE};strokeColor={INK};strokeWidth=2;", font_size=24, bold=True)
    d.shape(509, 213, 336, 72, "实际时长 · 等待 · 服务体验",
            f"rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor={INK};strokeWidth=2;", font_size=24)
    d.shape(509, 314, 336, 84, "比较可能解释\n资源不足？单次服务超时？",
            f"rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor={BLUE};strokeWidth=2;", font_size=24)
    d.shape(509, 425, 336, 62, "结论范围：实际观察到的表现",
            f"rounded=0;whiteSpace=wrap;html=1;fillColor={PALE};strokeColor={INK};strokeWidth=2;", font_size=24, bold=True)
    d.text(110, 533, 680, 40, "各自有独立验收范围；一项通过不替另一项通过", size=24, bold=True)
    d.text(85, 584, 730, 36, "若观察与模型假设冲突，可修订模型并重新检查", size=24, bold=True, color=BLUE)
    # Dashed line marks a possible feedback after a conflict, not automatic validation.
    d.line(678, 516, 222, 516, color=BLUE, width=2, dashed=True, arrow=True)
    return d.save()


def main():
    paths = [fig1_1(), fig1_3(), fig1_5(), fig1_7(), fig1_8()]
    for path in paths:
        # Parse each emitted document immediately to catch malformed XML from generated labels.
        ET.parse(path)
    print("\n".join(str(path.relative_to(ROOT)) for path in paths))


if __name__ == "__main__":
    main()
