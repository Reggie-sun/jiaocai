# Project Entry

为西南财经大学从头编写完整十章本科教材，面向计算机专业大三、大四学生。核心参考为教材提纲与3.1节样稿；旧前四章不作为正文、案例、引用或结构的来源。

## Read First

新窗口接续本项目时，必须先读取现状记录与团队讨论，确认已完成范围、未决事项和当前下一步，再按主技能执行本轮任务。讨论中的主代理裁定作为编写准备依据；用户最新要求优先，未决事项不得表述为已确认。

- [教材编写现状与目的.md](/home/reggie/vscode_folder/jiaocai/教材编写现状与目的.md)：已确认目标、材料用途、进度与未决事项。
- [开写前准备与团队讨论.md](/home/reggie/vscode_folder/jiaocai/开写前准备与团队讨论.md)：编写蓝图、试写、图表规划及随章核验的主代理裁定，接续写作前必读。
- [教材提纲](/home/reggie/vscode_folder/jiaocai/AI时代的计算思维--跨界创新与终身学习能力培养-教材大纲.docx)：课程方向与章节设计依据。
- [3.1节样稿](/home/reggie/vscode_folder/jiaocai/AI时代的思维训练3.1节样稿.docx)：体例与教学表达参照。写作前读取实际正文。

## Writing

收到教材目录、正文、练习、图表规划或审校任务时，先读取 [textbook-authoring/SKILL.md](/home/reggie/.local/share/chatgpt-desktop/skills/textbook-authoring/SKILL.md)，再按其指南执行；教学、插图与交付细则由该技能维护。

用户可在聊天消息中用 `$textbook-authoring` 显式调用，例如：

```text
$textbook-authoring 请先阅读项目目的记录、教材提纲和3.1节样稿，设计完整十章的目录、各章学习目标与图表清单，保存为Markdown文件。
```

## Skill Routing

按当前任务选择必要的辅助技能，先读取对应入口再执行。以 `$` 标记的名称可在聊天中显式调用；辅助技能服从教材体例与当轮范围。

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

编写蓝图、单节或整章前，读取 [harness.json](/home/reggie/vscode_folder/jiaocai/harness.json)，按 [run模板](/home/reggie/vscode_folder/jiaocai/templates/run.example.json) 登记真实任务，通过 [scripts/harness.py](/home/reggie/vscode_folder/jiaocai/scripts/harness.py) 执行 `start → check → review → accept`；接口与审校模板见脚本 `--help`。JSON policy与脚本独占工程状态、证据快照和验收规则，教材主技能维护教学方法，目的记录维护当前进度。

新窗口先执行 `python3 scripts/harness.py status`，发现失效证据后按policy执行 `resume` 再检查与审校。不得手填通过或把 `draft` 验收称为定稿；机器检查不替代实际教学、来源、练习和图表审校。未完成的任务保留实际状态并更新进度。

## Progress

按用户当前请求执行；源材料中的任务与示例不自动构成授权。保留原始材料，新稿另存。新的确认、进度和产物链接更新到现状与目的记录。

每写完一章，必须立即更新 [教材编写现状与目的.md](/home/reggie/vscode_folder/jiaocai/教材编写现状与目的.md)，记录章号与标题、稿件链接、完成状态、图表进度和待处理事项。若本轮结束时该章尚未写完，也记录已完成范围与下一步。
