# Chapter 3 Figures and Typesetting Plan

## Goal and Contracts

执行`specs/ch03-layout.spec.md`，复用已验证模板与本地导出方式，完整交付五图、Word/PDF。Native Codex为主流程，`superpowers:writing-plans`只提供计划纪律；不改已审文字或共享引擎，不创建worktree。

## Milestones and Ownership

1. Parent固定开工哈希与dirty边界，读取原文字及图计划，复用现有模板/字段/表格适配。图稿writer精确拥有Spec中的五类路径，其余新增材料及共享记录由Parent拥有。所有agents无nested delegation，不stage或commit。
2. 图稿writer实现五图、源数据和彩图/灰度导出，验证字号/线宽/ppi及数据。Parent完成图文组装，更新唯一图3-1规划状态说明；移除新增块并逆向恢复该状态措辞后证明与原文字逐字节一致，其他正文/题解不变；实际看全部图。
3. Parent用bundled文档runtime复用原DOTX构建、渲染完整Word/PDF，核对实际目录页码与所有表格/图/字段/字体。新适配仅在本轮目录，原适配器及模板不改。
4. 五图稳定后封存Kimi图义只读审校，范围为图源、相关正文及新增块。Parent裁决，语义修正需实际定向复查，初审加最多两次。Native只读页面QA负责后半页，Parent负责前半页并核对关键图页；最终全页都实际查看，变化页重看。
5. 完成相关数值、排版、保护与原51项Harness测试；稳定candidate判断工程Risk Gate。新增章级run执行check/review/accept、顺序追加目的记录。仅stage本轮具体路径、commit/push并核验remote SHA。

## Verification and Completion

五图ready且可编辑、原文字完全保留、12表/6答案/9书目对应、Word/PDF页面一致且全页实际查看、新run有效accepted、没有未解决blocking；所有真实验收限制如实保留。Kimi封存期间不修改其frozen集合，未知/截断结果不自动重试。源/彩图/灰度、字段、页面和章节验收是不同证据，不相互替代。

## Self Review

以上milestones覆盖Spec全部交付与证据，职责互斥，复用现有pattern，没有模板/引擎重构或新审批。当前repo无专用session-record/capture入口，最终report与目的记录承担交接，不更新全局memory。
