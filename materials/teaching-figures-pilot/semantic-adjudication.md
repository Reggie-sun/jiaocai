# Semantic QA Adjudication

## Scope and Route Evidence

受管Kimi `deep` 只读检查冻结的正文摘录、分钟/边集合数据和Spec/plan；未查看图片、灰度或Word/PDF，不是最终实现review。封存hash为 `0b3b29426f75bf8032f38040f1158b9c7945a137a1fab11d74d95a708a8bde27`，invocation为 `b6a5d6cc-a437-461f-8a27-37eb739cb7fa`。canonical receipt、原报告和可观察执行分别保存在本目录 `semantic-receipt.json`、`semantic-worker-report.json`、`semantic-execution-view.json`。Parent已核对完整Read及hash；`PARSED`只表示协议完成。

## Finding Resolution

| Finding | Parent decision and evidence |
| --- | --- |
| TFQA-01、02、03、10 | 确认语义基线：六条允许边、容量1、3项请求/2个可达位置、孤立d。XML和8种候选组合直接核验，无可行安排；不把必要条件画成充分条件。候选完整保留。 |
| TFQA-04、05、09 | 确认60分钟重叠与半开区间相接不重叠。三图面板有实心起点/空心终点及共同占用60/0标签；相接线不作为重叠区域。 |
| TFQA-06 | 确认有效占用为A `[540,680)`、B `[645,720)`，交集35分钟。拒绝报告中的子结论“660–680是B布置与A清理重叠”：B布置在660结束，该段实际为B活动与A清理重叠。图与生成数据未采用此错误拆分；前段645–660为B准备与A活动重叠。 |
| TFQA-07 | 确认条件性要求。第三面板标题与共同正文均注明准备/清理独占同一场地；不能推广到场外准备。 |
| TFQA-08、11 | 确认三例需区分。用三个独立面板、同一9至12点尺度，B在不同面板的起点明确；数据按分钟核验，没有合并成一条活动叙事。 |
| TFQA-12 | 确认原创教学示例的来源边界；图、题注、数据均不称实测或E01/E03练习数据。 |

PC-1、PC-2、PC-3的教学约束已落实。PC-4双标“午夜起算分钟/钟表时刻”不采纳：图中保留钟表时刻及60/0/35分钟，原始分钟值在 `data.json` 可复算；同时画540/9:00等重复数字会增加版面负担。不是删除核验数据。

三个问题由最终图回答：采用独立面板；准备/清理有独立纹理与条件标题；Parent及独立native视觉QA实际查看最终图片和四页插入效果。没有未解决语义blocker，也没有要求Kimi对其未见图片宣布验收。
