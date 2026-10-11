# Teaching Figure Capability Specification

## Goal and Authorization

用户授权检查开源 Skills、安装必要本地能力、建立教材薄路由，并用第一章两种图独立验证。Parent 自审后执行；付费绘图 API 未获授权。教材的视觉编码应服务学生判断，而不是把每种内容转成矩形流程框图。

## Scope and Owners

- `skills/textbook-authoring/SKILL.md` 保持教学与格式 owner，只补选择与核验入口。
- `skills/drawio-skill/`、`skills/scientific-visualization/` 保存选中的上游固定版本与许可证；`skills/textbook-authoring/references/teaching-figures.md` 维护教材适配说明，不复制上游工具手册。
- `assets/figures/teaching-pilot/` 保存两个独立候选的编辑源、图片和描述；`materials/teaching-figures-pilot/` 保存调研、生成器、数据、比较和检查；`output/teaching-figures-pilot/` 保存实际排版候选。
- 使用原 SDD、Multi-Agent、Harness 与 `textbook-style-v1.0`，不扩展 Harness/schema/阶段。

## Behavior and Invariants

图形选择以教学问题、关系性质、数量/时间编码和读者误解为依据。概念图可用集合、层次、网络、映射或对照；算法可用状态轨迹、递归树、伪代码联动或流程；系统用分层、组件和数据流；数据用共同尺度和明确单位；情境插画用已有 imagegen，精确文字/公式/关系在可编辑层保留。没有图形收益时保留表或正文。

原始数据、公式、边集合和条件必须能核验。区分实例与普遍结论；不能以几何检查或模型审美分数证明图意。中文、灰度、实际插入尺寸和正式题注沿用共用体例；保留编辑源与本地生成命令，不覆盖第一章正式稿或第二章在途文件。

## Pilot Acceptance

从最新第一章图1-2和图1-6取样。图1-2保存全部六条允许关系与孤立 d，用二分关系及位置容量帮助区分局部非空/整体无解；图1-6按分钟在共同时间尺度上区分重叠、半开区间相接及准备/清理后的冲突。保留原图对照，不自动替换正文。

必须实际查看两幅候选、灰度预览、与原图相同宽度的教材试排页面。比较教学表达、视觉清晰、中文可读和编辑成本，允许持平或退步，不以颜色变化作为改善。报告 AI 自审/独立意见与真实教师学生验收的边界。

## Verification and Self-Review

运行选中上游的结构/元数据检查，直接复算瓶颈和区间，检查源/成图/排版对应性及原章保护哈希；核对现有 Harness validate/status，不为非完整节试图建立教材 run。Parent 拥有工具选择、关键结论核验、最终 diff、风险判断和提交。后续章直接复用能力，新增内容仍须按其教学目标制作和审校。
