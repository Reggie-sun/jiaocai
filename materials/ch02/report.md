# Chapter 2 Delivery and Reuse Assessment

## Delivery Scope

本轮按用户2026-10-11授权，完成第二章《计算思维的核心方法与AI辅助》的Spec、Plan、五节正文、章首章末、E01—E06及集中题解、教学图和正式Word/PDF。正文为35,238个近似汉字，含答案，排除代码块及链接目标；13张表、8幅原创教学图、10项参考来源。正式PDF共78页。稿件与篇幅登记见[assembly.json](assembly.json)。

- [完整稿件](../../manuscripts/ch02/ch02.md)
- [Word](../../output/ch02/第二章-计算思维的核心方法与AI辅助.docx)
- [PDF](../../output/ch02/第二章-计算思维的核心方法与AI辅助.pdf)
- [Spec](../../specs/ch02.spec.md)与[Plan](../../plans/ch02.plan.md)

当前为整章完整教材初稿与正式排版交付，Harness沿用`chapter/draft`。正式排版、工程验收和出版定稿分别表述；真实教师/学生试读、课堂效果、校方与出版社审定尚未完成。

## Teaching Design

以大三、大四计算机专业读者已学编程、数据结构和基础图算法为先备，新增能力围绕“什么时候已有技术仍不足以支持判断”展开。2.1用任务相关信息合并及服务状态解释抽象充分性；2.2区分流程分段、信息隐藏与可组合的语义接口；2.3从有限记录到候选规则，定位例外、对象/时间泄漏及预测与因果的区别；2.4追踪BFS、局部贪心和Dijkstra的不同目标、确定不变量、失效反例与稳定排序副作用；2.5检验共同样本、分母、覆盖门槛、预处理成本和结果未知时的自动化恢复。

知识类型决定讲解组织，未复制第一章案例或统一套用其推理结构。场馆预约模块、入口记录、路线策略与自动化提交承担不同教学作用。E06综合导览将表示、依赖、算法、评价和失败诊断连接起来；小地图、时间、方向、服务条件和变化任务完整给出。AI辅助用于有界候选、反例与对照，不要求品牌、付费账户或把模型回答视为证据。

## Sources

Parent实际浏览10项原始/机构存档/官方来源，核对内容支持和书目信息，见[sources.json](sources.json)与[source-support.md](source-support.md)。正文按首次出现顺序编号，参考文献集中章末。沿用全书确定的`GB/T 7714-2025`引用基线；未声称本章逐条核验完整标准或出版社已认可。地图、记录、工期、门槛、失败惩罚及推导均标为原创教学模拟，没有把引用研究的结论冒充本章实测结果。

独立审校者收到原文定位账本，不因此被描述为独立重读了全部外部原文。失败链接与验证码未被记作已读支持；可读替代入口和限制均保留。

## Independent Review

独立教学审校为Native只读会话`/root/teaching_review`，实际`reviewer_high`。R1完整通读提出T01状态组合计数、T02关键依赖链教学先导、T03相同预测与相反实际标签三个发现；Parent分别调查、修正并复算。R2实际重新通读1—893行及当前Skill、Spec/Plan，确认三项触发问题消除，没有新增发现。报告见[teaching-review-r1.md](teaching-review-r1.md)、[teaching-review-r2.md](teaching-review-r2.md)。

R2→R3只有一处图2-6阅读定位措辞改变：“只看两根平均值柱”改为“只看平均值”，匹配最终表格与覆盖框；old/new SHA及完整差异见[editorial-equivalence.json](editorial-equivalence.json)。之后专业初审发现两处题解解释问题，实质修订E02/E06。教学reviewer最后一次定向复查实际读取方法、完整题干与题解，独立复算，确认新解释准确且T01—T03修复保持。全章审阅由前两轮提供，新字节由[teaching-review-r3.md](teaching-review-r3.md)明确范围覆盖，不伪称第三次全章通读。

专业审校先通过受管Kimi sealed/qualified deep route执行。R1因外来Skill并发变化返回`SOURCE_CHANGED`，输出隔离；R2本地执行exit143，canonical receipt查询返回`INCOMPLETE_RECEIPT`，第三次请求保持`OUTCOME_UNKNOWN`，不采用partial、不重跑旧seal。R3 canonical为`UPSTREAM_GENERATION_LIMIT`，运行782.34秒、3次请求，读取七项材料后未交付完整报告。三轮结束，不新增第四次Kimi。原消费与快照、qualified live route及实际Docker证据保留。

R3生成预算耗尽与R1源漂移不伪称为可计数runtime故障；未借“两次运行故障fallback”掩盖分类。按当前用户自主交付授权及SUBAGENTS耗尽后的有界升级，Spec/Plan自审一项窄恢复：一个新Native只读`/root/professional_native`、实际`reviewer_high`接手相同完整专业Scope，一次初审及最多两次必要修正复查。该独立会话不读取作者、教学或其他peer审校意见；复查阅读数值证据时自行裁决，不采用PASS字段。Native执行不冒充Kimi/Docker proof。恢复见[professional-recovery-r3.json](professional-recovery-r3.json)。

Native初审实际完整读取七项材料及正文1—893行，提出P01工期缩短解释自相矛盾、P02遗漏未知边乐观下界；Parent独立确认并修订。一次专业定向复查确认两项已修正，无新增finding；完整实际coverage及原SHA保留于[professional-review-native-r1.md](professional-review-native-r1.md)、[professional-review-native-r2.md](professional-review-native-r2.md)。Parent以差异、固定输入和独立数值核验逐项裁定，没有未解决blocking，见[professional-adjudication.md](professional-adjudication.md)。最终正文SHA为`e09aa94519f298a7fc7979f7c494c525f2146e1bbfcc56a913ba41d0311ca8b0`。

## Exercise Verification

独立会话`/root/verify_exercises`从固定输入重构可执行核验，没有把题解文本当作程序期望值。Parent在当前候选重跑46/46项检查通过，输入与脚本hash不变。证据见[exercise-verification.json](exercise-verification.json)、[exercise-verification-notes.md](exercise-verification-notes.md)，另有[editorial-verification.json](editorial-verification.json)复算审校修订的状态数、微型DAG和预测—标签对。

核验使用穷举路线与独立搜索结果相对照、增广状态/服务计费与截止边界、DAG前置最大值和全部链长、精确分数指标、稳定排序与成本比较。关键结果包括E02工期15及变体12分钟、E04三策略10/11/5分钟和负边最小反例、E05共同成功差7/3分钟但候选覆盖不达门槛、E06服务完成7分钟/最优到达12分钟及关闭/未知边区别。

专业修订另外实际复算5个案例：D=5/2/1时15/12/12；C—D关闭、固定7分钟C—X乐观可用或排除时14/15，两者均超过12。路线独立搜索与增广穷举相符；不确认未知边。完整输入、脚本SHA及轨迹见[professional-correction-verification.json](professional-correction-verification.json)。原46项检查在最后内容修订后再次通过，未改变独立脚本或输入来迎合答案。

检查覆盖给定有限教学输入，不能替代任意输入正确性证明、现实路线安全或平台提交验收。自动化核验未发送外部请求，UNKNOWN仍保持未知。

## Typesetting and Actual Page Evidence

复用`textbook-style-v1.0`及原DOTX。共用styles、fontTable、theme、settings、footer部分逐字节保持，章号/页眉缓存、内容、图和原生SEQ/REF/TOC/PAGEREF书签在本章slot适配。最终DOCX未通过LibreOffice另存；PDF由原bundled documents renderer生成。13表内容与Markdown完全对应，8图按155mm插入，约393ppi，最小图字约10.74pt，跨页表头重复、行不拆分，代码完整同页。27个REF及目录缓存与实际页面核对通过，字体全部嵌入。

R2全78页逐张实际检查：独立Native页面会话A查看1—30，B查看31—60，Parent查看61—78。Parent调查表2-3错位疑问后，以实际页面和PDF坐标反证判为FALSE_POSITIVE；确认图2-7框内文字触边、表2-11来源跨页孤立两项，并作最小修复。R3有64页PNG字节完全相同，继承对应原观察；14变化页53、57、67—78全部重新实际查看，两个阻断均关闭。独立B另看56/58相邻页。原发现、裁决及每页观察见[page-review-r2.md](page-review-r2.md)、[page-review-r3.md](page-review-r3.md)。

最终题解修订后重新渲染R4：67页PNG与R3逐字节相同，11变化页68—78逐张重新实际查看，未见新增阻断。完整记录见[page-review-r4.md](page-review-r4.md)与[page-delta-r3-r4.json](page-delta-r3-r4.json)。最终完整78张实际审查PNG保留在[snapshots/final-pages-r4.zip](snapshots/final-pages-r4.zip)，R3历史全页亦保留。逐条hash与最终稿件/Word/PDF身份见[page-review.json](page-review.json)。[layout-r4.json](layout-r4.json)是互补的可执行检查，未代替实际页面阅读。当前DOCX SHA为`1951b77359e96aaf8aa3dd82211c4fde1aa03b1ab1941fe78f41bab9d2ff1644`，PDF SHA为`b15717242ad58d9280193cdc05bd5104d9014ea25c3157a74bfe5a6fcf73281d`。

## Minimal Repairs and Preservation

修复局限本章：目录检测使用实际标题字号，避免正文提及“参考解与讨论”误触发；表2-11稍减单元格上下内边距并保持末行与来源相邻；图2-7改三行并局部增高框；正文图2-6定位与成图一致。内容修订以真实发现和可核验依据为准，没有重构Harness、模板或Agent路由。

本轮开工登记的200项旧文件中199项原字节保持；第200项教材Skill被另一会话修改，本轮保存其明确新SHA而没有覆盖、暂存或提交。外来绘图pilot、Skill及目的记录更新已由另一会话提交`4694718`；本章只接续追加自己的记录。历史第一章run因Skill依赖变化被Harness自动标为stale，不修改旧receipt或自动重做历史验收。见[concurrent-changes.json](concurrent-changes.json)和[protected-source-sha256.json](protected-source-sha256.json)。

## Engineering and Completion Gate

原51项Harness测试实际通过，原引擎与policy验证通过，见[harness-tests.txt](harness-tests.txt)、[harness-validation.json](harness-validation.json)。当前task-local实现Risk Gate为`KIMI_REVIEW_NOT_REQUIRED`：没有明确额外工程review要求、关键凭据/越权/难恢复生产状态失败路径，亦无同时满足重大后果、验证后实质缺口与额外review增益的具体证据；详见[implementation-risk.json](implementation-risk.json)。该判断不豁免独立教材专业/教学审校。

整章新run为`ch02-delivery`，通过原CLI登记、check、五维Parent AI自审review及accept；最终状态与完整证据由[harness.json](../../harness.json)及[runs/ch02.review.json](../../runs/ch02.review.json)独占，交付后只读状态另存[runs/ch02.status.json](../../runs/ch02.status.json)。本报告是内容和复用评估，不构成第二个工程状态owner。Parent拥有最终diff、finding裁决、质量和交付责任，不用reviewer verdict或机器PASS自动接受。目的记录与owned files在稳定checkpoint提交，保留并发第一章图稿。

## Cross-Chapter Reuse Assessment

第二章已验证主要生产机制适用于不同知识组织：同一质量Skill、Markdown Spec/Plan、互斥作者和独立检查职责、原Harness接口、共用样式/域与实际页面证据均能沿用；无需修改引擎、模板或路由。增加的是第二章内容、数据与有界适配器，而不是新控制面。

这个案例支持主体内容/核验/排版生产链跨章节复用；它不能独自证明十章均稳定、真实学习效果成立或全链路稳定。尤其Kimi专业审校三轮均未形成完整可用结果，需实际阻断后的Native窄恢复；这不支持“外部审校调用已稳定”的结论。配置与控制面未重构，恢复只调整本章独立职责的实际调用。独立页面审校存在一次误判，Parent用可查看反证裁决，说明判断owner与证据链仍不可省略。

最终专业/教学审校、数值与页面证据已经闭合。因此本轮证明了主体生产体系可以完成跨章节复用，未证明整条链无恢复即可稳定执行；外部审校调用是实际复用缺口。十章长期稳定性和教学效果仍需更多章节及真实读者证据。非阻断建议没有被升级为本轮重构任务。

## Follow-up Suggestions and Limits

不阻断本轮的建议：未来在有实际需求时参数化章号/目录适配器；协调共享Skill的snapshot变更窗口；保留教学图语义与缩放后实际查看；表2-12窄表头可在出版排版时进一步美化。未主动实现这些优化，也未新增工具或路由。

真实教师/学生试读、课堂试教、校方课时与目录确认、出版社体例、Microsoft Word原生域更新和实体打印尚未验证。更新Word域或改变分页后应重新核对目录和页面。后续章编写须按自己的学习目标另做内容设计；本次交付不授权直接开始第三章。
