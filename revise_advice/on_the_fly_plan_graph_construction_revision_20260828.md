# `ON-THE-FLY PLAN GRAPH CONSTRUCTION` 审稿式检查与修改方案

## 0. 总体结论

我对照检查了当前稿件的以下部分：

- Sec. III 中的 subtask、robot assignment 和 makespan 定义；
- Sec. IV 的 System Overview 与 Algorithm 1；
- Sec. V 输出的 pruned GBA \(G_\phi^{-}\)；
- Sec. VI 的 Definitions、Algorithms 2--4、Examples 4--5、Eqs. (4)--(8)、plan-graph simplification 和 plan extraction；
- Sec. VII 中 BnB 对 plan graph 的使用方式；
- Secs. IX--X 的 complexity / soundness / completeness 论证；
- Table III 中 \(\Pi_{\mathrm{init}}\)、\(\Pi_{\mathrm{plan}}\) 与 reported global optimum 的关系。

### 审稿结论

当前 Sec. VI 的**核心创新是明确且有价值的**：

\[
\text{new NBA transition}
\rightarrow
\text{induced subtask}
\rightarrow
\text{robot assignment}
\rightarrow
\text{plan-graph extension}
\rightarrow
\text{first accepting prefix--suffix plan}.
\]

真正的问题不只是英语表达或段落冗余，而是当前写法把三类不同对象放进了同一个 plan node：

1. **共享的逻辑结构**：NBA state 和 prefix--suffix progress；
2. **依赖具体到达路径的执行状态**：robot positions、completion times 和 remaining-action information；
3. **用于提取某一个方案的代表路径**：single representative predecessor 和 assignment。

当一个 plan node 有多个 parent 时，这三类信息不能再由一套唯一的
\((C_i,X_i,\Theta_i)\) 同时代表。当前 Algorithms 3--4 又仅根据当前 scalar makespan
\(J(\nu)\) 覆盖 shared node 中的 execution state，并向 descendants 传播。较小的当前 makespan 并不必然意味着更好的 robot positions、future reachability 或 continuation cost。因此，从严格审稿角度，当前章节需要的不只是压缩文字，而是先把**逻辑拓扑与路径相关执行状态分层表示**。

另外还有两个会直接影响理论主张的问题：

- `GREEDYASSIGN` 失败不等于不存在可行的 disjoint robot assignment；
- current remaining set
  \[
  M_j=
  \left(\bigcup_{(\nu_i,\nu_j)\in E_P}M_i\right)\setminus A(\omega_j)
  \]
  把不同 parent paths 的历史合并到一起，不再对应任何一条实际执行路径。

因此，我建议优先采用下面的**严谨修改路线**：

> 将 plan graph 保留为共享的 logical graph；在每个 logical plan node 上维护一组 path-dependent execution labels。NBA outgoing transitions 可以按 state 缓存，但每一个新 execution label 都必须独立执行 assignment、state update 和 score computation。

这种两层表示会同时解决：

- 多 parent node 的 execution-state ambiguity；
- representative predecessor 与 structural parents 混淆；
- 已扩展 NBA state 后新 execution context 无法被正确继续扩展；
- remaining set 的路径依赖；
- first-plan extraction 的一致性；
- safe dominance 和 completeness 的可证明性。

如果当前实现暂时不能改为 execution-label architecture，则应采用本文第 8 节给出的**最小改动安全路线**，并把理论主张收缩为：

> returned-plan soundness and optimization relative to the greedily generated plan graph,

而不能继续无条件声称全局 completeness。

---

# 1. 与前后文应该形成的逻辑接口

Sec. VI 不应孤立描述，而应明确承接 Sec. V、输出给 Sec. VII，并与实验中的三个 solution levels 对齐。

| 位置 | Sec. VI 应接收或输出的对象 | 推荐关系 |
|---|---|---|
| Sec. V | pruned GBA | \(G_\phi^{-}\) 是唯一 automaton input |
| Sec. III | subtask、requirements、cost | \(\omega_{ij}=(\gamma_{ij},\gamma_i^{\mathrm{hold}})\)，\(c(a)=(t(a),n(a),\ell(a))\)，makespan 与 Eq. (3) 一致 |
| Sec. IV | early output | Sec. VI 应显式输出 \(\Pi_{\mathrm{init}}\) 和 \(T_{\mathrm{first}}\) |
| Sec. VII | graph search domain + warm start | 输出 \(G_P\) 和 \(\Pi_{\mathrm{plan}}\)，后者仅是 construction-stage incumbent |
| Sec. VIII | retained graph | \(G_P\) 必须保留可重新展开或重新赋值的 task structure |
| Sec. IX | complexity parameters | 应统计 evaluated execution labels，而不只是 NBA states |
| Sec. X | correctness scope | soundness、conditional completeness 和 graph-relative optimization 必须分别陈述 |
| Table III | three solution levels | \(\Pi_{\mathrm{init}}\rightarrow\Pi_{\mathrm{plan}}\rightarrow\Pi^\star\)，不能混为一个“optimal solution” |

推荐的整体输出关系为：

\[
(G_P,\Pi_{\mathrm{init}},T_{\mathrm{first}},\Pi_{\mathrm{plan}})
=
\textsc{ConstructNBAAndPlanGraph}
(G_\phi^{-},R,c,X_0,\Theta_0).
\]

其中：

- \(\Pi_{\mathrm{init}}\)：第一个生成的 feasible accepting prefix--suffix plan；
- \(T_{\mathrm{first}}\)：从 planning 开始到 \(\Pi_{\mathrm{init}}\) 可用的 elapsed time；
- \(\Pi_{\mathrm{plan}}\)：joint construction 结束时，在所有已生成 terminal execution labels 中成本最低的方案；
- \(G_P\)：供后续 BnB refinement 和 online repair 使用的 retained structural graph。

Table III 中多个 task 的 \(J_{\mathrm{plan}}\neq J_{\mathrm{opt}}\)。因此，Sec. VI 应主动把
\(\Pi_{\mathrm{plan}}\) 定位为 **best construction-stage incumbent**，而不是暗示它保留或达到 original problem 的 global optimum。

---

# 2. 推荐修改章节标题和结构

## 2.1 标题

当前标题：

```latex
\section{On-the-Fly Plan Graph Construction}
```

建议改为：

```latex
\section{Joint On-the-Fly NBA and Plan-Graph Construction}
```

理由：

- 本节不是在一个已有 NBA 上单独建 plan graph；
- 本文最核心的创新正是 NBA generation 与 task allocation 同步发生；
- 与 Abstract、Contributions 和 System Overview 的 “synchronously constructs the NBA and plan graph” 保持一致；
- 使 reviewer 在目录中就能看到真正的 integration point。

## 2.2 章节结构

建议将当前结构重组为：

```text
VI. Joint On-the-Fly NBA and Plan-Graph Construction
    A. Plan Graph and Execution Labels
    B. Feasible Execution-Label Extension
    C. Residual-Obligation-Guided Expansion
    D. Graph Simplification and Plan Extraction
```

### 为什么这样重组

当前 Sec. VI-B 同时包含：

- worklist；
- LTL2BA simplification；
- plan-node extension；
- greedy assignment；
- node reuse；
- score；
- best-plan update。

这些内容在一个 subsection 中连续出现，导致 algorithm control flow、data structure 和 heuristic score 三条逻辑线相互穿插。

推荐结构分别回答四个问题：

1. **图中存什么？**
2. **一个 transition 如何形成可执行 successor？**
3. **successors 按什么顺序展开？**
4. **最终怎样删除 dead structure 并提取一致方案？**

---

# 3. 符号统一检查

下面的修改应与前面 Preliminaries 和 Problem Formulation 的推荐记号同步完成。

| 当前写法 | 推荐写法 | 原因 |
|---|---|---|
| \(\sigma_k\) 和 \(\sigma_{ij}\) | \(\sigma_k\) 表示 concrete word letter；\(\gamma_{ij}\) 表示 symbolic guard | 当前同一符号表示不同数学对象 |
| \(\Sigma_B\) | \(\Sigma=2^{AP}\) | 所有 automata 使用同一 alphabet |
| \(A(\omega)\) | \(\operatorname{Act}(\omega)\) | 避免与 action-proposition set \(A\) 混淆 |
| \(c(a_\ell)=(\tau_\ell,n_\ell,l_\ell)\) | \(c(a)=(t(a),n(a),\ell(a))\) | 避免 robot-type map、path \(\tau\) 和 action index 冲突 |
| \(R_{\tau_\ell}\) | \(R_{t(a)}\) | 与 requirement map 对齐 |
| \(x_i(r_k)=l_j\) | \(x_i(r_k)=y_k(l_j)\in l_j\)，或单独用 region-level location | \(x_i(r_k)\in W\)，不能等于 region set |
| `Prog` | phase \(\zeta\) 记录 prefix 或具体 suffix anchor | generic `suf` 无法说明 suffix 返回哪个 accepting state |
| `dead` plan node | 不插入 infeasible label | discarded branch 没有必要成为 graph node |
| \(J(\nu_i)\) | \(J(\lambda_i)\) | cost 属于 path-dependent execution context，而非共享 logical node |
| \(M_i\) stored once per node | \(M_{\lambda_i}\) stored per execution label | remaining history 与 parent path 有关 |
| \(S(\nu_i,e_{B,ij})\) | \(S(\lambda_j)\) | score 应基于执行当前 subtask 后的 successor state |
| \(Q_B^{\mathrm{exp}}\) 同时控制全部 contexts | outgoing-transition cache \(\mathsf{Out}(q_B)\) + label worklist `OPEN` | automaton transition generation 与 execution-context expansion 应分开 |

---

# 4. 当前写法的关键逻辑问题

## 4.1 Plan node 同时承担 logical node 和 execution state

当前：

\[
\nu_i=(q_{B,i},\mathrm{Prog}_i,\omega_i,C_i,X_i,\Theta_i).
\]

同时又允许：

> multiple plan nodes may be associated with the same NBA state；

以及：

> a compatible existing node can have multiple parents。

如果一个 shared node \(\nu_h\) 有两个 parents，则：

- 从 parent 1 到达时可能得到 \((C_h^{(1)},X_h^{(1)},\Theta_h^{(1)})\)；
- 从 parent 2 到达时可能得到 \((C_h^{(2)},X_h^{(2)},\Theta_h^{(2)})\)。

当前 node tuple 只能保存一套值。

Algorithm 3 通过比较 scalar makespan：

\[
\hat J<J(\nu_h)
\]

来覆盖 shared node 的 execution state。这并不是 safe dominance。

### 反例结构

考虑两个 contexts 到达相同 NBA state：

- Context 1：当前 makespan 为 10，但所需 type-1 robots 位于后续任务区域的远端；
- Context 2：当前 makespan 为 11，但这些 robots 已经位于下一必需区域附近。

虽然 \(10<11\)，Context 2 可能产生更低的 final makespan，甚至可能是唯一能完成 future holding/reachability constraints 的 context。

因此：

\[
J_1<J_2
\not\Rightarrow
\text{Context 1 dominates Context 2}.
\]

### 推荐

logical node 只保存：

\[
v=(q_B,\zeta),
\]

而 path-dependent state 存在 execution label：

\[
\lambda=(X,\Theta,M,\operatorname{pred},e^{\mathrm{in}},C^{\mathrm{in}}).
\]

一个 logical node 可以拥有多个 non-dominated labels。

---

## 4.2 `Prog={pre,suf,acc,dead}` 没有准确编码 suffix root

要确认一个 prefix--suffix plan 已完成，不只是需要知道“已经进入 suffix”，还需要知道：

> suffix 应返回哪个 accepting state。

generic `suf` 无法区分：

- suffix anchored at \(q_{B,f_1}\)；
- suffix anchored at \(q_{B,f_2}\)。

推荐 phase set：

\[
\mathcal Z
=
\{\mathrm{pre}\}
\cup
\bigl(\{\mathrm{suf},\mathrm{acc}\}\times Q_{B,F}\bigr).
\]

例如：

- \(\zeta=\mathrm{pre}\)：尚未选择 suffix root；
- \(\zeta=(\mathrm{suf},q_f)\)：suffix 以 \(q_f\) 为 anchor，正在寻找回到 \(q_f\) 的 cycle；
- \(\zeta=(\mathrm{acc},q_f)\)：已经返回 \(q_f\)，形成一个完整 prefix--suffix structure。

当 prefix 首次或再次到达 accepting state \(q_f\) 时，应创建一个 anchored successor；为了不强制“第一个 accepting state 必须成为 suffix root”，还可保留 prefix continuation。

---

## 4.3 Worklist 只按 NBA state 展开，会遗漏后来到达的 execution contexts

当前 `S_B` 存 NBA states，`Q_B^{exp}` 标记 state 是否已经 expanded。

问题是：

> NBA outgoing transitions 只依赖 automaton state，可以缓存一次；但 transition 是否可执行、执行后 robots 在哪里、completion times 是多少，依赖具体 execution context。

若 \(q_{B,j}\) 已经 expanded，后来又有一个不同 \((X,\Theta)\) 到达该 state，不能仅连接到原先 successor nodes。必须从新 context 重新计算：

- transition subtask feasibility；
- robot assignment；
- holding condition；
- successor \(X'\)、\(\Theta'\)；
- remaining set；
- ordering score。

当前 `REUSESUCCESSORS` 通过共享原 successor nodes 并覆盖 representative payload 来补救，但这正是上述语义冲突的来源。

### 推荐

- `\mathsf{Out}(q_B)`：只缓存已生成并经过 LTL2BA simplification 的 NBA outgoing transitions；
- `OPEN`：存尚未扩展的 execution labels，而不是 NBA states；
- 新 label 到达已生成过的 NBA state 时，复用 transition cache，但重新执行 label extension；
- 删除当前 Algorithm 4 `REUSESUCCESSORS`。

---

## 4.4 `GREEDYASSIGN` 失败不能推出 subtask infeasible

当前 procedure 按 action proposition index 逐个处理，并为当前 action 选 earliest-arrival robots。

设同一 subtask 中有两个同类型 actions \(a_1,a_2\)，各需 1 个 robot：

- robot \(r_1\) 可到达 \(a_1\) 和 \(a_2\)；
- robot \(r_2\) 只能到达 \(a_1\)；
- 对 \(a_1\)，\(r_1\) 比 \(r_2\) 到达更早。

若 greedy 先为 \(a_1\) 选择 \(r_1\)，则 \(a_2\) 失败；但可行 assignment 明明存在：

\[
C(a_1)=\{r_2\},
\qquad
C(a_2)=\{r_1\}.
\]

所以：

\[
\textsc{GreedyAssign fails}
\not\Rightarrow
\text{no feasible assignment exists}.
\]

### 两种合法处理方式

#### 方式 A：希望保留 completeness（推荐）

- greedy assignment 作为第一个候选，用于快速首解；
- greedy failure 后调用 exact bipartite \(b\)-matching / flow feasibility test；
- construction 继续时，lazy enumeration 其余 feasible assignments；
- 只保留 resulting execution states 中的 non-dominated labels。

#### 方式 B：保留当前实现

正文必须写成：

> the extension is discarded by the greedy construction rule,

不能写成：

> the subtask / branch is infeasible.

同时，Sec. X 的 completeness claim 必须限定为：

> completeness relative to the greedily generated labels,

或直接只保留 returned-plan soundness。

---

## 4.5 当前 assignment 更新没有明确检查 holding condition

Subtask 已定义为：

\[
\omega_{ij}
=
(\gamma_{ij},\gamma_i^{\mathrm{hold}}),
\]

但当前 GreedyAssign eligibility 只写：

- correct robot type；
- finite arrival time；
- not used by another action in the same subtask。

这没有说明：

- robots 在移动和等待期间如何保持 \(\gamma_i^{\mathrm{hold}}\)；
- negative region constraints 如何进入 path feasibility；
- collaborative actions 等待同步时是否仍满足 holding guard。

### 推荐

定义 holding-aware path oracle：

\[
d_k^{\omega}
\bigl(x,\ell\bigr)
\]

表示 robot \(r_k\) 从 \(x\) 到 target region \(\ell\) 且在整个移动/等待过程中满足
\(\gamma_i^{\mathrm{hold}}\) 的最短可行距离；若不存在，则为 \(+\infty\)。

若 holding condition 是 team-level 而不能逐 robot 分解，则应写：

> a candidate assignment is accepted only after the joint motion/waiting realization is verified by the lower-level feasibility oracle.

在没有执行这类检查时，只能声称 task-level assignment feasibility，而不能声称 physical path feasibility。

---

## 4.6 Completion-time update 应显式保持 subtask precedence

当前 arrival time：

\[
\hat t_i(r,a)
=
\theta_i(r)+
\frac{d_r(x_i(r),\ell(a))}{v(r)}.
\]

随后直接将 synchronized subtask completion time 设为 assigned robots 的最大 arrival time。

但一个 successor automaton transition 必须发生在 parent subtask 已完成之后。因此应写：

\[
t_{ij}
=
\max
\left\{
J(\lambda_i),
\max_{\substack{a\in\operatorname{Act}(\omega_{ij})\\
r\in C_{ij}(a)}}
\hat t_i(r,a)
\right\}.
\]

其中：

\[
J(\lambda_i)
=
\max_{r\in R}\theta_i(r).
\]

这样即使本次选中的 robots 在 parent task 结束前已经空闲，successor transition 也不会被错误地记为早于 automaton predecessor 完成。

---

## 4.7 Position notation 存在类型错误

前文定义：

\[
x_i(r_k)\in W.
\]

但 Example 4 写：

\[
x_1(r_k)=l_5,
\]

其中 \(l_5\subset W\) 是一个 region，不是 point。

### 推荐

为 robot-region pair 定义 service point：

\[
y_k(l)\in l,
\]

并写：

\[
x_j(r_k)=y_k(\ell(a)).
\]

或者，将高层位置直接定义成 region-valued state：

\[
\ell_i(r_k)\in L.
\]

当前全文使用 shortest distance from a point to a region，因此第一种写法更自然。

---

## 4.8 Remaining set 的 parent union 没有路径语义

当前：

\[
M_j=
\left(
\bigcup_{(\nu_i,\nu_j)\in E_P}M_i
\right)
\setminus A(\omega_j).
\]

假设同一 node 有两条 parent paths：

- Path 1 已完成 \(a_1\)，尚未完成 \(a_2\)；
- Path 2 已完成 \(a_2\)，尚未完成 \(a_1\)。

则 union 得到：

\[
M_j=\{a_1,a_2\},
\]

但没有任何一条实际路径同时剩余这两个 action。该集合不再对应执行历史。

### 推荐

remaining set 存在 execution label 上，并按单一路径更新：

\[
M_{\lambda_j}
=
M_{\lambda_i}
\setminus
\operatorname{Act}(\omega_{ij}).
\]

另外，当前 `ME` 规则最多应被称为：

> syntactic required-action approximation,

而不是严格的 semantic “must-eventually set”。它可能低估重复 temporal obligations，但只要 score 不用于 pruning，这种低估不会影响 correctness。

---

## 4.9 Score 应基于 successor execution state，并明确只是 ordering heuristic

当前在得到 successor node 后，却用 parent \(X_i,\Theta_i,J(\nu_i)\) 计算 future action arrival estimates。

更自然的语义是：

> 已经完成当前 subtask 后，从 successor execution state 出发，估计 remaining burden。

因此应使用：

\[
h_a(\lambda_j)
=
\text{\(n(a)\)-th smallest value of }
\left\{
\theta_j(r)+
\frac{d_r(x_j(r),\ell(a))}{v(r)}
\right\}_{r\in R_{t(a)}}.
\]

然后：

\[
H(\lambda_j)
=
\begin{cases}
\max_{a\in M_{\lambda_j}}h_a(\lambda_j),
&
M_{\lambda_j}\neq\emptyset,\\
J(\lambda_j),
&
M_{\lambda_j}=\emptyset,
\end{cases}
\]

\[
S(\lambda_j)
=
\max\{J(\lambda_j),H(\lambda_j)\}.
\]

必须明确：

- \(S\) 只改变 local expansion order；
- 它不是 Sec. VII 的 admissible BnB lower bound；
- 不使用 \(S\) 删除 label；
- 同一 successor NBA state 的不同 non-dominated labels不能只保留最小 score 的一个。

---

## 4.10 Plan extraction 必须沿同一 execution-label chain

当前 shared node 有多个 structural parents，但 plan extraction 只沿一个 representative predecessor。

如果 shared node payload 后来被另一 parent 更新，原先 terminal node 的 predecessor chain 与其 stored \(C,X,\Theta\) 可能不再来自同一执行历史。

推荐每个 execution label 保存：

- predecessor label；
- incoming structural edge；
- assignment used on that edge。

从 terminal label 回溯后得到的是一条单一、完整且内部一致的：

\[
\text{NBA transition sequence}
+
\text{subtask sequence}
+
\text{assignment sequence}
+
\text{execution-state sequence}.
\]

---

# 5. 推荐的两层表示

## 5.1 Structural plan graph

定义 edge-labeled directed multigraph：

\[
G_P=(V_P,E_P).
\]

每个 logical plan node：

\[
v_i=(q_{B,i},\zeta_i),
\]

其中：

\[
\zeta_i\in
\{\mathrm{pre}\}
\cup
\left(
\{\mathrm{suf},\mathrm{acc}\}
\times Q_{B,F}
\right).
\]

每个 plan-graph edge：

\[
\varepsilon_{ij}
=
(v_i,e^B_{ij},\omega_{ij},v_j),
\]

其中 \(e^B_{ij}\) 是对应 NBA transition，\(\omega_{ij}\) 是其 induced subtask。

使用 multigraph 是必要的，因为相同 source/destination states 之间可能存在不同 guards 或 subtasks。

## 5.2 Execution labels

每个 logical node \(v_i\) 维护 label set：

\[
\Lambda(v_i).
\]

一个 execution label：

\[
\lambda_i
=
\left(
X_i,\Theta_i,M_i,
\operatorname{pred}(\lambda_i),
\varepsilon_i^{\mathrm{in}},
C_i^{\mathrm{in}}
\right).
\]

其中：

- \(X_i\)：该具体 partial execution 后的 robot positions；
- \(\Theta_i\)：robot completion times；
- \(M_i\)：该具体 path 的 remaining-action approximation；
- \(\operatorname{pred}(\lambda_i)\)：plan extraction predecessor；
- \(\varepsilon_i^{\mathrm{in}}\)：incoming plan-graph edge；
- \(C_i^{\mathrm{in}}\)：该 incoming subtask 的 assignment。

label cost：

\[
J(\lambda_i)
=
\max_{r\in R}\theta_i(r).
\]

## 5.3 Safe dominance

最保守且容易证明的 dominance relation 为：

\[
\lambda^1\preceq\lambda^2
\]

当且仅当：

1. 两者位于同一个 logical node；
2. \(X^1=X^2\)；
3. \(M^1=M^2\)；
4. 对所有 robots：
   \[
   \theta^1(r)\leq\theta^2(r).
   \]

在本文无 deadlines、future dynamics 只依赖 current NBA state、robot positions 和 availability times 的模型下，\(\lambda^1\) 可以安全删除 \(\lambda^2\)。

不能使用：

\[
J(\lambda^1)<J(\lambda^2)
\]

单独作为 dominance criterion。

若 future feasibility 还依赖其他 history，例如 carried objects、battery state 或 previous-role bindings，则这些 variables 也必须进入 label 和 dominance comparison。

---

# 6. 最推荐的完整英文替换稿

## 使用前说明

下面给出的是**严谨推荐版本**。它要求实现同步采用：

1. logical plan nodes + execution labels；
2. greedy-first、exact-feasibility-backed assignment generation；
3. componentwise safe dominance；
4. label-level worklist；
5. score 只用于 ordering。

采用该版本后，才有条件继续论证 conditional completeness。

若实现仍保持当前 Algorithms 2--4，不应直接使用下面文本中的 exhaustive / non-dominated assignment statements，而应采用第 8 节的最小改动路线。

---

## VI. JOINT ON-THE-FLY NBA AND PLAN-GRAPH CONSTRUCTION

```latex
\section{Joint On-the-Fly NBA and Plan-Graph Construction}

Given the pruned GBA $G_\phi^{-}$ from Sec.~V, this section
constructs the NBA and a plan graph jointly. Whenever a new
symbolic NBA transition is generated, its induced subtask is
evaluated immediately from the currently available robot
execution contexts. A feasible extension is inserted into the
plan graph together with its path-dependent execution state.
Thus, the first feasible plan can be returned as soon as a
complete accepting prefix--suffix structure is generated,
without waiting for the complete NBA.

The construction order is guided by a residual-obligation
score. The score is used only to order feasible extensions; it
does not remove an automaton transition or a feasible execution
context. This separation is important: automaton generation
determines the logical task structure, exact assignment checks
determine feasibility, and the score determines only which
retained extension is explored first.
```

---

## A. Plan Graph and Execution Labels

```latex
\subsection{Plan Graph and Execution Labels}

The plan graph stores the shared logical structure induced by
the on-the-fly NBA, whereas path-dependent robot states are
stored separately as execution labels.

\textbf{Definition 8 (Plan graph and execution label).}
The plan graph is an edge-labeled directed multigraph
\[
G_P=(V_P,E_P).
\]
Each plan node is
\[
v_i=(q_{B,i},\zeta_i),
\]
where $q_{B,i}\in Q_B$ is an NBA state and
\[
\zeta_i\in
\{\mathrm{pre}\}
\cup
\bigl(
\{\mathrm{suf},\mathrm{acc}\}\times Q_{B,F}
\bigr)
\]
records the prefix--suffix phase. The value
$\zeta_i=\mathrm{pre}$ indicates that no suffix root has been
selected. The value
$\zeta_i=(\mathrm{suf},q_f)$ indicates that $q_f\in Q_{B,F}$
has been selected as the suffix root and that the construction
is seeking a return to $q_f$. Finally,
$\zeta_i=(\mathrm{acc},q_f)$ indicates that the suffix has
returned to $q_f$ and hence completes an accepting
prefix--suffix structure.

A plan-graph edge is
\[
\varepsilon_{ij}
=
(v_i,e^B_{ij},\omega_{ij},v_j),
\]
where
\[
e^B_{ij}:
q_{B,i}\xrightarrow{\gamma_{ij}}q_{B,j}
\]
is the corresponding symbolic NBA transition and
\[
\omega_{ij}
=
(\gamma_{ij},\gamma_i^{\mathrm{hold}})
\]
is its induced subtask.

Each plan node $v_i$ is associated with a set of execution
labels $\Lambda(v_i)$. A label is
\[
\lambda_i=
\left(
X_i,\Theta_i,M_i,
\operatorname{pred}(\lambda_i),
\varepsilon_i^{\mathrm{in}},
C_i^{\mathrm{in}}
\right),
\]
where $X_i$ and $\Theta_i$ are the predicted robot positions
and completion times after the corresponding partial
execution, $M_i$ is the path-dependent remaining-action
approximation, and the last three entries record the
predecessor label, incoming plan-graph edge, and robot
assignment used to generate $\lambda_i$. Its realized
makespan is
\[
J(\lambda_i)
=
\max_{r_k\in R}\theta_i(r_k).
\tag{4}
\]

The root node is
\[
v_0=(q_{B,0},\zeta_0),
\]
where $\zeta_0=\mathrm{pre}$ if
$q_{B,0}\notin Q_{B,F}$; otherwise, an anchored suffix-start
label at $q_{B,0}$ is also initialized. The root execution label
is
\[
\lambda_0=
(X_0,\Theta_0,M_0,\emptyset,\emptyset,\emptyset),
\]
with
\[
x_0(r_k)=x(r_k),
\qquad
\theta_0(r_k)=0.
\]

When an unanchored prefix extension reaches an accepting
state $q_f$, the construction creates a suffix-start context
anchored at $q_f$. The unanchored prefix context may also be
retained so that a later accepting state can serve as the suffix
root. A label is terminal only after a nonempty suffix path
returns to its selected root $q_f$.
```

### Dominance paragraph

```latex
Multiple execution labels may be associated with the same
plan node because different task-allocation histories can reach
the same logical automaton state. A label
$\lambda^1\in\Lambda(v)$ dominates
$\lambda^2\in\Lambda(v)$ only if they have identical robot
positions and remaining-action summaries and
\[
\theta^1(r_k)\leq\theta^2(r_k),
\qquad
\forall r_k\in R.
\]
Under the state model in Sec.~III, any continuation feasible
from $\lambda^2$ is then also feasible no later from
$\lambda^1$. Labels with different robot positions are retained;
a smaller scalar makespan alone is not used as a dominance
test.
```

---

## B. Feasible Execution-Label Extension

```latex
\subsection{Feasible Execution-Label Extension}

Consider an execution label $\lambda_i\in\Lambda(v_i)$ and
an outgoing NBA transition
\[
e^B_{ij}:
q_{B,i}\xrightarrow{\gamma_{ij}}q_{B,j}.
\]
The induced subtask is
\[
\omega_{ij}
=
(\gamma_{ij},\gamma_i^{\mathrm{hold}}).
\]
Let
\[
\operatorname{Act}(\omega_{ij})
\subseteq A
\]
denote the positive action propositions required by the selected
conjunctive guard clause. A synchronized assignment is a map
\[
C_{ij}:
\operatorname{Act}(\omega_{ij})
\rightarrow 2^R
\]
satisfying
\[
C_{ij}(a)\subseteq R_{t(a)},
\qquad
|C_{ij}(a)|=n(a),
\]
and
\[
C_{ij}(a)\cap C_{ij}(b)=\emptyset,
\qquad
a\neq b.
\]
In addition, every selected robot must admit a finite motion
and waiting realization that preserves
$\gamma_i^{\mathrm{hold}}$ until the transition guard is
satisfied.

For robot $r_k$ and action $a$, let
\[
d_k^{\omega_{ij}}
\bigl(x_i(r_k),\ell(a)\bigr)
\]
denote the shortest feasible distance under the holding
condition; it is $+\infty$ if no such realization exists. The
predicted arrival time is
\[
\widehat t_i(r_k,a)
=
\theta_i(r_k)
+
\frac{
d_k^{\omega_{ij}}
\bigl(x_i(r_k),\ell(a)\bigr)
}{
v(r_k)
}.
\tag{5}
\]
For a feasible assignment $C_{ij}$, the synchronized
completion time is
\[
t_{ij}
=
\max
\left\{
J(\lambda_i),
\max_{\substack{
a\in\operatorname{Act}(\omega_{ij})\\
r_k\in C_{ij}(a)
}}
\widehat t_i(r_k,a)
\right\}.
\tag{6}
\]
The first term enforces the precedence of the NBA transition:
the successor subtask cannot complete before the partial plan
represented by $\lambda_i$.

For every assigned robot $r_k\in C_{ij}(a)$, choose a service
point $y_k(\ell(a))\in\ell(a)$ and set
\[
x_j(r_k)=y_k(\ell(a)),
\qquad
\theta_j(r_k)=t_{ij}.
\]
Robots not assigned to $\omega_{ij}$ retain their positions and
completion times from $\lambda_i$. These updates produce
$X_j$ and $\Theta_j$.
```

### Assignment-generation scope

```latex
To obtain an early feasible plan, the assignment generator
returns a greedy earliest-arrival assignment first. A greedy
failure, however, is not treated as a proof of infeasibility.
Before an extension is discarded, an exact disjoint-assignment
feasibility test is applied. As construction continues, the
remaining feasible assignments can be generated lazily, and
only non-dominated successor execution labels are retained.
The greedy ordering therefore affects the time at which a
feasible label is discovered, but not the set of feasible
extensions eventually represented.
```

### Revised Example 4

```latex
\textbf{Example 4.}
Continuing Example~1, consider the root label $\lambda_0$
and the transition
\[
q_{B,0}\xrightarrow{a_1}q_{B,1}.
\]
The induced subtask requires two type-2 robots at $l_5$.
The first assignment generated is
\[
C_{01}(a_1)=\{r_4,r_5\}.
\]
For $r_k\in\{r_4,r_5\}$,
\[
\widehat t_0(r_k,a_1)
=
\frac{
d_k^{\omega_{01}}(x(r_k),l_5)
}{
v(r_k)
},
\]
and
\[
t_{01}
=
\max
\left\{
J(\lambda_0),
\widehat t_0(r_4,a_1),
\widehat t_0(r_5,a_1)
\right\}.
\]
The assigned robots are updated to service points in $l_5$ and
their completion times are set to $t_{01}$; all other robot
states are unchanged. The resulting successor execution label
is inserted at the plan node associated with $q_{B,1}$.
```

---

## C. Residual-Obligation-Guided Expansion

```latex
\subsection{Residual-Obligation-Guided Expansion}

The on-the-fly NBA construction inherited from LTL2BA
generates and simplifies the outgoing transitions of an NBA
state when that state is first required. The resulting outgoing
transition set is cached and reused for every execution label
that later reaches the same NBA state. Thus, automaton
structure is generated once, whereas assignment and execution
state propagation are performed separately for every retained
label.

To guide the local expansion order, we compute a syntactic
required-action approximation from the AST $T_\phi$. Let
$\operatorname{Req}(\psi)\subseteq A$ be recursively defined by
\[
\operatorname{Req}(\top)
=
\operatorname{Req}(\bot)
=
\emptyset,
\]
\[
\operatorname{Req}(a)=\{a\},
\quad a\in A,
\]
\[
\operatorname{Req}(p)
=
\operatorname{Req}(\neg\pi)
=
\emptyset,
\]
\[
\operatorname{Req}(\psi_1\land\psi_2)
=
\operatorname{Req}(\psi_1)
\cup
\operatorname{Req}(\psi_2),
\]
\[
\operatorname{Req}(\psi_1\lor\psi_2)
=
\operatorname{Req}(\psi_1)
\cap
\operatorname{Req}(\psi_2),
\]
\[
\operatorname{Req}(\bigcirc\psi)
=
\operatorname{Req}(\psi),
\]
and
\[
\operatorname{Req}(\psi_1\,\mathsf U\,\psi_2)
=
\operatorname{Req}(\psi_2),
\qquad
\operatorname{Req}(\psi_1\,\mathsf V\,\psi_2)
=
\operatorname{Req}(\psi_2).
\]
This approximation is used only as an ordering heuristic; it is
not an exact characterization of all future temporal
obligations and is not used for pruning.

At the root,
\[
M_0=\operatorname{Req}(\phi).
\]
For an extension from $\lambda_i$ through $\omega_{ij}$, the
path-dependent remaining set is
\[
M_j
=
M_i
\setminus
\operatorname{Act}(\omega_{ij}).
\tag{7}
\]
The update is performed separately for every execution label;
remaining sets from different parent paths are not combined.

For each $a\in M_j$, let $h_a(\lambda_j)$ be the
$n(a)$-th smallest finite arrival-time estimate from the
successor state $(X_j,\Theta_j)$ to $\ell(a)$ among robots in
$R_{t(a)}$. If fewer than $n(a)$ such robots have finite
estimates, set $h_a(\lambda_j)=+\infty$. Define
\[
H(\lambda_j)
=
\begin{cases}
\displaystyle
\max_{a\in M_j}h_a(\lambda_j),
&
M_j\neq\emptyset,\\[1ex]
J(\lambda_j),
&
M_j=\emptyset,
\end{cases}
\tag{8}
\]
and
\[
S(\lambda_j)
=
\max
\left\{
J(\lambda_j),
H(\lambda_j)
\right\}.
\tag{9}
\]
A smaller value gives the label higher priority among the
feasible successors generated in the current expansion batch.
The score is not a BnB lower bound and does not eliminate any
non-dominated execution label.
```

---

## Revised Algorithm 2

```latex
\begin{algorithm}[t]
\caption{Joint On-the-Fly NBA and Plan-Graph Construction}
\label{alg:joint-construction}
\begin{algorithmic}[1]
\Require Pruned GBA $G_\phi^{-}$, robot team $R$,
requirement map $c$, and initial execution state
$(X_0,\Theta_0)$.
\Ensure Plan graph $G_P$, first feasible plan
$\Pi_{\mathrm{init}}$, first-plan time $T_{\mathrm{first}}$,
and construction-stage incumbent $\Pi_{\mathrm{plan}}$,
or \textsc{Infeasible}.
\State Initialize the root plan node $v_0$ and root label
$\lambda_0$.
\State $G_P\gets(\{v_0\},\emptyset)$;
$\mathrm{OPEN}\gets[(v_0,\lambda_0)]$.
\State $\Pi_{\mathrm{init}}\gets\emptyset$;
$\Pi_{\mathrm{plan}}\gets\emptyset$.
\State Initialize an empty outgoing-transition cache
$\mathsf{Out}$.
\While{$\mathrm{OPEN}\neq\emptyset$}
    \State $(v_i,\lambda_i)\gets\textsc{Pop}(\mathrm{OPEN})$.
    \State $q_{B,i}\gets q_B(v_i)$.
    \If{$\mathsf{Out}(q_{B,i})$ is not available}
        \State Generate the outgoing NBA transitions of
        $q_{B,i}$ from $G_\phi^{-}$.
        \State Apply the standard on-the-fly LTL2BA
        simplification and cache the retained transitions in
        $\mathsf{Out}(q_{B,i})$.
    \EndIf
    \State $\mathrm{Cand}\gets\emptyset$.
    \ForAll{$e^B_{ij}\in\mathsf{Out}(q_{B,i})$}
        \State $\mathcal L\gets
        \textsc{ExtendExecutionLabels}
        (v_i,\lambda_i,e^B_{ij},R,c)$.
        \ForAll{$(v_j,\lambda_j,\varepsilon_{ij},
        \mathrm{status})\in\mathcal L$}
            \If{$\lambda_j$ is dominated at $v_j$}
                \State \textbf{continue}.
            \EndIf
            \State Remove labels dominated by $\lambda_j$;
            insert $v_j$, $\varepsilon_{ij}$, and $\lambda_j$.
            \If{$\mathrm{status}=\textsc{Terminal}$}
                \State $\Pi\gets\textsc{ExtractPlan}(\lambda_j)$.
                \If{$\Pi_{\mathrm{init}}=\emptyset$}
                    \State $\Pi_{\mathrm{init}}\gets\Pi$ and record
                    $T_{\mathrm{first}}$.
                \EndIf
                \If{$\Pi_{\mathrm{plan}}=\emptyset$ or
                $T(\Pi)<T(\Pi_{\mathrm{plan}})$}
                    \State $\Pi_{\mathrm{plan}}\gets\Pi$.
                \EndIf
            \Else
                \State Insert $(v_j,\lambda_j)$ into
                $\mathrm{Cand}$ with key $S(\lambda_j)$.
            \EndIf
        \EndFor
    \EndFor
    \State Sort $\mathrm{Cand}$ by nondecreasing score, using
    generation order to break ties.
    \State Push the sorted labels onto $\mathrm{OPEN}$ in
    reverse order.
\EndWhile
\If{$\Pi_{\mathrm{init}}=\emptyset$}
    \State \Return \textsc{Infeasible}.
\EndIf
\State Simplify $G_P$ and its label-transition structure as in
Sec.~VI-D.
\State \Return
$(G_P,\Pi_{\mathrm{init}},T_{\mathrm{first}},
\Pi_{\mathrm{plan}})$.
\end{algorithmic}
\end{algorithm}
```

### Algorithm 2 的关键语义

建议正文紧接着说明：

```latex
The cache $\mathsf{Out}$ prevents repeated automaton
generation, whereas $\mathrm{OPEN}$ contains execution labels
rather than NBA states. Consequently, when a new robot
execution context reaches an NBA state whose outgoing
transitions have already been generated, the cached
transitions are reused but their induced subtasks are evaluated
again from the new context. No representative execution state
is overwritten and no descendant-state propagation procedure
is required.
```

---

## Revised Algorithm 3

```latex
\begin{algorithm}[t]
\caption{Execution-Label Extension}
\label{alg:label-extension}
\begin{algorithmic}[1]
\Require Plan node $v_i$, execution label $\lambda_i$,
NBA transition $e^B_{ij}$, robot team $R$, and requirement
map $c$.
\Ensure A set of feasible successor label records.
\State Obtain
$\omega_{ij}=(\gamma_{ij},\gamma_i^{\mathrm{hold}})$.
\State Compute the admissible successor phases from
$\zeta_i$ and $q_{B,j}$.
\State Generate feasible synchronized assignments for
$\omega_{ij}$, returning the greedy assignment first.
\ForAll{retained assignments $C_{ij}$}
    \State Compute $t_{ij}$ using (6) and update
    $(X_j,\Theta_j)$.
    \State $M_j\gets
    M_i\setminus\operatorname{Act}(\omega_{ij})$.
    \ForAll{admissible successor phases $\zeta_j$}
        \State Obtain or create
        $v_j=(q_{B,j},\zeta_j)$ and
        $\varepsilon_{ij}=(v_i,e^B_{ij},\omega_{ij},v_j)$.
        \State Create
        \[
        \lambda_j=
        (X_j,\Theta_j,M_j,\lambda_i,
        \varepsilon_{ij},C_{ij}).
        \]
        \If{$\zeta_j=(\mathrm{acc},q_f)$}
            \State Record
            $(v_j,\lambda_j,\varepsilon_{ij},
            \textsc{Terminal})$.
        \Else
            \State Record
            $(v_j,\lambda_j,\varepsilon_{ij},
            \textsc{Feasible})$.
        \EndIf
    \EndFor
\EndFor
\State \Return all recorded successor labels.
\end{algorithmic}
\end{algorithm}
```

---

## D. Graph Simplification and Plan Extraction

```latex
\subsection{Graph Simplification and Plan Extraction}

After all retained execution labels have been processed, the
generated label-transition graph is simplified by standard
reachability tests. A forward search identifies the labels
reachable from the root label, and a reverse search from all
terminal labels identifies the labels that can contribute to a
complete accepting prefix--suffix plan. Labels and
label-transition records outside the intersection are removed.
A structural plan node or edge is retained if it is referenced
by at least one retained label transition.

\textbf{Lemma 3 (Preservation under final simplification).}
The final reachability-based simplification preserves every
terminal execution-label chain represented before
simplification.

\emph{Proof.}
Every generated feasible plan corresponds to a predecessor
chain from the root label to a terminal label. Every label on
this chain is root-reachable and can reach that terminal label.
Hence, the forward and backward reachability tests retain the
entire chain and all structural edges referenced by it.
\hfill$\square$

A plan is extracted from a terminal label $\lambda_f$ by
repeatedly following $\operatorname{pred}(\lambda)$ until
$\lambda_0$ is reached and then reversing the resulting
sequence. The incoming edge and assignment stored in each
label provide the NBA transition, induced subtask, and robot
assignment for that step. Therefore, the extracted subtask
sequence, assignment sequence, robot positions, and completion
times all arise from one consistent execution-label chain.

The first terminal label yields $\Pi_{\mathrm{init}}$. After
construction terminates, the lowest-cost terminal label yields
$\Pi_{\mathrm{plan}}$, which is subsequently used to warm-start
the BnB optimizer in Sec.~VII. The value
$\Pi_{\mathrm{plan}}$ is the best plan found by the joint
construction; it is not claimed to be globally optimal for
Problem~1.
```

---

# 7. 推荐删除或压缩的当前内容

## 7.1 删除开头重复句

当前开头对以下内容重复较多：

- “NBA and plan graph are constructed synchronously”；
- “first feasible plan before complete NBA”；
- “score favors promising partial plans”。

Introduction、Contributions 和 System Overview 已经完成动机说明。Sec. VI 开头只需保留：

> input \(G_\phi^{-}\) → joint transition/label expansion → early terminal plan → score only orders retained labels.

---

## 7.2 删除 Definition 8 后的重复解释段

当前 Definition 8 定义完每个 tuple component 后，下一段再次逐项解释：

> \(q_B\), `Prog`, \(\omega\), \(C\), \(X\), \(\Theta\) identify...

这一段可以删除。正式定义已经足够。

---

## 7.3 删除 Algorithm 2 前对 LTL2BA simplification 的教科书式重复

当前再次解释：

> On-the-fly automaton simplification is a key feature of LTL2BA...

Preliminaries 已介绍该规则。本节只需一句：

> The outgoing transitions are simplified by the standard LTL2BA implication/subsumption rule before planning extensions are evaluated.

---

## 7.4 删除 Algorithm 4 `REUSESUCCESSORS`

在 execution-label architecture 下：

- NBA transitions 被 cache；
- 新 execution label 使用 cached transitions 重新扩展；
- 不共享唯一 execution payload；
- 不需要 descendant propagation。

因此 Algorithm 4 可以整体删除。

---

## 7.5 压缩 AST score rules

当前 6 条规则后每条都有自然语言解释。建议只保留递推式和一句总说明：

> This is a syntactic under-approximation used only for ordering.

Example 5 可以保留，但建议压成 3 句。

---

# 8. 当前代码暂时不修改时的最小改动安全路线

如果当前实现必须保留：

- one representative payload per plan node；
- greedy-only assignment；
- scalar-cost representative update；
- `REUSESUCCESSORS`；
- state-level worklist；

则不要采用第 6 节中的 completeness-preserving 表述。至少进行以下修改。

## 8.1 收缩本节定位

开头写：

```latex
The procedure constructs a heuristic plan graph jointly with
the NBA. For each generated NBA transition, a greedy
assignment is evaluated from the representative execution
states currently stored in the plan graph. The resulting graph
therefore contains the task structures and representative
execution contexts discovered by this construction; it is not
claimed to represent every feasible execution context.
```

## 8.2 修改 greedy failure 表述

当前：

> If GREEDYASSIGN fails, the candidate extension is discarded.

可保留算法操作，但正文改成：

```latex
If the greedy assignment fails under the prescribed action and
robot ordering, the candidate extension is not inserted into the
heuristically generated plan graph. This failure does not, in
general, certify that no feasible assignment exists.
```

## 8.3 明确 node reuse 只是 heuristic aggregation

```latex
When several parent contexts reach a compatible plan node,
the implementation stores the context with the smallest current
makespan as its representative execution state. This is a
heuristic aggregation rule rather than a future-cost dominance
test; all optimality and completeness statements are therefore
understood relative to the retained representative contexts.
```

## 8.4 Remaining set 不使用 parent union

至少改为沿 representative predecessor 更新：

\[
M_j
=
M_{\operatorname{par}(\nu_j)}
\setminus
\operatorname{Act}(\omega_j).
\]

这仍然只对应 representative plan，但不会创造不存在的混合 path history。

## 8.5 新 parent edge 不能直接复用 child payload

`REUSESUCCESSORS` 至少需要对新 parent \(\nu_j\) 和每个 cached outgoing NBA transition 重新调用 assignment/state update。不能只增加：

\[
(\nu_j,\nu_h)\in E_P
\]

然后仍使用从另一 parent 得到的 \(C_h,X_h,\Theta_h\)。

## 8.6 修改 solution claim

- \(\Pi_{\mathrm{init}}\)：first plan under greedy construction；
- \(\Pi_{\mathrm{plan}}\)：best plan found among retained representative contexts；
- BnB：best/optimal over the paths retained in the generated plan graph；
- 不称该 graph 覆盖 all feasible plans of Problem 1。

## 8.7 理论结论

当前实现不变时，推荐把 Sec. X 改成：

```latex
Lemma (Construction soundness).
Every plan returned by the on-the-fly construction follows an
accepting NBA prefix--suffix structure and satisfies the
assignment and reachability checks performed by the extension
procedure.

The construction is heuristic because greedy-assignment
failure and representative-state aggregation may omit feasible
execution contexts. Consequently, completeness is stated only
with respect to the labels and edges retained by the generated
plan graph.
```

---

# 9. 与其他章节必须同步修改

## 9.1 Sec. III

统一：

\[
\omega_{ij}
=
(\gamma_{ij},\gamma_i^{\mathrm{hold}}),
\]

\[
\operatorname{Act}(\omega)
\]

以及：

\[
c(a)=(t(a),n(a),\ell(a)).
\]

---

## 9.2 Sec. IV / Algorithm 1

函数名改成：

```latex
\textsc{ConstructNBAAndPlanGraph}
```

并让 Algorithm 1 接收：

\[
(G_P,\Pi_{\mathrm{init}},T_{\mathrm{first}},
\Pi_{\mathrm{plan}}).
\]

---

## 9.3 Sec. VII

BnB 不再读取 child node 中唯一的 \(\omega_j\)，而是对每条 outgoing plan-graph edge
\(\varepsilon_{ij}\) 读取其 subtask \(\omega_{ij}\)。

应增加一句：

```latex
The execution state carried by a BnB node is search-specific
and is independent of the construction-stage execution labels
stored at the corresponding structural plan node.
```

BnB 的最优性继续限定为：

> the accepting paths and assignments retained in \(G_P\).

---

## 9.4 Sec. VIII

online repair 的 new root 应包含：

- current NBA state；
- current suffix phase/anchor；
- actual robot positions；
- current completion/availability times；
- remaining robot team。

它应创建一个新的 runtime execution label，而不是覆盖 original shared plan node。

---

## 9.5 Sec. IX Complexity Analysis

采用 execution labels 后，应区分：

- \(|V_P|\)：logical plan nodes；
- \(|E_P|\)：structural edges；
- \(N_\Lambda\)：evaluated execution labels；
- assignment feasibility / enumeration cost；
- local candidate sorting；
- dominance lookup；
- final label-graph reachability。

不要再只用 number of expanded NBA states 近似整个 construction cost。

---

## 9.6 Sec. X Theoretical Analysis

建议分成三层：

### Soundness

每个 returned plan：

- follows NBA transitions；
- closes a selected suffix anchor；
- has verified assignments；
- satisfies holding/reachability checks。

### Conditional completeness

只有在以下条件都成立时才能声称：

1. Sec. V pruning preserves a feasible accepting execution；
2. no candidate is discarded solely because a greedy assignment fails；
3. all relevant non-dominated execution labels are eventually generated；
4. label dominance is future-feasibility preserving；
5. score affects only ordering；
6. terminal phase exactly represents a return to the chosen suffix root。

### BnB optimality

只声称：

> optimal over the accepting paths and assignments represented in the generated plan graph,

除非进一步证明 \(G_P\) 保留 original problem 的 global optimum。

---

# 10. 推荐的最终写作主线

修改后的 Sec. VI 应向 reviewer 传达下面这一条单一、清楚的逻辑链：

\[
G_\phi^{-}
\]

\[
\Downarrow
\]

\[
\text{generate/cache a new NBA transition}
\]

\[
\Downarrow
\]

\[
\text{form its subtask and verify synchronized assignments}
\]

\[
\Downarrow
\]

\[
\text{propagate each non-dominated execution label}
\]

\[
\Downarrow
\]

\[
\text{order retained successor labels by residual score}
\]

\[
\Downarrow
\]

\[
\text{first terminal label}
\Rightarrow
(\Pi_{\mathrm{init}},T_{\mathrm{first}})
\]

\[
\Downarrow
\]

\[
\text{completed retained graph}
\Rightarrow
(G_P,\Pi_{\mathrm{plan}})
\]

\[
\Downarrow
\]

\[
\text{warm-started BnB refinement and online repair}.
\]

这条主线比当前“plan node + representative predecessor + node reuse + descendant propagation”的叙述更短，也更容易证明。

---

# 11. 最终修改优先级

## 必须优先处理

1. 区分 symbolic guard \(\gamma\) 与 input symbol \(\sigma\)；
2. 修正 \(x_i(r)=l_j\) 的类型错误；
3. 明确 completion time 不早于 parent makespan；
4. 明确 score 只用于 ordering，不用于 pruning；
5. 将 \(\Pi_{\mathrm{init}}\)、\(T_{\mathrm{first}}\)、\(\Pi_{\mathrm{plan}}\) 写入 Algorithm 2 interface；
6. 删除或收缩 “greedy failure means infeasible”；
7. 删除仅按 scalar makespan 覆盖 execution state 的 dominance 暗示；
8. 修正 parent-union remaining set；
9. 精确定义 suffix root；
10. 将 Section VII / X 的 claim 与 generated graph 的真实覆盖范围对齐。

## 强烈建议

11. 采用 logical nodes + execution labels；
12. worklist 改为 label-level；
13. 删除 `REUSESUCCESSORS`，改为 outgoing-transition cache；
14. greedy-first + exact assignment fallback；
15. plan extraction 沿 predecessor-label chain；
16. post-construction simplification 在 label-transition graph 上执行。

## 可选的语言精简

17. 删除 Definition 后的重复解释；
18. 压缩 LTL2BA simplification 介绍；
19. 将 6 条 AST rules 改成一个 cases equation；
20. Example 5 只保留计算结果和 score 作用。

---

## 最终评价

这一节真正值得突出的是：

> **task allocation begins at the moment a usable NBA transition is generated, and the first executable accepting structure can therefore be returned before complete automaton construction.**

当前版本的冗余和逻辑困难，主要来自 shared node 同时存储 logical structure 和 path-dependent execution state。将二者分离后，本节会更像一个严谨的 on-the-fly graph-construction algorithm，而不是依靠 representative-state updates 维持的一组实现规则。与此同时，first-plan latency、score-guided ordering、warm-started BnB 和 online repair 之间的关系也会自然连贯。
