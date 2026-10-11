# Progressive Edition Authoring Brief

## Shared Contracts

以`specs/ch02-progressive.spec.md`和最新版主Skill为准。每节必须导语、首小节案例文字描述与分析、中间概念/理论/方法、最后教学小节分层思维训练、最后反思。保持原提纲五节标题；三级标题自由设计，不套旧节内结构。中文连续教材正文，专业术语首次自然语言解释。基础小示范完整、独立题不同数据，AI候选明确为模拟，不宣称实际API结果。图后期统一由Parent制作，writers不写图片路径/占位图题，可用简短段内文字说明拟表达内容，提交时在final报告图的建议位置。

每节目标5000—5800近似汉字，不包含其章末答案；答案E01—E04各约550—850汉字，可按任务增加。不要用反复“必须检查”“AI不是万能”填充。实质比较：传统方式怎样形成表示/子任务/规则/策略，AI改变哪个环节、需要什么新输入、人的工作如何改变；至少一个有材料的跨界迁移分析，明确各领域知识提供什么。学习习惯是记录假设、补知识缺口、对照证据、改方案等实际操作。

## Data and Exercise Contract

旧数据`materials/ch02/exercise-inputs.json`为只读稳定输入。可读取旧版同章片段核对数据，但不能照搬原高起点展开。各题改成基础、应用、拓展；基础包含可用已示范方法完成的2—3个操作，应用使用原固定数据，拓展承接更复杂边界。每题增加AI模拟候选供学生辨别，所有判断用原材料核验；不要把答案紧跟在训练之后。完整答案单独写对应`answers-eXX.md`。

- E01：H→J2含楼梯、J→L2含楼梯且整条边在10:00前完成、H→K3、K→L4、L→H5；9:57出发，10:05前到L，无障碍要求。基础只选出所需字段/核对一条候选，不要求状态扩展。AI候选“经J更快”是独立审查对象，不在题前揭答案。
- E02：A2，B4依赖A，C3依赖A，D5依赖B/C，E2依赖B，F3依赖D/E，G1依赖F；变体D2/D1；R7/R8版本一致性作拓展。基础从此表识别可同时开始环节和一条依赖，不直接做关键链证明。
- E03：12条观察原JSON，RA=人数≥50，RB=人数≥50或活动=1且人数≥35；前8开发，后4封存测试。基础按给定规则做两三行判断，应用算误报漏报，再深化时间/对象泄漏。联邦学习/注意力解释需题前铺垫；不假设已会统计学习。
- E04：有向图S→A1、S→B4、A→B2、A→C1、A→T9、B→T2、C→T9。基础核对一个已给路线与求和，应用比较候选、已讲过的最短路。负权反例/稳定排序为可选拓展，可舍弃排序以确保AI主线。模拟预测不得覆盖实际边权。
- E05/E06由Parent负责。各题条件不要依赖前题答案，所有原数据标教学模拟。

## Source IDs and Boundaries

引用占位`[[Sxx]]`，Parent统一首次顺序编码；不自编参考序号。原来源S01 Wing、S02 Parnas、S03 scikit-learn common pitfalls、S04 cross-validation、S05 Dijkstra、S06 MIT6.006、S07 Python Sorting、S08 NIST AI RMF、S09 RFC9110、S10 Amershi人机交互。只在实际支撑论断时引用，不凑齐来源。

新增：S11 LeCun/Bengio/Hinton Deep learning（CNN学习表示）；S12 Vaswani Attention Is All You Need（attention/Transformer）；S13 Selvaraju Grad-CAM（梯度相关粗定位，不能证明因果/临床正确）；S14 McMahan Federated Learning（本地训练/共享更新）；S15 Zhu Deep Leakage from Gradients（数据不集中不等于更新无泄露）；S16 Vezhnevets FeUdal Networks（高层目标与低层动作的具体架构，不能泛化所有AI动态分解）；S17 Mnih Human-level control（从环境奖励学习策略，论文游戏任务不支持无人机/校园效果）；S18 Finn Model-Agnostic Meta-Learning（跨任务学可快速适应的初始化，不是机器万能自动选优化器）。Parent保存实际原文与支持位置；原提纲里的技术陈述需纠偏并解释。

## Writer Authority

只写被指派的新fragment文件。你不是唯一writer，保留其他人的修改。不得写共享规则、Spec/Plan、来源/输入/合并稿、图、报告、Word/PDF、harness、目的记录；不得stage/commit、创建worktree、调用外部CLI/provider、嵌套委派或改变目标。遇到规则冲突停止报告。最多60分钟初稿，补改最多两次；自检题干与答案、约束、标题和近似汉字。Parent拥有整合、来源核验、裁决及验收。
