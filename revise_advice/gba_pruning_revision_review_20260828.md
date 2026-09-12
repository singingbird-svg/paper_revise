# `Pruning for GBA` 审稿式检查与修改方案

## 0. 总体结论

当前 Sec. V 的技术主线是成立的，而且两类 pruning 的功能区分也基本正确：

1. **在 VWAA-to-GBA construction 过程中进行 robot-team infeasibility screening**，避免当前团队显然无法执行的 candidate transition 进入 GBA；
2. **在 GBA 完成后删除 progress-consistent decomposable transitions**，避免把不必要的同步要求传播到后续 NBA generation 和 plan-graph construction。

问题主要不在“缺少方法内容”，而在于当前版本的若干关键概念没有完全形式化，导致审稿人可能在以下位置产生疑问：

- `\sigma` 究竟是 alphabet symbol、literal set，还是 symbolic Boolean guard？
- “feasible transition”具体检查了什么：robot type/cardinality、workspace reachability，还是完整 assignment feasibility？
- 如果 transition guard 含有析取，是否会因为其中一个不可行分支而删除整个 transition？
- `\sigma_{ij}=\sigma_{ik}\cup\sigma_{kj}` 在一般 symbolic guard 下是否有严格含义？
- 为什么两步 decomposition 一定能够替代直接 transition，并且递归替换一定终止？
- “equivalent feasible solution”中的 `equivalent` 是语言等价、任务需求相同，还是代价相同？
- 删除 transition 后，accepting transition sets 和不可达 GBA states 如何更新？

这些问题会直接影响审稿人对 **pruning soundness、completeness preservation 和符号规范性** 的判断。

我建议将本节标题由：

```latex
\section{Pruning for GBA}
```

改为：

```latex
\section{Planning-Aware GBA Pruning}
```

并重构为三个逻辑层次：

```text
A. Team-Infeasible Candidate Pruning
B. Progress-Consistent Decomposition Pruning
C. Feasibility Preservation
```

这样比当前使用 `1)`、`2)` 连续叙述更清楚，也能让两类 pruning 的发生时机和理论作用一目了然。

---

# 1. 从审稿人角度看，当前版本最需要修正的问题

## 1.1 开头与前文重复较多，但没有立刻给出本节的技术边界

当前开头重复强调：

> pruning occurs before complete NBA construction；
>
> early pruning reduces GBA size；
>
> unnecessary transitions are not propagated downstream。

这些观点在 Introduction、Contributions 和 System Overview 中已经出现。

### 建议

方法章节开头应直接回答：

- pruning 在什么时候执行？
- 每一阶段检查什么？
- 最终输出什么？

推荐压缩为：

> This section introduces two planning-aware reductions before GBA-to-NBA degeneralization. The first removes candidate transition clauses that cannot be supported by the available robot types and cardinalities during GBA construction. The second removes direct composite transitions after GBA construction when an existing two-hop path separates their action requirements without changing the acceptance progress used in degeneralization.

这样开头已经包含完整方法地图，不再泛泛重复动机。

---

## 1.2 `\sigma` 的使用与 Preliminaries 不一致

在 Preliminaries 中：

\[
\sigma_k\in\Sigma=2^{AP}
\]

表示 infinite word 在第 \(k\) 步的 alphabet letter。

但在 Sec. V 中：

\[
e^g=(q_g,\sigma_g,q'_g)
\]

以及：

\[
\sigma_{ij}=\sigma_{ik}\cup\sigma_{kj}
\]

又把 `\sigma` 当成 symbolic transition condition 或 literal set。

这会产生类型混淆。

### 推荐统一

按照前面对 Preliminaries 的修改，全文采用：

- \(\sigma\in\Sigma\)：concrete input valuation；
- \(\gamma\)：symbolic Boolean guard。

因此写成：

\[
e^g=(q_g,\gamma_g,q'_g),
\]

或：

\[
q_{g,i}\xrightarrow{\gamma_{ij}}q_{g,j}.
\]

并明确：

\[
\sigma\models\gamma_{ij}
\]

表示 concrete valuation \(\sigma\) enables the symbolic transition。

本修改稿全部采用 `\gamma`。

如果你暂时不修改前文，可以把下面替换稿中的 `\gamma` 机械改回 `\sigma`；但从全文规范性看，不推荐继续混用。

---

## 1.3 当前“feasible transition”定义过宽

当前文字是：

> If no subset of \(R\) can satisfy the requirements, \(e^g\) is infeasible. Otherwise, it is retained.

这里有两个问题。

### 问题一：通过 screening 不等于 transition 已经“feasible”

当前 GBA-level check 的示例只使用了：

- required robot types；
- required robot cardinalities；
- 同一 transition 中不同 action assignments 必须 disjoint。

它没有检查：

- robots 当前的位置；
- target-region reachability；
- travel time；
- holding conditions；
- 与前序 assignment 的兼容性。

这些信息在 Sec. VI 的 plan-node extension 中才被使用。

因此，通过 GBA screening 的 transition 只能说：

> **not ruled out by the aggregate team-capacity test**

而不能说已经具备完整的 planning feasibility。

### 问题二：Introduction 中的 `workspace information` 与本节实际检查不一致

当前 Introduction 声称 automaton construction 使用了：

> robot-team feasibility and workspace information.

但 Sec. V 的 pruning 只明确使用 type/cardinality。

如果你的实现确实只做 type/cardinality screening，应将全文统一改成：

> robot-team type and cardinality information

或者：

> aggregate robot-team feasibility information.

如果代码还检查了 \(d_k(x(r_k),l(a))<\infty\)，则需要在本节明确写出 reachability-aware assignment test，而不能只给 cardinality example。

本修改稿的主版本采用**保守的 type/cardinality criterion**，因为这是当前论文和 Example 2 明确支持的内容。

---

## 1.4 如果 guard 含有析取，必须 clause-wise 处理

假设 candidate guard 为：

\[
\gamma=(a_1\land a_2)\lor a_3.
\]

即使 \(a_1\land a_2\) 对当前 team 不可行，只要 \(a_3\) 可行，整个 transition 就不能被删除。

因此专业写法应是：

- 对 symbolic guard 的每个 conjunctive clause 独立检查；
- 删除 team-infeasible clauses；
- 只有全部 clauses 都被删除时，才删除 candidate transition。

如果 LTL2BA implementation 已经将每个 clause 存成单独 symbolic edge，这一规则自然退化为逐 edge 检查，但正文仍应说明。

---

## 1.5 当前 generic example 与 Example 2 重复

当前先写了“3 个 type-1 robots 在 \(l_1\)，另外 3 个 type-1 robots 在 \(l_2\)”的泛化例子，紧接着又用 Example 2 解释 \(a_1,a_2\)。

这两段作用完全相同。

### 建议

删除 generic example，只保留：

1. 一个 formal demand criterion；
2. 一个与 Example 1 连贯的 Example 2。

这样更紧凑。

---

## 1.6 Definition 6 对 general symbolic guards 不够严谨

当前定义：

\[
\sigma_{ij}=\sigma_{ik}\cup\sigma_{kj}.
\]

如果 `\sigma` 是 symbolic Boolean formula，则集合并没有定义。

如果 `\sigma` 是 alphabet letter，则一条 direct transition 的 letter 与两个不同时间步的 letters 也不是同一语义对象。

### 推荐

明确说明 decomposition test 作用于 **consistent conjunctive guards**，并用 literal-set notation：

\[
\operatorname{Lit}(\gamma)
\]

表示 guard 中的 literals。

对包含析取的 guard，先 clause-wise split。

同时，由于你真正希望分解的是 simultaneously required positive action propositions，建议增加：

\[
\operatorname{Act}^{+}(\gamma_{ij})
=
\operatorname{Act}^{+}(\gamma_{ik})
\mathbin{\dot\cup}
\operatorname{Act}^{+}(\gamma_{kj}),
\]

其中 \(\dot\cup\) 表示 disjoint union，并要求两边均非空。

再要求：

\[
\operatorname{Lit}(\gamma_{ij})
=
\operatorname{Lit}(\gamma_{ik})
\cup
\operatorname{Lit}(\gamma_{kj}).
\]

这表示：

- direct transition 的 positive action requirements 被拆成两个非空、互不重叠的部分；
- two-hop witness 没有引入 direct guard 中不存在的新 literal；
- shared safety/holding literals 可以同时出现在两条 witness transitions 中；
- 每条 witness transition 的 positive action set 严格小于 direct transition，从而保证递归 decomposition 有一个严格下降的度量。

这比当前只写集合并更符合“独立 subtasks”的技术目的。

---

## 1.7 当前 Lemma 2 的递归终止理由不充分

当前 proof 写道：

> Since the GBA contains finitely many transitions, this decomposition process terminates.

有限 transition 数量本身不能排除 decomposition dependencies 形成环，例如：

\[
e_1\rightarrow e_2\rightarrow e_1.
\]

### 推荐

在 Definition 6 中加入 proper decomposition 条件：

- direct transition 的 positive action set 被拆成两个非空 strict subsets；
- 每次 replacement 后，每个 component 的 action count 严格减小。

则递归深度至多为：

\[
|\operatorname{Act}^{+}(\gamma_{ij})|-1.
\]

这样终止性由 well-founded rank 明确保证，而不是依赖“GBA finite”这一不足的理由。

---

## 1.8 `equivalent feasible solution` 未定义

当前 Lemma 2 写：

> the pruned GBA also admits an equivalent feasible solution.

但 decomposition 可能把同时发生的动作变成两个 automaton steps，因此：

- resulting word 的长度可能改变；
- makespan 可能改变；
- 不能保证保留 original cost-optimal solution。

你的实验中 plan-graph solution 与 reference global optimum 也并不总相同，因此这里绝不能暗示 cost preservation。

### 推荐

Lemma 2 只声称：

> **existence of a feasible accepting plan is preserved.**

也就是 completeness/feasibility preservation，而不是 cost equivalence。

可以写：

> The replacement may change the temporal realization and cost; the lemma preserves feasibility, not optimality.

---

## 1.9 删除 transition 后应明确更新 \(F_g\) 和 \(Q_g\)

当前没有正式定义 final pruned GBA。

建议加入：

\[
\rightarrow_g^{-}
=
\rightarrow_g\setminus E_{\mathrm{pc}},
\]

\[
F_{g,h}^{-}
=
F_{g,h}\cap\rightarrow_g^{-},
\qquad h=1,\ldots,m_g.
\]

随后进行 standard reachability cleanup，删除：

- 从 initial states 不可达的 states；
- pruning 后不再连接到任何 accepting continuation 的 dead structure。

最终定义：

\[
G_\phi^{-}
=
(Q_g^{-},Q_{g,0}^{-},\Sigma,
\rightarrow_g^{-},F_g^{-}).
\]

这能让 Sec. VI 的输入 \(G_\phi^{-}\) 有正式来源。

---

## 1.10 Lemma 1 的结论可以更精确

当前：

> Every NBA transition induced by a progress-consistent decomposable GBA transition is decomposable.

Proof 实际证明的是：

> 对任意 degeneralization index \(\ell\)，direct GBA transition 所诱导的 NBA transition 可以由一个经过相同 intermediate GBA state 的 two-transition NBA path 替换，并到达相同 terminal NBA state。

建议直接把 lemma 写成这个结论，而不是再次依赖一个泛化的“NBA decomposable”术语。

---

# 2. 推荐的符号系统

| 对象 | 推荐符号 | 说明 |
|---|---|---|
| concrete alphabet letter | \(\sigma\in\Sigma\) | 只用于 word semantics |
| symbolic transition guard | \(\gamma\) | 替代当前 transition 上的 \(\sigma\) |
| candidate GBA transition | \(e^g=(q_g,\gamma_g,q'_g)\) | symbolic representation |
| positive action literals | \(\operatorname{Act}^{+}(\gamma)\) | guard 中正出现的 action propositions |
| all literals | \(\operatorname{Lit}(\gamma)\) | guard 的 conjunctive literal set |
| type-\(j\) demand | \(d_j(C)\) | 一个 conjunctive clause 对 type \(j\) 的 robot demand |
| accepting-set memberships | \(\operatorname{Acc}(e^g)\) | 替代普通函数体 `Acc` |
| acceptance index set | \(\mathcal I_F=\{0,\ldots,m_g\}\) | 不使用易混淆的 `IF` |
| progress update | \(\eta(\ell,e^g)\) | 保留当前记号 |
| final pruned GBA | \(G_\phi^{-}\) | 明确定义 output |

如果你采用前面对 Problem Formulation 的推荐，则 action requirement 写成：

\[
c(a)=\bigl(t(a),n(a),l(a)\bigr).
\]

如果仍保留当前：

\[
c(a_i)=(\tau_i,n_i,l_i),
\]

下面的正文只需做机械替换。

---

# 3. 推荐的逻辑结构

## A. Team-Infeasible Candidate Pruning

逻辑顺序应为：

1. candidate GBA transition 如何表示；
2. 从 guard 中提取 positive action requirements；
3. 定义每种 robot type 的 aggregate demand；
4. clause-wise 判断；
5. 说明 screening 是 conservative；
6. Example 2。

核心结论：

> 该 pruning 删除的是“必然不能由当前 team 支持”的 clauses，而不是提前完成完整 task allocation。

---

## B. Progress-Consistent Decomposition Pruning

逻辑顺序应为：

1. 为什么 simultaneous composite transition 可能冗余；
2. 仅有 task decomposition 不够，因为 GBA 是 transition-based generalized acceptance；
3. 定义 proper task decomposition；
4. 定义 acceptance-progress function；
5. 定义 progress consistency；
6. 给 Example 3；
7. 正式定义 \(G_\phi^{-}\)。

核心结论：

> direct transition 只有在 task requirements 可被较小 transitions 分解，且 degeneralization progress 对任意 \(\ell\) 都保持一致时才删除。

---

## C. Feasibility Preservation

保留两个简短 lemmas：

1. direct induced NBA transition 可以由同 endpoint、同 progress 的 two-edge path 替代；
2. original GBA 中 feasible accepting plan 的存在性在 pruning 后仍被保留。

不要在本节声称 optimality preservation。

---

# 4. 最推荐的完整英文替换稿

下面版本按照前面推荐的统一记号编写。建议用它替换当前 Sec. V 的全部内容。

```latex
\section{Planning-Aware GBA Pruning}

This section introduces two planning-aware reductions applied
before GBA-to-NBA degeneralization. The first is integrated
into VWAA-to-GBA construction and removes candidate
transition clauses that cannot be supported by the types and
cardinalities of the available robot team. The second is applied
after the GBA has been constructed and removes direct
composite transitions whose task requirements can be separated
along an existing two-hop path without changing the acceptance
progress used in degeneralization. The resulting automaton,
denoted by $G_\phi^{-}$, is passed to the joint NBA--plan-graph
construction in Sec.~VI.

Throughout this section, a symbolic transition
\[
q_{g,i}\xrightarrow{\gamma_{ij}}q_{g,j}
\]
represents all concrete alphabet symbols $\sigma\in\Sigma$
satisfying the Boolean guard $\gamma_{ij}$.

\subsection{Team-Infeasible Candidate Pruning}

Consider a candidate GBA transition
\[
e^g=(q_g,\gamma_g,q'_g)
\]
generated by combining one outgoing VWAA transition from
each state represented in $q_g$. Let
$\mathcal C(\gamma_g)$ denote the set of consistent conjunctive
clauses in a disjunctive-normal-form representation of
$\gamma_g$. If the implementation already stores each clause
as a separate symbolic transition, then
$\mathcal C(\gamma_g)$ contains a single clause.

For a clause $C\in\mathcal C(\gamma_g)$, let
\[
\operatorname{Act}^{+}(C)
:=
\{a\in A \mid a \text{ occurs positively in } C\}
\]
be the action propositions that must hold simultaneously.
Recall that $c(a)=(t(a),n(a),l(a))$ specifies the required
robot type, cardinality, and target region. Since assignments
to distinct action propositions in the same transition are
required to be disjoint, the aggregate demand for robots of
type $j$ is
\[
d_j(C)
:=
\sum_{\substack{a\in\operatorname{Act}^{+}(C)\\t(a)=j}}
n(a).
\]

\textbf{Definition 6 (Team-infeasible clause).}
A conjunctive clause $C$ is team-infeasible if
\[
\exists j\in\mathcal T
\quad\text{s.t.}\quad
d_j(C)>|R_j|.
\]
A candidate transition is team-infeasible if every clause in
$\mathcal C(\gamma_g)$ is team-infeasible.

During GBA construction, team-infeasible clauses are removed
from $\gamma_g$. If no clause remains, the candidate transition
is discarded before its acceptance-set membership is computed
and before it is inserted into $\rightarrow_g$. Otherwise, the
transition is retained with the remaining guard clauses.

This test is deliberately conservative. Passing it only means
that a transition is not ruled out by aggregate type and
cardinality information; it does not yet guarantee a feasible
state-dependent assignment. Robot reachability, predicted
arrival times, and compatibility with the current partial plan
are evaluated during plan-graph extension in Sec.~VI.

\textbf{Example 2.}
Continuing Example~1, suppose that VWAA-to-GBA construction
produces a candidate guard containing
$a_1\land a_2$. Since
\[
c(a_1)=(2,2,l_5),
\qquad
c(a_2)=(2,1,l_6),
\]
the corresponding type-2 demand is
\[
d_2=2+1=3.
\]
However, the team contains only two type-2 robots, i.e.,
$|R_2|=2$. Because the assignments for $a_1$ and $a_2$ must
be disjoint when they occur in the same transition, this clause
is team-infeasible and is removed before insertion into the
GBA.

\subsection{Progress-Consistent Decomposition Pruning}

The first reduction removes transitions that the current team
cannot execute. The second targets a different source of
downstream complexity: a direct transition may require several
independent action propositions to hold at the same automaton
step, although the GBA already contains a two-hop path that
realizes the same task progress through smaller action sets.
Removing such a direct transition can avoid propagating
unnecessary synchronization to the degeneralized NBA.
However, guard decomposition alone is insufficient because
GBA-to-NBA degeneralization also tracks progress through the
accepting transition sets.

The following definition is applied to consistent conjunctive
guards. Guards containing disjunctions are tested clause-wise.
Let $\operatorname{Lit}(\gamma)$ denote the set of literals in
$\gamma$, and let $\operatorname{Act}^{+}(\gamma)$ denote its
positive action literals.

\textbf{Definition 7 (Properly task-decomposable transition).}
Consider a symbolic transition
\[
e^g_{ij}:
q_{g,i}\xrightarrow{\gamma_{ij}}q_{g,j}.
\]
It is properly task-decomposable if there exist a state
$q_{g,k}$ and transitions
\[
e^g_{ik}:
q_{g,i}\xrightarrow{\gamma_{ik}}q_{g,k},
\qquad
e^g_{kj}:
q_{g,k}\xrightarrow{\gamma_{kj}}q_{g,j},
\]
such that
\[
\operatorname{Act}^{+}(\gamma_{ij})
=
\operatorname{Act}^{+}(\gamma_{ik})
\mathbin{\dot\cup}
\operatorname{Act}^{+}(\gamma_{kj}),
\tag{4}
\]
where both sets on the right-hand side are nonempty, and
\[
\operatorname{Lit}(\gamma_{ij})
=
\operatorname{Lit}(\gamma_{ik})
\cup
\operatorname{Lit}(\gamma_{kj}).
\tag{5}
\]
The pair $(e^g_{ik},e^g_{kj})$ is called a decomposition
witness of $e^g_{ij}$.

Equation~(4) separates the simultaneous positive action
requirements into two nonempty disjoint subsets, whereas
(5) ensures that the two-hop witness collectively introduces no
guard literal absent from the direct transition. Non-action
safety or holding literals may occur in both witness guards.
The nonempty proper split also provides a strictly decreasing
measure on the number of positive action literals.

It remains to ensure that replacing the direct transition by
the two-hop path preserves the acceptance progress used in
degeneralization. Let
\[
F_g=\{F_{g,1},\ldots,F_{g,m_g}\},
\qquad
\mathcal I_F:=\{0,\ldots,m_g\}.
\]
For a GBA transition $e^g\in\rightarrow_g$, define
\[
\operatorname{Acc}(e^g)
:=
\{h\in\{1,\ldots,m_g\}\mid e^g\in F_{g,h}\}.
\]
An NBA state generated by degeneralization is represented by
$(q_g,\ell)$, where $\ell\in\mathcal I_F$ records the current
progress through the accepting transition sets. Before a new
acceptance round is tracked, define
\[
\bar{\ell}
:=
\begin{cases}
0, & \ell=m_g,\\
\ell, & \text{otherwise}.
\end{cases}
\]
The progress after traversing $e^g$ is
\[
\eta(\ell,e^g)
:=
\max
\left\{
r\in\{\bar{\ell},\ldots,m_g\}
\;\middle|\;
\{\bar{\ell}+1,\ldots,r\}
\subseteq
\operatorname{Acc}(e^g)
\right\}.
\tag{6}
\]
The empty interval is interpreted as the empty set, so the
maximum is always well defined.

\textbf{Definition 8 (Progress-consistent decomposition).}
A properly task-decomposable transition $e^g_{ij}$ is
progress-consistent if it has a decomposition witness
$(e^g_{ik},e^g_{kj})$ satisfying
\[
\eta\!\left(
\eta(\ell,e^g_{ik}),e^g_{kj}
\right)
=
\eta(\ell,e^g_{ij}),
\qquad
\forall\ell\in\mathcal I_F.
\tag{7}
\]
Only transitions satisfying Definitions~7 and~8 are removed.

\textbf{Example 3.}
Continuing Example~2, suppose that the GBA contains
\[
e^g_{ij}:
q_{g,i}\xrightarrow{a_2\land a_3}q_{g,j},
\]
together with
\[
e^g_{ik}:
q_{g,i}\xrightarrow{a_2}q_{g,k},
\qquad
e^g_{kj}:
q_{g,k}\xrightarrow{a_3}q_{g,j}.
\]
The positive action requirements of the direct transition are
the disjoint union of those on the two-hop path, so
$e^g_{ij}$ is properly task-decomposable. Let the three
relevant accepting transition sets be indexed by
$1,2,3$, and suppose
\[
\operatorname{Acc}(e^g_{ij})=\{1,2,3\},
\quad
\operatorname{Acc}(e^g_{ik})=\{1,2\},
\quad
\operatorname{Acc}(e^g_{kj})=\{1,2,3\}.
\]
Then, for every $\ell\in\{0,1,2,3\}$,
\[
\eta(\ell,e^g_{ij})=3,
\qquad
\eta(\ell,e^g_{ik})=2,
\qquad
\eta(2,e^g_{kj})=3.
\]
Hence,
\[
\eta\!\left(
\eta(\ell,e^g_{ik}),e^g_{kj}
\right)
=
\eta(\ell,e^g_{ij}),
\]
and $e^g_{ij}$ can be removed.

Let $E_{\mathrm{pc}}$ denote the set of all
progress-consistent decomposable transitions selected for
removal. The retained transition relation and accepting sets
are
\[
\rightarrow_g^{-}
:=
\rightarrow_g\setminus E_{\mathrm{pc}},
\]
and
\[
F_{g,h}^{-}
:=
F_{g,h}\cap\rightarrow_g^{-},
\qquad h=1,\ldots,m_g.
\]
After removing unreachable states using the standard LTL2BA
cleanup, the final pruned GBA is denoted by
\[
G_\phi^{-}
=
(Q_g^{-},Q_{g,0}^{-},\Sigma,
\rightarrow_g^{-},F_g^{-}).
\]

\subsection{Feasibility Preservation}

The following results state the role of the progress-consistency
test and the scope of the pruning guarantee.

\textbf{Lemma 1.}
Let $e^g_{ij}$ be a progress-consistent decomposable GBA
transition with witness $(e^g_{ik},e^g_{kj})$. For every
degeneralization index $\ell\in\mathcal I_F$, the NBA
transition induced by $e^g_{ij}$ can be replaced by a
two-transition NBA path through
\[
\left(
q_{g,k},
\eta(\ell,e^g_{ik})
\right)
\]
that reaches the same terminal NBA state.

\emph{Proof.}
From the NBA state $(q_{g,i},\ell)$, the direct transition
induced by $e^g_{ij}$ reaches
\[
\left(
q_{g,j},
\eta(\ell,e^g_{ij})
\right).
\]
The witness first reaches
\[
\left(
q_{g,k},
\eta(\ell,e^g_{ik})
\right)
\]
and then reaches
\[
\left(
q_{g,j},
\eta(
\eta(\ell,e^g_{ik}),
e^g_{kj})
\right).
\]
These terminal states coincide by (7). Equations~(4)--(5)
ensure that the positive action requirements are separated
without introducing new guard literals. \hfill$\square$

\textbf{Lemma 2 (Feasibility preservation).}
Let $B_\phi$ and $B_\phi^{-}$ be the NBAs obtained from the
original and pruned GBAs, respectively. If $B_\phi$ admits a
feasible accepting plan under the robot model in Sec.~III,
then $B_\phi^{-}$ also admits a feasible accepting plan.

\emph{Proof.}
A clause removed by the team-capacity test cannot occur in a
feasible plan, because its simultaneous action requirements
would require more robots of some type than are available
under the disjoint-assignment rule.

Now consider an occurrence of a transition induced by a
progress-consistent decomposable GBA transition. By Lemma~1,
it can be replaced by the NBA path induced by its two-hop
witness without changing the terminal NBA state or the
acceptance progress. The feasible assignment of the direct
transition can be restricted to the two disjoint action subsets in
(4), while (5) introduces no additional literal requirement.
If a witness transition is itself removed, the same replacement
is applied recursively. Because each component contains
strictly fewer positive action propositions than its parent
transition, this recursion terminates after finitely many steps.
Replacing every removed occurrence therefore yields a feasible
accepting plan in $B_\phi^{-}$. \hfill$\square$

Lemma~2 preserves the existence of a feasible plan. It does not
claim that the replacement has the same makespan or that
cost-optimal plans of the unpruned automaton are retained.
```

---

# 5. 为什么推荐版本比当前版本更严密

## 5.1 两类 pruning 的作用不再混淆

修改后：

- Stage A 只做 **aggregate team-capacity infeasibility screening**；
- Stage B 只做 **acceptance-progress-preserving structural reduction**；
- state-dependent reachability 和 assignment 留在 Sec. VI。

这样 reviewer 不会误以为 GBA-level pruning 已经完成了完整 robot allocation。

---

## 5.2 `\gamma` 与 `\sigma` 的语义分离

修改后：

\[
\sigma\in 2^{AP}
\]

始终是 concrete valuation；

\[
\gamma
\]

始终是 symbolic guard。

Definition 7 中的 literal set 也有明确来源，不再对一个含义不清的 `\sigma` 做集合并。

---

## 5.3 对析取 guard 的处理是 sound 的

修改后只在所有 clauses 均不可行时删除 transition，不会因为一个 infeasible alternative 而误删其他 feasible alternatives。

---

## 5.4 decomposition 与 acceptance consistency 分成两层

修改后逻辑为：

\[
\text{task decomposition}
+
\text{degeneralization progress equivalence}
\Rightarrow
\text{removable direct transition}.
\]

这正是你方法最重要的技术判断。

---

## 5.5 completeness proof 有明确的 termination measure

每次 decomposition 都严格减少 positive action count，因此不存在循环展开问题。

---

## 5.6 不再过度声称 cost preservation

修改后的 Lemma 2 只保证：

\[
\text{feasible plan exists before pruning}
\Rightarrow
\text{feasible plan exists after pruning}.
\]

这与论文的 soundness/completeness 主张一致，也与实验中 pruned plan graph 未必保留 original global optimum 的现象一致。

---

# 6. 如果你的实现确实检查 workspace reachability

当前替换稿采用 type/cardinality test，因为这是现稿明确描述和实验支持的内容。

如果代码实际在 GBA stage 还使用了 robot-region reachability，可将 Definition 6 替换成下面更强的版本。

令：

\[
R_j(l)
:=
\left\{
r_k\in R_j
\mid
d_k(x(r_k),l)<+\infty
\right\}.
\]

一个 clause \(C\) 是 team-and-reachability feasible，当且仅当存在 assignment：

\[
\mathcal C_C:
\operatorname{Act}^{+}(C)\rightarrow 2^R
\]

满足：

\[
\mathcal C_C(a)
\subseteq
R_{t(a)}(l(a)),
\]

\[
|\mathcal C_C(a)|=n(a),
\]

以及：

\[
\mathcal C_C(a)\cap\mathcal C_C(b)=\emptyset,
\quad a\neq b.
\]

该判定可以写成 bipartite \(b\)-matching 或 small flow feasibility test。

只有当你的代码真正执行了这一步时，正文才应使用：

> robot-team and workspace feasibility

否则建议统一写成：

> aggregate robot-team type/cardinality feasibility.

---

# 7. 与其他章节需要同步修改的地方

## 7.1 Preliminaries

将：

```latex
e_g=(q_g,\sigma_g,q'_g)
```

统一改为：

```latex
e^g=(q_g,\gamma_g,q'_g).
```

并说明：

```latex
\sigma\models\gamma_g.
```

---

## 7.2 Problem Formulation

将 subtask：

\[
\omega_{ij}=(\sigma_{ij},\sigma_i^s)
\]

改为：

\[
\omega_{ij}=(\gamma_{ij},\gamma_i^{\mathrm{hold}}).
\]

---

## 7.3 System Overview

建议写：

> During GBA construction, aggregate type/cardinality
> information removes team-infeasible candidate clauses.

不要在实现仅做 cardinality screening 时写：

> workspace information is incorporated during GBA pruning.

---

## 7.4 Sec. VI

Algorithm 2 和 Algorithm 3 中所有 transition labels：

```latex
q_{B,i}\xrightarrow{\sigma_{ij}}q_{B,j}
```

改为：

```latex
q_{B,i}\xrightarrow{\gamma_{ij}}q_{B,j}.
```

---

## 7.5 Complexity Analysis

全文统一使用：

> progress-consistent decomposition pruning

不要再混用：

- ST pruning；
- decomposition-inducing transition pruning；
- decomposition-preserving pruning；
- redundant-transition pruning。

如果需要短名称，可第一次定义：

> progress-consistent decomposition (PCD) pruning

后文统一使用 `PCD pruning`。

---

## 7.6 Theoretical Analysis

后面的 main theorem 不要重新证明 Sec. V 已证明的 pruning property，只需引用：

```latex
By Lemma~2, GBA-level pruning preserves the existence of a
feasible accepting plan.
```

这样可以减少理论部分重复。

---

# 8. 一个更保守、改动更小的版本

如果你暂时不希望增加 DNF clause 和 proper-decomposition notation，至少应完成以下修改：

1. `\sigma_{ij}` 全部改为 `\gamma_{ij}`；
2. 把 “feasible transition” 改成 “not ruled out by the team-capacity test”；
3. 删除 generic 3+3 example；
4. Definition 6 改为：
   \[
   \operatorname{Lit}(\gamma_{ij})
   =
   \operatorname{Lit}(\gamma_{ik})
   \cup
   \operatorname{Lit}(\gamma_{kj});
   \]
5. 要求两个 component 的 positive action sets 都是 nonempty strict subsets；
6. Lemma 2 删除 `equivalent`；
7. 递归终止理由改成 action-set cardinality strictly decreases；
8. 定义 \(G_\phi^{-}\)、\(\rightarrow_g^{-}\) 和 \(F_g^{-}\)。

不过从审稿稳健性看，我更推荐第 4 节的完整版本。

---

# 9. 最终审稿建议

修改后的 Sec. V 应让审稿人清楚得到以下结论：

> The first pruning rule is a conservative, system-dependent
> infeasibility test applied before a candidate GBA transition is
> materialized. The second rule is a structural reduction applied
> to the completed GBA, but only when task decomposition and
> generalized-acceptance progress agree. The first rule cannot
> remove a feasible assignment because it discards only clauses
> whose aggregate type demand exceeds the available team. The
> second cannot remove the last feasible accepting behavior
> because every removed transition has a strictly smaller,
> progress-equivalent witness path. Therefore, the pruned GBA
> reduces downstream structure while preserving feasibility, but
> not necessarily optimal cost.

如果 reviewer 能从本节直接形成这一认识，那么该部分的逻辑、符号和理论边界就是清楚的。
