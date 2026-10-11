# Chapter 1 Teaching Figure Edition

## Delivery

第一章全部八幅教学图已重设计并实际插入完整教材。[新版Word](../../output/ch01/第一章-计算思维-教学图新版.docx)、[新版PDF](../../output/ch01/第一章-计算思维-教学图新版.pdf)共82页，上一版79页及其源稿/图片保留。正文、26表、E01—E05、引用、正式图题与来源不变；[新版源稿](../../manuscripts/ch01-figures/ch01.md)仅更新八处图片路径。正式文件仍采用`textbook-style-v1.0`，本轮章级工程范围为chapter/draft，不升格为出版定稿。

## Product Changes

| Figure | New expression and teaching use | Editing source |
| --- | --- | --- |
| 1-1 | 五行要求—判断类型—检查项对应；硬约束、偏好、待确认分别用矩形、椭圆、虚线表达，可沿一条具体要求核查 | draw.io |
| 1-2 | 真实二分关系图及3对2数量对照；六条允许边完整，孤立d置于瓶颈外，不把候选关系误画为已选安排 | draw.io + exact data |
| 1-3 | 三行证据—失效来源—修改对象的诊断对应；分别处理重复占用、表示不足及穷尽选择无解，避免固定流程读法 | draw.io |
| 1-4 | 真实出版年份的共同尺度；四文献节点分开，2010定义表述标出Cuny/Snyder/Wing，1936收稿/宣读另注，无传承箭头 | SVG + script/data |
| 1-5 | 逐行对齐请求、位置、允许关系和唯一占用，容量/设施筛选单列；资源身份及冲突口径仍须核查 | draw.io |
| 1-6 | 同一分钟尺度的三组区间；半开端点、纹理、独占准备/清理与60/0/35分钟交集可直接读出 | SVG + script/data |
| 1-7 | 六视角环绕同一步道照明问题，列不同提问与证据；辐条无箭头、无权重，不暗示分类互斥或执行顺序 | draw.io |
| 1-8 | 两个并列证据域分别列观察、检查和结论范围；虚线表示观察冲突后的模型修订，独立验收边界明确 | draw.io |

Parent实际查看新版八图和八个插入页，以及旧图1/3/4/5/7/8；旧图2/6的实际对照证据保留在[前轮pilot报告](../teaching-figures-pilot/report.md)。图2/6的关系、区间编码改进最明显；图1/3/5/7/8主要通过对应关系和证据层级提高操作清晰度，仍保留有教学用途的框线。图4从三个同距卡片改为四个真实年份节点，并使定义使用者与文章作者的区别更清楚。这个判断是AI产品审阅，不是学生学习增益的实证。

## Local Tools and Reproducibility

复用已固定版本的`drawio-skill`、`scientific-visualization`及主Skill薄路由，没有再次安装或改造Harness。结构关系使用官方draw.io 32.4.1；时间数据与年份使用本地Matplotlib。图形编辑源、PNG/SVG/PDF、灰度版与尺寸/hash见[manifest](../../assets/figures/ch01-figures/manifest.json)。本轮未调用付费绘图API；受管Kimi只用于standing授权的语义调查。

同版本环境重建八图到新目录：

```bash
PYTHONDONTWRITEBYTECODE=1 /home/reggie/miniconda3/bin/python \
  materials/ch01-figures/rebuild_figures.py --output-dir /tmp/ch01-figures-rebuild
```

生成器直接复用前轮已验证的图2/6绘制函数，但读取本轮data.json并输出到指定目录，原pilot不会被覆盖。关系图按整页导出，修正后的图3按内容边界导出；曾发现默认裁内容与整页导出不能混用，已固定实际参数。fresh临时目录复现的八张PNG全部逐字节相同，见[replay-check.json](replay-check.json)。SVG/PDF的时间元数据不保证逐字节相同。

结构图通常可直接在draw.io里移动节点、编辑中文，保存源后按明确参数重导；区间及年份图保留数据/脚本，数值变更需重算并重生成。PNG作为Word插入件；draw.io SVG的foreignObject文本存在跨应用兼容限制，因此可编辑owner仍是`.drawio`。

## Typesetting and Verification

本轮直接复用已交付、由共用DOTX生成的Word，替换八个PNG媒体部件、相应尺寸/alt描述及实际PAGEREF缓存。仅九个DOCX部件变化，所有其他XML/样式/原生SEQ、REF、TOC、书签、页眉页脚及26表逐字节保留；文档主体规范化比较也只允许上述图属性与目录缓存改变，见[layout-final.json](layout-final.json)。旧章adapter被第二章保护哈希引用，本轮未修改它或第二章任何文件，也没有建立新全书格式owner。

- 全部图在155mm下有效分辨率约400ppi，最小中文10.5pt；图高112—157mm。各图、图题和来源同页；目录按82页实际位置回填，字体全部嵌入，页码连续，25个REF/PAGEREF目标存在。
- 六份draw.io严格校验均0 errors/0 warnings；数值重跑与日期/引用对应核验见drawio-validation.json、numeric-proof.json与semantic-adjudication.md。
- 独立会话实际逐张看八幅彩图及八幅灰度版，共16个当前文件，图3修正后重新查看，见figure-review.json。
- 两名独立会话逐张看完第1—42、第43—82页，共82页；Parent实际看八个图页、章首、目录及41—43连续区间的过渡，hash清单与真实查看记录见page-review.json、parent-page-review.json及page-images.json。页面PNG为可复现的内部中间件，交付绑定最终PDF。
- 图3首稿把“候选共享位置”当作失效证据，Parent纠正为“所选安排重复占用”，并明确“全部合法选择已穷尽”；仅此图的当前版本重新进行了独立图像检查。图7导出偏移已在writer首轮修正。没有降低信息契约换取外观。
- 原章/原始材料/前轮pilot/已安装Skill等279项保护文件字节不变。原Harness51项测试与validate通过。最终章级check/review/accept沿用既有CLI；实际状态与证据绑定以harness.json和runs/ch01-figures.review.json为准。

原完整章专业与教学审校仅对等价的正文、数据及引用保留适用性，见content-equivalence.json；新图和新分页依赖本轮实际独立审阅，不能宣称旧审校看过新图。Parent汇总review使用`ai_self`，不因报告中有独立QA而改称独立整章验收。

## Limits and Reuse

新图占页更多，整章增加3页；后续图仍应按教学目的和版心选择布局，不能机械复制高度或八图数量。尚未执行真实教师/学生试读、纸张打印、Microsoft Word原生域更新及校方/出版社审定；Word改变分页或更新域后需重新查目录和图文位置。当前交付是完整初稿及正式排版，课堂效果和出版定稿未确认。

第二章可直接复用现有两项Skill、薄路由、字体、共用模板和质量核验方式；本轮未改第二章在途内容。共享harness.json与现状记录的写入顺序已由用户明确指定为第一章先更新、第二章随后追加。

## Session Record Evaluation

当前repository未声明独立session-capture Skill。实质教学图实现、产品判断、独立QA、Kimi身份与实际Read、原版保护、工程证据均保留在本目录及现有目的记录，无新增台账体系或memory写入。
