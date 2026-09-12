# Preliminaries（先验知识）检查与修改建议

## 一、总体判断

对照你的 Sec. II **Preliminaries**、后续 Secs. III–VI 对符号的实际使用，以及两篇参考论文的 formal-background 写法，我认为你当前先验知识的内容选择总体正确：**LTL、NBA、AST、VWAA、GBA 以及 LTL2BA translation pipeline 都有保留必要**。原因是你的方法不是单纯“使用一个已经生成好的 NBA”，而是直接修改 GBA construction 和 GBA-to-NBA generation，因此不能像一般 LTL planning 论文那样只定义 LTL 和 NBA。

当前最需要改的不是“删很多内容”，而是**统一 formal notation、消除重复定义、把 LTL2BA 介绍写得更精确紧凑**。

---

## 二、从两篇模板中应借鉴的写法

### 1. *Temporal Logic Task Allocation in Heterogeneous Multirobot Systems*

这篇与你的问题最接近。它的 Preliminaries 有几个值得直接借鉴的原则：

- `AP`、`Σ=2^{AP}`、infinite word、`Words(φ)`、NBA、run、acceptance、prefix–suffix 依次定义；
- alphabet 始终只用一个 `Σ`；
- 明确给出
  \[
  L(B_\phi)=Words(\phi);
  \]
- 每个符号只承担一种语义。

你的 Sec. II-A 整体结构已经接近这篇，但还需要进一步收紧 notation。

### 2. *From Ambiguous Language to Verifiable Plans*

这篇的 Preliminary Background 更短，只定义后文真正需要的 formal objects。它最值得借鉴的是：

> **Preliminaries 不承担教科书功能，只为后续方法建立最小、充分、统一的数学语言。**

你的论文不能完全照它压缩，因为 automaton translation 本身就是你的研究对象。因此最适合你的写法是：

- LTL/NBA：像模板一样简洁；
- LTL2BA/VWAA/GBA：保留，但只讲与你后续 pruning 和 joint construction 直接相关的结构。

---

# 三、符号统一：必须优先修改的问题

## 1. `Σ` 与 `Σ_B` 重复

你先定义：

\[
\Sigma=2^{AP},
\]

随后 NBA 又使用 `Σ_B`，Sec. III-C 再写一次 `Σ_B=2^{AP}`。

### 推荐

全文统一：

\[
\Sigma:=2^{AP}.
\]

NBA、VWAA、GBA 都使用同一个 alphabet：

\[
B_\phi=(Q_B,q_{B,0},\Sigma,\rightarrow_B,Q_{B,F}),
\]

\[
V_\phi=(Q_v,\Sigma,\delta_v,I_v,F_v,\preceq_v),
\]

\[
G_\phi=(Q_g,Q_{g,0},\Sigma,\rightarrow_g,F_g).
\]

不再使用 `Σ_B`。

---

## 2. `σ_k` 与 `σ_{ij}` 语义混用——这是最重要的问题

你在 infinite word 中写：

\[
w=\sigma_0\sigma_1\cdots,\qquad \sigma_k\in\Sigma.
\]

这里 `σ_k` 是某个时刻的 **alphabet letter / truth valuation**。

但后面又写：

\[
(q_{B,i},\sigma_{ij},q_{B,j}),
\]

并把 `σ_{ij}` 当成：

- transition condition；
- task requirement；
- literal set；
- 甚至在 Definition 6 中做集合并。

这与前面的 `σ_k∈2^{AP}` 不是同一类数学对象。

### 最推荐的改法

保留：

\[
\sigma_k\in\Sigma
\]

只表示 input word 的 letter。

把 automaton 的 symbolic transition condition 全部改为：

\[
\gamma_{ij}.
\]

例如：

\[
q_{B,i}\xrightarrow{\gamma_{ij}}q_{B,j}.
\]

self-loop condition 改为：

\[
\gamma_i^s.
\]

subtask 改为：

\[
\omega_{ij}=(\gamma_{ij},\gamma_i^s).
\]

并明确：

> a transition guard \(\gamma_{ij}\) is enabled by a letter \(\sigma\in\Sigma\) iff \(\sigma\models\gamma_{ij}\).

这会显著提高 formal clarity，也与 Luo & Zavlanos 使用 `γ` 表示 automaton propositional label 的习惯一致。

### Definition 6 也应同步修改

当前：

\[
\sigma_{ij}=\sigma_{ik}\cup\sigma_{kj}.
\]

如果 transition condition 是 Boolean guard，更规范的写法应是：

\[
\gamma_{ij}\equiv\gamma_{ik}\land\gamma_{kj}.
\]

如果你的代码内部确实把 conjunctive guard 存成 literal set，则可以额外说明：

\[
\mathrm{Lit}(\gamma_{ij})
=
\mathrm{Lit}(\gamma_{ik})\cup
\mathrm{Lit}(\gamma_{kj}).
\]

不要同时把 transition label 定义成 alphabet symbol，又把它当 literal set 使用。

---

## 3. `Q_{B,0}` 与 `q_{B,0}` 不统一

Sec. II-A 用：

\[
Q_{B,0}\subseteq Q_B
\]

表示 initial-state set，但后面 plan graph root 和 Algorithm 2 都直接使用单个：

\[
q_{B,0}.
\]

### 推荐

如果你的 LTL2BA implementation 实际使用唯一初始 NBA state，则全文统一成：

\[
q_{B,0}\in Q_B.
\]

这与你的 single-root plan graph 完全一致。

如果实现可能产生多个 initial states，则应保留 `Q_{B,0}`，但后面算法必须相应增加 super-root 或同时初始化多个 initial states。

从你当前算法结构看，**使用唯一 `q_{B,0}` 更合适**。

---

## 4. `F_v` 术语不一致

当前 Definition 3 中写：

> `F_v` is the set of accepting states

后面又称：

> co-Büchi state \(f\in F_v\)

建议统一为：

> \(F_v\) is the co-Büchi acceptance set.

不要先用普通 Büchi “accepting states”的说法，再切换成 co-Büchi terminology。

---

## 5. `F_g` 应明确为 transition-based acceptance sets

你定义：

\[
F_g=\{F_{g,1},\dots,F_{g,m_g}\},
\qquad
F_{g,i}\subseteq\rightarrow_g.
\]

因此你实际使用的是 **transition-based generalized Büchi acceptance**。

建议第一次定义时直接说明：

> a transition-based generalized Büchi automaton (GBA)

或者至少明确：

> \(F_g\) is a collection of accepting transition sets.

这样后面 `Acc(e^g)` 的定义会更自然。

---

## 6. `⊥`、`∨`、release `V` 应在 Sec. II-A 一次性定义

后文 AST 和 residual-obligation rules 使用：

- `⊥`;
- `∨`;
- release `V`.

建议在 LTL preliminaries 中统一给出：

\[
\bot:=\neg\top,
\]

\[
\phi_1\vee\phi_2
:=\neg(\neg\phi_1\land\neg\phi_2),
\]

\[
\Diamond\phi:=\top U\phi,
\]

\[
\Box\phi:=\neg\Diamond\neg\phi,
\]

\[
\phi_1 V\phi_2
:=\neg(\neg\phi_1 U\neg\phi_2).
\]

后文就不需要重新解释这些符号。

---

# 四、冗余与专业性检查

## 1. NBA language equivalence 应补上

当前：

> It is well known that any satisfiable LTL formula can be translated into an NBA.

更正式的写法是：

\[
L(B_\phi)=Words(\phi).
\]

建议改成：

> For every LTL formula \(\phi\), there exists an NBA \(B_\phi\) whose accepted language satisfies \(L(B_\phi)=Words(\phi)\).

不必限定 “satisfiable”，因为不可满足的公式对应空语言即可。

---

## 2. `Inf(ρ)` 建议正式定义

你使用：

\[
Inf(\rho)\cap Q_{B,F}\neq\emptyset
\]

但没有单独说明 `Inf(ρ)`。

建议补一句：

> where \(\mathrm{Inf}(\rho)\) denotes the set of states that occur infinitely often in \(\rho\).

---

## 3. prefix–suffix 描述建议更准确

当前：

> the prefix reaches an accepting state once ...

建议删掉 `once`，改成：

> If \(L(B_\phi)\neq\emptyset\), there exists an accepting run in prefix--suffix form
> \[
> \rho=\rho^{pre}(\rho^{suf})^\omega,
> \]
> where the prefix reaches an accepting state and the suffix is a cycle returning to that state.

---

## 4. AST 可以缩短，但不应删除

AST 后面被用于 residual-obligation score，因此 `T_\phi` 必须保留。

但当前 AST definition 偏 textbook，可以压缩成：

> The simplified formula is represented by an AST \(T_\phi\), whose internal nodes are logical or temporal operators and whose leaves are literals or Boolean constants. The same representation is later reused to compute residual task obligations.

这样直接解释它在本文中的作用。

---

## 5. VWAA 的自然语言解释偏长，但 `δ_v` 的 formal description 反而不够精确

当前只说：

> `δ_v` is the transition function.

但后面实际操作是：

> select one transition from each \(\delta_v(q_{v,i})\).

建议写成：

> \(\delta_v\) associates each VWAA state with a finite set of symbolic transitions, each consisting of a propositional guard and a successor-state set.

这和后文 GBA candidate construction 直接对应。

---

## 6. GBA construction 建议改成数学形式

当前多句解释可以压成：

若从每个 \(q_{v,i}\in q_g\) 选择 symbolic transition \((\gamma_i,S_i)\)，则：

\[
\gamma_g=\bigwedge_i\gamma_i,
\qquad
q_g'=\bigcup_i S_i.
\]

若 `γ_g` satisfiable，则形成 candidate transition：

\[
q_g\xrightarrow{\gamma_g}q_g'.
\]

比“conjoin conditions / intersect satisfying symbols / combine successor sets”更简洁专业。

---

## 7. Sec. III-C 重复定义 NBA，应删除

Sec. II 已定义 NBA，但 Sec. III-C 又完整写了一遍 tuple 和每个 component。

建议改成：

```latex
Consider an LTL formula $\phi$ over $AP$, and let $B_\phi$
denote its NBA as defined in Sec.~II-A. To connect the
automaton structure with task-level planning, we associate
each symbolic NBA transition with a subtask.
```

随后直接进入 Definition 5。

这是当前全文最明显的一处 background redundancy。

---

# 五、推荐的 Sec. II 完整替换稿

下面版本保留你现有 Definition numbering，便于直接替换。

## A. Linear Temporal Logic

```latex
\section{Preliminaries}

This section reviews the temporal-logic and automata-theoretic
notions used throughout the paper. Since the proposed framework
intervenes directly in the LTL-to-automaton translation process,
we also summarize the intermediate automata in the LTL2BA
pipeline that are relevant to the proposed pruning and on-the-fly
planning procedures.

\subsection{Linear Temporal Logic}

Let $AP$ be a finite set of atomic propositions. An LTL formula
over $AP$ is recursively defined by
\[
\phi ::= \top \mid \pi \mid \neg\phi \mid
\phi_1\land\phi_2 \mid \bigcirc\phi \mid
\phi_1\,\mathsf{U}\,\phi_2,
\]
where $\pi\in AP$, $\top$ denotes true, $\bigcirc$ is the
next operator, and $\mathsf{U}$ is the until operator. Other
Boolean and temporal operators are defined in the standard way,
including $\bot:=\neg\top$,
$\phi_1\vee\phi_2:=\neg(\neg\phi_1\land\neg\phi_2)$,
$\Diamond\phi:=\top\,\mathsf{U}\,\phi$,
$\Box\phi:=\neg\Diamond\neg\phi$, and
$\phi_1\,\mathsf{V}\,\phi_2:=
\neg(\neg\phi_1\,\mathsf{U}\,\neg\phi_2)$.

Let $\Sigma:=2^{AP}$ be the alphabet. An infinite word over
$\Sigma$ is a sequence
\[
w=\sigma_0\sigma_1\cdots\in\Sigma^\omega,
\]
where $\sigma_k\in\Sigma$ is the set of atomic propositions
that are true at step $k$. We write $w\models\phi$ if $w$
satisfies $\phi$, and define
\[
\mathrm{Words}(\phi)
:=\{w\in\Sigma^\omega\mid w\models\phi\}.
\]

For every LTL formula $\phi$, there exists a nondeterministic
B\"uchi automaton (NBA) whose accepted language coincides with
$\mathrm{Words}(\phi)$.

\textbf{Definition 1 (Nondeterministic B\"uchi Automaton).}
An NBA associated with $\phi$ is a tuple
\[
B_\phi=(Q_B,q_{B,0},\Sigma,\rightarrow_B,Q_{B,F}),
\]
where $Q_B$ is a finite set of states, $q_{B,0}\in Q_B$ is the
initial state, $\Sigma$ is the alphabet,
$\rightarrow_B\subseteq Q_B\times\Sigma\times Q_B$ is the
transition relation, and $Q_{B,F}\subseteq Q_B$ is the set of
accepting states.

An infinite run of $B_\phi$ over
$w=\sigma_0\sigma_1\cdots$ is a sequence
$\rho=q_0q_1\cdots$ such that $q_0=q_{B,0}$ and
$(q_k,\sigma_k,q_{k+1})\in\rightarrow_B$ for all $k\geq0$.
The run is accepting if
\[
\mathrm{Inf}(\rho)\cap Q_{B,F}\neq\emptyset,
\]
where $\mathrm{Inf}(\rho)$ denotes the set of states that occur
infinitely often in $\rho$. The accepted language of $B_\phi$
is denoted by $L(B_\phi)$, and
\[
L(B_\phi)=\mathrm{Words}(\phi).
\]

If $L(B_\phi)\neq\emptyset$, there exists an accepting run in
prefix--suffix form,
\[
\rho=\rho^{\mathrm{pre}}
\left(\rho^{\mathrm{suf}}\right)^\omega,
\]
where $\rho^{\mathrm{pre}}$ reaches an accepting state and
$\rho^{\mathrm{suf}}$ is a cycle returning to that state.

For compact representation, automaton transitions are stored
symbolically in the remainder of this paper. We write
\[
q_{B,i}\xrightarrow{\gamma_{ij}}q_{B,j}
\]
when a propositional guard $\gamma_{ij}$ over $AP$ represents
all alphabet symbols $\sigma\in\Sigma$ satisfying
$\sigma\models\gamma_{ij}$. Thus, $\sigma_k$ is reserved for
an input-word letter, whereas $\gamma_{ij}$ denotes a symbolic
transition condition.
```

> 注：上面使用单个 `q_{B,0}` 是为了与你当前 Algorithm 2 的 single-root 写法一致。如果实际代码会生成多个 initial states，应保留 `Q_{B,0}` 并同步修改算法。

---

## B. LTL2BA Translation

```latex
\subsection{LTL2BA Translation}

We follow the LTL2BA translation procedure in~[13]. Given an
LTL formula $\phi$, LTL2BA first rewrites it into negative
normal form (NNF), so that negation appears only in front of
atomic propositions, and applies standard rewriting rules to
simplify the formula before automaton generation.

\textbf{Definition 2 (Abstract Syntax Tree).}
The simplified formula is represented by an abstract syntax tree
(AST), denoted by $T_\phi$. Each internal node is a logical or
temporal operator, whereas each leaf is a literal or a Boolean
constant. The same representation is later reused to compute
residual task obligations.

LTL2BA next constructs a very weak alternating automaton
(VWAA), which compactly represents simultaneous temporal
obligations.

\textbf{Definition 3 (Very Weak Alternating Automaton).}
A VWAA is a tuple
\[
V_\phi=(Q_v,\Sigma,\delta_v,I_v,F_v,\preceq_v),
\]
where $Q_v$ is a finite set of states, $\Sigma$ is the alphabet,
$\delta_v$ associates each state with a finite set of symbolic
transitions, $I_v$ is the initial condition,
$F_v\subseteq Q_v$ is the co-B\"uchi acceptance set, and
$\preceq_v$ is a partial order such that every successor state
appearing in a transition from $q_v\in Q_v$ is no higher than
$q_v$ under $\preceq_v$.

The VWAA is subsequently converted into a transition-based
generalized B\"uchi automaton (GBA), which retains multiple
acceptance requirements before degeneralization.

\textbf{Definition 4 (Generalized B\"uchi Automaton).}
A transition-based GBA is a tuple
\[
G_\phi=(Q_g,Q_{g,0},\Sigma,\rightarrow_g,F_g),
\]
where $Q_g$ is a finite set of states,
$Q_{g,0}\subseteq Q_g$ is the set of initial states,
$\Sigma$ is the alphabet, $\rightarrow_g$ is the transition
relation, and
\[
F_g=\{F_{g,1},\ldots,F_{g,m_g}\}
\]
is a finite collection of accepting transition sets. A run is
accepting if it traverses a transition in every
$F_{g,h}\in F_g$ infinitely often.

Following~[13], each GBA state is a set of VWAA states,
$q_g\in Q_g\subseteq2^{Q_v}$, representing their conjunction.
Let
\[
q_g=\{q_{v,1},\ldots,q_{v,n}\}.
\]
For each $q_{v,i}$, select one symbolic VWAA transition with
guard $\gamma_i$ and successor-state set $S_i$. The selected
transitions induce
\[
\gamma_g=\bigwedge_{i=1}^{n}\gamma_i,
\qquad
q_g'=\bigcup_{i=1}^{n}S_i.
\]
If $\gamma_g$ is satisfiable, the candidate transition
\[
q_g\xrightarrow{\gamma_g}q_g'
\]
is considered for insertion into the GBA after the standard
LTL2BA simplifications. The VWAA co-B\"uchi condition is
transferred to the generalized transition-based acceptance sets
$F_g$, which are subsequently used during GBA-to-NBA
degeneralization.

After the GBA is constructed, LTL2BA performs
degeneralization to obtain $B_\phi$. The translation pipeline
used in this work is therefore summarized as
\[
\phi\rightarrow T_\phi\rightarrow V_\phi
\rightarrow G_\phi\rightarrow B_\phi.
\]

LTL2BA applies simplification throughout the translation,
including formula rewriting and on-the-fly removal of
unreachable or subsumed automaton structure. The proposed
framework retains these standard simplifications and further
introduces robot-team and planning-related information during
GBA and NBA generation.
```

---

# 六、采用上述版本后，后文应同步修改

至少同步以下位置：

1. Sec. III-C：
   \[
   \sigma_{ij}\rightarrow\gamma_{ij},
   \qquad
   \sigma_i^s\rightarrow\gamma_i^s.
   \]

2. Definition 5：
   \[
   \omega_{ij}=(\gamma_{ij},\gamma_i^s).
   \]

3. Sec. V candidate transition：
   \[
   e_g=(q_g,\gamma_g,q_g').
   \]

4. Definition 6：
   \[
   \gamma_{ij}\equiv\gamma_{ik}\land\gamma_{kj},
   \]
   或者显式使用 literal-set representation。

5. Sec. III-C 删除重复 NBA tuple，只引用 Sec. II-A。

6. 全文删除 `Σ_B`，统一为 `Σ`。

---

# 七、推荐的修改优先级

### 必须修改

1. `Σ_B → Σ`；
2. 区分 `σ_k` 与 symbolic guard `γ_{ij}`；
3. 统一 `Q_{B,0}` / `q_{B,0}`；
4. `F_v` 改成 co-Büchi acceptance set；
5. 补充 \(L(B_\phi)=Words(\phi)\)；
6. 删除 Sec. III-C 的 NBA 重复定义。

### 强烈建议

7. 一次性定义 `⊥`、`∨`、`◇`、`□`、release `V`；
8. 更精确说明 `δ_v`；
9. 明确 GBA 是 transition-based；
10. 用 guard conjunction / successor union 压缩 VWAA-to-GBA construction。

### 不建议删除

- GBA definition；
- VWAA-to-GBA candidate construction；
- prefix–suffix structure；
- AST notation \(T_\phi\)。

因为这些都直接服务你的后续方法，而不是普通背景知识。

---

## 最终效果

修改后，整篇论文的 formal symbols 会形成清晰链条：

\[
\phi
\rightarrow
w=\sigma_0\sigma_1\cdots
\rightarrow
T_\phi
\rightarrow
V_\phi
\rightarrow
G_\phi
\rightarrow
B_\phi,
\]

其中：

- `σ` 始终表示 input valuation；
- `γ` 始终表示 symbolic transition guard；
- `q_v,q_g,q_B` 分别属于不同 translation stage；
- `F_v,F_g,Q_{B,F}` 的 acceptance semantics 清楚区分；
- Sec. III 不再重复定义 NBA；
- Sec. V 的 GBA pruning 可以直接接着 Sec. II-B 阅读。

这会比当前版本更符合 IEEE T-RO formal-method papers 的写法：**定义充分但不过度、符号单义、术语规范、preliminaries 直接服务方法。**
