# 实验部分审稿式修改方案与直接替换稿

## 0. 总体判断

当前论文的实验覆盖面其实较完整，已经包含：

1. BnB 搜索行为；
2. GBA-level pruning 与 on-the-fly plan-graph construction 的消融；
3. residual-obligation score 对 first-solution quality 的影响；
4. 与 poset-based 和 MILP-based 方法的 scalability comparison；
5. robot unavailability 下的 online repair；
6. TurtleBot3 实物验证。

因此，当前实验部分的主要问题不是“缺少实验类型”，而是**实验组织尚未完全围绕论文前文提出的研究问题展开**。目前读者需要自己从五个实验中推断：

- 哪个实验在验证“task allocation 前移到 NBA generation”；
- 哪个实验在验证 GBA pruning；
- 哪个实验在验证 residual-obligation score；
- 哪个实验在验证 retained plan graph 对 BnB 和 repair 的价值；
- 哪些结论只是当前实例上的现象，哪些结论有跨任务、跨规模的证据。

从审稿人的角度，最需要修改的是以下五点：

1. **实验顺序与论文创新主线不一致。**  
   论文的第一核心问题是 time to the first executable plan，但实验首先从 BnB 开始，容易使读者误以为 BnB 是主要贡献。

2. **实验问题没有显式提出。**  
   每节虽然说明“we evaluate…”，但没有形成统一的 evaluation questions，导致结论与 Introduction/Contributions 的对应关系不够直接。

3. **若干结果存在过度概括。**  
   例如，score-guided first plans 与所报告 optimum 的差距在四个任务上约为 \(1.8\%\)–\(22.0\%\)，因此不能笼统表述为“均接近 global optimum”；scalability table 主要证明 first-plan latency 优势，而不能证明在所有设置下 exhaustive search 都最快。

4. **实验协议不够集中、部分统计信息缺失。**  
   当前没有统一定义 \(T_{\mathrm{first}}\)、\(T_{\mathrm{plan}}\)、\(T_{\mathrm{best}}\)、\(T_{\mathrm{search}}\) 的计时起点和终点，也没有集中说明 random seeds、obstacle density、baseline implementation、solver settings 和 timeout。Fig. 4 显示 median/min--max curves，但正文未明确 trial count。

5. **repair 和 hardware evidence 仍偏 case-study。**  
   当前 repair 只有一个 robot-unavailability configuration，且没有“reuse retained graph vs. rebuild from scratch”的直接对照；实物部分展示了代表性成功执行，但没有 repeated-trial success rate。因此它们可以支持 feasibility demonstration，却暂时不能单独支持广泛的 robustness/superiority claim。

最适合本文的实验叙事不是按算法章节顺序逐项展示，而是围绕以下证据链组织：

\[
\boxed{
\text{serial front end causes delay}
}
\]

\[
\Downarrow
\]

\[
\boxed{
\text{early GBA pruning + joint NBA/allocation reduce }
T_{\mathrm{first}}
}
\]

\[
\Downarrow
\]

\[
\boxed{
\text{score guidance preserves early availability while improving quality}
}
\]

\[
\Downarrow
\]

\[
\boxed{
\text{retained graph supports subsequent BnB improvement}
}
\]

\[
\Downarrow
\]

\[
\boxed{
\text{the advantage persists with task/team scale and enables rapid repair}
}
\]

\[
\Downarrow
\]

\[
\boxed{
\text{the resulting plans are executable on physical robots}
}
\]

---

# 1. 三篇参考论文中最值得借鉴的实验写法

## 1.1 *From Ambiguous Language to Verifiable Plans*

这篇论文最值得借鉴的是 **question-driven evaluation**。其评估部分明确使用 Q1、Q2、Q3 将每组实验绑定到一个研究问题，并且每个 subsection 开头直接说明：

> To address question Qx, we evaluate whether...

此外，它还采用：

- component-wise ablation；
- matched experimental conditions；
- static → dynamic → long-horizon 的渐进式实物验证；
- success rate、recovery time 和 trial count；
- 对跨系统 comparison 的公平性边界作明确说明。

### 对本文的启发

你的实验也应该先提出明确问题，而不是直接进入 BnB example。最适合本文的问题是：

- **Q1:** 将 allocation 前移到 automaton generation 是否减少 first-plan latency？
- **Q2:** GBA pruning 和 residual-obligation ordering 分别贡献了什么？
- **Q3:** retained plan graph 是否支持有效的 subsequent refinement？
- **Q4:** 该优势是否随 task/team scale 保持？
- **Q5:** retained graph 是否能在 robot unavailability 后快速产生 continuation plan，并在真实机器人上执行？

需要借鉴的是“问题—实验—证据—结论”的结构，而不是其具体模块名称或表格形式。

---

## 1.2 *An Exploration-Enhanced Search Algorithm for Robot Indoor Source Searching*

这篇论文的实验设计强调：

- 明确的 scenario taxonomy；
- 每个 scenario 大量重复运行；
- success rate 与 efficiency metric 同时报告；
- 不只给总体均值，还解释方法为何在某类场景有效或失效；
- simulation 与 real-world experiment 采用一致的任务分类。

### 对本文的启发

你的 scalability 和 online-repair 实验不应只报告几个大表格，而应说明：

- 哪类 LTL structure 对应 sequential、concurrent、alternative 和 recurring obligations；
- 哪类结构主要增加 automaton-front-end cost；
- 哪类结构主要增加 assignment combinatorics；
- 方法在什么情况下仍会出现 timeout 或 first-plan quality degradation。

也就是说，结果分析应从“数值更小”进一步走向：

> **结果变化是否与本文提出的计算瓶颈和技术机制相吻合？**

---

## 1.3 *Temporal Logic Task Allocation in Heterogeneous Multirobot Systems*

这篇与你的研究方向最接近。它把 numerical experiments 分成：

1. suboptimality；
2. quality of the first solution；
3. scalability。

每一个 case study 只回答一个问题，并且对结果边界比较诚实，例如明确说明 first solution 通常质量较好，但并非所有 specification 都是 first solution 最优。

### 对本文的启发

你的 experiment sections 也应避免把多个结论混在同一张表中。例如当前 Table III 同时承载：

- score ordering；
- first-plan quality；
- GBA pruning ratio；
- plan-graph size；
- reported optimum。

建议正文分析时严格拆开：

- score 是否改善 first plan；
- first plan 与 construction-stage incumbent 的差距；
- pruning 对结构规模的影响；
- BnB 后续还能改善多少。

---

# 2. 建议建立的“前文主张—实验证据”对应关系

| 前文主张 | 应回答的问题 | 当前证据 | 审稿判断 |
|---|---|---|---|
| allocation during NBA generation reduces first-plan latency | Q1 | Table I: proposed vs delayed allocation | 证据直接，但应使用 descriptive variant names |
| GBA-level pruning prevents unnecessary transitions from propagating | Q2a | Table II: full vs pruned NBA transition counts | 证据较强，应报告 reduction percentage |
| residual-obligation score improves early-plan quality | Q2b | Table III: discovery order vs score-guided order | 证据直接，但不能笼统说均接近 optimum |
| \(\Pi_{\mathrm{plan}}\) provides a useful BnB warm start | Q3 | Fig. 4 shows incumbent improvement and pruning | 只证明 BnB 有效，**尚未隔离 warm-start contribution** |
| method scales better to usable solutions | Q4 | Table IV comparisons | first-plan latency 证据强；exhaustive-search superiority 不统一 |
| retained graph enables fast repair | Q5a | 25 runs of one failure instance | 能支持该实例下的 rapid repair；缺少 rebuild baseline 和 scenario diversity |
| plans are physically executable | Q5b | nominal and one failure TurtleBot demonstration | 支持 feasibility demonstration；缺少 repeated success statistics |
| theory is sound/complete | theoretical question | Sec. X | 实验不能“证明” soundness/completeness，只能验证 implementation behavior |

---

# 3. 最推荐的实验章节结构

建议将 Numerical Experiments 重组为：

```text
XI. NUMERICAL EXPERIMENTS
    A. Evaluation Questions and Common Protocol
    B. Contributions of Early GBA Pruning and Joint Construction
    C. First-Plan Quality under Residual-Obligation Ordering
    D. Branch-and-Bound Refinement
    E. Scalability against Representative Baselines
    F. Repair under Robot Unavailability

XII. PHYSICAL-ROBOT EXPERIMENTS
    A. Platform and Protocol
    B. Nominal LTL-MRTA Execution
    C. Execution and Repair under Robot Unavailability
```

### 为什么 BnB 不应放在第一个实验

论文最核心的创新是：

> task allocation begins while the NBA is being generated.

所以实验部分首先应证明：

1. conventional serial front end 确实带来 latency；
2. joint construction 的确减少 \(T_{\mathrm{first}}\)；
3. GBA pruning 进一步减少前端结构和时间。

BnB 是 first plan 之后的 refinement，应当在前两项之后出现。

---

# 4. 建议统一定义的 evaluation questions

建议在 Numerical Experiments 开头直接写：

```latex
The experiments address the following questions:

\textbf{Q1:} Does performing robot allocation during NBA
generation reduce the time to the first feasible plan compared
with a serial automaton-then-allocation pipeline?

\textbf{Q2:} How do GBA-level pruning and residual-obligation
ordering affect the generated structure, first-plan latency, and
first-plan quality?

\textbf{Q3:} How effectively does the retained plan graph
support subsequent BnB refinement?

\textbf{Q4:} How does the method scale with task complexity
and robot-team size relative to representative poset- and
MILP-based approaches?

\textbf{Q5:} Can the retained plan graph produce a feasible
continuation rapidly after robot unavailability, and can the
resulting plans be executed by physical robots?
```

这五个问题与前文形成直接对应：

| Evaluation question | Introduction / Contribution |
|---|---|
| Q1 | serial translation-allocation bottleneck；joint co-construction |
| Q2 | planning-aware GBA reduction；residual-obligation score |
| Q3 | plan-graph-based refinement |
| Q4 | large-scale LTL-MRTA motivation |
| Q5 | reusable graph for online repair and execution |

---

# 5. Common Protocol 必须补充的内容

当前实验设置分散在各节。建议增加统一 subsection，至少说明以下内容。

## 5.1 计时指标

建议统一定义：

\[
T_{\mathrm{first}}
\]

从输入原始 LTL formula 并开始 translation 起，到第一个 executable accepting prefix--suffix plan 可用为止。

\[
T_{\mathrm{plan}}
\]

从 planning 开始，到 joint NBA--plan-graph construction 完成并得到
\(\Pi_{\mathrm{plan}}\) 为止。

\[
T_{\mathrm{best}}
\]

从 planning 开始，到最终报告的 best incumbent 首次被发现为止。

\[
T_{\mathrm{search}}
\]

从 planning 开始，到完整搜索结束、timeout 或 memory limit 为止。

必须说明：

- 是否包含 LTL parsing、VWAA、GBA、NBA generation；
- 是否包含 shortest-path preprocessing；
- 是否包含 BnB；
- baseline 的 preprocessing 是否同样计入。

因为本文主张的就是 front-end latency，若不说明计时起点，核心 comparison 会缺乏可解释性。

---

## 5.2 质量指标

建议统一：

\[
J_{\mathrm{first}}
=
J_\phi(\Pi_{\mathrm{init}}),
\]

\[
J_{\mathrm{plan}}
=
J_\phi(\Pi_{\mathrm{plan}}),
\]

\[
J_{\mathrm{best}}
=
J_\phi(\Pi^\star).
\]

并报告 relative gap：

\[
\mathrm{Gap}_{\mathrm{first}}
=
\frac{
J_{\mathrm{first}}-J_{\mathrm{ref}}
}{
J_{\mathrm{ref}}
}\times 100\%.
\]

### `global optimum` 的命名必须谨慎

若 \(J_{\mathrm{ref}}\) 仅由 retained plan graph 上完整 BnB 得到，应写：

\[
J^\star_{G_P}
\]

并称：

> graph-optimal cost over the path-and-assignment space retained in \(G_P\).

只有在通过 independent exhaustive search、MILP 或另一种能够覆盖原始 Problem 1 全部可行解的过程认证后，才能写：

\[
J^\star_{\mathrm{global}}.
\]

---

## 5.3 统计协议

建议补充：

- 每个 configuration 的 trial 数；
- random seed；
- obstacle density / generation process；
- initial robot position sampling rule；
- 是否使用 paired instances；
- reported statistic：median [IQR] 或 mean \(\pm\) standard deviation；
- timeout 后如何计入统计；
- success rate；
- 对随机算法是否固定 seed；
- code/solver version 和 key parameters。

当前 ablation 已经采用“相同 robot initial positions reused across methods”，这是正确的 paired design，应明确写成 protocol，而不是埋在正文中。

---

## 5.4 Baseline fairness

对于 poset 和 MILP baselines，建议说明：

- 使用 authors' public implementation、authors' code，还是 reimplementation；
- hardware、language、solver；
- 是否包含 automaton preprocessing；
- stopping criterion；
- 是否允许 early return；
- 是否使用同一 motion-cost oracle；
- inability/timeout 如何记录。

若 baseline architecture 不同，应明确：

> The comparison is an end-to-end matched-instance comparison rather than a component-wise comparison.

---

# 6. 基于当前数据应怎样重新解释结果

## 6.1 On-the-fly construction 与 GBA pruning

当前三种设置建议重命名为：

| 当前名称 | 推荐名称 | 保留/移除的机制 |
|---|---|---|
| Proposed | **Full / Ours** | early GBA pruning + allocation during NBA generation |
| Case I | **Delayed Allocation** | early GBA pruning；等待 complete NBA 后 allocation |
| Case II | **Post-NBA Pruning and Allocation** | complete NBA 后才 pruning 和 allocation |

这样的命名使消融关系一目了然：

- `Full vs Delayed Allocation`：隔离 joint on-the-fly allocation；
- `Delayed Allocation vs Post-NBA Pruning and Allocation`：隔离 early GBA pruning；
- `Full vs Post-NBA...`：完整框架相对 serial pipeline 的总体收益。

### 当前数据可支持的精确结论

对于 \(m=12,\ldots,15\)：

- Full 相对 Delayed Allocation 将 \(T_{\mathrm{first}}\) 降低约：
  \[
  18.1\%,\,42.2\%,\,28.2\%,\,30.2\%.
  \]
- Delayed Allocation 相对 Post-NBA variant 将 \(T_{\mathrm{first}}\) 降低约：
  \[
  6.5\%,\,22.4\%,\,9.4\%,\,16.1\%.
  \]
- 完整方法相对 Post-NBA serial variant 降低约：
  \[
  23.5\%\text{--}55.2\%.
  \]
- early GBA pruning 将后续 NBA transition 数减少约：
  \[
  53.3\%\text{--}60.0\%.
  \]

### 这组实验真正证明什么

它支持两个彼此独立的因果判断：

1. 即使 final pruned NBA 相同，**提前使用 robot-team feasibility** 仍能避免先生成再删除大量 transitions；
2. 即使使用同样的 early pruning，**让 allocation 与 NBA generation 重叠** 仍能进一步减少 first-plan latency。

这正好对应 Introduction 中的两个成因：

- planning-unaware front end；
- serial translation-allocation pipeline。

### 不应声称什么

不要写：

> the proposed method avoids exponential growth.

更准确的是：

> it does not change the worst-case exponential complexity of LTL-to-NBA translation, but substantially reduces the intermediate transition structure and the observed first-plan latency.

---

## 6.2 Residual-obligation score

当前四个任务上，score-guided order 相对 discovery order 将 first-plan cost 降低约：

\[
8.5\%,\,7.2\%,\,14.7\%,\,15.4\%.
\]

其 first-plan cost 与 \(\Pi_{\mathrm{plan}}\) 的差距为：

\[
0\%,\,0\%,\,1.8\%,\,4.5\%.
\]

这是一组很有说服力的结果，可以支持：

> score improves the solution encountered early, without requiring completion of the plan graph.

但相对表中 reported optimum 的差距约为：

\[
22.0\%,\,9.3\%,\,1.8\%,\,20.4\%.
\]

因此当前：

> the first feasible plans remain close to the corresponding global optima

应改成更准确的：

> The score-guided first plans are consistently better than
> those obtained in the original discovery order and remain
> within \(0\%\)–\(4.5\%\) of the best plans found during joint
> construction. Their gaps to the reported reference optima vary
> across task structures, from \(1.8\%\) to \(22.0\%\), showing
> that the score is effective as an early-ordering heuristic but
> does not eliminate the need for subsequent refinement.

这段分析更加可信，也能自然引出 BnB。

---

## 6.3 BnB experiment

当前 example 中：

\[
J_{\mathrm{plan}}=47.21\ \mathrm{s},
\qquad
J_{\mathrm{best}}=43.32\ \mathrm{s},
\]

即 BnB 将 incumbent 改善约：

\[
8.24\%.
\]

同时：

\[
\frac{122362}{138145}\times100\%
=
88.57\%
\]

的 visited assignment nodes 被 lower-bound pruning 删除。

这支持：

- \(\Pi_{\mathrm{plan}}\) 是一个有效 incumbent；
- lower bound 可显著减少实际搜索；
- retained graph 可用于 continued refinement。

### 当前实验没有单独证明什么

它尚未证明：

> warm starting is better than starting BnB without \(\Pi_{\mathrm{plan}}\).

因为没有 no-warm-start ablation。

### 强烈建议增加

比较：

1. warm start with \(\Pi_{\mathrm{plan}}\)；
2. no seed (\(J^\star=+\infty\))；
3. optional random/first feasible seed。

报告：

- time to first finite incumbent；
- time to best incumbent；
- nodes expanded；
- pruning ratio；
- final cost；
- timeout gap。

这会直接支撑 Contributions 中 “\(\Pi_{\mathrm{plan}}\) warm-starts BnB” 的价值。

---

## 6.4 Scalability

当前 Table IV 能支持一项非常强的结论：

- proposed \(T_{\mathrm{first}}\)：约 \(0.31\)–\(1.78\) s；
- poset \(T_{\mathrm{first}}\)：约 \(17.12\)–\(270.42\) s；
- MILP \(T_{\mathrm{first}}\)：约 \(6.50\)–\(483.97\) s。

对应 first-plan speedup 大致为：

- 相对 poset：
  \[
  40.8\times\text{--}201.5\times;
  \]
- 相对 MILP：
  \[
  16.7\times\text{--}271.9\times.
  \]

对于完成搜索的 instances，各方法最终达到相同 \(J_{\mathrm{best}}\)，说明本文显著提前获得 usable plan，同时没有在这些 completed instances 上牺牲最终 best cost。

### 需要保留的审稿式边界

- proposed first-plan cost 并不在所有 configuration 上都优于 poset；
- proposed \(T_{\mathrm{search}}\) 也并非在所有 configuration 上最小；
- 某些 largest instances 中不同方法出现不同 timeout pattern。

因此最准确的结论是：

> The strongest advantage is time to a usable feasible plan
> and anytime refinement, rather than uniformly faster exhaustive
> certification in every instance.

这种表述不会削弱论文，反而使核心优势更清楚。

---

## 6.5 Online repair

当前 fixed scenario 中：

\[
T_{\mathrm{repair,first}}
=
45.74\ \mathrm{ms},
\]

\[
T_{\mathrm{repair,best}}
=
390.32\ \mathrm{ms}.
\]

该结果能够支持：

> retained \(G_P\) can be re-rooted and reused to produce a feasible continuation rapidly in the demonstrated robot-unavailability event.

但暂时不能支持：

> the method is generally faster than replanning from scratch.

因为没有 reconstruction baseline。

### 强烈建议增加

至少测试：

- failure time：early / middle / late；
- unavailable robot：assigned / currently idle；
- robot type：abundant / scarce；
- loss of one vs multiple robots；
- remaining task feasible vs infeasible；
- different task structures。

比较：

1. retained-graph repair；
2. full LTL-to-automaton reconstruction；
3. optional local reassignment-only baseline。

报告：

- repair success rate；
- \(T_{\mathrm{repair,first}}\)；
- \(T_{\mathrm{repair,best}}\)；
- repaired cost increase；
- number of graph nodes re-expanded；
- infeasibility detection time。

---

# 7. Table 和 Figure 的具体修改建议

## 7.1 Table I–II：建议合并或形成相邻的 paired ablation

推荐列：

| \(m\) | Variant | \(T_{\mathrm{first}}\) | NBA states | NBA transitions generated | transitions retained | transition reduction |
|---|---:|---:|---:|---:|---:|---:|

这样读者不必跨两张表推断：

- 时间收益来自哪里；
- 是否生成了额外结构；
- final pruned automaton 是否相同。

---

## 7.2 Table III：增加 relative gaps

建议增加：

\[
\Delta_{\mathrm{score}}
=
\frac{J_{\mathrm{disc}}-J_{\mathrm{first}}}
{J_{\mathrm{disc}}}\times100\%,
\]

\[
\mathrm{Gap}_{\mathrm{plan}}
=
\frac{J_{\mathrm{first}}-J_{\mathrm{plan}}}
{J_{\mathrm{plan}}}\times100\%,
\]

\[
\mathrm{Gap}_{\mathrm{ref}}
=
\frac{J_{\mathrm{first}}-J_{\mathrm{ref}}}
{J_{\mathrm{ref}}}\times100\%.
\]

这样“score improves early quality”和“first plan 还需要多少 refinement”可以直接读出。

---

## 7.3 Fig. 4：改成具有 optimality meaning 的曲线

当前图中的 node UB/LB 很噪声，而且 caption 中说 curves 为 medians/min--max，但正文没有明确 trials。

更推荐画：

- incumbent cost：
  \[
  J^\star(k);
  \]
- open queue minimum lower bound：
  \[
  \underline J_Q(k)=\min_{\mu\in Q_k}LB(\mu);
  \]
- optional optimality gap：
  \[
  J^\star(k)-\underline J_Q(k).
  \]

这样图能够直接说明：

- warm start 给出初始 upper bound；
- incumbent 如何改善；
- lower bound 如何收敛；
- 何时获得 graph-relative optimality certificate。

若保留现图，caption 必须把 `UB` 和 `LB` 称为：

> bounds of the expanded search nodes,

不能让读者误以为它们是 global incumbent/open-frontier bounds。

---

## 7.4 Table IV：按 latency、quality、completion status 分组

当前表列较多。建议将每个 method 的指标统一为：

- solved / timeout；
- \(T_{\mathrm{first}}\)；
- \(J_{\mathrm{first}}\)；
- \(T_{\mathrm{best}}\)；
- \(J_{\mathrm{best}}\)；
- \(T_{\mathrm{search}}\)。

所有 timeout 使用统一标记，并在 caption 说明：

> \(J_{\mathrm{best}}\) is the best incumbent before timeout.

---

## 7.5 Repair table

当前 repair 只有正文数字。建议新增 table：

| Failure scenario | Method | Repair SR | \(T_{\mathrm{first}}\) | \(T_{\mathrm{best}}\) | repaired cost | search status |
|---|---|---:|---:|---:|---:|---|

---

## 7.6 Physical figures

Fig. 7/8 的 frame sequence 应在 caption 中明确：

- 当前 active subtask；
- assigned robots；
- proposition / automaton progress；
- failure injection time；
- reassigned robot；
- completion event。

不要只用“robot travels to...”的流水账。图应该承担验证 temporal order、collaboration 和 repair 的作用。

---

# 8. 推荐的 Numerical Experiments 完整替换稿

## 使用说明

下面英文稿基于当前论文已经报告的数据编写。以 `[TO REPORT: ...]` 标出的内容在 PDF 中没有足够信息，投稿前需要根据代码和实验记录补充，不能凭空填写。

同时，下面使用：

\[
J^\star_{G_P}
\]

表示 retained plan graph 上经完整 BnB 认证的 optimum。若你已经通过独立 exhaustive method 证明其为 Problem 1 的 true global optimum，可以统一改为 \(J^\star_{\mathrm{global}}\)。

---

## XI. NUMERICAL EXPERIMENTS

```latex
\section{Numerical Experiments}

This section evaluates the proposed framework with respect to
the computational bottlenecks and capabilities identified in
Sec.~I. The experiments address five questions:

\textbf{Q1:} Does performing task allocation during NBA
generation reduce the time to the first feasible plan compared
with a serial automaton-then-allocation pipeline?

\textbf{Q2:} How do GBA-level pruning and
residual-obligation ordering affect the generated structure,
first-plan latency, and first-plan quality?

\textbf{Q3:} How effectively does the retained plan graph
support subsequent BnB refinement?

\textbf{Q4:} How does the framework scale with task
complexity and robot-team size relative to representative
poset- and MILP-based methods?

\textbf{Q5:} Can the retained plan graph produce a feasible
continuation rapidly after the available robot team changes?

All algorithms are implemented in Cython~0.29.24 and
evaluated on a workstation with a 3.40-GHz Intel Core
i7-11390H CPU and 16~GB RAM. Unless stated otherwise, the
experiments use the $40\,\mathrm{m}\times40\,\mathrm{m}$
warehouse in Fig.~1. Obstacles are generated
[TO REPORT: obstacle density and generation rule], and robot
initial positions are sampled
[TO REPORT: sampling rule]. The same generated instance,
including the obstacle map, robot positions, and robot
parameters, is reused across methods within each paired trial.

We measure planning time from the moment the input LTL
formula is submitted, so that LTL parsing, GBA/NBA
generation, task allocation, and the applicable optimization
stages are included. Specifically, $T_{\mathrm{first}}$ is the
elapsed time until the first executable accepting
prefix--suffix plan $\Pi_{\mathrm{init}}$ becomes available;
$T_{\mathrm{plan}}$ is the time until joint NBA--plan-graph
construction finishes and returns $\Pi_{\mathrm{plan}}$;
$T_{\mathrm{best}}$ is the time at which the reported best
incumbent is first found; and $T_{\mathrm{search}}$ is the time
until exhaustive termination or the common
$20\,000$-s timeout. Plan quality is measured by the
makespan $J_\phi$ in (3).

[TO REPORT: For every experiment, state the number of trials,
random seeds, reported statistic (e.g., median and IQR or mean
and standard deviation), treatment of timeouts, and success
rate.]
```

---

## A. Effects of Early GBA Pruning and Joint Construction

```latex
\subsection{Effects of Early GBA Pruning and Joint Construction}

We first answer Q1 and the pruning component of Q2. The
experiment uses the patrol family
\[
\phi_m=\bigwedge_{i=1}^{m}\Diamond a_i,
\qquad
m\in\{12,13,14,15\},
\]
so that increasing $m$ systematically increases the number of
temporal obligations and the size of the generated automaton.
For $i=1,\ldots,8$,
$c(a_i)=(1,3,l_i)$, whereas for
$i=9,\ldots,15$, $c(a_i)=(2,3,l_{i-8})$.
The team contains five robots of each type. Each configuration
is run 25 times, and the same robot initial positions are reused
across all variants in a paired trial.

We compare three variants:

1) \emph{Full (ours):} team-aware GBA pruning is performed
before degeneralization, and task allocation begins as NBA
transitions are generated;

2) \emph{Delayed allocation:} the same GBA pruning is
retained, but task allocation and plan-graph construction begin
only after the complete pruned NBA has been generated; and

3) \emph{Post-NBA pruning and allocation:} the complete
unpruned NBA is generated before redundant transitions are
removed and task allocation begins.

The comparison between the first two variants isolates the
effect of overlapping allocation with NBA generation. The
comparison between the latter two isolates the effect of moving
the pruning operation ahead of complete NBA generation.

Table~I shows that the full framework obtains the first feasible
plan earlier than delayed allocation for every tested value of
$m$. The reductions in $T_{\mathrm{first}}$ are
$18.1\%$, $42.2\%$, $28.2\%$, and $30.2\%$ for
$m=12,\ldots,15$, respectively. Thus, even when both
variants use the same pruned GBA, beginning allocation from
newly available NBA transitions removes a serial wait from the
critical path to the first executable plan.

Early GBA pruning provides a separate benefit. Relative to
post-NBA pruning and allocation, applying the same reduction
before degeneralization removes $53.3\%$--$60.0\%$ of the
NBA transitions that would otherwise be generated and stored.
Consequently, delayed allocation with early pruning reduces
$T_{\mathrm{first}}$ by $6.5\%$--$22.4\%$ relative to the
post-NBA variant. Combining both mechanisms yields an overall
$23.5\%$--$55.2\%$ reduction in first-plan latency.

These results separate the two causes discussed in Sec.~I:
planning-unaware automaton generation propagates unnecessary
structure, whereas a serial translation-allocation pipeline
prevents allocation from using temporal progress that is already
available. Early GBA pruning addresses the former, and joint
NBA--plan-graph construction addresses the latter. The
experiment does not claim to change the worst-case exponential
complexity of LTL-to-NBA translation; rather, it demonstrates
a substantial reduction in the intermediate transition structure
and observed first-plan latency.
```

### 推荐 Table I caption

```latex
\caption{Paired ablation of early GBA pruning and task
allocation during NBA generation. $T_{\mathrm{first}}$ includes
the complete front-end processing from the input LTL formula
to the first executable accepting plan. ``Generated'' denotes
the transitions materialized before pruning, whereas
``retained'' denotes those passed to downstream planning.
Values are [TO REPORT: statistic] over 25 paired trials.}
```

---

## B. First-Plan Quality under Residual-Obligation Ordering

```latex
\subsection{First-Plan Quality under Residual-Obligation Ordering}

We next address the ordering component of Q2. The purpose of
the residual-obligation score is not to certify optimality, but to
make a lower-cost accepting branch available early during joint
construction. We evaluate four specifications containing
different combinations of sequential, concurrent, alternative,
and recurring task requirements:
[retain the four formulas and their concise semantic
descriptions from the current manuscript].

For every specification, we compare the first plan obtained in
the original LTL2BA discovery order with the score-guided
first plan $\Pi_{\mathrm{init}}$. We additionally report the best
construction-stage plan $\Pi_{\mathrm{plan}}$ and the reference
cost $J^\star_{G_P}$ obtained after exhaustive BnB search on
the retained plan graph. The same workspace, robot team, and
initial states are used in all ordering variants.

As shown in Table~III, residual-obligation ordering reduces
the first-plan cost by $7.2\%$--$15.4\%$ relative to the
original discovery order. The absolute difference in first-plan
time is small for the tested instances
([TO REPORT or retain the tabulated values]: from $-0.01$ to
$0.08$~s), indicating that the quality improvement does not
require waiting for complete graph construction.

The score-guided first plans are identical to
$\Pi_{\mathrm{plan}}$ for $\phi_1$ and $\phi_2$ and are within
$1.8\%$ and $4.5\%$ for $\phi_3$ and $\phi_4$,
respectively. Hence, the ordering heuristic usually exposes
most of the construction-stage solution quality in the first
accepting plan. The gaps to $J^\star_{G_P}$ vary more
substantially, from $1.8\%$ to $22.0\%$. This variation is
expected because the score estimates residual travel burden but
does not enumerate all future path and assignment choices.
The results therefore support the score as an effective
early-ordering heuristic while also motivating the subsequent
BnB refinement in Sec.~VII.
```

### 推荐避免的原句

不要写：

```latex
the first feasible plans remain close to the corresponding
global optima
```

建议写：

```latex
the first feasible plans are consistently improved relative to
the original discovery order and are close to the best
construction-stage plans, while their gaps to the graph-optimal
reference vary with task structure.
```

---

## C. Branch-and-Bound Refinement

```latex
\subsection{Branch-and-Bound Refinement}

This experiment addresses Q3 by examining whether the
retained plan graph supports effective post-construction
refinement. We use the warehouse cargo-handling and
safety-inspection task
[retain the formula and action requirements from the current
manuscript]. Robot initial positions are sampled randomly in
the workspace.

The construction-stage plan provides the initial BnB incumbent
with
\[
J_{\mathrm{plan}}=47.21~\mathrm{s}.
\]
Because this upper bound is available before exact search
begins, nodes with lower bounds no smaller than
$47.21$~s can be discarded immediately. The first pruning
event occurs after $0.29$~s. Feasible completions subsequently
tighten the incumbent, and the best plan is first found after
$2.37$~s with
\[
J_{\mathrm{best}}=43.32~\mathrm{s},
\]
an $8.24\%$ makespan reduction relative to
$\Pi_{\mathrm{plan}}$.

Overall, the search prunes $122\,362$ of the $138\,145$
visited assignment nodes, corresponding to a pruning ratio of
$88.57\%$. These results demonstrate that the plan graph is
not only an early-solution representation: it also provides a
search domain in which feasible incumbents and lower bounds
can be combined to reduce subsequent assignment search.

Figure~4 should distinguish the incumbent upper bound
$J^\star(k)$ from the minimum lower bound remaining in the
open queue,
\[
\underline J_Q(k)=\min_{\mu\in Q_k}LB(\mu).
\]
Their difference is the unresolved optimality gap over the
search space represented in $G_P$. If the current figure retains
the bounds of individual expanded nodes, the caption should
state this explicitly and should report the number of repeated
runs used to form the median and minimum--maximum envelopes.

The present experiment establishes the effectiveness of BnB
refinement, but it does not isolate the benefit of the warm
start itself. To support the warm-start claim directly, we
additionally compare the reported initialization with a
no-seed BnB run
($J^\star=+\infty$) under the same search order and report
[TO REPORT: time to first incumbent, number of expanded
nodes, pruning ratio, time to best plan, and final cost].
```

### 若暂时无法增加 warm-start ablation

删除最后一句 “demonstrates the benefit of warm starting”，改为：

> demonstrates that the retained plan graph supports effective BnB refinement.

---

## D. Scalability against Representative Baselines

```latex
\subsection{Scalability against Representative Baselines}

We address Q4 by comparing the proposed method with the
poset-based method in~[3] and the MILP-based method in~[7].
The specifications cover persistent inspection, collaborative
maintenance with precedence and restricted-region constraints,
and pickup-and-delivery tasks. For each specification, we test
teams of five robot types with 5, 10, and 20 robots per type.
All methods use the same workspace instances, initial robot
states, action requirements, and motion-cost oracle. The common
timeout is $20\,000$~s.

[TO REPORT: Identify whether each baseline uses the authors'
public code or a reimplementation; give software/solver versions,
preprocessing included in timing, parameter settings, trial
count, random seeds, and timeout treatment.]

Table~IV shows that the largest and most consistent advantage
of the proposed framework is first-plan latency. Across the
tested configurations, it returns a feasible plan in
$0.31$--$1.78$~s, compared with
$17.12$--$270.42$~s for the poset-based method and
$6.50$--$483.97$~s for the MILP-based method. This
corresponds to speedups of approximately
$40.8\times$--$201.5\times$ and
$16.7\times$--$271.9\times$, respectively.

For instances in which all methods complete their
optimization, they reach the same reported best cost. The
proposed method therefore achieves its latency advantage
without reducing the final solution quality on these completed
instances. Its first-plan cost is not uniformly lower than that
of every baseline, which is consistent with the objective of the
joint construction: return a usable plan early and refine it as
additional computation becomes available.

The exhaustive search time is not uniformly smallest for every
method and instance, and the largest cases exhibit different
timeout patterns. Accordingly, the scalability evidence should
be interpreted as follows: moving allocation into automaton
generation substantially improves the time to a usable solution
and the anytime solution trajectory, whereas the cost of full
optimality certification can still be high for all approaches due
to combinatorial robot assignments. This distinction aligns the
experimental conclusion with the scope of the proposed
framework and avoids conflating first-solution scalability with
uniformly faster exhaustive search.
```

---

## E. Repair under Robot Unavailability

```latex
\subsection{Repair under Robot Unavailability}

Finally, we address Q5 by introducing robot unavailability
during execution. We use the task and robot team from
Sec.~XI-C. Robot $r_{20}$ becomes unavailable at
$t=20$~s, after task execution has begun. The current task
progress, robot positions, and unavailability time are kept
identical across 25 runs. The retained plan graph is re-rooted
at the latest confirmed execution state, and the unfinished
assignments are optimized over the remaining team.

The first repaired feasible plan is returned in an average of
$45.74$~ms, and BnB refinement returns the best repaired
plan in $390.32$~ms. In the repaired assignment, robot
$r_{23}$ replaces $r_{20}$ for $a_5$, while the other robots
assigned to the collaborative action remain unchanged. This
case study demonstrates that a retained plan graph can be
reused to update an unfinished assignment without repeating
the initial LTL-to-automaton translation and plan-graph
construction.

The result should be interpreted as evidence for rapid repair in
the demonstrated configuration rather than as a general
comparison with replanning from scratch. A direct evaluation
of the reuse mechanism should additionally compare retained-
graph repair with complete reconstruction over multiple
unavailability times, robot types, and task structures, reporting
repair success rate, first-repair latency, best-repair latency,
cost degradation, and infeasibility-detection time.
```

---

## F. Numerical Experiment Summary

建议增加一个简短收束段：

```latex
\subsection{Summary of Numerical Results}

The numerical results answer the evaluation questions as
follows. First, early GBA pruning and joint NBA--plan-graph
construction address distinct portions of first-plan latency:
the former prevents more than half of the tested NBA
transitions from being propagated, whereas the latter removes
the need to wait for complete NBA generation before
allocation begins. Second, residual-obligation ordering
improves the first feasible plan by $7.2\%$--$15.4\%$ over
the original discovery order and usually returns a plan close
to the best construction-stage incumbent. Third, the retained
plan graph supports further BnB improvement, reducing the
representative incumbent by $8.24\%$ while pruning
$88.57\%$ of the visited assignment nodes. Fourth, the
first-plan latency advantage persists across the tested task and
team scales. Finally, the retained graph produces a repaired
continuation within tens of milliseconds in the demonstrated
robot-unavailability event. Together, these results support the
claimed reduction in usable-plan latency and the reuse of a
common planning structure for refinement and repair; they do
not alter the worst-case exponential complexity of the
underlying problem.
```

---

# 9. 推荐的 Physical Experiments 完整替换稿

## 9.1 标题

建议使用：

```latex
\section{Physical-Robot Experiments}
```

比 `Physical Experiments` 更具体。

---

## XII. PHYSICAL-ROBOT EXPERIMENTS

```latex
\section{Physical-Robot Experiments}

The physical experiments examine whether the task-level plans
produced by the proposed framework can be executed by a
heterogeneous robot team and whether the retained plan graph
can support repair after robot unavailability. These experiments
are intended as execution and repair demonstrations; statistical
claims about real-world robustness require repeated trials and
are reported only where such repetitions are available.
```

---

## A. Platform and Protocol

```latex
\subsection{Platform and Protocol}

The platform consists of four TurtleBot3 robots operating in
the laboratory workspace shown in Fig.~6. Robots $r_1$ and
$r_2$ are Type-1 robots, whereas $r_3$ and $r_4$ are
Type-2 robots. The workspace contains five regions of interest:
$l_1$ and $l_4$ are the inbound and outbound areas,
$l_2$ and $l_5$ are storage areas, and $l_3$ is the central
control area. The physical obstacles and their map
representation are shown in Figs.~6(a) and~6(b).

The planning software runs in Python~3.8.10 on Ubuntu~20.04
with ROS Noetic on a laptop equipped with an Intel Core
i7-11390H CPU and 16~GB RAM. Robot localization uses
[TO REPORT], and point-to-point motion is executed using
[TO REPORT: navigation stack and local planner]. Collision
avoidance and the negative region constraints are enforced by
[TO REPORT]. Planning times reported below include
[TO REPORT: exact stages] and exclude
[TO REPORT: communication and physical execution, if
excluded].

The warehouse inspection mission is
\[
\phi =
\Diamond a_1
\land
\Diamond\!\left(
a_2\land
(\Diamond a_3\land\Diamond a_4)
\right)
\land
\Diamond(a_5\land a_6).
\]
Action $a_1$ requires one Type-1 robot at $l_1$;
$a_2$ requires one Type-2 robot at $l_3$;
$a_3$ requires two Type-1 robots to collaborate at $l_2$;
$a_4$ requires one Type-1 robot at $l_5$; and
$a_5$ and $a_6$ require Type-1 and Type-2 robots,
respectively, to perform the final inspection concurrently at
$l_4$.
```

建议增加一个 action-requirement table，避免长段落重复解释 \(a_1,\ldots,a_6\)。

---

## B. Nominal LTL-MRTA Execution

```latex
\subsection{Nominal LTL-MRTA Execution}

Figure~7 shows a representative nominal execution. The first
feasible accepting plan is generated after $0.217$~s. The
best plan over the retained plan graph is first found after
$1.291$~s, and the complete search terminates after
$4.328$~s. If the final value is certified only over $G_P$,
it is referred to as the graph-optimal plan rather than the
global optimum of Problem~1.

The execution realizes the following temporal and collaborative
requirements. Robot $r_3$ first travels to $l_3$ and completes
$a_2$. Robots $r_1$ and $r_2$ then meet at $l_2$ to
complete the collaborative action $a_3$. Robot $r_2$
subsequently performs $a_1$ at $l_1$, while $r_1$ performs
$a_4$ at $l_5$. Finally, $r_1$ and $r_4$ execute $a_5$
and $a_6$ concurrently at $l_4$. The corresponding NBA
progress reaches the accepting prefix--suffix structure, showing
that the generated assignment respects the task precedence,
robot-type, cardinality, and synchronization requirements in
the physical environment.

This experiment demonstrates physical executability for the
reported mission. To quantify nominal reliability, the final
paper should additionally report
[TO REPORT: number of repeated trials, task success rate,
planning-time distribution, navigation failures, and execution
time].
```

---

## C. Execution and Repair under Robot Unavailability

```latex
\subsection{Execution and Repair under Robot Unavailability}

We next inject an unavailability event while $r_3$ is traveling
to $l_3$ to execute $a_2$, as shown in Fig.~8. The event is
detected before $a_2$ is confirmed complete. The planner
therefore re-roots the retained graph at the current task-progress
state, removes $r_3$ from the available team, and re-optimizes
the unfinished assignments.

A feasible repaired plan is obtained after $4.662$~ms. The
best retained-graph plan is found at the same point
[retain only if verified], and exhaustive graph search finishes
after $87.392$~ms. Robot $r_4$ is reassigned to $a_2$ and
travels to $l_3$. After obtaining the goods information, it
continues to $l_4$ for the final Type-2 action $a_6$, while the
remaining robots execute the Type-1 subtasks. The mission
therefore reaches the required accepting progress despite the
loss of the originally assigned Type-2 robot.

This demonstration verifies that the runtime state can be
mapped back to the retained plan graph and that a consistent
continuation assignment can be executed. It does not by itself
establish a general repair success rate. A stronger physical
evaluation should repeat the experiment for different
unavailability times and affected robots and report the repair
success rate and latency distribution, ideally together with a
full-reconstruction baseline.
```

---

## D. Physical Experiment Summary

```latex
\subsection{Summary of Physical-Robot Results}

The physical experiments complement the numerical evaluation
by demonstrating the complete information flow from an LTL
mission to heterogeneous robot assignments, navigation, and
proposition-confirmed task progress. The nominal trial
demonstrates temporal ordering and collaborative execution,
whereas the injected unavailability event demonstrates
re-rooting and reassignment of unfinished tasks. These results
validate implementation feasibility on the reported platform;
the broader statistical robustness of online repair is evaluated
only to the extent supported by the number and diversity of
repeated trials.
```

---

# 10. 强烈建议补充的实验

## 10.1 必须优先补充：BnB warm-start ablation

这是当前“方法声称—实验”之间最明显的缺口。

比较：

| Variant | Seed |
|---|---|
| Warm-started BnB | \(\Pi_{\mathrm{plan}}\) |
| First-plan seed | \(\Pi_{\mathrm{init}}\) |
| No seed | \(+\infty\) |

报告：

- first finite incumbent time；
- expanded nodes；
- pruned nodes；
- \(T_{\mathrm{best}}\)；
- \(J_{\mathrm{best}}\)；
- terminal gap。

---

## 10.2 必须优先补充：repair reuse vs rebuild

比较：

- retained graph re-root + BnB；
- rebuild GBA/NBA/plan graph from current state；
- optional assignment-only repair。

这项实验最直接证明：

> retained plan graph is valuable for repair,

而不仅仅证明“当前代码能很快运行一次”。

---

## 10.3 建议补充：多场景 robot unavailability

建议至少构造一个小型 matrix：

| Factor | Levels |
|---|---|
| failure time | early / middle / late |
| affected robot | active / idle |
| type scarcity | redundant / critical |
| number unavailable | 1 / 2 |
| continuation | feasible / infeasible |
| task structure | sequence / parallel / alternative / recurring |

---

## 10.4 建议补充：hardware repeated trials

至少报告：

- nominal trials；
- unavailability trials；
- success rate；
- mean/median repair time；
- localization/navigation failure causes；
- infeasibility-detection outcome。

参考论文中的实物评估之所以有说服力，不只是有 frame sequence，而是对多类 disturbance 做了 repeated trials 和 controlled ablation。

---

# 11. 推荐的结果分析模板

以后每个 subsection 建议使用四句式：

### 第一句：问题

> This experiment evaluates whether...

### 第二句：控制变量与比较对象

> We compare X and Y under the same...

### 第三句：定量结果

> X reduces/increases ... by ...

### 第四句：机制解释与证据边界

> This occurs because... The result supports ..., but does not imply ...

例如：

```latex
This experiment evaluates whether allocation during NBA
generation, rather than GBA pruning alone, reduces
first-plan latency. Both variants use the same pruned GBA and
the same paired robot instances; they differ only in when task
allocation begins. Joint construction reduces
$T_{\mathrm{first}}$ by $18.1\%$--$42.2\%$, with larger
absolute savings as the task formula grows. The reduction is
consistent with the removal of the serial wait between complete
NBA construction and allocation; it does not indicate a change
in the worst-case complexity of LTL translation.
```

这比：

> “Our method is faster because it is on-the-fly.”

更严密。

---

# 12. 建议删除或弱化的当前表述

## 12.1 不建议写

> The experiments prove the correctness of the method.

改为：

> The experiments validate the implementation and empirical
> behavior; soundness and completeness are established
> theoretically in Sec.~X.

---

## 12.2 不建议写

> The score-guided first plans are close to the global optimum.

改为：

> The score-guided first plans improve on the discovery-order
> solutions and remain within \(0\%\)–\(4.5\%\) of the best
> construction-stage plans; their gaps to the reported reference
> optimum vary from \(1.8\%\) to \(22.0\%\).

---

## 12.3 不建议写

> The scalability experiment shows that our method is always faster.

改为：

> The method is consistently faster in time to the first and best
> usable plans across the tested configurations, while exhaustive
> search time remains instance-dependent.

---

## 12.4 不建议写

> The online experiment demonstrates efficient replanning in general.

改为：

> The case study demonstrates millisecond-scale repair in the
> tested unavailability event; broader claims require multiple
> failure scenarios and a reconstruction baseline.

---

## 12.5 不建议在实物部分写过多小数

将：

- `0.2168939 s` 改为 `0.217 s`；
- `1.290683 s` 改为 `1.291 s`；
- `4.327640 s` 改为 `4.328 s`；
- `0.004662 s` 改为 `4.662 ms`；
- `0.087392 s` 改为 `87.392 ms`。

---

# 13. 投稿前实验核查清单

## Common protocol

- [ ] 计时从 raw LTL input 开始；
- [ ] baseline preprocessing 同样计入；
- [ ] 明确 \(T_{\mathrm{first}},T_{\mathrm{plan}},T_{\mathrm{best}},T_{\mathrm{search}}\)；
- [ ] 明确 trial counts、seeds 和 statistics；
- [ ] 报告 success/timeout counts；
- [ ] 给出 obstacle density 和 robot sampling rule；
- [ ] 给出 baseline code、solver 和 parameter source。

## Claims

- [ ] `global optimum` 有独立认证，否则改为 `graph-optimal`；
- [ ] experiments 不称为理论证明；
- [ ] scalability conclusion 聚焦 usable-plan latency；
- [ ] repair conclusion 不超出 current scenarios；
- [ ] hardware conclusion 与 trial count 匹配。

## Missing direct evidence

- [ ] warm-start vs no-warm-start；
- [ ] retained graph vs full rebuild；
- [ ] multiple failure times/types；
- [ ] hardware repeated trials。

## Presentation

- [ ] subsection title 直接表达被验证的 mechanism；
- [ ] 每节结尾明确“证明了什么”和“没有证明什么”；
- [ ] tables 包含 unit、timeout、statistic；
- [ ] figures caption 自包含；
- [ ] 统一使用 `robot unavailability`，避免与 `failure` 混用；
- [ ] \(\Pi_{\mathrm{init}}\)、\(\Pi_{\mathrm{plan}}\)、\(\Pi^\star\) 含义全文一致。

---

# 14. 最终推荐

当前实验最有说服力的核心结论应当被整理成：

1. **Full vs Delayed Allocation** 直接证明：  
   allocation 前移到 NBA generation 能够减少 first-plan critical path。

2. **Delayed Allocation vs Post-NBA Pruning** 直接证明：  
   planning-aware GBA pruning 能够避免大量无效 transition 被 materialized 和 propagated。

3. **Discovery vs Score-Guided Order** 直接证明：  
   residual-obligation score 在几乎不增加 first-plan time 的情况下改善 first-plan cost。

4. **\(\Pi_{\mathrm{plan}}\) vs BnB incumbent** 证明：  
   retained plan graph 支持 continued refinement；但 warm-start 的独立贡献还需要消融。

5. **Scalability comparison** 证明：  
   本文最强优势是大规模任务下的 time-to-usable-plan，而不是所有实例中 exhaustive search 总时间都最小。

6. **Repair + physical execution** 证明：  
   retained graph 可以在示例事件中快速生成并实际执行 continuation plan；general robustness 需要更多 repeated scenarios。

按这条证据链重写后，实验部分会与 Introduction、Contributions、System Overview 以及 Sections V–VIII 形成闭环：

\[
\text{problem cause}
\rightarrow
\text{method mechanism}
\rightarrow
\text{controlled experiment}
\rightarrow
\text{quantitative evidence}
\rightarrow
\text{properly scoped conclusion}.
\]
