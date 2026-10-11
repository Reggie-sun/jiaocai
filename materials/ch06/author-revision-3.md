# 第六章作者修订记录 3

- 修订项：C6-P05（README精度说明）。
- README修改前 SHA-256：`8c613fd1f0c0245c3982b0ae9794f03e267c9f49236f467b5ca2f0e8488d38ab`。
- README修改后 SHA-256：`e730258db62a5e1ce9325968e86c0a948ed67c0228c5fd5541c8f24ee3debf81`。
- 正文未变，SHA-256仍为：`900bb39564d336ee0c58089f110720813225a42d4a033a61794a46c5f8995b77`。
- 原型代码未变，SHA-256仍为：`b634101c71bd7d2439088a4f998d81c714aaccd9380bb726a499992a3836f4d9`。

## README精确差异

旧文：

> The report prints the teaching price at its supplied decimal precision; only monetary totals are rounded to cents, so the displayed amount can be recomputed from the displayed price and energy.

新文：

> The report prints the teaching price at its full supplied decimal precision and displays energy quantities rounded to 0.001 kWh. Monetary amounts are calculated from unrounded energy values and the full input price, then rounded to cents. Because displayed energy is rounded, multiplying the displayed energy by the displayed price may differ from the reported amount by a cent. Reproduce an exact amount from the original inputs and formula, not from the rounded energy display.

## Actual Runtime Check

通过内存输入实际调用原型（未改写输入文件）：比较期30天；A区48盏×18瓦/盏；基线12小时/天；候选11.9997小时/天；教学模拟价0.625元/kWh；保护状态`confirmed_no`。实际报告关键输出：

```text
比较期：30天；教学模拟价：0.625元/kWh
基线/候选：311.04 / 311.032 kWh
基线减候选：0.008 kWh
模拟金额差：0.00元
通过检查分区的基线减候选电量合计：0.008 kWh
通过检查分区的模拟金额差合计：0.00元
```

独立使用原始输入复算：`0.864 × (12 − 11.9997) × 30 = 0.007776 kWh`；未舍入金额`0.007776 × 0.625 = 0.00486元`，按分显示`0.00元`。若误用报表显示电量复算，`0.008 × 0.625 = 0.005元`，四舍五入为`0.01元`。故README现明确指出电量显示按0.001 kWh舍入、金额使用未舍入电量、价格保留完整输入精度，精确复算须从原始输入和公式开始。
