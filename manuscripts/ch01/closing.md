## 综合训练 E05：社区数字服务咨询预约

一家虚构社区服务点准备提供数字服务咨询。四个预约各需一个完整时段、一个能满足所需条件的工作人员。请把设备借用与场地分配的共同结构迁移到这一情境，重点检查资格例外。全部数据为教学示例；这里的资格是题目给定的能力条件，不能作为真实认证或服务授权。

三个时段S1、S2、S3顺序为1、2、3；不允许把一个时段拆成两次服务。每名工作人员每时段只能服务一个请求，每个请求参与人数为1，持续时段数为1。

表1-31 E05工作人员与资格

| 工作人员 | 可用时段 | 给定资格 | 每时段容量 |
| --- | --- | --- | ---: |
| V1 | S1、S2、S3 | general：一般数字操作咨询 | 1个请求 |
| V2 | S2、S3 | general；screen_reader：可提供屏幕阅读器操作帮助 | 1个请求 |

表1-32 E05咨询请求

| 请求 | 允许时段 | 所需资格 |
| --- | --- | --- |
| P1 | S1 | general |
| P2 | S1、S2 | general |
| P3 | S2、S3 | screen_reader |
| P4 | S2、S3 | general |

目标是为全部请求形成可检查的安排。硬约束包括恰好一次、双方时段允许、资格满足、同一工作人员同时段不能重复占用，以及容量与时长要求。较早完成可以作为偏好，但必须说明比较口径；请求编号不能自行变成价值优先级。

![图1-7 综合任务的目标、约束与检验](../../assets/figures/ch01/fig1-7.png)

来源：本书原创教学图，依据E05模拟数据与本章问题表示、迁移和检验框架绘制。

图1-7连接目标、资格数据、候选、检验与条件变化。读图时找到P3对应的资格检查，再沿虚线指出条件变化后应回到哪里；最后说明图中的检查还不能回答哪一个现实问题。

**任务与交付。**建议用时六十分钟。提交一页问题说明、三列安排表（请求、工作人员、时段）、逐项检验表和一段迁移反思。先列目标、输入、约束、偏好与输出；再对照E01或E03标出可继承的规则和必须新建的资格条件。给出至少一条失败候选并解释失败，随后形成合格安排。最后撤除V2的screen_reader资格，保留general，重新判断可行性；若提出协商方案，单独列明改动与待确认事项。

你可以手工列允许位置、使用表格筛选或写有限枚举程序。使用AI时，输入限于本题模拟数据和明确规则，要求输出候选及理由；再由你核对全部硬约束、纠正错误并保存变化记录。没有AI的作业按相同标准评价。

**参考指引。**一组可行安排为P1—V1—S1、P2—V1—S2、P3—V2—S2、P4—V1—S3。四个请求各一次，时段双方允许；P3由具备screen_reader的V2服务，其余所需general都满足；每工作人员—时段位置唯一，每次服务1个请求。本题原条件有限枚举得到6条可行安排，参考表只展示其中一条。

撤除V2的screen_reader后，P3没有任何合格工作人员，因此原硬约束下无解。给P3安排V1，或把P3的需求改成general，都会违反当前条件。请求增援或确认替代服务可以成为新任务的协商提案，不能算原题已经解决。

模型内可行还没有证明服务满意、公平或现实可达。你可以提出先了解用户完成任务所需帮助、实际服务时长和超时情况的调查路径，也可以先比较流程是否让一部分用户难以预约；两条路径都须指出新增证据及其用途。不要收集本练习不需要的真实个人信息。不同建议只要有清楚依据，就不必收敛成同一个价值立场。

## 评价与反馈

E01—E05都使用同一四级量规，各维度独立评分并注明作品证据。0表示缺失或关键错误；1表示有尝试但漏掉关键条件或证据；2表示满足当前任务并解释依据；3表示满足要求，并能处理有意义的例外、说明适用边界。分数用于定位改进方向，不能只看总分掩盖一项硬约束错误。

表1-33 E01—E05成果评价

| 任务 | 评价维度 | 达到要求的主要证据 |
| --- | --- | --- |
| E01 | 条件、表示、约束、结论状态、修正 | 合格安排及D2关闭后的无解依据 |
| E02 | 追溯、贡献、解释边界、因果谨慎 | 三份原文定位与思想比较表 |
| E03 | 结构对应、新条件、例外、调整依据 | 容量与设施检查，容量变化分析 |
| E04 | 问题与视角、证据、代价、结论强度 | 多视角建议，明确模拟资料缺口 |
| E05 | 问题说明、表示、执行、检验、迁移边界 | 完整过程与资格变化后的判断 |

评价不按工具数量、语言流畅度或立场一致性进行。若一个安排存在重复占用，即使说明很流畅，“满足全部硬约束”这一维度仍有关键错误；若开放题选择了不同候选，但说明了证据缺口与核验路径，仍可达到要求。互评时先指出作品中的具体位置，再说明相应条件和可执行的修改建议。

## 本章回顾与反思

计算思维把现实任务中的重要对象、关系和规则组织为可以处理与检查的表示。程序是执行方式之一，工具是参与者之一。判断过程是否可靠，需要检查目标、数据和规则是否合适，并把候选结果对照明确标准。无解、信息不足和搜索尚未成功，需要不同证据与不同回应。

本章的历史阅读让我们区分计算理论、教育设计与通用能力倡议；迁移练习让我们发现共同结构并处理新条件；照明情境提醒我们，模型内正确与现实有效需要不同证据。多个视角可以共同作用，也可以要求重新定义问题。

请回看最初的一条失败候选，说明它如何改变了你的表示或步骤。再选一个未被模型纳入的条件，解释为何暂时排除、若它变化会影响什么，以及下次应该向谁取得什么信息。能够提出有限而准确的结论，是继续深入学习的起点。

## 术语表

表1-34 本章术语

| 术语 | 本章使用的含义 |
| --- | --- |
| 计算思维 | 本章工作性定义：围绕目标组织表示、规则、可执行或推演的步骤，并检查、修正与说明方案 |
| 问题表示 | 为当前目标选择对象、关系和状态的表达方式 |
| 抽象 | 保留相关信息，明确被略去的信息与代价 |
| 分解 | 拆开子问题，同时保留依赖与整体检查 |
| 模式识别 | 提出共同结构或规则，并保留例外 |
| 算法 | 有明确输入、操作、判断和输出，且能在给定任务中终止的处理步骤 |
| 评估 | 对照目标与标准检查候选，并说明结论的适用范围 |
| 自动化 | 让程序或工具重复执行已明确的操作 |
| 泛化 | 提出规则的适用范围，并用新条件和例外检查它 |
| 硬约束／偏好 | 前者决定方案资格，后者比较合格候选 |
| 可行／无解 | 前者满足当前硬约束；后者有证据说明不存在满足者 |
| 迁移 | 对应结构、重建新条件并检验适用范围 |
| 模型边界 | 当前表示、假设和结论覆盖的范围 |
| 实证检验 | 用适当观察与比较检查现实主张 |

## 参考文献

引用暂用编号体例；正文及图中的编号对应下列原文。在线资料查阅日期为2026年10月11日。

[1] Wing, J. M. Computational Thinking. *Communications of the ACM*, 2006, 49(3):33–35. DOI: [10.1145/1118178.1118215](https://doi.org/10.1145/1118178.1118215)。[原文](https://www.cs.cmu.edu/~15110-s13/Wing06-ct.pdf)。

[2] Wing, J. M. *Computational Thinking: What and Why?* 17 November 2010. [作者稿](https://www.cs.cmu.edu/~CompThink/resources/TheLinkWing.pdf)，第1页定义归属说明。

[3] Turing, A. M. On Computable Numbers, with an Application to the Entscheidungsproblem. *Proceedings of the London Mathematical Society*, 1937, s2-42(1):230–265. DOI: [10.1112/plms/s2-42.1.230](https://doi.org/10.1112/plms/s2-42.1.230)。[原文](https://www.cs.virginia.edu/~robins/Turing_Paper_1936.pdf)。原文记载1936年收稿与报告，引用年份依出版社书目。

[4] Papert, S.; Solomon, C. *Twenty Things To Do With A Computer*. MIT Artificial Intelligence Memo No.248 / LOGO Memo No.3, June 1971. [MIT记录](https://dspace.mit.edu/entities/publication/35dcc702-9306-4ad7-8a42-1209517c9c1c)。[2022经许可重印的原报告扫描](https://citejournal.org/wp-content/uploads/2022/03/v21iSeminal1.pdf)。本章采用原报告开篇及活动1。

[5] Facione, P. A. *Critical Thinking: A Statement of Expert Consensus for Purposes of Educational Assessment and Instruction. Research Findings and Recommendations*. 1990. ERIC ED315423. [原报告](https://files.eric.ed.gov/fulltext/ED315423.pdf)。

[6] Design Council. *Framework for Innovation*. [官方说明](https://www.designcouncil.org.uk/resources/framework-for-innovation/)，设计过程与原则部分；网页未注明本页发布日期。

[7] NIST/SEMATECH. *e-Handbook of Statistical Methods*, §5.1.1 What is experimental design? [官方手册](https://itl.nist.gov/div898/handbook/pri/section1/pri11.htm)。

[8] Meadows, D. H. *Leverage Points: Places to Intervene in a System*. 1999. [作者文章存档](https://donellameadows.org/archives/leverage-points-places-to-intervene-in-a-system/)，反馈时延及负反馈部分。

[9] NIST. *Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile*. NIST AI 600-1, July 2024. DOI: [10.6028/NIST.AI.600-1](https://doi.org/10.6028/NIST.AI.600-1)。[原文](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)，§2.2。
