# 第六章作者修订记录 1

- 目标文件：`manuscripts/ch06/ch06.md`
- 修订后 SHA-256：`23256b7f7091250591489ade370140339e05a39739876905410e5281f25a67aa`
- 修订位置：第6.2节数据字典 `candidate_hours_per_day` 行（同时同步源片段 `manuscripts/ch06/s6-2.md`）；全文合稿 `manuscripts/ch06/ch06.md` 已由opening、五节和closing重新组装。
- 修订内容：将“0至24之间；不得大于基线”改为“0至24之间；允许大于基线，并明确标记为候选情景估算增耗，不称节能建议”。
- 修订理由：候选运行时间高于基线是合法的方案比较输入，程序保留带方向的差值，并以 `SCENARIO_INCREASE` 标记估算增耗；E04练习也使用了候选9小时、基线8小时的情景。旧数据字典条件与正文的方向解释、练习、题解和已测实现冲突。超过24小时、未知或受保护状态的暂停规则不变；未改动程序和计算逻辑。
- 验证：`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v`：13项通过；`PYTHONDONTWRITEBYTECODE=1 python3 ../verify_exercises.py`：10个数值/示例案例与12项行为检查通过。
