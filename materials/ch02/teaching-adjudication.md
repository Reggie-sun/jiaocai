# Parent Teaching Finding Adjudication

## Exact Snapshots

初审稿R1 SHA256 `13efa16c8ee5b77f409859f64412a7b349d707084532dd6670389ca99e814ad3`；实质修订与独立完整复查稿R2 SHA256 `fa7c59dbee87a1649f6ba7a3e859fca5ae468e7bb22ffbcfab8e76626cecd002`；编辑稿R3 SHA256 `9333b146ef618d60add19a21c8c4aac04d117feeb33405f8e3684b9d4b26a300`；最终稿SHA256 `e09aa94519f298a7fc7979f7c494c525f2146e1bbfcc56a913ba41d0311ca8b0`。原报告、完整稿件和差异保留，未替换旧报告的hash。

## Findings and Decisions

| ID | Parent Decision and Evidence | Correction and Recheck |
| --- | --- | --- |
| T01 | CONFIRMED。原标记加三个新增二值分量，共四个；n×2⁴为16n，n=3独立枚举48，原8n错误。 | 2.1.4明确保留原标记、16n及全部组合上界。独立教学R2全文复查实际读到修订；Parent当前再执行枚举，证据editorial-verification.json。 |
| T02 | CONFIRMED as teaching improvement。E02虽有前置最大值评价提示，首次遇关键链的读者缺少题前推演；提供一般方法不等于泄露独立题结论。 | 2.2.3以W/Y/Z/V不同数据补前置最大值、并行时间表、工期6及两条同长链。Parent用独立schedule()复算两组；教学R2实际重读全文确认材料充足且未泄露E02答案。 |
| T03 | CONFIRMED。d7/d11的RB均预测1，标签分别1/0；原“规则给出相反结果”混淆预测与实际。 | E03题解明确“规则判断相同，实际结果仍可能相反”。Parent核对完整输入/指标；教学R2实际读新上下文，确认触发消除。 |

Parent还独立检查固定路线期望之和不要求独立性，并把原过窄的“独立平均时间”表达改为期望线性及概率承诺限制；预约情境改为场馆讲解以避免沿用第一章共享设备案例；E04邻接表明确其表示对象。完整R1→R2差异与独立教学R2报告包括这些上下文，没有新未解决发现。

## Current Editorial Boundary

R2→R3仅把图2-6阅读定位中的“平均值柱”改为“平均值”，与实际成图一致。方法、数据、练习和答案等价证据及完整diff见editorial-equivalence.json。当前实际53页由独立页面会话复查，确认文字/图对应。不能把教学R2声称为读取过R3新字节；本次证明等价的编辑不自动消耗第二次实质复查预算。

## Parent Outcome and Limits

专业初审后E02/E06两处解释发生实质修订，不能用上述编辑等价替代审查。教学reviewer最后一次定向复查实际读取方法/题干/完整答案和T01—T03修复点，独立复算15/12/12工期及14/15路线界限，确认解释准确、原修复保持、无新增finding。完整coverage见[teaching-review-r3.md](teaching-review-r3.md)，Parent据固定输入和专业复查独立裁定闭合。R1/R2提供全章阅读，本次只覆盖新差异及影响范围。

教学finding无未解决blocking或待补证据。审校由真实独立AI会话完成，Parent调查并裁决，没有投票或把空finding自动当作验收。此记录只支持教学文本与任务组织；专业内容审校、实际页面和项目最终验收各依其当前证据，真实教师/学生效果尚未验证。
