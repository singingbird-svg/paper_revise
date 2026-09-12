# Introduction 中“两类方法—本文方法”衔接问题的修改方案

## 1. 修改范围与核心判断

本文件针对当前论文 **Introduction 中 Related Work 之前的部分**，重点修改以下逻辑链：

> 复杂 LTL 规格导致规划较慢  
> → 现有工作采用结构化规格或学习方法  
> → 本文在自动机构造过程中进行任务分配

当前文本的问题不在于缺少文献，而在于上述三步之间缺少一个明确的“剩余问题”。读者能够理解两类现有方法各自做了什么，却无法立即理解：

1. 为什么这两类方法仍未解决本文关心的问题；
2. 为什么它们的局限会自然导向“在自动机构造过程中进行任务分配”；
3. 本文究竟是在解决一般的 LTL-to-automaton 复杂度，还是在解决异构多机器人任务分配中特定的首次可执行方案延迟。

建议将论文的核心问题从笼统的“复杂公式转换较慢”进一步收紧为：

> **在传统的顺序式 LTL-MRTA 流程中，自动机构造主要依据逻辑可满足性，而当前机器人团队的类型、数量、可达性和分配状态直到后续规划阶段才被使用。因此，复杂规格会放大这一阶段分离造成的代价：对当前团队不可执行的转移和包含不必要同步的任务进程仍可能被构造并传播，从而推迟首次可执行分配的产生。**

这一定义能够直接解释为什么本文不是简单地“再提出一种加速方法”，而是要改变自动机构造与任务分配之间的关系。

---

## 2. 当前文本为什么显得突兀

当前相关段落先说明现有研究主要采用两类方法：

- 通过层次化、分解或组合结构降低规格和规划复杂度；
- 通过学习公式或自动机表示，将部分时序推理成本摊销到训练阶段。

随后直接使用：

> `Motivated by these limitations, we propose ...`

引出本文方法。这里存在四个具体问题。

### 2.1 两类方法与本文方法处理的不是同一层问题

结构化方法主要改变**规格的表达或分解方式**；学习方法主要改变**时序推理成本在训练与部署之间的分配方式**。本文则改变**自动机构造与机器人分配的执行顺序和信息耦合方式**。如果不先指出这一层次差异，本文方法会像第三种并列的加速技巧，而不是由前文缺口必然推导出的设计。

### 2.2 对两类方法的局限描述过于宽泛

当前对学习方法使用了：

> `can still be difficult to apply to large heterogeneous robot teams with complex collaboration and temporal requirements`

这一表述没有说明“困难”具体在哪里，也无法解释为什么本文的方法能够解决它。应明确指出，本文要求的是针对**当前给定的异构团队**产生显式机器人分配，并处理机器人类型、需求数量、同一子任务内分配互斥、区域可达性和 makespan。当前引用的学习方法主要面向公式条件策略或目标表示的泛化，并不直接输出这种实例级分配结果。

### 2.3 没有指出两类方法之后仍然存在的共同问题

前文需要增加一个明确的研究问题：

> 在保留显式自动机以表示和验证时序进程的前提下，如何让当前团队的可执行性信息在自动机构造期间就参与候选结构的生成，而不是等到完整自动机生成后再进行检查？

只有提出这一问题，后面的 GBA 剪枝和 NBA-plan graph 同步构造才会显得必要。

### 2.4 当前表述容易让审稿人误解本文的主张范围

本文并没有消除一般 LTL-to-automaton translation 的最坏情况复杂度，也没有证明复杂公式不再导致自动机规模增长。本文真正能够支持的论点是：

- 在 GBA 阶段提前去除对当前团队不可行的候选转移；
- 在最终 NBA 完成前同步推进任务分配；
- 使接受结构一旦对应可行分配，就可以形成首次可执行方案；
- 保留计划图用于后续 makespan 改进和未完成任务的重新分配。

因此，应避免把论文定位成“解决长 LTL 公式转换问题”，而应定位成“减少顺序式 translation-then-allocation 流程对首次可执行方案造成的延迟”。

---

## 3. 建议采用的完整逻辑链

建议 Related Work 之前的 Introduction 按以下逻辑推进。

### 第一步：从实际任务引出 LTL-MRTA

说明仓储、巡检或维护任务同时包含：

- 顺序与持续约束；
- 不同能力机器人的协作；
- 某些动作需要多个机器人同时参与；
- LTL 规定团队任务，但不预先指定机器人身份。

### 第二步：说明计算困难来自“逻辑进程与资源分配的耦合”

不要只写“公式越复杂越慢”。应指出：

- 复杂规格会产生更多候选任务进程；
- 每个任务进程还必须与机器人类型、数量、可达性、互斥分配和执行时间相匹配；
- 实际部署首先需要的是一个可执行分配，而不是先得到完整自动机或最终最优解。

### 第三步：指出传统顺序式流程的根因

明确说明：

- 自动机构造先进行，任务分配后进行；
- 自动机构造阶段主要保留逻辑上允许的行为；
- 当前团队能否执行这些行为，要到后续分配阶段才知道；
- 因而团队不可行结构和可避免同步可能被无效传播；
- 复杂规格只是放大了这一阶段分离造成的代价。

### 第四步：公平介绍两类现有缓解方式

将两类方法写成对同一计算负担的不同处理方式：

1. **结构利用或规格分解**：缩小或重组需要规划的逻辑结构；
2. **学习式公式/自动机表示**：通过训练摊销时序推理，并在部署时进行快速策略推断。

先承认其有效性，再说明其与本文问题的边界。

### 第五步：提出“仍未解决的问题”

建议用一句明确的转折统领后文：

> **These approaches reduce the burden of temporal reasoning, but they do not remove the need to couple logical task progress with the executability of the current heterogeneous team.**

随后说明：

- 结构化方法通常要求适合的规格形式或额外分解；
- 学习方法主要解决策略泛化，不直接产生本文所需的实例级显式分配；
- 对本文场景，仍需保留显式自动机并验证时序进程；
- 真正缺失的是让团队可行性在自动机构造时就进入。

### 第六步：由缺口直接推出本文设计

本文方法不应通过泛化的 `Motivated by these limitations` 引出，而应写成：

> 因为问题来自 translation 与 allocation 的阶段分离，所以解决思路是让二者同步推进。

这样可形成一一对应关系：

| 前文问题 | 本文设计 |
|---|---|
| 逻辑上允许但当前团队不可执行的转移被继续构造 | 在 GBA 候选转移插入前检查机器人类型和数量 |
| 独立动作被不必要地绑定在同一转移中 | 去除保持接受进程的 progress-consistent decomposable transitions |
| 分配必须等待最终 NBA | NBA 与 plan graph 同步构造 |
| 标准生成顺序不考虑当前方案代价和剩余任务 | residual-obligation score 用于候选扩展排序 |
| 首次方案与后续优化由不同流程产生 | 保留 plan graph，并以当前方案 warm-start BnB |
| 团队变化后需要重新处理未完成分配 | 从当前执行状态重新根定并优化剩余分配 |

---

## 4. 推荐的完整替换稿

以下英文可直接替换当前论文从 `I. INTRODUCTION` 开始到 `A. Related Work` 之前的正文。该版本没有单独列出 Contributions，正式贡献仍可保留在后续 Contributions 部分。

### Revised Introduction Before Related Work

Multi-robot systems (MRSs) are increasingly deployed in applications such as persistent surveillance [1], logistics [2], and autonomous maintenance [3], where missions combine temporal dependencies with heterogeneous collaboration. Consider a warehouse inspection mission in which incoming goods must be registered before inspection, stored goods must be checked under persistent safety constraints, and outgoing goods may require coordinated verification by robots with different capabilities. Linear temporal logic (LTL) provides a rigorous language for specifying such ordering, persistence, and collaboration requirements [4]-[6]. When a global LTL formula specifies what the team must accomplish without preassigning individual robots to the required actions, planning gives rise to the LTL-based multi-robot task-allocation (LTL-MRTA) problem [7].

In LTL-MRTA, computational difficulty arises from the coupling between logical task progression and robot assignment. A more complex specification typically induces more candidate task progressions, while each progression must also be evaluated against robot types, required cardinalities, workspace reachability, mutual exclusion among simultaneous assignments, and accumulated execution times. Consequently, mixed-integer linear programming (MILP)-based methods [7], [8] and search-based methods [9], [10] can require substantial computation in large-scale problems, even before one feasible team allocation is available. In practical deployments, however, execution cannot begin until the current team has an executable allocation. The planning objective is therefore twofold: to obtain a feasible plan early and to continue refining its makespan as computation permits.

Many existing LTL-MRTA pipelines treat automaton construction and task allocation as separate stages. Planning-decision-tree-based methods [11]-[13] and poset-based methods [3], for example, perform allocation or optimization on an automaton or on a task structure derived from it. This separation places automaton construction or task-structure extraction on the critical path to the first executable plan. It also creates a mismatch between the information used at the two stages: automaton translation preserves logically admissible behaviors, whereas executability depends on the current robot team and workspace. As a result, transitions that are logically valid but cannot be assigned to the available robots, as well as transitions that impose avoidable synchronization among independent actions, may be generated and propagated before being rejected during downstream planning. The delay caused by this separation becomes more pronounced as the specification and the induced automaton grow.

Existing work reduces this burden in two broad ways. Structure-exploiting methods reorganize or decompose temporal-logic specifications into hierarchical or compositional components [14], thereby reducing the planning problem when the mission admits the required structure. Learning-based methods instead amortize temporal reasoning across a task distribution by conditioning policies on learned formula or automaton representations [15], [16]. Once trained, these methods can support fast action selection and, in some formulations, avoid constructing a separate explicit automaton for every deployment task. These approaches are valuable, but they address different assumptions from the setting considered here. Structure-exploiting methods require a suitable specification form or an additional decomposition step. Learning-based methods focus primarily on policy generalization and do not directly produce an explicit, instance-specific assignment for the current heterogeneous team under robot-type, cardinality, reachability, disjointness, and makespan constraints. Thus, the remaining issue is not simply how to shorten or bypass automaton construction. Rather, it is how to retain an explicit temporal-logic representation while allowing deployment-specific allocation feasibility to influence the construction before irrelevant task progressions are fully generated.

To address this issue, we integrate task-allocation reasoning into the LTL-to-automaton translation process. The central idea is to let automaton construction and allocation proceed together: team-level feasibility is used to filter candidate task progressions, and each retained progression is evaluated for assignment as soon as it is generated. Following the LTL2BA pipeline [17], the framework first screens candidate generalized Büchi automaton (GBA) transitions against the robot types and cardinalities available in the team and discards candidates whose simultaneous action requirements cannot be met. It then removes progress-consistent decomposable transitions that would otherwise impose unnecessary synchronization before the final nondeterministic Büchi automaton (NBA) is constructed.

During GBA-to-NBA generation, the NBA and a plan graph are constructed in lockstep. Each newly generated NBA transition induces a subtask, which is evaluated using the current partial assignment, predicted robot positions and completion times, and workspace reachability. Feasible extensions are recorded in the plan graph, whereas extensions that fail the allocation check are not added. A residual-obligation score orders feasible successors according to the current plan cost and an estimate of the remaining positive action requirements. Consequently, an executable plan can be extracted as soon as an accepting prefix-suffix structure with a feasible allocation is reached, without waiting for the complete NBA. The retained plan graph continues to update the best plan found during construction and subsequently warm-starts a branch-and-bound optimizer for makespan refinement. When the available robot set changes during execution while the LTL mission remains unchanged, the same graph is re-rooted at the latest confirmed execution state and the unfinished assignments are re-optimized over the remaining team. In this way, the framework preserves the explicit automaton representation while moving team-specific feasibility and allocation to the stage at which candidate task progressions are created.

---

## 5. 只修改问题段落的最小替换版本

若不希望重写前两段，可保留现有开篇和问题背景，仅将当前从：

> `Many existing methods for LTL-MRTA separate these two planning stages ...`

开始，到 `A. Related Work` 之前的内容替换为以下版本。

### Minimal Replacement

Many existing LTL-MRTA pipelines treat automaton construction and task allocation as separate stages. Planning-decision-tree-based methods [11]-[13] and poset-based methods [3], for example, perform allocation or optimization on an automaton or on a task structure derived from it. This separation places automaton construction or task-structure extraction on the critical path to the first executable plan. It also creates a mismatch between the information used at the two stages: automaton translation preserves logically admissible behaviors, whereas executability depends on the current robot team and workspace. Consequently, transitions that are logically valid but cannot be assigned to the available robots, as well as transitions that impose avoidable synchronization among independent actions, may be generated and propagated before being rejected during downstream planning. This delay becomes increasingly significant for complex specifications with large induced automata.

Existing work reduces this burden in two broad ways. Structure-exploiting methods reorganize or decompose temporal-logic specifications into hierarchical or compositional components [14], thereby reducing planning complexity when the mission admits the required structure. Learning-based methods amortize temporal reasoning across a task distribution by conditioning policies on learned formula or automaton representations [15], [16]. Once trained, they can support fast action selection and, in some formulations, avoid constructing a separate explicit automaton for every deployment task. These approaches are valuable, but they do not remove the need to couple logical task progress with the executability of the current heterogeneous team. Structure-exploiting methods require a suitable specification form or an additional decomposition step, whereas learning-based methods focus primarily on policy generalization rather than producing an explicit, instance-specific assignment under robot-type, cardinality, reachability, disjointness, and makespan constraints. For the setting studied here, the remaining question is therefore how to retain an explicit automaton representation while allowing team feasibility and concrete task assignments to shape its construction.

To answer this question, we integrate task-allocation reasoning into the LTL-to-automaton translation process. Instead of treating automaton generation as a planning-independent preprocessing stage, the proposed framework uses information about the available robot team to filter candidate task progressions and evaluates each retained progression for assignment as soon as it is generated. Following the LTL2BA pipeline [17], candidate GBA transitions whose simultaneous action requirements exceed the available robot types or cardinalities are discarded before insertion. Progress-consistent decomposable transitions are subsequently removed to avoid unnecessary synchronization. During GBA-to-NBA generation, the NBA and a plan graph are constructed in lockstep, and each newly generated NBA transition is immediately evaluated as a subtask using the current partial assignment, workspace reachability, and predicted execution state.

A residual-obligation score orders feasible successors according to the current plan cost and an estimate of the remaining positive action requirements. An executable plan can therefore be extracted once an accepting prefix-suffix structure with a feasible allocation is reached, without waiting for the complete NBA. The retained plan graph is then used for continued makespan refinement and, when the LTL mission remains unchanged, for updating unfinished assignments after a change in robot availability. Thus, the proposed framework does not replace the automaton representation; it makes automaton construction responsive to the allocation constraints that determine whether the resulting task progression is executable by the current team.

---

## 6. 文献编号与分类需要同步调整

当前参考文献中：

- `[14]` 是层次化规格下的 decomposition-based task allocation and planning，可用于支持结构利用或规格分解；
- `[15]` 是 compositional automata embeddings for goal-conditioned reinforcement learning，属于学习式目标表示；
- `[16]` 是 LTL2Action，属于公式条件的多任务强化学习；
- `[17]` 是 LTL2BA translation。

因此，当前正文将 `[14], [15]` 一起作为“structured task specifications”的依据不够准确。建议改为：

- 结构利用或规格分解：`[14]`，必要时再结合前文已经出现的 poset 文献 `[3]`；
- 学习式公式或自动机表示：`[15], [16]`；
- 本文采用的翻译流程：`[17]`。

建议不要将所有学习方法都写成“avoid explicit automaton construction”。更准确的概括是：

> `Learning-based methods amortize temporal reasoning by conditioning policies on learned formula or automaton representations [15], [16].`

随后再限定：

> `In some formulations, this can avoid constructing a separate explicit automaton for every deployment task.`

这样既覆盖 LTL2Action，也不会错误地把 automata embeddings 描述为完全绕开自动机。

---

## 7. 关键用词与主张边界

| 当前或容易出现的表述 | 主要问题 | 建议表述 |
|---|---|---|
| `complex formulas are slow` | 过于笼统，无法导向本文设计 | `complex specifications amplify the cost of separating automaton construction from team-specific allocation` |
| `high-quality executable plan as early as possible` | 将首次解时间和质量混成一个目标 | `obtain a feasible plan early and continue refining its makespan` |
| `task planing` | 拼写错误 | `task planning` |
| `can still be difficult to apply` | 缺少可核查的具体原因 | 明确写 type, cardinality, reachability, disjointness, and makespan constraints |
| `Motivated by these limitations` | 缺少因果推导 | `For the setting studied here, the remaining question is therefore ...` |
| `novel framework` | 自我评价，且不能解释创新 | 直接说明 `we integrate task-allocation reasoning into the LTL-to-automaton translation process` |
| `redundant transitions` | 含义过宽 | `progress-consistent decomposable transitions that impose avoidable synchronization` |
| `higher-quality initial solution` | residual score 不提供质量保证 | 说明 score `orders feasible successors`，不要写成最优性保证 |
| `continued improvement toward better solutions` | 目标不明确 | `continued makespan refinement` |
| `repair the remaining mission` | LTL mission 本身未改变 | `re-optimize the unfinished assignments` |

还应避免以下过强主张：

1. 不要声称本文解决了 LTL-to-automaton translation 的最坏情况指数复杂度；
2. 不要声称学习方法无法处理长 LTL 公式；
3. 不要将 residual-obligation score 描述为 admissible heuristic 或最优性保证，除非后文已经证明；
4. 不要将 BnB 结果写成不加限定的 global optimum，除非理论明确覆盖完整任务进程和完整分配空间；
5. 机器人不可用后的处理应限定在全局 LTL mission 不变的情形，修复对象是未完成的计划和分配。

---

## 8. 修改后的核心呼应关系

修改后，Introduction 的前后逻辑应形成以下闭环：

1. **实际需求**：当前团队需要尽早获得可执行分配；
2. **计算困难**：复杂规格产生更多逻辑进程，并与异构资源分配组合；
3. **根因**：自动机构造与任务分配分离，使团队可执行性进入过晚；
4. **现有缓解方式**：结构化方法改变规格形式，学习方法摊销时序推理；
5. **剩余缺口**：两者均未直接解决“保留显式自动机时，如何让当前团队可行性参与其构造”；
6. **本文设计**：GBA 阶段提前检查，NBA 与 plan graph 同步构造；
7. **直接结果**：接受结构一旦具有可行分配即可形成首次方案；
8. **后续利用**：同一计划图支持 makespan 改进和未完成分配更新。

这条逻辑能够突出“为什么必须这样设计”，而不是仅仅陈述“本文用了哪些算法组件”。
