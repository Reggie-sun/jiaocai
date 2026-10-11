# Chapter 1 Figure Edition Plan

## Goal and Scope

实施[本轮Spec](../specs/ch01-figures.spec.md)，将八幅新图实际插入完整第一章；沿用既定教学方法、格式和Harness，不改旧稿或第二章。Native Codex为primary，`superpowers:writing-plans`只提供durable plan。

## Major Milestones

| Milestone | Ownership and deliverable | Verification |
| --- | --- | --- |
| M1 Freeze | Parent固定旧章保护hash及八图正文语义，保存新Spec/plan | 现有status、精确ownership；Kimi封存语义QA输入 |
| M2 Draw | bounded native worker仅写图1/3/5/7/8源和局部生成器；Parent负责图4、复用图2/6、整合manifest | writer集合不重叠；本地导出、图意/尺寸/灰度实际查看；Kimi文本QA与Parent裁决 |
| M3 Typeset | Parent只替换完整稿八处路径，复用原章adapter与DOTX生成新Word/PDF | 正文等价、原生域/26表/8图、字体/目录/页码；独立审校者分段实际看全部页，Parent看八幅图及关键插入页 |
| M4 Deliver | Parent记录独立意见、关键修正、旧章保护及risk判断，登记新版chapter run并执行check/review/accept | 稳定完整快照、原引擎测试/validate，更新目的记录，specific-file commit |

## Boundaries and Recovery

worker所有文件位于新目录，仅拥有`render_relations.py`及图1/3/5/7/8的`.drawio/.svg/.png/.pdf`和灰度文件；不得写manifest、旧图、正文、Harness、Spec/plan或共享排版adapter。Parent不编辑其owned files，待worker完成后接管。受管Kimi只读新的冻结语义包，不能依其未见图片作视觉结论；未知结果不盲目重试。图若未改善则以清楚、准确为先，按具体缺陷有限修正，不增复杂治理。

## Self-Review

依赖先语义、后图、再排版和当前快照验收；覆盖本轮所有八图、完整页检和上一版保留。正文等价证据允许复用旧章内容审校的实际范围，新图及分页由真实新审校补齐，不声称旧审校看过新图。
