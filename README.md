# jiaocai

为西南财经大学计算机专业大三、大四学生编写完整十章教材。教材目标、材料与进度见 [现状记录](教材编写现状与目的.md)，教学方法见 [textbook-authoring](/home/reggie/.local/share/chatgpt-desktop/skills/textbook-authoring/SKILL.md)。

## Authoring

教学方法的版本化owner是 [textbook-authoring](skills/textbook-authoring/SKILL.md)，本机安装入口转接到该文件。当前质量改进契约见 [质量规格](specs/authoring-quality.spec.md)，第一章增量见 [ch01-quality.spec.md](specs/ch01-quality.spec.md)。第一章仅为第一轮基线；后续章的Spec应独立校准读者起点、知识增量及合适的分析/实践，不复制本轮案例或组织样式。

整章交付前按主Skill安排独立专业内容与教学阅读审校，具体发现、Parent裁决和实质修改后的复查并入现有核验材料。Harness五项审校与接口保持不变。独立QA的存在不能把Parent汇总自审改名成独立整章审校，机器或AI判断也不能代替真实教师/学生验证。

模型根据学习目标自主选择策略、任务拆分、工具与修改顺序。章级spec约束交付内容与质量，plan提供依赖和里程碑；不要求逐条照演命令。探索、试写、检索、改稿与分节合并无需逐次登记或验收。按章推进时默认只在整章交付节点验收，只有实际交付独立蓝图或单节时才为该范围登记run。

## Delivery

`harness.json` 与 `scripts/harness.py` 独占工程状态和证据规则。稿件准备交付时，按 [run模板](templates/run.example.json) 填写实际范围、文件、图表、材料和待办，然后运行：

```bash
python3 scripts/harness.py start --id ch01-draft --spec runs/ch01-draft.spec.json
python3 scripts/harness.py check --id ch01-draft
python3 scripts/harness.py review-template --id ch01-draft > runs/ch01-draft.review.json
# 实际审校当前快照，填写审校类型、审校者、时间和五项依据。
python3 scripts/harness.py review --id ch01-draft --evidence runs/ch01-draft.review.json
# 在现状记录写入稿件链接、scope/stage、完成范围、图表进度与未决事项。
python3 scripts/harness.py accept --id ch01-draft
```

`start` 仅首次登记，也可以提前用于接续记录；已有run不再start。`check` 自动读取最新spec并重新检查当前文件，保留历史，不需要先status或resume。原检查通过且所有依赖未变时，重复check直接保留检查和审校。正文、图表、材料、spec、核心输入、实际质量门槛或脚本变更后重新check，再审校受影响内容；审校证据必须绑定整个当前快照，不能仅改时间或哈希复用旧结论。

审校文件填错，可修正后直接重试review；缺少进度链接，可补齐后直接重试accept。这两种恢复仍重新核对证据新鲜度。`resume` 保留为主动清除当前证据、重新登记的兼容入口，通常无需使用。

```bash
python3 scripts/harness.py status
python3 scripts/harness.py validate
python3 -m unittest discover -s tests -v
```

status只读，默认提供简短概览，指定 `--id` 查看完整历史与证据。它报告保存状态、`effective_state`、`stale_reasons` 与审校类型；发现变更时退出1，旧accepted不能继续当作当前交付。交付文件变更后必须重新check/review/accept；旧交付的范围与证据保留在历史中。说明性policy文字、其他run和日常进度更新不会使稿件证据失效，真正的门槛与依赖仍严格比较哈希。

## Evidence and Quality

机器检查验证声明的结构、文件、图表登记、状态和快照。内容审校另评估教学适配、来源支持、练习及答案、图表语义和章间一致性。必须实际通读、核算、查原文和查看采用的图；关键词与文件存在不证明教学质量。

新审校证据使用 `review_kind`：`ai_self` 为编写模型自审，`independent` 为另一个实际审阅当前快照的独立审校者，`human` 为真实人工审校。填写身份和实际依据，独立性不能由改角色名获得。历史未分类记录显示 `legacy_unspecified`，不自动升级为独立审校。Harness记录所声明的类型，无法认证身份或替代真实学生试读、课堂试教及校方验收。

draft仅接受声明范围的初稿，可保留公开待办；final拒绝待办、占位、未完成图表和pending审校，完整章仍检查篇幅及必需配图。两种阶段都拒绝缺失正文、材料或ready图，且交付时验证和审校必须对应最终文件。原始材料保留；Word/PDF版式与正式字数另行检查。
