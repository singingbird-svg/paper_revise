# System Overview 修改方案

## 0. 总体判断

当前 **System Overview** 已经覆盖了主要流程：

\[
\phi
\rightarrow
\text{VWAA}
\rightarrow
\text{GBA pruning}
\rightarrow
\text{joint NBA/plan-graph construction}
\rightarrow
\Pi_{\mathrm{init}}
\rightarrow
\Pi_{\mathrm{plan}}
\rightarrow
\text{BnB}.
\]

但从审稿人的阅读体验看，它目前更像是对 Introduction 中方法段落的再次压缩，而不是一张真正的“框架地图”。最明显的问题不是内容缺失很多，而是：

1. **核心设计原则没有被抽象出来。**  
   你真正有价值的设计不是简单串联几个模块，而是让不同粒度的 planning information 分阶段进入 automaton generation：
   - 在 GBA construction 中使用 robot-type/cardinality feasibility，提前删除当前团队必然无法执行的结构；
   - 在 NBA generation 中使用具体 assignment、predicted position 和 completion time，立即判断新出现的 temporal progress 能否转化为 executable plan progress。

2. **三个规划结果之间的关系没有完全讲清楚。**
   - \(\Pi_{\mathrm{init}}\)：joint construction 中最先发现的 accepting feasible plan；
   - \(\Pi_{\mathrm{plan}}\)：joint construction 完成时，plan graph 中发现的最低代价 plan；
   - \(\Pi^\star\)：warm-started BnB 返回的最佳 incumbent。

   当前文本虽然都提到了，但没有把这三个对象明确组织成“早期首解—构造阶段改进—BnB 精化”的三级关系。

3. **System Overview 与 Fig. 2、Algorithm 1 不完全一致。**
   - Fig. 2 包含 execution 和 online replanning，但正文没有解释这条闭环；
   - Algorithm 1 只包含 initial planning 和 BnB，没有反映 online repair；
   - Algorithm 1 的 `CONSTRUCTPLANGRAPH` 实际同时生成 NBA，却没有在函数名中体现本文最核心的 joint construction；
   - Algorithm 1 计算了 \(J^\star\)，但输出只写 “Feasible plan \(\Pi^\star\)”；
   - retained plan graph 是 online repair 的关键输入，但 Algorithm 1 没有把 \(G_P\) 作为需要保留的输出。

4. **阶段边界还不够清楚。**  
   当前第一段连续讲 AST、VWAA、两类 GBA pruning；第二段连续讲 assignment、first plan、\(\Pi_{\mathrm{plan}}\) 和 BnB。审稿人可以理解流程，但不容易快速回答：
   - 哪一步使用的是 aggregate team feasibility？
   - 哪一步开始做具体 robot assignment？
   - 哪个阶段首次产生 executable plan？
   - 哪个结构被后续优化和 failure repair 复用？

因此，我建议把当前两段式概述重构为：

> **central design principle → planning-aware GBA reduction → joint NBA–plan-graph construction → BnB refinement and execution-time repair**

并让每一阶段都明确说明：

> 输入是什么 → 核心操作是什么 → 输出传给谁 → 解决什么问题。

---

# 1. 两篇参考论文最值得借鉴的写法

## 1.1 *From Ambiguous Language to Verifiable Plans*

这篇论文的 `Methodology—Overview` 很短，但写法非常清楚。它先给出一个 **unifying design principle**，随后按模块说明：

- 每个模块接收什么信息；
- 生成什么中间结果；
- 该结果如何传给下一个模块；
- 三个模块如何共同服务一个中心目标。

它没有在 Overview 中提前给出算法公式，也没有逐行解释 pseudocode。

### 适合你借鉴的原则

你的 System Overview 第一段也应该先提出一个统一设计原则：

> **Planning information is introduced progressively during LTL-to-automaton translation: coarse robot-team feasibility is used at the GBA level, whereas state-dependent robot allocation is performed during NBA generation.**

这句话比单纯写：

> “We integrate task allocation into automaton construction.”

更精确，也能把你的两类 pruning 和 joint construction 统一起来。

### 不适合直接模仿的地方

该参考论文的三个模块相对独立，且有清晰的 perception/semantic/planning 边界。你的方法则是一条连续的 automata-based planning pipeline，所以不适合机械地写成三个并列模块。你的阶段之间存在明确的前后依赖：

\[
G_\phi^-
\rightarrow
(G_P,\Pi_{\mathrm{init}},\Pi_{\mathrm{plan}})
\rightarrow
\Pi^\star.
\]

因此，你应该采用“阶段式架构”，而不是照搬“独立模块式架构”。

---

## 1.2 *Temporal Logic Task Allocation in Heterogeneous Multirobot Systems*

这篇论文的 `Outline of the Proposed Method` 更强调：

- 方法分成哪几个阶段；
- Algorithm 1 如何体现这些阶段；
- 每一阶段产生什么中间结构；
- 后续章节分别解释哪一个阶段。

它的优点是 workflow 非常清楚，而且正文与 pseudocode、section organization 之间完全对应。

### 适合你借鉴的原则

你的 Overview 应该明确建立以下映射：

| Overview 阶段 | 后续章节 |
|---|---|
| Planning-aware GBA reduction | Sec. V |
| Joint NBA–plan-graph construction and residual-obligation ordering | Sec. VI |
| Warm-started BnB refinement | Sec. VII |
| Repair under robot unavailability | Sec. VIII |

这样审稿人读完 Overview 后，已经知道后文的技术结构。

### 不适合直接模仿的地方

Luo and Zavlanos 的 outline 几乎逐行跟随 Algorithm 1，篇幅较长。你的论文已经有 Fig. 2，而且后续 Sections V–VIII 分工明确，因此没有必要在 Overview 中再次展开：

- greedy assignment 的完整规则；
- score 的公式；
- BnB lower/upper bound；
- repair 的具体搜索细节。

这些应留在对应方法章节。

---

# 2. 最适合本文的写法

综合两篇参考论文，我建议采用一种混合写法：

1. **借鉴第一篇参考论文：**  
   用第一段提出统一设计原则，并概括整个 architecture。

2. **借鉴第二篇参考论文：**  
   按前后依赖顺序解释各阶段的 input/output，并把各阶段映射到后续章节。

3. **根据你自己的创新重新组织：**  
   将整个系统写成三个主要 planning stages 和一个 execution-time feedback loop：

   1. Planning-Aware GBA Reduction；
   2. Joint NBA–Plan-Graph Construction；
   3. Plan-Graph BnB Refinement；
   4. Execution-Time Plan Repair。

这不是照搬任何一篇模板，而是与你的实际技术结构最匹配的方式。

---

# 3. 当前版本的具体问题

## 3.1 第一段仍在重复 Introduction，而没有完全承担 Overview 的功能

当前开头：

> The key idea is to integrate task-allocation reasoning into the LTL-to-automaton translation process, instead of constructing the complete NBA before planning.

这句话本身没有问题，但在 Introduction 和 Contributions 中已经多次出现。System Overview 不应只重复这句话，而应立即进一步说明：

> **planning information 在哪两个 translation stage 进入，以及两个阶段使用的信息粒度有何不同。**

推荐改为：

> The framework introduces planning information progressively into the LTL2BA pipeline: aggregate robot-team feasibility is used during GBA construction, whereas explicit state-dependent robot allocation is performed during GBA-to-NBA generation.

这样一开始就增加了新的架构信息。

---

## 3.2 两类 GBA pruning 应明确区分发生时间和作用

当前写法：

> During the subsequent GBA construction, transitions that cannot be realized ... are pruned immediately. After the GBA is generated, progress-consistent decomposable transitions are removed ...

内容是对的，但建议明确包装成一个统一阶段：

> **Planning-Aware GBA Reduction**

其中：

- during GBA construction：
  team-infeasible candidate transition screening；
- after GBA construction but before degeneralization：
  progress-consistent decomposable-transition pruning。

两者共同的输出是：

\[
G_\phi^-.
\]

这样后文进入 joint construction 时，输入非常清楚。

---

## 3.3 “infeasible successors are discarded” 容易产生歧义

当前写法：

> Infeasible successors are discarded, whereas feasible task progressions are inserted into the plan graph.

这可能被理解为：

> 一个 assignment 在某个 plan node 上失败，就把对应 NBA successor/state/transition 全局删除。

但从 Algorithm 2–3 看，失败的是特定的 **parent-plan-node/transition extension**；同一个 NBA transition 可能从另一个 execution state 或 plan node 获得可行 assignment。

### 建议改成

> If the induced subtask cannot be assigned from a particular parent plan node, only that plan-graph extension is discarded; otherwise, a successor plan node is created or reused.

这会更严谨。

---

## 3.4 residual-obligation score 在 Overview 中过弱

Fig. 2 明确画出了 score-guided expansion，但当前 System Overview 正文没有解释它。

建议用一句话概括，不需要提前给公式：

> A residual-obligation score combines the current partial-plan cost with an estimate of the unavoidable remaining task burden and prioritizes the corresponding NBA states and plan-graph branches.

这句话同时解释：

- score 看什么；
- score 排序谁；
- 为什么它与 joint construction 有关。

---

## 3.5 三类 plan 的关系应明确写成层级

建议在 Overview 中直接建立：

\[
\Pi_{\mathrm{init}}
\longrightarrow
\Pi_{\mathrm{plan}}
\longrightarrow
\Pi^\star.
\]

具体含义：

| 符号 | 获得时刻 | 含义 |
|---|---|---|
| \(\Pi_{\mathrm{init}}\) | 首次生成 accepting prefix–suffix structure | 第一个可执行方案 |
| \(\Pi_{\mathrm{plan}}\) | joint construction 完成 | construction 阶段发现的最佳方案 |
| \(\Pi^\star\) | BnB 搜索后 | BnB 返回的最佳 incumbent |

还应明确：

- \(T_{\mathrm{first}}\) 是从 planning 开始到 \(\Pi_{\mathrm{init}}\) 首次可用的 elapsed time；
- \(\Pi_{\mathrm{plan}}\) warm-starts BnB；
- 如果 BnB 完整结束，\(\Pi^\star\) 在 retained \(G_P\) 上最优；
- 如果受到 runtime/memory limit，\(\Pi^\star\) 是 best incumbent，而不应无条件称为 original problem 的 global optimum。

---

## 3.6 online repair 是当前 Overview 最大的内容缺口

Fig. 2 的下方清楚画出：

> execution → robot failure → current task progress → new root → BnB re-optimization → repaired plan

但 System Overview 完全没有解释。

这会使审稿人产生两个疑问：

1. retained plan graph 为什么需要保留？
2. online repair 与 initial BnB 的关系是什么？

建议明确写出：

- execution layer monitors confirmed task progress and robot availability；
- unavailable robots are removed；
- the retained plan graph is re-rooted at the latest confirmed progress/execution state；
- unfinished assignments are re-optimized over the remaining team；
- LTL-to-automaton translation and plan-graph construction do not need to be repeated；
- if no feasible continuation remains, the repair procedure reports infeasibility。

注意全文建议统一使用：

> **robot unavailability**

而不是 Fig. 2 中的 `robot failure`、正文中的 `failure`、标题中的 `unavailability` 混用。

---

## 3.7 path-planning block 应在正文中解释其范围

Fig. 2 包含 `Path Planning`，但 Overview 没有说明它与本文方法的关系。

建议补一句：

> The resulting task-level plan specifies the assigned robots and target regions and is passed to a conventional path-planning layer for execution; the focus of this work is the high-level temporal-logic task-allocation process.

这样不会让审稿人误以为后面还应出现一个新的 path-planning algorithm。

---

# 4. 推荐的阶段输入—输出关系

| 阶段 | 主要输入 | 核心处理 | 主要输出 |
|---|---|---|---|
| Planning-Aware GBA Reduction | \(\phi,V_\phi,R,c\) | team-feasibility screening + progress-consistent decomposition pruning | \(G_\phi^-\) |
| Joint NBA–Plan-Graph Construction | \(G_\phi^-,R,\nu_0\) | synchronous degeneralization, assignment, score-guided expansion | \(G_P,\Pi_{\mathrm{init}},T_{\mathrm{first}},\Pi_{\mathrm{plan}}\) |
| BnB Refinement | \(G_P,\Pi_{\mathrm{plan}}\) | path/assignment optimization with warm start | \(\Pi^\star,J^\star\) |
| Online Repair | \(G_P,\nu_{\mathrm{cur}},R_{\mathrm{avail}}\) | re-rooting + BnB re-optimization | \(\Pi_{\mathrm{rep}},J_{\mathrm{rep}}\) or infeasibility |

这张关系表不一定需要放入论文正文，但应当作为你重写 Overview 时的内部逻辑。

---

# 5. 最推荐的完整英文替换稿

建议将当前 `IV. SYSTEM OVERVIEW` 的两段正文全部替换为下面版本。标题也可以考虑由 `SYSTEM OVERVIEW` 改成更准确的：

```latex
\section{Framework Overview}
```

如果你希望保持当前标题，正文不受影响。

```latex
\section{System Overview}

Figure~2 illustrates the proposed framework, and
Algorithm~1 summarizes its initial planning and refinement
procedure. For convenience, let
$\mathcal{I}=(\phi,W,R,c)$ denote an instance of the
LTL-MRTA problem in Sec.~III, where $c$ is the
action-requirement map. The framework converts the global LTL specification into an executable robot-assignment plan while
avoiding a strict separation between temporal-logic processing
and task allocation. Its central design principle is to introduce
planning information progressively into the LTL2BA pipeline:
aggregate robot-team feasibility is used during GBA generation,
whereas explicit state-dependent robot allocation is performed
as NBA transitions are generated. The resulting plan graph is
retained as a common planning structure for early solution
extraction, subsequent optimization, and execution-time repair.

\emph{1) Planning-aware GBA reduction:}
The input formula $\phi$ is first parsed into an abstract syntax
tree and translated into a VWAA following the standard LTL2BA
front end. During VWAA-to-GBA construction, each candidate
GBA transition is checked against the type and cardinality
requirements of the available robot team. A candidate that
cannot be realized by any robot assignment is discarded before
it is inserted into the GBA. After GBA construction, a second
reduction removes progress-consistent decomposable transitions
whose acceptance progress can be reproduced by a sequence of
less restrictive transitions. This step avoids propagating
team-infeasible structure and unnecessary synchronization to
the subsequent NBA and planning stages. The resulting pruned
GBA is denoted by $G_\phi^-$ and is detailed in Sec.~V.

\emph{2) Joint NBA--plan-graph construction:}
Starting from $G_\phi^-$, the framework performs
GBA-to-NBA degeneralization while constructing the plan graph
$G_P$ synchronously. The root plan node $\nu_0$ is initialized
from the initial robot positions and completion times. Whenever
a symbolic NBA transition is generated, its induced subtask is
evaluated from each compatible parent plan node using the
stored robot assignments and predicted execution state. If no
feasible assignment exists for a particular parent--transition
extension, only that plan-graph extension is discarded;
otherwise, a successor plan node is created or reused and its
predicted robot positions and completion times are updated.
A residual-obligation score combines the current partial-plan
cost with an estimate of the unavoidable remaining task burden
and prioritizes the corresponding NBA states and plan-graph
branches. As soon as an accepting prefix--suffix structure is
reached, the first feasible plan $\Pi_{\mathrm{init}}$ is made
available, and the elapsed time is recorded as
$T_{\mathrm{first}}$. The construction then continues, with
$\Pi_{\mathrm{plan}}$ initialized by $\Pi_{\mathrm{init}}$ and
updated whenever a lower-cost accepting plan is found.
Consequently, $\Pi_{\mathrm{plan}}$ is the best feasible plan
found during the complete joint construction. This stage is
presented in Sec.~VI.

\emph{3) Plan refinement and execution-time repair:}
After joint construction and reachability-based simplification
of $G_P$, the plan-graph solution $\Pi_{\mathrm{plan}}$
warm-starts the branch-and-bound optimizer in Sec.~VII. The
optimizer jointly selects a root-to-accepting path in $G_P$ and
feasible robot assignments along that path. If the search is
completed, the returned plan is optimal over the paths and
assignments retained in $G_P$; if it is terminated by a runtime
or memory limit, the best incumbent found so far is returned as
$\Pi^\star$. The resulting task-level plan is passed to a
path-planning layer for execution. During execution, the
confirmed task progress and robot availability are monitored.
When a robot becomes unavailable, the retained plan graph is
re-rooted at the latest confirmed progress and execution state,
and the unfinished subtasks are re-optimized over the remaining
team, as described in Sec.~VIII. This reuse avoids repeating the
LTL-to-automaton translation and joint plan-graph construction;
if no feasible continuation remains, the repair procedure reports
infeasibility.
```

---

# 6. 为什么这一版更适合你的论文

## 6.1 第一段不再重复 Introduction，而是给出新的架构抽象

最关键的新表述是：

> aggregate robot-team feasibility is used during GBA generation, whereas explicit state-dependent robot allocation is performed as NBA transitions are generated.

它准确区分了：

- GBA 阶段并没有进行完整的具体 robot assignment，而是做 coarse team-feasibility screening；
- 具体 assignment 从 NBA generation / plan-graph extension 开始。

这比笼统说“planning is integrated during automaton construction”更专业。

---

## 6.2 每一阶段都有明确的输入和输出

审稿人能够快速得到：

\[
\phi
\rightarrow
G_\phi^-
\rightarrow
(G_P,\Pi_{\mathrm{init}},\Pi_{\mathrm{plan}})
\rightarrow
\Pi^\star.
\]

并理解 \(G_P\) 为什么需要在 execution 中保留。

---

## 6.3 对 first solution、construction solution 和 refined solution 的定位不再混乱

该版本明确区分：

\[
\Pi_{\mathrm{init}}
\neq
\Pi_{\mathrm{plan}}
\neq
\Pi^\star
\]

在一般情况下分别对应：

- earliest feasible；
- best found during construction；
- best returned after BnB。

这与后续实验中的 \(J_{\mathrm{first}}\)、\(J_{\mathrm{plan}}\)、\(J_{\mathrm{best}}\) 也更容易对齐。

---

## 6.4 repair 不再像附加模块

当前 Fig. 2 已经表明 repair 使用 retained plan graph，但正文没有建立这种关系。

推荐版明确说明：

> \(G_P\) 是 first-plan generation、refinement 和 repair 的 shared planning structure。

因此 repair 变成 architecture 的自然延伸，而不是最后额外添加的一节。

---

# 7. Algorithm 1 的推荐修改

## 7.1 当前 Algorithm 1 的主要问题

当前：

```latex
Require: LTL formula $\phi$, workspace $W$, robot team $R$,
atomic propositions $AP$.
Ensure: Feasible plan $\Pi^\star$.
```

存在以下问题：

1. `AP` 已由 task specification 和 \(\phi\) 给出，单独作为 input 意义较弱；
2. 算法实际还依赖 action-requirement map \(c\)；
3. `CONSTRUCTPLANGRAPH` 的名称没有体现它同时构造 NBA；
4. 算法得到 \(J^\star\)，但 output 没有写；
5. online repair 需要 retained \(G_P\)，但 output 没有保留；
6. \(\Pi_{\mathrm{init}}\) 和 \(T_{\mathrm{first}}\) 是论文核心评价对象，但 algorithm interface 没有显示；
7. `Feasible plan` 没有考虑无可行 continuation 的输出。

---

## 7.2 最推荐的 Algorithm 1

建议让 Algorithm 1 专门描述 **initial planning and refinement**。Online repair 在 Overview 正文和 Sec. VIII 中说明，不建议把 asynchronous execution loop 强行塞入同一个 pseudocode。

```latex
\begin{algorithm}[t]
\caption{Initial On-the-Fly Planning and Refinement}
\label{alg:framework}
\begin{algorithmic}[1]
\Require LTL-MRTA instance
$\mathcal{I}=(\phi,W,R,c)$.
\Ensure Best plan found $\Pi^\star$, its cost $J^\star$,
and retained plan graph $G_P$, or \textsc{Infeasible}.
\State $T_\phi \gets \textsc{ParseToAST}(\phi)$.
\State $V_\phi \gets \textsc{ConstructVWAA}(T_\phi)$.
\State $G_\phi^- \gets
\textsc{ConstructAndPruneGBA}(V_\phi,R,c)$.
\State $\nu_0 \gets \textsc{InitializeRootNode}(\mathcal{I})$.
\State $(G_P,\Pi_{\mathrm{init}},T_{\mathrm{first}},
\Pi_{\mathrm{plan}})
\gets
\textsc{ConstructNBAAndPlanGraph}
(G_\phi^-,\mathcal{I},\nu_0)$.
\If{$\Pi_{\mathrm{plan}}=\emptyset$}
    \State \Return \textsc{Infeasible}.
\EndIf
\State $(\Pi^\star,J^\star)
\gets
\textsc{BnBOptimizer}(G_P,\Pi_{\mathrm{plan}})$.
\State \Return
$(\Pi^\star,J^\star,G_P)$.
\end{algorithmic}
\end{algorithm}
```

### 最重要的函数名修改

当前：

```latex
CONSTRUCTPLANGRAPH
```

建议改为：

```latex
CONSTRUCTNBAANDPLANGRAPH
```

或：

```latex
JOINTAUTOMATONPLANCONSTRUCTION
```

我更推荐第一个，因为它直接、无歧义，而且与 Sec. VI 的内容一致。

如果不希望大规模更改函数名，至少应在 Algorithm 1 前明确写：

> `CONSTRUCTPLANGRAPH` performs GBA-to-NBA degeneralization and plan-graph construction jointly.

但从突出创新的角度，直接改名效果更好。

---

## 7.3 online repair 的 overview-level interface

不必在 Algorithm 1 中写完整 execution loop，但建议在 Sec. VIII 或 Overview 末尾明确给出：

\[
(\Pi_{\mathrm{rep}},J_{\mathrm{rep}})
=
\textsc{BnBRepair}
\bigl(
G_P,\nu_{\mathrm{cur}},R_{\mathrm{avail}}
\bigr),
\]

其中：

- \(\nu_{\mathrm{cur}}\)：由 latest confirmed task progress 和 execution state 确定的新 root；
- \(R_{\mathrm{avail}}\)：剩余可用 robot team；
- \(\Pi_{\mathrm{rep}}\)：repaired continuation plan。

并明确当不存在 feasible continuation 时返回 `Infeasible`。

---

# 8. Fig. 2 的修改建议

当前 Fig. 2 已经能够显示大体流程，但视觉上还没有完全突出本文真正的 integration point。

## 8.1 建议修改模块标题

当前：

> On-the-fly Plan Graph Construction

建议：

> **Joint NBA–Plan-Graph Construction**

或者：

> **On-the-Fly Automaton–Allocation Co-Construction**

前者更直观，也与方法章节对应。

---

## 8.2 在中间模块中明确画出 NBA

当前图中 plan graph 比较突出，但 NBA generation 不够明显。

建议中间模块明确画成：

```text
Pruned GBA
    ↓ GBA-to-NBA degeneralization
New NBA transition
    ↓ immediate assignment evaluation
Plan-graph extension
```

这样 reviewer 一眼能看出：

> allocation 介入的是 NBA generation，而不是在已有完整 NBA 上搜索。

---

## 8.3 从中间模块增加一个 early-output arrow

建议从 joint construction 模块直接引出：

\[
(\Pi_{\mathrm{init}},T_{\mathrm{first}})
\]

并标注：

> first accepting prefix–suffix structure

然后再从 construction completion 输出：

\[
(G_P,\Pi_{\mathrm{plan}})
\]

到 BnB。

这能把本文最重要的“before complete NBA”视觉化，而不只依赖正文说明。

---

## 8.4 明确 BnB 的 warm start

从 joint construction 到 BnB 的箭头建议标注：

\[
\Pi_{\mathrm{plan}} \quad \text{(warm start)}
\]

同时 \(G_P\) 作为 search domain 输入 BnB。

---

## 8.5 统一 repair terminology

建议全文和图中统一采用：

- `Robot Unavailability`
- `Online Plan Repair`
- `Re-root Retained Plan Graph`
- `BnB Re-optimization`

避免混用：

- Robot Failure；
- Online Replanning；
- Plan Adaptation；
- Repair。

论文节标题可以保留：

> Plan Adaptation under Robot Unavailability

但图中最好采用更短的：

> Online Plan Repair。

---

## 8.6 建议的新 Fig. 2 caption

```latex
\caption{Overview of the proposed on-the-fly LTL-MRTA
framework. The input LTL formula is first reduced at the GBA
level using robot-team feasibility and progress-consistent
decomposition. During GBA-to-NBA degeneralization, each newly
generated NBA transition is evaluated through robot assignment,
and feasible extensions are stored in the plan graph. The first
accepting prefix--suffix plan $\Pi_{\mathrm{init}}$ is made
available immediately, while construction continues to obtain
the plan-graph solution $\Pi_{\mathrm{plan}}$.
$\Pi_{\mathrm{plan}}$ warm-starts branch-and-bound refinement.
During execution, robot unavailability triggers re-rooting of the
retained plan graph and BnB re-optimization over the remaining
team.}
```

---

# 9. 与后续章节标题的协调建议

为了让 Overview 和后文完全一致，可以考虑以下标题：

| 当前标题 | 推荐标题 |
|---|---|
| IV. System Overview | IV. Framework Overview |
| V. Pruning for GBA | V. Planning-Aware GBA Reduction |
| VI. On-the-Fly Plan Graph Construction | VI. Joint NBA–Plan-Graph Construction |
| VII. Branch-and-Bound Optimization | 保留 |
| VIII. Plan Adaptation Under Robot Unavailability | 保留或改为 Online Plan Repair Under Robot Unavailability |

不是必须全部修改，但 Sec. VI 强烈建议加入 `NBA`，因为只写 `Plan Graph Construction` 会弱化你的核心创新。

---

# 10. 一个版面更紧的备选文本

如果完整版过长，可以使用下面的压缩版。

```latex
\section{System Overview}

Figure~2 and Algorithm~1 summarize the proposed framework.
Its central design principle is to introduce planning information
progressively into LTL-to-automaton translation: aggregate
robot-team feasibility is used during GBA generation, whereas
explicit state-dependent robot allocation is performed as NBA
transitions are generated.

The input LTL formula is first parsed into an AST and
translated into a VWAA. During VWAA-to-GBA construction,
candidate transitions that cannot be realized by the available
robot types and cardinalities are discarded before insertion.
After the GBA is constructed, progress-consistent decomposable
transitions are removed to avoid propagating unnecessary
synchronization. The resulting pruned GBA $G_\phi^-$ is then
degeneralized into an NBA while the plan graph $G_P$ is
constructed synchronously.

Each newly generated NBA transition induces a subtask that
is evaluated from the execution state stored in its parent plan
nodes. An infeasible parent--transition extension is discarded,
whereas a feasible assignment creates or reuses a successor plan
node. A residual-obligation score prioritizes successor NBA
states according to partial-plan cost and estimated remaining
task burden. The first accepting prefix--suffix structure yields
$\Pi_{\mathrm{init}}$ and $T_{\mathrm{first}}$. Construction then
continues, updating $\Pi_{\mathrm{plan}}$ whenever a lower-cost
accepting plan is found.

After $G_P$ is completed and simplified,
$\Pi_{\mathrm{plan}}$ warm-starts a branch-and-bound search,
which returns the best plan $\Pi^\star$ found over the retained
graph. The same graph is retained during execution. If a robot
becomes unavailable, $G_P$ is re-rooted at the latest confirmed
task progress and the unfinished assignments are re-optimized
over the remaining team without repeating automaton
translation or plan-graph construction.
```

### 推荐选择

优先使用第 5 节的完整版，因为你的 framework 确实包含四个相互关联的阶段，而且 repair 是论文完整性的重要部分。

版面压力较大时，再使用本节压缩版。

---

# 11. 最终推荐

最适合你的 System Overview 不应只是“方法流水账”，也不应照搬参考论文的模块命名。它应该让审稿人形成下面这张清楚的内部图景：

\[
\underbrace{
\text{team-level feasibility}
}_{\text{coarse planning information}}
\rightarrow
\text{GBA reduction}
\]

\[
\underbrace{
\text{assignments + predicted execution state}
}_{\text{state-dependent planning information}}
\rightarrow
\text{joint NBA--plan-graph construction}
\]

\[
\Pi_{\mathrm{init}}
\rightarrow
\Pi_{\mathrm{plan}}
\rightarrow
\Pi^\star
\]

\[
G_P
+
\text{confirmed progress}
+
R_{\mathrm{avail}}
\rightarrow
\Pi_{\mathrm{rep}}.
\]

这四行就是整个 System Overview 应向 reviewer 传达的核心内容。

其中最重要的创新定位是：

> **本文不是简单在 automaton construction 后增加一个更快的 allocator，而是让 planning information 以不同粒度进入 automaton generation，并用同一个 retained plan graph 串联 early feasibility、subsequent refinement 和 execution-time repair。**
