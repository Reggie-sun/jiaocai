# Project Entry

为西南财经大学从头编写完整十章本科教材，面向计算机专业大三、大四学生。核心参考为教材提纲与3.1节样稿；旧前四章不作为正文、案例、引用或结构的来源。

## Read First

新窗口接续本项目时，必须先读取现状记录与团队讨论，确认已完成范围、未决事项和当前下一步，再按主技能执行本轮任务。讨论中的主代理裁定作为编写准备依据；用户最新要求优先，未决事项不得表述为已确认。

- [教材编写现状与目的.md](/home/reggie/vscode_folder/jiaocai/教材编写现状与目的.md)：已确认目标、材料用途、进度与未决事项。
- [开写前准备与团队讨论.md](/home/reggie/vscode_folder/jiaocai/开写前准备与团队讨论.md)：编写蓝图、试写、图表规划及随章核验的主代理裁定，接续写作前必读。
- [教材提纲](/home/reggie/vscode_folder/jiaocai/AI时代的计算思维--跨界创新与终身学习能力培养-教材大纲.docx)：课程方向与章节设计依据。
- [3.1节样稿](/home/reggie/vscode_folder/jiaocai/AI时代的思维训练3.1节样稿.docx)：体例与教学表达参照。写作前读取实际正文。

## Writing

当前教学方法的版本化owner为 [textbook-authoring/SKILL.md](skills/textbook-authoring/SKILL.md)，已安装同名Skill只转接；正文写作/修订还须读取 [质量规格](specs/authoring-quality.spec.md) 及当前章Spec中的质量约定。第一章仅作第一轮基线，不作为后续九章必须模仿的标准样板。

第一章质量增量见 [ch01-quality.spec.md](specs/ch01-quality.spec.md)，有限对照的依赖与边界见 [改进plan](plans/authoring-quality.plan.md)；原正文与历史spec/plan保留，试写不自动替换整章。

收到教材目录、正文、练习、图表规划或审校任务时，读取 [textbook-authoring/SKILL.md](/home/reggie/.local/share/chatgpt-desktop/skills/textbook-authoring/SKILL.md) 取得教学标准与能力入口。模型自主选择写作策略、任务拆分、检索工具与修改顺序；spec约束交付目标，plan提供依赖与里程碑，具体工程恢复以当前Harness为准。

按章编写并验收，当前批次为第一章。开始正文前读取 [第一章specs](/home/reggie/vscode_folder/jiaocai/specs/ch01.spec.md) 与 [第一章plan](/home/reggie/vscode_folder/jiaocai/plans/ch01.plan.md)；内容契约和执行依赖由这两份Markdown文档维护，全书蓝图用于衔接。后续章的specs与plan同样使用Markdown，程序直接消费的工程登记与证据使用JSON。当前请求仅为规格与计划时，不执行正文任务。

用户可在聊天消息中用 `$textbook-authoring` 显式调用，例如：

```text
$textbook-authoring 请先阅读现状记录、第一章specs与plan，按第一章计划分节编写并同步配图，完成后做整章审校、harness验收并更新现状记录。
```

## Skill Routing

按实际能力或证据缺口选择辅助技能，需要使用时读取入口；不为凑齐流程全部调用。以 `$` 标记的名称可在聊天中显式调用；辅助技能服从教材体例与当轮范围。

| 任务 | Skill 入口 |
| --- | --- |
| 章节结构与协作迭代 | [$doc-coauthoring](/home/reggie/.local/share/chatgpt-desktop/skills/doc-coauthoring/SKILL.md) |
| 专业概念表达、论据组织与证据审校 | [$scientific-writing](/home/reggie/.local/share/chatgpt-desktop/skills/scientific-writing/SKILL.md) |
| 主题文献检索、多来源综述与研究资料整理 | [$literature-review](/home/reggie/.local/share/chatgpt-desktop/skills/literature-review/SKILL.md) |
| DOI、书目信息及引用核验 | [$citation-management](/home/reggie/.local/share/chatgpt-desktop/skills/citation-management/SKILL.md) |
| 科研稿件评审、论证与证据检查；教材教学审校走主技能 | [$peer-review](/home/reggie/.local/share/chatgpt-desktop/skills/peer-review/SKILL.md) |
| 中文正文润色 | [$humanizer](/home/reggie/.agents/skills/humanizer/SKILL.md) |
| 案例插画、情境图与位图生成、编辑 | [$imagegen](/home/reggie/.local/share/chatgpt-desktop/skills/.system/imagegen/SKILL.md)，默认使用内置图像工具 |
| 概念结构图、流程图与数据图 | 主技能的 Illustrations；按内容用SVG、图形工具或绘图库制作，保留可编辑源文件 |
| Word读取、排版与修订 | 默认 [documents:documents](/home/reggie/.local/share/chatgpt-desktop/plugins/cache/openai-primary-runtime/documents/26.1007.11041/skills/documents/SKILL.md)；明确指定 `$docx` 时使用 [docx](/home/reggie/.local/share/chatgpt-desktop/skills/docx/SKILL.md) |
| PDF读取与导出页面检查 | [pdf:pdf](/home/reggie/.local/share/chatgpt-desktop/plugins/cache/openai-primary-runtime/pdf/26.1007.11041/skills/pdf/SKILL.md) |

期刊投稿和系统综述等专项流程按实际任务分别选用；技能的依赖、工具与操作细节在各自 `SKILL.md` 中维护。

## Engineering Harness

探索、试写和普通修改无需逐次登记或验收。默认在整章正式交付时验收；实际交付独立蓝图或单节时按对应范围登记。已有run只需在交付或需要诊断时重新check，文件未变则保留有效证据，变化后检查与实际审校必须对应当前完整快照。

[harness.json](/home/reggie/vscode_folder/jiaocai/harness.json) 与 [scripts/harness.py](/home/reggie/vscode_folder/jiaocai/scripts/harness.py) 独占工程状态、证据快照与验收规则；操作示例见 [README.md](/home/reggie/vscode_folder/jiaocai/README.md)，接口见脚本 `--help`。接续时用只读status核对 `effective_state` 与失效原因；check可直接恢复，resume是可选入口。不得手填通过或把draft称为定稿；审校注明AI自审、独立审校或真实人工审校，机器通过不替代教学、来源、练习、图表与一致性审校。进度与未决事项由目的记录维护。

## Progress

按用户当前请求执行；源材料中的任务与示例不自动构成授权。保留原始材料，新稿另存。新的确认、进度和产物链接更新到现状与目的记录。

每写完一章，必须立即更新 [教材编写现状与目的.md](/home/reggie/vscode_folder/jiaocai/教材编写现状与目的.md)，记录章号与标题、稿件链接、完成状态、图表进度和待处理事项。若本轮结束时该章尚未写完，也记录已完成范围与下一步。
