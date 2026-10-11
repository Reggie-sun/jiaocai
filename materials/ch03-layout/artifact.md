# Textbook Template Execution Contract

## Reference and Runtime

保留`templates/textbook-style-v1.0.dotx`，SHA256 `eef8ce505c3d9afb3493e61af1f38ee26bca6ff9a0aa12f7ad3e2a8cacad6473`。同一模板已在前两章实际渲染并审查；本轮核对哈希，复用同字节模板的设计与package inventory，不重新设计。Parent本轮重看一页原模板截图。当前bundled runtime manifest为26.1009.11318，Python3.12.14、Node24.19.0、headless LibreOffice25.2；路径及无公开dependency-loader接口的事实见`runtime.json`。直接复用已解析runtime，不调用桌面LibreOffice。

## Page System and Styles

直接继承`textbook-style-v1.0`：A4镜像页边距、上/下25mm、内30/外25mm、页眉页脚15mm；Body为Noto Serif CJK SC12pt、1.5倍行距、两端对齐、首行2汉字；章/节/小节18/16/14pt。表格、图表题、来源与文献10.5pt/1.2倍行距，三线表、重复表头和普通行不拆页；图155mm插入。所有样式和设置保持原字节。

## Slots and Preservation

替换模板示例body槽位为完整图文第三章，章号及编号起始为3，节/小节和图/表由原生SEQ计数；页眉缓存改为本章题。增加章内目录TOC/PAGEREF、`fig3_N`/`tbl3_N`书签/REF、六个集中答案`answer_E01`—`answer_E06`；保留PAGE及原settings/updateFields。根据实际PDF核对后缓存目录，不经LibreOffice保存最终DOCX，不声称Microsoft Word原生刷新完成。

可编辑parts为`word/document.xml`、其rels、core metadata、当前header缓存、numbering的章起始override及template→document内容类型；允许新增media。其余模板parts全部preserve-only且逐字节核对，详见`template-parts.json`。标题及原正文不重写；新增图块及原图3-1的规划状态更新单独登记，逆向恢复后核对原文字。

## Fidelity and Shipping Gates

全部原文字/12表逐项对应、五图片源/嵌入字节/alt description和插入宽度一致、SEQ/REF/TOC/PAGE及全部答案目标完整、实际目录页码和字体嵌入核验。最终Word必须实际渲染，同版PDF每页PNG实际查看，发现影响交付的分页/裁切/重叠/缺字先修复；纯XML或脚本PASS不能替代像素查看。当前为AI审校完整教材初稿及正式排版，真实教师/学生、打印、校方和出版社验收另列。
