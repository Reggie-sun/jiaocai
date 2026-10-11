**PRO-01 — blocking_candidate：E02把漏报记录作为提醒队列排序可处理的对象**

- **位置与原文**：[review-r1.md:683](/home/reggie/vscode_folder/jiaocai/materials/ch03/snapshots/review-r1.md:683)，E02参考解：“保留所有提醒，再按……排序……多笔付款超过授权额度……可优先查看。”
- **触发与证据**：“多笔付款超过授权额度”对应记录03；[题表第207行](/home/reggie/vscode_folder/jiaocai/materials/ch03/snapshots/review-r1.md:207)明确其“系统提醒”为“否”。实际提醒集合是01、02、04、05、06、09，03不在其中。
- **违反契约与影响**：违反Chapter 3 Spec的题解对应、有限行动和条件可核验要求。该答案会让学生误以为给现有提醒排序能够找回漏报，混淆队列内部优先级调整与新增检测规则，也使每天三条的处理方案无法按给定队列执行。
- **最小修正**：排序示例只选已有提醒，如01、02、04；若要优先处理03，明确需要额外规则或人工抽查先将其发现并纳入队列，再重新检查每日容量。
- **最小验证**：从表3-4提取所有“系统提醒＝是”的ID，断言现有队列排序的候选均属于该集合。独立只读复算已确认03不属于提醒集合；现有`exercise-verification.json`检查提醒数量，但未检查排序示例的集合成员关系。

**Review Metadata**

- 快照：`materials/ch03/snapshots/review-r1.md`；首尾核验SHA256均为`950da6e74abdbb17ea2b008231f7c515b2d17de0b40bf8f0f77a0f221347a80c`。
- 正文实际通读：1–100、101–200、201–300、301–400、401–500、501–600、601–700、701–798，覆盖完整章及全部参考解。
- 配套阅读：`AGENTS.md`全文；Spec 1–50；Skill 1–261；`source-excerpts.md` 1–272；`source-supplement.md` 1–61；`exercise-verification.json` 1–318。材料内嵌的自评和裁决说明未作为判断依据；未读取同行报告或单独裁决文件。
- 验证：独立复算E02/E03分类计数、E05/E06基线与条件变化、采购费用；补查[UNESCO官方框架](https://www.unesco.org/en/articles/ai-competency-framework-students)和[小米官方年度报告](https://ir.mi.com/system/files-encrypted/nasdaq_kms/assets/2025/04/24/5-27-15/%E8%8B%B1%E6%96%87.pdf)相关原文。其余来源检查限于提供的原文片段，不声称全文审读。
- 限制：本轮为文字内容专业审校，未验证真实课堂效果、真实模型表现或Word/PDF排版；无文件修改。

