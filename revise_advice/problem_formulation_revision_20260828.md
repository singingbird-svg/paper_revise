# Problem Formulation（问题描述）检查与修改方案

## 0. 总体结论

我对照检查了当前论文的 Sec. II **Preliminaries**、Sec. III **Problem Description**、后续 Secs. V–VIII 对相关符号的实际使用，以及参考论文 *Temporal Logic Task Allocation in Heterogeneous Multirobot Systems* 的 Problem Definition/Assumptions 写法。

当前问题描述的基本结构是合理的：

1. Workspace and Heterogeneous Robot Team；
2. Task Specification；
3. Problem Definition。

但从审稿人的角度看，仍有四类需要优先处理的问题：

1. **符号与前文及后文存在冲突或类型不一致；**
2. **NBA 在 Preliminaries 和 Problem Definition 中被重复定义；**
3. **你希望加入的两项内容不能直接照搬参考论文，需要转换成适合本文模型的假设；**
4. **“robot path \(\tau\) satisfies \(\phi\)”需要区分物理执行路径、自动机 accepting run 和 proposition word，否则 formal semantics 不够严谨。**

最推荐的组织方式是将本节改名为：

```latex
\section{Problem Formulation}
```

并调整为：

```text
A. Workspace and Heterogeneous Robot Team
B. Task Specification
C. Feasible Plans and Optimization Problem
D. Assumptions
```

这种结构借鉴了参考论文“先建模—再定义任务—再给出问题—最后集中声明假设”的优点，但不照搬其 Transition System、induced proposition、restricted accepting run 等不适用于你论文的方法细节。

---

# 1. 与前文和后文对应的符号检查

## 1.1 `T` 同时表示 robot-type set 和 plan completion time

当前 Sec. III-A 中：

\[
T=\{1,2,\ldots,n_t\}
\]

表示机器人类型集合。

但 Sec. III-C 中又使用：

\[
T(\Pi)
\]

表示计划完成时间。

虽然上下文能够区分，但 formal paper 中不建议同一个大写字母同时表示集合和函数。

### 推荐

将 robot-type set 改为：

\[
\mathcal T=\{1,2,\ldots,n_t\}.
\]

保留 \(T(\Pi)\) 表示 makespan。

这样后文所有：

```latex
\tau_i \in T
```

应相应改为：

```latex
t(a_i)\in\mathcal T
```

或简写为 \(t_i\in\mathcal T\)。

---

## 1.2 当前的 type map `\tau(r_k)` 与你希望新增的 path `\tau` 冲突

当前写法：

\[
\tau(r_k)\in T
\]

表示机器人 \(r_k\) 的类型。

但你希望增加：

> a path \(\tau\) that satisfies \(\phi\)

如果二者同时保留，`\tau` 既表示 type map，又表示 team path，读者很容易混淆。

### 推荐

把机器人类型映射改成：

\[
\kappa:R\rightarrow\mathcal T,
\]

其中 \(\kappa(r_k)\) 是机器人 \(r_k\) 的类型，并定义：

\[
R_j:=\{r_k\in R\mid \kappa(r_k)=j\}.
\]

将 `\tau` 专门保留给 team execution/path。

这是为了加入第二个假设必须进行的符号调整。

---

## 1.3 不建议直接从范文复制 `A_\phi=(V,E)`

参考论文将 NBA 作为图记为：

\[
A_\phi=(V,E).
\]

但你的论文已经在 Sec. II 中使用：

\[
B_\phi=(Q_B,q_{B,0},\Sigma,\rightarrow_B,Q_{B,F})
\]

表示 NBA，同时在 Sec. III-B 中使用 \(A\) 表示 action-proposition set。

因此直接引入 \(A_\phi\) 会造成两个问题：

1. 同一个自动机同时用 \(A_\phi\) 和 \(B_\phi\) 表示；
2. \(A\) 已经表示 action set，\(A_\phi\) 视觉上容易与其混淆。

### 最推荐的处理方式

保留前文已经定义的 \(B_\phi\)，并在需要强调 graph structure 时写：

\[
\mathcal G(B_\phi)=(Q_B,E_B),
\]

其中

\[
E_B:=
\left\{
(q_{B,i},q_{B,j})
\;\middle|\;
\exists\,\gamma_{ij}:
q_{B,i}\xrightarrow{\gamma_{ij}}q_{B,j}
\right\}.
\]

这样既表达了参考论文中“在 NBA graph 上寻找 accepting path”的思想，又不引入新的 automaton notation。

---

## 1.4 LTL2BA 的引用编号不能照搬 `[44]`

参考论文中 LTL2BA 是文献 [44]。

但在你当前论文中：

- LTL2BA/Gastin–Oddoux 是 **[13]**；
- [44] 是 TurtleBot hardware reference。

因此你的正文中不能写：

> constructed using LTL2BA developed by [44]

而应使用你自己的 BibTeX citation key；在当前编译版本中对应：

> constructed using LTL2BA [13].

这是一个必须修正的引用编号问题。

---

## 1.5 `\sigma_k` 与 `\sigma_{ij}` 的问题需要延续前一部分修改

如果采用上一轮 Preliminaries 的推荐记号：

- \(\sigma_k\in\Sigma\)：input word 在第 \(k\) 步的 valuation；
- \(\gamma_{ij}\)：symbolic transition guard；

那么 Problem Formulation 中也应统一使用：

\[
q_{B,i}\xrightarrow{\gamma_{ij}}q_{B,j},
\qquad
\omega_{ij}=(\gamma_{ij},\gamma_i^{\mathrm{hold}}).
\]

不建议继续用 \(\sigma_{ij}\) 表示 transition guard，因为这会再次与 word letter \(\sigma_k\) 混淆。

下面的完整替换稿按照 `\gamma` 记号编写。

---

## 1.6 `c(a_i)=(\tau_i,n_i,l_i)` 的索引容易误导

当前写法：

\[
c(a_i)=(\tau_i,n_i,l_i)
\]

容易让读者误以为 action \(a_i\) 必然对应 region \(l_i\)。

但你的 Example 1 中：

\[
c(a_2)=(2,1,l_6),
\]

显然 action index 和 region index 并不对应。

### 推荐

使用函数式记号：

\[
c(a)=\bigl(t(a),n(a),\ell(a)\bigr),
\]

其中：

- \(t(a)\in\mathcal T\)：required type；
- \(n(a)\in\mathbb N_{>0}\)：required number；
- \(\ell(a)\in L\)：target region。

该写法在后续 greedy assignment、score、BnB lower bound 中也更清楚。

---

## 1.7 `G_{r,k}` 当前没有在后文真正使用

Sec. III-A 定义：

\[
G_{r,k}=(V_{r,k},\rightarrow_{r,k}),
\]

但后续算法实际只使用：

\[
d_k(x,l_i)
\]

判断 reachability 和计算 arrival time。

因此 \(G_{r,k}\) 在当前版本中属于“定义了但没有继续使用”的符号。

### 推荐

正文中直接删除 \(G_{r,k}\)，并说明 robot-specific motion constraints 已经包含在 \(d_k\) 中：

> Robot-specific kinematic, obstacle, and traversability constraints are incorporated into \(d_k\).

如果你确实需要保留 transition graph，则至少应改成：

\[
\mathcal G_k=(V_k,E_k),
\]

而不是 \(G_{r,k}\)，因为下标 \(r,k\) 对 robot \(r_k\) 是重复的。

---

## 1.8 `x_i(r_k)` 后文被设为 region label，存在类型不一致

Sec. III-A 中：

\[
x(r_k)\in W
\]

表示一个 workspace position。

但后文 Example 4 中出现：

\[
x_1(r_k)=l_5,
\]

右侧是 region，而不是 position。

### 两种可选修正

#### 方案 A（推荐）

令 \(x_i(r_k)\in W\) 始终表示位置，并为 robot-region pair 定义 service point：

\[
y_k(l_i)\in l_i.
\]

任务完成后更新为：

\[
x_{i+1}(r_k)=y_k(l_i),
\]

而不是 \(x_{i+1}(r_k)=l_i\)。

#### 方案 B

如果你的 high-level planner 只存储 region-level location，则把 \(x_i(r_k)\) 改成：

\[
\ell_i(r_k)\in L\cup\{\text{initial positions}\},
\]

但这样需要重写距离函数。

从当前 \(d_k(x,l_i)\) 的定义和物理实验中的 target points 看，方案 A 更自然。

---

## 1.9 NBA 不应在 Sec. III-C 再定义一次

Sec. II 已经完整定义 \(B_\phi\)，但 Sec. III-C 又重新给出 tuple 及每个 component。

建议将整段：

> Consider an LTL formula... Let \(B_\phi=(\cdots)\)... Here \(Q_B\) is...

压缩为：

```latex
Consider an LTL formula $\phi$ over $AP$, and let $B_\phi$
denote the corresponding NBA defined in Sec.~II-A. To connect
automaton progress with robot planning, we associate each
symbolic NBA transition with a subtask.
```

---

# 2. 如何专业地加入第一个假设

你希望加入：

> Regions do not overlap and each region spans consecutive cells.

## 2.1 “consecutive cells” 不是标准 formal term

更专业的表述是：

> each region is represented by a connected set of adjacent free cells.

也就是使用 **connected**，而不是 `consecutive`。

## 2.2 不能直接照搬参考论文的全部 workspace assumption

参考论文还要求：

> there exists a label-free path between any two regions...

但你的当前模型明确允许：

\[
d_k(x,l_i)=+\infty
\]

表示某个 region 对某个 robot 不可达。

如果再假设任意 region 都连通，就会削弱甚至冲突于你的 robot-specific reachability model。

### 最适合本文的假设

```latex
\textbf{Assumption 1 (Workspace regularity).}
The regions of interest are pairwise disjoint and do not
intersect obstacle or forbidden regions. Under the finite
workspace discretization used for motion planning, each
region is represented by a nonempty connected set of adjacent
free cells.
```

随后解释：

> This assumption ensures that each region represents a single connected semantic location. Global connectivity between arbitrary regions is not required; robot-specific unreachability is represented by \(d_k(x,l_i)=+\infty\).

这样既满足你希望加入的内容，又保留本文比范文更一般的 robot-specific reachability。

---

# 3. 如何专业地加入第二个假设

你希望加入：

> can find a path \(\tau\) that satisfies \(\phi\) by operating on the corresponding NBA \(A_\phi=(V,E)\), which can be constructed using LTL2BA.

这句话中有三层概念需要区分。

## 3.1 “LTL2BA 可以构造 NBA”不是假设

由 LTL-to-NBA translation 可知：

\[
L(B_\phi)=\mathrm{Words}(\phi).
\]

这是 standard automata-theoretic result，不应写成 assumption。

## 3.2 真正需要假设的是“存在 physically realizable accepting execution”

一个 accepting run 只说明 logical satisfiability；它未必能由当前 robot team 执行。

因此真正适合你的假设应同时要求：

1. \(B_\phi\) 中存在 accepting prefix–suffix run；
2. 该 run 诱导的 action requirements 可以分配给当前 heterogeneous team；
3. 对应 target regions 对 assigned robots 可达；
4. induced team execution 的 proposition word 满足 \(\phi\)。

## 3.3 区分三个对象

建议使用：

- \(\rho\)：NBA accepting run；
- \(\tau\)：physical team execution（robot paths + action events）；
- \(w(\tau)\)：execution induced proposition word。

满足关系为：

\[
w(\tau)\in L(B_\phi)=\mathrm{Words}(\phi),
\]

等价于：

\[
w(\tau)\models\phi.
\]

### 最推荐的假设

```latex
\textbf{Assumption 2 (Existence of a feasible accepting execution).}
For the initial planning instance, there exists an accepting
prefix--suffix run $\rho$ of the NBA $B_\phi$ generated by
LTL2BA~[13] and a corresponding team execution $\tau$ such
that $w(\tau)\in L(B_\phi)=\mathrm{Words}(\phi)$. Moreover,
the action requirements induced by $\rho$ admit type-compatible,
pairwise-disjoint robot assignments, and every assigned robot
can reach its required target region along a finite feasible path.
```

也可以用 feasible-plan set 写得更简洁：

\[
\mathfrak P_\phi\neq\emptyset.
\]

### 关于 online robot failure

建议补充一句：

> Assumption 2 concerns the initial planning instance. After the available team changes, the replanning procedure may report infeasibility if no feasible continuation exists for the remaining robots.

这样不会让审稿人误以为你假设“任何 failure 后都一定可修复”。

---

# 4. 推荐的章节结构

```latex
III. PROBLEM FORMULATION

A. Workspace and Heterogeneous Robot Team
B. Task Specification
C. Feasible Plans and Optimization Problem
D. Assumptions
```

这种结构和参考论文的优点一致：

- 先给出 system/task objects；
- 再定义 optimization problem；
- 最后把 completeness/soundness 所依赖的 assumptions 集中列出。

但不复制参考论文中的：

- cell-level transition system；
- product transition system；
- induced atomic propositions；
- restricted accepting runs；
- label-free all-pairs connectivity。

这些内容并不服务你的 on-the-fly GBA/NBA framework，加入后反而会增加冗余。

---

# 5. 最推荐的完整英文替换稿

下面版本按前一轮推荐的统一记号编写：

- robot type set：\(\mathcal T\)；
- robot type map：\(\kappa\)；
- word letter：\(\sigma_k\)；
- symbolic transition guard：\(\gamma_{ij}\)；
- NBA：沿用 \(B_\phi\)，不另引入 \(A_\phi\)。

---

## III. PROBLEM FORMULATION

```latex
\section{Problem Formulation}

This section introduces the workspace and heterogeneous robot
team, defines the atomic propositions used in the temporal-logic
specification, and formulates the LTL-based multi-robot task
allocation problem. The assumptions used in the subsequent
planning and theoretical analysis are stated at the end of the
section.

\subsection{Workspace and Heterogeneous Robot Team}

Consider a bounded workspace $W\subset\mathbb{R}^{2}$ containing
a finite set of regions of interest
\[
L=\{l_1,l_2,\ldots,l_{n_l}\}
\]
and a finite set of obstacle or forbidden regions
\[
O=\{o_1,o_2,\ldots,o_{n_o}\}.
\]
The geometric regularity of these regions is stated in
Assumption~1.

A heterogeneous robot team is denoted by
\[
R=\{r_1,r_2,\ldots,r_{n_r}\}.
\]
The robots belong to a finite type set
\[
\mathcal T=\{1,2,\ldots,n_t\},
\]
where each type represents a task-relevant capability, such as
sensing, manipulation, or mobility. Each robot belongs to
exactly one type. Let
\[
\kappa:R\rightarrow\mathcal T
\]
denote the robot-type map, and define
\[
R_j:=\{r_k\in R\mid \kappa(r_k)=j\}
\]
as the set of robots of type $j\in\mathcal T$.

The current position and constant travel speed of robot $r_k$
are denoted by $x(r_k)\in W$ and $v(r_k)>0$, respectively.
For any feasible robot position $x\in W$ and target region
$l_i\in L$, let
\[
d_k(x,l_i)\in[0,+\infty]
\]
denote the length of a shortest collision-free path by which
robot $r_k$ can reach $l_i$ from $x$. Robot-specific motion,
obstacle, and traversability constraints are incorporated into
$d_k$. We set $d_k(x,l_i)=+\infty$ if $l_i$ is unreachable
by $r_k$.
```

### 说明

这一版删除了当前没有被后文使用的：

```latex
G_{r,k}=(V_{r,k},\rightarrow_{r,k}).
```

如果你后续确实需要这个 graph，则可以恢复为：

```latex
\mathcal G_k=(V_k,E_k),
```

但应在后续至少引用一次。

---

## B. Task Specification

```latex
\subsection{Task Specification}

The temporal-logic specification is defined over two disjoint
classes of atomic propositions. First, let
\[
P:=\{p_i\mid l_i\in L\}
\]
be the set of region propositions, where $p_i$ is true whenever
at least one available robot is located in region $l_i$.

Second, let
\[
A:=\{a_1,a_2,\ldots,a_{n_a}\}
\]
be the set of action propositions. Each action proposition
$a\in A$ is associated with an execution requirement
\[
c(a):=\bigl(t(a),n(a),l(a)\bigr),
\]
where $t(a)\in\mathcal T$ is the required robot type,
$n(a)\in\mathbb{N}_{>0}$ is the required number of robots,
and $l(a)\in L$ is the target region. The proposition $a$ is
true when a set of $n(a)$ robots of type $t(a)$ executes the
corresponding operation in $l(a)$. The identities of these
robots are not prescribed by the proposition.

The complete atomic-proposition set is
\[
AP:=P\cup A,
\qquad
P\cap A=\emptyset.
\]

\textbf{Example 1.}
Consider the warehouse workspace shown in Fig.~1, with
\[
L=\{l_1,l_2,\ldots,l_8\},
\]
and the robot team
\[
R=\{r_1,r_2,r_3,r_4,r_5\},
\]
where $r_1,r_2,r_3$ are type-1 robots and $r_4,r_5$ are
type-2 robots. Consider the specification
\[
\phi=
\Diamond\!\left(
a_1\land(\Diamond a_2\land\Diamond a_3)
\right)
\land
\Box\neg p_8,
\]
with
\[
c(a_1)=(2,2,l_5),\qquad
c(a_2)=(2,1,l_6),\qquad
c(a_3)=(1,1,l_1).
\]
The specification requires all robots to avoid the restricted
region $l_8$. It further requires two type-2 robots to perform
the collaborative inspection represented by $a_1$ at $l_5$.
Afterward, one type-2 robot must execute $a_2$ at $l_6$, and
one type-1 robot must execute $a_3$ at $l_1$.
```

### 说明

这里使用：

\[
c(a)=(t(a),n(a),l(a))
\]

代替：

\[
c(a_i)=(\tau_i,n_i,l_i),
\]

避免 action index 与 region index 被误认为一一对应。

---

## C. Feasible Plans and Optimization Problem

```latex
\subsection{Feasible Plans and Optimization Problem}

Consider an LTL formula $\phi$ over $AP$, and let $B_\phi$
denote the corresponding NBA defined in Sec.~II-A. To connect
automaton progress with robot planning, we associate each
symbolic NBA transition with a subtask.

\textbf{Definition 5 (Subtask).}
Consider a symbolic NBA transition
\[
e_{B,ij}:
q_{B,i}\xrightarrow{\gamma_{ij}}q_{B,j},
\]
where $q_{B,i},q_{B,j}\in Q_B$ and $\gamma_{ij}$ is the
transition guard. Let $\gamma_i^{\mathrm{hold}}$ denote the
holding condition associated with the selected self-loop at
$q_{B,i}$; if no holding condition is imposed, set
$\gamma_i^{\mathrm{hold}}=\top$. The subtask induced by
$e_{B,ij}$ is
\[
\omega_{ij}:=
\bigl(\gamma_{ij},\gamma_i^{\mathrm{hold}}\bigr).
\]
The guard $\gamma_{ij}$ specifies the propositions that enable
the transition to $q_{B,j}$, whereas
$\gamma_i^{\mathrm{hold}}$ specifies the propositions that must
remain satisfied while the subtask is being completed.

A plan is represented by
\[
\Pi=
\bigl(\boldsymbol{\omega},\rho,\boldsymbol{C}\bigr),
\]
where
\[
\boldsymbol{\omega}=\omega_0\omega_1\omega_2\cdots
\]
is the subtask sequence,
\[
\rho=q_0q_1q_2\cdots
\]
is the corresponding NBA-state sequence, and
\[
\boldsymbol{C}=C_0C_1C_2\cdots
\]
is the robot-assignment sequence.

For a subtask $\omega_k$, let
\[
\mathrm{Act}(\omega_k)\subseteq A
\]
denote the set of positive action propositions required by its
transition guard. The assignment
\[
C_k:\mathrm{Act}(\omega_k)\rightarrow 2^{R}
\]
must satisfy, for every $a\in\mathrm{Act}(\omega_k)$,
\[
C_k(a)\subseteq R_{t(a)},
\qquad
|C_k(a)|=n(a),
\]
and assignments to distinct action propositions in the same
subtask must be disjoint:
\[
C_k(a)\cap C_k(b)=\emptyset,
\qquad
a\neq b.
\]

Together with the robot motion paths, a plan $\Pi$ induces a
team execution $\tau_\Pi$ and an infinite proposition word
$w(\tau_\Pi)\in\Sigma^\omega$. A plan is feasible if its robot
assignments satisfy the above type, cardinality, and
disjointness requirements, all assigned robots can reach the
required regions while satisfying the holding conditions, and
\[
w(\tau_\Pi)\in L(B_\phi)=\mathrm{Words}(\phi).
\]
Let $\mathfrak P_\phi$ denote the set of all feasible plans for
$\phi$.

An accepting run has a prefix--suffix representation
\[
\rho=
\rho^{\mathrm{pre}}
\left(\rho^{\mathrm{suf}}\right)^\omega.
\]
Accordingly, the associated plan is written as
\[
\Pi=
\Pi^{\mathrm{pre}}
\left(\Pi^{\mathrm{suf}}\right)^\omega.
\]
Let
\[
\Pi^{\mathrm{fin}}
:=
\Pi^{\mathrm{pre}}\Pi^{\mathrm{suf}}
\]
denote one finite traversal of the prefix and suffix. Let
$T(\Pi^{\mathrm{fin}})$ denote its makespan, i.e., the time at
which all subtasks in $\Pi^{\mathrm{fin}}$ have been completed.
The plan cost is
\[
J_\phi(\Pi):=T(\Pi^{\mathrm{fin}}).
\]

\textbf{Problem 1 (LTL-MRTA).}
Given the workspace $W$, the region and obstacle sets $L$ and
$O$, a heterogeneous robot team $R$ with type set
$\mathcal T$, and an LTL formula $\phi$ over
$AP=P\cup A$, determine
\[
\Pi^\star
\in
\arg\min_{\Pi\in\mathfrak P_\phi}
J_\phi(\Pi).
\]
That is, the objective is to find a feasible prefix--suffix plan,
together with its robot assignments and induced team execution,
that satisfies $\phi$ and minimizes the makespan.
```

---

## D. Assumptions

```latex
\subsection{Assumptions}

The following assumptions specify the workspace regularity and
the feasibility scope considered in the subsequent theoretical
analysis.

\textbf{Assumption 1 (Workspace regularity).}
The regions of interest are pairwise disjoint and do not
intersect obstacle or forbidden regions:
\[
l_i\cap l_j=\emptyset,
\quad \forall i\neq j,
\]
and
\[
l_i\cap o_h=\emptyset,
\quad
\forall i\in\{1,\ldots,n_l\},
\quad
\forall h\in\{1,\ldots,n_o\}.
\]
Under the finite workspace discretization used for motion
planning, each region $l_i$ is represented by a nonempty
connected set of adjacent free cells.

Assumption~1 ensures that every region corresponds to a
single connected semantic location. It does not require every
pair of regions to be mutually reachable. Robot-specific
unreachability is represented by $d_k(x,l_i)=+\infty$.

The NBA $B_\phi$ is constructed from $\phi$ using
LTL2BA~[13]. Equivalently, its underlying directed graph can be
written as
\[
\mathcal G(B_\phi)=(Q_B,E_B),
\]
where
\[
E_B=
\left\{
(q_{B,i},q_{B,j})
\;\middle|\;
\exists\,\gamma_{ij}:
q_{B,i}\xrightarrow{\gamma_{ij}}q_{B,j}
\right\}.
\]
Searching this graph together with its transition guards and
acceptance condition yields accepting prefix--suffix runs.

\textbf{Assumption 2 (Existence of a feasible accepting
execution).}
For the initial planning instance, there exists an accepting
prefix--suffix run $\rho$ of $B_\phi$ and a corresponding team
execution $\tau$ such that
\[
w(\tau)\in L(B_\phi)=\mathrm{Words}(\phi).
\]
Moreover, the action requirements induced by $\rho$ admit
type-compatible and pairwise-disjoint robot assignments, and
every assigned robot can reach its required target region along
a finite feasible path. Equivalently,
\[
\mathfrak P_\phi\neq\emptyset.
\]

Assumption~2 concerns the initial planning instance. If the
available team changes during execution, a feasible continuation
for the remaining robots is not assumed to exist; the online
repair procedure may report infeasibility when
the corresponding feasible-plan set becomes empty.
```

---

# 6. 为什么这两项 assumption 不能简单照搬范文

## 6.1 Workspace assumption 的差异

参考论文的 workspace 是 cell-level transition system，因此直接写：

> each region spans consecutive cells

是自然的。

你的 high-level model 是：

- bounded workspace；
- region-level actions；
- robot-specific shortest distance \(d_k\)；
- region may be unreachable for a specific robot。

因此最合适的改写是：

> connected set of adjacent free cells under the motion-planning discretization.

并且不添加参考论文中的 all-pairs label-free connectivity。

---

## 6.2 NBA/path assumption 的差异

参考论文直接把 NBA 当作 graph \(A_\phi=(V,E)\)，后面的方法也始终沿用这个 notation。

你的论文已经：

- 用 \(B_\phi\) 表示 NBA；
- 用 \(A\) 表示 action set；
- 区分 GBA、NBA 和 plan graph；
- 用 \(\rho\) 表示 NBA run。

因此最专业的改写不是再次引入 \(A_\phi\)，而是：

> retain \(B_\phi\), optionally define its underlying graph \(\mathcal G(B_\phi)\), and distinguish accepting run \(\rho\) from physical team execution \(\tau\).

这保留了参考论文的核心思想，但不会破坏你自己的 notation system。

---

# 7. 后文需要同步修改的位置

采用上述版本后，至少同步以下位置。

## 7.1 Sec. V GBA candidate transition

将：

```latex
e_g=(q_g,\sigma_g,q_g')
```

改为：

```latex
e_g=(q_g,\gamma_g,q_g').
```

## 7.2 Definition 6

将：

```latex
e_{ij}=(q_i,\sigma_{ij},q_j)
```

改为：

```latex
e_{ij}=(q_i,\gamma_{ij},q_j).
```

若 guards 是 conjunction，则写：

\[
\gamma_{ij}\equiv\gamma_{ik}\land\gamma_{kj}.
\]

如果代码内部存储 literal sets，则另写：

\[
\mathrm{Lit}(\gamma_{ij})
=
\mathrm{Lit}(\gamma_{ik})
\cup
\mathrm{Lit}(\gamma_{kj}).
\]

## 7.3 Sec. VI Algorithms 2–3

将所有：

```latex
q_{B,i}\xrightarrow{\sigma_{ij}}q_{B,j}
```

改成：

```latex
q_{B,i}\xrightarrow{\gamma_{ij}}q_{B,j}.
```

并将：

```latex
\omega_{ij}=(\sigma_{ij},\sigma_i^s)
```

改为：

```latex
\omega_{ij}=(\gamma_{ij},\gamma_i^{\mathrm{hold}}).
```

## 7.4 Robot type notation

将：

```latex
\tau(r_k)
```

改为：

```latex
\kappa(r_k).
```

将：

```latex
R_{\tau_a}
```

改为：

```latex
R_{t(a)}.
```

## 7.5 Action requirements

将：

```latex
c(a)=(\tau_a,n_a,l_a)
```

改为：

```latex
c(a)=(t(a),n(a),l(a)).
```

## 7.6 Required-action extraction

建议将：

```latex
A(\omega)
```

改为：

```latex
\mathrm{Act}(\omega),
```

避免函数 \(A(\cdot)\) 和 action-proposition set \(A\) 视觉混淆。

## 7.7 Predicted positions

如果 \(x_i(r_k)\in W\)，则不要再写：

```latex
x_i(r_k)=l_j.
```

建议使用：

```latex
x_i(r_k)=y_k(l_j)\in l_j,
```

其中 \(y_k(l_j)\) 是 robot \(r_k\) 在 region \(l_j\) 的 task/service point。

---

# 8. 对理论部分的衔接建议

当前 Theorem 1 的开头是：

> Under the problem formulation and pruning conditions stated above...

加入 assumptions 后建议改为：

```latex
\textbf{Theorem 1.}
Under Assumption~1 and the pruning conditions stated above,
the proposed framework is sound. Moreover, for every instance
with $\mathfrak P_\phi\neq\emptyset$ as in Assumption~2, the
framework returns a feasible plan satisfying $\phi$.
```

不过需要注意：你的当前 completeness proof 声称：

> every transition along the feasible accepting run is eventually considered.

这一点必须与 score-guided expansion、node reuse 和 pruning rule 完全一致。Assumption 2 只保证 feasible plan 存在，不能替代对“算法不会漏掉该 run”的证明。

---

# 9. 最终建议

最值得优先完成的修改是：

1. 将 `Problem Description` 改为 `Problem Formulation`；
2. 将 type set \(T\) 改为 \(\mathcal T\)，type map `\tau` 改为 `\kappa`；
3. 保留 NBA notation \(B_\phi\)，不要照搬 \(A_\phi=(V,E)\)；
4. 用 \(\rho\) 表示 accepting run、用 \(\tau\) 表示 physical team execution、用 \(w(\tau)\) 表示 proposition trace；
5. 将 workspace assumption 写成 connected adjacent cells，而不是非专业的 consecutive cells；
6. 将 LTL2BA 的引用改为你论文中的 [13]，不能复制参考论文的 [44]；
7. 将真正的第二个 assumption 写成“存在 physically feasible accepting execution”，而不是笼统说“可以在 NBA 上找到 path”；
8. 删除 Sec. III-C 对 NBA tuple 的重复定义；
9. 统一 transition guard 为 \(\gamma_{ij}\)；
10. 修正 \(x_i(r_k)\in W\) 与 \(x_i(r_k)=l_j\) 的类型不一致。

按照上面的版本修改后，Problem Formulation 会形成清楚的逻辑链：

\[
\text{workspace/team}
\rightarrow
\text{atomic propositions}
\rightarrow
\text{NBA-induced subtasks}
\rightarrow
\text{assignments}
\rightarrow
\text{team execution }\tau
\rightarrow
w(\tau)\models\phi
\rightarrow
\min J_\phi.
\]

这比直接模仿范文的符号和句式更适合你的 on-the-fly GBA/NBA task-allocation framework。
