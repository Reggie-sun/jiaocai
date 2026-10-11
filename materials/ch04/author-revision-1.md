# Revision Record

## Baseline

本轮修订基于审校快照 `98b48cda79a75408677601a1fc5d491e46fba4c3d4d233a96a04fe6a3fa268a6`。修订涉及 `manuscripts/ch04/**`、`materials/ch04/author-exercise-verification.json` 与本记录；未改布局稿、绘图manifest、进度记录或Harness文件。

## Applied Revisions

| Review ID | Location | Rationale and change |
| --- | --- | --- |
| C4-T01 | `manuscripts/ch04/s4-1.md` 至 `s4-4.md`；同步 `ch04.md` | 在每节标题后、案例小节前补入两句导语，交代本节学习方向及与前文的关系，不提前给案例结论。 |
| C4-P01/T02 | `manuscripts/ch04/s4-2.md` 的“伪相关与因果越界”小节；`manuscripts/ch04/closing.md` 的E03题干、评价与参考解；同步 `ch04.md` | 以自然语言解释随机分配如何减少自选差异、观察比较为何要求两组在影响结果的重要条件上可比，以及未记录因素和参与度分层仍可能留下差异；补充课程提醒比较设计，并在正文中解释“（条件）交换性假设”。E03现要求说明如何检查可比条件和剩余不确定性，参考解改用已铺垫的知识回答。 |
| C4-T03 | `manuscripts/ch04/closing.md` 的E05题干、评价与参考解；同步 `ch04.md` | 明确区分使用模拟来源进行的隔离组件规则测试，与依赖实际人工入口和责任人的端到端测试。答案要求记录缺失入口和责任人，不能将模拟停止状态称为已转接，也不能把离线规则通过表述为完整流程通过；真实用户运行前须具备实际人工路径。 |
| C4-Parent01 | `manuscripts/ch04/s4-1.md` 至 `s4-4.md`；同步 `ch04.md` | 按教材样式将40个教学三级标题依次编号为`4.N.M`，涵盖案例、知识小节、训练和本节反思。章末E题及其他功能标题保持原样。 |

## Verification

- `materials/ch04/verify_exercises.py`：40项数值复算全部通过；输入数据未改。
- 整合结构检查通过：四节导语位于案例之前；四节下三级标题连续编号；图4-1至图4-6与图注清单一致；表4-1至表4-9连续；E01–E06题目与章末集中参考解对应；文献首次引用顺序为[1]至[4]。
- Han字数为32,147，统计时排除代码围栏和URL，符合本章2.8万至4万字要求。
- 修订后的独立读者定向复核尚待Parent安排；以上检查不代表复审或最终验收。

## Final Snapshot

`manuscripts/ch04/ch04.md` SHA-256：`dd6eab95dc5dc3d23619445d352e0c2b522303edff974cc344d671f5b83d7e99`
