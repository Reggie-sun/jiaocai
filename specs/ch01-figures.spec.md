# Chapter 1 Teaching Figure Edition

## Authorization and Goal

用户最新要求“你把第一章的图也改了”授权将新绘图能力用于第一章全部八图，并交付实际更新后的整章Word/PDF。前一轮pilot-only边界不限制本轮。保留上一版，图形改进必须帮助读者判断，不能只改颜色。

## Scope and Owners

新编辑源/图片为`assets/figures/ch01-figures/`，任务脚本/语义和页面证据为`materials/ch01-figures/`，图路径更新后的完整稿为`manuscripts/ch01-figures/ch01.md`，正式输出为`output/ch01/第一章-计算思维-教学图新版.docx`及PDF。旧`ch01-rewrite`源/图/输出与pilot保留。新chapter/draft run沿用Harness登记、check、五项review及accept；不修改引擎、schema、主Skill或共用格式，不处理第二章在途文件。

## Invariants and Figure Contracts

章节文字、26表、E01—E05数据/任务/答案、引用、图号、正式图题和来源不变，稿件只改八处图片路径。原生SEQ/REF、目录/页码与`textbook-style-v1.0`保持，实际分页后更新目录缓存并检查。插图155 mm下中文≥10.5 pt、位图≥300 ppi、灰度可辨，保留可编辑源和本地生成方法。

| Figure | Teaching contract and direction |
| --- | --- |
| 1-1 | 从口头要求找到对象/检查；硬约束、偏好及待确认价值分开，需求分解/对应表达 |
| 1-2 | 六条允许边、孤立d、容量1和3对2瓶颈；采用已验证二分图/数量对照 |
| 1-3 | 错误证据分别定位选择、表示、条件；三类不是固定执行顺序，修改后重新检查 |
| 1-4 | 1937图灵出版、1971Papert/Solomon、2006Wing、2010Cuny/Snyder/Wing；1936收稿/宣读单独说明，无影响/因果箭头 |
| 1-5 | 请求—资源时段与唯一占用的结构可对应；容量、设施、资源身份须重新核查，不暗示全部解等价 |
| 1-6 | 三例共同分钟尺度、半开端点、独占准备/清理，交集60/0/35分钟；采用已验证时间图 |
| 1-7 | 六视角围绕同一问题提出不同证据；并列互补，不是互斥分类、固定步骤或量化占比 |
| 1-8 | 模型内检查与现实证据分别限制结论，可反馈但不能相互代替验收 |

## Acceptance and Verification

八幅图实际查看并有独立图意/阅读检查；图文语义与旧章对应，数值/日期/关系直接核验。实际渲染新版整章、检查所有页面，必要时依据完全相同的页图hash复用已真实查看页面；不能用缩略图或机器检查冒充逐页阅读。所有图题/正文REF、表格、字体、目录和页码核对，实际内容review绑定稳定完整快照。课堂试读、纸张打印、Microsoft Word原生更新及出版社审定仍未完成。

## Self-Review

八图契约均可在现有内容及本地工具实现，图2/6复用真实已验证结果；正文不重写以避免扩大范围。历史证据保留，新版章有自己的真实运行，不把旧hash改成新验收。付费绘图API不调用，Kimi按standing授权只作受管只读语义QA。
