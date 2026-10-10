"""生成第一章原创SVG，并用Chromium按同一源文件导出PNG。"""

import html
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets/figures/ch01"
FONT = "'Noto Sans CJK SC', 'Noto Sans CJK', sans-serif"


class Figure:
    def __init__(self, number, title, height=800):
        self.number = number
        self.height = height
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="{height}" viewBox="0 0 1400 {height}">',
            f'<title>图1-{number} {html.escape(title)}</title>',
            '<defs><marker id="arrow" markerWidth="12" markerHeight="12" refX="9" refY="4" orient="auto"><path d="M0,0 L9,4 L0,8" fill="none" stroke="#414141" stroke-width="1.5"/></marker></defs>',
            f'<rect width="1400" height="{height}" fill="white"/>',
        ]
        self.text(50, 60, f"图1-{number}  {title}", 36, bold=True)

    def text(self, x, y, value, size=28, bold=False, anchor="start"):
        self.parts.append(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" fill="#202020" font-weight="{700 if bold else 400}" text-anchor="{anchor}">{html.escape(value)}</text>')

    def box(self, x, y, width, height, lines, shade="#f5f5f5", size=28):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="7" fill="{shade}" stroke="#414141" stroke-width="2"/>')
        for i, line in enumerate(lines):
            self.text(x + 22, y + 42 + i * 44, line, size, bold=i == 0)

    def arrow(self, points, dashed=False):
        self.parts.append(f'<polyline points="{points}" fill="none" stroke="#414141" stroke-width="2.5" marker-end="url(#arrow)"' + (' stroke-dasharray="9 6"' if dashed else '') + '/>')

    def line(self, x1, y1, x2, y2):
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#7b7b7b" stroke-width="1.5"/>')

    def save(self):
        self.parts.append('</svg>')
        path = OUT / f"fig1-{self.number}.svg"
        path.write_text('\n'.join(self.parts) + '\n', encoding="utf-8")
        return path


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    paths = []
    f = Figure(1, "需求如何变成可检查的规则", 840)
    headers = [(50, '口头需求'), (500, '数据表示'), (950, '检查规则')]
    for x, s in headers:
        f.text(x + 12, 126, s, 30, True)
    rows = [
        (["每组都借到一次"], ["request_id", "完整请求清单"], ["每请求恰好一次", "同时检查遗漏和重复"]),
        (["只能在方便时借"], ["allowed_slots", "available_slots"], ["时段属于两表交集", "不能擅自改可用时间"]),
        (["需要显示功能"], ["required_capability", "capabilities"], ["功能满足请求", "开放不等于功能满足"]),
        (["设备不能撞期"], ["device_id + slot_id", "占用位置"], ["每位置至多一请求", "跨行检查重复占用"]),
    ]
    for i, row in enumerate(rows):
        y = 150 + i * 138
        for j, values in enumerate(row):
            f.box(50 + j * 450, y, 380, 114, values, size=27)
            if j < 2:
                f.arrow(f"438,{y+57} 491,{y+57}")
    f.text(50, 759, "教学示例：每请求占一个完整时段；现实应用还须确认时长和交接。", 27)
    f.text(50, 805, "读图：哪一项规则必须检查整张安排表，而不能只检查单行？", 27)
    paths.append(f.save())

    f = Figure(2, "从问题表示到检验的反馈", 880)
    f.box(50, 142, 280, 140, ["需求与条件", "目标、已知与待确认"], size=25)
    f.box(390, 142, 280, 140, ["问题表示", "字段、关系与规则"], size=25)
    f.box(730, 142, 280, 140, ["处理步骤", "生成并保存候选"], size=25)
    f.box(1070, 142, 280, 140, ["实际检验", "逐项检查并记录"], size=25)
    for a, b in [(330, 390), (670, 730), (1010, 1070)]:
        f.arrow(f"{a+7},212 {b-10},212")
    f.text(70, 106, "上方箭头：本轮处理；下方虚线：依据失败返回相应位置", 26)
    f.box(930, 425, 420, 170, ["检验结果与失败位置", "通过：保留有边界的方案", "失败：说明哪个条件不满足"], size=26)
    f.arrow("1210,289 1210,413")
    f.box(50, 660, 365, 142, ["条件有误或发生变化", "回到需求重新确认"], size=27)
    f.box(505, 660, 365, 142, ["字段或关系遗漏", "修订表示与规则"], size=27)
    f.box(960, 660, 365, 142, ["候选存在占用冲突", "修正处理步骤并重检"], size=27)
    f.arrow("1090,602 1090,625 1142,625 1142,650", True)
    f.arrow("1040,602 1040,625 687,625 687,650", True)
    f.arrow("980,602 980,625 232,625 232,650", True)
    f.arrow("50,730 25,730 25,315 190,315 190,292", True)
    f.arrow("505,730 470,730 470,325 530,325 530,292", True)
    f.arrow("1325,730 1375,730 1375,335 870,335 870,292", True)
    f.text(50, 852, "本书教学组织图：反馈可能改条件、表示或步骤，不是只重跑同一候选。", 26)
    paths.append(f.save())

    f = Figure(3, "可借用组合与候选安排", 850)
    f.text(50, 115, "○ 允许但未选     ● 本次已选     — 不允许；每列是一个开放的设备时段", 27)
    xs = [430, 625, 820, 1015, 1210]
    for x, name in zip(xs, ['D1-S1', 'D1-S2', 'D1-S3', 'D2-S2', 'D2-S3']):
        f.text(x, 183, name, 30, True, 'middle')
    allowed = [{0}, {0, 1, 3}, {1, 2, 3, 4}, {1, 2, 3, 4}]
    selected = [0, 1, 3, 2]
    for i, name in enumerate(['R1', 'R2', 'R3', 'R4']):
        y = 257 + i * 94
        f.text(95, y, name, 32, True)
        f.line(50, y + 30, 1345, y + 30)
        for j, x in enumerate(xs):
            f.text(x, y, '●' if selected[i] == j else '○' if j in allowed[i] else '—', 36, anchor='middle')
    f.box(50, 647, 1295, 127, ["关闭D2后：只剩D1-S1、D1-S2、D1-S3三个位置", "四个请求各需一个不同位置；4 > 3，因此原硬约束下无解。"], size=29)
    f.text(50, 815, "教学示例；D2-S1不开放，未列入可选位置。读图：R2为什么不能选择D1-S1？", 25)
    paths.append(f.save())

    f = Figure(4, "思想节点、贡献与证据", 800)
    f.text(50, 116, "按文献时间并置；本图没有直接影响箭头，横向位置不构成因果证明。", 27)
    blocks = [
        (50, ["1936收稿 / 1937书目", "Turing  [3]", "有限状态与符号操作", "通用计算机器", "及判定问题边界", "原文：§1、§6、§11"]),
        (510, ["1971  MIT报告", "Papert与Solomon  [4]", "学习者编程与探索", "通过活动表达想法", "教育设计主张", "原文：开篇及活动1"]),
        (970, ["2006  CACM观点文章", "Wing  [1]", "计算思维通用能力倡议", "强调概念思考超越编程", "不是首创全部思想的证据", "原文：pp.33–35"]),
    ]
    for x, lines in blocks:
        f.box(x, 170, 380, 345, lines, size=26)
    f.box(50, 574, 1300, 151, ["本书教学比较：如何表达可计算过程 / 如何借程序学习 / 谁需要这种能力", "三类问题互相启发；所附短摘录不足以建立人物之间的直接影响链。"], size=27)
    f.text(50, 772, "读图：从原文可以确认哪个贡献？哪个教育效果或影响关系仍不能确认？", 27)
    paths.append(f.save())

    f = Figure(5, "结构迁移与新增条件", 890)
    f.text(65, 125, "设备借用 E01", 31, True)
    f.text(615, 125, "社区场地 E03", 31, True)
    pairs = [('device_id', 'room_id'), ('capabilities', 'facilities（集合包含）'), ('allowed_slots', 'allowed_slots'), ('设备在某时段开放', '场地在某时段开放'), ('device_id / slot_id唯一', 'room_id / slot_id唯一')]
    for i, (left, right) in enumerate(pairs):
        y = 150 + i * 86
        f.box(50, y, 420, 66, [left], size=25)
        f.arrow(f"481,{y+33} 581,{y+33}")
        f.box(595, y, 540, 66, [right], size=25)
    f.box(50, 617, 1300, 194, ["新增条件：participants ≤ capacity；required_facilities ⊆ facilities", "反例：Q3有20人，C1容量12。时段不冲突、有投影仍不能安排。", "变体：C2降到18人后，Q3在两个场地都无位置；不能只换名字沿用旧解。"], size=28)
    f.text(50, 858, "教学示例；箭头只表示字段或规则对应，不表示两个领域的条件完全相同。", 27)
    paths.append(f.save())

    f = Figure(6, "不同思维视角需要的证据", 975)
    f.text(50, 119, "同一照明问题可同时使用多个视角；下面是本书教学综合，不是互斥分类。", 27)
    headers = [(55, '视角'), (265, '所问问题'), (685, '所需证据'), (1120, '回答边界')]
    for x, value in headers:
        f.text(x, 183, value, 29, True)
    rows = [
        ('计算', ['规则如何表示', '候选如何重复检查'], ['字段、条件', '实际检查结果'], ['模型内可行', '非现实效果']),
        ('数学', ['预算与能耗', '是否核算正确'], ['单位与假设', '可重算公式'], ['推算有条件', '瓦数非照度']),
        ('实证', ['台阶是否更易辨认', '溢出光是否减少'], ['适当比较', '实际观察与任务'], ['当前仅模拟', '尚无因果证据']),
        ('批判', ['主张是否过强', '谁的需求被遗漏'], ['原始支持', '假设与替代解释'], ['暴露证据缺口', '不等于给定结论']),
        ('设计', ['使用者怎样体验', '候选怎样修改'], ['用户任务', '原型与反馈'], ['需要真实验证', '不能假定需求']),
        ('系统', ['局部调整影响谁', '反馈是否有时延'], ['关系与边界', '维护和其他区域'], ['关系为待查假设', '非实测因果图']),
    ]
    for i, row in enumerate(rows):
        y = 215 + i * 110
        f.line(50, y - 9, 1350, y - 9)
        f.text(55, y + 38, row[0], 29, True)
        for x, values in zip([265, 685, 1120], row[1:]):
            for j, value in enumerate(values):
                f.text(x, y + 30 + 38 * j, value, 26)
    f.box(50, 893, 1300, 66, ['读图：一份正确的能耗表，还缺哪些证据才能回答“现实使用是否改善”？'], size=26)
    paths.append(f.save())

    f = Figure(7, "综合任务的目标、约束与检验", 875)
    f.text(50, 116, "E05虚构社区数字服务咨询预约；每请求一个完整时段，每工作人员每时段1个请求。", 26)
    f.box(50, 170, 385, 188, ['目标与问题说明', '全部4个请求得到安排', '效率偏好须另行说明'], size=28)
    f.box(510, 170, 385, 188, ['数据与资格例外', 'V1：general', 'V2：另具screen_reader'], size=27)
    f.box(970, 170, 385, 188, ['候选安排', '工作人员 + 请求 + 时段', 'P3必须由V2服务'], size=27)
    f.arrow('444,260 500,260')
    f.arrow('904,260 960,260')
    f.box(750, 444, 605, 154, ['逐项检验', '恰好一次、时间允许、资格满足', '同一工作人员同一时段不可重复'], size=28)
    f.arrow('1162,367 1162,434')
    f.box(50, 444, 605, 154, ['迁移与现实边界', '会安排不证明满意、公平或可达性', '需要领域信息与真实服务效果证据'], size=28)
    f.arrow('740,520 665,520')
    f.box(50, 667, 1305, 129, ['条件变化：撤除V2的screen_reader资格，P3无合格工作人员 → 无解', '可提出增援等协商提案，但不能把原条件下不合格的安排交付为可行解。'], size=28)
    f.arrow('1162,607 1162,657', True)
    f.arrow('50,732 25,732 25,400 700,400 700,368', True)
    f.text(50, 836, '读图：找出从条件变化返回资格数据的步骤，再指出模型未回答的一个问题。', 26)
    paths.append(f.save())
    return paths


def main():
    paths = build()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        page = browser.new_page(viewport={"width": 1400, "height": 1000}, device_scale_factor=2)
        for path in paths:
            page.goto(path.as_uri())
            page.locator('svg').screenshot(path=str(path.with_suffix('.png')))
            print(path.name, path.with_suffix('.png').stat().st_size)
        browser.close()


if __name__ == '__main__':
    main()
