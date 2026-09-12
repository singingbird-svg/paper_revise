# Related Work 修改方案：以“提前获得可执行方案”为主线的审稿式重构

## 0. 结论先行

我建议**不要把 Related Work 写成“LTL-MRTA 方法大全”**，而是围绕本文真正需要回答的一个问题组织：

> **对于由全局 LTL 指定、且具体机器人身份未预先分配的异构多机器人任务，现有方法分别在哪一个阶段降低计算负担？为什么这些努力仍没有直接解决“在自动机尚未完整生成时就利用团队可行性和部分分配信息、尽早得到可执行方案”这一问题？**

这条主线比“现有方法计算慢”更精确，也比“我们支持在线重规划”更能体现本文的独特位置。

当前 Related Work 已经覆盖了 bottom-up/top-down、product automaton、sampling、STAP/MILP、planning decision tree、poset、HLTL 等主要方向，但仍有三个问题：

1. **分类依据不够统一。** 前半部分按 bottom-up/top-down 分类，后半部分又在 sampling、MILP、PDT、poset、HLTL 之间连续切换，读者能看懂文献，但不容易看出这些方法和本文的核心差别到底在哪里。
2. **最接近本文的工作没有获得最高写作权重。** 真正需要重点比较的是：
   - 快速 first feasible solution / anytime：PDT、poset；
   - 复杂 specification 的处理：HLTL / structured formulations；
   - 不走显式自动机规划流程的另一条路线：learning；
   - 以及这些方法和本文“把 allocation 前移到 GBA/NBA generation”之间的本质差别。
3. **结尾 gap 仍然偏宽。** “rapid first feasible plan + optimization + plan repair”三项一起作为 gap，容易让审稿人逐项寻找反例。更安全的 gap 应该落在**integration point**上：现有 model-based LTL-MRTA 通常在某种时序结构被构造/提取之后才进行机器人分配，而本文把团队可行性、部分分配和执行状态直接引入 automaton generation。

因此，我建议采用：

> **scope narrowing → conventional symbolic planning → fast/anytime allocation → structured specifications and learning alternatives → precise gap**

而不是继续增加更多文献类别。

---

# 1. 从三篇参考论文中，最值得借鉴的不是“模板”，而是三种写法

## 1.1 *An Exploration-Enhanced Search Algorithm for Robot Indoor Source Searching*

这篇论文没有单独堆一个很长的 Related Work，而是在 Introduction 中把已有方法压缩成几类，例如 biomimetic methods、probability-based methods。每一类的写法基本都是：

> 方法类别 → 代表性机制/代表工作 → 共同优势 → **共同假设或共同缺陷**

它最值得你借鉴的是：**不要逐篇论文平均用力，而是先找“共同机制”和“共同限制”。**

对应到你的论文：

- product-automaton / sampling-based methods 可以作为一组；
- decomposition / MILP 可以作为一组；
- PDT / poset 可以作为“early-feasibility / anytime planning”一组；
- HLTL / structured formulation 可以作为“change/exploit specification structure”一组；
- learning 可以作为“amortize temporal reasoning through training”这一条不同路线。

这样比现在“一个方法接一个方法”更紧凑。

---

## 1.2 *From Ambiguous Language to Verifiable Plans*

这篇论文的 Related Work 分成三个方向，每个方向几乎都和自己的一个核心模块对应，并在最后设置 `Summary and Research Gap`。

你不适合照搬“三个 subsection + comparison table”，因为你的创新不是三个彼此独立的研究方向，而是一条连续的计算流程：

> GBA pruning → on-the-fly NBA/plan-graph construction → early feasible plan → BnB refinement → repair

但是它有一个非常值得借鉴的原则：

> **每一组文献的最后一句都应该自然推出本文的一个设计必要性。**

例如：

- product/sampling → 说明为什么不能只在完整 product 上做文章；
- PDT/poset → 说明为什么“first solution”很重要，以及为什么 preprocessing latency 仍值得关注；
- HLTL → 说明改变 specification structure 是有效路线，但有额外 formulation assumptions；
- learning → 说明 deployment-time action selection 可以很快，但计算被转移到 training，且依赖 learned generalization；
- 最后顺势推出：本文选择保留 model-based symbolic formulation，但把 planning information 前移到 automaton generation。

这比单独说“our method is faster”更有说服力。

---

## 1.3 *Temporal Logic Task Allocation in Heterogeneous Multirobot Systems*

这篇是与你最接近、最应该借鉴其“领域定位方式”的参考文献。

它先区分：

- local specifications vs. global specification；
- global specification 中 explicit robot assignment vs. no explicit assignment；

随后才讨论 decomposition、sampling、MILP、counting temporal logic 等方法。

你的 current Related Work 已经继承了这种思路，这是对的。但我建议进一步压缩第一层 taxonomy，因为你的问题定义已经很清楚：

> **本文只需要用一小段说明 bottom-up/local-LTL 不属于本文问题设置，然后立即进入 global LTL / no preassigned robot identities 的 top-down LTL-MRTA。**

没有必要对 bottom-up 方法展开太多，因为它们不是本文创新的直接竞争对象。

---

# 2. 从审稿人的视角看，当前版本最可能产生的疑问

## 2.1 “你到底是在解决 state explosion，还是 first-solution latency？”

当前 Related Work 同时讨论：

- product automaton state explosion；
- robot assignment combinatorics；
- MILP scalability；
- greedy local optimum；
- poset extraction；
- structured LTL；
- online repair。

这些都是相关问题，但如果没有一条更高层的线，审稿人会觉得你的 gap 在移动。

### 建议

明确区分两个概念：

- **overall computational complexity / scalability**
- **latency before an executable first plan becomes available**

本文最强的是第二个。

你的方法并没有改变 LTL-to-NBA 的 worst-case exponential complexity，论文自己也已经承认这一点。真正的创新是：

> **不再把“完整自动机生成”视为 task allocation 开始之前必须完成的 preprocessing。**

所以 Related Work 应该不断回到 `when can allocation start?`，而不是泛泛讨论“谁的复杂度更低”。

---

## 2.2 对 poset 方法的批评目前略显过重

当前文本强调：

> for an automaton with hundreds of states, the algorithm may require tens or even hundreds of seconds to obtain the first partial order.

即使这个事实来自原论文，这种非常具体的负面数字在 Related Work 中容易显得像在“挑 baseline 的弱点”，尤其当实验部分已经直接比较 poset 方法时。

### 建议

Related Work 中改成更中性的机制性表述：

> However, the partial-order structures must first be extracted from the task automaton, so the time to the first allocation can still increase with automaton complexity.

如果需要具体几十/几百秒，让实验部分的结果说话。

这样审稿人更容易接受，也减少“是否公平比较”的争论。

---

## 2.3 当前 HLTL 段落已经接近正确，但还缺一个“另一条路线”

你现在已经写到：

> Some work reduces the burden of complex specifications by changing or exploiting the structure of the task formula.

这是加入 learning 的最佳位置。

因为这里其实可以形成一个很清楚的二分：

### 路线 A：改变/利用 specification structure

- hierarchical temporal logic；
- conjunction of subformulas；
- poset products。

### 路线 B：不在部署时进行传统 automaton-based planning，而把一部分计算摊销到 learning

- LTL2Action [12]。

这样 learning 不是突然插入，而是回答同一个问题：

> **复杂 LTL 带来的部署时计算负担还能从哪里减少？**

---

# 3. Learning 内容应该怎么写才最安全

## 3.1 不建议写成

> Learning-based methods avoid automaton construction.

这个表述过宽。

你当前引用的 LTL2Action [12] 更准确的机制是：

- 用 **LTL progression** 表示任务剩余义务；
- 将当前环境状态和 progressed LTL instruction 作为策略输入；
- 训练 task-conditioned RL policy；
- 因此不需要为每个任务在部署阶段先编译 Büchi automaton 再进行传统图搜索。

所以更严谨的说法是：

> **learning-based approaches can avoid compiling each LTL instruction into an explicit automaton for deployment-time action selection**

而不是声称所有 learning 方法都“不要自动机”。

---

## 3.2 缺点也不要只写“需要很多数据”

LTL2Action 本身恰恰强调了：

- compositional generalization；
- unseen LTL instructions；
- environment-agnostic LTL pretraining；
- sample efficiency。

如果简单写成“需要大量训练数据、泛化差”，容易被熟悉该工作的审稿人认为过于粗糙。

### 更合适的批评角度

建议写成：

> This shifts a substantial part of the computational burden from online symbolic synthesis to offline policy training, and deployment performance depends on how well the learned policy generalizes to the encountered task and environment distribution.

然后再加一句限定其与本文的关系：

> Such methods are complementary to the model-based LTL-MRTA setting considered here, since they are not designed to explicitly optimize heterogeneous robot assignments under changing team composition with the same symbolic completeness guarantees.

这比“learning 方法不好”更公平。

核心意思不是否定 learning，而是说明：

> **它通过另一组 assumptions 换取 deployment speed；本文则研究在不引入 training requirement、仍保留 symbolic model-based planning 的前提下，如何减少 first-plan latency。**

这是最有利于你的位置。

---

# 4. 建议的详略分配

| 文献方向 | 建议篇幅 | 原因 |
|---|---:|---|
| Bottom-up/local LTL [14], [15] | 很短 | 只用于限定 problem scope，不是直接竞争方法 |
| Product automaton [9], [16] + sampling [10], [17] | 中等 | 说明经典 state-explosion 背景，但不是本文最直接创新点 |
| STAP/decomposition [18], [19] + MILP [7], [8], [20] | 中等偏短 | 说明 task allocation 与 temporal structure 解耦后的典型做法 |
| PDT [21], [22] | 中等偏重点 | 和你的“快速 first feasible plan”最接近 |
| Poset/anytime [3] | **重点** | 与 first-solution + subsequent improvement 目标高度一致 |
| HLTL / structured formulations [23], [24] | **重点但简洁** | 直接对应复杂 formula 的另一种处理思路 |
| Learning/LTL2Action [12] | **一小段，约 3-4 句** | 必须覆盖，但不是你的直接 baseline，不应喧宾夺主 |
| Final research gap | **重点** | 必须准确落到“allocation 与 automaton generation 的 integration point” |

---

# 5. 推荐的 Related Work 逻辑结构

## Paragraph 1 — Scope narrowing

目的只有一个：

> local-LTL/bottom-up 与本文不是同一问题设置；本文研究 global LTL、robot identities not preassigned 的 top-down LTL-MRTA。

不要在这里花太多篇幅讲在线协调细节。

---

## Paragraph 2 — Conventional symbolic top-down planning

按照“什么时候进行 robot allocation”来组织：

1. product automaton；
2. sampling-based approximation；
3. task decomposition/STAP；
4. MILP。

这里的共同结论不是“这些方法都很慢”，而是：

> 大多数方法仍然需要先获得完整或足够成熟的 temporal/task representation，随后才进入 allocation/planning。

---

## Paragraph 3 — Methods closest to early first-solution generation

重点讲：

- PDT；
- poset anytime。

这一段是最接近你的工作，因此要比 product automaton 段更细。

关键 contrast：

> PDT：增量表示和 greedy allocation → 很快，但 quality trade-off；
>
> poset：anytime + BnB → quality/anytime 很好，但需要先从 task automaton 提取 partial-order structure；
>
> 本文：把 integration point 再前移，直接在 GBA/NBA generation 中进行 feasibility screening 和 allocation。

---

## Paragraph 4 — Complex specification: structure-based vs. learning-based

先讲 HLTL / structured methods，再自然转 learning。

逻辑：

> 当瓶颈来自复杂 specification 时，一类方法改变/利用 specification structure；另一类方法把 temporal semantics 融入 learned policy，从而减少 deployment-time symbolic planning。

最后不要说谁“更差”，而是指出 assumptions 不同。

---

## Paragraph 5 — Precise gap

不要再写：

> existing methods cannot simultaneously achieve rapid first solution, optimization, and repair.

建议改成：

> existing approaches reduce different computational bottlenecks, but they generally either operate after a temporal planning structure has been constructed/extracted or replace the symbolic pipeline with structured specifications or learned policies. For model-based LTL-MRTA with unassigned robot identities, the opportunity to exploit robot-team feasibility **during** LTL-to-automaton generation remains comparatively underexplored.

然后自然进入本文。

---

# 6. 推荐的英文 Related Work 完整替换稿

下面这一版是我最推荐的版本。它不是照抄三篇参考论文的模板，而是：

- 用 Luo & Zavlanos 的 domain taxonomy 限定 scope；
- 用 source-search 论文的“method family → common limitation”方式压缩文献；
- 用 *From Ambiguous Language to Verifiable Plans* 的“每类文献都导向一个明确 design gap”的方式收束；
- 最终把所有内容统一到你的核心创新：**task allocation during automaton generation**。

---

## A. Related Work

Existing planning methods under LTL constraints can broadly be divided into bottom-up and top-down approaches. Bottom-up methods assign local LTL specifications to individual robots and achieve team-level behavior through coordination, synchronization, and online reconfiguration [14], [15]. In contrast, top-down methods begin with a global temporal-logic specification describing the collective mission. This work considers the latter setting, with the additional feature that the identities of the robots executing individual subtasks are not prescribed by the specification.

A classical top-down strategy constructs a product between the automaton translated from the global LTL formula and the robots' transition systems, and then searches the resulting product space for a satisfying plan [9], [16]. Although systematic, this approach suffers from state explosion as the workspace, team size, and task complexity increase. Sampling-based methods [10], [17] alleviate this burden by incrementally approximating the product space rather than constructing it explicitly. Their efficient biased search, however, typically assumes that robot-specific task propositions are given in the LTL formula; when the assignment is not known a priori, explicitly enumerating admissible robot combinations can substantially enlarge the specification. Other methods decouple task allocation from low-level planning. The STAP framework [18], [19] decomposes a global temporal-logic mission into subtasks and jointly considers their allocation and execution, whereas MILP-based formulations [7], [8], [20] encode task and temporal constraints as optimization problems. These approaches improve scalability in different ways, but the resulting allocation problem can still become expensive as the number of robots, subtasks, and temporal dependencies grows. 

Several methods place greater emphasis on obtaining a feasible plan quickly. Planning-decision-tree-based approaches [21], [22] represent task progress and robot assignments incrementally, enabling fast reactive planning for large heterogeneous teams. Their efficiency is obtained partly through greedy allocation decisions, which can limit solution quality. Liu et al. [3] instead extract partial-order relations from the task automaton and use branch-and-bound search in an anytime framework, so that a feasible plan can be returned first and subsequently improved. This is closely related to the objective considered in this work. However, the partial-order structure must be extracted before the corresponding allocation search begins, and this preprocessing cost can increase with automaton complexity. These methods therefore accelerate the allocation/search stage, but do not specifically exploit robot-team feasibility while the LTL automaton itself is being generated.

Another line of work reduces the burden associated with complex temporal specifications by changing or exploiting their structure. Hierarchical temporal-logic formulations [23] organize a mission into a hierarchy of specifications, while [24] exploits sc-LTL missions expressed as conjunctions of subformulas and combines their posets online. Such structure-aware methods can substantially simplify planning when the mission admits the required hierarchical or conjunctive representation, at the cost of additional assumptions on specification structure or decomposition. A different direction is to amortize temporal reasoning through learning. For example, LTL2Action [12] uses LTL progression together with a task-conditioned reinforcement-learning policy, avoiding the need to compile each instruction into an explicit Büchi automaton for deployment-time action selection. Once trained, such policies can produce actions rapidly and can generalize across LTL instructions. However, a substantial part of the computation is shifted to offline training, and deployment performance depends on the learned policy's generalization to the encountered task and environment distribution. Moreover, such learning-based methods are complementary to the model-based LTL-MRTA problem considered here rather than direct substitutes for explicit heterogeneous-robot assignment and optimization.

Overall, existing approaches reduce computational burden at different stages: product-space construction, task-allocation search, specification decomposition, or deployment-time decision making. For model-based LTL-MRTA with a global specification and no preassigned robot identities, however, robot-team feasibility and partial allocation information are still typically introduced only after a suitable temporal planning structure has been constructed or extracted. This separation can delay the first executable plan and allows automaton structure that is irrelevant to the current heterogeneous team to be generated before planning can exploit it. The proposed framework addresses this issue by moving task-allocation reasoning upstream into the LTL-to-automaton translation process: infeasible and unnecessary transitions are removed at the GBA level, while the NBA and plan graph are constructed synchronously so that feasible assignments can be evaluated as soon as new temporal transitions become available. The retained plan graph then supports subsequent optimization and repair when the available robot team changes during execution.

---

# 7. 为什么我认为这一版比当前版本更适合审稿

## 7.1 创新点不再依赖一句 “to the best of our knowledge”

即使删掉 Contributions 中的首创性声明，Related Work 本身已经让审稿人看到：

- product/sampling：主要处理 product-space；
- STAP/MILP：主要处理 allocation/optimization；
- PDT/poset：主要处理 fast allocation / anytime；
- HLTL：主要处理 specification structure；
- learning：主要把在线计算转移到 policy training；
- **你：改变 allocation 介入 temporal compilation 的时间点。**

这就是比“我们更快”更稳固的 novelty positioning。

---

## 7.2 对 learning 的定位是“complementary”，而不是强行建立优劣关系

这是非常重要的。

LTL2Action 的研究问题并不是 heterogeneous MRTA。它的价值在于通过 LTL progression + learned task-conditioned policy 实现跨 LTL instruction 的策略泛化。

所以最合理的写法不是：

> learning is limited, therefore our method is better.

而是：

> learning provides a different way to reduce deployment latency, but under a different computational model and different assumptions; our work focuses on retaining explicit model-based symbolic task allocation.

这种写法审稿人基本没有必要与你争论。

---

## 7.3 HLTL 后面接 learning 的逻辑是自然的

这一段的上位问题是：

> **如果复杂 LTL specification 本身是 computational burden 的来源，有哪些替代处理方式？**

然后：

- HLTL：改变/利用 formula structure；
- learning：不把每个 formula 都转换成 deployment-time automaton/search problem，而是学习 task-conditioned policy。

两者都是“从 conventional full symbolic pipeline 外部改变负担”的思路，因此放在一起非常自然。

---

# 8. 与 Introduction 的最小协调修改

你当前 Introduction 在 Related Work 前已经有一段：

> Existing studies have made several efforts to reduce this burden. Some reformulate the LTL specification ... Other studies seek to avoid explicit automaton construction at deployment through learning-based approaches ...

如果 Related Work 按上面的版本展开，这一段会发生轻微重复。

我建议 Introduction 中**保留这个观点，但进一步压缩**，不要在那里详细评价 HLTL 和 learning。

可以改成：

> Existing work reduces this burden from several directions, including exploiting structured temporal-logic formulations and amortizing temporal reasoning through learning. These approaches introduce different assumptions on task representation or training, as discussed in Sec. I-A. Here, we pursue a complementary model-based direction: rather than changing the specification language or replacing symbolic planning with a learned policy, we ask whether robot allocation can begin while the LTL automaton is still being generated.

这样有三个好处：

1. Introduction 只负责**提出设计方向**；
2. Related Work 负责**公平展开文献与 limitations**；
3. 不会让 [12]/[23] 在相邻两部分被几乎重复描述两次。

---

# 9. 建议删除或弱化的表述

## 建议弱化 1

当前：

> As illustrated in the paper, for an automaton with hundreds of states, the algorithm may require tens or even hundreds of seconds to obtain the first partial order.

建议删除具体秒数，改成机制性判断：

> the preprocessing cost of extracting partial-order structures can increase with automaton complexity.

---

## 建议弱化 2

当前：

> they still struggle to simultaneously provide a rapid first feasible plan, effective subsequent optimization, and efficient plan repair

建议不要用三项全包式 gap。

改成更精确：

> the separation between temporal-structure construction and robot allocation can still introduce avoidable latency before the first executable plan becomes available.

优化和 repair 作为本文 plan graph 带来的**后续收益**，不要都包装成“所有现有工作共同缺失”。

---

## 建议避免 3

不要写：

> learning-based methods lack formal guarantees

除非你明确限定“learned policy itself does not provide the same model-based completeness guarantee in our LTL-MRTA formulation”。

因为 RL + temporal logic 文献中存在多种 formal/verification 结合方式，笼统说 learning 没有 formal guarantee 容易被反例攻击。

---

# 10. 最终建议

如果只做一次修改，我建议优先完成以下三件事：

1. **把 Related Work 的最后 gap 从“性能指标集合”改成“integration point gap”。**
2. **把 PDT + poset 作为最接近本文的方法重点讨论，而不是平均展开所有 LTL planning 文献。**
3. **在 HLTL 后加入 learning，但用“different assumptions / complementary direction”定位，不要把它写成被本文击败的 baseline。**

修改后，审稿人读完 Related Work 应该自然形成如下理解：

> “作者不是声称解决 LTL planning 的所有 scalability 问题，也不是简单提出另一个 anytime optimizer。现有工作主要在 product search、allocation、task decomposition 或 learned deployment policy 上减少开销；这篇文章的切入点是更早——在 GBA/NBA 生成过程中就让当前异构团队的可行性和部分 allocation 参与进来，从而减少无效结构传播并提前得到 executable plan。后面的 BnB 和 repair 是这个 retained plan graph 的自然延伸。”

如果审稿人形成的是这个认识，你的 Related Work 就已经完成了最重要的任务。

---

## 附：learning 文献表述的事实核查说明

你当前文献 [12] 为 P. Vaezipoor *et al.*, **“LTL2Action: Generalizing LTL Instructions for Multi-Task RL,” ICML 2021**。该方法不是先把每个 LTL instruction 编译为 Büchi automaton 再做图搜索，而是使用 **LTL progression** 更新剩余公式，并训练接收环境状态与当前 LTL instruction 的 task-conditioned RL policy。因此，在你的 Related Work 中使用“avoiding explicit Büchi-automaton compilation for deployment-time action selection”比笼统的“learning methods do not construct automata”更准确。
