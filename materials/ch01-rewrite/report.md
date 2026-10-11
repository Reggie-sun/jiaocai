# Chapter 1 Rewrite and Formal Typesetting

## Delivery

完成第一章《计算思维：从现实问题到可检验的解决过程》的整章重写与正式Word/PDF排版，按`textbook-style-v1.0`交付。范围包括章首、四节、章末综合训练、回顾、术语、E01—E05及集中参考解；没有开始第二章。旧第一章、质量试写、两份原始Word、原Spec/plan、共用模板等57项保护文件保持原哈希。

- [整章正文](../../manuscripts/ch01-rewrite/ch01.md)：35,017汉字，口径为排除代码块与链接目标的近似统计，包含集中题解与文献，不等同于Word或出版社字数。
- [Word](../../output/ch01/第一章-计算思维.docx)与[PDF](../../output/ch01/第一章-计算思维.pdf)：79页，8幅原创教学图、26张表、10条原始或官方来源。
- [整章Spec](../../specs/ch01-rewrite.spec.md)、[implementation plan](../../plans/ch01-rewrite.plan.md)及[可编辑图源/成图清单](../../assets/figures/ch01-rewrite/manifest.json)保留执行契约与素材。

新稿加强问题表示、候选筛选、必要条件与充分判断、失败解释、迁移条件和证据边界。讲解案例与正式练习分开，既保留练习原数据和硬约束，也要求学生产生新的判断。内容组织按学习目标调整，未把第一章旧稿或样张当作统一节内结构。

## Content Review

整章有受管Kimi deep专业初审与复查、独立native reviewer_high教学审校。Parent逐项调查并裁定结论，没有把reviewer verdict直接当验收。专业R1提出的图表导读与体例问题已修复；独立教学审校发现E04可以摘录前文完成，Parent确认该缺陷并否决专业R1对应的过度肯定。

E04使用与练习不同的讲解数据，练习要求提出新的未决判断、竞争解释、区分证据与结果预测。独立教学R2实际读取改稿后关闭TR-01；专业R3独立复算并确认任务、答案、量规和原JSON相符。最后删除辅助反思中的比例答案，由同一教学reviewer对最终SHA实际局部复查，finding为空。

专业R2调用中断为`OUTCOME_UNKNOWN`，没有采用部分输出。恢复判断及第三轮最后一次受管审查另有记录；三轮预算结束。Kimi R3实际读到的正文SHA为`9ea7a7acd3686bc71d3fb9bb445382396f138698dc0b3b9138f13c5094cfcc30`，之后只有五处可追溯编辑微调。最终SHA为`9a741d30cc9e6bf04e2bbf0d6c2ab5597a753f03ce190c1fda95cdd2e4c664ec`；[等价核对](editorial-equivalence.json)证明E04主任务/量规与全体章末参考解逐字节不变，参考元数据仅增加三条真实查阅日期。不宣称Kimi读取了最终字节。

详细证据见[专业裁定](professional-adjudication-r3.md)、[恢复记录](professional-recovery-r2.md)、[教学初审](teaching-review-r1.md)、[教学复查](teaching-review-r2.md)和[最终局部复查](teaching-review-r3.md)。Canonical receipt与worker report按轮保留；`teaching-r2-to-professional-r3.diff`对应教学R2至专业R3，`post-review-editorial.diff`对应专业R3至最终稿。

Parent实际核验10项原始或官方来源的书目、定位与论断边界，包括NASA Mars Climate Orbiter报告；模拟数据、教学综合与来源支持的事实分别标示。Turing日期、Papert/Solomon双署名、2010定义归属、NIST报告作者及引用次序已核对。文献格式参照GB/T 7714-2025实际扫描件的相关页面，不宣称逐条审遍全部标准；十条在线文献统一记录本轮真实查阅日。[来源账本](sources.json)与[格式核对](reference-format-check.json)保留范围。

## Executable and Page Evidence

[数值证据](numeric-proof.json)复算E01原条件12条、变体0条，E03原条件2条、变体0条，E05原条件6条、变体0条；E04原练习能耗14.4/21.6/14.4 kWh及观察比例20%/15%保持，讲解另用7.56/10.08 kWh及10%/15%。这些比例不是因果效应。原练习JSON未修改。

[当前版式核对](layout-complete.json)通过：26表逐项对应正文、8图尺寸与哈希一致，原生SEQ/REF/TOC/PAGEREF/PAGE及书签有效，有可编辑OMML分式；PDF字体嵌入、文字未越出版心、页码连续，目录缓存与实际页面相符。固定模板适配器没有更改共用模板。51项原Harness测试已在本轮实际运行通过，Harness engine和tests未修改。

[页检记录](page-review.md)覆盖全部79页。Parent与两名独立native reviewer_high实际按页查看；编号修正后重新看16个变化页，图引导调整重看第52页，最后编辑重看58/78/79页。其余页面以相同页图SHA复用真实观察；没有用抽取文字、拼图或换绑哈希代替逐页检查。8幅独立PNG也已实际逐张查看。

最终正文SHA、Word SHA及PDF SHA分别为：

```text
9a741d30cc9e6bf04e2bbf0d6c2ab5597a753f03ce190c1fda95cdd2e4c664ec
fcf0d2a20c601b51a3830168377681c8812808911a086080e92b42924a893654
9cc42db1a774d9c527273c1223740495cf55576ec9ad0d41c5736e5df00b164b
```

## Engineering Acceptance

本轮注册`ch01-rewrite`，沿原G11采用`chapter/draft`范围。登记材料包括当前正文、图源与成图、数值/来源证据、独立审校与Parent裁定、Word/PDF、全部页检链及新Spec/plan。`check`、五项内容`review`及`accept`的实际结果由[harness.json](../../harness.json)独占；本报告不手填工程状态。旧`ch01-draft`的有效验收与旧稿保留，历史蓝图run的失效状态不在本轮改写。

Parent在稳定候选完成[Implementation Review Risk Gate](implementation-risk.json)：本地可逆组装/绘图/排版适配没有凭据、权限或生产状态变更，实际对应性检查和页检覆盖其实现风险，未触发额外工程Kimi reviewer。教材内容独立审校已经单独履行。

## Limits and Next Step

这是完整初稿与正式排版交付，不是校方或出版社审定稿。尚未实施真实教师/学生试读、课堂试教、纸张打印与Microsoft Word原生目录更新。Bundled LibreOffice不重建TOC/PAGEREF；当前Word保留原生域，目录缓存以当前PDF实际页码回填并核验。后续在Word改变分页或更新域后须重查目录和受影响页面。

中文及主西文字体为Noto，少量数学/特殊符号使用已嵌入Liberation/DejaVu fallback，实际可读。当前所有表均未跨页；重复表头与禁止拆行已检查XML，但不宣称实际验过跨页续表头。正式课时、校方目录与出版社纸张/装帧要求仍待明确。

下一步为读者与教学场景验收，或按用户新请求进入后续章节。没有自动把本稿升格为出版定稿，也没有自动启动第二章。

## Record Assessment

本轮为substantial implementation、内容重写、审校与排版工作，需要durable记录。Repository没有声明专用session-record/capture Skill；按现有owner更新[现状记录](../../教材编写现状与目的.md)，并以本报告、独立审校/receipt及Harness保存结果。未创建第二套进度owner，也未修改全局memory。
