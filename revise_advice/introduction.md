# Introduction 修改建议：弱化机器人减少，突出主创新边界

你这个提醒非常关键：机器人减少时的动态重规划不能写成本文的主要创新点。更稳妥的 introduction 逻辑应该是：

1. 先讲静态 LTL-MRTA 本身已经很难：全局 LTL、机器人不预分配、协同任务、状态爆炸、快速得到可行解困难。
2. 再讲真实部署中静态假设会受到动态因素挑战，包括任务变化、环境变化、机器人可用性变化。
3. 综述一些 reactive/dynamic 文章，说明这个方向重要。
4. 回到本文核心：本文主要解决的是在给定 global LTL 和当前机器人团队时，如何把 planning 信息嵌入自动机构造，快速得到可行解并继续优化。
5. 最后轻描淡写地提一句：由于工程实现中可用机器人集合可以更新，本文方法也可用于机器人减少后的重新规划；但这不是本文核心贡献。

## 1. 总体写作原则

### 应该强调

- 本文核心创新是 planning-aware automaton generation。
- 本文不是提出新的动态故障恢复框架。
- 机器人减少只作为实际部署中会出现的动态扰动，用来说明为什么快速重新求解/快速得到可行解有实际价值。
- 如果提到机器人减少，建议用“engineering extension”“practical implementation”“can be rerun with updated team information”这类语气。

### 应该避免

避免把以下表述放在 contribution 或 abstract 里：

```text
We propose a dynamic replanning method for robot removal.
```

```text
The proposed method solves failure recovery under reduced robot availability.
```

```text
This work explicitly addresses robot failures as a main contribution.
```

更稳的表述是：

```text
Although dynamic team changes are not the main focus of this paper, the implemented planner can be invoked with an updated available robot set, which allows robot-removal cases to be handled as a practical replanning extension.
```

## 2. Introduction 中动态内容的正确位置

动态机器人减少不建议放在“本文方法总述”或“贡献”里作为亮点。建议放在两个位置：

1. 动机段：说明静态规划在真实部署中会遇到动态扰动。
2. Related work 末尾或方法过渡段：简短说本文实现也能在更新机器人集合后重新规划，但本文重点仍是快速求解静态 LTL-MRTA 实例。

## 3. 开头动机段建议

当前 introduction 开头可以先讲静态任务：

```text
Multi-robot systems (MRS) have been widely used in applications such as persistent surveillance, logistics, and autonomous maintenance, where multiple robots can operate concurrently and cooperatively to accomplish tasks that are beyond the capability of a single robot. In many such applications, the mission is naturally specified by temporal requirements, such as ordering, persistence, and synchronization.
```

然后补一句动态背景，但不要把机器人减少抬得太高：

```text
Although many planning methods are developed for a static mission and a fixed robot team, real deployments may deviate from this idealized setting. Environmental conditions may change, additional tasks may be requested, and some robots may become unavailable because of faults, battery depletion, or communication loss. These dynamic factors make it desirable for a planner to generate executable solutions quickly, so that replanning can be performed when the current planning instance is updated.
```

这段的重点是“静态问题需要快速求解，因此动态时也有用”，而不是“本文主要解决动态问题”。

## 4. LTL-MRTA 定义段建议

这里可以保留 LTL-MRTA 的静态定义，不要过早展开机器人减少。建议只在段末补一句轻量背景：

```text
In this paper, we focus on the LTL-MRTA problem for a given task specification and a given robot team. This static formulation is the basic computational problem that must be solved both for initial planning and whenever a practical system updates the planning instance during execution.
```

如果必须提机器人减少，可以写得更低调：

```text
For example, if the available robot set changes during execution, the planner can be called again with the updated team; the resulting problem is still an LTL-MRTA instance with modified robot availability.
```

## 5. Related Work 建议结构

建议把 related work 分成三条线，但第三条动态线只做背景，不导向本文贡献。

### 5.1 静态 top-down LTL-MRTA

这里继续讲 product automaton、sampling、MILP、PDT、partial order 等。核心 gap 是：

```text
Although these methods have improved scalability from different perspectives, obtaining an initial feasible solution can still be computationally demanding for large-scale LTL-MRTA problems, especially when the automaton or planning abstraction must be constructed before allocation begins.
```

### 5.2 动态/reactive 规划作为背景

这里引用 Chen and Kan、reactive multiconstraint framework、poset product 等文章，说明动态问题被广泛关注，但不要说本文在这方面创新。

可插入英文：

```text
Dynamic and reactive variants of temporal-logic task allocation have also been studied. Existing work has considered environmental changes, temporary task requests, task addition and removal, resource variation, and agent failures. These studies show that practical multi-robot systems often need to update their plans during execution. In this paper, however, dynamic replanning is not treated as the main algorithmic contribution. Instead, these scenarios motivate the need for a planner that can solve the current LTL-MRTA instance quickly whenever planning is invoked.
```

如果要单独提机器人减少：

```text
Robot removal can be viewed as one such practical update: the available robot set is reduced, and the planner is invoked on the updated team. Our implementation supports this use case, but the main technical focus of the paper remains the efficient solution of each resulting LTL-MRTA instance.
```

### 5.3 HLTL / 子公式交集 / poset 方法

这一段仍然应该保留，因为它直接关系到“为什么有 HLTL 等方法时，本文仍有意义”。

可插入英文：

```text
Another line of work improves scalability by restructuring the task specification itself. Hierarchical temporal-logic representations, such as H-LTLf, improve interpretability and planning efficiency by organizing a complex mission into multiple levels of temporal specifications. Poset- and decomposition-based methods exploit conjunctive or weakly coupled subformulas by extracting subtasks and partial-order relations, thereby avoiding the direct construction of a monolithic automaton for the full formula. These approaches are powerful and complementary, especially when the mission admits a meaningful hierarchy or can be decomposed into subformulas with limited interactions.
```

然后接本文差异：

```text
However, long temporal specifications are not always naturally separable at the specification level. Shared propositions, nested temporal dependencies, disjunctive choices, until-style waiting constraints, synchronized collaborative subtasks, and prefix-suffix coupling may make the interactions among subformulas essential for planning. In such cases, specification-level decomposition alone may not remove the need to jointly reason about automaton progress, robot assignment, and motion-induced cost. This paper therefore takes an orthogonal direction: instead of changing the specification language or relying on a prior decomposition, we keep the standard global LTL formulation and make the automaton-generation process itself planning-aware.
```

## 6. 本文方法总述建议

方法总述中不要写：

```text
This design enables fast feasible replanning under reduced robot availability.
```

这会让读者觉得动态机器人减少是核心贡献。

建议改成：

```text
To address the computational bottleneck of LTL-MRTA, we propose a framework that integrates robot planning into the automaton-generation process. Unlike methods that first construct the complete NBA and then perform planning on top of it, the proposed approach introduces information about the robot team, the workspace, and intermediate planning results during the translation from LTL to automata. In this way, the generated automaton and planning graph are better aligned with the executable allocation problem, allowing the planner to obtain an initial feasible solution quickly and then improve it through warm-started branch-and-bound.
```

如果要提动态，只在这一段后面加一句：

```text
In the implementation, the same planner can also be invoked with updated robot-team information, for example after robot removal, but this is treated as a practical extension rather than the main contribution of the paper.
```

## 7. Contributions 建议写法

贡献里建议完全不要出现“机器人减少”“动态重规划”“failure recovery”。可以把贡献写成下面三点：

```text
The main contributions of this work are summarized as follows.

1) We develop a new framework for LTL-MRTA that tightly couples task planning with the automaton-generation process, instead of treating automaton construction and planning as two separate stages. By introducing robot-team information, workspace information, and intermediate planning results into the translation procedure, the proposed method better aligns the generated automaton structure with the downstream planning problem.

2) We propose a planning-oriented pruning strategy during automaton construction. Branches that are irrelevant, infeasible, or unpromising for task planning are removed early in the GBA stage, and an NBA is then constructed together with a planning graph in an incremental manner. This design allows the method to produce an initial feasible solution quickly while reducing redundant search.

3) We develop a warm-start branch-and-bound procedure on the generated planning graph to further improve solution quality after a feasible plan is found. Therefore, the proposed framework explicitly addresses two practically important objectives in LTL-MRTA: rapid first-solution generation and continued improvement of the final plan quality.
```

如果导师/审稿人希望看到动态相关工作，可以在 contributions 后用一句非常轻的补充，不列为 contribution：

```text
We also implement a practical replanning interface that allows the planner to be called with an updated robot team, which is useful for robot-removal cases during execution.
```

但这句最好不要放在 numbered contributions 里。

## 8. 推荐的 introduction 逻辑顺序

建议整体顺序改成：

1. MRS 应用和 temporal requirements。
2. LTL-MRTA 静态问题定义：global LTL 给任务，不预先指定机器人。
3. 静态 LTL-MRTA 的计算困难：product automaton、机器人组合、任务复杂度。
4. 真实部署存在动态扰动：环境变化、任务变化、机器人减少；这些作为背景说明快速求解的重要性。
5. Related work：静态 LTL-MRTA 方法。
6. Related work：dynamic/reactive 方法，说明本文不以此为核心创新。
7. Related work：HLTL、子公式分解、poset 方法。
8. Gap：不是所有任务都适合规格层分解；本文从方法层把 planning 信息注入自动机构造。
9. 本文方法和贡献：快速 first feasible solution + 后续优化。

## 9. 可直接整合进 introduction 的版本

下面这版已经把机器人减少降为背景和工程扩展，不作为核心贡献：

```text
Multi-robot systems (MRS) have been widely used in applications such as persistent surveillance, logistics, and autonomous maintenance, where multiple robots can operate concurrently and cooperatively to accomplish tasks that are beyond the capability of a single robot. In many such applications, the mission is naturally subject to temporal requirements, such as ordering, persistence, and synchronization. Linear temporal logic (LTL) provides a rigorous language for specifying such requirements.

In this work, we consider the multi-robot task allocation problem under temporal logic specifications, referred to as LTL-MRTA. In LTL-MRTA, the global task is specified by an LTL formula, while the specific robots assigned to each subtask are not predetermined by the formula. This static problem is already computationally challenging because the search space grows with the number of robots, the workspace size, and the complexity of the temporal specification. Moreover, in practical deployments, planning may need to be invoked repeatedly when the current instance changes, for example because of environmental changes, temporary task requests, or reduced robot availability. These dynamic scenarios further motivate fast solution methods for the underlying LTL-MRTA problem, although dynamic replanning itself is not the main focus of this paper.

Existing top-down methods usually translate the global LTL formula into an automaton and then solve the resulting planning or allocation problem. Product-automaton, sampling-based, MILP-based, planning-tree-based, and partial-order-based methods have improved scalability from different perspectives. However, many of them still require substantial computation before a planning structure suitable for allocation is obtained, which can delay the discovery of the first feasible solution.

Dynamic and reactive variants of temporal-logic task allocation have also been studied, including methods that respond to environmental changes, temporary tasks, resource variation, and agent failures. These works show that practical multi-robot systems often need to update plans during execution. In this paper, such scenarios are treated mainly as motivation for fast planning: whenever the current task or robot-team information is updated, the planner should be able to solve the resulting LTL-MRTA instance efficiently. In particular, robot removal can be handled in implementation by invoking the planner with the reduced available robot set, but this is considered a practical extension rather than a core algorithmic contribution.

Another line of work improves scalability by restructuring the task specification itself. Hierarchical temporal-logic representations, such as H-LTLf, improve interpretability and planning efficiency by organizing a complex mission into multiple levels of temporal specifications. Poset- and decomposition-based methods exploit conjunctive or weakly coupled subformulas by extracting subtasks and partial-order relations, thereby avoiding the direct construction of a monolithic automaton for the full formula. These approaches are powerful and complementary, especially when the mission admits a meaningful hierarchy or can be decomposed into subformulas with limited interactions.

However, long temporal specifications are not always naturally separable at the specification level. Shared propositions, nested temporal dependencies, disjunctive choices, until-style waiting constraints, synchronized collaborative subtasks, and prefix-suffix coupling may make the interactions among subformulas essential for planning. In such cases, specification-level decomposition alone may not remove the need to jointly reason about automaton progress, robot assignment, and motion-induced cost. This paper therefore takes an orthogonal direction: instead of changing the specification language or relying on a prior decomposition, we keep the standard global LTL formulation and make the automaton-generation process itself planning-aware.

Specifically, we follow the LTL2BA-style translation pipeline from LTL to VWAA, GBA, and NBA. During this process, robot-team information, workspace information, and intermediate planning results are introduced into automaton construction. Planning-irrelevant or infeasible branches are pruned early, and the NBA is constructed together with a planning graph in an incremental manner. Once an accepting prefix-suffix structure is reached, an initial feasible plan can be extracted and then used to warm-start branch-and-bound optimization. In this way, the proposed framework supports rapid first-solution generation and continued improvement of solution quality for LTL-MRTA.
```

## 10. 最终建议

最重要的改法是：把动态机器人减少从“本文贡献”中移除，放到“背景动机”和“工程实现补充”里。文章主线仍然应该是：

```text
static LTL-MRTA is hard -> dynamic deployment makes fast solving more valuable -> existing HLTL/decomposition methods solve a different/specification-level issue -> this paper solves the method-level bottleneck by planning-aware automaton generation.
```

