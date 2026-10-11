# Textbook Style Pilot Plan

## Goal and Scope

按用户最新要求只进行小范围格式试排。第一章仍需后续内容修订，本轮不整理或排版整章，不合入质量试写，不推进第二章。应用既定`textbook-style-v1.0`，生成可复用Word样式模板与约4—8页样张，检查真实页面，提交并push。

格式唯一owner是[主Skill](../skills/textbook-authoring/SKILL.md#formal-textbook-style)。本plan安排验证，不重选或复制全书样式。

## Ownership and Invariants

Parent拥有本轮全部写入及最终裁决。新建`manuscripts/style-pilot/sample.md`作为独立试排源，`materials/style-pilot/`保存生成脚本、样张图源、核验与独立QA证据，`templates/textbook-style-v1.0.dotx`保存共享模板，`output/style-pilot/`保存样张Word/PDF。README只增加入口，现状记录追加本轮范围与限制。

第一章整章和分节、原图、练习数据/答案、质量试写、历史Spec/plan、原始Word、Harness引擎/policy/runs均保持原字节。样张独立连续编号，不能据其编号重写原章清单，不能将其答案搬迁或减表当作原章已实施。采用的题目材料和评价标准留在题目处，可读参考解放在样张末尾。

## Milestones

### M1: Representative Source

从当前新写第一章抽取章首、概念说明与E01数据/任务/答案。用一小段连续正文示范解释性表格的改写，保留数据表；补一个明确标注的跨页表格测试材料。图以原创可编辑结构图实现同一教学用途，独立于原图。引用使用少量已核验的真实来源，格式化前查阅正式`GB/T 7714-2025`相关条款。不宣称所有第一章参考文献已经改完。

### M2: Shared Styles and Rendered Pilot

用已安装的Codex bundled runtime及`python-docx`实现主Skill命名样式、镜像页边距、自动章号/题注/交叉引用/页码/目录和三线表。输出真正的`.dotx`以及样张`.docx`，保留原生域并填入显示结果。使用bundled LibreOffice与主技能renderer导出PDF/页面PNG，核对字体嵌入、图尺寸/清晰度、跨页表头和完整行。模板不附加机械节内栏目。

### M3: Verification and Delivery

逐页打开最新PNG，修复影响阅读的布局问题。进行一次受管Kimi只读QA，读取冻结样张源与生成实现，检查题目/题解对应及样式、域和正文完整性；不要求其接受整章或判断未见页面。Parent核对route/receipt/实际Read并裁决发现，必要时最多两轮有依据的复查。独立内容/结构QA与Parent实际视觉页检分别记录。

可执行检查包括：源数据及E01基线/变体复算；DOCX/DOTX内容类型、域及bookmark完整性、样式/边距/表头/边框；bundled LibreOffice更新域后的编号与交叉引用；PDF字体嵌入及页数/文本/对象边界；保护文件SHA-256未变；现有Harness validate/status。样张不是完整节或章，不建立伪造的Harness run。不修改Harness/tests，因此不重复整套工程测试。

## Acceptance and Limits

交付共用模板、可读样张Word/PDF及可重建源；样张范围内无已知裁切、重叠、题注分离、缺字或表格缺行。参考解位置与题号一致，数据和量规可在题目处获得；自动域与正文引用目标一致。README和现状记录明确：这是小范围试排，第一章仍需修改，原章尚未排版验收，实际Microsoft Word行为和教师/学生阅读效果未由本轮证明。

## Self-Review

已用用户最新的“小范围测试”收窄此前整章实施意图。全部既有章节产物受保护，样式由唯一owner继承；无需整章重新编号、运行登记或增加排版状态。模板及样张都要通过实际渲染，不能只检查XML。受管QA采用只读最小package，生成与页检由Parent完成；这项独立目的不重复通用Implementation Risk Gate。
