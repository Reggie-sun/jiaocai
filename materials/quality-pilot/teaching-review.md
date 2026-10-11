# Independent Teaching Review

## Identity and Scope

实际独立会话`/root/teaching_comparison`，native profile `reviewer_high`，read-only；非Parent自审，非工程final review。模型与推理档位按所选profile配置，未另做Provider身份认证。两个小节的X/Y身份映射未提供，未读取其他审校和Parent裁决。以下为代理实际返回的发现，由Parent保存；不构成课堂效果或整章审校。

## Findings

**TC-01，non_blocking，1.1.3 X：回退时恢复候选的步骤未讲清。**

`comparison-x.md:25`要求“从其他请求的候选中移除同一设备与时段”“回退并尝试其他选择”。学生若直接修改候选集合，却在回退时只撤销安排、没有恢复此前删除的候选，原本可行的分支仍会表现为无候选。“回退”不足以使未学相关搜索的读者复现状态恢复。

最小修正：说明恢复本次选择造成的删除，或保留原候选、另维护占用状态。核验：R2先选D1-S1令R1无候选，回退后改选D1-S2，说明R1如何重新获得D1-S1。Y的`comparison-y.md:36`明确要求“撤销占用”，此前没有要求破坏性删除原候选，减少这一歧义。

**TC-02，non_blocking，1.3.2 Y：连续占用没有落实到冲突机制。**

`comparison-y.md:91`提出“场地连续使用两小时”和时段粒度问题，但未说明一次选择占用哪些位置、旧唯一占用为何漏判；邻节`s1-3.md:102`再次要求表达连续占用，也未给判断过程。学生可能只加时长字段或细分时段；即使粒度足够，只登记开始位置仍会漏掉冲突。

最小修正：给开始位置不同、实际重叠的两活动反例，同时改变占用表示和冲突检查。核验：区分[9,11)与[10,11)的重叠，以及[9,10)与[10,11)的相接，解释细分时段为何不能单独修复旧检查。X的`comparison-x.md:64—72`提供了该机制与对照。

## Actual Reading Evidence

全文读取brief、两版本、基线1.1及1.3；实际`view_image`查看新图。开始与结束SHA-256一致：

| 文件 | SHA-256 |
| --- | --- |
| AGENTS.md | `231fa88bfbf645c9806778de91f03a3e36704db1b487b78e894f01167a79d234` |
| materials/quality-pilot/review-brief.md | `32339ffc251baea489dc6719a55c04105c50703bfd35d0be77adf87b449f546a` |
| materials/quality-pilot/comparison-x.md | `4a83314f0587a340cce3521ebce8d4b1be3a451cde27f2374607a68c7d653b32` |
| materials/quality-pilot/comparison-y.md | `49e8e41bd6d8e3e36031e9ccfae0d87e242a0be8675a712b8e39466479b67551` |
| manuscripts/ch01/s1-1.md | `a126c693df95494dc71a7eba14be3a59860f586d0ad6b80981fad48d0e78e4aa` |
| manuscripts/ch01/s1-3.md | `d2d5202bd63b38930e0805e0c741b2beb535208e89552bb0ae28b176d5bcb894` |
| assets/figures/quality-pilot/bottleneck.png | `705362f2c0c50faf99ded793491fcc22ec11533414321c303f58925ed880299e` |

未核验外部来源和其他图，未读取其他章节、作者自评、identity key、peer review或Parent裁决；无学生实测或课堂观察。本次发现均指向基线片段，未提出试写稿阻断项；Parent仍须独立判断。
