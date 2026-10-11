# Chapter 1 Rewrite and Typesetting Plan

## Goal

按[本轮规格](../specs/ch01-rewrite.spec.md)完成第一章新稿、统一教学图及正式Word/PDF，并建立当前完整快照的内容和页面核验证据。

## Contracts and Boundaries

四节主题、LO、五项练习数据和原稿保留；共用`textbook-style-v1.0`与现有Harness接口不变。新稿是新内容owner，整章合并稿由分节源生成；排版内容修改先回写源稿，不能分叉。Parent拥有整合、来源核验、图表、排版、最终裁决和提交。

## Milestones

| ID | 成果与owner | 依赖与核验 |
| --- | --- | --- |
| M1 | Parent核对原Word、当前契约、原稿与试写，保存保护文件哈希和来源支持 | 只读status；本轮Spec/plan自审；确认精确文件ownership |
| M2 | Parent重写1.1、章首/章末；两名有界native writer分别写1.2/1.4与1.3，及各自练习答案片段 | writer只写指定新文件，不改共享契约、数据或基线；各节按知识增量和字数检查 |
| M3 | Parent合并、去重、集中E01—E05题解，统一来源与图/表编号，重制教学图 | 数据与全部条件复算；核对图文；篇幅及首次引用排序；所有旧文件保护检查 |
| M4 | 受管Kimi独立专业内容审校、native独立教学阅读审校，Parent调查裁决与修正 | 输入只含目标/规格/当前稿/必要材料，不放作者PASS；冻结source直至receipt；语义修改实际复查，初审+最多两轮 |
| M5 | Parent复用模板生成Word，渲染序列/交叉引用/页码，按PDF实测页码回填目录缓存并保留原生TOC/PAGEREF，再逐页检查 | `documents:documents`与`pdf:pdf`能力；脚本结构核验+实际页检，不用机器检查代替阅读；Word原生更新未执行 |
| M6 | Parent运行现有工程测试/新run五项内容核验，更新目的记录、accept、提交owned files | 真实完整快照、read-only status、最终diff与旧稿哈希；未决出版/人类验收状态明确 |

## Delegation and Recovery

第一名native writer的allowed_paths为`manuscripts/ch01-rewrite/s1-2.md`、`s1-4.md`、`answers-e02.md`、`answers-e04.md`；第二名为`s1-3.md`与`answers-e03.md`。追加独立的1.3 writer用于降低整章写作的上下文负载，三方写入集合完全不相交，直接共享current working tree。作者停写后Parent接管整合。只读审校独立于作者；Kimi通过sealed contract与canonical receipt运行，不直接provider调用。连续两次可计数的运行故障按SUBAGENTS fallback，不采纳partial/UNKNOWN结果。来源不足时移除或准确限定，不改练习硬约束冒充可行。

## Self-Review

M1—M6覆盖本轮规格：内容深度、保护边界、答案分离、篇幅、来源/图表、独立内容审校、真实页面和Harness证据均有owner与验证。两名writer仅拥有互斥的分节文件；互补审校不重复作者职责；无额外用户批准步骤、worktree或格式设计。
