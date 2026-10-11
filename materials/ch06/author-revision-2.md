# 第六章作者修订记录 2

## 变更范围

- 修订项：C6-P01、C6-P02、C6-P03、C6-P04。
- 正文 `manuscripts/ch06/ch06.md` SHA-256：`900bb39564d336ee0c58089f110720813225a42d4a033a61794a46c5f8995b77`。
- 原型 `materials/ch06/project/prototype.py` SHA-256：`b634101c71bd7d2439088a4f998d81c714aaccd9380bb726a499992a3836f4d9`。

## 修订位置与理由

- C6-P01：`project/prototype.py` 中 `analyze_dataset` 的所有分区结果现在保存 `input_snapshot`；`render_report` 为READY与HOLD分区显示灯具数量、单灯功率、基线与候选时长、应急照明状态及单位，并原样显示`source_note`。`project/expected-output.txt`已由原型重跑生成。这样A区读者可独立复算，D区的保护状态与来源也可追溯；状态、计算值、汇总边界和离线行为不变。
- C6-P02：`_decimal`现在只接收`int`、`float`、`Decimal`，明确拒绝`bool`、字符串和`None`。`project/README.md`与正文6.2.2数据字典后的接口说明已注明JSON数字类型约定，灯具数量及比较期要求JSON整数。
- C6-P03：价格显示改为完整十进制输入文本，金额仍按分四舍五入。新增0.625单价回归，确认99.36 kWh × 0.625元/kWh = 62.10元，报告显示的单价与金额可复算。
- C6-P04：集中答案E04已改为“沿用正文A区教学数据”，并点明48盏、18瓦/盏、12小时基线与10.5小时候选，消除与E02区域X数据的混淆。

## Red-Green Evidence

- Red：先加入5个行为测试（旧13项共18项）；首轮18项测试结果为6 failures、1 error。失败证据覆盖READY/HOLD缺少输入快照与来源、数字字符串被当数值接受，以及0.625被显示为0.63。测试组合包含数字、数字字符串、非数字字符串、布尔和null；期间没有先改实现。
- Green：完成实现后，调整两条断言以匹配报告中有引号的JSON字符串状态值和`source_note`字段标签；最终完整运行18项测试，全部通过。随后练习复核输出`PASS: 10 numeric/example cases; 12 behavior checks`，并实际重生成`project/expected-output.txt`。
