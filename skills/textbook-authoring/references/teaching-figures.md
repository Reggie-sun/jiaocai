# Teaching Figure Routes

## Choose the Encoding

学习目标先于工具。用一句话说明“学生通过图能作出什么判断”，记录需要保真的对象、关系、条件或数据。选择能让关键差异看得见的表示，不把上游的 architecture preset 当作全书模板。

| 学生需要判断 | 可用表达 | 能力入口与编辑源 |
| --- | --- | --- |
| 包含、区别、对应或依赖 | 集合、层次、二分图、映射、对照、概念网络 | [drawio-skill](../../drawio-skill/SKILL.md)：`.drawio`；简单图可继续用SVG |
| 算法怎样改变状态或失败 | 状态快照、搜索/递归树、时间轨迹、带条件的流程 | `.drawio` 或基于实际trace的SVG/绘图库；不只画步骤名 |
| 系统组件怎样协作 | 分层、组件、泳道、数据流或时序 | `drawio-skill`；区分控制流、数据流、部署与逻辑关系 |
| 数量、分布、趋势、区间和冲突 | 点线、分组/区间图、共同时间轴、适当的热图 | [scientific-visualization](../../scientific-visualization/SKILL.md)：数据+绘图脚本+SVG/PDF/PNG |
| 现实情境或操作怎样发生 | 必要的教学插画、局部细节示意 | 已有 `imagegen`；保留提示词/原始图，精确中文与关系另用可编辑标注 |

复杂关系先冻结边集合/语义，公式先核对符号与适用条件，数据先保留单位/缺失/转换口径。不能为了画成某类图改变问题；图不比表格或正文清楚时不强配。概念关系不自动添加方向箭头，年代先后不等同因果，单个尝试失败不证明整体无解。

## Local Tools and Compatibility

两个选中的上游 Skill 已按固定 commit 保存于仓库；身份见各自 `UPSTREAM.json`，许可证随目录保留。工具操作读取其原入口及所需 reference，不复制全部手册。`drawio-skill` 的 `disable-model-invocation` 上游元数据保留；教材主 Skill 按任务显式读取/选择，不依赖全局自动触发。无需注册新的MCP服务或使用上游IR/CI治理来制作小教学图。

本机 `draw.io 32.4.1` 为用户目录中解包的官方Linux发行版，不改系统软件；本轮实际二进制是 `/home/reggie/.local/share/jiaocai-tools/drawio-32.4.1/opt/drawio/drawio`，`xvfb-run` 用于headless导出。其他主机按上游CLI安装说明核对实际路径与版本。原始 `.drawio` 是正式编辑owner，导出SVG只作为下游格式；本轮即使使用纯文字标签，实际SVG仍带 `foreignObject`，Word/非浏览器兼容性不能假定。本轮Word采用高分辨率PNG，编辑回到 `.drawio`；需要矢量插入时先检查实际渲染。

许可区分：两个Skill代码为MIT，drawio的shape-index附带Apache-2.0；实际桌面32.4.1为 `GPL-3.0-only`，不随本仓库分发。本机使用官方未修改版本，具体版本/依赖/许可核对见 [Research](../../../materials/teaching-figures-pilot/upstream-research.md)。

绘图库采用本机已存在的 `/home/reggie/miniconda3/bin/python`，本轮实测版本及可重建依赖见 [requirements.txt](../../../materials/teaching-figures-pilot/requirements.txt)。不安装整个scientific-agent-skills插件或可选Plotly/Seaborn/云图标链。默认结构图仅用本地图元；品牌素材、远程字体、CDN或在线viewer不得冒充离线链路。

`scientific-schematics` 本轮未采用：其生成和视觉评分依赖付费API，输出PNG，不能替代可核验矢量图/数据图。已有 `imagegen` 仍用于必要情境；新增外部付费绘图API必须先获得用户对具体调用/预算的确认，不自动找key、调用、重试或通过“质检”隐藏第二次收费。任务必须能先使用本地路线推进。

## Author and Verify

1. 保留最少但足够的“教学用途—事实/数据—表达方式”说明，可写入已有图表清单；不新建逐图治理台账。
2. `.drawio` 保留稳定ID、真实source/target与标签；数据图从明确数据生成，保留脚本。新编辑另存候选，不覆盖已交付章。
3. 按上游运行 `validate.py` 或数据export/metadata检查。几何得分、DPI、模型评分都不证明图意正确；直接复算数量、关系、公式、坐标与条件，并实际查看图片。
4. 使用本书白底、深色文字/线条、强调色 `#1F4E79`、`Noto Sans CJK SC`。沿用 `textbook-style-v1.0` 的155 mm版心、插入后最小10.5 pt文字/0.5 pt线条及至少300 ppi；覆盖上游8 pt、西文字体、期刊尺寸和配色。灰度仍以位置、标签、形状、线型/纹理区分。
5. 数量/时间图保留共同尺度及单位，真实与教学示例分别标明。导出固定物理尺寸时 `bbox_inches=None`，不通过tight裁切无意改变字号；保留可编辑文字SVG（依赖安装字体）和必要PNG/PDF，需要字形路径版时另存，不能覆盖编辑源。
6. 图编号不烘焙入图；图题、来源和简短替代文字沿用已有清单/正文。插入使用共用模板和原生题注/REF；实际渲染并查看图及题注所在教材页，尤其核对缩小后的中文、边界、灰度和线条。

## Delivery and Reuse

与正常章交付一起纳入原Harness的图表/materials及五项审校；独立试图不是完整节，不造新run或新gate。教学准确性、真实看图和页面检查按实际身份记录，AI比较不等同学生学习效果。第一章两类独立试图与实测入口见 [Pilot Report](../../../materials/teaching-figures-pilot/report.md)。第二章可直接调用这些能力，但须用第二章自己的教学目标、数据和图意审校，不把两个样本当作固定图式。
