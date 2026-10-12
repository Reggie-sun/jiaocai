# Nationwide Textbook Feedback Revision Plan

## Goal and Current Authorization

按[修订Spec](../specs/revision-feedback.spec.md)落实截图反馈。当前用户选择 `AB`，因此本轮只完成反馈清单、项目要求和相关Spec/Plan更新及其文档验证；M1—M5正文工作未启动，列作后续执行路线，不借本计划扩展当前授权。

Native Codex保留lifecycle与最终裁定。使用 `textbook-authoring` 维护教学契约，`superpowers:writing-plans`提供计划自审，`external-subagent`承担一次受管只读源mapping；不升级完整workflow、不创建worktree、不叠加Spec/Plan reviewer。

## File Structure and Ownership

| Owner / Files | Responsibility |
| --- | --- |
| `skills/textbook-authoring/SKILL.md` | 全国定位、二级节案例与可替换工具方法的唯一教学规则 |
| `specs/revision-feedback.spec.md` | 本次跨章增量、原纲覆盖、章节边界、验收标准 |
| 本Plan | 依赖、工作边界与后续验证路线 |
| `materials/revision-feedback-20261012/feedback.md`、`case-plan.md` | 原话/更正与逐章/逐节可审阅修改清单 |
| 同目录源提取、清单、时间线、receipt/裁决、验证记录 | 现有输入与本轮实测证据；不冒充正文验收 |
| `AGENTS.md`、质量Spec、讨论/蓝图、现状记录、相关章Spec/Plan顶部路由 | 指向唯一owner，消解旧全国/校本与旧轮次执行范围冲突 |

本轮只有Parent写文档。foreign第二章未跟踪来源和tests缓存、1754项非目标tracked文件受保护；准确集合和开工SHA见[保护清单](../materials/revision-feedback-20261012/preservation-before.json)。用户没有要求新的branch/worktree或push，沿当前 `chapter-02-delivery` 工作并只提交owned paths。

后续内容另存 `manuscripts/chNN-feedback/`，图文稿另存 `manuscripts/chNN-feedback-layout/`，证据在 `materials/chNN-feedback/`，确需变化的图在 `assets/figures/chNN-feedback/`，Word/PDF与交付说明在 `output/chNN-feedback/`；NN取01—10。原稿及历史输出不覆盖。原始DOCX保留，若后续交付全国版大纲，另存 `output/outline-feedback/`，仅清理学校专属文字并保留其余课程说明。以上是后续文件owner定义，本轮不创建正文/输出目录。

## Invariants and Compatibility

原纲章序、主题及非学校专属标题保持；第六章校本章题作有限通用化，第九章继续为补充提案。完整章2.8万—4万字，困难逐步铺垫、基础任务可用手工/本地路径完成。参考解集中章末，题/解/数据/图边界一致，史实、原文、作者解释与模拟分开。

沿用 `textbook-style-v1.0`、共用DOTX、图文和原生字段约定；不改Harness引擎/policy/schema。新规则使旧证据失效时保留真实状态与历史，不改哈希复用已失效review。正文、图或分页变化后核验新完整快照；真实教师/学生、课堂及出版审定另述。

## Major Milestones

### M0 Requirements and Planning Delivery

**Files:** 本Spec/Plan、反馈/案例清单、项目/主Skill入口和相关章契约路由、源与时间线记录、只读status及文档验证。

**Contract:** 以F08作为删除边界，以用户时间线更正和Git日期定位最新稿/第二章初版。第二章源mapping在sealed snapshot上只读执行；Parent核验actual Read、报告/receipt哈希并直接核对关键发现。其余规则与Spec/Plan由Parent自审。

**Acceptance:** R1—R7的本轮可审阅项完成；全国定位和原纲主题要求无双owner，正文/原材料/正式输出/Harness/foreign字节不变，文档链接及章节路由有效，稳定提交。初版/当前版身份由时间线解决，不再作为无依据的额外审批点。

**Verification:** `git diff --check`、主Skill官方quick validation、本轮链接/要求映射/精确路径/哈希检查；`python3 scripts/harness.py validate`及只读 `status`。本轮只执行M0，结果写入 `materials/revision-feedback-20261012/verification.json` 与报告。

### M1 Nationwide Editing Map and Full Version Comparison

**Files:** 后续 `materials/chNN-feedback/` 编辑清单；第二章三版完整比对记录；需要交付时，全国版大纲另存路径。

**Dependencies:** 后续正文任务启动后，读取最新Spec/主Skill并核对M0保存的源SHA。时间线基线：1—3来自 `8bc7300`，4—6来自 `098cd16`，7—10来自 `5806a63`；第二章初版来自 `93681de`。

**Contract:** 扫描“西南财经/西南财大/西财/本校特色/学校名称”等并逐处判断用途，保留一般导入、通用校园情境、有效事实/文献。先完整阅读第二章初版、递进版、最新稿，建立原纲五节的“要求→现稿位置→初版可取内容→修改选择→来源核验”表；节首片段不足以判断全章缺失。禁止恢复废弃旧前四章的来源资格。

**Acceptance:** 学校专属清理可逐处复核；第二章每项原纲主题有采用位置或需要纠正的技术理由，原有有效基础讲解与练习保留。第六章全国版题名采用Spec的编辑方案，不改PBL主题或其它既定标题。

**Verification:** 原DOCX实际文本/表格和三版完整稿比对、SHA核对、精确修改清单、保留说明/教学内容的上下文复读；不只做字符串删除。

### M2 Chapter 2 Multi Case Revision

**Files:** `manuscripts/ch02-feedback/`、`materials/ch02-feedback/`；图/排版在M5前不作为推进前置。

**Dependencies:** M1第二章完整比对和相关一手来源查证。

**Contract:** 五节原题与Spec的CNN/LLM、无人机/Grad-CAM、医院/电网、三组算法比较、元学习/银行主题逐项展开。一个易懂案例引入，再用领域对照说明AI改变了什么、人工判断如何保留及机制局限；校园导览继续作为章末综合任务。初版材料先评估再融入，不能倒退为高难入口或逐字拼接重复内容。

**Acceptance:** 原纲案例主题实际可定位、不是仅点名；学生能凭先行解释完成基础任务；术语和不同AI机制不混同；篇幅、题解和来源一致。纯模拟输出不能当作真实模型表现。

**Verification:** 结构/标题/字数、原纲主题映射、题解/边界复算、引用原文支持检查及必要相邻章阅读；完整专业/教学审读在M4执行。

### M3 Chapter 8 Domestic Tools and Academic Resources

**Files:** `materials/ch08-feedback/` 官方来源与功能/访问证据、资源选择表；`manuscripts/ch08-feedback/` 的8.3—8.6及必要章末任务。

**Dependencies:** M1确认章节分工；可与第二章独立推进，writer paths须互斥。

**Contract:** 按学习任务组织国内可用路径和国际大学开放课/文档/论文/学术社区。官方查证功能、账号/价格/下载导出、访问/语言与更新日期；实际本机可用只说明环境范围。国际参照保留，有需要时提供替代方案；不把工具选择等同于学习效果。设计一条“学习目标→选资源→练习/提取→整理→独立表现→反馈调整”的完整流程。

**Acceptance:** 对国内不同网络/设备/预算条件给可执行选择，推荐和限制有来源；基础任务有无付费账户、本地或纸笔路径；国际资源说明适用目的、先备、引用/评审身份。没有官方或当前访问证据的易变主张保持未知或删去，不虚称已测试。

**Verification:** 对每个实际采用工具/资源在线核验官方页面；涉及操作的方案按最小材料实际演练并记录输出/截图或本地文件。不要求发布、注册付费或上传个人资料；静态资源介绍不凭造截图确认全国可达。

### M4 Chapters 4 to 9 Section Cases and Content Review

**Files:** 对应 `manuscripts/ch04-feedback/` 至 `ch09-feedback/` 及各章 `materials/chNN-feedback/`；8章与M3由同一章owner整合。1/3/10只做已计划的学校信息清理及必要局部修补。

**Dependencies:** 各章M1清理/原纲核对，8章包含M3资源输入；与M2互不形成循环。

**Contract:** 按[32节案例清单](../materials/revision-feedback-20261012/case-plan.md)逐节选择/补写/重组，第一小节案例与主题分析独立可理解，概念解释、训练与反思相连。第六章阶段案例服务同一完整项目，保留现有离线输入/测试与综合成果；第九章提案不越过第十章领导力主题。

**Acceptance:** 每节案例位置、材料、知识差异与分析可定位；有教学价值的旧文保留，新增案例不变成同题换名或篇幅填充。两名不同实际只读会话分别检查专业/来源与教学/递进，整章实际读取、Parent裁决、确认实质修改真实复查。局部修订的范围如实记录，不虚称全书已审。

**Verification:** 按主Skill `Independent Content Review` 及全局受管route；每职责初审加最多两次有依据复查，不能自动重试UNKNOWN/partial。先核验题解/数据/引用，再封存稳定稿审读；不叠加无独立目的工程review。源数据或案例关系变动后复算相应检查及邻节依赖。

### M5 Figures Documents and Bound Delivery

**Files:** 新图文稿、确需变化的editable图资产、新Word/PDF、报告与现有CLI创建的各章修订run；每章立即更新现状记录。

**Dependencies:** 当前章文字稳定、来源/练习核验、M4独立内容审校与Parent裁决完成；各章可独立交付。

**Contract:** 图后期统一处理；未改变图义的旧图可引用，但路径/编号/来源/实际尺寸要复核。复用模板和既有导出能力，改正文时回写写作源，渲染PDF并实际查看最终所有页面，只有PNG字节相同页才能继承先前观察。保留原生题注、引用、答案定位、目录与页码。

**Acceptance:** 新稿、图/题解、Word/PDF和证据对应同一当前快照；完成现有 `chapter/draft` check→review→accept，记录真实review来源和人工/课堂/出版限制，owned commit。原版本/失败/消费记录保留；未获发布请求不上传。

**Verification:** 新稿所需数值检查、全文/逐表/图嵌入/域/字体/目录、全页观察、原文件保护；按现有README和CLI登记，不重写schema或手填通过。行为/适配器若实际变化才运行相关工程测试，按照实际风险判断Implementation Review Risk Gate。

## Acceptance Coverage and Self-Review

| Requirement | 本轮落地 | 后续实施 |
| --- | --- | --- |
| R1 原话/更正/时间线 | M0反馈和证据 | M1上下文清理 |
| R2 全国定位 | M0唯一主Skill与薄路由 | M1、M4各章实际内容 |
| R3 第二章原纲/初版 | M0主题表与时间线 | M1全稿比对、M2成稿 |
| R4 32节案例 | M0候选与差异清单 | M4逐节正文与独立审校 |
| R5 学习工具/资源 | M0核验及任务契约 | M3在线查证和操作演练 |
| R6 计划/章节路由 | M0 | M2—M5对应当前快照 |
| R7 保护/验证/提交 | M0 | M5新章交付 |

Parent自审：R1—R7全部覆盖；M1是必要材料核对，M2/3/4可按章启动并守住精确file ownership，M5依赖内容稳定，不设同文件并行。不同章任务无循环或额外审批点；未知来源的处理、资源核验和回退路径明确，不用空泛占位替代方案。当前自然停止点为M0文档交付，下一步正文修订由用户后续任务启动。
