# Chapter 1 Figure and Typesetting Implementation Plan

## Goal and Contracts

执行`specs/ch01-history-layout.spec.md`，将历史回顾文字稿交付为七图完整Markdown、Word和PDF。格式直接继承`textbook-style-v1.0`，正文基线与新图语义分别验证，Native Codex为主流程。

## Milestones

1. 固定基线和文件职责；复用共用模板、现有字段/表格/排版模式，图稿writer只写新图资产与清单。
2. 制作七个可编辑教学图和彩图/灰度导出，核对格子、历史日期、关系、限制及实际插入尺寸；组装另存图文稿并验证基线文字逐字节保留。
3. 用bundled文档运行时构建Word，渲染同版PDF，依据实际页码回填目录缓存，修复分页或图文问题；保留原生字段和模板样式。
4. 受管Kimi核查新增图语义；实际查看全页与图稿，结构/文本/字体/字段检查与人工可见页面证据各自记录，不互相冒充。
5. 登记新完整章run并执行原Harness验收；更新目的记录，核对保护范围和最终diff，提交本轮owned files，提供Word/PDF。

## Completion Criteria

七图ready，源/灰度/导出可追溯；正文与答案保留，Word/PDF一致；目录、题注、引用、图表、字体及页码核验通过；全部最终页面实际查看，未解决blocking为零；新run的有效状态与交付说明一致。保留原版本、外部变化与真实验收边界。
