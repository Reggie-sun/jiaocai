# Chapter 3 Authoring Brief

## Scope

新写第三章三节，每节约8500—9500汉字，沿`specs/ch03.spec.md`、`plans/ch03.plan.md`与主Skill。文字必须自足，图只规划。本brief在来源调用与作者工作期间保持冻结。只用当前提纲和样稿；旧前四章不取材。每节正文是学生教材，用中文标题；英文section title规则适用于Spec/plan/report等工程artifact，不覆盖教材标题。

## Source Map

以下固定引用号在组装时由Parent检查首次顺序。论断—来源—实际支持范围由Parent独立核验，不把机构报告当全部产品效果证明。

| ID | Primary source | Safe intended claim and boundary |
| --- | --- | --- |
| [1] | Computer History Museum. Apple Macintosh, 1984. https://www.computerhistory.org/revolution/personal-computers/17/303/1203 ; screenshot https://www.computerhistory.org/revolution/artifact/303/1200 | 1984 Macintosh采用图形桌面、窗口图标菜单和指向设备；不是GUI起源、乔布斯个人独创或单手操作优化证明。跨学科分析明确是作者教学解读。 |
| [2] | WING J M. Computational thinking. Communications of the ACM, 2006,49(3):33-35. DOI:10.1145/1118178.1118215. https://www.cs.cmu.edu/~15110-s13/Wing06-ct.pdf | 计算思维超越编程并可联系其他领域；不重复第一章历史，问题类型—步骤—工具为本书框架。 |
| [3] | XIAOMI CORPORATION. Annual Report 2024. https://ir.mi.com/system/files-encrypted/nasdaq_kms/assets/2025/04/24/5-27-15/%E8%8B%B1%E6%96%87.pdf | 公司报告描述手机/AIoT与设备连接战略；只据此说明报告中的跨设备主题，不能证明社区反馈天然代表全部用户、每种设备互通或特定迭代因果。不要杜撰雷军对白/研发经历。 |
| [4] | LONG D, MAGERKO B. What is AI literacy? Competencies and design considerations. CHI 2020, 1-16. DOI:10.1145/3313831.3376727. 作者实验室入口 https://computationalliteracies.net/publications/long-2020-what/ | AI素养不只是点击工具，也包含理解、评估、交流与使用；不用作者论文替本纲四维分类背书。 |
| [5] | UNESCO. AI competency framework for students. Paris:UNESCO,2024. https://www.unesco.org/en/articles/ai-competency-framework-students | 原框架四维是human-centred mindset/ethics of AI/AI techniques and applications/AI system design，三级understand/apply/create。与本纲四维不同，只作对照与渐进学习依据，不称其证明本课课堂效果。 |
| [6] | TABASSI E. Artificial Intelligence Risk Management Framework (AI RMF 1.0). NIST AI100-1,2023. DOI:10.6028/NIST.AI.100-1. https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf | 可信性涉及有效可靠、公平及有害偏差、隐私、透明责任等，指标需情境化。不宣称法律合规或单一公平指标足够。 |
| [7] | AUTIO C, SCHWARTZ R, DUNETZ J, et al. Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile. NIST AI600-1,2024. DOI:10.6028/NIST.AI.600-1. https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf | confabulation、隐私、信息完整性与人机配置风险；结果流畅/自评不提供事实保证。三重校验为本书教学方法。 |
| [8] | BROWN T B, MANN B, RYDER N, et al. Language models are few-shot learners. NeurIPS33,2020:1877-1901. https://arxiv.org/abs/2005.14165 | GPT-3为autoregressive语言模型；上下文少样本与参数训练区别。不是所有今天AI仅是同一GPT3机制；不承诺提示改写必然正确。 |
| [9] | GRESHAKE K, ABDELNABI S, MISHRA S, et al. Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection. AISec2023:79-90. DOI:10.1145/3605764.3623985. https://arxiv.org/abs/2302.12173 | 外部检索数据可包含恶意指令、影响接入应用；不能把一句“忽略恶意指令”视为充分系统安全。 |

## Section and Exercise Boundaries

Writer A只写`s3-1.md`与`answers-e01.md`、`answers-e02.md`。重点从Macintosh可观察界面→用户动作/反馈→计算机×数学×工程×科学整合，接小米跨设备的条件/接口/反馈局限，再用明确模拟的金融风控展示领域规则改变标签、误伤和评价。金融材料无真实个人数据，不提供投资或真实授信建议；不声称蚂蚁集团有特定算法或300特征。E01简单跨领域需求/表示/评价，E02风控模拟记录分析，提供固定材料、基础/应用/拓展和评价。正文表号暂从表3-1起，最多必要数量。

Writer B只写`s3-2.md`与`answers-e03.md`、`answers-e04.md`。重点四维，逐步解释记录/标签/覆盖/误报漏报/训练测试/推荐反馈/隐私授权/结果校验，医疗影像只做数据审查，不给诊断；人脸识别只做模拟错误比较，不推断种族本质。E03可计数数据/分组任务，E04推荐或研究助手的事实—逻辑—伦理分析，提供候选文本和可追溯材料；引文必须检验而非品牌承诺。表号暂从表3-10起，Parent统一重编号。

Parent负责3.3与章首章末，E05校园节能候选的数量与证据核验，E06综合人机协作计划。表号暂从表3-20起。3.3不重讲3.2完整数据/伦理基础，而增加生成机制、检索来源边界、候选结构差异、验证成本和实际证据驱动修订。仅模拟AI文本，不进行真实农药或设施控制。

## Teaching and Verification

每节先导语，首小节首段完整描述案例再分析，基础例子自然语言讲明再引术语。中段连续段落解释理由与中间步骤，表格只用于必要比较、数据或可操作记录。最后教学小节给独立训练，之后反思。例题在正文完整讲解，独立训练的关键结论与详细答案仅在单独答案文件；组装后统一章末。练习数据不能和例题相同。

每一练习注明模拟、数据/来源/单位/条件、任务、提交物和评价；未知标未知，条件变化后重新检查。开放题有可评价参考分析及允许不同合理方案。基础可手工完成，程序仅替代，不要求外部账号。请实际计汉字数，不足时补有价值的示范、反例、迁移和应用解释；不能用重复警告凑数。

## Delegation Contract

Role：bounded writer；Authority：仅assigned exact files write-capable，其他read-only。Boundaries：不改共享规则、Spec/plan、brief、来源包、记录、引擎或其他作者文件；不commit/stage/push，不新增依赖或external CLI，不调用任何其他provider或subagent。你并非独自在workspace，必须保留他人修改。Nested delegation禁止。遇更高规则或ownership冲突停止报告Parent。最多本次起草加一次Parent明确指出缺口后的修正，不自行无限续写。

Expected output：实际写入的文件、字数、练习数值和采用来源、完成核验/剩余限制；不要在聊天返回整节。Parent持有最终整合与critical claim verification。
