# Ten-Chapter Teaching Rules Inheritance

## Decision and Scope

2026-10-12，用户说明“不能写入规则吗”“因为我要写10章”。本次在前三章跨章审校提交`8bc7300`后补充可继承的教学规则，保存已修订前三章及其原验收证据，供后续起稿与修订使用。具体问题留在[原裁决](adjudication.md)，不把每项发现都变成新增规则，也不因规则更新重写已交付章节。

唯一教学owner为[主Skill](../../skills/textbook-authoring/SKILL.md)，规格入口见[十章增量](../../specs/authoring-quality.spec.md#ten-chapter-continuity-amendment)，实施范围见[Plan](../../plans/ten-chapter-quality-rules.plan.md)。后续章级Spec读取并引用这些规则，明确自己的已教先备和新增能力；没有重复的全书规则副本、评分器或审校系统。

## Evidence and Rule Placement

| 已有依据 | 规则落实位置与取舍 |
| --- | --- |
| CON-01：原纲3.4被历史Spec误判遗漏 | Titles and Chapter Roles补逐项核对原提纲实际正文及勘误，原Spec不能替代原始证据。 |
| CON-02：指定互联网思维主题被设备状态主题替代 | 同节补标题/名称齐全不等于主题实际展开；不把小米或某个案例规定为各章模板。 |
| PRO-03及全书递进审校：术语对象改变、章间依赖需明确 | 新增Cross-Chapter Continuity，章级Spec简述已教先备、本章新能力和后章边界；同名术语换语境就地辨析。 |
| 合理复现与案例多样性裁决 | 新节要求按教学作用区分巩固与新增操作，保留有价值的复现；不强制每次复现加难或每章换领域。 |
| TEA-01：迁移练习可直接复写示范 | Practice and Reflection区分模仿题与独立应用/迁移题，变化需引发新选择和解释。 |
| TEA-02：拓展允许暂缓，却混入基础提交/评价 | 同节补分层贯穿题目、提交、评价与参考解，拓展不作为基础完成条件。 |
| PRO-01/02：完整枚举缺项、时间边界冲突 | 同节补枚举完整性与正文/图表/题解/核验的边界一致性。 |
| PAR-01：图中暴露练习关键结论 | Illustrations补图像、图题和说明的信息时机；按已有共用答案位置处理，不新设答案版式。 |
| 企业事实与作者模拟的证据裁决 | Evidence and Language补自披露只支持实际陈述的事实，模拟不能冒充内部事件或效果证明。 |

标题单字尾行已有页面核验规则覆盖，不再新增禁词、固定换行或逐章例外。节内首尾顺序与中段灵活性在质量规格中澄清，避免历史宽泛表述覆盖现行Teaching Design。

## Review and Acceptance Boundaries

继承依据包括已完成的独立内容审读、实际原纲核对及Parent裁决；最终专业复查receipt为`a5e0e438-59ce-48d4-ac62-b9f474956b7b`，原三次物理调用与20次wire记录保留。本次不发起第四次调用，不把原独立报告称为已审过新增规则。Parent核对规则与证据的关系及最终diff，不机械照收建议。

原章节验收属于其当时完整规则/材料快照。新增规则若使依赖哈希失效，保留Harness的真实`effective_state`，不改旧证据或声称自动通过新要求；重新交付章节时再核对当前稿。规则本身不能证明十章已完成、学生已掌握或课堂容量适合，实际师生试读仍待开展。

共享目的记录正在被另一会话修改，本次不写入该文件；本记录与质量规格保存新的确认和交付范围。本轮没有接管第四至六章或启动任何新章。

## Verification

安装Skill实际转接到仓库唯一owner；新增及相关11个本地链接/标题锚点检查通过。原`Formal Textbook Style`段落完整字节、DOTX、Harness引擎、前三章完整稿、六份Word/PDF、交付ZIP及原审校记录等18项文件/段落保护检查通过；教材内容和正式输出本轮未变，未重新渲染或冒称再次页面验收。`git diff --check`针对本轮文件通过；纯规则修改不新增教学评分测试，原51项Harness测试属于此前产品交付证据，未称本轮重跑。

Harness只读`validate`返回`valid=true`，policy与engine SHA和`8bc7300`一致；原11个run对象逐项保持。另一会话在本次期间新增`ch04-layout`、`ch05-layout`、`ch06-layout`，本轮未操作共享Harness写接口或提交其改动。

规则更新后的只读`status`返回1，准确标明依赖旧Skill/质量规格的快照失效：前三章三个`crossreview`及三个前序图文run新增的失效原因均仅为这两个规则文件改变；原五个历史失效run仍保留。另一会话三个新增run当次观察也显示相同规则依赖失效。该状态是新规则尚未绑定章节审校证据，不是发现新增正文错误；本次没有重填旧review或修改哈希使其通过。后续重新交付时由对应owner核对当前规则与稿件并按既有check/review/accept恢复。

实施风险判断为`KIMI_REVIEW_NOT_REQUIRED`：本次未被要求增加Kimi实现复审，无具体凭据/越权/关键生产状态失败路径；规则文档可审阅、可回退，入口、依赖、证据适用边界和既有产品字节均已核对，没有后果重大且未覆盖的实现语义缺口。不额外叠加独立工程review。

上述判断对应`8bc7300`上的当前增量：主Skill SHA256为`bc08bde674c2dba84c100f9dd0c2e7448b1fd961c1c44fc2986456269a2ec5da`，质量规格SHA256为`7c5c2e24ffb99f6d9e3013c7bcc3e7dc1f4b7d04e9f6af078f6f7057a05c7a14`；适用Plan为本轮四文件提交中的`plans/ten-chapter-quality-rules.plan.md`。

本次规则继承已完成。按项目入口评估记录要求，未声明专门session-record Skill；本记录即现有`materials/`下的稳定交付与接续证据，不写入全局memory。
