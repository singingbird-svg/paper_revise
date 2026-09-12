# LTL-MRTA 论文 Introduction 修改方案

## 修改范围

- **待修改论文**：*On-the-Fly Temporal-Logic Task Allocation for Heterogeneous Multi-Robot Systems during Büchi Automaton Generation*
- **参考论文**：*From Ambiguous Language to Verifiable Plans: Integrating Formal Synthesis and Dynamic Affordance Reasoning*
- **本次范围**：仅修改 `I. INTRODUCTION` 中 **`A. Related Work` 之前的正文**。
- **不在本部分单独列出 Contributions**：创新性通过问题推导、设计要求和方法概述自然体现；正式贡献仍放在后续 `Contributions` 小节。
- **资料依据**：待修改论文第 1-2 页；参考论文第 1-2 页。

---

## 1. 总体判断

当前版本已经包含应用背景、LTL-MRTA 问题、现有方法、学习方法以及本文框架，但各段之间仍偏向“背景介绍 + 方法流程说明”，尚未形成参考论文那种连续、闭合的必要性论证。

参考论文最值得借鉴的不是其具体技术术语，而是以下写作链条：

> **实际场景中的矛盾 -> 抽象出核心问题 -> 说明现有范式为何产生该问题 -> 给出具体后果 -> 推导设计要求 -> 用一句 central idea 统领方法 -> 说明各机制如何逐一满足前述要求。**

对于本文，最合适的主线不是“机器人失效后需要重规划”，也不是笼统的“复杂 LTL 导致计算量大”，而是：

> **逻辑上允许的任务进程不一定能由当前异构团队执行；如果机器人类型、数量和部分分配状态直到完整自动机生成后才进入规划，大量对当前团队无执行价值的结构仍会被传播，从而延迟首次可执行分配。**

这条主线可以同时解释为什么需要 GBA 层剪枝、为什么要同步构造 NBA 与 plan graph、为什么要使用 residual-obligation score，以及为什么保留 plan graph 能支持后续 makespan refinement 和机器人不可用后的计划修复。

---

## 2. 参考论文风格中应借鉴的部分

### 2.1 用一个实际场景暴露“方法为什么必须这样设计”

参考论文不是先罗列技术背景，而是先用一个容易理解的任务说明“现有系统会在哪里失败”。本文也应采用仓储或工厂场景，但应控制在任务层面，不写机器人编号、具体数量、区域编号或 LTL 公式。这些细节属于 `Problem Description` 和 `Example 1`。

本文开篇场景应展示以下事实：

- 任务同时包含顺序、持续、安全和协作要求；
- 同一个全局 LTL 任务允许多种逻辑进程；
- 其中一些进程可能超过当前团队的类型或数量能力；
- 一些独立任务可能被不必要地绑定在同一转移上；
- 如果这些问题到完整自动机生成后才被发现，前期计算没有直接转化为可执行方案。

### 2.2 不只说“现有方法慢”，而要说明“为什么慢”

当前版本从规模增长直接跳到“first feasible solution 很重要”，中间缺少根因。应明确指出：

- 自动机构造主要依据逻辑一致性；
- 机器人可执行性还依赖类型、基数、可达性、同一子任务中的互斥分配以及预测执行状态；
- 当 translation 与 allocation 被分开时，这些信息进入得过晚；
- 因而 automaton construction 或 task-structure extraction 仍位于首次可行解的关键路径上。

### 2.3 先推导设计要求，再介绍方法

参考论文在介绍框架前先总结三项 requirements。本文也适合采用这一方式，但这些是**设计要求**，不是贡献列表：

1. 在无价值结构进入最终 NBA 之前，识别团队不可行性和可避免的同步；
2. 使任务分配随自动机生成同步推进，使接受结构一旦可分配即可返回执行方案；
3. 保留早期方案和中间搜索结构，以支持后续 makespan refinement，并在全局 LTL 任务不变时更新未完成分配。

### 2.4 用一句 central idea 统领全部机制

建议采用如下核心表达：

> **The central idea is to treat automaton construction as a planning process informed by the current robot team, rather than as a planning-independent preprocessing stage.**

这句话与后文形成一一对应：

- “informed by the current robot team” -> GBA 阶段的类型/基数可行性检查；
- “planning process” -> NBA 与 plan graph 同步构造；
- “rather than preprocessing” -> 首次可行分配不再等待完整 NBA；
- 保留生成结构 -> BnB warm start 与 robot-unavailability repair。

---

## 3. 当前文本中的主要问题及修改方式

### 3.1 第一段场景存在，但尚未揭示核心矛盾

**当前问题**：仓储检查场景只说明存在 temporal dependencies 和 multi-robot coordination，尚未说明为什么传统的“先翻译、后分配”会造成实际问题。因此，场景与本文算法设计之间的因果联系较弱。

**修改方式**：在第一段末加入“逻辑可行不等于当前团队可执行”的矛盾，并进一步指出，如果团队信息在完整自动机之后才进入，非执行性或不必要同步会继续传播。这样，第一段就能直接为 GBA pruning 和 joint construction 提供动机。

### 3.2 “尽早得到高质量方案”混合了两个不同目标

**当前问题**：`obtain a high-quality executable plan as early as possible` 同时包含首次可行解时间和方案质量，审稿人会追问二者如何同时保证。

**修改方式**：拆分为两个阶段性目标：

- 尽早返回一个具有显式机器人分配的 feasible plan；
- 在该方案始终可用的前提下继续降低 makespan。

这与本文的 plan-graph solution 和 BnB refinement 正好呼应。

### 3.3 对顺序式范式的批评还不够具体

**当前问题**：现有文本主要说 planning starts after automaton construction，因此会慢，但没有说明完整自动机中究竟传播了什么无效信息。

**修改方式**：明确写出 automaton construction 与 executability 所使用的信息不同：前者依据逻辑一致性，后者还依赖 robot types、cardinalities、reachability、assignment disjointness 和 predicted execution state。由此得出“team-infeasible transitions and avoidable synchronization survive into downstream planning”的直接后果。

### 3.4 学习方法的优点和适用边界需要更公平、准确

当前版本已经提到 learned policy，但表述 `can still be difficult to apply to large heterogeneous robot teams with complex collaboration and temporal requirements` 过于笼统，容易被审稿人要求提供证据。

建议改成以下更精确的对照：

- **优点**：学习方法可以把部分时序推理成本摊销到训练阶段；训练完成后策略推断较快；直接公式编码方法在部署时可不为每个任务显式构造一套自动机。
- **边界**：性能通常依赖训练任务分布和训练时使用的符号接口；当前引用的学习方法并不直接输出本文所需的实例级异构分配，即同时满足类型、基数、同一子任务分配互斥、可达性和 makespan 目标。
- **结论**：学习改变了部分计算成本发生的位置，但没有消除 LTL-MRTA 中“时序进展与当前团队资源可行性”的耦合。

#### 引文分类需要修正

当前参考文献中：

- `[5]` 和 `[14]` 适合支撑 decomposition / hierarchical specification；
- `[15]` 是 *Compositional Automata Embeddings for Goal-Conditioned Reinforcement Learning*，应归入学习或 automaton-representation learning，而不应与 `[14]` 一起仅作为 structured specification 文献；
- `[16]` 是 *LTL2Action*，适合支撑直接编码 LTL 指令和多任务强化学习；
- `[17]` 是 LTL2BA，可用于本文 central idea 之后的方法落点。

因此，建议把结构化方法写为 `[5], [14]`，把学习方法写为 `[15], [16]`。最终编号仍需在 LaTeX/BibTeX 编译后复核。

### 3.5 方法段目前过于接近算法流程，中心思想不够醒目

**当前问题**：方法段直接进入 GBA、NBA、plan graph、score、BnB 和 repair，技术信息完整，但读者需要自己归纳这些模块为何属于同一创新。

**修改方式**：先给出一句 central idea，再按前述三项设计要求的顺序介绍机制：

1. GBA 层提前过滤；
2. NBA 与 plan graph 同步生成并进行即时分配；
3. 首次解、持续优化和图复用。

### 3.6 在线修复应保留，但不应成为开篇主矛盾

机器人不可用后的计划修复是 retained plan graph 的重要用途，但本文的主要方法必要性首先来自“allocation information enters automaton construction too late”。因此，repair 应放在方法概述的末尾，作为统一图表示的延伸能力，而不是第一段的主要问题。

---

## 4. 推荐的段落逻辑及前后呼应

| 段落 | 主要功能 | 本段提出的问题 | 后文对应回应 |
|---|---|---|---|
| P1 | 实际仓储场景 | 逻辑允许的进程不一定适合当前团队；还可能包含可避免同步 | P6 的 team-feasibility screen 和 decomposition pruning |
| P2 | 定义 LTL-MRTA 与实际评价目标 | 需要尽早得到显式可执行分配，同时保留后续优化能力 | P6 的 first feasible plan 和 BnB refinement |
| P3 | 解释顺序式范式的根因 | translation 只处理逻辑，allocation 才处理团队与执行状态 | P6 的 NBA-plan graph lockstep construction |
| P4 | 公平定位结构化与学习路线 | 它们分别改变规格结构或摊销推理，但不直接解决当前团队的显式异构分配 | P6 保留形式自动机并把团队信息前移 |
| P5 | 推导三项设计要求 | 提前筛选、同步分配、保留结构 | P6 按相同顺序逐项实现 |
| P6 | central idea 与方法概述 | 说明本文为何能满足前述要求 | 与 P1-P5 闭环，不另列 contributions |

这套结构中的核心“呼应”是：每个方法组件都必须回答前文已经提出的一个具体问题，而不是在最后突然出现。

---

## 5. 可直接替换的英文文本

> 下列内容可直接替换当前 `I. INTRODUCTION` 标题之后、`A. Related Work` 标题之前的全部正文。正式 Contributions 仍保留在后续小节，不在此处编号列出。

### Revised Introduction Before Related Work

Consider a large warehouse in which heterogeneous robots must retrieve inventory information, inspect storage and loading areas, service equipment, and monitor restricted zones under a common mission. Some operations must be completed in sequence, others may proceed independently, and some require robots with different capabilities to act concurrently. Linear temporal logic (LTL) provides a rigorous language for expressing such ordering, persistence, safety, and coordination requirements [4]-[6]. However, a task progression that is logically admissible need not be executable by the available team: it may demand unavailable capabilities or excessive robot cardinalities, or it may combine independent actions into an avoidable synchronization. If these facts are considered only after the complete task automaton has been generated, non-executable or unnecessarily restrictive structure is propagated into later planning stages.

This setting gives rise to LTL-based multi-robot task allocation (LTL-MRTA) [7], where the global LTL formula specifies what the team must accomplish but does not predetermine which robot performs each subtask. The planner must therefore resolve temporal progress, heterogeneous resource requirements, and robot assignments jointly. The combinatorial burden grows with the number of robots, task alternatives, and intermediate automaton transitions, and existing mixed-integer linear programming and search-based formulations can require substantial computation even to obtain one feasible solution [7]-[10]. In deployment, the relevant criterion is not only whether a solution can eventually be found: execution cannot begin until the current team has an explicit feasible allocation. At the same time, an early solution should remain available while computation continues to reduce the makespan.

Planning-decision-tree methods [11]-[13] emphasize rapid feasible-plan generation, while the poset-based method in [3] uses an anytime optimization scheme to return a valid plan and subsequently improve it. Nevertheless, their allocation or optimization stages are built on a task automaton or a task structure extracted from it. More broadly, many top-down LTL-MRTA pipelines separate LTL-to-automaton translation from robot assignment. This separation creates a structural mismatch: automaton construction is governed primarily by logical consistency, whereas executability also depends on robot types, cardinalities, reachability, mutual exclusion among simultaneous assignments, and the predicted execution state. As a result, team-infeasible transitions and branches with avoidable synchronization may survive until downstream planning, while automaton construction or task-structure extraction remains on the critical path to the first executable plan.

Existing work reduces this burden in two complementary ways. Structure-exploiting methods decompose a specification or require it to be expressed in hierarchical or otherwise compositional form [5], [14], which can substantially reduce planning complexity but transfers part of the burden to specification design and decomposition. Learning-based methods amortize temporal reasoning across a task distribution by encoding LTL formulas directly or by using automaton-derived goal representations [15], [16]. Once trained, they can provide fast policy inference, and direct formula encoders can avoid constructing a separate explicit automaton for each deployment task. These advantages are important, but they address a different source of complexity: performance depends on the learned task distribution and symbolic interface, and the cited formulations do not directly produce explicit assignments for a given heterogeneous team under robot-type, cardinality, disjointness, reachability, and makespan constraints. For the LTL-MRTA setting studied here, the remaining question is how to retain a verifiable automaton representation while allowing team feasibility and assignment information to shape its construction.

These observations suggest three design requirements. First, team-level infeasibility and avoidable synchronization should be removed before they are propagated to the final Büchi automaton. Second, task allocation should advance together with automaton generation, so that a feasible accepting progression immediately yields an executable plan rather than waiting for the complete automaton. Third, the early plan and the partial planning structure should be retained for subsequent makespan refinement and, when the temporal mission remains unchanged, for updating unfinished assignments after changes in robot availability.

To meet these requirements, we propose a framework that integrates task-allocation reasoning into the LTL-to-automaton translation process. The central idea is to treat automaton construction as a planning process informed by the current robot team, rather than as a planning-independent preprocessing stage. Building on the LTL2BA translation pipeline [17], the framework screens candidate generalized Büchi automaton (GBA) transitions against the robot types and cardinalities available in the team before insertion. After GBA construction and before degeneralization, it removes progress-consistent decomposable transitions that would otherwise impose unnecessary synchronization. During GBA-to-nondeterministic Büchi automaton (NBA) generation, the NBA and a plan graph are constructed in lockstep. Each newly generated NBA transition induces a subtask, and its feasible assignment, predicted robot positions, and completion times are recorded immediately in the plan graph. A residual-obligation score orders pending successors according to the current plan cost and an estimate of the remaining positive action obligations, allowing lower-scored feasible branches to be explored earlier. The joint construction returns a feasible plan as soon as it reaches an accepting prefix-suffix structure with a valid allocation; it then continues to update the best plan-graph solution, which warm-starts branch-and-bound makespan refinement over the retained graph. If robots become unavailable during execution, the same graph is re-rooted at the last confirmed task progress and the unfinished assignments are re-optimized over the surviving team. Thus, the proposed workflow connects early executability, continued plan improvement, and plan repair through a single representation while preserving the original global LTL mission.

---

## 6. 为什么上述版本更适合本文

### 6.1 第一段直接解释算法设计的实际必要性

新版没有使用具体机器人数量、机器人编号或 LTL 公式，但明确呈现了两类与本文方法直接相关的实际问题：

- 当前团队无法执行某些逻辑上允许的联合要求；
- 独立动作可能被自动机转移不必要地同步。

这两个问题分别对应 infeasible-transition pruning 和 progress-consistent decomposition，而不是泛泛地说“大规模问题计算慢”。

### 6.2 首次解和方案质量被明确分成两个阶段

新版使用：

- `execution cannot begin until ... an explicit feasible allocation` 说明首次解的实际价值；
- `computation continues to reduce the makespan` 说明后续优化目标。

因此，residual-obligation ordering、plan-graph solution 和 BnB refinement 不再像三个松散模块，而是共同服务于“先可执行、后改进”的同一目标。

### 6.3 对学习方法的定位不会产生明显反驳点

新版没有声称“学习方法不能处理长 LTL”或“学习方法没有形式保证”，而是承认其可以摊销推理并加快部署推断。区别被限定为本文问题真正要求的输出：针对**给定异构团队**生成满足类型、数量、互斥、可达性和 makespan 约束的显式分配。这一比较更公平，也更难被相关工作反驳。

### 6.4 创新点通过因果关系突出，而不是提前重复 Contributions

新版没有使用 `The key contributions are as follows`，也没有编号列出贡献。创新性体现在以下明确差异上：

- 在 GBA transition 插入前使用团队类型和基数信息；
- 在 GBA-to-NBA 过程中同步扩展 plan graph；
- 用当前 plan cost 和 remaining positive action obligations 排序候选；
- 把同一个 retained graph 用于首次解、后续优化和机器人不可用后的未完成分配更新。

这些内容足以在 Introduction 中建立辨识度，而正式的 novelty、theoretical result 和 experimental evidence 可以留到后面的 Contributions 小节集中陈述。

---

## 7. 语言与术语的具体修改建议

| 当前或类似表达 | 问题 | 建议表达 |
|---|---|---|
| `Formal languages such as LTL provides ...` | 主谓不一致 | `LTL provides ...` 或 `Formal languages such as LTL provide ...` |
| `the search and optimization space may expand explosively` | `explosively` 缺乏定义和证据 | `the joint space of task progressions and robot assignments grows combinatorially with ...` |
| `a high-quality executable plan as early as possible` | 混合首次解速度与质量 | `an executable allocation early, followed by makespan refinement` |
| `can still be difficult to apply to ...` | 评价过于宽泛 | 明确列出其未直接处理的 type/cardinality/disjointness/reachability/makespan constraints |
| `Motivated by these limitations, we propose a novel framework` | `novel` 属于自我评价，且缺少中心思想 | `To meet these requirements, we propose a framework that integrates ...` |
| `redundant transitions` | 太笼统 | `progress-consistent decomposable transitions that impose avoidable synchronization` |
| `higher-quality initial solution` | 若无理论保证，表述偏强 | `a lower-cost first plan empirically`，或只写 score 的排序机制 |
| `smaller estimated burdens for the remaining parts` | `parts` 不专业且含义不明确 | `an estimate of the remaining positive action obligations` |
| `continued improvement toward better solutions` | `better` 无目标函数 | `continued makespan refinement` |
| `repair the remaining mission` | 全局 LTL mission 并未改变 | `re-optimize the unfinished assignments` 或 `repair the unfinished plan` |
| `task planing` | 拼写错误 | `task planning` |
| `synchronously builds an NBA and a plan graph` | 可更自然、专业 | `constructs the NBA and the plan graph in lockstep` |

---

## 8. 需要控制的主张边界

为避免 Introduction 与后文理论范围不一致，建议注意：

1. **不要声称解决了 LTL-to-automaton translation 的最坏情况指数复杂度。** 当前方法支持的结论是提前过滤对当前团队无价值的结构，并缩短实验中的 first-plan latency。
2. **不要把 residual-obligation score 写成最优性保证。** 它是 expansion-ordering heuristic；它帮助较低分支更早被探索，但不是 admissible lower bound。
3. **不要在本部分使用宽泛的 `the first method` 声明。** 首创性应在 Contributions 中限定到可核查的机制组合，并与 Related Work 的文献比较一致。
4. **BnB 的最优性表述应与实际搜索空间一致。** 若其搜索基于 retained plan graph，应写成对该图中表示的路径和分配进行 makespan refinement，除非后文已严格证明完整全局最优性。
5. **机器人不可用后的修复应限定为全局 LTL mission 不变。** 修复对象是未完成的 assignment/plan，而不是重新解释或改变任务规范。

---

## 9. 与后续 Related Work 和 Contributions 的衔接建议

### 9.1 Related Work 不要重复本段的完整论证

本段只做研究路线的高度概括。后续 `Related Work` 应提供详细证据和代表文献，建议继续按以下主题展开：

- bottom-up 与 top-down temporal-logic planning；
- product/sampling、MILP/STAP、planning decision tree 与 poset；
- structure-exploiting specifications；
- learning-based LTL execution and automaton representations；
- 最后一段总结本文在“team information enters automaton construction when and how”方面的差异。

### 9.2 Contributions 继续单独保留

后续 Contributions 应集中回答：

- 提出了什么机制；
- 相比最接近方法，机制在哪个构造阶段介入；
- 保留了什么性质或支持什么输出；
- 理论和实验分别验证了什么。

不要在 Contributions 中再次从仓储场景开始，也不要逐句重复本次替换稿的方法概述。

---

## 10. 最终替换前检查清单

- [ ] 第一段没有机器人编号、具体数量、区域编号或 LTL 公式。
- [ ] 第一段明确出现“logically admissible but not executable by the available team”。
- [ ] 首次可行解时间与 makespan 质量被分开描述。
- [ ] 顺序式 translation-allocation 的局限被解释为信息进入过晚，而不只是笼统的“慢”。
- [ ] 结构化方法使用 `[5], [14]`，学习方法使用 `[15], [16]`，并在最终 BibTeX 编译后复核编号。
- [ ] 学习方法的优点被明确承认，没有使用“完全没有保证”等笼统判断。
- [ ] central idea 在方法细节之前出现。
- [ ] GBA pruning、joint NBA/plan-graph construction、residual-obligation ordering 和 BnB/repair 与前文问题逐项对应。
- [ ] 本部分没有 `The key contributions are as follows`，也没有编号贡献列表。
- [ ] 在线修复位于方法概述末尾，未成为开篇主线。
- [ ] `task planing`、主谓一致和 `better/novel/high-quality` 等模糊表达已清理。
