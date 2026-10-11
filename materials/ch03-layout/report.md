# Chapter 3 Figures and Document Delivery

## Deliverables

本轮按用户“五幅图、Word/PDF”制作第三章图文排版稿：

- [可编辑Word](../../output/ch03-layout/第三章-计算思维与人工智能素养.docx)
- [78页同版PDF](../../output/ch03-layout/第三章-计算思维与人工智能素养.pdf)
- [五幅教学图打包](../../output/ch03-layout/第三章-五幅教学图.zip)：五SVG、五2400px彩图、五灰度PNG及源数据和说明。
- [图文Markdown](../../manuscripts/ch03-layout/ch03.md)、[Spec](../../specs/ch03-layout.spec.md)、[Plan](../../plans/ch03-layout.plan.md)。

PDF SHA256为`9383a5ad709ddf8cff6bd29501a58bb5862700980f0472f265dc049b4a039366`，Word为`f1e2bd9d4c4cb5f380260ebfc1f6ea268c2fb59ac816453c7c5b0b283479be8f`。交付件和页面存档的完整哈希见`package-check.json`，源图哈希与成图状态见`figure-manifest.json`。

## Text and Figure Fidelity

保留原`manuscripts/ch03/ch03.md`以及全部原章审校和练习核验。图文稿增加五个读图/图片/图题/来源块，原3.1.3的“图3-1（规划）/尚待后期制作”仅更新为成图状态。撤销这些声明的增量后，与原章SHA256 `38d90d7a397ba98f0279055838bf4aace2cd76cddf684001609cee748e719709`逐字节相同。当前图文Markdown约36,550汉字；三节、12表、六项练习/集中答案、九项书目均保留。

原专业/教学独立审校与38项练习核验仅继承到相同字节的原文，不声称本轮新审校者重读整章。`assembly.json`和`content-inheritance.json`给出边界及原证据哈希。

五图全部为原创教学示意：领域知识与设计链、跨设备指令与确认、表3-6总体/误报/漏报、主张三重核验、E05四教室照明时长。数据逐项对应原表，不混入E03；三种错误比例使用同一0–100%尺度及各自分母；未知状态不写作执行成功；照明轴表示日时长，保留学生对候选方案的判断。

五彩图和五灰度图均实际查看；R2变化的图3-1/3-4又逐幅复看彩图和灰度，其余三图仅在完整字节相同时继承观察。155mm插入约393ppi，最小标签约10.74pt、最小线宽约0.98pt。`figure-check.json`记录数值核验与像素观察，二者互不替代。

## Template and Page Verification

复用原`textbook-style-v1.0.dotx`，未改模板、共享Skill、前两章或原适配器。继承全部样式、镜像页边距、三线表及原生SEQ/REF/TOC/PAGEREF/PAGE；目录缓存按实际PDF核对，不经LibreOffice保存最终DOCX。运行环境及模板package保留约定见`runtime.json`、`artifact.md`、`template-parts.json`。

实际验证全部正文/12表与Word对应、五图嵌入字节/alt说明/宽度、22个引用目标及六个答案书签、八个外部超链接与源URL集合、全部PDF字体嵌入、连续1–78页码、图题与图片同页。八项目录实际页码分别为4、23、41、60、62、63、64、77；五图位于11、14、32、50、59页。最终`layout-final.json`为可执行PASS，目录缓存与实际页码一致。

Parent实际查看r2第1–39页，独立Native reviewer_high实际查看第40–78页。最终相对r2仅11、14、32、49、50、59页变化，全部由Parent实际复看；Native亦复看r4的50/59页和r5的49/50页。其余72页逐PNG完整SHA256相同，才继承既有观察。`page-review.json`记录最终78页覆盖；原r2全页、最终全页及r4定向页面分别保留压缩存档，独立报告保留具体观察和限制。

实际发现并解决`LAY-01`：模板Body的字符首行缩进及inline默认间距使图水平偏出正文区域。只在图段落设置`firstLineChars=0`及四边`wp:inline`距离为0，未修改模板。增强后的实际PDF图像版心检查先拒绝r3，最终r5可执行检查和五图页像素复看均通过。分页与目录未变。

## Reviews and Delivery Gate

受管Kimi的独立图义审读只读SVG文字/几何及相关原文/新增块；PNG视觉、整章教学、Spec approval与最终交付不属于其权限。R1三项发现由Parent裁决并修正：回返到“表示”的箭头、处置标签“修正/待调查”、不再把单向检查图描述为有返回箭头。封存、真实route/identity、实际完整Read及report的核验见各`figure-receipt-check-rN.json`，定向复核与最终裁决见`figure-review.json`。

R2 invocation `3a953c92-8738-44fd-90a6-ef81bb29a475`完整读取八项必读材料及当前Spec/Plan，独立确认三项均解决、未发现新增缺陷。Parent结合真实图稿/图页观察闭合这三项；仍不把PARSED或exit 0当作验收。

本轮已实际运行原51项Harness测试，51通过；引擎未改。工程Implementation Risk Gate的stable snapshot和裁决见`implementation-risk.json`。最终章节工程证据由`runs/ch03-layout.spec.json`、`check.json`、`review.json`及`harness.json`登记拥有；五维Parent汇总声明为`ai_self`，独立图义/页面证据另列，不升级成真实人工审校。只读status用于核对实际有效状态，不由本报告手填通过。

## Reproduction

使用`runtime.json`中已验证bundled Python，依次执行本目录`render_figures.py`、实际像素复查并登记ready、`assemble.py`、`build_docx.py --toc-pages materials/ch03-layout/toc-pages.json`；用documents Skill的`render_docx.py --emit_pdf`导出到新的本地render目录，再执行`verify_layout.py --pdf <实际PDF> --output <新核验JSON>`。分页改变时按新的实际页码更新缓存后重导。`package_outputs.py`只打包已经核验的快照；任何源文/数据/图/分页改变后须重新进行相应审读和Harness检查，不能复用历史哈希为新内容背书。

## Limits and Next Step

交付为完整教材初稿与正式排版文件，验收scope为`chapter/draft`。Microsoft Word原生字段/目录刷新、实体打印、教师/学生试读、课堂试教及校方/出版社审定尚未完成。全页可见排版检查、机器PASS和AI审校均不替代这些真实验收。修改Word分页或更新域后重新核对目录及页面；后续按用户安排开展真实教学审阅或下一章。

原tracked及foreign源文件的840项保护检查，除授权的目的记录追加和新Harness登记外保持原字节，详见`preservation-check.json`。本轮没有repo专用session-record Skill；本报告、审校材料和目的记录提供交接，不写全局memory。
