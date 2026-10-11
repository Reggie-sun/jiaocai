# Chapter 3 Text Draft Delivery

## Result and Scope

2026年10月12日，按用户“写第三章”完成《计算思维与人工智能素养》的[完整文字稿](../../manuscripts/ch03/ch03.md)。[Spec](../../specs/ch03.spec.md)及[Plan](../../plans/ch03.plan.md)在当前写作授权内由Parent自审后执行，沿用`textbook-style-v1.0`。原提纲实际为三节，早期蓝图的四节未覆盖原纲；旧前四章未参与正文、案例、引用或结构取材。

最终稿约35,742汉字，包含三节、章首章末、E01—E06及集中参考解，12张连续编号的教学表和9项参考文献。[统计](assembly.json)排除代码和链接目标，包含答案与题注，不等同Word或出版社字数。完整稿SHA256为`38d90d7a397ba98f0279055838bf4aace2cd76cddf684001609cee748e719709`。

| Section | Title | Knowledge and student action |
| --- | --- | --- |
| 3.1 | 计算思维的演进与跨学科融合 | 从界面目标、表示与反馈出发，解释数学、工程、科学与人文知识怎样改变条件；跨设备状态与模拟金融核验落实领域知识、误报漏报及有限处理能力。 |
| 3.2 | 人工智能素养：四大核心维度 | 从八条图像质量记录起步，建立数据意识、算法理解、伦理安全和生成式AI驾驭；计算分组错误并审查有材料支持的研究助手候选。 |
| 3.3 | 生成式AI与高阶思维 | 从模拟校园节能候选进入生成机制、任务组织、事实/逻辑/伦理核验、检索与工具边界；比较结构不同的方案，设计有限验证和学习行动。 |

C1通过领域条件与E01/E02落实；C2/C3通过小数据、分组计数和反馈落实；C4通过授权、隐私、公平、纠错与E04落实；C5通过生成候选及E04/E05落实；C6由E06综合协作计划落实。基础任务可纸笔完成，无账户或模型训练前提，应用/拓展增加条件。实际史实、机构/企业报告主张、作者分析与教学模拟分开陈述，四维沿用本纲，不冒称UNESCO分类。

## Content Review and Corrections

两个不同实际只读Native会话分别完整审读r1的1—798行，一个负责专业机制/来源/数据，一个负责教学入口/递进/任务/重复。两者独立发现E02把未被提醒的记录作为队列排序候选，Parent确认并修正：排序仅用已有提醒，漏报另设发现入口并重新检查容量。教学审校还发现E04量规提前提示关键答案，已改为一般评分条件，具体分析保留章末。

原会话分别实际读完r2完整差异及受影响区间复查；未变内容只按字节一致继承初审观察。没有未解决blocking。实际报告、范围、快照与Parent裁决见[内容裁决](content-adjudication.md)及四份报告；数值或审校者意见均不自动构成真实教学验收。

## Source Investigation

受管Kimi以封存、qualified Docker route和canonical receipt完成固定七组论断的只读调查，`deep` route，invocation `f6daca78-1078-46a3-81f7-7e5aa4e2d7f6`。实际Read范围、报告哈希、预算、资格和状态见[source-run-r1.json](source-run-r1.json)、[source-receipt-r1.json](source-receipt-r1.json)。`PARSED`和exit 0只表示执行/协议结果，Parent另核实际读取与报告。

唯一确认发现是来源包未覆盖正文拟用的全部NIST风险类别；Parent查原始文本后增加独立补充文件，原封存材料不改。整章专业审校实际读取补充；不声称Kimi复查新材料，也不把七组来源调查说成全章或整篇论文审读。小米和UNESCO部分依据由Parent通过浏览工具核对，范围限制与原始文件路径纠正保留在[source-supplement.md](source-supplement.md)。

## Executable Verification

- `python3 materials/ch03/assemble.py`：三节原题、字数范围、连续表号、六个对应答案、首次引用顺序与书目一致；记录全部组件及完整稿SHA256。
- `python3 materials/ch03/verify_exercises.py`：38项PASS，从实际题表复算计数、人数/分组、提醒成员、能耗、容量/照明约束、预算与变化条件。对应输入哈希见[练习核验](exercise-verification.json)。
- 原Harness的51项测试PASS，实际输出见[harness-tests.log](harness-tests.log)；`python3 scripts/harness.py validate`通过，见[harness-validate.json](harness-validate.json)。引擎与policy未改。
- 只读`status`的exit 1来自五个旧快照的已存在stale状态；`ch02-progressive`与`ch01-history-layout`当前accepted。新第三章没有实图，不登记缺图的完整chapter acceptance、不刷新或改写历史run，见[harness-status.json](harness-status.json)。

最终快照、审校溯源、工程Risk Gate及保护检查汇总见[verification.json](verification.json)。工程Risk Gate对新稿及两个本地组装/核验脚本判断为`KIMI_REVIEW_NOT_REQUIRED`：用户未要求工程Kimi审查；没有凭据/授权/public contract或生产持久状态变更；本地脚本只写本轮可重建材料，失败后果和剩余运行时缺口不满足重大风险联合条件。教材内容的两个独立审校职责已另实际完成。

## Figures and Remaining Work

[五幅图计划](figures.md)全部planned。正文自足，图后期统一制作，尚未生成实图、核验图义/像素或制作Word/PDF。采用实图后再核图文、正式排版和登记当前完整章快照；不能借用前两章的图或历史acceptance。

真实教师/学生试读、课堂试教、实体打印和校方/出版社审定仍待完成。所有医疗、金融、人脸和照明数值情境均为明确教学模拟，不表示真实系统性能或实施效果。

## Workspace and Handoff

开工HEAD `339c970719ba898d210002390c395020aeeca8fb`，沿用当前`chapter-02-delivery`工作树和branch，无新worktree。只新增第三章Spec/plan、源稿与materials，并顺序追加[目的记录](../../教材编写现状与目的.md)。793项保护基线中原tracked和另一会话未跟踪资料均保留；唯一授权变化是目的记录的顺序追加。第二章未跟踪来源资料及`tests/__pycache__/`不stage。

两个writer的精确文件集合互斥，退出写作后Parent接管修订；两个reviewer全程read-only。Final diff、保护哈希与已知工作区核验由Parent完成。只stage本轮owned文件，在稳定checkpoint commit、push并对比remote SHA。当前repo未提供专用session-record/capture入口，本报告和目的记录承担交接；不更新全局memory。下一步为后期图稿与排版，或用户授权的其他章节编写。
