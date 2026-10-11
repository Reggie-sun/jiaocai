# Figure Production Notes

## Reproducibility

`python3 materials/ch02/render_figures.py` rebuilds eight editable SVG sources and their PNG exports under `assets/figures/ch02/`, then refreshes `materials/ch02/figure-manifest.json`. The renderer uses the installed headless Chrome and only the chapter's authored teaching data. SVG is the editable source of truth.

All PNGs are 2400 pixels wide. At the manifest's 155 mm insertion width this is approximately 393 ppi. The smallest declared SVG text is 22 px on a 900 px viewBox, or 10.74 pt at the stated insertion width. Captions match the current chapter manuscript. The palette uses white, dark ink and `#1F4E79`; labels, arrows, line patterns and node shapes carry the meanings independently of color.

## Figure Review

八张最终 PNG 均以原始分辨率逐张打开查看；另用 `ffmpeg -vf format=gray` 生成临时灰度副本并逐张查看，副本只保存在 `/tmp/jiaocai-ch02-grayscale/`。复查包含文字可读性、图元边界、连线端点、箭头与权重标签、节点/标签间距，以及灰度下的符号和线型区分。图2-2和图2-8在首次查看后作了留白调整，之后又分别复查最终彩色图与灰度图。这里记录的是图像级检查，不代替将图片嵌入 Word/PDF 后的实际页面检查。

| Figure | 设计目的与最终查看重点 |
| --- | --- |
| 图2-1 | 并置建筑级合并表示和入口级表示；右图分别标出西门到N的3分钟、西门到M的7分钟、N到M的建筑外绕行4分钟及入口通行属性。灰度下路线标签和箭头仍清楚。 |
| 图2-2 | 两层状态图中普通移动保持同一进度，只有C点完成服务时由`0`跨到`1`；2分钟与5分钟均标为到达P的整段时间，未拆分未知路段，也未把5分钟延伸至出口。SVG说明同时注明从P到出口的时间未给定，最终目标仍为`X,1`。最终版节点、跨层箭头和注释之间留有间距。 |
| 图2-3 | 显示A—G有向依赖关系、虚线模块边界、`map=M1`/`C1`版本标记与兼容要求；不含耗时或关键链答案。灰度下模块虚线框仍可辨认。 |
| 图2-4 | 概念性局部观察支持范围；实心、空心和叉号样本分别由图例解释，范围外叉号旁标注“先复核”，轴标签和边界标注与图框保持间距。图注明确边界不是阈值或统计置信区间。 |
| 图2-5 | 按章内Dijkstra示例画出八条有向边及权重；`C=5`后`D=7`、`E=8`仍在前沿，A→D的11分钟箭头由上方进入D，和C→D的2分钟箭头分开；`距P=7`移至弧线左侧，彩色与灰度最终图中标签均不被线条穿过。灰度下双圆、虚线方框和较粗路线仍可区分。 |
| 图2-6 | 五个请求逐项呈现B=`6,7,8,9,10`、C=`5,6,7,失败,失败`，并展示成功均值、覆盖率、共同成功子集；通行分组标为“未提供”，未补造标签。 |
| 图2-7 | 流程区分提交前拒绝、权威确认和`UNKNOWN`；提交前检查的“符合”箭头进入提交框，“拒绝”支路向下，两个结果明确分开。右上未知状态框将“断连或超时”“UNKNOWN”“暂停重试”分成三行，最终彩色与灰度图中三行均有清楚内边距、未接触边框；下接原操作ID查询的虚线箭头仍从状态框底边引出。查询结果分为已应用、确认未执行且无在途请求/幂等契约允许的有限次同ID重试、仍未知并暂停，支路可在灰度下辨认。 |
| 图2-8 | 核对E06十条无向边及全部分钟数；`P—Q`为唯一虚线台阶边，其余为实线无台阶边。`Q—C=2`白底标记紧邻对应斜边，并与`Q—X=6`清楚分离。六个节点、边权和约束框不互相遮挡；最终版台阶文字与虚线留有清楚间隔。 |

## Artifact Verification

执行`python3 -m py_compile materials/ch02/render_figures.py`与`python3 materials/ch02/render_figures.py`。随后逐项检查manifest中的八个ID、PNG/SVG相对路径、文件字节数、PNG实际宽高、PNG与SVG SHA-256、155 mm插入宽度、计算得到的393 ppi及10.74 pt最小字号；八项均与生成文件一致。

图表生成和文件完整性核验已完成。最终教材的Word/PDF页面位置、缩放和换页效果仍由整章排版与实际页面检查确认。
