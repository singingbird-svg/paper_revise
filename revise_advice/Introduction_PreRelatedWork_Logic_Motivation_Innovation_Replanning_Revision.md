# Introduction（Related Work 之前）修改意见与可直接替换稿

## 0. 修改范围

本文档针对当前稿件 **“On-the-Fly Temporal-Logic Task Allocation for Heterogeneous Multi-Robot Systems during Büchi Automaton Generation”** 中从 `I. INTRODUCTION` 开始至 `A. Related Work` 之前的内容进行检查与重写。

本次修改不改动后续 `Related Work` 和 `Contributions` 的章节安排，也不在 Introduction 前半部分单独列贡献。重点是：

1. 建立严密且前后呼应的研究动机；
2. 将“快速获得首次可行解、后续优化、在线重规划”组织成统一的实际需求；
3. 解释为什么必须把任务分配引入自动机构造，而不是只说“本文采用了 on-the-fly 方法”；
4. 将当前偏流水账式的方法描述改为围绕核心创新组织；
5. 修正文献分类、术语和部分过强或不够准确的表述。

---

## 1. 总体判断

当前 Introduction 已经包含本文所需的主要元素：

- LTL-MRTA 的实际应用背景；
- 大规模问题中的首次可行解延迟；
- planning-decision-tree 与 poset 方法之间的速度—质量权衡；
- 自动机构造与任务分配顺序执行所造成的等待；
- 结构化规格和学习方法两类缓解路线；
- GBA 剪枝、NBA–plan graph 同步构造、score-guided expansion、BnB 优化和机器人不可用后的重规划。

问题主要不在于“内容缺失”，而在于这些内容尚未形成一条足够集中的因果链。当前读者能够知道本文做了哪些步骤，却仍可能提出以下问题：

> 为什么复杂规格一定要求把任务分配前移到自动机构造阶段？  
> 为什么已有的 anytime planning、结构化规格或学习方法仍不足以解决本文问题？  
> 为什么 retained plan graph 不只是一个中间数据结构，而是本文同时实现首次规划、持续优化和在线修复的关键？

建议将 Introduction 的主线收紧为：

> **LTL-MRTA 的困难来自逻辑任务进程与异构资源分配的耦合，而传统流程却将两者分开处理。复杂规格会放大这种阶段分离的代价：对当前团队不可执行或包含可避免同步的逻辑进程仍被生成，任务分配必须等待自动机构造完成，执行阶段发生机器人不可用时也缺少可直接复用的分配结构。因此，本文让团队可行性、部分分配和执行状态在自动机构造过程中就参与搜索，并将同步生成的 plan graph 贯穿首次解、后续优化和在线重规划。**

这一主线能够同时解释：

- 为什么要做 GBA-level pruning；
- 为什么 NBA 与 plan graph 必须同步构造；
- 为什么需要 residual-obligation score；
- 为什么首次接受结构出现时即可返回计划；
- 为什么 plan graph 应被保留并用于 BnB 和机器人不可用后的在线重规划。

---

## 2. 当前文本的主要问题及修改方式

### 2.1 “复杂公式较慢”仍然过于笼统

当前第二段主要写道，机器人数量和规格复杂度增长会使搜索与优化空间快速扩大。这个判断本身没有问题，但它不足以直接推出本文的算法设计。

审稿人更关心的是：**复杂性具体在哪一层产生，以及本文改变了哪一层的信息流。**

建议明确写出两个相互耦合的组合空间：

1. LTL 规格诱导的逻辑任务进程；
2. 针对每条任务进程的机器人类型、数量、可达性、同一时刻的互斥分配以及完成时间组合。

这样，后文才能自然得出：

> 本文不是单纯加快一般意义上的 LTL-to-automaton translation，而是减少“先生成逻辑结构、后判断当前团队是否能执行”所造成的无效传播和首次方案延迟。

---

### 2.2 “首次可行解”和“高质量解”混在同一句中

当前文本多次使用：

> `obtain a high-quality executable plan as early as possible`

该表述把两个不同目标混在一起：

- **响应性**：尽快得到第一份可执行方案；
- **解质量**：在后续计算中降低 makespan。

你的方法实际上也是分阶段满足这两个目标：

- 同步构造 NBA 和 plan graph，用于尽早得到第一份可行计划；
- 在构造过程中更新较低代价计划，并用 `Πplan` warm-start BnB，用于继续改进 makespan。

建议统一改写为：

> `obtain a feasible plan early and continue refining its makespan as computation permits`

这样既与算法流程一致，也避免暗示 first feasible plan 必然具有某种已证明的质量保证。

---

### 2.3 在线重规划在当前动机中出现得太晚

当前重规划只在方法段落末尾出现：

> `When a robot becomes unavailable during execution, ...`

由于前文没有先说明为什么机器人不可用是一个必须解决的实际问题，这句话容易被读成附加功能，而不是 plan graph 设计的重要价值。

建议在讨论 anytime planning 后加入一段简短动机：

- 机器人可能因硬件故障、定位失效或能量不足而退出团队；
- 此时全局 LTL mission 本身未必改变；
- 改变的是可用机器人集合以及尚未完成的分配；
- 从原始公式重新开始完整规划会丢弃已经完成的任务进度和已有的候选分配结构；
- 因而规划器应保留可从当前执行状态重新定根并复用的表示。

这样，后文“retained plan graph 用于 re-rooting 和 re-optimization”就成为前文需求的直接回应。

需要注意：重规划应被提升到“本文方法生命周期价值”的位置，但不应取代本文的核心主线。核心创新仍是**在自动机构造期间耦合任务分配**；重规划是该统一图表示带来的重要执行阶段能力。

---

### 2.4 对顺序式流程的批评还不够深入

当前文本主要指出：

> 规划只能在自动机构造完成后开始，因此首次方案时间包含 automaton construction 和 subsequent planning。

这只说明了“等待”，但尚未充分解释为什么你的 GBA 剪枝和同步构造是必要的。

建议增加“信息不匹配”这一层：

- 自动机翻译保留的是逻辑上允许的行为；
- 实际可执行性取决于当前团队的机器人类型、数量、可达性和分配状态；
- 如果这些信息直到后续规划才进入，那么对当前团队不可执行的转移，以及把独立动作强制同步的转移，仍可能被生成并传递到 NBA 和分配阶段；
- 因而复杂规格放大的不只是自动机规模，也包括大量对当前部署实例没有规划价值的中间结构。

这才能直接推出：

> team feasibility 应在 candidate transition 被创建时参与判断，而不是在完整自动机构造后再检查。

---

### 2.5 两类缓解方法与本文方法之间需要一个明确的“剩余缺口”

当前 Introduction 已经提到：

1. 结构化或分解式规格；
2. 学习式方法。

但必须进一步明确：这两类方法分别改变了什么，又没有改变什么。

建议采用以下定位：

- 结构化方法通过层次化、分解或组合形式减少需要处理的逻辑结构，但要求任务具有合适的表示形式，或需要额外分解；
- 学习方法将部分时序推理成本摊销到训练阶段，并可在部署时快速推断；
- 但本文处理的是给定异构团队下的**显式、实例级任务分配**，其中包含机器人类型、需求数量、可达性、并发分配互斥和 makespan；
- 因而本文的剩余问题不是简单地“缩短或绕开自动机构造”，而是：

> **在保留显式自动机以表达和检查时序进程的同时，如何让当前团队的可执行性和部分分配状态在自动机构造期间就影响搜索。**

这句话应直接放在两类方法之后，作为引出本文设计的桥梁。

---

### 2.6 方法段落目前按执行顺序罗列，创新层次不够突出

当前最后一段依次介绍：

1. LTL2BA；
2. GBA 剪枝；
3. NBA 与 plan graph；
4. greedy allocation；
5. residual-obligation score；
6. first feasible plan；
7. plan update；
8. BnB；
9. replanning。

这种写法技术上完整，但读起来类似系统流程说明。审稿人容易记住模块名称，却不一定理解这些模块共同构成了什么新的方法思想。

建议按照三个概念层次组织，而不是按照代码执行顺序组织：

#### 层次一：让自动机结构受到当前团队可执行性的约束

强调 GBA-level pruning 不是普通的后处理压缩，而是在 NBA 生成前：

- 排除当前团队在类型和数量上无法完成的 candidate transitions；
- 排除保持 acceptance progress 的 progress-consistent decomposable transitions，避免独立任务被不必要地同步。

#### 层次二：将自动机搜索和分配搜索统一为同一个增量过程

强调本文最核心的区别是：

- NBA 与 plan graph 同步增长；
- 每个新 NBA transition 在生成时即被解释为 subtask 并进行分配检查；
- logical successor ordering 同时决定 allocation-branch ordering；
- 可行接受结构一旦出现即可形成第一份可执行方案，无需等待完整 NBA。

#### 层次三：让同一个 plan graph 覆盖整个计划生命周期

强调 plan graph 不是一次性中间结果，而是：

- 构造期间持续更新较低代价方案；
- 构造完成后为 BnB 提供 incumbent；
- 执行期间在机器人不可用时，从最后确认状态重新定根并重新分配未完成任务。

这样，“创新”不再是多个组件的并列集合，而是一个统一设计：

> **同一个 planning-informed graph 将自动机生成、首次方案提取、makespan 改进和在线计划修复连接起来。**

---

### 2.7 文献编号存在分类错误

当前文本把 `[14], [15]` 一起用于支持 structured task specifications，但当前参考文献中：

- `[5]`：finite LTL specification decomposition；
- `[14]`：hierarchical temporal-logic task allocation；
- `[15]`：compositional automata embeddings for goal-conditioned reinforcement learning；
- `[16]`：LTL2Action；
- `[17]`：LTL2BA。

因此建议调整为：

- 结构化、层次化或分解式方法：`[5], [14]`；
- 学习式公式/自动机表示与策略泛化：`[15], [16]`；
- 本文采用的 on-the-fly translation pipeline：`[17]`。

否则审稿人核对参考文献时，会发现 `[15]` 的正文归类与题目不一致。

---

## 3. 推荐的段落逻辑

修改后的 Related Work 之前部分建议采用以下八段结构：

| 段落 | 核心功能 | 与后文的呼应 |
|---|---|---|
| 第 1 段 | 从真实多机器人任务引出时序、协作和 LTL-MRTA | 对应 problem formulation 中的 temporal and collaboration requirements |
| 第 2 段 | 说明困难来自逻辑进程与异构分配的耦合，并区分 first-plan latency 与 makespan | 对应 `T_first`、`Π_init` 和后续 BnB |
| 第 3 段 | 讨论首次解—解质量权衡，并简要引出机器人不可用后的在线重规划需求 | 对应 anytime workflow 和 Section VIII |
| 第 4 段 | 指出顺序式 translation-then-allocation 的根因是信息进入过晚 | 对应 GBA feasibility pruning 和 joint construction |
| 第 5 段 | 公平说明结构化方法和学习方法的优势，再提出它们之后仍存在的缺口 | 对应本文保留显式自动机但改变构造方式 |
| 第 6 段 | 用一个明确 design question 汇总全文需求 | 同时呼应 early plan、optimization、repair |
| 第 7 段 | 介绍第一层创新：受团队可执行性约束的 GBA 构造 | 对应 infeasible-transition pruning 和 decomposable-transition pruning |
| 第 8 段 | 介绍核心创新：NBA–plan graph 同步构造以及同一图在首次规划、优化和重规划中的复用 | 对应 Sections VI–VIII |

---

## 4. 可直接替换的英文版本

以下文本可直接替换当前论文从 `I. INTRODUCTION` 开始到 `A. Related Work` 之前的全部正文。引用编号按照当前参考文献表调整，其中结构化方法使用 `[5], [14]`，学习方法使用 `[15], [16]`。

## I. INTRODUCTION

Multi-robot systems (MRSs) are increasingly deployed in applications such as persistent surveillance [1], logistics [2], and autonomous maintenance [3], where heterogeneous robots must coordinate under temporal and collaborative requirements. Consider a warehouse inspection mission in which information about incoming goods must be retrieved before downstream inspections, some checks require robots with different capabilities to act jointly, and monitoring duties may need to remain active throughout execution. Such missions involve ordering, persistence, and synchronization constraints that are difficult to express reliably through an unordered task list. Linear temporal logic (LTL) provides a rigorous language for specifying these requirements [4]–[6]. When a global LTL formula specifies the team-level mission without preassigning individual robots to the required actions, planning gives rise to the LTL-based multi-robot task-allocation (LTL-MRTA) problem [7].

The computational difficulty of LTL-MRTA arises from the coupling between logical task progression and heterogeneous robot assignment. As a specification becomes more complex, the number of logically admissible task progressions can increase substantially; as the team grows, each progression must be considered together with more assignment combinations. A candidate plan must satisfy not only the temporal specification, but also robot-type and cardinality requirements, workspace reachability, disjoint assignments for simultaneous actions, and the resulting travel and completion times. Consequently, mixed-integer linear programming (MILP)-based methods [7], [8] and search-based methods [9], [10] can require substantial computation in large-scale problems, even when only a first feasible solution is needed. In deployment, however, a plan becomes operationally useful only after an executable allocation has been produced. The relevant objective is therefore to obtain a feasible plan early and to continue refining its makespan as computation permits.

Planning-decision-tree methods [11]–[13] pursue fast response by incrementally representing task progression and robot allocation, but their mainly greedy allocation decisions may lead to locally suboptimal plans. Poset-based methods [3] improve assignment quality by extracting partial-order relations and applying branch-and-bound search, although the required structural extraction can delay the first solution for complex tasks. These approaches expose a practical trade-off between response time and solution quality and motivate a planning workflow that returns an executable plan early and improves it thereafter. The same time sensitivity persists during execution. A robot may become unavailable because of a hardware fault, localization failure, or energy depletion. Such an event need not change the global LTL mission, but it invalidates unfinished assignments involving that robot. A practical LTL-MRTA planner should therefore preserve the completed task progress and reuse the remaining planning structure to repair the plan from the current execution state, rather than restart the entire synthesis process.

A fundamental source of both first-plan delay and repeated planning effort is the sequential treatment of temporal-logic translation and robot assignment. Most LTL-MRTA pipelines first translate the specification into an automaton and then perform task allocation on the resulting structure. This separation is not only a scheduling delay; it also creates an information mismatch. Automaton translation retains logically admissible behaviors, whereas executability depends on the available robot types and cardinalities, workspace reachability, and the current allocation state. Consequently, transitions whose simultaneous action requirements cannot be met by the current team, as well as transitions that impose avoidable synchronization on independent actions, may be generated and propagated before being rejected during downstream planning. Task allocation remains blocked until the required automaton structure has been produced, and the sequential pipeline does not by itself provide an execution-state-indexed allocation structure that can be directly reused after the team changes.

Existing work reduces the burden of temporal reasoning in two broad directions. Structure-exploiting methods decompose or reorganize the specification, for example through finite-LTL decomposition or hierarchical temporal-logic formulations [5], [14], and can substantially reduce planning effort when the mission admits the required structure. Learning-based methods amortize temporal reasoning across a task distribution by conditioning policies on learned formula or automaton representations [15], [16], enabling fast inference after training. These directions are valuable, but they address different assumptions from the setting considered here. Structure-exploiting methods require a suitable specification form or an additional decomposition procedure. The cited learning-based formulations primarily target policy generalization across specifications rather than an explicit, instance-specific allocation for the current heterogeneous team under robot-type, cardinality, reachability, disjointness, and makespan constraints. The remaining issue is therefore not simply how to shorten or bypass automaton construction, but how to retain an explicit temporal-logic representation while allowing deployment-specific allocation feasibility to influence its construction.

This leads to the central design question of this work: can automaton generation and task allocation be coupled so that non-executable task progressions are rejected when they are created, a feasible accepting plan can be returned before the complete automaton is available, and the resulting partial-plan structure remains reusable when the available team changes? We address this question by treating automaton construction and robot allocation as a single incremental search rather than two sequential stages.

Inspired by the on-the-fly construction in LTL2BA [17], the proposed framework makes robot-team constraints part of automaton generation instead of applying them only after translation. Before NBA generation, each candidate generalized Büchi automaton (GBA) transition is screened against the robot types and cardinalities available in the team. Candidates whose simultaneous action requirements cannot be satisfied are discarded before they enter the downstream search. The framework also removes progress-consistent decomposable GBA transitions that would otherwise impose avoidable synchronization while preserving the acceptance progress used in GBA-to-NBA degeneralization. These operations are not merely post-processing reductions of a completed automaton; they prevent task structures that are infeasible or unnecessarily restrictive for the current team from being propagated to the allocation stage.

The central coupling occurs during GBA-to-NBA generation, where the nondeterministic Büchi automaton (NBA) and a plan graph are constructed synchronously. Each newly generated NBA transition immediately induces a subtask that is evaluated using the partial assignment, predicted robot positions and completion times, and workspace reachability stored in the current plan node. Feasible extensions are recorded in the plan graph, whereas infeasible extensions are not propagated. A residual-obligation score jointly orders automaton successors and their associated allocation branches according to the current plan cost and the estimated burden of the remaining positive action requirements, thereby biasing the search toward lower-cost accepting branches without delaying first-plan generation. Once an accepting prefix–suffix structure with feasible assignments is reached, an executable plan can be returned before the complete NBA has been constructed. The same plan graph continues to update the best plan found during construction and subsequently provides the incumbent for branch-and-bound makespan refinement. Crucially, the graph is retained during execution: if a robot becomes unavailable, it is re-rooted at the last confirmed execution state and the unfinished assignments are re-optimized over the surviving team. The plan graph therefore serves as a common search structure for early plan extraction, subsequent optimization, and online plan repair, rather than as a temporary intermediate representation.

---

## 5. 修改后各段之间的呼应关系

### 5.1 第 2 段与最后一段的呼应

第 2 段提出两个目标：

- early feasible plan；
- continued makespan refinement。

最后一段对应说明：

- accepting prefix–suffix structure 出现时即可返回 executable plan；
- plan graph 持续更新，并为 BnB 提供 incumbent。

这样避免了前文提出“高质量首次解”，后文却只能证明“首次可行解”的表述错位。

### 5.2 第 3 段与最后一段的呼应

第 3 段说明：

- 机器人不可用不一定改变 LTL mission；
- 改变的是 available team 和 unfinished assignments；
- 需要从 current execution state 复用规划结构。

最后一段对应说明：

- retained plan graph 被 re-root；
- unfinished assignments 在 surviving team 上重新优化。

因此，在线重规划不再是突然出现的附加功能，而是对明确实际需求的回答。

### 5.3 第 4 段与第 7 段的呼应

第 4 段指出：

- 逻辑上允许但对当前团队不可执行的结构被传播；
- 独立动作可能被不必要地同步。

第 7 段对应说明：

- GBA candidate transition 的 type/cardinality screening；
- progress-consistent decomposable-transition removal。

这样，GBA-level pruning 的每一部分都有前文问题作为动机。

### 5.4 第 4、6 段与第 8 段的呼应

第 4 段指出 allocation information 进入过晚；第 6 段提出 automaton generation 与 task allocation 应同步。

第 8 段对应说明：

- 每个 NBA transition 生成时立即诱导 subtask；
- assignment、predicted positions、completion times 和 reachability 同时参与；
- score 同时排序 logical successors 和 allocation branches。

这直接突出本文最重要的创新不是单独的 greedy assignment、score 或 plan graph，而是**自动机搜索与任务分配搜索被统一为一个增量过程**。

---

## 6. 关键措辞修改

| 当前表述或风险表述 | 问题 | 推荐表述 |
|---|---|---|
| `Formal languages such as linear temporal logic provides` | 主谓不一致 | `Linear temporal logic provides` |
| `obtain a high-quality executable plan as early as possible` | 将首次解时间和质量保证混为一体 | `obtain a feasible plan early and continue refining its makespan` |
| `redundant and infeasible transitions` | `redundant` 范围过宽，未对应正式定义 | `team-infeasible and progress-consistent decomposable transitions` |
| `estimated burdens for the remaining parts` | 含义模糊 | `estimated burden of the remaining positive action requirements` |
| `obtain a higher-quality initial solution` | 容易被理解为保证 | `bias the search toward lower-cost accepting branches` |
| `continued improvement toward better solutions` | 目标不明确 | `continued makespan refinement` |
| `repair the remaining mission` | LTL mission 本身没有改变 | `repair the unfinished assignments` 或 `repair the remaining plan` |
| `re-planning process` | IEEE 论文中通常统一写作 | `replanning process` |
| `novel framework` | 自我评价，不能说明创新 | 直接说明 `couples automaton generation with task allocation` |
| `introduces information ... during translation` | 信息类型不够具体 | 分别说明 GBA 阶段使用 type/cardinality，NBA 阶段使用 assignment/execution state/reachability |

---

## 7. 主张边界

修改稿有意避免以下容易受到审稿人质疑的表述：

1. **不声称消除了 LTL-to-automaton 的最坏情况指数复杂度。**  
   本文降低的是对当前团队无执行价值的中间结构，并提前获得可行计划。

2. **不声称学习方法无法处理复杂 LTL。**  
   修改稿承认其在训练后快速推断和跨规格泛化方面的优势，只说明其研究目标与本文的实例级异构 MRTA 不同。

3. **不声称 residual-obligation score 保证 first plan 最优。**  
   使用 `biasing the search toward lower-cost accepting branches`，而不是 `guarantees a high-quality solution`。

4. **不将重规划描述为重新求解新的 LTL mission。**  
   当前论文的情形是 LTL mission 保持不变，可用团队发生变化，重新优化的是 unfinished assignments。

5. **不在 Introduction 中重复 Contributions 小节。**  
   此处只说明方法思想、关键机制和它们如何回答前文问题；正式首创性和贡献仍放在后续 `Contributions` 部分。

---

## 8. 替换时的同步检查

将上述英文正文替换到 LaTeX 后，还应同步检查：

- 将原 Introduction 中 structured-method citations 从 `[14], [15]` 改为 `[5], [14]`；
- 将 learning-based citations 统一为 `[15], [16]`；
- 保留 LTL2BA 为 `[17]`；
- 检查 `Büchi` 的编码和字体是否正常；
- 全文统一使用 `replanning`，不要在 `re-planning`、`online repair`、`plan adaptation` 之间无规则切换；
- Introduction 中建议使用 `online plan repair` 作为一般能力表述，Section VIII 标题可继续使用 `Plan Adaptation under Robot Unavailability`；
- 若后续 Contributions 仍写 `higher-quality first feasible plan`，建议改为“score-guided construction tends to find a lower-cost first feasible plan”或结合实验结果表述，避免把启发式效果写成理论保证。
