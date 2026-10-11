# Template Contract

## Reference and Evidence

设计owner为`skills/textbook-authoring/SKILL.md#formal-textbook-style`的`textbook-style-v1.0`，保留模板`templates/textbook-style-v1.0.dotx`。本轮实际只读渲染该DOTX的一页样式起点并查看`/tmp/jiaocai-ch02-template/page-1.png`，检查标题、节/小节、页眉与页脚。原第一章的Word/PDF与样张保留；不把空模板的单页视图当作第二章实际验收。

## Preserve and Allowed Slots

模板一节A4竖向、镜像页边距，正文可用宽155mm；正文与标题、题注、表格、来源、文献、代码均使用模板的已有命名样式。具体字号与段落参数由原模板独占，生成器不重新设计。保留`word/styles.xml`、theme、fontTable、footer、settings与样式关系；删除样例body标题/节/小节起点，填入完整第二章，保留section properties。

必要slot变化：章号numId80的startOverride=2，隐含SEQ Chapter计数从2开始，页眉STYLEREF的缓存章名变为第二章标题；native Section/Subsection/Figure/Table计数、REF、TOC/PAGEREF、PAGE沿用既有机制。六份答案增设定位书签；正文明确带ID的E02/E03/E04定位使用REF，其他三题按当前任务指向章末并以相同ID对应。生成的新document、media及相关relationships可变；不通过LibreOffice另存改写最终DOCX。

## Content and Fidelity

完整章首、目录、五节、综合训练、回顾、术语、集中答案、参考文献按稿件顺序填入。短内容不扩大字号，长内容自然分页，表行不拆开、跨页表头重复；精确图按155mm插入保留原比例及替代文字。全部图表与文字须与最终Markdown/输入数据一致。

`build.json`记录模板、稿件、Word哈希与目录缓存；`verify_layout.py`检查正文/表格覆盖、域/书签、字体、图像清晰度、页面编号和目录实测页码；package fidelity另保存模板保留部分比较。所有实际输出页面必须渲染并逐页查看，允许仅有预期内容流动与本章号码变化。Microsoft Word原生执行未在本机评估，updateFields保留；当前PDF由既有bundled LibreOffice渲染验证。
