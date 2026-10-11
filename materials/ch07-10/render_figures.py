"""Editable teaching diagrams; reuse the verified print-size SVG exporter."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("figure_primitives", ROOT / "materials/ch03-layout/render_figures.py")
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)


def card(x, y, width, title, lines, height=110, dashed=False):
    return (p.box(x, y, width, height, fill=p.WHITE, stroke=p.BLUE,
                  dash="7 6" if dashed else None)
            + p.text(x + width / 2, y + 34, title, 24, weight="bold", fill=p.BLUE)
            + p.text_lines(x + width / 2, y + 66, lines, 22, step=28))


def horizontal(labels, details, *, feedback=None, context=None, feedback_index=0):
    count = len(labels)
    width = 150 if count == 5 else 194
    gap = 20 if count == 5 else 28
    start = (900 - count * width - (count - 1) * gap) / 2
    y = 120 if context else 40
    body = []
    if context:
        body += [p.box(30, 15, 840, 58, fill=p.PALE, stroke=p.GRAY),
                 p.text(450, 51, context, 23, weight="bold")]
    for i, (label, detail) in enumerate(zip(labels, details)):
        x = start + i * (width + gap)
        body.append(card(x, y, width, label, detail, 110))
        if i < count - 1:
            body.append(p.line(x + width + 3, y + 55, x + width + gap - 4,
                               y + 55, color=p.BLUE, arrow=True))
        if context:
            body.append(p.line(x + width / 2, 78, x + width / 2, y - 7,
                               color=p.GRAY, dash="5 5", arrow=True))
    height = y + 160
    if feedback:
        left = start + feedback_index * (width + gap) + width / 2
        right = start + (count - 1) * (width + gap) + width / 2
        body += [p.path(f"M{right} {y + 118} V{y + 145} H{left} V{y + 118}",
                        color=p.BLUE, arrow=True),
                 p.text(450, y + 182, feedback, 22, weight="bold")]
        height = y + 210
    return height, "".join(body)


def seven_one():
    return horizontal(["事件", "解释", "目标", "行动", "新证据"],
                      [["当前结果"], ["暂定理解"], ["具体任务"], ["练习与求助"], ["检查表现"]],
                      feedback="行动结果返回解释；能力判断可以随证据调整。",
                      context="课程资源、任务难度与评价环境影响各环节", feedback_index=1)


def seven_two():
    labels = ["参加特定练习", "观察到脑影像变化", "技能表现发生变化",
              "迁移到另一任务", "某种教育干预普遍有效"]
    questions = ["练习对象与条件是什么？", "观察方法能说明什么？", "表现怎样测量与比较？",
                 "新任务与原任务有何不同？", "人群、环境与重复证据是否支持？"]
    body = [p.text(450, 34, "五个不同问题，每个结论都须有自己的证据", 24, weight="bold")]
    for i, (label, question) in enumerate(zip(labels, questions)):
        y = 65 + i * 100
        body += [p.box(35, y, 575, 75, stroke=p.BLUE),
                 p.text(55, y + 30, f"{i + 1}  {label}", 23, anchor="start", weight="bold"),
                 p.text(55, y + 60, question, 22, anchor="start")]
        if i < 4:
            body += [p.line(322, y + 79, 322, y + 85, color=p.GRAY),
                     p.line(322, y + 93, 322, y + 98, color=p.GRAY),
                     p.text(650, y + 92, "另需独立证据", 22, anchor="start")]
    body.append(p.text(450, 583, "前一层得到支持，不自动证明后一层。", 23, weight="bold"))
    return 615, "".join(body)


def seven_three():
    return horizontal(["事件", "反应", "事实与解释", "行动", "新证据"],
                      [["反馈与挑战"], ["识别情绪"], ["分开记录"], ["调整或求助"], ["再查效果"]],
                      feedback="没有改善时，返回检查问题、策略与支持条件。",
                      context="情绪与资源条件参与判断；坚持原计划只是一个选项")


def seven_four():
    body = [card(300, 20, 300, "同伴展示的结果", ["先追问过程与条件"], 90)]
    labels = [(20, "先备与资源", ["已有知识", "时间与支持"]),
              (310, "行动与反馈", ["做了什么", "怎样检查"]),
              (600, "我的当前任务", ["相似条件", "关键差异"])]
    for x, label, lines in labels:
        body += [p.line(450, 115, x + 140, 157, arrow=True),
                 card(x, 165, 280, label, lines, 115)]
    body += [p.path("M160 287 V322 H740 V287", color=p.BLUE),
             p.line(450, 287, 450, 355, color=p.BLUE)]
    for x, label, lines in [(20, "直接借用", ["关键条件一致"]),
                            (310, "修改后试用", ["有差异可调整"]),
                            (600, "暂不适用", ["必要条件缺失"])]:
        body += [card(x, 380, 280, label, lines, 90, dashed=label == "暂不适用")]
    body += [p.path("M450 355 H160 V375", arrow=True),
             p.line(450, 355, 450, 375, arrow=True),
             p.path("M450 355 H740 V375", arrow=True),
             p.text(450, 515, "迁移的是可检查的方法，不能复制他人的成功保证。", 22, weight="bold")]
    return 545, "".join(body)


def seven_five():
    body = [p.text(450, 32, "2005年公开讲稿对过往经历的回顾", 24, weight="bold"),
            p.line(105, 140, 795, 140, color=p.BLUE, arrow=True)]
    for x, time, lines in [(110, "三十岁时", ["离开苹果"]),
                           (335, "其后", ["创办NeXT", "参与创办Pixar"]),
                           (560, "多年后", ["苹果收购NeXT", "回到苹果"]),
                           (785, "2005年", ["公开回顾经历"])]:
        body += [p.text(x, 99, time, 23, weight="bold"),
                 p.box(x - 6, 134, 12, 12, fill=p.BLUE, stroke=p.BLUE, radius=6),
                 p.text_lines(x, 192, lines, 22, step=30)]
    body += [card(25, 280, 410, "叙述的经历", ["说明他怎样讲述事件", "仍有其他历史材料可核对"], 125),
             card(465, 280, 410, "当事人的回望解释", ["他赋予经历的意义", "不构成他人结果的预测"], 125, dashed=True),
             p.text(450, 453, "公开叙述的顺序不证明挫折必然导致成功。", 22, weight="bold")]
    return 485, "".join(body)


def seven_six():
    body = [card(25, 25, 410, "群体中的差异", ["比较不同的人", "同一时期的评分", "问：哪些变量与差异有关？"], 160),
            card(465, 25, 410, "个人随时间的变化", ["追踪同一个人", "多个时期的评分", "问：变化怎样发生与维持？"], 160)]
    for x, labels in [(65, ["甲", "乙", "丙"]), (505, ["时点一", "时点二", "时点三"])]:
        for i, label in enumerate(labels):
            cx = x + i * 125
            body += [p.box(cx, 220, 100, 60, fill=p.PALE, stroke=p.GRAY),
                     p.text(cx + 50, 258, label, 22, weight="bold")]
        if x == 505:
            body += [p.line(608, 250, 627, 250, arrow=True),
                     p.line(733, 250, 752, 250, arrow=True)]
    body += [p.line(260, 335, 640, 335, color=p.GRAY, dash="7 7"),
             p.line(437, 322, 463, 348, color=p.INK, width=3),
             p.line(437, 348, 463, 322, color=p.INK, width=3),
             p.text(450, 389, "群体方差比例不能直接变成个人的幸福配方。", 23, weight="bold"),
             p.text(450, 427, "结构示意，不包含实际评分或研究数据。", 22)]
    return 460, "".join(body)


def eight_one():
    return horizontal(["外部信号", "具体任务", "能力差距", "学习行动", "表现检查"],
                      [["预期或采用"], ["工作怎样变"], ["当前做不到"], ["练习与资源"], ["独立完成"]],
                      feedback="证据缺失时先核实；检查结果可以修订学习目标。",
                      context="调查预期、组织采用与个人任务属于不同层次", feedback_index=2)


def eight_two():
    body = [p.text(450, 33, "示例安排：日期只表示教学顺序，不是最佳间隔", 23, weight="bold"),
            p.line(105, 115, 795, 115, color=p.BLUE, arrow=True)]
    for x, day, title, lines in [(110, "第1天", "理解", ["读材料与示例", "写出关键关系"]),
                                (335, "第3天", "提取", ["关闭资料作答", "暴露遗漏与错误"]),
                                (560, "第7天", "核对与修正", ["回看材料", "改解释与练习"]),
                                (785, "第14天", "变化任务应用", ["换输入或情境", "检查能否迁移"])]:
        body += [p.text(x, 83, day, 23, weight="bold"),
                 p.box(x - 6, 109, 12, 12, fill=p.BLUE, stroke=p.BLUE, radius=6),
                 card(x - 105, 150, 210, title, lines, 115)]
    body += [p.path("M785 275 V313 H335 V275", color=p.BLUE, arrow=True),
             p.text(450, 354, "根据错误类型改活动；无需只增加同一种重读。", 22, weight="bold")]
    return 390, "".join(body)


def eight_three():
    return horizontal(["问题与版本", "来源选择", "主张定位", "条件核验", "保存记录"],
                      [["明确要查什么"], ["找到原始材料"], ["指出支持位置"], ["比较适用条件"], ["可复查结论"]],
                      feedback="关键材料不足：补查，或保留“待验证”状态。",
                      context="可复查的结论需要问题、出处、条件与当前证据")


def eight_four():
    nodes = [(320, 20, "目标记录", ["计划与检查点"]),
             (25, 155, "来源材料", ["文档、论文与课程"]),
             (615, 155, "提取练习", ["问题、作答与修正"]),
             (120, 340, "作品", ["代码、解释与结果"]),
             (520, 340, "反馈", ["差距与下一次调整"])]
    body = []
    for x, y, _, _ in nodes:
        body.append(p.line(450, 250, x + 130, y + 48, color=p.GRAY))
    for x, y, title, lines in nodes:
        body.append(card(x, y, 260, title, lines, 95))
    body += [p.box(320, 195, 260, 105, fill=p.PALE, stroke=p.BLUE),
             p.text_lines(450, 238, ["要完成的任务", "及其表现证据"], 24, weight="bold", step=34),
             p.text(450, 490, "应用、纸笔与本地文件都可承载这些关系。", 23, weight="bold"),
             p.text(450, 526, "连接可追踪材料，不以安装工具数量评价学习。", 22)]
    return 560, "".join(body)


def eight_five():
    body = [card(15, 190, 220, "具体学习问题", ["任务与当前困难"], 95),
            card(645, 190, 240, "个人判断", ["核验、整理与贡献"], 95)]
    for y, title, lines in [(15, "来源", ["原始说明与研究"]),
                            (145, "同伴", ["复述与互查"]),
                            (275, "社区", ["有边界的提问"]),
                            (405, "实践反馈", ["实际任务的结果"])]:
        body += [p.line(235, 237, 318, y + 45, color=p.GRAY),
                 p.line(582, y + 45, 645, 237, color=p.GRAY),
                 card(325, y, 250, title, lines, 90)]
    body += [p.path("M765 290 V535 H125 V290", color=p.BLUE, arrow=True),
             p.text(450, 578, "提问与贡献形成往返；多个节点可能引用同一来源。", 22, weight="bold")]
    return 615, "".join(body)


def eight_six():
    items = [(25, 35, "动机与起点", ["兴趣和当前表现"]),
             (345, 35, "可检查的目标", ["任务、条件与标准"]),
             (665, 35, "资源与时间", ["材料、先备与预算"]),
             (665, 245, "练习", ["执行具体学习活动"]),
             (345, 245, "证据与检查点", ["比较实际表现"]),
             (25, 245, "调整与理由", ["修改一个关键条件"])]
    body = [card(x, y, 210, title, lines, 105) for x, y, title, lines in items]
    body += [p.line(240, 87, 340, 87, arrow=True), p.line(560, 87, 660, 87, arrow=True),
             p.line(770, 145, 770, 240, arrow=True), p.line(660, 297, 560, 297, arrow=True),
             p.line(340, 297, 240, 297, arrow=True),
             p.path("M130 240 V190 H450 V145", dash="7 6", arrow=True),
             p.path("M450 190 H690 V145", dash="7 6", arrow=True),
             p.text(450, 404, "改目标、先备、练习或时间，并保留调整依据。", 22, weight="bold"),
             p.text(450, 442, "流程关系示意，不是实证效果模型。", 22)]
    return 480, "".join(body)


def nine_one():
    body = [card(25, 40, 260, "读者与任务", ["谁要做什么", "当前困难是什么"], 115),
            card(320, 40, 260, "交付物", ["可使用的内容与系统", "范围与状态清楚"], 115),
            card(615, 40, 260, "验收证据", ["读者能否完成任务", "来源与行为能否复查"], 115),
            p.line(290, 98, 315, 98, color=p.BLUE, arrow=True),
            p.line(585, 98, 610, 98, color=p.BLUE, arrow=True),
            p.box(170, 225, 560, 105, fill=p.PALE, stroke=p.GRAY, dash="7 6"),
            p.text(450, 265, "边界与未知", 24, weight="bold"),
            p.text(450, 303, "未确认要求保留为待决项，不伪装成共同决定", 22)]
    for x in [155, 450, 745]:
        body.append(p.line(x, 160, 450, 219, color=p.GRAY, dash="6 6"))
    body.append(p.text(450, 380, "每条箭头都要说明前一步如何支持后一步。", 22, weight="bold"))
    return 415, "".join(body)


def nine_two():
    body = [card(320, 20, 260, "确认目标", ["范围与验收条件"], 90),
            card(70, 160, 320, "内容核对", ["来源、状态与读者任务"], 95),
            card(510, 160, 320, "字段结构准备", ["表示、输入与接口"], 95),
            card(320, 320, 260, "页面整合", ["两项输出均已齐备"], 90),
            card(320, 465, 260, "评审", ["检查行为与内容"], 90)]
    body += [p.path("M450 115 V132 H230 V155", color=p.BLUE, arrow=True),
             p.path("M450 132 H670 V155", color=p.BLUE, arrow=True),
             p.path("M230 260 V293 H450 V315", color=p.BLUE, arrow=True),
             p.path("M670 260 V293 H450", color=p.BLUE),
             p.line(450, 415, 450, 460, color=p.BLUE, arrow=True),
             p.path("M315 510 H25 V205 H65", color=p.GRAY, dash="7 6", arrow=True),
             p.path("M585 510 H875 V205 H835", color=p.GRAY, dash="7 6", arrow=True),
             p.text(450, 605, "实线：输出依赖；虚线：评审后可能返回检查。", 22, weight="bold")]
    return 640, "".join(body)


def nine_three():
    items = [(40, 35, "描述情境", ["限定当前对象"]),
             (345, 35, "给出证据", ["可复查的观察"]),
             (650, 35, "提出问题", ["请求核实或改进"]),
             (650, 240, "复述确认", ["分清理解与认同"]),
             (345, 240, "决定回应", ["责任、动作与期限"]),
             (40, 240, "检查后续", ["复查实际变化"])]
    body = [card(x, y, 210, title, lines, 100) for x, y, title, lines in items]
    body += [p.line(255, 85, 340, 85, arrow=True), p.line(560, 85, 645, 85, arrow=True),
             p.line(755, 140, 755, 235, arrow=True), p.line(645, 290, 560, 290, arrow=True),
             p.line(340, 290, 255, 290, arrow=True), p.line(145, 235, 145, 140, arrow=True),
             p.text(450, 184, "证据不足时，先补查", 23, weight="bold"),
             p.text(450, 389, "反馈指向任务与条件；未经证实的归因不能替代观察。", 22)]
    return 425, "".join(body)


def nine_four():
    body = [card(30, 25, 280, "候选方案", ["明确目标与范围"], 90),
            card(30, 155, 280, "硬约束检查", ["权限、安全与期限", "已满足还是仍未知？"], 115),
            card(525, 155, 340, "暂停候选", ["未满足或关键条件未知", "补证据、调整或退出"], 115, dashed=True),
            card(30, 320, 280, "比较偏好与证据", ["收益、成本与不确定性"], 90),
            card(525, 320, 340, "记录决定", ["决定者、理由与复核条件"], 90),
            p.line(170, 120, 170, 150, arrow=True),
            p.line(315, 210, 520, 210, arrow=True),
            p.text(415, 192, "未满足 / 未知", 22),
            p.line(170, 275, 170, 315, arrow=True),
            p.text(270, 301, "满足", 22),
            p.line(315, 365, 520, 365, arrow=True),
            p.path("M695 415 V458 H15 V210 H25", dash="7 6", arrow=True),
            p.text(450, 501, "新条件触发复核时，返回硬约束检查。", 22, weight="bold")]
    return 535, "".join(body)


def nine_five():
    body = [p.text(225, 35, "支持他人", 25, weight="bold"),
            p.text(675, 35, "共同复盘", 25, weight="bold"),
            card(60, 70, 330, "识别阻碍", ["先备、资源与协作条件"], 90),
            card(60, 215, 330, "支持行动", ["解释、配对与调整任务"], 90),
            card(510, 70, 330, "任务证据", ["观察支持后的实际表现"], 90),
            card(510, 215, 330, "流程调整", ["明确下一次怎样验证"], 90),
            p.line(225, 165, 225, 210, arrow=True),
            p.path("M395 260 H450 V115 H505", arrow=True),
            p.line(675, 165, 675, 210, arrow=True),
            p.path("M675 310 V360 H20 V115 H55", arrow=True),
            p.text(450, 410, "新的共同任务检验调整，结果再成为支持与复盘的依据。", 22, weight="bold")]
    return 450, "".join(body)


def ten_one():
    return horizontal(["共同方向", "专业贡献", "授权与资源", "决定或暂缓"],
                      [["说明愿景", "与结果标准"], ["聆听、澄清", "客观表达"],
                       ["任务和权限", "支持与责任"], ["比较证据", "说明边界"]],
                      feedback="结果与新证据返回目标；需要时也可回到贡献与授权。",
                      context="事实、边界与责任贯穿各环节")


def ten_two():
    labels = ["目标与边界", "工作包与估时", "联合检查条件",
              "责任分配与交接", "实际负担与反馈", "维持或调整"]
    details = [["本轮要达成什么"], ["依赖与工作量"],
               ["技能 / 可用容量", "学习机会 / 风险"],
               ["共同确认接收条件"], ["用时、表现与风险"], ["缩小或重新分配"]]
    locations = [(30, 40), (320, 40), (610, 40),
                 (30, 240), (320, 240), (610, 240)]
    body = [p.text(450, 24, "公平性与容量需要共同检查，熟练程度不是唯一依据。", 22)]
    for (x, y), label, lines in zip(locations, labels, details):
        body.append(card(x, y, 260, label, lines, 115))
    body += [p.line(295, 97, 315, 97, arrow=True),
             p.line(585, 97, 605, 97, arrow=True),
             p.path("M740 162 V194 H160 V233", arrow=True),
             p.line(295, 297, 315, 297, arrow=True),
             p.line(585, 297, 605, 297, arrow=True),
             p.path("M740 362 V400 H12 V97 H25", dash="7 6", arrow=True),
             p.text(450, 440, "反馈返回目标与容量；分配结果仍需实际执行和复核。", 22, weight="bold")]
    return 470, "".join(body)


def ten_three():
    body = [p.text(450, 26, "箭头提示接触或影响关系，需要调查确认。", 23, weight="bold"),
            card(315, 250, 270, "数字展技术方案", ["当前学生原型", "设计、数据与输出"], 115)]
    outer = [(15, 55, "直接使用者", ["怎样接触与使用"]),
             (615, 55, "被描述或分类者", ["是否知情、能否纠正"]),
             (15, 250, "资料或故事提供者", ["提供范围与使用条件"]),
             (615, 250, "团队成员", ["执行、协作与负担"]),
             (15, 445, "课程或组织授权方", ["确认许可与公开范围"]),
             (615, 445, "更广泛的公众", ["间接后果与公共影响"])]
    for x, y, label, lines in outer:
        body.append(card(x, y, 270, label, lines, 90))
    body += [p.line(150, 150, 310, 260, arrow=True),
             p.line(750, 150, 590, 260, arrow=True),
             p.line(290, 295, 310, 295, arrow=True),
             p.line(590, 315, 610, 315, arrow=True),
             p.line(150, 440, 310, 355, arrow=True),
             p.line(590, 355, 750, 440, arrow=True),
             p.box(25, 580, 400, 72, fill=p.PALE, stroke=p.BLUE),
             p.text(225, 610, "团队当前可决定", 23, weight="bold"),
             p.text(225, 640, "获准范围内的设计与记录", 22),
             p.box(475, 580, 400, 72, fill=p.WHITE, stroke=p.GRAY, dash="7 6"),
             p.text(675, 610, "须由授权主体确认", 23, weight="bold"),
             p.text(675, 640, "许可、公开范围与敏感事项", 22)]
    return 690, "".join(body)


def ten_four():
    body = [p.box(25, 20, 850, 420, fill=p.WHITE, stroke=p.BLUE, dash="7 6"),
            p.box(65, 45, 770, 85, fill=p.PALE, stroke=p.BLUE),
            p.text(450, 79, "GOVERN  治理", 25, weight="bold"),
            p.text(450, 112, "责任、规则与问责贯穿全部功能", 23),
            card(60, 175, 240, "MAP  情境", ["使用情境", "与影响对象"], 115),
            card(330, 175, 240, "MEASURE  检查", ["性能与风险", "方法及证据边界"], 115),
            card(600, 175, 240, "MANAGE  应对", ["限制、缓解", "监测或停止"], 115),
            p.line(305, 232, 325, 232, arrow=True),
            p.line(575, 232, 595, 232, arrow=True),
            p.path("M720 297 V345 H180 V297", arrow=True),
            p.text(450, 385, "使用、情境或新证据变化时，返回检查并迭代。", 22, weight="bold"),
            p.text(450, 420, "功能相互联系，可按情境进入与裁剪。", 22),
            p.text(450, 490, "自愿框架；图示不是固定顺序、认证或法律合规证明。", 22, weight="bold")]
    return 525, "".join(body)


BUILDERS = {"7-1": seven_one, "7-2": seven_two, "7-3": seven_three,
            "7-4": seven_four, "7-5": seven_five, "7-6": seven_six,
            "8-1": eight_one, "8-2": eight_two, "8-3": eight_three,
            "8-4": eight_four, "8-5": eight_five, "8-6": eight_six,
            "9-1": nine_one, "9-2": nine_two,
            "9-3": nine_three, "9-4": nine_four, "9-5": nine_five,
            "10-1": ten_one, "10-2": ten_two,
            "10-3": ten_three, "10-4": ten_four}


def source_for(chapter):
    directory = ROOT / f"manuscripts/ch{chapter:02d}"
    whole = directory / f"ch{chapter:02d}.md"
    return whole.read_text() if whole.exists() else "\n".join(path.read_text() for path in sorted(directory.glob("*.md")))


def render(ids):
    grouped = {}
    for figure_id in ids:
        chapter = int(figure_id.split("-")[0])
        source = source_for(chapter)
        caption = re.search(rf"\*\*图{re.escape(figure_id)} (.+?)\*\*", source)
        if not caption:
            raise ValueError(f"Missing author caption: {figure_id}")
        tail = source[caption.end():]
        source_line = re.search(r"^来源：(.+)$", tail, re.M)
        guide = re.search(r"^读图(?:引导)?：(.+)$", tail, re.M)
        if not source_line or not guide:
            raise ValueError(f"Missing source/read guide: {figure_id}")
        description = guide.group(1)
        height, body = BUILDERS[figure_id]()
        svg = p.svg_doc(height, f"图{figure_id} {caption.group(1)}", description, body)
        out = ROOT / f"assets/figures/ch{chapter:02d}"
        out.mkdir(parents=True, exist_ok=True)
        svg_path = out / f"fig{figure_id}.svg"
        png_path = out / f"fig{figure_id}.png"
        svg_path.write_text(svg)
        min_font = p.validate_svg(svg, svg_path)
        rendered = p.render_svg(svg_path, png_path, height)
        record = {"id": f"图{figure_id}", "caption": caption.group(1),
                  "source": "来源：" + source_line.group(1), "description": description,
                  "file": str(png_path.relative_to(ROOT)), "png": str(png_path.relative_to(ROOT)),
                  "editable_source": str(svg_path.relative_to(ROOT)),
                  "grayscale_png": str(rendered["grayscale_png"].relative_to(ROOT)),
                  "sha256": rendered["sha256"], "gray_sha256": rendered["gray_sha256"],
                  "svg_sha256": hashlib.sha256(svg_path.read_bytes()).hexdigest(),
                  "dimensions_px": rendered["dimensions_px"], "insert_width_mm": p.INSERT_MM,
                  "png_ppi_at_insert": p.PPI, "min_font_pt_at_insert": p.MIN_FONT_PT,
                  "min_label_pt_at_insert": p.MIN_FONT_PT, "declared_min_label_px": min_font,
                  "status": "rendered", "gray_semantics": "标签、位置、边框和线型承载含义；颜色为辅助。"}
        grouped.setdefault(chapter, []).append(record)
    for chapter, records in grouped.items():
        here = ROOT / f"materials/ch{chapter:02d}"
        here.mkdir(parents=True, exist_ok=True)
        manifest_path = here / "figure-manifest.json"
        existing = json.loads(manifest_path.read_text())["figures"] if manifest_path.exists() else []
        replaced = {record["id"] for record in records}
        records = [record for record in existing if record["id"] not in replaced] + records
        records.sort(key=lambda record: int(record["id"].split("-")[1]))
        manifest = {"style": "textbook-style-v1.0", "insert_width_mm": p.INSERT_MM,
                    "png_ppi_at_insert": p.PPI, "min_label_pt_at_insert": p.MIN_FONT_PT,
                    "visual_review": {"status": "pending_actual_image_view", "items": []}, "figures": records}
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"rendered": ids, "ppi": p.PPI, "min_font_pt": p.MIN_FONT_PT}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ids", nargs="+", choices=list(BUILDERS), required=True)
    args = parser.parse_args()
    render(args.ids)
