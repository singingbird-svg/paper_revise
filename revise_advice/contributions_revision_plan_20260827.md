# Contributions 修改方案

## 1. 总体判断

当前论文的 **Contributions** 并不是技术内容不足，而是**组织层级没有拉开**。现在的写法基本按照算法执行过程连续叙述：

> task allocation during NBA construction  
> → plan graph grows with NBA  
> → accepting structure gives a plan  
> → GBA pruning  
> → residual-obligation score  
> → score also guides allocation branches  
> → first-feasible-plan quality

这些内容本身都重要，但放在一个连续段落里以后，出现了三个问题：

1. **核心创新和支撑机制混在同一层级。**  
   “在 automaton generation 中进行 task allocation”是本文最核心的架构创新；GBA pruning 和 residual-obligation score 是使这一架构高效、使首个方案质量更好的关键机制；BnB 与 online repair 则是 retained plan graph 带来的后续能力。这三层现在没有区分开。

2. **重复描述 joint NBA–plan-graph construction。**  
   当前段落多次表达 “NBA and plan graph are constructed together / graph grows synchronously / same ordering guides task-allocation branches”，使真正的创新点被重复的流程描述稀释。

3. **与论文整体贡献不完全对应。**  
   Abstract、Introduction、System Overview、Sections VII–VIII 以及实验都把 **BnB refinement** 和 **robot-unavailability repair** 作为完整框架的重要部分，但当前 Contributions 几乎没有正式把它们纳入贡献。因此审稿人读完 Contributions 后，得到的“论文贡献地图”和后文实际结构并不一致。

我建议把 Contributions 从“算法流程描述”改成**3 个层级清楚、彼此互补的贡献点**：

1. **核心架构创新：On-the-fly automaton–allocation co-construction**
2. **支撑首解速度和质量的关键机制：planning-aware GBA reduction + residual-obligation-guided expansion**
3. **共享 plan graph 带来的后续能力：anytime refinement + online repair**

理论保证和实验验证放在列表后的一个收束句中，不建议单独列成第四个“创新”，否则会削弱前三项方法创新的权重。

---

# 2. 两篇模板的 Contributions 写法各自值得借鉴什么

## 2.1 模板一：*From Ambiguous Language to Verifiable Plans*

这篇文章最值得借鉴的是**“模块化命名 + 每项只回答一个核心问题”**的写法。

它的 Contributions 不是把方法流程完整复述一遍，而是：

- 先给出一个总的 central idea；
- 然后列出三个有明确名称的贡献：
  1. Scene-Conditioned Specification Synthesis；
  2. Specification-Preserving Functional Substitution；
  3. Monitor-Guided Hierarchical Recovery；
- 每一项内部基本遵循：

  > **提出什么 → 核心机制是什么 → 它解决什么问题/产生什么能力**

这种写法对你的论文非常合适，因为你的后文也天然分成：

- GBA-level pruning；
- joint NBA / plan-graph construction；
- BnB optimization；
- repair。

但是你不应该机械地“一节对应一个 contribution”，因为那样又会变成目录式描述。应该按照**创新逻辑**重新组合。

---

## 2.2 模板二：*An Exploration-Enhanced Search Algorithm for Robot Indoor Source Searching*

这篇文章的 Contributions 更简洁。它没有解释算法每一步，而是在贡献层面强调：

- 核心算法及其组成；
- 算法最终获得的新能力；
- 实验验证/benchmark。

最值得借鉴的是：

> **Contribution 不应该承担 Method section 的职责。**

例如，你当前写：

> “The score reflects the current plan cost and the estimated travel needed for the remaining tasks. Rather than following a DFS order used in standard LTL2BA construction, our method gives priority to Büchi successors with lower scores. The NBA and the plan graph are constructed together. Thus, the same ordering also guides the exploration of task-allocation branches.”

这些细节在 Section VI 很重要，但在 Contributions 中可以压缩成一句：

> “A residual-obligation score couples partial-plan cost with the estimated burden of unavoidable remaining actions, prioritizing promising automaton–allocation branches and improving first-plan quality.”

这样创新反而更突出。

---

# 3. 当前 Contributions 的具体问题

当前原文的开头是：

> We propose a new on-the-fly approach to LTL-MRTA that performs task allocation as the NBA is generated.

这句话是正确的，而且应该保留为第一贡献的核心。

但是后面连续出现：

> performs task allocation incrementally  
> feasible partial assignments ... are recorded in a plan graph  
> This graph grows synchronously with the NBA  
> executable plan becomes available ...  
> NBA and plan graph are constructed together  
> same ordering also guides ... task-allocation branches

这些句子实际上反复围绕同一个创新讲了几遍。

### 建议压缩为一个清晰的因果链

> **new NBA transition appears**  
> → **induced subtask is immediately evaluated and assigned**  
> → **feasible partial execution state is stored in the plan graph**  
> → **accepting prefix–suffix structure immediately yields a feasible plan**

四步已经足够。

---

## 3.1 “using a greedy procedure” 不建议在第一贡献里突出

当前：

> our method performs task allocation incrementally using a greedy procedure during NBA construction.

“greedy procedure”属于实现机制，不是你的核心 novelty；而且在 Contribution 的第一句话就强调 greedy，可能反而让审稿人首先想到“局部最优”。

更好的写法是：

> each newly generated NBA transition is immediately evaluated through robot assignment using the execution state stored in the current plan node.

具体 greedy assignment 留到 Section VI。

---

## 3.2 GBA pruning 的位置应该更清楚

当前先讲完 joint construction，随后才说：

> One innovation of our approach is that the GBA is pruned before NBA construction begins.

从论文机制上，GBA reduction 是在 GBA-to-NBA degeneralization 之前用于减少向下游传播的 transition structure。它应该被明确包装成：

> **planning-aware reduction before NBA generation**

同时最好区分两部分：

- during GBA construction：robot-team-infeasible transition pruning；
- after GBA construction but before degeneralization：progress-consistent decomposable-transition pruning。

这样比笼统的 “discard transitions that are infeasible or impose avoidable synchronization” 更能体现技术深度。

---

## 3.3 residual-obligation score 应突出“为什么”，而不是重复“怎么排序”

当前用了较多句子解释：

- score includes current cost；
- score includes estimated remaining burden；
- unlike DFS；
- lower score first；
- same ordering guides plan graph；
- promising branches earlier；
- better first solution。

建议压缩为：

> A residual-obligation score combines partial-plan cost with an estimate of the unavoidable remaining task burden, so the joint automaton–allocation construction explores promising branches earlier and improves first-plan quality without sacrificing early plan availability.

重点是：

> **不是单纯改变 DFS 顺序，而是在 joint construction 中用 planning information 改变 temporal-state expansion priority。**

这才是创新。

---

## 3.4 当前 Contributions 严重弱化了 BnB 和 repair

你的 Abstract 明确写了：

- plan-graph solution warm-starts BnB；
- the same graph-based workflow repairs the remaining mission under robot unavailability。

System Overview、Section VII、Section VIII 和实验也都把这两项作为完整框架的一部分。

但当前 Contributions 几乎完全没有提。

这会导致一个明显问题：

> 审稿人读 Contributions 时以为论文的创新只有 “early plan generation”，但后面又看到一整节新的 BnB 和一整节 online repair，不清楚作者是否把它们视为贡献，还是仅仅附加模块。

建议明确设置第三个贡献：

> **Plan-Graph-Based Anytime Refinement and Repair**

这样整个论文结构会立刻清楚。

---

# 4. 最适合本文的 Contributions 组织方式

我建议使用三个 numbered contributions，而不是一个长段落。

## Contribution 1 — 核心架构

### On-the-Fly Automaton–Allocation Co-Construction

回答：

> 你的论文最核心的新东西是什么？

核心内容：

- task allocation 不再等待 complete NBA；
- NBA 与 plan graph 同步构造；
- 每个新 transition 立即进入 feasibility/allocation evaluation；
- accepting prefix–suffix 一出现即可得到 first feasible plan。

这一项应当放在最前面，并且篇幅最大。

---

## Contribution 2 — 为什么这个架构既快又不只是“早一点开始”

### Planning-Aware Automaton Reduction and Score-Guided Expansion

回答：

> joint construction 以后，如何避免大量无效结构，并避免 first feasible plan 质量过差？

包括两个互补机制：

**前端 reduction：**

- GBA candidate transition 的 robot-team feasibility screening；
- progress-consistent decomposable-transition pruning；
- 减少 infeasible/unnecessary synchronization 向 NBA 传播。

**搜索顺序：**

- residual-obligation score；
- partial-plan cost + unavoidable remaining burden；
- promising automaton–allocation branches earlier。

把这两个机制放在一个 contribution 中的原因是：它们都服务于同一个目标——

> **让 on-the-fly joint construction 更高效，并使早期得到的方案更有质量。**

---

## Contribution 3 — 同一 plan graph 如何支持首解之后的工作

### Plan-Graph-Based Anytime Refinement and Online Repair

回答：

> first feasible plan 得到以后，论文还做了什么？

核心内容：

- retained plan graph 不被丢弃；
- construction 得到的 best plan warm-starts BnB；
- BnB 在 plan graph 上继续联合优化 path/assignment；
- robot unavailable 时，以最新 confirmed task progress 为新 root；
- 在剩余 team 上 re-optimize unfinished assignments。

这一项可以把你的论文从“fast first-plan generator”提升为：

> **一个从 first feasibility → refinement → execution-time repair 共用同一规划结构的完整框架。**

这是一个很值得强调的系统级创新点。

---

# 5. 最推荐的 Contributions 完整替换稿

下面这一版最适合你现在整篇论文的 Introduction、Related Work、System Overview 和后续各方法章节。

建议把当前 `B. Contributions` 下从

> `We propose a new on-the-fly approach...`

到

> `...during score-guided NBA construction.`

全部替换。

```latex
\subsection{Contributions}

The main contributions of this work are as follows:

1) \emph{On-the-Fly Automaton--Allocation Co-Construction:}
We develop an LTL-MRTA framework that moves robot task allocation into the GBA-to-NBA translation process rather than waiting for the complete NBA. The NBA and a plan graph are constructed synchronously, and each newly generated NBA transition induces a subtask that is immediately evaluated using the robot assignments and predicted execution states stored in the current plan nodes. As a result, a feasible plan can be extracted as soon as an accepting prefix--suffix structure is reached, eliminating the requirement that task allocation wait for complete NBA construction.

2) \emph{Planning-Aware Automaton Reduction and Score-Guided Expansion:}
We introduce planning-aware reduction at the GBA level to prevent unhelpful task structure from propagating to downstream planning. Candidate transitions that cannot be realized by the available robot team are removed during GBA construction, while progress-consistent decomposable transitions are pruned before GBA-to-NBA degeneralization to avoid unnecessary synchronization. We further introduce a residual-obligation score that combines the cost of a partial plan with an estimate of the unavoidable remaining task burden, thereby prioritizing promising automaton--allocation branches. Together, these mechanisms reduce automaton-construction effort and improve the quality of the first feasible plan while preserving early plan generation.

3) \emph{Plan-Graph-Based Anytime Refinement and Online Repair:}
The synchronously constructed plan graph is retained as a reusable planning structure after the first feasible plan is found. Its best feasible plan provides a warm start for a branch-and-bound optimizer that further improves the makespan over the generated plan graph. When robots become unavailable during execution, the same graph is re-rooted according to the confirmed task progress and the unfinished assignments are re-optimized over the remaining team, enabling rapid repair without reconstructing the temporal planning structure from scratch.

Under the stated assumptions, we establish soundness and completeness of the proposed framework. Extensive numerical studies, ablation experiments, scalability comparisons, and physical-robot experiments validate the contributions to first-plan latency, solution quality, scalability, and online repair.
```

---

# 6. 为什么这一版比当前版本更能突出创新

## 6.1 第一眼就能看到三层创新

审稿人快速扫 Contributions 时会直接得到：

> **1. 改变 pipeline**  
> **2. 改变 automaton generation / expansion 的 planning-awareness**  
> **3. 用统一 plan graph 支持 optimization + repair**

而不是看到一整段关于 NBA、plan graph、score 的连续过程。

---

## 6.2 与 Introduction 的问题成因完全对应

你的 Introduction 已经明确提出两个 first-plan latency 成因：

### 成因 A

automaton construction 与 allocation 串行。

对应：

> **Contribution 1: On-the-Fly Automaton–Allocation Co-Construction**

### 成因 B

automaton generation 不使用 robot-team/planning information，因此无效结构仍可能生成和传播。

对应：

> **Contribution 2: Planning-Aware Automaton Reduction**

此外，单纯“尽早得到可行解”可能导致方案质量较差。

对应：

> **Contribution 2: residual-obligation score**

最后，实际机器人执行需要：

- 有时间就继续改进；
- robot unavailable 后快速 repair。

对应：

> **Contribution 3: reusable plan graph + BnB + repair**

因此 Introduction 提的问题和 Contributions 给出的答案是一一对应的。

---

# 7. 推荐保留和删除的当前句子

## 建议保留核心思想

当前：

> We propose a new on-the-fly approach to LTL-MRTA that performs task allocation as the NBA is generated.

建议保留其思想，但升级为 contribution title：

> **On-the-Fly Automaton--Allocation Co-Construction**

---

## 建议删除重复句

以下几句不建议在 Contributions 中继续分别出现：

> This graph grows synchronously with the NBA.

> The NBA and the plan graph are constructed together.

> Thus, the same ordering also guides the exploration of task-allocation branches.

原因：这些都是同一件事的不同表述，可以压缩到一个完整的机制句里。

---

## 建议从 Contributions 移到 Method section

> our method performs task allocation incrementally using a greedy procedure

Contribution 中不需要强调 greedy。

---

## 建议改写

当前：

> One innovation of our approach is that the GBA is pruned before NBA construction begins.

建议：

> We introduce planning-aware reduction at the GBA level to prevent unhelpful task structure from propagating to downstream planning.

后者先讲**作用与设计思想**，再说具体 pruning，更像 contribution。

---

## 建议改写

当前：

> Another distinctive aspect is that a residual-obligation score guides both the NBA and the plan graph as they are constructed.

建议：

> We further introduce a residual-obligation score that combines the cost of a partial plan with an estimate of the unavoidable remaining task burden, thereby prioritizing promising automaton--allocation branches.

这样 score 不是“another aspect”，而是一个明确技术创新。

---

# 8. 关于 “To the best of our knowledge” 的建议

当前最后一句：

> To the best of our knowledge, this is the first LTL-MRTA framework to perform task allocation during score-guided NBA construction.

这个 claim 可以保留，但我不建议再把它作为 Contributions 的收尾核心句。

原因是你的真正说服力应该来自：

> **serial pipeline 导致 first-plan latency → joint construction 直接针对这个瓶颈**

而不是：

> **以前没人这么做 → 我是第一个。**

如果你已经做过充分文献检索，确实希望保留 priority claim，建议缩窄并放在第一项贡献末尾，例如：

```latex
To the best of our knowledge, this is the first LTL-MRTA framework in which robot task allocation is performed during NBA generation rather than after the complete automaton has been constructed.
```

我不建议把 `score-guided` 放进 “first” claim，因为：

1. 它把核心创新限定得过细；
2. 审稿人更可能针对“score-guided”寻找局部相似工作；
3. 真正有意义的架构差异是 **allocation during NBA generation**。

如果没有必要争取“first”表述，直接删掉会更稳，创新仍然非常清楚。

---

# 9. 一个更精简的版本

如果版面比较紧，可以采用下面这一版。它保留三项贡献，但每项控制在 2 句左右。

```latex
\subsection{Contributions}

The main contributions of this work are as follows:

1) \emph{On-the-Fly Automaton--Allocation Co-Construction:}
We integrate robot task allocation into GBA-to-NBA translation by constructing the NBA and a plan graph synchronously. Newly generated NBA transitions are immediately evaluated through robot assignment, allowing a feasible prefix--suffix plan to be returned before the complete NBA is available.

2) \emph{Planning-Aware Reduction and Search Guidance:}
We prune robot-team-infeasible and progress-consistent decomposable transitions at the GBA level so that infeasible or unnecessarily synchronized task structure is not propagated to the NBA. A residual-obligation score further prioritizes promising automaton--allocation branches according to partial-plan cost and remaining task burden, improving first-plan quality while retaining rapid plan generation.

3) \emph{Plan-Graph-Based Refinement and Repair:}
The retained plan graph supports continued branch-and-bound optimization after the first feasible plan is found and is reused for task repair when robots become unavailable. This provides a common planning structure for early feasibility, subsequent makespan improvement, and rapid reassignment of unfinished tasks.

We establish soundness and completeness under the stated assumptions and validate the framework through numerical and physical experiments.
```

### 我的推荐

正文允许的情况下，优先使用第 5 节的**完整版**。

完整版更清楚地解释了：

- 为什么 GBA pruning 是 innovation；
- 为什么 score 与 joint construction 是一体的；
- 为什么 retained plan graph 不是临时数据结构，而是支撑 refinement 和 repair 的统一表示。

---

# 10. 不建议把 Contributions 写成四五个很碎的小点

你的方法虽然包含：

- infeasible-transition pruning；
- decomposable-transition pruning；
- greedy assignment；
- plan graph；
- residual score；
- BnB lower bound；
- rollout upper bound；
- online repair；

但这些不应该全部独立列成 contributions。

否则审稿人会看到“8 个小技巧”，而不是一个具有明确设计思想的框架。

最适合本文的 abstraction level 是：

> **架构创新**  
> + **支撑该架构的 planning-aware reduction / guidance**  
> + **共享结构带来的 refinement / repair**

这也是两篇模板共同体现出的优点：**贡献列表描述研究层面的新能力和新机制，而不是复述算法目录。**

---

# 11. Contributions 与论文后文章节的映射

采用推荐版本后，论文结构非常自然：

| Contribution | 对应章节 | 核心作用 |
|---|---|---|
| On-the-Fly Automaton–Allocation Co-Construction | Sec. VI | 降低 first feasible plan latency |
| Planning-Aware Automaton Reduction and Score-Guided Expansion | Sec. V + Sec. VI-B3 | 减少无效结构 + 提升 first-plan quality |
| Plan-Graph-Based Anytime Refinement and Online Repair | Sec. VII + Sec. VIII | continued optimization + failure repair |
| Theory / validation（收束句） | Sec. IX–XII | complexity, guarantees, numerical/physical validation |

这一映射比当前 Contributions 和后文的对应关系清晰很多。

---

# 12. 最终建议

我最建议的写法不是“照模板把 Contributions 变成三个 bullet”，而是借鉴模板背后的原则：

### 从模板一借鉴

> **每一个 contribution 有清楚的概念名称，并回答一个独立研究问题。**

### 从模板二借鉴

> **Contribution 保持在方法/能力层面，不把 Method section 的细节全部提前展开。**

结合你的论文，最适合的三项就是：

1. **On-the-Fly Automaton--Allocation Co-Construction**
2. **Planning-Aware Automaton Reduction and Score-Guided Expansion**
3. **Plan-Graph-Based Anytime Refinement and Online Repair**

这三项之间的关系不是简单并列，而是：

> **新的 pipeline architecture**  
> → **让该 architecture 高效且保证 early-solution quality 的机制**  
> → **利用同一结构继续 optimization 和 repair**

这会比当前“一段式流水账”更容易让审稿人快速理解本文真正的技术贡献。
