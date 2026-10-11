"""Editable task figures; numerical inputs remain in the author manifest."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import math
import re

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("figure_primitives", ROOT / "materials/ch03-layout/render_figures.py")
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)
text, lines, box, line, path = p.text, p.text_lines, p.box, p.line, p.path
BLUE, GRAY, PALE, WHITE = p.BLUE, p.GRAY, p.PALE, p.WHITE


def node(x, y, width, values, height=85):
    return box(x, y, width, height, stroke=BLUE) + lines(x + width / 2, y + 33, values, step=30)


def circle(x, y, values, radius=76):
    return f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{WHITE}" stroke="{BLUE}" stroke-width="2"/>' + lines(x, y - 10, values, step=30)


def cycle(labels):
    out = []
    points = [(450 + 285 * math.cos(-math.pi / 2 + i * 2 * math.pi / len(labels)), 280 + 170 * math.sin(-math.pi / 2 + i * 2 * math.pi / len(labels))) for i in range(len(labels))]
    for i, (x, y) in enumerate(points):
        xx, yy = points[(i + 1) % len(points)]
        dx, dy = xx - x, yy - y
        distance = math.hypot(dx, dy)
        out.append(line(x + dx / distance * 79, y + dy / distance * 79, xx - dx / distance * 87, yy - dy / distance * 87, color=BLUE, arrow=True))
    for (x, y), label in zip(points, labels):
        out.append(circle(x, y, label))
    out += [text(450, 273, "依据证据往返", 24, weight="bold"), text(450, 306, "并记录修正理由", 22), text(450, 582, "环路是教学组织，不表示每次都按固定顺序执行", 22)]
    return 620, "".join(out)


def chapter4(number, item):
    number = {2: 3, 3: 4, 4: 2}.get(number, number)
    if number == 1:
        return cycle([["解读", "任务与语境"], ["分析", "主张与理由"], ["评估", "证据与规则"], ["推理", "暂定结论"], ["解释", "说明依据"], ["自我调节", "检查并修正"]])
    if number == 2:
        out = [node(40, 50, 330, ["转发数与评论", "只说明传播情况"]), node(530, 50, 330, ["原始材料与来源", "检查对应主张"]), text(450, 100, "≠", 40, weight="bold")]
        out += [line(695, 145, 695, 207, color=BLUE, arrow=True), node(515, 217, 360, ["来源是否彼此独立？", "同一稿件转载≠多份证据"])]
        out += [line(695, 312, 695, 365, color=BLUE, arrow=True), node(40, 377, 820, ["结论范围：材料支持什么，又没有支持什么？", "将传播热度与事实支持分别记录"], 100)]
        return 510, "".join(out)
    if number == 3:
        out = [node(305, 35, 290, ["先前准备程度", "可能的共同原因"]), node(60, 300, 290, ["是否使用AI", "观察到的选择"]), node(550, 300, 290, ["通过结果", "观察到的结果"])]
        out += [line(340, 130, 230, 286, color=BLUE, arrow=True), line(565, 130, 665, 286, color=BLUE, arrow=True), line(363, 343, 537, 343, color=BLUE, dash="8 7", arrow=True), text(450, 318, "待检验", 22), text(450, 457, "共同原因可能产生相关；虚线不是已证实的因果效应", 22)]
        return 495, "".join(out)
    if number == 4:
        data = item["data"]
        assert data["tp"] + data["fn"] + data["fp"] + data["tn"] == data["total"]
        out = [text(520, 40, "教学模拟：1000条记录", 24, weight="bold"), text(370, 94, "系统提示专员", 22), text(670, 94, "系统未提示", 22)]
        for y, label, left, right in [(122, "实际需要专员", ["正确提示", str(data["tp"])], ["漏报", str(data["fn"])]), (260, "实际普通问题", ["误报", str(data["fp"])], ["正确放行", str(data["tn"])])]:
            out += [lines(105, y + 58, [label[:4], label[4:]], step=30), node(220, y, 290, left, 125), node(520, y, 300, right, 125)]
        out += [text(450, 438, "提示精确率＝96÷(96＋132)≈42.1%", 22), text(450, 477, "召回率＝96÷(96＋24)＝80.0%", 22), text(450, 516, "准确率＝(96＋748)÷1000＝84.4%", 22)]
        return 550, "".join(out)
    if number == 5:
        out = [node(40, 40, 330, ["证据：有限试点记录", "对象、时间和口径清楚"]), node(530, 40, 330, ["假设：能迁移到新对象", "需要额外核验"]), node(250, 235, 400, ["推理连接", "证据怎样支持这一主张？"], 100)]
        out += [line(215, 135, 360, 218, color=BLUE, arrow=True), line(695, 135, 540, 218, color=BLUE, dash="8 7", arrow=True), line(450, 345, 450, 392, color=BLUE, arrow=True), node(40, 402, 820, ["有限结论：在已测条件下，可继续有限验证", "反例、反对理由与回应需在旁边公开"], 100)]
        return 535, "".join(out)
    out = [text(450, 40, "从复杂争论到可以检查的问题", 24, weight="bold")]
    labels = [["分解", "目标与对象", "证据及缺口"], ["模式识别", "共同结构", "保留例外"], ["检查规则", "分母与约束", "检验假设"], ["比较与反馈", "敏感性分析", "结论边界"]]
    for i, values in enumerate(labels):
        out.append(node(35 + i * 220, 115, 185, values, 140))
        if i < 3:
            out.append(line(225 + i * 220, 183, 249 + i * 220, 183, color=BLUE, arrow=True))
    out += [path("M795 280 V350 H135 V280", color=BLUE, arrow=True), text(450, 395, "证据不足或排序不稳：返回补材料、改表示或缩小结论", 22), text(450, 444, "可执行检查帮助论证；价值取舍仍需说明理由", 22)]
    return 480, "".join(out)


def chapter5(number, item):
    if number == 1:
        out = [node(305, 30, 290, ["调查任务与约束", "先界定要解决的问题"])]
        for i, label in enumerate([["改变信息表达"], ["改变服务渠道"], ["改变匹配顺序"], ["改变确认流程"]]):
            x = 30 + i * 220
            out += [line(450, 127, x + 90, 205, color=BLUE, arrow=True), node(x, 220, 180, label, 75), line(x + 90, 306, 450, 380, color=BLUE, arrow=True)]
        out += [node(220, 395, 460, ["硬约束先筛查，再比较偏好", "总分不能抵消硬约束", "选择有限原型并测试"], 130), path("M690 445 H885 V73 H610", color=BLUE, arrow=True), text(450, 580, "未覆盖关键问题或测试失败 → 返回调查与发散", 22)]
        return 615, "".join(out)
    if number == 2:
        out = [node(40, 30, 820, ["模拟观察：页面显示空位，仍未完成预约", "先记录差异，不能直接决定原因"], 100)]
        for x, label in [(50, ["候选解释A", "状态更新延迟"]), (350, ["候选解释B", "资格或规则不清"]), (650, ["候选解释C", "入口操作有障碍"])]:
            out += [node(x, 205, 200, label, 100), line(450, 141, x + 100, 191, color=BLUE, dash="8 7", arrow=True), line(x + 100, 317, 450, 375, color=BLUE, arrow=True)]
        out += [node(145, 390, 610, ["证据能区分哪种解释？", "检查记录、任务操作与对应条件"], 100), path("M775 441 H870 V75", color=BLUE, arrow=True), text(450, 550, "无法区分时保留“未知”，修订问题与下一步", 22)]
        return 590, "".join(out)
    if number == 3:
        out = [text(450, 36, "五种工作模式，入口可按实际问题选择", 24, weight="bold")]
        labels = [["共情", "理解人的任务"], ["定义", "明确问题"], ["构思", "形成候选"], ["原型", "表达假设"], ["测试", "取得反馈"]]
        for i, label in enumerate(labels):
            x = 20 + i * 180
            out += [node(x, 110, 145, label, 115), line(x + 72, 62, x + 72, 96, color=BLUE, arrow=True)]
        out += [path("M812 245 V305 H272 V245", color=BLUE, arrow=True), path("M632 259 V363 H92 V245", color=BLUE, arrow=True), node(65, 425, 770, ["模式名称与任选入口：d.school资料", "回返路径：本书为教学迭代绘制", "纸面原型可检验假设，不等同于可上线的MVP"], 140)]
        return 600, "".join(out)
    if number == 4:
        out = [text(245, 37, "源域：在线服务", 24, weight="bold"), text(665, 37, "目标域：维修预约", 24, weight="bold")]
        pairs = [(["用户提出请求"], ["顾客描述维修任务"]), (["服务方检查资源"], ["技师确认零件与时段"]), (["服务状态变化"], ["维修阶段与预约变更"]), (["双方获得反馈"], ["电话/窗口/线上同步"])]
        for i, (left, right) in enumerate(pairs):
            y = 95 + i * 95
            out += [node(40, y, 350, left, 75), node(510, y, 350, right, 75), line(400, y + 37, 498, y + 37, color=BLUE, arrow=True)]
        out += [node(40, 550, 820, ["失效点：账户与设备门槛、库存滞后、责任未落实", "保留的是任务关系；访问方式与现场条件须重新核验"], 100), text(450, 498, "实线表示候选对应，不是迁移成功的实测证明", 22)]
        return 680, "".join(out)
    if number == 5:
        out = [text(450, 35, "四类材料支持不同范围的论断", 24, weight="bold")]
        rows = [(["Stukeley回忆", "后来记述的谈话"], ["苹果谈话的线索", "存在记忆距离"], ["不能推出", "一次顿悟完成理论"]), (["Orville当日日记", "飞行与计时记录"], ["当时的观察", "保留计时不确定"], ["不能推出", "完整航空发展脉络"]), (["Smithsonian综述", "馆藏研究整理"], ["观察、测量和试验", "研究过程的脉络"], ["不能视为", "同日原始观察"]), (["Jinek等实验论文", "2012年体外实验"], ["特定实验中的", "RNA引导DNA切割"], ["不能直接推出", "全部应用安全与伦理"])]
        for i, (left, middle, right) in enumerate(rows):
            y = 95 + i * 150
            out += [node(35, y, 250, left, 110), node(325, y, 250, middle, 110), node(615, y, 250, right, 110), line(291, y + 55, 315, y + 55, color=BLUE, arrow=True), line(585, y + 55, 609, y + 55, color=BLUE, dash="7 6")]
        out += [text(450, 733, "先看材料记录，再限定推论，最后说明教学解释", 22), text(450, 778, "四行不是简单的证据高低排名", 22)]
        return 815, "".join(out)
    if number == 6:
        values = [["默认前提", "先选房间"], ["反向问题", "先描述任务？"], ["保留约束", "资源与责任"], ["可证伪测试", "任务能完成？"]]
        out = [text(450, 35, "反转一个主要前提，保留必要条件", 24, weight="bold")]
        for i, label in enumerate(values):
            out += [node(30 + i * 220, 110, 180, label, 100)]
            if i < 3:
                out += [line(216 + i * 220, 160, 242 + i * 220, 160, color=BLUE, arrow=True)]
        out += [path("M780 225 V295 H120 V225", color=BLUE, arrow=True), node(40, 360, 820, ["原型不接入真实资源，使用相同教学数据与任务", "能否理解匹配、检查错误、请求帮助？", "发现访问障碍、隐私或责任问题时返回修订"], 140), text(450, 555, "循环允许否定新设想，不承诺必然获得创新", 22)]
        return 590, "".join(out)
    out = [text(130, 32, "强化学习", 24, weight="bold"), node(155, 73, 220, ["智能体", "依据策略选行动"], 85), node(605, 73, 220, ["环境", "后续结果"], 85), line(386, 95, 594, 95, color=BLUE, arrow=True), text(490, 75, "行动", 22), line(595, 148, 386, 148, color=BLUE, arrow=True), text(490, 185, "状态与奖励", 22), text(450, 223, "评估累计目标与试错边界", 22), line(35, 250, 865, 250)]
    out += [text(130, 285, "迁移学习", 24, weight="bold"), node(100, 320, 270, ["源任务知识", "参数或表示"], 90), node(570, 320, 270, ["目标任务适配", "独立验证"], 90), line(381, 365, 559, 365, color=BLUE, arrow=True), text(475, 339, "迁移", 22), text(450, 458, "比较目标基线，检查负迁移与分布差异", 22), line(35, 485, 865, 485)]
    out += [text(130, 525, "联邦学习", 24, weight="bold"), node(335, 550, 230, ["聚合方", "全局模型"], 90), node(95, 700, 260, ["参与方A：本地数据", "本地训练"], 90), node(565, 700, 260, ["参与方B：本地数据", "本地训练"], 90), line(348, 648, 255, 689, color=BLUE, arrow=True), line(242, 688, 326, 620, color=BLUE, dash="8 7", arrow=True), line(551, 648, 654, 689, color=BLUE, arrow=True), line(667, 688, 574, 620, color=BLUE, dash="8 7", arrow=True), text(450, 670, "模型↓ 更新↑", 22), text(450, 837, "数据留端 ≠ 隐私保证；核验更新、权限与退出规则", 22)]
    return 875, "".join(out)


def chapter6(number, item):
    if number == 1:
        out = [text(450, 38, "每项需求都要连到可以查看的证据", 24, weight="bold")]
        labels = [["用户关切", "说明来源"], ["需求编号", "验收条件"], ["模块响应", "责任边界"], ["测试用例", "实际输出"], ["答辩结论", "保留限制"]]
        for i, values in enumerate(labels):
            out.append(node(20 + i * 180, 85, 145, values, 100))
            if i < 4:
                out.append(line(172 + i * 180, 135, 193 + i * 180, 135, color=BLUE, arrow=True))
        out += [node(40, 245, 390, ["R-01：分区电量估算", "手算 ↔ 计算模块 ↔ T01"], 100), node(470, 245, 390, ["R-02：保护条件优先", "保护状态 ↔ 审查模块 ↔ T02"], 100), text(450, 410, "实线：已有教学契约；虚线：仍待取得的依据", 22), line(160, 450, 350, 450, color=BLUE, dash="8 7", arrow=True), text(590, 458, "现场需求是否认可？尚待确认", 22)]
        return 500, "".join(out)
    if number == 2:
        out = [text(450, 36, "活动不同，照明责任也可能不同", 24, weight="bold"), text(450, 74, "以下是待核验关系，不是校园空间实测图", 22)]
        columns = [(150, "活动"), (385, "可能涉及空间"), (650, "需要确认的条件")]
        for x, label in columns:
            out.append(text(x, 123, label, 22, weight="bold"))
        values = [("阅读、讨论", "座位区、讨论区", "使用者任务与时间？"), ("通行", "通道、入口", "通行与安全职责？"), ("清洁、巡查", "作业区域", "作业计划与责任人？"), ("应急活动", "应急照明相关区域", "设施与保护范围？")]
        for i, row in enumerate(values):
            y = 165 + i * 100
            out += [node(35, y, 220, [row[0]], 70), node(285, y, 245, [row[1]], 70), node(570, y, 295, [row[2]], 70), line(260, y + 35, 280, y + 35, color=BLUE, dash="6 5", arrow=True), line(535, y + 35, 564, y + 35, color=BLUE, dash="6 5", arrow=True)]
        out.append(text(450, 607, "空座位只是一个观察，不能独自推出“可以关灯”", 22))
        return 640, "".join(out)
    if number == 3:
        out = [node(35, 40, 255, ["输入记录", "字段、单位、期间", "来源标记"], 130), node(325, 40, 250, ["校验与公式", "缺失不补猜测值", "单位先统一"], 130), node(610, 40, 255, ["教学估算", "仅在设定条件下", "保留输入版本"], 130)]
        out += [line(295, 105, 320, 105, color=BLUE, arrow=True), line(580, 105, 605, 105, color=BLUE, arrow=True), node(40, 235, 820, ["A区教学输入：48盏 × 18 W/盏；12与10.5 h/天；30天", "教学单价0.62元/kWh；这些数值不代表真实校园"], 100), node(40, 400, 820, ["待确认：灯具实测、运行条件、保护范围、实际费率", "正确复算 ≠ 已经测得现实节能效果"], 100), line(162, 229, 162, 185, color=BLUE, arrow=True), line(80, 366, 820, 366, color=BLUE, dash="8 7")]
        return 535, "".join(out)
    if number == 4:
        out = [text(450, 35, "A区：教学输入与独立手算", 24, weight="bold"), node(40, 70, 820, ["48盏 × 18 W/盏 ＝ 864 W ＝ 0.864 kW", "电量 ＝ 功率(kW) × 每天小时(h/天) × 天数(天)"], 100)]
        scale, start = 1.55, 255
        for y, label, value, hatch in [(245, "基线：12 h/天", 311.04, False), (335, "候选：10.5 h/天", 272.16, True)]:
            out += [text(145, y + 22, label, 22), box(start, y, value * scale, 38, fill="url(#teaching)" if hatch else PALE, stroke=BLUE, radius=0), text(start + value * scale + 70, y + 27, f"{value:.2f} kWh", 22)]
        out += [line(start, 400, start + 350 * scale, 400, color=GRAY)]
        for value in [0, 100, 200, 300]:
            x = start + value * scale
            out += [line(x, 400, x, 410), text(x, 440, str(value), 22)]
        out += [text(805, 440, "kWh", 22), text(450, 500, "30天差值：311.04 − 272.16 ＝ 38.88 kWh", 22), text(450, 546, "模拟金额：38.88 × 0.62 ＝ 24.1056元 → 24.11元", 22), text(450, 591, "价格为教学设定；柱长从0开始，不表示实测节能", 22)]
        return 625, "".join(out)
    if number == 5:
        out = [node(35, 30, 240, ["本地JSON输入", "无网络或设备接口"]), node(330, 30, 240, ["字段与数值检查", "完整且范围有效"]), node(625, 30, 240, ["保护状态检查", "明确不含保护对象"])]
        out += [line(280, 73, 322, 73, color=BLUE, arrow=True), line(575, 73, 617, 73, color=BLUE, arrow=True), node(330, 220, 240, ["情景估算", "保留增加/减少方向"]), node(625, 220, 240, ["人工复核", "解释条件和限制"]), path("M745 126 V176 H450 V210", color=BLUE, arrow=True), line(575, 263, 617, 263, color=BLUE, arrow=True), node(35, 415, 830, ["缺失、冲突、保护或未知 → 暂停该分区并列出待确认项", "输出是信息与教学估算；流程没有设备控制出口"], 110), path("M450 126 V165 H120 V405", color=BLUE, dash="8 7", arrow=True), path("M865 74 H890 V365 H820 V405", color=BLUE, dash="8 7", arrow=True)]
        return 560, "".join(out)
    if number == 6:
        values = [["触发输入", "保留版本"], ["预期与实际", "定位差异"], ["追踪根因", "修订规则"], ["回归检查", "记录证据"]]
        out = [text(450, 35, "观察到的失败，才能成为修订的依据", 24, weight="bold")]
        for i, label in enumerate(values):
            out.append(node(30 + i * 220, 90, 180, label, 100))
            if i < 3:
                out.append(line(216 + i * 220, 140, 242 + i * 220, 140, color=BLUE, arrow=True))
        out += [path("M780 200 V260 H120 V200", color=BLUE, arrow=True), node(40, 315, 820, ["例1：D区保护对象 → 不产生可调整差值", "例2：候选小时增加 → 不得贴上“节能”标签", "修订后重跑原失败用例、正常用例和相邻条件"], 140), text(450, 511, "一次通过只覆盖已运行的条件，不构成普遍可靠性证明", 22)]
        return 545, "".join(out)
    if number == 7:
        out = [text(450, 35, "四项规定成果与反馈点", 24, weight="bold"), line(85, 125, 810, 125, color=BLUE, arrow=True)]
        values = [["需求分析报告", "需求与来源", "第一次检查"], ["技术方案设计书", "接口与可行性", "方案评审"], ["原型演示/模拟", "测试与版本", "中期评审"], ["最终答辩", "证据与限制", "展示与复盘"]]
        for i, label in enumerate(values):
            x = 25 + i * 225
            out += [f'<circle cx="{x+95}" cy="125" r="12" fill="{WHITE}" stroke="{BLUE}" stroke-width="2"/>', node(x, 175, 195, label, 140)]
        out += [path("M790 330 V390 H340 V330", color=BLUE, arrow=True), path("M565 345 V445 H115 V330", color=BLUE, arrow=True), text(450, 503, "反馈改变前提时，回写需求、方案、测试和说明", 22), text(450, 546, "里程碑来自教材提纲；反馈路径为本章教学组织", 22)]
        return 580, "".join(out)
    out = [text(450, 35, "能力表现必须落到实际工件", 24, weight="bold")]
    headers = ["阶段", "计算思维", "批判判断", "跨界协作", "反思问题"]
    xpos = [90, 275, 460, 645, 825]
    for x, label in zip(xpos, headers):
        out.append(text(x, 95, label, 22, weight="bold"))
    rows = [["需求报告", "分解任务", "核验来源", "确认职责", "漏掉谁？"], ["技术方案", "表示接口", "检查假设", "协调约束", "为何这样？"], ["原型测试", "检查规则", "寻找反例", "解释失败", "改了什么？"], ["最终答辩", "说明结构", "限定结论", "共同说明", "如何迁移？"]]
    for i, row in enumerate(rows):
        y = 155 + i * 95
        out.append(box(20, y - 32, 860, 76, fill=PALE if i % 2 == 0 else WHITE, stroke=GRAY, radius=0))
        for x, value in zip(xpos, row):
            out.append(text(x, y + 9, value, 22))
    out += [text(450, 555, "表中列出可观察的操作，不是学习效果评分", 22), text(450, 600, "同一能力在多个阶段反复出现，需用工件举证", 22)]
    return 635, "".join(out)


def export(chapter, number, item, height, drawing):
    here = ROOT / f"materials/ch0{chapter}"
    out = ROOT / f"assets/figures/ch0{chapter}"
    out.mkdir(parents=True, exist_ok=True)
    stem = f"fig{chapter}-{number}"
    description = item.get("alt_text", item.get("teaching_content", item.get("description", item["caption"])))
    if isinstance(description, list):
        description = "；".join(description)
    svg = p.svg_doc(height, item["caption"], description, drawing)
    svg_path, png = out / (stem + ".svg"), out / (stem + ".png")
    svg_path.write_text(svg)
    minimum = p.validate_svg(svg, svg_path)
    raster = p.render_svg(svg_path, png.resolve(), height)
    result = {**item, "file": str(png.relative_to(ROOT)), "editable_source": str(svg_path.relative_to(ROOT)), "grayscale_png": str(raster["grayscale_png"].relative_to(ROOT)), "description": description, "status": "ready", "sha256": raster["sha256"], "svg_sha256": hashlib.sha256(svg_path.read_bytes()).hexdigest(), "gray_sha256": raster["gray_sha256"], "width_px": raster["dimensions_px"]["width_px"], "height_px": raster["dimensions_px"]["height_px"], "insert_mm": 155, "ppi_at_insert": 2400 / (155 / 25.4), "min_font_pt_at_insert": minimum * 155 * 72 / 25.4 / 900, "min_line_pt_at_insert": 2 * 155 * 72 / 25.4 / 900}
    result["plan_id"] = item["id"]
    result["id"] = f"图{chapter}-{number}"
    if chapter == 5 and number == 4:
        result["data"] = {"source_domain": "在线服务教学结构", "target_domain": "维修预约教学模拟", "relation_pairs": 4}
        result["adaptation"] = "采用正文首个类比案例绘制；不表示实测迁移成功。"
    return result


def main(chapter):
    here = ROOT / f"materials/ch0{chapter}"
    plan = json.loads((here / "author-figures.json").read_text())
    figures = plan["figures"] if isinstance(plan, dict) else plan
    result = []
    for number, item in enumerate(figures, 1):
        drawing_function = {4: chapter4, 5: chapter5, 6: chapter6}.get(chapter)
        if drawing_function is None:
            raise ValueError("Chapter-specific evidence drawing must be implemented before export")
        height, drawing = drawing_function(number, item)
        result.append(export(chapter, number, item, height, drawing))
    (here / "figure-manifest.json").write_text(json.dumps({"chapter": chapter, "style": "textbook-style-v1.0", "figures": result}, ensure_ascii=False, indent=2))
    print(json.dumps({"chapter": chapter, "figures": len(result)}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--chapter", type=int, required=True)
    main(parser.parse_args().chapter)
