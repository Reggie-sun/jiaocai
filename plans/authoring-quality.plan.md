# Authoring Quality Implementation Plan

## Goal and Scope

实现[Authoring Quality Specification](../specs/authoring-quality.spec.md) Q1—Q6。Native Codex保持primary及唯一写入、裁决owner；受管Kimi做只读原稿诊断，独立研究提供一手依据，当前样本完成后再分配内容比较。代理之间不重复同一职责，也不接管验收。

## Contracts

原稿和历史证据不可覆盖；本轮样本独立存储，主Skill是教学方法唯一owner，章Spec只表达本章知识增量。Harness五项审校接口与状态机不变。已完成的工程验收是基线draft证据，不证明新增质量已达标。篇幅、来源、图、练习条件保留；不能为某种分析形式强迫每节套同样模板。

## Milestones

| ID | 成果与文件 | 依赖 | Verification |
| --- | --- | --- | --- |
| M1 | 原稿、Skill、Spec、真实审校scope诊断；`materials/quality-pilot/diagnosis.*`与一手依据笔记 | 读取当前规则与status | 核对原文、canonical receipt和真实Read，不继承旧PASS |
| M2 | 版本化`skills/textbook-authoring/SKILL.md`及安装转接入口；`specs/ch01-quality.spec.md`、AGENTS路由 | M1；冻结诊断文件在receipt结束前不改 | Skill校验、入口一致；Spec自审读者、深度、增量及原要求保留 |
| M3 | 原稿1.1.3与1.3.2两个功能的试写；`manuscripts/ch01-quality-pilot/`与材料 | M2；对照前核对教学依据 | 保留原段、原图；新示例复算，真实案例核对原始报告；记录篇幅及取舍 |
| M4 | 独立专业内容比较与独立教学阅读比较、Parent裁决；`materials/quality-pilot/` | 当前M3快照 | 版本中性标记、不向审校者给期待结论；可报告持平/退步；实质修复重新核算、绑定新快照复查 |
| M5 | 工程验证、基线不变、最新进度及仅owned内容commit | M4 | 测试、status、最终diff与提交范围；公开样本外及真实课堂限制 |

## Review and Stop Conditions

内容审校不同于Implementation Review Risk Gate：本轮用户明确要求验证教材生成与审校范式，因此实际内容比较属于产品验收证据，不据此追加重复工程review。默认一轮独立比较、至多两轮有明确理由的内容修复复查；保留原轮次与失败receipt，不未知重试。超预算或独立route真实阻断时记录未完成，不伪造质量通过。全章扩写不属于当前停止条件。

审校发现按具体学生影响裁决，确认为当前范围的关键缺陷先修正；持平或退步如实保留。无证据的偏好不构成强制改写；Parent核对关键判断、数值及来源。机械测试、AI评价与真实人类教学效果分开报告。

## Self-Review

M1覆盖Q4基线与诊断，M2覆盖Q1—Q3，M3/M4覆盖Q4/Q5，M5覆盖Q6。原资料与原章不变；无额外工具安装、分支/worktree、引擎schema或主观quality gate。两片段同时包含一个具体机制分析和一个迁移分析，足以检查范式能否改变正文，但不能证明长期稳定产出。规格实际SHA-256在`materials/quality-pilot/snapshot.json`绑定；产物状态由实测记录及进度维护。
