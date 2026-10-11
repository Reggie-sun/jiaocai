# Teaching Figure Capability Pilot

## Result

采用 `drawio-skill` 与 `scientific-visualization`，保持已有 `imagegen` 插画入口；不安装 `scientific-schematics`。两张独立候选在关键判断的可见性上优于原图，尤其是时间图的端点和实际占用；这是Parent与独立AI看图的判断，尚无教师/学生试读证据。没有替换第一章任何正文、原图、Word或PDF。

直接查看 [四页PDF对照](../../output/teaching-figures-pilot/教学图对照试排.pdf) 或 [可编辑Word](../../output/teaching-figures-pilot/教学图对照试排.docx)：第1/2页为图1-2原图/候选，第3/4页为图1-6原图/候选。两版本用相同正文、155 mm插图宽度、共用DOTX样式和原生题注/REF，比较不靠改变页面字体。

## Adopted Capabilities

| Capability | Decision and actual use |
| --- | --- |
| [drawio-skill](../../skills/drawio-skill/SKILL.md) 3.4.3 | 固定上游commit；本地可编辑关系、算法和系统图路线。本轮生成可直接用draw.io打开的`.drawio`并实际导出PNG/SVG/PDF、运行几何校验。Skill代码MIT，shape-index附Apache-2.0。 |
| [scientific-visualization](../../skills/scientific-visualization/SKILL.md) 1.4 | 固定上游commit；采用真实数据/共同尺度、物理尺寸导出、provenance与元数据/调色检查。本轮用Matplotlib生成分钟区间图，保留数据、脚本、文字SVG、PDF/PNG。Skill代码MIT。 |
| scientific-schematics 1.10 | 源码核验后未采用。生成及视觉评分均调用OpenRouter付费API，PNG不支持关系/公式的精确编辑，与已有情境生成入口重叠；本轮没有调用该API或自动读取key。 |
| existing imagegen | 继续承担必要情境插画，精确中文、公式、边与数据在可编辑层表达。本轮两图属于关系和数量表达，没有为了装饰额外生成插画。 |

实际能力、依赖、维护/社区信号、许可证和软件引用见 [上游调研](upstream-research.md)。社区stars与代码测试不是教材教学效果证据。实际桌面依赖draw.io 32.4.1为`GPL-3.0-only`，官方未修改二进制仅本机使用，不随仓库分发；没有误用旧版Apache说明。

主Skill只增加选择与核验的薄入口，具体适配在 [Teaching Figure Routes](../../skills/textbook-authoring/references/teaching-figures.md)。`AGENTS.md`、Harness代码/schema/登记及`textbook-style-v1.0`模板保持原字节，没有新绘图治理或第二套验收体系。Spec/plan沿用现有SDD，调用现有受管Kimi与native只读能力。

## Figure Comparison

### Figure 1-2 — Local Candidates and Global Bottleneck

[原图](../../assets/figures/ch01-rewrite/fig1-2.png) → [候选PNG](../../assets/figures/teaching-pilot/fig1-2-candidate.png)；[编辑源](../../assets/figures/teaching-pilot/fig1-2-candidate.drawio)。

原图的结论准确，文字较大、占页少，但多条斜线交叉，容量假设主要靠上下文；“三项请求争用两个位置”在底部文字中说明。候选采用无交叉的二分关系排布、请求/位置的不同形状、明确容量1、瓶颈集合外的孤立d，再用3个请求符号与2个位置符号直接作数量对照。学生可以同时检查允许关系和无解原因，不必只相信底部结论。

六条边完整保留且不加方向箭头；连线明确是允许关系，不是已选安排。枚举8种候选组合，满足位置不重复的方案为0。下方数量对照增加教学信息而不是更换配色，但也使图高从66.33 mm增到124.01 mm，约1.87倍；用于核心反例合适，紧凑复习页仍可选择原图。样本不证明drawio自动布局对任意大图都有效。

### Figure 1-6 — Intervals and Actual Occupancy

[原图](../../assets/figures/ch01-rewrite/fig1-6.png) → [候选PNG](../../assets/figures/teaching-pilot/fig1-6-candidate.png)；[编辑SVG](../../assets/figures/teaching-pilot/fig1-6-candidate.svg)、[数据](data.json)与[绘图脚本](build_figures.py)。

原图准确示意三种关系，但没有共同坐标刻度，半开端点和扩展后的35分钟冲突需阅读标签推算。候选用三个独立面板、统一9至12点刻度、按分钟比例绘制的区间、实心/空心端点，以及不同纹理的重叠/清理/准备。第三面板明确独占条件，直接标出10:45—11:20共同占用35分钟；与前两面板60/0分钟形成可核验对照。

这是从示意条带改为准确时间编码，视觉改善比图1-2更明显；灰度仍能判断A/B、准备/清理和边界。图高从77.50 mm增到157.03 mm，约2.03倍，完整三例比较需要较多版面，不能把文字缩小来强行追回空间。后续章可选单例或分图，但应按该章教学目的决定。

| Comparison | Original | Candidates |
| --- | --- | --- |
| 教学表达 | 核心结论准确、简洁 | 容量和瓶颈直接可数；端点与有效占用直接可读 |
| 视觉效果 | 清楚但以矩形和说明文字为主 | 关系图有语义形状/集合/计数，时间图有尺度/端点/纹理，保持教材克制风格 |
| 中文可读 | 原图字号大、适合快速扫读 | 155 mm下最小11.70/10.5 pt，中文实际页检清楚；信息增加，阅读负担和面积也增加 |
| 可编辑性 | 原来已有SVG与生成器，可编辑 | 新增draw.io直接改节点/边，数据图用明确参数联动生成；不是把原图变成不可编辑位图 |

## Actual Editing and Reproduction

在临时目录执行 [编辑探针](edit_probe.py)，没有改正式候选：关系图将b改名b′，只改两个标签值，六条边不变，重新导出约2.07秒、校验0错误0警告；时间图将清理20改为30分钟，同时更新有效末端和预期交集三处JSON值，不改代码，即显示45分钟与11:30，导出约0.55秒。结果见 [editing-probe.json](editing-probe.json)。机器导出时间不是人工编辑时长，没有声称测量教师的操作效率。

编辑测试先暴露了清理标注与括号端点仍写死的问题，修正为从数据计算后通过。最后从正式数据完整重建，两个PNG和灰度图与已看过的候选字节一致，约5.08秒；见 [reproduction-check.json](reproduction-check.json)。SVG/PDF的时间戳或文档ID可能变化，不要求二进制逐字相等。

初次环境准备有成本：下载draw.io、配置headless导出、核对字体；新venv的pip因proxy不可达失败，最后使用实际已存在的固定环境。drawio的节点/标签直接编辑容易，但修改拓扑仍须重新布局、复核计数与重导出；本轮生成器只是两张教材示例，不是任意关系图的通用渲染器。时间图的文字SVG可编辑，但数值修改应回到JSON和脚本，避免手工拖动造成比例错误。

## Runtime and Rebuild

两项Skill分别保留79/18个上游文件原字节，仅添加身份/许可证资料；安装入口与对照见 [installation-check.json](installation-check.json)。本机Codex与桌面Skill目录symlink均指向仓库owner，后续会话可发现。未安装完整scientific仓库、Graphviz/Plotly/Kaleido、MCP服务或云图标链。

- 绘图：`/home/reggie/miniconda3/bin/python` 3.13.5；Matplotlib 3.10.7、NumPy 2.2.6、Pillow 11.3.0、fontTools 4.60.1，见 [requirements.txt](requirements.txt)。
- draw.io：官方32.4.1；二进制 `/home/reggie/.local/share/jiaocai-tools/drawio-32.4.1/opt/drawio/drawio`，deb SHA-256 `f4455b3bba3d3b539c3cd069218fc64f0462b1b01610fe8d11acc3ca8566f32b`，`xvfb-run`导出。SVG实际包含`foreignObject`及fallback文字，所以Word采用PNG；正式编辑owner是`.drawio`。
- 中文：本机Noto Sans CJK SC；用fontTools从fontconfig实际匹配的TTC提取SC字面，缓存到用户工具目录再注册Matplotlib，避免JP/DejaVu回退。文字SVG依赖字体，PDF/PNG更稳定。
- 排版/检查：Codex primary runtime Python 3.12.14、python-docx 1.2.0、Pillow 12.3.0、pypdf 6.10.0；bundled LibreOffice 25.2。样张样式XML与共用DOTX逐字一致。

在仓库根目录可重建独立输出：

```bash
PYTHONDONTWRITEBYTECODE=1 /home/reggie/miniconda3/bin/python materials/teaching-figures-pilot/build_figures.py --output-dir /tmp/jiaocai-figure-rebuild
PYTHONDONTWRITEBYTECODE=1 /home/reggie/miniconda3/bin/python materials/teaching-figures-pilot/edit_probe.py
PYTHONDONTWRITEBYTECODE=1 /home/reggie/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python materials/teaching-figures-pilot/build_comparison.py
PYTHONDONTWRITEBYTECODE=1 /home/reggie/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python materials/teaching-figures-pilot/verify.py
```

第三条只重建Word；改变图片/Word后需用既有documents `render_docx.py`重渲染PDF并实际页检，再运行第四条，不复用旧页面证据。完整上游CLI用法保留在其Skill，不另建包装服务。

## Verification and Human Limits

[verification.json](verification.json)记录：134个原章、历史稿/图、正式输出、共用模板、AGENTS及Harness文件哈希未变；六条边、容量和8种组合直接核验；三例交集60/0/35分钟及准备/清理扩展独立复算；PNG约400 ppi且不透明；图内字≥10.5 pt；Word四图155 mm、四题注/REF，样式与DOTX一致；实际PDF为四页。drawio strict检查0错误/0警告，上游metadata/palette CLI实际运行，Skill入口校验通过。

Parent实际查看原图、最终候选、灰度和四页插入效果。独立native `reviewer_high`仅以正文摘录/数据为基线，实际打开相同10张图片，未读作者比较报告或Kimi意见，finding set为空。图片与输入快照见 [visual-review.json](visual-review.json)。页面最终无裁切、文字重叠、题注分离或多余第五页；初次字体回退和末尾来源说明跨页均已修正。真实纸张打印、Microsoft Word原生更新、教师/学生理解与课堂迁移尚未验证。

受管Kimi只做文本/数据语义QA，route receipt与Parent逐项裁决见 [Semantic Adjudication](semantic-adjudication.md)。Parent纠正了其关于11:00—11:20仍是“B准备”的错误子判断，未盲从审校。最后实现风险门见 [completion-review.json](completion-review.json)；本轮没有重大凭据/状态后果或残余验证缺口，不触发额外Kimi adversarial implementation review。独立视觉QA用于真实图像效果判断。

现有Harness validate通过，工程owner未改。只读status如实显示：历史`ch01-rewrite` acceptance仍保留，但`effective_state=blocked`的唯一新增失效原因是本轮主Skill路由文件hash变化；章正文/图/Word/PDF本身未变。没有把历史证据冒充新快照，也没有为两张非完整节试图造新run。后续第一章如需恢复当前完整快照验收，应按既有Harness做check及受影响审校；本轮不扩展为整章重审。[状态记录](harness-status.json)保留具体原因。

## Reuse in Chapter 2

第二章可以直接复用。Codex先写出学生需要作出的判断，再选概念/算法状态图、系统分层/数据流、准确数据图或必要情境插画，读取相应上游入口并沿用155 mm、中文字体、编辑源、灰度和实际插入页检。公式与复杂关系仍需符号/条件/边集合核验；本轮仅验证二分容量图与分钟区间图，不声称已试遍全部算法、系统或公式图。

后续正常章节把源图、图片和材料纳入现有图表清单与章级Harness审校即可。无需重新安装选中Skill、重新设计样式或新增绘图治理；其他主机须核对draw.io、字体与Python环境。第二章在途文件全部保留，不属于本次提交。
