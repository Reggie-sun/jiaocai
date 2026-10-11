# Ten-Chapter Teaching Rules Plan

## Goal and Scope

按[质量规格的十章增量](../specs/authoring-quality.spec.md#ten-chapter-continuity-amendment)，把前三章审校中确认的可迁移经验固化到现有主Skill，供十章持续起稿与修订引用。Parent为唯一writer与裁决者。本轮不改教材正文、图、正式输出或开始新章。

## Ownership and Contracts

修改`skills/textbook-authoring/SKILL.md`作为唯一教学方法owner，`specs/authoring-quality.spec.md`仅维护当前范围、适用关系与Q7，不复制方法目录。新增本Plan与`materials/ch01-03-review/ten-chapter-rules.md`记录继承依据、取舍和验证。安装Skill只转接，AGENTS继续保留已有入口。

保持`Formal Textbook Style`、DOTX、Harness引擎/状态机/五项接口、Agent路由和历史审校记录。共享目的记录及第四至六章属于另一会话的在途工作，本轮不写入或提交。规则继承记录保存本次确认及完成状态，通过质量规格链接可发现，不接管他人的进度文件。

## Milestones

1. 对照实际主Skill、质量规格与前三章裁决，选择可迁移且尚不明确的要求；已有合理规则只补必要细节，不把单章内容变成十章统一模板。
2. 将原纲核对、知识依赖/新增能力、术语桥接、练习分层/迁移、图中答案与数值/来源边界分别写入已有owner；当前质量规格注明增量及历史Scope身份。
3. 检查入口、相对链接和规则冲突，比较正文/正式输出及样式字节，运行Harness只读`validate`/`status`。保留因规则依赖变化而失效的实际证据，不重写历史验收；审阅精确diff，仅提交本轮四个文件。

## Acceptance and Verification

Q7的规则均有既有审校问题或教学要求作为依据，后续章级Spec可以引用唯一owner。读取安装入口并核对其指向，实际解析新增Markdown本地链接及标题锚点；`git diff --check`、正文/输出/样式哈希比较和Harness只读检查完成。不添加模拟教学评分测试，不为无正文变化重复渲染Word/PDF。

## Self-Review

这是原跨章审校任务的规则继承增量，受管Kimi与Native独立内容意见已实际提供，Parent在现有裁决基础上提炼；不新增重复审校或重置调用预算，也不声称新规则获得独立者复审。文档规则修改无关键级凭据、越权或生产状态后果；稳定候选在验证后由Parent判断Implementation Review Risk Gate。有效性由后续稿件与真实试读检验，本次只确认规则可用、范围清楚与原产品不变。
