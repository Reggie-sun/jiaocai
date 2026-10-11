# Chapter 1 Illustrated Historical Edition Specification

## Goal

按2026年10月12日用户“出图、Word/PDF排版”的授权，为历史回顾版第一章制作七幅教学图，生成完整可编辑Word与同版PDF并完成真实页面检查。原章题和四节题保持，正文以已审校的`manuscripts/ch01-history/ch01.md`为基线；旧稿、图、输出和历史证据保留。

## Scope and Ownership

新增`manuscripts/ch01-history-layout/`、`materials/ch01-history-layout/`、`assets/figures/ch01-history-layout/`、`output/ch01-history-layout/`及本Spec/对应Plan。Parent负责图文组装、排版适配、验收和进度；图稿writer仅负责新图资产、绘图脚本、数据和清单，其余文件不得修改。共享目的记录和Harness只在无同文件writer/dirty冲突时顺序更新。第二章及其未跟踪资料不属本轮。

## Content and Figure Contract

七图采用`materials/ch01-history/figures.md`的语义、位置与图号，新增真实图题、来源、描述和正文引用。基线正文、E01—E09、答案和九项引用保持；通过去除本轮插入图块后的逐字节比较证明继承范围。新增文字仅用于读图和引用，不增加史实或教学门槛。

图1-1表达目录/卡片/原文/判断的不同层次；图1-2对照同一目标的纸卡、表格、程序；图1-3区分历史问题、贡献与限制，1936/1937分开，位置不表示等时或因果；图1-4分清理想几何、指令轨迹、真实移动三类证据；图1-5原格1001/0110/0110/1001与E05变更第三行0010一一对应，仅第3行第2列改变；图1-6迁移不画成完全同构；图1-7四种视角无高低排序。全部为原创教学示意，历史信息沿用已核验来源，不冒充历史实物复原。

## Format Contract

直接引用`skills/textbook-authoring/SKILL.md`的`Formal Textbook Style`、`textbook-style-v1.0`与`templates/textbook-style-v1.0.dotx`。模板保留原字节。SVG保留可编辑文字/形状，彩图与灰度PNG在155mm插入尺寸达到300ppi，图内文字至少10.5pt、线至少0.5pt，标题与来源置于图外。正文、目录、题注、表格、答案和参考文献使用模板命名样式；图表使用原生SEQ/REF，目录TOC/PAGEREF和页码PAGE保留。

## Verification and Acceptance

图稿数据/文字与正文逐项核对，实际查看七彩图/灰度效果；受管Kimi只读检查图的教学语义和编码关系，视觉观察单独以实际图片/页面读取为证。Word/PDF逐项核对正文、表格、图号、书签、字段、字体、页码及目录缓存。最终每页PNG实际查看，修订后重看变化页，只有相同PNG哈希可继承观察。未执行的Word原生更新、实体打印和教师/学生学习效果明确保留边界。

新完整章按原Harness的`chapter/draft`登记、check、五维内容review和accept；证据对应当前完整文件快照，不降低门槛或改引擎。Parent进行最终diff/保护文件核验，仅提交本轮文件和授权共享更新。

## Self Review

任务仅把已完成文字稿推进到用户明确要求的图文与正式排版阶段。无正文重写、标题变更、第二章工作、模板/引擎重构或出版验收。范围明确且可逆，按已有授权直接执行。
