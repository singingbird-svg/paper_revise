# `BRANCH-AND-BOUND OPTIMIZATION` 审稿式检查与修改方案

## 0. 总体判断

我对照检查了当前稿件中的：

- Sec. III：计划、robot assignment 和 makespan 定义；
- Sec. VI：plan graph、representative execution state、plan extraction 与 \(\Pi_{\mathrm{plan}}\)；
- Sec. VII：Algorithm 4、Node Expansion、Lower Bound、Upper Bound、Branching and Pruning；
- Sec. VIII：robot unavailability 下无 warm start 的 BnB re-optimization；
- Secs. IX–X：复杂度、soundness/completeness；
- Sec. XI-A：BnB bound evolution 与 incumbent improvement。

当前 BnB 部分的整体技术框架已经比较完整：

\[
\Pi_{\mathrm{plan}}
\;\longrightarrow\;
\text{warm-started BnB}
\;\longrightarrow\;
\text{path/assignment enumeration}
\;\longrightarrow\;
\text{lower-bound pruning}
\;\longrightarrow\;
\Pi^\star .
\]

特别是，当前版本已经不再把“所有下游可达 action 的并集”直接作为 lower bound，而是引入了

\[
A_{\mathrm{must}}(\nu),
\]

即所有 accepting continuations 共同需要的 action propositions。这一方向是正确的。

不过，从严格审稿角度看，本节仍有若干需要修改的地方。最重要的不是英语表达，而是以下几个逻辑边界还没有完全说明：

1. **BnB 的最优性范围是 generated plan graph 内，而不是自动等同于原始 LTL-MRTA problem 的 global optimum。**
2. **BnB search state 与 Sec. VI plan node 中保存的 representative payload 必须明确分离。**
3. **\(A_{\mathrm{must}}\) 的语义、计算方法和 lower-bound admissibility 还缺少正式说明。**
4. **当前 Algorithm 4 强制要求 \(\Pi_{\mathrm{plan}}\) 作为 warm start，与 Sec. VIII 中“without a warm start”的 repair setting 不一致。**
5. **Upper Bound 子节实际描述的是 greedy rollout，而不是一个独立的数学 upper-bound function。**
6. **rollout 只尝试一个 successor，若该 successor 的 greedy assignment 失败就立即终止，可能错过同一步其他容易获得的 feasible successor。**
7. **Algorithm 4 在相关符号和 lower bound 尚未定义前就出现，阅读顺序不够自然。**
8. **如果 plan graph 中仍有 structural cycles，需要明确 BnB 为什么会终止。**

我建议将本节重组为四个紧密衔接的子节：

```text
A. Search State and Node Expansion
B. Admissible Lower Bound
C. Greedy Rollout for Incumbent Update
D. Search Order, Pruning, and Termination
```

并把 Algorithm 4 放在这些定义之后。

---

# 1. 与前后文的接口应当明确到什么程度

## 1.1 从 Sec. VI 接收什么

Sec. VII 的输入应明确为：

\[
G_P=(V_P,E_P),
\qquad
\Pi_{\mathrm{plan}}.
\]

其中：

- \(G_P\) 是 Sec. VI simplification 后保留的 plan graph；
- \(\Pi_{\mathrm{plan}}\) 是 construction stage 中发现的最佳 feasible incumbent；
- \(\Pi_{\mathrm{plan}}\) 不是本节重新证明的 optimal solution；
- BnB 会重新枚举 retained graph 上的 alternative robot assignments，而不是简单重放 plan node 中保存的 greedy assignment。

建议在 Sec. VII 开头明确写：

> The execution state carried by a BnB search node is search-specific and is independent of the representative assignment and execution state stored in the corresponding construction-stage plan node.

这句话非常重要。否则，审稿人会怀疑 BnB 是否真的重新搜索了 assignments，还是仍然依赖 Sec. VI 中每个 plan node 只保存的一套 representative payload。

---

## 1.2 输出给 Sec. VIII 什么

当前 Algorithm 4 强制使用：

\[
\Pi^\star\leftarrow\Pi_{\mathrm{plan}}.
\]

但 Sec. VIII 明确说：robot becomes unavailable 后，previous assignment 可能已经失效，因此 replanning：

> is initialized without a warm start.

两者不一致。

### 推荐

将 BnB 的输入改为：

\[
\Pi_{\mathrm{seed}}
\]

这一 **optional feasible plan**。

若有 warm start：

\[
(\Pi^\star,J^\star)
=
\left(
\Pi_{\mathrm{seed}},
T(\Pi_{\mathrm{seed}})
\right).
\]

若没有：

\[
\Pi^\star=\emptyset,
\qquad
J^\star=+\infty.
\]

于是：

- initial planning：
  \[
  \Pi_{\mathrm{seed}}=\Pi_{\mathrm{plan}};
  \]
- online repair：
  \[
  \Pi_{\mathrm{seed}}=\emptyset
  \]
  或使用一个仍然有效的 repaired seed。

---

## 1.3 与 Sec. IX 的复杂度范围

Sec. IX 当前正确指出 BnB worst case 是 exponential，因为每个 edge 上的 assignment choices 会沿 plan-graph path 组合。

建议复杂度分析明确写成：

\[
N_{\mathrm{BnB}}
\]

表示实际生成的 BnB search nodes，避免只用 \(|V_P|\) 表示 BnB 规模。一个 plan node 可以对应很多不同的：

\[
(X_\mu,\Theta_\mu,C_\mu)
\]

search contexts。

---

## 1.4 与 Sec. X 的最优性结论

本节最稳妥、也最容易严格证明的结论是：

> If the retained plan graph is finite, every feasible assignment represented by its edges is enumerated, the lower bound is admissible, and the BnB frontier is exhausted, then the returned plan has minimum makespan over the accepting paths and robot assignments represented in \(G_P\).

不应直接写成：

> globally optimal for the original LTL-MRTA problem

除非 Sec. V–VI 已经另外证明：

- GBA pruning 不删除任何 global optimum；
- plan-node reuse 不合并掉任何可能属于 global optimum 的 execution context；
- greedy construction 不遗漏任何必要 structural edge；
- plan-graph simplification 保留全部 globally relevant paths。

因此，建议全文统一使用：

> optimal over the path-and-assignment space represented in \(G_P\).

---

# 2. 符号统一建议

下面的直接替换稿优先沿用当前 PDF 的主要符号：

- subtask：\(\xi\)；
- action set：\(A(\xi)\)；
- requirement：
  \[
  c(a)=(\tau(a),n(a),l(a));
  \]
- plan node：\(\nu\)。

如果你采用前几轮修改中更规范的记号，可做如下机械替换：

| 当前 PDF | 推荐的全文统一记号 |
|---|---|
| \(\xi_{ij}\) | \(\omega_{ij}\) |
| \(A(\xi)\) | \(\operatorname{Act}(\omega)\) |
| \(\tau(a)\) | \(t(a)\) |
| \(l(a)\) | \(\ell(a)\) |
| \(R_{\tau(a)}\) | \(R_{t(a)}\) |

BnB 本节内部建议统一如下。

| 当前写法 | 推荐写法 | 原因 |
|---|---|---|
| \(\mu_i=(\nu_i,X_i^b,\Theta_i^b,C_i^b)\) | \(\mu=(\nu,X_\mu,\Theta_\mu)\)，incoming assignment 作为 predecessor metadata | 避免与 plan-node payload 混淆 |
| \(C_j^b\) | \(C_{ij}\) | assignment 依赖 parent context 和 edge |
| \(J(\mu_i)\) | \(J_{\mathrm{cur}}(\mu)\) | 与 \(J_\phi\)、\(J(\nu)\)、\(J^\star\) 区分 |
| “best solution \(J^\star\)” | incumbent plan \(\Pi^\star\) and incumbent cost \(J^\star\) | plan 与 cost 不是同一对象 |
| “Upper Bound” | Greedy Rollout for Incumbent Update | 当前内容是构造 feasible incumbent |
| \(\xi_j\) | \(\xi_{ij}\) | 若 plan node 有多个 parents，subtask 更适合属于 edge |
| \(A_{\mathrm{must}}(\nu_i)\) | 保留 | 已经是正确方向 |
| \(h_a(\mu_i)\) | 保留或改成 \(\underline t_a(\mu)\) | 明确是 relaxed earliest completion estimate |
| queue \(Q\) | 保留 | standard notation |
| `Prog = acc` | 与 Sec. VI terminal condition 一致 | 不在本节重新定义 acceptance |

---

# 3. 当前版本的具体问题和修改意见

## 3.1 开头应该立即明确“搜索空间”和“最优性范围”

当前开头已经写到：

> the returned plan has the minimum makespan over the paths and assignments retained in \(G_P\).

这是正确的，但建议进一步明确：

- BnB 同时选择：
  1. one retained root-to-accepting path；
  2. one feasible assignment for each edge/subtask；
- BnB search state 的 execution state 不等于 plan node 中的 representative state；
- graph-optimality 不自动推出 original-problem global optimality。

建议把 opening paragraph 压缩成一个非常清楚的定位段，而不是重复解释 plan graph 已经完成。

---

## 3.2 Algorithm 4 出现在符号定义之前

当前排版中，Algorithm 4 在：

- BnB node；
- \(J(\mu)\)；
- \(A_{\mathrm{must}}\)；
- \(LB(\mu)\)；
- greedy rollout；

尚未完整定义之前出现。

审稿人第一次看到：

```latex
LB(\mu_0)
```

时还不知道 lower bound 的定义。

### 推荐

先按顺序定义：

1. BnB state；
2. node expansion；
3. \(A_{\mathrm{must}}\)；
4. \(LB\)；
5. rollout；
6. queue/pruning/termination；

最后给出 Algorithm 4 作为总结。

---

## 3.3 BnB search node 不应复用 plan-node payload 的符号层级

当前：

\[
\mu_i=(\nu_i,X_i^b,\Theta_i^b,C_i^b).
\]

其基本思想是对的：BnB 自己携带 execution state。

但目前文字只说 \(X_i^b,\Theta_i^b\) are carried by \(\mu_i\)，没有明确它们和：

\[
\nu_i.X,\qquad \nu_i.\Theta
\]

之间的关系。

### 建议

明确：

> \(X_\mu\) and \(\Theta_\mu\) are search-specific and need not equal the representative payload stored in \(\nu\).

assignment 更适合写成 edge/context-specific：

\[
C_{ij}:A(\xi_{ij})\rightarrow 2^R.
\]

完整 assignment history 不需要放进 tuple 中，可以通过：

\[
\operatorname{pred}(\mu_j)=\mu_i,
\qquad
C^{\mathrm{in}}(\mu_j)=C_{ij}
\]

恢复。

这样 BnB node 可简化为：

\[
\mu=(\nu,X_\mu,\Theta_\mu).
\]

---

## 3.4 propagation 必须和 Sec. VI 的 temporal semantics 一致

当前写：

> The state-update rules in Sec. VI-B1 are applied.

但建议至少在本节重申一个关键点：

\[
t_{ij}
=
\max
\left\{
J_{\mathrm{cur}}(\mu_i),
\max_{\substack{a\in A(\xi_{ij})\\r\in C_{ij}(a)}}
\left[
\theta_{\mu_i}(r)
+
\frac{d_r(x_{\mu_i}(r),l(a))}{v(r)}
\right]
\right\}.
\]

也就是说，successor subtask 的 logical completion time 不能早于 parent partial plan 的 makespan。

robots 可以提前移动或等待，但 automaton successor event 的 completion time 至少为：

\[
J_{\mathrm{cur}}(\mu_i).
\]

若 Sec. VI 仍没有这一项，Sec. VII 也会继承 temporal-order inconsistency。

---

## 3.5 \(A_{\mathrm{must}}\) 的方向正确，但需要先给 semantic definition

当前直接给 backward recursion：

\[
A_{\mathrm{must}}(\nu_i)
=
\bigcap_{(\nu_i,\nu_j)\in E_P}
\left(
A(\xi_j)\cup A_{\mathrm{must}}(\nu_j)
\right).
\]

建议先定义接受 continuation 集合：

\[
\mathcal P_{\mathrm{acc}}(\nu)
\]

为从 \(\nu\) 到 terminal accepting node 的所有 finite plan-graph paths。

随后从语义上定义：

\[
A_{\mathrm{must}}(\nu)
=
\bigcap_{P\in\mathcal P_{\mathrm{acc}}(\nu)}
\;
\bigcup_{\varepsilon\in P}
A(\xi_\varepsilon).
\]

这清楚表达：

> 一个 action 只有在每一条 accepting continuation 上至少出现一次，才进入 \(A_{\mathrm{must}}\)。

随后再给 recurrence。

### 关于重复 action

因为 \(A_{\mathrm{must}}\) 是 set，而不是 multiset，所以同一个 proposition 重复出现时只计一次。这会使 bound 更松，但不会破坏 admissibility。建议明确说明。

---

## 3.6 如果 \(G_P\) 有 cycle，不能只说“computed backward”

若 simplified plan graph 是 DAG，可以用 reverse topological order。

如果 node reuse 后仍有 cycles，则上述 equations 是 fixed-point equations。

建议补一句：

> On an acyclic accepting core, the sets are computed in reverse topological order. If structural cycles remain, the same monotone equations are solved to their greatest fixed point over the accepting core.

为什么是 greatest fixed point：它对应“所有 finite accepting continuations 的共同 action set”。如果从空集开始做 least-fixed-point iteration，在有 self-loop/exit 的图上可能得到过弱甚至错误的结果。

如果你的 implementation 实际保证 \(G_P\) 在 prefix–one-suffix representation 下是 DAG，则直接在 Sec. VI 或本节明确这一点，写法会更简单。

---

## 3.7 lower bound 需要一个正式 admissibility lemma

当前定义：

\[
LB(\mu_i)
=
\max
\left\{
J(\mu_i),
\max_{a\in A_{\mathrm{must}}(\nu_i)}
h_a(\mu_i)
\right\}
\]

是合理的，但正文没有严格解释它为什么是 lower bound。

推荐定义：

\[
J_{\mathrm{cur}}(\mu)
=
\max_{r\in R}\theta_\mu(r).
\]

对 action \(a\)，令：

\[
\underline t_k(a\mid\mu)
=
\theta_\mu(r_k)
+
\frac{d_k(x_\mu(r_k),l(a))}{v(r_k)}.
\]

令 \(h_a(\mu)\) 为 compatible robots 中第 \(n(a)\) 小的 finite value。

该估计忽略：

- future precedence constraints；
- different future actions 对同一 robot 的竞争；
- future holding constraints；
- preceding subtasks 对 robot states 的影响；
- action multiplicity。

这些 relaxation 只会让估计更小，因此：

\[
LB(\mu)
\]

不会超过任何 accepting completion 的最终 makespan。

建议在本节中加入一个简短 lemma 和 proof。否则，后面的：

\[
LB(\mu)\geq J^\star
\Rightarrow
\text{prune}
\]

缺少形式上的依据。

---

## 3.8 “Upper Bound” 应改名

当前 C 小节并没有定义一个 closed-form upper-bound function，而是描述：

> 从 child node 出发做 greedy rollout，若得到 complete feasible plan，就用其 cost 更新 incumbent。

因此标题建议改为：

```latex
C. Greedy Rollout for Incumbent Update
```

并统一使用 standard terms：

- feasible completion；
- incumbent plan；
- incumbent cost；
- rollout cost；
- upper bound。

不要使用过多自造表达，如 “completion pressure”。

---

## 3.9 rollout 不应因为优先 successor 不可赋值就立刻放弃全部同层 alternatives

当前逻辑是：

1. 根据 \(K(\nu_j)\) 选一个 successor；
2. 只对这个 successor 做 greedy assignment；
3. 如果失败，rollout 立即终止。

这样虽然不会影响 exact BnB 的 correctness，但会显著削弱 rollout 获得 upper bound 的能力。

### 推荐

在每个 rollout step：

1. 按 \(K\) 对 outgoing successors 排序；
2. 依次尝试 greedy assignment；
3. 选择第一个 assignment 成功的 successor；
4. 若所有 successors 都失败，rollout 才终止。

这几乎不改变现有 heuristic，但更稳健。

---

## 3.10 rollout 需要避免循环

若 plan graph 中存在 cycles，greedy rollout 可能无限重复。

建议：

- 在 rollout 中维护当前 predecessor chain 上的 visited plan-node/phase set；
- 若 successor 已经出现在当前 rollout chain 中，则跳过；
- 或者明确 \(G_P\) 已被构造成 finite acyclic prefix–suffix search graph。

---

## 3.11 pruning 与 termination 可以合并成一个逻辑段

当前 D 小节和 Algorithm 4 重复解释 queue、pop、prune、termination。

建议正文只保留：

- \(Q\) 按 nondecreasing \(LB\) 排序；
- 若 minimum queue key \(\geq J^\star\)，可直接停止；
- 若 queue empty 且有 incumbent，incumbent 是 graph-optimal；
- 若 queue empty 且无 incumbent，retained graph 内 infeasible；
- 若 time/memory limit，返回 incumbent 和 unresolved lower bound。

建议定义：

\[
\underline J_Q
=
\min_{\mu\in Q}LB(\mu).
\]

若被 limit 截止，可报告：

\[
J^\star-\underline J_Q
\]

或 relative gap，作为当前 solution quality certificate。

---

# 4. 推荐的章节结构

```latex
\section{Branch-and-Bound Optimization}

\subsection{Search State and Node Expansion}

\subsection{Admissible Lower Bound}

\subsection{Greedy Rollout for Incumbent Update}

\subsection{Search Order, Pruning, and Termination}
```

Algorithm 4 放在 D 小节末尾。

---

# 5. 可直接替换的英文版本

## VII. BRANCH-AND-BOUND OPTIMIZATION

```latex
\section{Branch-and-Bound Optimization}

After the plan graph has been constructed and simplified, the
construction-stage plan $\Pi_{\mathrm{plan}}$ provides a feasible
warm start but need not be optimal. We therefore apply a
branch-and-bound (BnB) search that jointly selects an accepting
root-to-terminal path retained in $G_P$ and a feasible robot
assignment for every subtask on that path. The objective is the
makespan $J_\phi$ defined in Sec.~III.

Let $\Pi_{\mathrm{seed}}$ denote an optional feasible warm-start
plan. For initial planning, we set
$\Pi_{\mathrm{seed}}=\Pi_{\mathrm{plan}}$. For repair after robot
unavailability, the seed may be empty if the previous plan is no
longer feasible. The incumbent is initialized as
\[
(\Pi^\star,J^\star)
=
\begin{cases}
\bigl(\Pi_{\mathrm{seed}},T(\Pi_{\mathrm{seed}})\bigr),
&
\Pi_{\mathrm{seed}}\neq\emptyset,\\
(\emptyset,+\infty),
&
\Pi_{\mathrm{seed}}=\emptyset.
\end{cases}
\]

The BnB search is exact with respect to the accepting paths and
robot assignments represented in $G_P$. This statement does not
imply global optimality for the original LTL-MRTA problem unless
the preceding automaton pruning and plan-graph construction are
also shown to preserve a globally optimal execution.
```

---

## A. Search State and Node Expansion

```latex
\subsection{Search State and Node Expansion}

A BnB search node is represented by
\[
\mu=(\nu,X_\mu,\Theta_\mu),
\]
where $\nu\in V_P$ is the current plan node,
\[
X_\mu=(x_\mu(r_1),\ldots,x_\mu(r_{n_r}))
\]
contains the robot positions carried by the current search state,
and
\[
\Theta_\mu=(\theta_\mu(r_1),\ldots,\theta_\mu(r_{n_r}))
\]
contains their completion times. The current makespan is
\[
J_{\mathrm{cur}}(\mu)
=
\max_{r_k\in R}\theta_\mu(r_k).
\tag{8}
\]
The quantities $X_\mu$ and $\Theta_\mu$ are search-specific and
need not equal the representative execution state stored in the
construction-stage plan node $\nu$.

Each non-root BnB node also stores a predecessor pointer, the
incoming plan-graph edge, and the assignment used on that edge.
These records are used only to recover the complete plan and
need not be included in the search-state tuple.

Consider a BnB node
$\mu_i=(\nu_i,X_{\mu_i},\Theta_{\mu_i})$ and a plan-graph edge
\[
\varepsilon_{ij}=(\nu_i,\nu_j)\in E_P.
\]
Let $\xi_{ij}$ denote the subtask associated with this edge; in
the current node-labeled implementation, $\xi_{ij}$ is the
subtask stored in $\nu_j$. For this edge, the search enumerates
all assignment maps
\[
C_{ij}:A(\xi_{ij})\rightarrow 2^R
\]
that satisfy the robot-type, cardinality, within-subtask
disjointness, reachability, and holding-condition constraints
defined in Secs.~III and~VI.

For every feasible $C_{ij}$, the robot state is propagated using
the same motion and synchronization model as in Sec.~VI. In
particular, the logical completion time of the successor subtask
is
\[
t_{ij}
=
\max
\left\{
J_{\mathrm{cur}}(\mu_i),
\max_{\substack{
a\in A(\xi_{ij})\\
r_k\in C_{ij}(a)
}}
\left[
\theta_{\mu_i}(r_k)
+
\frac{d_k(x_{\mu_i}(r_k),l(a))}{v(r_k)}
\right]
\right\}.
\tag{9}
\]
Thus, robots may move or wait concurrently, but the successor
transition cannot complete before the partial plan represented by
$\mu_i$. Updating the assigned robots' positions and completion
times produces a child search node
\[
\mu_j=(\nu_j,X_{\mu_j},\Theta_{\mu_j}).
\]
The node $\mu_i$, edge $\varepsilon_{ij}$, and assignment
$C_{ij}$ are stored as the predecessor record of $\mu_j$.
```

---

## B. Admissible Lower Bound

```latex
\subsection{Admissible Lower Bound}

The lower bound combines the realized makespan of the partial
plan with relaxed completion-time estimates for actions that are
unavoidable in every accepting continuation.

Let $\mathcal P_{\mathrm{acc}}(\nu)$ denote the set of finite
plan-graph paths from $\nu$ to a terminal plan node with
$\mathrm{Prog}=\mathrm{acc}$. The unavoidable action set is
defined semantically as
\[
A_{\mathrm{must}}(\nu)
=
\bigcap_{P\in\mathcal P_{\mathrm{acc}}(\nu)}
\;
\bigcup_{\varepsilon\in P} A(\xi_\varepsilon).
\tag{10}
\]
Hence, an action is included only if it occurs on every
accepting continuation from $\nu$. Action multiplicities are
ignored, which may weaken the bound but does not compromise
its admissibility.

For a terminal accepting node,
\[
A_{\mathrm{must}}(\nu)=\emptyset.
\]
On an acyclic accepting core, the remaining sets are computed
in reverse topological order using
\[
A_{\mathrm{must}}(\nu_i)
=
\bigcap_{(\nu_i,\nu_j)\in E_P}
\left(
A(\xi_{ij})
\cup
A_{\mathrm{must}}(\nu_j)
\right).
\tag{11}
\]
If structural cycles remain in $G_P$, the same monotone
equations are solved to their greatest fixed point over the
accepting core.

For an action $a\in A_{\mathrm{must}}(\nu)$ with
\[
c(a)=(\tau(a),n(a),l(a)),
\]
define the relaxed arrival time of a compatible robot $r_k$ as
\[
\underline t_k(a\mid\mu)
=
\theta_\mu(r_k)
+
\frac{d_k(x_\mu(r_k),l(a))}{v(r_k)}.
\tag{12}
\]
Let $h_a(\mu)$ be the $n(a)$-th smallest finite value among
the compatible robots in $R_{\tau(a)}$. If fewer than $n(a)$
compatible robots can reach $l(a)$, set
\[
h_a(\mu)=+\infty.
\]
The lower bound is
\[
LB(\mu)
=
\max
\left\{
J_{\mathrm{cur}}(\mu),
\max_{a\in A_{\mathrm{must}}(\nu)}
h_a(\mu)
\right\},
\tag{13}
\]
where the second term is omitted when
$A_{\mathrm{must}}(\nu)=\emptyset$.

\textbf{Lemma 4 (Admissibility of the lower bound).}
For every BnB node $\mu$, $LB(\mu)$ does not exceed the
makespan of any feasible accepting completion rooted at $\mu$.

\emph{Proof.}
Every accepting completion has makespan at least
$J_{\mathrm{cur}}(\mu)$. Moreover, each
$a\in A_{\mathrm{must}}(\nu)$ must be completed at least once
on every accepting continuation. The value $h_a(\mu)$ estimates
the earliest possible completion of $a$ while ignoring future
precedence constraints, competition among different future
actions for the same robots, and the robot-state changes induced
by preceding subtasks. These relaxations cannot increase the
estimate. Therefore, the makespan of any accepting completion
is no smaller than every term in (13), and hence no smaller than
$LB(\mu)$. \hfill$\square$
```

---

## C. Greedy Rollout for Incumbent Update

```latex
\subsection{Greedy Rollout for Incumbent Update}

Whenever a feasible child BnB node is generated, a greedy
rollout is attempted to obtain a complete feasible plan and
tighten the incumbent cost. The rollout is an upper-bound
heuristic only; it is not used to prune exact BnB branches and
does not provide an optimality certificate.

Consider a rollout node $\mu_i$ and an outgoing edge
$\varepsilon_{ij}=(\nu_i,\nu_j)$. The normalized demand of
its immediate subtask is
\[
D(\xi_{ij})
=
\sum_{a\in A(\xi_{ij})}
\frac{n(a)}{|R_{\tau(a)}|}.
\tag{14}
\]
The total normalized demand associated with this continuation
is
\[
W(\varepsilon_{ij})
=
\sum_{a\in
A(\xi_{ij})\cup A_{\mathrm{must}}(\nu_j)}
\frac{n(a)}{|R_{\tau(a)}|}.
\tag{15}
\]
If $|R_{\tau(a)}|=0$ for a required action, the corresponding
edge is infeasible for the active team.

The rollout orders the outgoing edges lexicographically by
\[
K(\varepsilon_{ij})
=
\bigl(
W(\varepsilon_{ij}),
-D(\xi_{ij})
\bigr).
\tag{16}
\]
The first component favors continuations with smaller mandatory
robot demand. Among equal values, the second component gives
priority to the more resource-demanding immediate subtask,
thereby scheduling scarce-resource requirements earlier.

The outgoing edges are tested in this order until a greedy
feasible assignment is found. The corresponding child becomes
the next rollout node. If no outgoing edge admits a greedy
assignment, the rollout fails without changing the incumbent.
The rollout also terminates if it would revisit a plan node on
its current predecessor chain. If it reaches a terminal accepting
node with makespan $J_{\mathrm{roll}}<J^\star$, the incumbent is
updated to the recovered rollout plan and cost. The priority rule
in (16) affects only the rollout and is not used for BnB
pruning.
```

---

## D. Search Order, Pruning, and Termination

```latex
\subsection{Search Order, Pruning, and Termination}

The open set is maintained as a priority queue $Q$ ordered by
nondecreasing lower bound. At each iteration, the node with the
smallest value of $LB$ is selected. A node is discarded when
\[
LB(\mu)\geq J^\star,
\]
because no accepting completion rooted at $\mu$ can improve
the incumbent. A child is not generated if its next subtask
admits no feasible robot assignment.

If $Q$ becomes empty, or if its smallest key is no smaller
than $J^\star$, no unexplored BnB node can improve the
incumbent. The returned plan is then optimal over the accepting
paths and robot assignments represented in $G_P$. If no
incumbent exists when the queue becomes empty, no feasible
plan is represented in the retained graph.

If a user-specified runtime or memory limit is reached first,
the algorithm returns the best feasible incumbent found so far.
Let
\[
\underline J_Q
=
\min_{\mu\in Q}LB(\mu)
\]
be the smallest lower bound remaining in the queue. When an
incumbent exists, $J^\star-\underline J_Q$ provides an
unresolved absolute optimality gap within the retained graph.
```

---

# 6. 修改后的 Algorithm 4

```latex
\begin{algorithm}[t]
\caption{Warm-Started BnB on the Retained Plan Graph}
\label{alg:bnb}
\begin{algorithmic}[1]
\Require Plan graph $G_P=(V_P,E_P)$; root execution
context $(\nu_{\mathrm r},X_{\mathrm r},\Theta_{\mathrm r})$;
active robot team $R$; optional feasible plan
$\Pi_{\mathrm{seed}}$; runtime/memory limits.
\Ensure Incumbent plan $\Pi^\star$, incumbent cost
$J^\star$, and search status.
\If{$\Pi_{\mathrm{seed}}\neq\emptyset$}
    \State $(\Pi^\star,J^\star)
    \gets
    (\Pi_{\mathrm{seed}},T(\Pi_{\mathrm{seed}}))$.
\Else
    \State $(\Pi^\star,J^\star)\gets(\emptyset,+\infty)$.
\EndIf
\State Precompute $A_{\mathrm{must}}(\nu)$ for all
$\nu\in V_P$.
\State $\mu_0\gets
(\nu_{\mathrm r},X_{\mathrm r},\Theta_{\mathrm r})$.
\State Attempt a greedy rollout from $\mu_0$ and update
$(\Pi^\star,J^\star)$ if successful.
\State Insert $\mu_0$ into a priority queue $Q$ with key
$LB(\mu_0)$.
\While{$Q\neq\emptyset$ and no user-specified limit is reached}
    \If{$\min_{\mu\in Q}LB(\mu)\geq J^\star$}
        \State \Return
        $(\Pi^\star,J^\star,\textsc{Optimal-In-Graph})$.
    \EndIf
    \State $\mu_i\gets\textsc{PopMin}(Q)$.
    \If{$\nu_i.\mathrm{Prog}=\mathrm{acc}$}
        \If{$J_{\mathrm{cur}}(\mu_i)<J^\star$}
            \State Recover the predecessor chain and update
            $(\Pi^\star,J^\star)$.
        \EndIf
        \State \textbf{continue}.
    \EndIf
    \ForAll{$\varepsilon_{ij}=(\nu_i,\nu_j)\in E_P$}
        \ForAll{$C_{ij}\in
        \textsc{FeasibleAssignments}
        (\mu_i,\varepsilon_{ij},R)$}
            \State $\mu_j\gets
            \textsc{Propagate}(\mu_i,\varepsilon_{ij},C_{ij})$.
            \State Store $\mu_i$, $\varepsilon_{ij}$, and
            $C_{ij}$ as the predecessor record of $\mu_j$.
            \If{$LB(\mu_j)\geq J^\star$}
                \State \textbf{continue}.
            \EndIf
            \State
            $(\Pi_{\mathrm{roll}},J_{\mathrm{roll}})
            \gets
            \textsc{GreedyRollout}(\mu_j,G_P,R)$.
            \If{$\Pi_{\mathrm{roll}}\neq\emptyset$
            and $J_{\mathrm{roll}}<J^\star$}
                \State
                $(\Pi^\star,J^\star)
                \gets
                (\Pi_{\mathrm{roll}},J_{\mathrm{roll}})$.
            \EndIf
            \If{$LB(\mu_j)<J^\star$}
                \State Insert $\mu_j$ into $Q$ with key
                $LB(\mu_j)$.
            \EndIf
        \EndFor
    \EndFor
\EndWhile
\If{a user-specified limit was reached}
    \State \Return
    $(\Pi^\star,J^\star,\textsc{Limit-Reached})$.
\ElsIf{$\Pi^\star=\emptyset$}
    \State \Return
    $(\emptyset,+\infty,\textsc{Infeasible-In-Graph})$.
\Else
    \State \Return
    $(\Pi^\star,J^\star,\textsc{Optimal-In-Graph})$.
\EndIf
\end{algorithmic}
\end{algorithm}
```

---

# 7. 建议增加的 BnB 最优性结论

建议不要把这一结论混在整个 framework 的 soundness/completeness theorem 中，而是在 Sec. VII 或 Sec. X 单独给出。

```latex
\textbf{Theorem 2 (Optimality within the retained plan graph).}
Assume that the accepting search space represented by $G_P$
is finite, every feasible assignment for each retained
plan-graph edge is enumerated, and the lower bound in (13) is
admissible. If Algorithm~\ref{alg:bnb} terminates without a
runtime or memory limit, then the returned plan has minimum
makespan over all accepting paths and robot assignments
represented in $G_P$.

\emph{Proof.}
The incumbent is updated only by complete feasible plans, so
$J^\star$ is always a valid upper bound. By Lemma~4,
$LB(\mu)$ is no greater than the cost of any accepting
completion rooted at $\mu$. Hence, a node is pruned only when
none of its completions can improve the incumbent. Since all
remaining feasible children are eventually inserted into the
priority queue and the represented search space is finite, every
candidate that could improve the incumbent is either explored
or safely pruned. When the queue is empty or its smallest key is
no smaller than $J^\star$, no unexamined completion has lower
cost. Therefore, the incumbent is optimal over the search space
represented in $G_P$. \hfill$\square$
```

随后加一句边界说明：

```latex
The theorem is graph-relative. Equality with the global optimum
of Problem~1 additionally requires that the preceding GBA
pruning and plan-graph construction preserve at least one
globally optimal execution.
```

---

# 8. 当前版本哪些内容应删除或压缩

## 8.1 删除重复的 queue 描述

Algorithm 和 D 小节不需要分别逐句重复：

- queue stores nodes；
- sorted by LB；
- pop minimum；
- prune if LB exceeds incumbent。

正文说明原则，Algorithm 展示过程即可。

## 8.2 删除 “Upper Bound” 中过长的文献动机

当前先讲 resource-constrained project scheduling，再讲 priority-rule heuristics，随后才进入自己的 \(D/W/K\)。

建议压缩成一句：

> Motivated by resource-aware priority rules, the rollout orders successors using their immediate and unavoidable downstream robot demand.

避免让读者以为这里提出了一个新的 scheduling formulation。

## 8.3 不要再次解释 Problem 1 的 objective

开头写：

> The objective is the makespan defined in Sec. III.

即可，不需要重新引入新 cost notation。

---

# 9. 与 Sec. VIII 的同步修改

推荐把 Sec. VIII 中相关部分改成：

```latex
The same BnB procedure is invoked on the retained plan graph
using the current execution progress as the new root context and
the remaining robots as the active team. If robot unavailability
invalidates the previous plan, the search is initialized without
an incumbent:
\[
\Pi_{\mathrm{seed}}=\emptyset,
\qquad
J^\star=+\infty.
\]
A greedy rollout from the runtime root is attempted first to
obtain a repaired incumbent quickly, after which exact BnB
refinement continues over the retained graph.
```

如果 retained graph 中没有 continuation，只能写：

> infeasible in the retained plan graph

除非你的方法还会恢复 on-the-fly NBA/plan-graph generation。

---

# 10. 与 Sec. IX Complexity Analysis 的同步修改

建议写清：

1. \(A_{\mathrm{must}}\)：
   - DAG：bitset backward DP；
   - cyclic graph：fixed-point iteration。
2. BnB branching factor：
   \[
   |\mathcal C_{ij}|
   \leq
   \prod_{a\in A(\xi_{ij})}
   \binom{|R_{\tau(a)}|}{n(a)},
   \]
   这是忽略 assignment disjointness 后的上界。
3. 总时间依赖实际生成的 BnB nodes：
   \[
   N_{\mathrm{BnB}}.
   \]
4. priority-queue operation：
   \[
   O(\log |Q|).
   \]
5. rollout 是 heuristic，不枚举所有 combinations。

---

# 11. 与 Sec. XI-A 实验图的同步修改

当前 Fig. 4 建议明确区分：

- \(J^\star(k)\)：第 \(k\) 次 iteration 后的 incumbent upper bound；
- \(\underline J_Q(k)\)：open queue 中的最小 lower bound；
- selected-node \(LB(\mu_k)\)：当前被展开 node 的 lower bound。

如果论文只画一个 “LB” 曲线，最有意义的是：

\[
\underline J_Q(k)
=
\min_{\mu\in Q_k}LB(\mu),
\]

因为它与 \(J^\star\) 一起构成 graph-relative optimality gap。

建议 caption 改成类似：

```latex
Evolution of the incumbent cost $J^\star$ and the minimum
open-node lower bound $\underline J_Q$ during BnB search.
Their difference is the unresolved optimality gap over the
search space represented in $G_P$.
```

若实验在 limit 前没有满足：

\[
\underline J_Q\geq J^\star,
\]

则不要称结果为 certified optimum，只称 best incumbent。

---

# 12. 如果暂时不修改代码的最小改动版本

如果代码仍然：

- 强制使用 \(\Pi_{\mathrm{plan}}\)；
- rollout 只尝试一个 successor；
- 不处理 graph cycles；
- 不输出 status/gap；

至少应完成以下文字修改：

1. 明确 BnB 只保证 retained \(G_P\) 内最优；
2. 明确 \(X_i^b,\Theta_i^b\) 是 BnB-specific；
3. 将 \(C_j^b\) 改成 edge/context-specific \(C_{ij}^b\)；
4. 给 \(A_{\mathrm{must}}\) 增加 semantic definition；
5. 给 lower bound 增加 admissibility proof；
6. 将 `Upper Bound` 改成 `Greedy Rollout`;
7. 明确 rollout failure 不表示该 BnB branch infeasible；
8. Sec. VIII 另行调用一个 no-warm-start initialization：
   \[
   (\Pi^\star,J^\star)=(\emptyset,+\infty);
   \]
9. 若 graph 有 cycles，增加 rollout depth/visited check；
10. 把 global-optimal wording 改成 graph-relative optimality。

---

# 13. 最终推荐的逻辑主线

修改后的 Sec. VII 应让审稿人快速形成下面的理解：

\[
(G_P,\Pi_{\mathrm{plan}})
\]

\[
\Downarrow
\]

\[
\text{initialize feasible incumbent}
\]

\[
\Downarrow
\]

\[
\text{enumerate retained path edges and exact feasible assignments}
\]

\[
\Downarrow
\]

\[
\text{propagate search-specific robot states}
\]

\[
\Downarrow
\]

\[
\text{prune only with an admissible }LB
\]

\[
\Downarrow
\]

\[
\text{use greedy rollout only to tighten }J^\star
\]

\[
\Downarrow
\]

\[
\text{exhausted frontier}
\Rightarrow
\text{optimal in }G_P
\]

\[
\text{resource limit}
\Rightarrow
\text{best incumbent + remaining gap}.
\]

这条主线比当前 “Node Expansion—Lower Bound—Upper Bound—Branching” 的表面并列关系更清楚：lower bound 负责安全 pruning，rollout 只负责改善 incumbent，priority queue 负责搜索次序，三者的 correctness roles 彼此独立。
