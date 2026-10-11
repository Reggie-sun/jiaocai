# Chapter 2 Progressive Edition Implementation Plan

## Goal and Contracts

按[Spec](../specs/ch02-progressive.spec.md)交付第二章递进版，恢复原提纲标题并把AI时代的方法重构写成可理解、可练习的主线。Native Codex拥有lifecycle；复用最新版`textbook-authoring`、Markdown SDD、互斥作者职责、原Harness及`textbook-style-v1.0`。旧章、原材料、引擎、policy、模板不变。

## Current and Target Behavior

现版在抽象、依赖、算法与状态边界处起点偏高，章题/节题不符合最新保留原纲要求。新版本从文字材料、小任务和手工比较进入，先使学生能够操作，再解释AI引起的表示、知识来源、求解、检验及责任变化，深层机制建立在已讲知识上。

## Milestones and Ownership

| Milestone | Owner and Files | Acceptance and Verification |
| --- | --- | --- |
| M1 | Parent：本Spec/Plan、`materials/ch02-progressive/authoring-brief.md`、来源与输入材料 | 原提纲实际Word核对，最新规则完整读取，旧产物保护清单；有界来源调查不冻结在途正文 |
| M2 | writer A：`manuscripts/ch02-progressive/s2-1.md`、`s2-2.md`、`answers-e01.md`、`answers-e02.md`；writer B：`s2-3.md`、`s2-4.md`、`answers-e03.md`、`answers-e04.md`；Parent：其余正文 | 所有target-file互斥；每节导语/案例/解释/训练/反思完整，示范与独立题分离；片段篇幅及数据自检 |
| M3 | Parent：当前合并稿、`prepare.py`、独立数值验证、图表清单/源文件 | 全章28000—40000近似汉字；新旧数据复算；逐条引用支持与图表编号一致；文字稳定后统一配图 |
| M4 | 两个独立只读实际会话专业/教学审校；Parent保存报告及裁决 | 整章真实读取记录、exact SHA，无作者PASS或peer结论；确认问题修订，实际新快照复查闭合 |
| M5 | Parent复用旧任务适配器到新证据目录，生成新Word/PDF | 共用DOTX原字节、原生域/书签、实测目录、字/图/表内容一致；最终全页实际查看并记录哈希 |
| M6 | Parent：新run、报告、目的记录与owned commit | 原51项Harness测试、当前新run五维review与accept、旧文件保护、最终diff与提交；评价可复用范围和真实教学限制 |

## Verification and Recovery

复用原练习核验程序作为只读数值依赖，新增基础与AI候选核对以独立脚本记录；不把旧46项PASS当作新题干可读性证明。任务本地适配器仅调整新路径、标题和必要图表数量，不改模板/引擎/路由。实际页面有问题才作最小修复，修改正文回写源并重渲染，证据在最终Harness check前稳定。受管源调查、正式专业/教学审校和页面检查是不同职责，报告说明实际覆盖，不能互相替代。

## Self-Review

M1—M6覆盖Spec A1—A7，先文字后配图，先内容稳定后独立审校与排版，最后完整快照验收。无逐步确认、无原产物覆盖、无重构和额外workflow升级。先备短回顾支持操作，专业深度按递进承担，最终学习效果仍需教师/学生验证。
