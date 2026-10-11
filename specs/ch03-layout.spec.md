# Chapter 3 Illustrated Edition Specification

## Goal and Scope

按2026年10月12日用户“五幅图、Word/PDF”的授权，将第三章文字稿交付为五图完整Markdown、可编辑Word和同版PDF。原文字稿`manuscripts/ch03/ch03.md`及原审校、Spec/plan保留；新稿另存`manuscripts/ch03-layout/ch03.md`。继承`textbook-style-v1.0`、原DOTX和主Skill，不改章题、三节题、六项练习、集中答案与九项书目。

## Figure Contract

沿用`materials/ch03/figures.md`五项计划。图3-1显示领域条件、表示与评价如何相互影响，学科不是互斥部门；图3-2分开操作、指令、设备执行与确认返回，先授权，不把未知画成成功；图3-3采用表3-6组A/组B数据，误报率/漏报率各自以实际负类/正类2条为分母，整体错误以4条为分母，不混用E03数据；图3-4连接主张、来源、推理及影响对象，并显示修正/待调查/暂停入口；图3-5采用E05中A/B与C/D原8小时、需要6/5小时加0.5小时额外照明，统一减少3小时后只剩5小时，四室均违反需要。全部为原创教学示意，不是产品接口、实测效果或真实历史研发记录。

每图保留可编辑SVG、2400px彩图与灰度PNG、数据/源脚本、图题/来源/说明。155mm插入时至少300ppi、最小10.5pt文字及0.5pt线条；白底深色，强调色`#1F4E79`，中文`Noto Sans CJK SC`，编号不烘焙进图。正文增加读图、图片、图题和来源块；原3.1.3唯一一处“图3-1（规划）/尚待后期制作”说明转为成图读图说明并单独登记。移除新增块、逆向恢复该状态措辞后必须与已审校文字逐字节一致；其余正文、练习与答案保持。

## Ownership and Format

图稿writer只写`assets/figures/ch03-layout/`、`materials/ch03-layout/render_figures.py`、`figure-data.json`、`figure-manifest.json`及`figure-export.json`。Parent拥有其余新增`materials/ch03-layout/`、`manuscripts/ch03-layout/`、`output/ch03-layout/`、本Spec/对应Plan与最后的目的记录和新Harness登记。writer结束后Parent才接管图稿修订；不修改前两章、旧第三章、模板、共享规则或引擎。各writer路径不相交，无worktree。

Word从原DOTX复制并复用命名样式、三线表、SEQ/REF、TOC/PAGEREF/PAGE。bundled runtime已在前轮解析，本轮核对`runtime.json`及实际路径版本后复用；不调用桌面LibreOffice。目录页码依据最终PDF核对并缓存，不称为Microsoft Word原生更新验证。

## Verification and Acceptance

实际查看全部五彩图和灰度稿，数据/关系/条件独立复核；受管Kimi只读检查新增图义与文字编码，不冒称像素阅读。实际查看最终每页PNG；修改后重看变化页，只有PNG字节一致区间可继承观察。Word/PDF核对全部表格、五图、字体嵌入、页码、目录、引用和答案定位。继承原专业/教学审校仅限逐字节相同文字，新增图块另审。

原Harness登记新`chapter/draft` run，执行当前check、五维Parent汇总`ai_self`审校及accept，不复用旧章的通过或修改门槛。完整稿及正式排版为自然停止点；真实教师/学生、课堂、实体打印、Microsoft Word原生更新和校方/出版社审定不冒称完成。最后更新进度、保护检查、仅提交本轮owned文件并push核验远端。

## Self Review

五图与原计划和实际题表对应，文字保留、图义、排版、可编辑性、证据范围与交付明确。任务授权包含图与两种文档，直接执行，无正文重写或额外审批点。
