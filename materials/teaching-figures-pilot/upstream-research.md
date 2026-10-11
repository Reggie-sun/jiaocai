# Teaching Figure Skills Research

## Decision

采用 `drawio-skill` 3.4.3 与 `scientific-visualization` 1.4，沿用现有 `imagegen` 情境插画入口；不安装或运行 `scientific-schematics` 1.10。下面是实际源码调查，不代表中文教材效果已获社区或学生验证。

## Sources and Maturity

| Upstream | Pinned commit | Community snapshot |
| --- | --- | --- |
| [Agents365-ai/drawio-skill](https://github.com/Agents365-ai/drawio-skill) | `57270820d3cd71cbdf4fb6b2f7091d4fb37bb019` | GitHub API核对：10,063 stars、707 forks；最后push 2026-10-11 |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | `92ace75ac21efe19a620434e0ca4e356081fe807` | 48,371 stars、4,349 forks；最后push 2026-10-05 |

上述数值为2026-10-11快照，只反映传播。独立 native `workflow-research-agent` 实读源码、许可证、测试和Changelog：drawio快照有15个测试文件、静态247个test方法；visualization的专用测试文件有30个方法，依赖/原生测试可能跳过。该调查未实际运行整套上游测试，不称全链验证。[drawio tests](https://github.com/Agents365-ai/drawio-skill/tree/57270820d3cd71cbdf4fb6b2f7091d4fb37bb019/tests)、[visualization tests](https://github.com/K-Dense-AI/scientific-agent-skills/blob/92ace75ac21efe19a620434e0ca4e356081fe807/tests/scientific-visualization/test_scripts.py)。

## Capability and Dependency Assessment

### drawio-skill

[实际入口](https://github.com/Agents365-ai/drawio-skill/blob/57270820d3cd71cbdf4fb6b2f7091d4fb37bb019/skills/drawio-skill/SKILL.md)和`diagramctl.py/diagram_ir.py`提供可编辑 `.drawio`、关系/结构/时序/泳道及布局工具。核心XML/IR/check使用Python标准库；Graphviz自动布局可选，PNG/SVG/PDF需要draw.io desktop。Linux headless需Xvfb/Electron依赖；本轮使用官方32.4.1解包发行版，未装全局服务。

适合精确概念关系、算法/系统结构及人工调整。`validate.py`的几何分数不能证明图意、中文或标签清晰；本轮另看图、复算六条边和容量。品牌CDN/在线viewer是可选网络链，本轮只用本地图元。`disable-model-invocation`元数据保持上游原值，主Skill显式路由读取。

额外核对实际桌面依赖的[32.4.1 package.json](https://github.com/jgraph/drawio-desktop/blob/v32.4.1/package.json)：当前许可为 `GPL-3.0-only`，有别于旧版本说明中的Apache-2.0。本轮使用官方未修改发行版，仅在本机解包；没有将桌面程序、Electron或其二进制随教材仓库分发。Skill本身仍为MIT，不能把两者许可混为一谈。

### scientific-visualization

[实际入口](https://github.com/K-Dense-AI/scientific-agent-skills/blob/92ace75ac21efe19a620434e0ca4e356081fe807/skills/scientific-visualization/SKILL.md)及`figure_export.py/image_metadata.py/palette_audit.py`支持真实数据编码、固定物理尺寸导出、provenance、覆盖保护及元数据/对比度检查。CLIs离线运行，按功能延迟加载Matplotlib/Pillow/pypdf；Python≥3.11，uv只用于上游示例。没有安装整个仓库开发环境或Plotly/Kaleido。

采用本机现有Matplotlib 3.10.7及Pillow 11.3.0。上游直接版本示例不是本机环境，首次pip尝试因proxy不可达失败，未声称安装成功；改用已经存在、实际跑通的固定环境。依赖身份见`requirements.txt`。默认8/7pt、西文字体和期刊宽度被教材既定体例覆盖。文字SVG保留编辑性但不嵌字体，PDF/PNG供稳定输出。

### scientific-schematics

[生成实现](https://github.com/K-Dense-AI/scientific-agent-skills/blob/92ace75ac21efe19a620434e0ca4e356081fe807/skills/scientific-schematics/scripts/generate_schematic_ai.py)的`ScientificSchematicGenerator`要求requests、网络和`OPENROUTER_API_KEY`，生成和视觉评分调用外部付费API，输出仅PNG，无本地矢量后端和精确字号/DPI控制。入口还会从父目录`.env`找key；不具备用户收费确认机制。

默认至多两次生成，评分可推动下一轮；失败的付费请求不自动重放。mock接口测试不能证明真实付费端到端效果。它与现有情境生成能力重叠，不能承担本书的拓扑/公式/数值核验，故不安装，也未读取其key或调用API。

## Licenses and Installation

两个选中Skill代码均MIT，保留[drawio许可](../../skills/drawio-skill/LICENSE)与[K-Dense许可](../../skills/scientific-visualization/LICENSE.md)。只安装选中子目录，保留相对资源层级。drawio携带的shape-index来源为Apache-2.0，已保留上游NOTICE并补入[完整Apache-2.0许可](../../skills/drawio-skill/data/APACHE-2.0.txt)；本轮没有使用品牌素材。

本轮使用 `skill-installer` 固定commit安装到仓库`skills/`，本机Codex与桌面Skill目录各提供指向该owner的symlink。上游文件未改编，仅补许可证/UPSTREAM身份；教材限制由主Skill薄路由维护。下一轮可发现这些安装项，当前轮已直接读取入口使用。

## Pilot Grounding and Adjudication

独立研究首版误用了旧稿七图清单，Parent未采纳其旧图1-3/图1-7取样建议；researcher随后完整读取最新八图清单及图1-2/图1-6正文，纠正为本轮真正基线。采用的是 `assets/figures/ch01-rewrite/`，不是历史 `ch01/`。这个更正不会改写历史文件。

Parent选图1-2的关系/容量图及图1-6的精确分钟区间图。两种可编辑路线的真实结果、灰度、排版与编辑代价见[试图报告](report.md)。社区信号、检查脚本和研究建议均不替代该结果。

## Software Reference

已联网核对[arXiv实际元数据](https://arxiv.org/abs/2609.00065)：KASSIS T, AGARWAL V, HE Y, PATEL D, BRUECKNER A M. Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents[EB/OL]. 2026[2026-10-11]. https://doi.org/10.48550/arXiv.2609.00065.

按上游Skill要求在软件调研报告中加入该引用，未插入第一章正文或其参考文献。论文摘要明确没有task-level evaluation或host selection rate，不能用它声称教学效果已得到实证。
