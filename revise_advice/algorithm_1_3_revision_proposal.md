# Algorithm 1–3 修改草案（待用户同意）

本文档仅供审核，尚未改入 `incremental_ltl_new/bare_jrnl_new_sample4.tex`。本轮已执行的修改仅涉及用户列出的正文措辞、空格和数字单位间距。

## 1. 统一使用式 (5) 的阶段更新

令 `UpdateProg(p, q)` 表示现有式 (5) 的结果，不改变该式的数学内容：

| 父节点阶段 p | 后继 q 不属于接受集 | 后继 q 属于接受集 |
| --- | --- | --- |
| pre | pre | suf |
| suf | suf | acc |

`acc` 和 `dead` 不参与后续扩展。正式修改时给现有式 (5) 添加标签 `eq:planning_status_update`，以交叉引用替代硬编码编号。

## 2. Algorithm 1：补齐调用参数

将 `Extend_PlanGraph` 的调用改为：

```latex
\STATE $\nu'\gets\textsc{Extend\_PlanGraph}
(\mathcal V_i^B(p),q_{B,j},\xi_{ij},\mathcal R,\mathcal W)$.
```

这与 Algorithm 2 已声明的输入顺序一致。沿用原稿中 Algorithm 2 对当前计划图的就地更新约定。

## 3. Algorithm 2：替换逻辑草案

以下是拟写入伪代码的完整处理顺序。`C_i`、`X_i`、`Theta_i` 和 `feasible_i` 均为针对当前父节点的局部候选量，不提前修改公共子节点。

```text
Input: parent set V_i^B(p), successor q_B,j, subtask xi_ij, R, W
Output: common child nu', or empty set

V_i^feas(p) <- empty set
for each parent nu_i in V_i^B(p):
    C_i <- empty assignment; U_i <- empty robot set
    feasible_i <- true
    for each action a_l in A(xi_ij):
        compute predicted arrival times for robots of type tau(a_l)
            not already in U_i, using the existing arrival-time equation
        R_i^eli(a_l) <- robots with finite arrival times among these robots
        if |R_i^eli(a_l)| < n(a_l):
            feasible_i <- false
            break the action loop
        C_i(a_l) <- the n(a_l) eligible robots with smallest arrival times
        U_i <- U_i union C_i(a_l)
        t_i(a_l) <- maximum arrival time among C_i(a_l)
    if feasible_i is false:
        continue with the next parent
    if A(xi_ij) is empty:
        t_i(xi_ij) <- J(nu_i); X_i <- nu_i.X; Theta_i <- nu_i.Theta
    else:
        compute t_i(xi_ij) using the existing subtask-completion equation
        obtain X_i and Theta_i from nu_i and C_i using the existing update rule
    save (C_i, X_i, Theta_i, t_i(xi_ij)) for this parent
    V_i^feas(p) <- V_i^feas(p) union {nu_i}

if V_i^feas(p) is empty:
    return empty set

nu_star <- parent in V_i^feas(p) with smallest t_i(xi_ij)
           (retain the manuscript's first-evaluated tie-break rule)
create nu'
nu'.q_B <- q_B,j; nu'.xi <- xi_ij
nu'.Prog <- UpdateProg(nu_star.Prog, q_B,j), using Eq. (5)
(nu'.C, nu'.X, nu'.Theta) <- saved candidate values for nu_star
par(nu') <- nu_star
insert nu' into V_P
add (nu_i, nu') to the plan-graph edge set for every nu_i in V_i^feas(p)
return nu'
```

对应修复：

- 定义、初始化并填充可行父节点集合。
- 输入为空或所有父节点不可行时，均在选择代表父节点前返回空集。
- 单个父节点失败只丢弃该候选，不将公共子节点标记为 `dead`；失败候选不会继续计算子任务完成时间。
- 显式保存每个父节点的分配结果，保证最后复制的是所选代表父节点的结果。
- 显式填写后继 NBA 状态、子任务和按式 (5) 更新的阶段，供 Algorithm 1 读取。
- 增加空动作集合的边界处理，避免在子任务完成时间公式中对空集取最大值；此项也包含在待审核范围内。

## 4. Algorithm 3：修正兼容后继的筛选

对每条实际 NBA 出边 `(q_B,j, sigma_jh, q_B,h)`，先获取其诱导子任务 `xi_jh`，再计算

```latex
\STATE $p_h\gets\textsc{UpdateProg}(\nu_j.\mathrm{Prog},q_{B,h})$
       according to Eq.~\eqref{eq:planning_status_update}.
```

将原来的 `nu_h.Prog = nu_j.Prog` 改为 `nu_h.Prog = p_h`。兼容集合建议完整写成：

\[
\begin{aligned}
\mathcal V_h=\{\nu_h\in V_P\mid{}&
\nu_h.q_B=q_{B,h},\quad \nu_h.\xi=\xi_{jh},\quad
\nu_h.\mathrm{Prog}=p_h,\\
&\exists\nu_\ell\in V_P:\quad
\nu_\ell.q_B=q_{B,j},\quad
\nu_\ell.\mathrm{Prog}=\nu_j.\mathrm{Prog},\quad
(\nu_\ell,\nu_h)\in\rightarrow_P\}.
\end{aligned}
\]

这样既检查式 (5) 所要求的后继阶段，也保留正文“由相同父 NBA 状态、相同父阶段生成的后继”的含义。检查 `xi_jh` 是为了区分终点相同但标签或诱导子任务不同的出边。

正文中目前重复出现的条件 `nu_h.Prog = nu_j.Prog` 也应同步改为上述更新结果，避免只改算法而留下相同的文字错误。

## 5. 建议一并纳入审核的两处衔接

这两项超出了单纯替换阶段等号，但与修正后的控制流程直接相关，尚未写入论文：

1. **没有兼容后继时。** `q_B,j` 已展开，只能证明它的 NBA 出边已经生成，不能保证当前父阶段对应的计划节点已经存在。如果 `V_h` 为空，建议调用修正后的 `Extend_PlanGraph({nu_j}, q_B,h, xi_jh, R, W)` 创建后继。创建成功后，按 Algorithm 1 的相同规则处理：`acc` 节点用于更新解；后继 NBA 状态已展开则复用其出边；未展开则更新分数并加入待处理状态集合。只复用已生成的 NBA 出边，无须重新生成自动机出边。
2. **复用到达 acc 时。** 新建或改进 `acc` 节点后，应调用 `Extract_Plan`，按现有成本比较规则更新 `Pi_plan`，并停止从该节点递归。否则，即使改正筛选，Algorithm 1 也可能无法收到复用过程中找到的更优接受解。建议将 `Pi_plan` 和待处理 NBA 状态集合显式列为 Algorithm 3 的就地更新对象，并同步调整 Algorithm 1 的调用及递归调用。

## 6. 审核后应检查的情况

- 父节点集合为空；全部父节点不可行；第一个父节点失败而后续父节点可行。
- 多个可行父节点时，公共子节点的分配与代表父节点一致，同一子任务内机器人集合互不重叠。
- 空动作子任务保留父节点的执行状态。
- 表格所列四种阶段转换均可通过兼容性筛选，尤其是 `pre -> suf` 和 `suf -> acc`。
- 同一终点但不同诱导子任务不会错误复用。
- 没有兼容后继时能补建；接受节点能更新解且不再递归。

**批准范围建议：Algorithm 1 的参数传递、Algorithm 2 的完整候选与失败处理、Algorithm 3 的阶段筛选及上述两处衔接、对应正文说明和算法行号引用。**
