# Chapter 2 Authoring Brief

## Shared Contract

读取`AGENTS.md`、`skills/textbook-authoring/SKILL.md`、`specs/ch02.spec.md`、`plans/ch02.plan.md`和本brief。只写assigned allowed_paths；无其他写入/commit/stage/嵌套委派。正文中文，正式章/节题中文；Spec/Plan/report用英文section title。源稿使用`[[S01]]`等来源占位，Parent最后按首次出现统一；不得造引用。以下来源标识是内容locator，不代表writer独立查过原文，Parent负责保存实际核验。

章名《计算思维的核心方法与AI辅助》。各节约5000—6200汉字（不算代码/链接），不能以术语表、重复提示或代码凑数；continuous explanatory prose为主。已有基本编程/图先备，聚焦超越实现的新判断，不写品牌工具教程。导语和开头情境自然组织，节内一般到`2.n.m`三级。独立练习完整材料/评价在节末附近，完整答案另写assigned answer片段，组装后统一章末。反思保留具体决策问题。正文可以另设完整worked example，必须不同于独立练习数据/关键结论。

## Sources and Figure Reservations

- S01：Wing, Computational Thinking: What and Why?, CMU, 2010；表示与抽象的有限概念支持。Parent 2.1使用。
- S02：Parnas, On the Criteria To Be Used in Decomposing Systems into Modules, CACM 15(12):1053–1058, 1972, DOI 10.1145/361598.361623；信息隐藏与流程式分段的区别。2.2使用，原文核验由Parent保存。
- S03：scikit-learn官方Common pitfalls, https://scikit-learn.org/stable/common_pitfalls.html ，§12.1–12.2；一致变换、预处理和数据泄漏。2.2可引用变换一致，2.3引用泄漏。不把文档样例复刻成正文。
- S04：scikit-learn官方Cross-validation, https://scikit-learn.org/stable/modules/cross_validation.html ，§3.1.2.4、§3.1.2.6；同组/时序划分。2.3使用，只讲所需边界。
- S05：Dijkstra, A note on two problems in connexion with graphs, Numerische Mathematik 1:269–271, 1959, DOI 10.1007/BF01386390；非负边权最短路径（原论文positive length）。2.4使用，现代零权扩展说明为标准实现条件，不归给原论文原话。
- S06：MIT OpenCourseWare 6.006, Lecture 13 BFS / Lecture 16 Dijkstra / Lecture 14 DFS，官方教材；Parent提供准确URL与核验，2.4不写未经核实的历史细节。
- S07：Python官方Sorting HOW TO，https://docs.python.org/3/howto/sorting.html ，Sort Stability and Complex Sorts；稳定排序与复合键。2.4使用。
- S08：NIST AI RMF 1.0，2023，doi:10.6028/NIST.AI.100-1；有限用途的风险/测量/监控边界。Parent 2.5使用。
- S09：RFC 9110, HTTP Semantics, §9.2.2, 2022；幂等语义与自动重试前提，Parent 2.5使用。
- S10：Amershi等, Guidelines for Human-AI Interaction, CHI 2019, DOI 10.1145/3290605.3300233；错误时纠正/控制的有限设计支持，Parent 2.5使用。

图2-1两种表示、图2-2状态扩展：Parent 2.1；图2-3 DAG与版本接口：writer A在2.2引用，Parent制图；图2-4观察规则的适用区域：writer A在2.3引用，Parent制图；图2-5路径与算法状态：writer B在2.4引用，Parent制图；图2-6同批评估、图2-7自动化状态：Parent 2.5；图2-8综合导览图：章末。writer只以Markdown嵌入`../../assets/figures/ch02/fig2-n.png`及图题/来源/正文读图任务，不制作或写figure files。编号不烘焙入图。表格使用临时`表2-XA1`（2.2）、`表2-XB1`（2.3）、`表2-XC1`（2.4），Parent连续编号。

## E02 Fixed Data

原创教学数据：无资源冲突、无限可并行的处理环节。A读取快照2分钟，无前置；B统一节点标识4分钟，依赖A；C核对通行规则3分钟，依赖A；D计算路线5分钟，依赖B/C；E生成节点说明2分钟，依赖B；F端到端检查3分钟，依赖D/E；G发布交付包1分钟，依赖F。时长确定，启动时刻0，输出只有完成后可用。数据版本必须一致，规则摘要含map_version与profile，路线也含这些字段；不可只比较字段名。任务：依赖图、两种合法执行序列、无限并行的最早完成与关键依赖链；诊断B提供R7节点而C提供R8规则；变化D耗时由5改2，重新推导关键链/工期。writer设计完整题设及评价，答案给手算过程，Parent可执行复算。

## E03 Fixed Data

预测下一10分钟某入口是否拥堵。x为预测时点前5分钟已观测人数，event为当时已知是否安排活动，y为未来10分钟实测拥堵标记；都是模拟。记录按时间d1—d12排列，相互不同场次，开发集d1—d8，冻结测试d9—d12，不可用y作为输入。列表(x,event,y)：d1(80,0,1)、d2(70,0,1)、d3(55,0,1)、d4(45,0,0)、d5(30,0,0)、d6(60,1,1)、d7(40,1,1)、d8(20,1,0)、d9(65,0,1)、d10(48,0,1)、d11(38,1,0)、d12(25,0,0)。候选RA：x>=50；RB：x>=50或(event=1且x>=35)。这些候选作为预给规则，学生先开发比较并记录选用，再揭示/使用测试；全表随书给出，说明自学时覆盖后四行即可。任务：两规则开发和测试混淆计数、有限支持结论、反例、一个追加信息方案、时序/同对象划分反例。答案不宣称小测试显著性/普遍优越/因果。正文worked example另造不同小数据，不能提前算E03。

## E04 Fixed Data

原创有向图：S→A=1、S→B=4、A→B=2、A→C=1、A→T=9、B→T=2、C→T=9，单位分钟，其余边不存在，边权静态非负。BFS邻接按字母升序，目标T在出队时停止；局部最小边策略每次选当前最小边，平局按字母，禁止重复节点；Dijkstra按最小暂定距离确定节点，平局字母。任务：比较三策略路径/代价，逐步Dijkstra，说明BFS与局部贪心的目标错误；把B→T改为-3，指出标准确定后不再更新的Dijkstra可失效的条件但不得声称本图一定失败，另构造最小失败图；排序记录(id,priority,submitted)：r1(2,09:03),r2(1,09:02),r3(2,09:01),r4(1,09:01)，先priority升序再同priority按submitted升序，解释稳定多次排序次序及复合键。答案给完整验证，负权扩展只比较算法假设，不采用负时间为现实导览数据。

## Boundaries Between Sections

2.1讲任务相关表示/状态，不讲完整路径算法；2.2讲协作语义和依赖，不再讲资源排程；2.3讲从样本到有限规则及检验，不写模型训练教程；2.4讲算法过程/证明条件，评估数值与自动化在2.5；2.5讲测量/反馈/执行状态，不系统展开第三章素养或第四章因果。第一章不作为内容/结构来源；可以只读新第一章opening/closing核对术语边界。
