# Chapters 1–3 Review and Revision Plan

## Current Feedback Revision

2026-10-12最新稿反馈中的第一、三章全国定位清理与第二章原纲/多案例修订，按[跨章修订Spec](../specs/revision-feedback.spec.md)与[Plan](../plans/revision-feedback.plan.md)执行。当前用户选择 `AB`，只交付清单/要求/Spec/Plan，未启动正文或Word/PDF修订；下文保留原交付轮次契约，不因新增路由重启旧任务或追认旧稿满足新要求。当前增量与下文冲突时以修订Spec及最新主Skill为准。

## Goal and Scope

完成[本轮Spec](../specs/ch01-03-review.spec.md)的横向教学审校、必要内容修订及对应正式交付。Parent是唯一writer与最终裁决者；历史章节、工程机制、模板及第四章以后不在修改范围。

## Milestones

### 1. Bind Current Editions and Independent Reading

核对实际Word/PDF与Markdown、原提纲/样稿、当前章契约及必要旧审校。保存文件哈希与foreign dirty清单到`materials/ch01-03-review/`。Kimi受管只读检查跨章专业机制/知识依赖；Native独立角色分别检查教学体验和全书一致性，范围分开。不给作者预判或其他审校者意见。冻结审校源直到receipt核验完成。

### 2. Adjudicate and Apply Bounded Repairs

Parent通读与核对关键证据，逐项裁决；新完整稿存`manuscripts/ch01-03-review/ch01.md`等，精确diff保留。只修改证据充分的问题及直接依赖的答案/图/引用。复算受影响示例，实际独立复查新快照与修改上下文，不将局部复查称为重读全书。保留合理的教学复现。

### 3. Verify and Deliver Current Products

复用原章适配器与Bundled LibreOffice生成`output/ch01-03-review/`Word/PDF，不用桌面LibreOffice。完成正文/数值/图文/编号/目录核对与逐页实际检查，既有页面继承只限相同PNG字节。`python3 -m unittest discover -s tests -v`及`python3 scripts/harness.py validate`核对工程健康，沿既有CLI登记修订章。简明报告、目的记录、保护检查与owned files提交构成停止点，不启动第四章。

## Self-Review

七项方向覆盖于独立阅读和Parent裁决；修订、复查、正式排版与当前证据存在明确依赖。无微步骤、额外审批、worktree或重复工程review。实现review按稳定候选的风险判断另行记录，不与教学独立审校混同。
