# Chapter 1 Historical Revision Implementation Plan

## Goal and Scope

依据`specs/ch01-history.spec.md`完成第一章新版文字初稿与相关核验。Native Codex负责整合、史实查证、最终裁决和交付；`superpowers:writing-plans`仅提供计划约束，不接管生命周期。沿用`textbook-style-v1.0`，原提纲总纲、旧稿、图、输出和历史run保持。

## Ownership and Contract Surfaces

新稿独占`manuscripts/ch01-history/`，资料独占`materials/ch01-history/`。Parent写1.2、1.3、章首/章末与合并稿；一个native bounded writer独占1.1、1.4及其答案片段；没有同文件并行写入。专业内容审校交给受管Kimi，教学阅读交给独立native只读会话。审校输入是稳定快照，不给作者PASS结论；Kimi封存期间不修改其ReadPaths。Parent更新现状记录前重新核对是否出现外来同文件修改。

当前工作区未跟踪的`materials/ch02-progressive/`、`plans/ch02-progressive.plan.md`、`specs/ch02-progressive.spec.md`及`tests/__pycache__/`不属于本轮，保留且不stage。原`specs/ch01.spec.md`、`plans/ch01.plan.md`和历次正文保持历史身份；新契约由现状记录链接，不形成旧稿静默替换。

## Major Milestones

### Milestone 1: 原材料和来源成为可执行写作依据

已读取原提纲相关正文和3.1样稿正文、表格，核对四节主题；保存本轮原始输入和历史产物保护哈希。Parent检索原论文及官方历史记录，形成`materials/ch01-history/sources.md`，明确事实与作者解释。验收依据为每个采用的历史节点有实际支持位置，不依赖未核验的名字、年代、产品能力或课堂效果。

### Milestone 2: 四节及章首章末形成完整学生稿

创建`manuscripts/ch01-history/section-1.1.md`至`section-1.4.md`及章首/章末片段，合并为`ch01.md`。每节遵守导语、首小节案例描述及分析、逐步讲解、训练和最后反思；E01—E09题解集中章末。案例体现各节独有增量，不重复换名。通过自然语言、可手工执行的小步骤进入，历史与跨界知识贯穿，不以复杂排程作主线。

### Milestone 3: 当前内容与出处得到核验和独立审校

检查近似汉字数2.8万—4万、原题名、章节编号、练习/答案对应、引用双向关系与首次顺序；实际复算数量和规则例子。先完成Parent内容检查，再封存全章与来源包进行专业内容审校，独立native会话检查难度、连贯性、重复和任务可做性。报告及Parent裁决进入`materials/ch01-history/`；确认的关键缺陷修正并重检，实质修正由相应会话读取新快照复查。每个职责初审及最多两次有依据的复查。

### Milestone 4: 文字阶段交付与图文后续边界清楚

创建`materials/ch01-history/figures.md`及`report.md`，记录各图用途、内容、位置与已规划状态；将核验快照写入`verification.json`。执行`python3 scripts/harness.py validate`及只读`status`，解释历史stale证据而不恢复旧run冒称新稿验收。更新`教材编写现状与目的.md`链接新契约与完整文字稿，明确实图、Word/PDF、真实读者验证未完成。只stage本轮精确文件并commit，复查Git状态。

## Verification and Completion

文字阶段的结构、字数、引用、题解、示范复算与来源证据可执行核对；教学内容以实际独立报告和Parent裁决支撑，不把字符统计当教学验收。工程Risk Gate在稳定候选上评估，本轮内容审校不冒称工程强制review。完整图文Harness acceptance保持既有规则，延后出图不豁免。

## Self Review

所有Spec要求均在上述四个里程碑有归属；当前边界明确、无占位任务、无未批准的图像/排版制作、无第二章实施或worktree。执行本计划不需要新的用户批准。
