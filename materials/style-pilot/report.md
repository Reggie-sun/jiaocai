# Textbook Style Pilot

## Scope

按用户最新要求，仅用独立样张测试已经确定的`textbook-style-v1.0`，第一章仍需后续修订。本轮不替换第一章整章/分节、原图、34张原表、练习数据或引用清单，不修改原Spec/plan、原始Word及Harness。全书规则仍由[主Skill](../../skills/textbook-authoring/SKILL.md#formal-textbook-style)独占，后九章直接继承。

样张包含问题导入、少量方法说明、原创重绘图、E01题目/数据/评价标准、独立跨页表格测试记录、章末参考解及两项真实来源。样张编号独立于原章；删减和后移只发生在此副本。跨页测试不是新增教材内容，也不作为练习答案。

## Files and Reuse

- [Word样式模板](../../templates/textbook-style-v1.0.dotx)：真正的DOTX，包含命名样式、页面设置、页眉/页码与章/节标题起点；不固化每节栏目。
- [样张Word](../../output/style-pilot/textbook-style-pilot.docx)及[样张PDF](../../output/style-pilot/textbook-style-pilot.pdf)：同一内容的可编辑文件与页面快照。
- [Markdown源](../../manuscripts/style-pilot/sample.md)、[SVG](fig1-1.svg)/[PNG](fig1-1.png)、[有界生成器](build_sample.py)与[聚焦检查](verify_sample.py)：可重建这份样张，不是完整教材通用导出器。

Word端须安装模板指定的Noto CJK字体。创建新文档时使用DOTX并应用现有样式；复制完整标题/计数器组合（章题后、节题前的隐藏段），保留原生SEQ/REF域和bookmark。章号、节号及图/表各自计数；图表增删后更新全部域并重新导出/查看页面。新章的内容与具体图表宽度按其任务决定，不重新设计全书样式。单独导出后续章时仍须由对应导出实现提供正确章号，不能将这份第一章试排脚本当作十章转换器。

目录使用原生TOC域，本样张限定在`pilot_body`bookmark内、仅显示节标题。当前显示结果的页码通过PDF核对后缓存；bundled LibreOffice未重新生成该目录。实际Microsoft Word中的目录更新仍待验证，不能把缓存显示称为Word更新测试通过。

## Verification

可执行结果见[verification.json](verification.json)，源文件保护哈希见[protected-source-sha256.json](protected-source-sha256.json)。Parent实际页面检查与独立QA范围分别记录，不将XML检查、机器PASS或AI检查称为教师/学生验收。

最终8页与模板预览已实际查看；结构、样式、字体嵌入、短表同页/长表重复表头、普通行完整与原文件保护检查通过。临时副本插入新表后，表号及REF引用同步更新；追加第二章后章号、节号、图/表号重置正确；同章新节的小节号从1开始。E01实际枚举为12条可行安排，D2关闭后0条，参考安排符合全部约束。103项既有保护文件保持原哈希。

一次受管Kimi静态QA完成，receipt/实际Read/产物哈希与qualified live路由均已核验，见[report](qa-worker-report.json)和[receipt](qa-invocation-receipt.json)。Parent确认并补齐表1-4正文编号引用；随后显式计数器重置及断行保护的实现由Parent实际更新域和渲染检查，不宣称Kimi已审过这些新bytes。教学正文与题解语义未变，不重复静态QA；风险判断未触发额外最终工程review。

本轮只运行与样张相关的检查及现有Harness validate/status，不重跑整套Harness测试，也不为非完整章/节的样张建立run。原`ch01-draft`保持既有契约下的accepted chapter/draft；旧蓝图因此前policy/engine变更失效的状态保留。

## Reference Check

正式GB/T 7714-2025的[官方元数据](https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14)及[正式文本扫描件](https://www2.abc.edu.cn/xbbjb/upload/2026-01/26012010262341.pdf)已核对；不是征求意见稿。查阅印刷页4、7—8、11—12、15—16，应用姓名缩写、期刊与报告著录、日期/页码及DOI URL规则，只处理样张两项文献。

Wing原始条目沿用已核验来源；NIST报告作者与2024-07-26发布日期核对[官方出版记录](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)，confabulation支持位置为[报告](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)印刷页6。正式标准扫描文件留在临时核验目录，不复制到仓库。原章九项参考文献尚未按新体例整体修订。

## Rebuild

使用已加载的Codex bundled Python及documents renderer，不调用桌面LibreOffice或另装依赖。下面变量指向本轮实际runtime；其他环境先加载并核对自己的runtime根路径。

```bash
pilot_runtime=/home/reggie/.cache/codex-runtimes/codex-primary-runtime
pilot_python="$pilot_runtime/dependencies/python/bin/python"
pilot_renderer="$pilot_runtime/plugins/openai-primary-runtime/plugins/documents/skills/documents/render_docx.py"
pilot_temp=$(mktemp -d /tmp/jiaocai-style-pilot-XXXXXX)
PYTHONDONTWRITEBYTECODE=1 "$pilot_python" materials/style-pilot/build_sample.py --output-dir "$pilot_temp/build" --template "$pilot_temp/textbook-style-v1.0.dotx"
"$pilot_python" "$pilot_renderer" "$pilot_temp/build/textbook-style-pilot.docx" --output_dir "$pilot_temp/render" --emit_pdf
"$pilot_python" materials/style-pilot/verify_sample.py --docx "$pilot_temp/build/textbook-style-pilot.docx" --make-probe "$pilot_temp/numbering-probe.docx"
"$pilot_python" "$pilot_renderer" "$pilot_temp/numbering-probe.docx" --output_dir "$pilot_temp/probe" --emit_pdf
"$pilot_python" materials/style-pilot/verify_sample.py --docx "$pilot_temp/build/textbook-style-pilot.docx" --pdf "$pilot_temp/render/textbook-style-pilot.pdf" --template "$pilot_temp/textbook-style-v1.0.dotx" --probe-pdf "$pilot_temp/probe/numbering-probe.pdf" --baseline materials/style-pilot/protected-source-sha256.json --output "$pilot_temp/checks.json"
```

## Limits and Next Step

这次只证明样张范围的样式与已实际测试的域行为。Microsoft Word原生执行、真实打印、整章排版、全部原章引用与真实教师/学生阅读尚未验收。后续按明确授权修订第一章内容，再使用共用模板排版；不自动启动整章修订或第二章。
