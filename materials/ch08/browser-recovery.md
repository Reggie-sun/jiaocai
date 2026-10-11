# Browser Verification Recovery

## Actual Failures and Correction

Chrome MCP的new_page因共享profile已被使用而失败。Parent未关闭或读取已有用户tab；改用临时自有profile、loopback CDP、Node24内置WebSocket，无新依赖。第一次自有浏览器截图在10秒内未返回；子进程已结束，未产生通过结论。加入既有图导出采用的disable-gpu、disable-dev-shm-usage并限制viewport截图后，截图可取得。

实际键盘轨迹显示七次Tab进入四字段，日期原生月、日、年和日历按钮占多个Tab停点。原CSS在日历按钮停点使host不匹配:focus-visible，外框为none；作者补date的:focus-within。补后该停点仍不匹配host的:focus-visible，但实测outer outline已经为蓝色solid3px。Parent原断言错误地把host伪类当作可见焦点必要条件，已改为验证实际computed outline并保留伪类值及截图，不能把日期内部停点遗漏。

## Acceptance Boundary

所有失败不构成通过。最终JSON必须由修正后的实际一次完整前进、反向键盘走查生成，Root打开截图后另记录视觉观察。无真实用户、第二引擎、屏幕阅读器或两周学习效果验收。
