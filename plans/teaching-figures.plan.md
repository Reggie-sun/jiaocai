# Teaching Figure Capability Implementation Plan

## Goal and Contracts

实现[绘图能力 Spec](../specs/teaching-figures.spec.md)。保持教学方法 owner、`textbook-style-v1.0`、原 Harness 接口和已交付第一章不变；Parent 负责集成与候选，独立 researcher 只调查上游，受管 Kimi 只核验有限语义材料。

## Major Milestones

| Milestone | Files and outcome | Verification |
| --- | --- | --- |
| M1 Research | `materials/teaching-figures-pilot/upstream-research.md`：固定源版本、依赖、MIT、社区信号与局限；明确不采用付费 schematics | 一手 README、实际脚本、许可证；不把 stars 视为教材质量证据 |
| M2 Integrate | 选中两个上游 Skill、本机必要运行依赖及主 Skill 薄路由；具体使用参考下沉 `references/teaching-figures.md` | 入口/许可证/本地依赖可读；固定版本、离线生成与上游检查可执行 |
| M3 Pilot | 两幅新图、原始分钟/关系数据、可编辑源、PNG/SVG/PDF与相同155 mm宽度的独立Word/PDF对照样张 | 全部边/容量及区间独立复算；实际看图、灰度和每页排版，不覆盖原图 |
| M4 Deliver | 比较报告、保护哈希、运行/审校记录、目的记录增量和 owned commit | Harness validate/status、目标检查、最终 diff；后续章复用与未验收范围明确 |

## Boundaries and Recovery

主线程在 current working tree 执行，不建 worktree，不处理第二章的在途产物。研究 agent read-only，由 Parent 保存结果。生成导出失败时调查本地依赖/日志并有限修复；不回退付费 API。Kimi 遵守 sealed contract、canonical receipt 和故障 fallback；其 text QA 不代替图片/页面检查。图案若不改善教学判断则如实报告，不机械追求不同外观。

## Self-Review

四个里程碑覆盖安装、路由、两类图、准确性、编辑性、实际页面与提交；没有微步骤或新增治理。候选独立保留允许自然回退；原章全部文件以哈希保护，现有第二章不归本任务 ownership。
