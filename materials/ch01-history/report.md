# Chapter 1 Historical Text Revision

## Delivery

2026年10月12日，按用户选择A完成[第一章完整文字初稿](../../manuscripts/ch01-history/ch01.md)。章题《计算思维：数字时代的核心素养》和四节主标题保持原提纲，历史问题与思想演进贯穿全章，从手工查找、记录和比较进入，再讲计算与信息思想、跨界迁移及互补思维。AI时代的变化在相关节点衔接，重构机制集中留第二章。

当前契约为[Spec](../../specs/ch01-history.spec.md)与[plan](../../plans/ch01-history.plan.md)。完整学生稿以`ch01.md`为准；同目录片段是分工写作与组装输入，来源键和制作注释不进入学生稿。旧稿、旧图、Word/PDF、原始材料及历史审校保留，没有静默替换。

## Content and Verification

- 35,014个汉字，含章末参考解；去除代码块、HTML制作注释与URL目标，以近似汉字数核对2.8万—4万范围。另列去除链接目标后的41,981字符，不冒称出版社正式字数。
- 四节均有导语、首小节单段案例描述与后续分析，逐步讲解后安排训练及结尾反思。节中组织随知识类型变化，不套固定小节模板。
- E01—E09连续，详细答案集中章末。题内提供纸笔操作的材料，基础与应用逐步递进，拓展不构成基础门槛。
- 九项来源按首次出现顺序对应[1]—[9]，史实与原创课堂模拟、作者解释分开，来源事实及未核验范围见[登记](sources.md)。
- 已核对标题、章节和练习/答案编号、引用顺序与对应、未替换来源键、制作注释及占位内容；复算资料筛选、三类计数、格图改动、指令闭合和误读位置。E09示例为163个汉字、含标点179字符，满足题设150—200字。

[组装记录](assembly.json)、[文字检查](text-check.json)与[最终快照](snapshot-final.json)绑定当前正文SHA256：`0821dd957553a84a03f38f8b38132a968d48537bf6eac266ed1b0f53c5f036bb`。检查仅证明所列文字与示例条件，不证明教学效果。

## Independent Content Review

专业初审为受管Kimi独立只读会话，实际完整阅读S1稿、Spec、plan及来源登记；教学初审为另一个Native独立只读会话，实际阅读全文及适用教学规则。两类职责独立，Parent逐项调查裁决。报告、读取范围、snapshot和限制见[专业裁决](professional-adjudication.md)与[教学记录](teaching-review.md)。

确认的修正包括：E08答案只用题内许可的模拟文字；E09补齐可核对的原句和摘要；E05增加工业技术与工具变化的成果证据；来源登记补齐已有正文细节；E09展板说明达到题设篇幅。Native R2实际复查前三项的S2与上下文，S2到最终稿仅增加最后一项展板说明。[S1到最终稿差异](review-delta-r1-final.patch)供专业R2作最终快照上的有界复查；不能把局部复查称为又一次全章阅读。

专业R2已完成实际有界复读，覆盖全部修订及相应题设、案例和答案，新增finding set为空。Parent核对完整receipt、原文及复算后关闭已确认问题，无未解决blocking；最终正文与专业R2所读字节完全相同。专业两轮及教学两轮均为AI审校，不构成真实师生或课堂验收。

## Figures and Engineering Evidence

[七幅图表](figures.md)均已规划，当前未制作实图；练习不依赖它们。Word/PDF及页面检查未执行。文字先行是当前阶段边界，完整图文章级交付仍需实际图、图文核验与当前Harness check/review/accept。

`python3 scripts/harness.py validate`通过，见[验证证据](harness-validate.json)。只读`status`显示原五个run的`effective_state=blocked`，因为蓝图、Skill或质量契约等依赖快照已经失效，见[状态证据](harness-status.json)。没有修改引擎、policy或历史run，没有申请无实图的完整chapter acceptance，没有用旧run证明新稿通过。

开工559个tracked文件中，仅本轮的AGENTS路由与现状记录改变，其余557个保持原字节。其他会话的第二章progressive资料、稿件、图及其Spec/plan不属于本轮，不stage。未增加引擎测试或变更工程契约；本轮采用文字、来源、示例复算、独立内容审校及Harness合法性核验。

## Remaining Work

后续按授权制作插图、完成图文审校与正式排版，再登记当前完整章快照。真实教师/学生试读、课堂试教、校方及出版社审定尚未完成。当前产物是完整文字初稿，不能称出版定稿。
