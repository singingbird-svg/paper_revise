# Related Work 末尾总结修改方案

## 1. 修改目标

我仔细对照了当前稿件中 **Related Work 之前的 Introduction**、当前 **Related Work 的四个主体段落**，以及紧随其后的 **Contributions**。目前真正需要解决的不是“总结得不够多”，而是 **Related Work 最后一段的因果链还没有和 Introduction 中已经建立好的动机完全对齐**。

当前总结为：

> Overall, while existing top-down methods have advanced LTL-MRTA from different perspectives, they still struggle to simultaneously provide a rapid first feasible plan, effective subsequent optimization, and efficient plan repair in large-scale problems. This limitation is particularly evident when substantial preprocessing is required before task allocation can begin. The proposed framework addresses this gap by incorporating planning information during automaton construction.

这段的主要问题有三个：

1. **“rapid first feasible plan + subsequent optimization + plan repair” 是一个过宽的三项能力列表。**  
   前面的 Related Work 并没有证明“现有方法普遍同时缺少这三项能力”。特别是 poset-based methods 已经明确支持 early feasible solution + subsequent improvement，一些方法也具有在线适应能力。因此，这样写容易让审稿人把注意力放到“是否存在反例”上，而不是你的核心创新上。

2. **第二句和第一句的因果关系不完全一致。**  
   `substantial preprocessing before task allocation` 直接导致的是 **first-solution latency**，但它并不能直接解释为什么现有方法缺少“subsequent optimization”或“plan repair”。因此现在的逻辑是：

   > 三个问题 → preprocessing

   但实际上更准确的是：

   > first-plan latency → serial front-end processing + planning-unaware automaton generation.

3. **最后一句对你的创新描述过于抽象。**  
   `incorporating planning information during automaton construction` 是正确的，但没有把 Introduction 中已经讲清楚的两个关键原因—机制对应关系再次收束出来：

   - 前端生成过程中缺少当前 robot-team feasibility / planning information  
     → 无效或不必要同步的结构会继续向后传播  
     → **GBA-level early pruning**
   - automaton construction 与 allocation 串行  
     → allocation 必须等待前端结构生成  
     → **NBA generation 与 plan-graph construction 同步进行，并立即评估新生成 transition 的 robot assignment**

   residual-obligation score 则进一步回答：

   - 既然要尽早得到 first feasible plan，不能只“更早开始搜索”，还需要让更有希望的联合 automaton–allocation branches 更早被探索。

因此，Related Work 的结尾应当从“能力清单式 gap”改成：

> **现有工作从不同阶段降低计算负担 → 对本文所研究的 automata-based LTL-MRTA，first executable plan 的一个关键延迟来源仍然是 translation/allocation 的串行组织以及 automaton generation 对 planning information 的缺失 → 这种机制会导致无效结构传播、allocation 不能及时利用已经出现的 temporal progress → 因此要降低 first-plan latency，需要把 pruning 和 allocation 前移到 automaton generation 本身 → 本文的 GBA pruning + synchronous NBA/plan-graph construction + score-guided exploration 正好针对这一成因。**

这样形成的是“**问题成因 → 方法设计**”的逻辑，而不是“别人没有这样做 → 所以我这样做”。

---

# 2. 当前 Related Work 实际已经总结出了哪些方向

你现在的 Related Work 主体已经覆盖了四类重要路线：

### 2.1 经典 top-down automata-based planning

包括：

- product automaton；
- sampling-based approximation；
- STAP / decomposition；
- MILP。

这些方法主要从 **product-space size、task decomposition、allocation/optimization formulation** 等角度降低计算负担。

### 2.2 强调快速 first feasible solution 的方法

包括：

- planning-decision-tree-based methods；
- poset-based anytime methods。

这一类和你的工作最接近，因为它们已经认识到：

> 与其等待完整最优解，不如尽快得到一个 feasible plan，再继续改进。

因此不能把 gap 写成“现有工作没有快速 first feasible solution 或没有 anytime optimization”。

真正应该进一步追问的是：

> **在 first feasible solution 成为目标之后，first solution 之前还有哪些计算处于 critical path？**

这正好与 Introduction 中的 front-end processing 形成呼应。

### 2.3 通过 specification structure 降低复杂度的方法

包括：

- hierarchical temporal logic；
- conjunctive / decomposable structures；
- related decomposition approaches。

这类方法通过改变或利用 specification structure 降低问题难度，但引入了相应的 specification/decomposition assumptions。

### 2.4 learning-based 方法

这类方法通过学习 task-conditioned representations/policies，把一部分 temporal reasoning 的计算摊销到训练阶段，从而获得快速 deployment-time inference。

它们不应该被强行纳入“automaton construction → task allocation 的串行瓶颈”中，因为它们本来就是不同 computational paradigm。

因此总结时应先承认：

> existing work attacks computational burden at different stages and under different assumptions.

然后再缩小范围：

> **For the automata-based LTL-MRTA setting considered here...**

这样逻辑最严谨，也不会对 learning/HLTL 做过度概括。

---

# 3. 最推荐的总结逻辑

建议 Related Work 最后一段采用如下六步：

### Step 1：真正总结已有工作

先承认已有方法从不同阶段减少计算负担，而不是直接说它们“仍然不行”。

### Step 2：缩小到本文问题设置

明确：

> For the automata-based LTL-MRTA setting considered here...

避免把 learning-based / structured-specification methods 强行套进你的瓶颈。

### Step 3：指出核心问题

不要说：

> nobody has performed allocation during automaton generation.

而要说：

> first-solution latency is partly caused by the serial organization of temporal-logic translation and robot allocation.

这是**问题成因**。

### Step 4：进一步解释为什么这个串行结构会造成额外负担

因为 automaton generation 阶段没有充分利用当前 robot team 和 planning information：

- team-infeasible transitions 可能先被生成；
- avoidable synchronization 可能继续传播；
- 已经生成的 feasible temporal progress 不能立即转化成 robot assignment / executable partial plan。

这是你 GBA pruning 和 joint construction 的直接动机。

### Step 5：从原因推出设计原则

用一句非常重要的话：

> reducing the time to the first executable plan requires not only accelerating downstream search, but also reducing unhelpful automaton structure early and exploiting newly generated task progress immediately.

这句话是整个总结的核心。

它表达的是：

> **因为问题来自前端结构生成和串行等待，所以解决方案必须进入前端，而不是因为“过去没人进入前端”。**

### Step 6：简洁对应本文方法

只需要收束到：

- GBA-level pruning；
- synchronous NBA / plan-graph construction；
- residual-obligation score；
- early first plan；
- retained plan graph → refinement + repair。

注意最后的 optimization 和 repair 应该作为 **同一 retained plan graph 带来的后续收益**，而不是作为“现有方法共同缺失的 gap”。

---

# 4. 最推荐的英文替换稿

建议用下面这一段直接替换当前 Related Work 最后的：

> `Overall, while existing top-down methods...`

到 `B. Contributions` 之前的全部总结。

```latex
Overall, existing top-down approaches reduce the computational burden of LTL-MRTA at different stages. Product-space, decomposition, and optimization methods primarily reduce the cost of downstream planning and allocation; planning-decision-tree methods emphasize rapid feasible-plan generation, while poset-based methods further support continued solution improvement; structured-specification and learning-based approaches reduce online complexity under additional formulation or training assumptions. For the automata-based LTL-MRTA setting considered here, however, a key source of first-solution latency remains the serial organization of temporal-logic translation and robot allocation. When automaton generation proceeds without exploiting robot-team feasibility and planning information, transitions that are infeasible for the current team or impose avoidable synchronization may be generated and propagated to later stages, while task allocation cannot immediately exploit feasible temporal progress as it becomes available. Thus, reducing the time to the first executable plan requires not only accelerating downstream search, but also eliminating unhelpful automaton structure early and using newly generated task progress for allocation without waiting for the complete automaton. Following this principle, our framework performs planning-aware pruning at the GBA level and constructs the NBA and plan graph synchronously, with newly generated transitions evaluated through robot assignment and promising branches prioritized by a residual-obligation score. Consequently, a feasible prefix--suffix plan can be returned before the complete NBA is available, while the retained plan graph provides a common search structure for subsequent branch-and-bound refinement and rapid repair when robots become unavailable.
```

---

# 5. 为什么这一版和 Introduction 的创新点是一致的

你当前 Introduction 已经建立了非常清楚的核心诊断：

> `A remaining source of latency ... lies in the front-end processing that must be completed before robot assignment can begin.`

并进一步指出：

> automaton construction 与 task allocation 串行；

以及：

> robot-team feasibility / workspace information 通常没有进入 automaton construction，因此 redundant or infeasible structures 可能先被生成和处理。

推荐版 Related Work 总结没有重新发明一套 gap，而是把 Related Work 中各种方法总结后，重新落回这两个根因。

对应关系如下。

| Introduction 中的原因 | Related Work 总结中的表述 | 本文对应机制 |
|---|---|---|
| translation 和 allocation 串行 | `serial organization of temporal-logic translation and robot allocation` | synchronous NBA / plan-graph construction |
| front-end processing 位于 first-plan critical path | `a key source of first-solution latency` | accepting prefix–suffix 出现即可返回方案 |
| automaton generation 缺少 robot-team/planning information | `without exploiting robot-team feasibility and planning information` | planning-aware generation |
| infeasible structure 被生成并传播 | `infeasible for the current team ... generated and propagated` | GBA infeasible-transition pruning |
| independent tasks 被不必要同步 | `impose avoidable synchronization` | progress-consistent decomposable-transition pruning |
| 仅提前搜索不保证 first-plan quality | `promising branches prioritized by a residual-obligation score` | score-guided joint expansion |
| first plan 后仍需改进 | retained plan graph | warm-started BnB |
| team composition 改变后需快速 repair | retained plan graph | re-root / BnB re-optimization |

这样 Introduction、Related Work 总结、Contributions 三部分讲的是**同一条逻辑线**，只是功能不同：

- **Introduction**：提出问题和成因；
- **Related Work**：证明这些成因放在已有研究脉络中是合理而有意义的；
- **Contributions**：具体说明你的技术机制。

---

# 6. 这版刻意避免了“别人没做，所以我做”的逻辑

最需要保留的是下面这组逻辑：

> `a key source of first-solution latency remains the serial organization ...`

↓

> `When automaton generation proceeds without exploiting ...`

↓

> `... infeasible ... or avoidable synchronization may be generated and propagated ...`

↓

> `Thus, reducing the time ... requires not only accelerating downstream search, but also ...`

↓

> `Following this principle, our framework ...`

这里的方法是由**瓶颈的机制**推出来的。

它没有说：

> Existing work does not perform allocation during automaton generation. Therefore, we perform allocation during automaton generation.

两种写法的审稿效果差异很大。

前者表达：

> **我发现 first-plan latency 的一部分是由 pipeline organization 导致的，所以我重组 pipeline。**

后者表达：

> **我发现一个没人做过的操作，所以把它当创新。**

你的工作显然应该采用前一种论证。

---

# 7. 为什么不建议继续使用当前的“三项能力”总结

当前：

> `they still struggle to simultaneously provide a rapid first feasible plan, effective subsequent optimization, and efficient plan repair`

我建议删除。

原因不是这句话一定“错误”，而是从论文论证角度它不够稳。

### 第一，容易产生反例争论

审稿人可以分别问：

- poset-based method 不是已经 first feasible + anytime improvement 了吗？
- 某些 reactive/replanning 方法不是已经支持 repair 了吗？
- learning-based 方法为什么要按这三个指标比较？

这会把讨论带偏。

### 第二，它不能解释为什么你的技术设计是必要的

即便接受“三项能力还不能同时达到”，也不能自然推出：

> 为什么必须在 GBA pruning？
>
> 为什么必须 synchronous NBA-plan graph？
>
> 为什么必须 residual-obligation score？

而“serial front-end + planning-unaware generation”可以直接推出这些设计。

### 第三，它弱化了你真正最独特的创新

你的核心不是简单把三个功能装进一个系统，而是：

> **改变 temporal-logic translation 与 task allocation 的耦合方式，使 planning information 在 automaton 尚未完整生成时就进入结构生成和搜索过程。**

BnB optimization 和 online repair 是这一 shared plan graph 架构继续发挥作用的结果。

---

# 8. 对推荐段落的逐句作用说明

### Sentence 1

> `Overall, existing top-down approaches reduce the computational burden of LTL-MRTA at different stages.`

作用：公平总结。

不要开头就说 existing work “fails”。

### Sentence 2

> `Product-space ... planning-decision-tree ... poset-based ... structured-specification and learning-based ...`

作用：真正覆盖 Related Work 前面讲过的四类方法，让这段确实承担“summary”的功能。

### Sentence 3

> `For the automata-based LTL-MRTA setting considered here, however, a key source of first-solution latency remains the serial organization ...`

这是核心 gap，但它是一个 **causal bottleneck**，不是 novelty claim。

建议保留 `a key source`，而不是 `the key source`，避免过度声称。

### Sentence 4

> `When automaton generation proceeds without exploiting ...`

这是最关键的“为什么”。

它和 Introduction 中的：

> `since robot-team feasibility and workspace information are typically not incorporated during automaton construction...`

直接对齐。

### Sentence 5

> `Thus, reducing the time ... requires not only accelerating downstream search, but also ...`

这是整个逻辑中最重要的桥梁句。

建议不要删。

它让 GBA pruning 和 on-the-fly allocation 显得是从问题机制自然推导出来的，而不是人为寻找 novelty。

### Sentence 6

> `Following this principle, our framework ...`

这里开始说本文，但只说 central mechanisms，不展开 algorithm 流程。

### Sentence 7

> `Consequently ... while the retained plan graph ...`

把三层收益摆清楚：

1. early first feasible plan；
2. subsequent refinement；
3. repair。

但是它们在这里是**方法带来的结果**，而不是“所有 existing work 都不具备的三个缺口”。

---

# 9. 一个更短的备选版本

如果你觉得推荐版作为 Related Work 结尾稍长，可以压缩成下面这一版。

```latex
Overall, existing top-down approaches reduce the computational burden of LTL-MRTA through product-space approximation, task decomposition and optimization, incremental allocation, structured specifications, or learned policies. For the automata-based setting considered here, however, a key source of first-solution latency is the serial organization of temporal-logic translation and robot allocation. Because automaton generation does not directly exploit robot-team feasibility and planning information, infeasible or unnecessarily synchronized transitions may be propagated to downstream planning, while allocation cannot immediately use feasible task progress as it emerges. This suggests that reducing first-plan latency requires moving part of the planning process upstream rather than only accelerating the search performed after temporal preprocessing. Accordingly, our framework prunes unhelpful transitions at the GBA level and couples NBA generation with score-guided plan-graph construction, allowing feasible assignments to be evaluated as new transitions are generated. An executable plan can therefore be returned once an accepting prefix--suffix structure is reached, and the retained plan graph is subsequently reused for solution refinement and repair under robot unavailability.
```

## 推荐意见

如果版面允许，我更推荐前面的**完整版**。

原因是完整版第一、二句对已有 Related Work 的总结更充分，特别是能够明确区分：

- downstream planning / allocation；
- rapid first feasible solution；
- anytime refinement；
- structured specifications；
- learning-based alternatives。

因此审稿人更容易看到你确实是在“总结整个 Related Work 后定位本文”，而不是只在最后再次重复 Introduction。

---

# 10. 与 Contributions 的衔接建议

当前下一节第一句是：

> `We propose a new on-the-fly approach to LTL-MRTA that performs task allocation as the NBA is generated.`

如果采用推荐的 Related Work 总结，这句可以保留。

因为两部分的功能不同：

Related Work 最后一句回答：

> **为什么这种设计能对应前述 bottleneck，以及整体上带来什么结果？**

Contributions 则回答：

> **具体有哪些技术贡献？**

因此不会构成严重重复。

不过 Contributions 中建议继续把重点放在技术层面：

1. joint NBA / plan-graph construction；
2. GBA-level pruning；
3. residual-obligation score；
4. BnB / repair。

而不要再用大量篇幅重新证明“serial pipeline 是问题”，因为这件事已经在 Introduction 和 Related Work 完成。

---

# 11. 最终推荐

我建议最终直接替换为第 4 节的完整版。

最重要的不是其中某一个单词，而是保持下面这条完整推导：

> **existing work reduces burden at different stages**  
> → **for automata-based LTL-MRTA, first-plan latency still contains a serial front-end component**  
> → **this component is costly because planning/team feasibility is not used while automaton structure is being generated**  
> → **therefore unhelpful structure propagates and feasible temporal progress cannot immediately trigger allocation**  
> → **so the solution should couple planning with automaton generation**  
> → **GBA early pruning + synchronous NBA/plan graph + score-guided exploration**  
> → **early first plan**  
> → **the retained graph naturally supports later optimization and repair**.

这条逻辑与当前 Introduction 中已经建立的创新主线是一致的，而且避免了“因为别人没这样做，所以我这样做”的 novelty-by-absence 论证。
