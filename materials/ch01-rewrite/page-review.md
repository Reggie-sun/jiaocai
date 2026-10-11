# Chapter 1 Page Review

## Binding

当前正文SHA 9a741d30cc9e6bf04e2bbf0d6c2ab5597a753f03ce190c1fda95cdd2e4c664ec，Word SHA fcf0d2a20c601b51a3830168377681c8812808911a086080e92b42924a893654，交付PDF `output/ch01/第一章-计算思维.pdf` SHA 9cc42db1a774d9c527273c1223740495cf55576ec9ad0d41c5736e5df00b164b，79页。`page-review.json`保存全部最终页图哈希；三个delta文件保留逐次变化链。bundle renderer 110dpi实际页图阅读，非缩略拼图，非仅文字抽取。

## Actual Viewing

Parent逐张view_image original查看render-final第1—29页，检查中文/西文、表格、符号、代码、题注、页码与长链接。两名独立native reviewer_high：layout_pages_30_54实际查看30—54页；31/32/34/35页与此前实际看过的候选页SHA完全相同，复用其观察，其余21页重新看；layout_pages_55_78实际重新查看55—79页全部25页。初始79页观察finding集除第9页编号断行外为空。

最终排版修正仅修改编号显示：保留原生SEQ/REF，caption bookmark只包含编号，正文图/表前缀用不换行空格连接，正文内容不变。render-release与已查看render-final比较，16页像素改变，其余63页逐字节一致。Parent实际重新查看5/9/11/15/16/20/21/22/23/24/25/29页；前一reviewer实际重新查看36/39页，后一reviewer实际重新查看61/63页，2+2页hash均由Parent对比。全部最终79页有实际看过的相同字节页证据，未以换hash代替查看。

此后图1-7正文引导补编号，仅第52页像素改变，Parent按original实际重新看该页，其他78页字节不变，见`final-guide-page-delta.json`。最后删去反思题的比例提示并为三条DOI补真实查阅日期，仅58/78/79页改变；Parent实际逐张重新查看这三页，反思任务与参考文献均完整可读，其他76页字节不变，见`final-editorial-page-delta.json`。相对最初已查看的render-final，最终共20页改变且全部重新看过，其余59页以相同页图SHA复用观察。当前79页都有对应实际视觉证据。

## Findings and Decisions

- 第9页原来行尾留“表”、次行仅“1-1”；word joiner和书签内不换行空格均未阻止LibreOffice拆分，不宣称成功。改为书签仅含自动编号，前缀和不换行空格置于REF外后，实际看到“表 1-1”完整在同一行。
- 32页三张数据表完整；36/40/53页图、题注、来源同页，46页原生分式完整，54页E04表无裁切。
- 55页观察/能耗数据表完整；57页量规完整；61页插图与题注同页，回顾有正文；63页术语和E01标题/引导可读。
- 69/70页E03安排和逐项检查、72页数值表、77页综合训练安排完整。78—79页十项参考文献与URL全部可读，未越出版心。
- 2页学习路线之后留白为前置目录分隔；60/65/76页留白对应后续完整图表，实际未见遗漏，不列blocking。当前26表均未跨页；配置重复表头/禁止行拆分经XML检查，不能声称真实看到了续表头。
- 代码完整，中文和主西文字体为Noto家族，少量数学/特殊符号有已嵌入Liberation/DejaVu fallback，实际符号/公式可读，详细字符见layout-complete.json；不是缺字。

## Limits

这是真实页面AI视觉检查，非真实教师/学生、纸张印刷或出版社验收。Word保留原生可更新TOC/PAGEREF，目录缓存按实际PDF页码回填后再次验证；bundled LibreOffice不重建TOC/PAGEREF，未执行Microsoft Word原生更新。后续改变正文或Word分页须重新生成目录缓存并检查受影响页面。页面PNG是内部QA中间件，哈希与复现步骤保留，交付以绑定的DOCX/PDF为准。
