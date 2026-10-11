# AI Mechanism Claim Investigation Package

## Scope
对以下八项教材拟用机制及限定逐条核对，依据实际原文excerpt而非原提纲的宣传性概括；不审Spec/Plan，不评价尚在写的整章。原文包含两个栏的提取，请按上下文阅读。

## S11 Deep learning
多层表示由训练形成，局部连接/共享权重；不是保证各层总有唯一语义。
位置：Introduction; Convolutional neural networks
原文：https://www.cs.toronto.edu/~hinton/absps/NatureDeepReview.pdf
边界：真实研究只支持机制；本章小案例/候选/数值为原创模拟，不能推出真实模型性能。

## S12 Attention Is All You Need
注意力依据查询与键的匹配组织值，序列位置需表示；原实验翻译，不直接证明电网预测效果。
位置：Section3.2 Attention;3.5 Positional Encoding
原文：https://arxiv.org/pdf/1706.03762
边界：真实研究只支持机制；本章小案例/候选/数值为原创模拟，不能推出真实模型性能。

## S13 Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization
目标类别梯度与最后卷积层产生粗定位图，不是因果解释或临床结论。
位置：Abstract; Section3 Grad-CAM
原文：https://arxiv.org/pdf/1610.02391
边界：真实研究只支持机制；本章小案例/候选/数值为原创模拟，不能推出真实模型性能。

## S14 Communication-Efficient Learning of Deep Networks from Decentralized Data
本地计算更新、按样本量聚合；原始数据不集中不等于更新无隐私风险。
位置：Algorithm1; Federated Averaging
原文：https://proceedings.mlr.press/v54/mcmahan17a/mcmahan17a.pdf
边界：真实研究只支持机制；本章小案例/候选/数值为原创模拟，不能推出真实模型性能。

## S15 Deep Leakage from Gradients
论文条件下共享梯度可泄露样本；不是所有聚合都必定被还原。
位置：Abstract; Section2/3 gradient inversion
原文：https://arxiv.org/pdf/1906.08935
边界：真实研究只支持机制；本章小案例/候选/数值为原创模拟，不能推出真实模型性能。

## S16 FeUdal Networks for Hierarchical Reinforcement Learning
具体架构高层设目标、低层执行动作，不代表所有AI自动识别正确任务边界。
位置：Abstract; Manager and Worker architecture
原文：https://arxiv.org/pdf/1703.01161
边界：真实研究只支持机制；本章小案例/候选/数值为原创模拟，不能推出真实模型性能。

## S17 Human-level control through deep reinforcement learning
在游戏观察与奖励中学习动作价值，实验效果不推广到校园/无人机，硬约束须另行验证。
位置：Abstract; Methods DQN/replay
原文：https://storage.googleapis.com/deepmind-media/dqn/DQNNaturePaper.pdf
边界：真实研究只支持机制；本章小案例/候选/数值为原创模拟，不能推出真实模型性能。

## S18 Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks
元训练得到易于在新任务上少步适应的初始化，并非普遍自动选优化器/永不需人工评估。
位置：Abstract; Algorithm1
原文：https://proceedings.mlr.press/v70/finn17a/finn17a.pdf
边界：真实研究只支持机制；本章小案例/候选/数值为原创模拟，不能推出真实模型性能。

