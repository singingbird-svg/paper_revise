# Introduction 中“结构化公式与学习方法”段落的取舍与最佳修改方案

## 0. 结论先行

**这段内容没有必要以当前的五句、独立段落形式放在 `Related Work` 之前，也不应被如此突出。**

最稳妥的处理是：

- 将其压缩为 **1–2 句“研究边界/方法定位”**，只说明结构化规格与学习方法是在不同假设下减轻计算负担的互补方向；
- 随即把论证拉回本文真正解决的问题：**automaton generation 与 task allocation 的串行组织，使完整的前端处理位于首次可执行方案的关键路径上**；
- 层次化规格的详细优缺点留在 `Related Work`；
- 学习方法若在后文没有系统讨论、没有实验比较，也可以从 Introduction 中完全删除。若希望表明作者并未忽略该方向，则保留一句“orthogonal/complementary”定位即可。

审稿人熟悉这些方法时，他最需要的不是再读一遍方法简介，而是迅速确认三件事：

1. 本文针对的到底是哪一个尚未解决的瓶颈；
2. 层次化或学习方法与本文是直接竞争、替代关系，还是不同假设下的互补关系；
3. 本文提出的每个机制是否由前述瓶颈自然推导出来。

当前段落对第 2 点讲得过多，却削弱了第 1 和第 3 点。

---

## 1. 为什么当前段落不适合继续突出

当前文字是：

> Existing studies have made several efforts to reduce this burden. Some reformulate the LTL specification to expose more exploitable task structures, such as hierarchical temporal-logic formulations. While effective, such methods rely on structured task specifications and may require additional decomposition effort. Other studies seek to avoid explicit automaton construction at deployment through learning-based approaches. Although these methods can enable rapid decision-making once trained, they typically require representative training data covering relevant task and environment conditions. These approaches reduce the computational burden from different perspectives, but each introduces its own requirements on task formulation or training.

### 1.1 “this burden”所指不够精确

上一段同时提到了：

- LTL-to-automaton translation 的时间；
- downstream task allocation/planning 的时间；
- complex specification 导致的规模增长；
- first feasible plan 的延迟。

因此，`this burden` 并不清楚究竟指“自动机构造成本”“完整规划成本”还是“首次方案前的串行延迟”。层次化规格与学习方法实际上分别改变了规格组织方式或把部分计算摊销到训练阶段，它们并不直接对应同一个、定义清楚的瓶颈。

### 1.2 两类方法并不能构成本文问题的自然分类

层次化规格与学习型策略不是 LTL-MRTA 计算减负方法的两个主要或穷尽性类别。审稿人很容易继续问：

- sampling-based methods 呢？
- MILP-based methods 呢？
- planning-decision-tree methods 呢？
- poset extraction 和 task decomposition 呢？

一旦 Introduction 采用“已有工作主要有两类”的语气，就会无意中制造分类不完整的问题。本文的 `Related Work` 已经系统讨论了 product automaton、sampling、decomposition、MILP、decision tree、poset 和 hierarchical specifications，因此没有必要在前面再选取两个并非最接近的方向加以突出。

### 1.3 学习方法不是本文最直接的比较对象

本文研究的是具有显式全局 LTL 规格、异构机器人类型/数量约束、任务分配、形式化可行性与在线修复的 model-based LTL-MRTA。所引学习工作主要用于说明“训练后可以快速执行”这一不同范式，但它并不是本文实验中的直接基线，也不是本文理论分析所覆盖的同一问题设置。

若在核心动机段中给它较大篇幅，反而会引出额外疑问：

- 为什么没有学习基线？
- 两类方法的形式化保证是否可比？
- 训练成本是否被公平计入？
- 学习策略是否真的解决了异构团队分配，而不仅是 LTL-conditioned control？

这些问题都不是本文希望在 Introduction 中打开的讨论支线。

### 1.4 现有限制并不能直接推出本文方法

当前逻辑近似为：

> hierarchical methods 需要结构化规格；learning methods 需要训练数据；所以我们把 task allocation 放进 automaton generation。

这个“所以”并不充分。真正能够直接推出本文方法的是：

> automaton generation 与 task allocation 被串行处理；前者不了解当前团队可行性和部分分配状态；因此无执行价值或不必要同步的结构仍可能传播，且分配必须等待前端处理完成。

这条因果链才能自然推出：

- GBA-level team-feasibility pruning；
- progress-consistent decomposable-transition pruning；
- synchronous NBA/plan-graph construction；
- residual-obligation ordering；
- first-plan early return；
- retained graph for refinement and repair。

### 1.5 当前写法与论文的实验证据不完全对齐

本文最直接的消融实验比较的是：

- **Case I**：保留 GBA pruning，但等待完整 NBA 后才构造 plan graph；
- **Case II**：先生成完整 NBA，再进行 pruning 与 plan-graph construction。

Table I 和 Table II 分别直接证明：

- task allocation 与 NBA generation 同步进行，可缩短 `T_first`；
- GBA-level pruning 可避免大量无须进入 NBA 的 transitions，并进一步缩短 `T_first`。

论文的主要外部比较也是 poset- 和 MILP-based methods，而不是 learning-based control。因此，Introduction 最强的证据闭环应当是：

> **串行前端瓶颈 → 团队信息前移与同步构造 → 消融验证首次方案时间下降。**

而不是：

> **hierarchical/learning 各有要求 → 本文提出第三条路线。**

后者会弱化论文真正有辨识度的创新。

---

## 2. 两篇参考论文给出的写作启示

| 论文 | 是否有独立 Related Work | Introduction 中前置文献的作用 | 对本文的启示 |
|---|---:|---|---|
| *An Exploration-Enhanced Search Algorithm for Robot Indoor Source Searching* | 否 | 在 Introduction 中直接回顾 biomimetic 与 probability-based 方法，并指出它们共同依赖的场景假设，因为后文没有独立文献综述 | 该文必须把较多相关工作放在 Introduction；不应机械照搬到已有独立 `Related Work` 的本文 |
| *From Ambiguous Language to Verifiable Plans* | 是 | 只在 Introduction 中保留一个高层范式对比：hard-coded mappings 与 LLM/VLM methods 共享 fixed symbolic interface 的核心限制；随后由此推导三个 design requirements | 前置文献只有在它构成“方法必要性”的逻辑前提时才值得展开；细节仍放在 Related Work |
| 本文 | 是 | 当前提前介绍 hierarchical 与 learning 两个互补方向，但二者并不共享一个直接导向 on-the-fly allocation 的共同瓶颈 | 应压缩为边界说明，把篇幅让给“serial pipeline + team-agnostic translation”这一真正的共同瓶颈 |

### 2.1 第二篇参考论文为何可以在 Introduction 中写较多现有方法

该文没有单独的 `Related Work`。它在第 2 页先提出三个具体场景挑战，然后回顾 biomimetic 与 probability-based 方法，并反复指出这些方法依赖“机器人初始位置在源的下风向”“源位于气流中”“环境较简单”等假设。现有方法的限制与其新算法的三个组成部分一一对应，因此详细回顾是论证链的一部分，而不是重复综述。

### 2.2 第三篇参考论文真正值得借鉴的地方

该文虽然也在 `Related Work` 前提到 symbolic 与 learning-based 两个范式，但它不是为了展示文献覆盖面，而是为了建立一个共同瓶颈：**二者都受 fixed symbolic interface 限制**。随后，论文直接从该瓶颈推出 scene-conditioned symbolic interface、functional substitution 和 monitor-guided recovery 三个要求。

本文应借鉴的是这种“共同瓶颈 → 设计要求 → 方法机制”的推导方式，而不是形式上也放置“两类方法及其缺点”。

---

## 3. 推荐的 Introduction 逻辑顺序

在 `A. Related Work` 之前，建议形成以下连续链条：

### 第 1 段：应用与问题定义

保留当前 warehouse example、temporal dependency、collaboration 和 LTL-MRTA 定义。

### 第 2 段：实际需求

强调大规模问题中 first feasible plan 的时间重要，并说明获得方案后仍需继续优化；机器人不可用时还需要快速修复。重规划在这里是重要应用需求，但不应取代“首次方案延迟”成为主线。

### 第 3 段：精确诊断瓶颈

不要写 `Most existing LTL-MRTA methods...`，改为更稳妥的：

> `A common automata-based LTL-MRTA pipeline ...`

核心应当是：

- automaton/specification processing 与 allocation 串行；
- 完整前端处理位于 first executable plan 的 critical path；
- translation/generation 阶段不了解当前团队类型、数量和部分执行状态；
- team-infeasible 或 unnecessary-synchronization structures 会继续向后传播。

### 第 4 段：只用一句界定互补方向，然后提出研究问题

层次化规格和学习方法只需承担“作者知道这些方向，但本文针对不同瓶颈”的作用。不要再分别解释两三句缺点。

### 第 5 段：用 central idea 统领方法

不要按算法执行顺序流水账式枚举，而要体现三个因果对应：

1. **在结构传播前消除无用部分**：GBA-level pruning；
2. **在 automaton 出现 task progress 时立即做 allocation**：joint NBA/plan-graph construction + score-guided exploration；
3. **复用同一搜索结构完成后续优化与故障修复**：warm-started BnB + graph reuse/re-rooting。

---

## 4. 最推荐的英文替换稿

下面这版建议替换从当前

> `Recent studies have recognized ...`

开始，到 `A. Related Work` 之前的全部内容。`liu2024time` 请核对并替换为你文中 Ref. [3] 的实际 BibTeX key（若不同）。

```latex
Recent work has emphasized the value of anytime planning, in which a feasible plan is returned early and subsequently improved, as exemplified by poset-based methods~\cite{liu2024time}. A remaining source of latency, however, lies in the front-end processing that must be completed before robot assignment can begin. In a common automata-based LTL-MRTA pipeline, the LTL specification is first translated into a task automaton and, when needed, additional task structures are extracted before allocation and scheduling are performed. This serial organization places specification processing on the critical path to the first executable plan. Moreover, because the generation process is largely unaware of the available robot types and cardinalities and of the evolving execution state, transitions that cannot be realized by the current team, as well as transitions that impose avoidable synchronization, may be propagated to downstream planning.

Complementary approaches exploit structured specifications or learned policies under different modeling and training assumptions~\cite{luo2024decomposition,vaezipoor2021ltl2action}. Rather than treating them as direct alternatives, this work focuses on a distinct pipeline-level question within automata-based LTL-MRTA: can robot-team feasibility and task-allocation reasoning be introduced while the automaton is being generated, so that unhelpful structure is removed early and executable assignments are explored before the complete automaton is available?

To answer this question, we propose an on-the-fly LTL-MRTA framework that couples automaton generation with task allocation. At the GBA level, the framework discards transitions that are infeasible for the available team and removes combined transitions whose synchronization can be decomposed without changing acceptance progress. During the GBA-to-NBA translation, each newly generated NBA transition is immediately interpreted as a candidate subtask, assigned to feasible robots, and recorded in a plan graph that grows synchronously with the NBA. A residual-obligation score jointly prioritizes automaton successors and allocation branches according to the current plan cost and the estimated burden of the remaining actions. Consequently, an executable prefix--suffix plan can be returned as soon as an accepting structure is reached, before the complete NBA has been constructed. The completed plan graph then warm-starts branch-and-bound refinement and is retained as a reusable search structure for rapid plan repair when robots become unavailable during execution.
```

### 这版相对当前文字的主要改进

- 用 `front-end processing` 和 `critical path` 明确“慢”具体慢在哪里；
- 用 `a common automata-based ... pipeline` 避免对所有 LTL-MRTA 方法作过强概括；
- 把 hierarchical/learning 从“两个主要替代方案”降为“不同假设下的互补方向”；
- 研究问题直接导向本文的 on-the-fly coupling；
- 方法段不再是模块列表，而是“early elimination → immediate allocation → reusable structure”的创新链；
- 在线修复被保留为同一 plan graph 带来的后续能力，而不是与主线竞争。

---

## 5. 若只想最小改动：替换原争议段即可

若暂时不希望重写前后段落，原五句可以直接压缩为以下两句：

```latex
Complementary approaches reduce computation by exploiting structured specifications or learned policies under different modeling and training assumptions~\cite{luo2024decomposition,vaezipoor2021ltl2action}. Rather than treating these approaches as direct alternatives, this work targets a distinct source of latency in automata-based LTL-MRTA: the serial separation between automaton generation and task allocation.
```

随后把下一段改为：

```latex
This observation raises a natural question: can robot-team feasibility and task-allocation reasoning be introduced while the automaton is being generated, rather than after its construction is complete? Such an integration would allow infeasible or unnecessary structure to be eliminated before it propagates and would enable feasible assignments to be explored as soon as the corresponding temporal transitions appear.
```

这是改动最小、风险最低的版本。它保留两篇文献，但不让它们喧宾夺主。

---

## 6. Related Work 中如何处理这两类方法

### 6.1 Hierarchical specifications

当前 `Related Work` 已经讨论 hierarchical temporal-logic specifications、conjunctive structure 和 poset products。建议：

- 将 `\cite{luo2024decomposition}` 合并到该段；
- 在那里详细说明其优势与适用的结构化输入；
- Introduction 中不再重复“require additional decomposition effort”这一完整论述。

### 6.2 Learning-based approaches

有两种稳妥选择。

**选择 A：删除 Introduction 中的 learning citation。**

适用于：论文后文不再讨论学习方法，且学习工作与异构团队任务分配并非直接同问题设置。这样论证最干净。

**选择 B：保留一句 scope statement。**

适用于：希望审稿人明确看到作者知道 learning-based LTL execution。写作时应强调“orthogonal”，不要把它作为本文必须击败的直接基线。例如：

```latex
Learning-based approaches provide an orthogonal means of amortizing LTL-conditioned decision making over training~\cite{vaezipoor2021ltl2action}; the present work instead considers explicit heterogeneous-team allocation with model-based temporal-logic reasoning.
```

若采用选择 B，建议把这句话放在 `Related Work` 末尾或 Introduction 的压缩定位句中，而不要恢复原来的独立长段。

---

## 7. 具体措辞层面的修改建议

### 7.1 避免过强概括

当前：

> Most existing LTL-MRTA methods first construct the automaton ...

建议：

> A common automata-based LTL-MRTA pipeline first constructs the task automaton ...

这样不会被非自动机、层次化、学习型或直接 MILP 方法反例挑战。

### 7.2 避免模糊的“another direction”

当前：

> These observations motivate us to explore another direction ...

建议直接提出问题：

> This observation raises a pipeline-level question: must automaton generation and task allocation remain serial?

或使用推荐稿中的完整问句。

### 7.3 统一“feasible”与“executable”

当你强调方案不仅逻辑可接受，而且已经包含机器人分配与可达性判断时，`first executable plan` 比 `first feasible solution` 更能突出本文区别。全文仍可保留正式符号 `first feasible plan`，但在动机段可适度使用 `executable` 解释其实际意义。

### 7.4 修正拼写

当前：

> These obervations ...

应改为：

> This observation ...

### 7.5 不要把“训练数据需求”写成核心反驳

`representative training data covering relevant task and environment conditions` 是合理的一般性描述，但若没有专门文献分析，很容易显得笼统。本文不需要依靠削弱学习方法来建立价值；只需说明问题设置与计算位置不同即可。

---

## 8. 从审稿人视角，修改后的 Introduction 应当立即回答的问题

修改后，审稿人在进入 `Related Work` 前应能清楚回答：

1. **为什么需要早期方案？**——执行不能长期等待，且故障后需要快速修复。
2. **当前延迟的具体来源是什么？**——automaton/specification processing 与 allocation 串行，完整前端处理处于 first-plan critical path。
3. **为什么必须在生成期间引入团队信息？**——否则 team-infeasible 与 unnecessary-synchronization structures 会继续传播，且 allocation 无法提前开始。
4. **本文与 hierarchical/learning 方法是什么关系？**——不同假设下的互补方向，不是本文刻意设置的两个“待击败对手”。
5. **方法为何包含这些组件？**——GBA pruning 消除早期无用结构；joint construction 早做分配；score 提升首个方案质量；retained graph 支持优化和修复。

只要这五个问题都能被顺畅回答，审稿人通常不会再对“为什么要这样做”产生结构性疑惑。

---

## 9. 最终建议

**推荐采用第 4 节的完整替换稿。**

若篇幅非常紧张，则采用第 5 节的最小改动版本。无论采用哪一版，都不建议保留当前五句独立段落。其最合理的功能是“用一句话界定互补方向”，而不是承担主要动机。本文应当把最强的叙事资源集中到：

> **把异构团队可行性与任务分配前移到 GBA/NBA 构造过程，使无执行价值的结构更早被抑制，并在完整自动机生成前得到可执行方案。**
