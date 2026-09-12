# Introduction—Related Work 逻辑审阅报告（双角色、六轮讨论）

## 1. 审阅范围与方式

- 主审文本：`incremental_ltl_new/bare_jrnl_new_sample4.tex` 第 74–153 行，即 `INTRODUCTION` 正文与 `Related Work`。
- 一致性参照：摘要、第 154–164 行 `Contributions`、问题模型、计划图算法、理论分析及直接支撑引言声明的实验。
- 角色：
  - 博士生作者视角：关注论证链、术语边界、方法—贡献闭环和可修复性。
  - 严格匿名审稿人视角：关注新颖性、相关工作公平性、claim 的可证伪性及拒稿风险。
- 讨论共六轮：独立审阅、交叉质询、叙事重构、原始文献核验、投稿优先级、最终签署。
- 本轮未修改论文 `.tex`，也未修改任何现有 Markdown；本文件是唯一新增文件。

> 总结性判断：当前段落的主线可以辨认，但核心问题不是英语润色，而是 **claim 边界、最近邻定位和理论保证之间尚未闭合**。在动笔改写 Introduction/Related Work 前，应先决定如何处理 completeness、如何界定“general LTL”、以及 repair 是否仍作为核心贡献。

## 2. 双方共同签署的最终结论

本文目前最可防守的中心贡献不是笼统的 “on-the-fly / anytime / repair”，而是：

> 在明确的 region/action 与机器人可达性模型下，将 team-aware GBA pruning、任务分配、plan-graph construction 和 robot-state-guided ordering 嵌入 GBA→NBA 构造；一旦联合构造产生可行的 accepting plan node，即可事件触发地输出一个 incumbent，而不要求先完成剩余 NBA 构造，随后再利用保留的 plan graph 继续优化。

这句话需要同时遵守三个边界：

1. 它表示算法具备“无需先等待 NBA 完成”的能力，不保证每个实例都严格早于完整 NBA 得到首解。
2. 它不自动推出首解必然 “rapid” 或 “high-quality”；这两项只能由统一计时和质量指标的实验支持。
3. 在 GreedyAssign 和 plan-node merge 的正确性问题解决前，不能据此无条件宣称整个框架 complete。

双方对以下八项形成共识：

1. 主线应收窄为 planning-aware automaton generation 改变可行 incumbent 的发现/输出时点。
2. 接受分支可能最后才被发现，因此不能保证每个实例都 “before the complete NBA”。
3. 当前 GreedyAssign 与 plan-node merge 均对 completeness 构成可构造反例风险。
4. `research0337` 是直接竞争者；Liu et al. 2024 的 failure repair 必须承认；Yalcinkaya et al. 2024 不应被归为 LTL-MRTA formula decomposition。
5. Related Work 主体应按 planning information 进入 temporal-representation pipeline 的时点组织；local/global 只用于划定问题范围。
6. 没有 repair baseline 时，repair 最多是 secondary demonstrated capability，不能作为文献空白或相对优势。
7. “general LTL”最多表示标准、非层次/非预分解的 LTL 输入；不能暗示 action、协作、运动和可达性模型同样一般。
8. 对 poset preprocessing 的讨论必须区分 automaton construction/pruning、first poset、best/all posets 和 first plan，不能只用状态数代替端到端时延证据。

唯一保留分歧是：博士生视角认为可以在“修复算法并重证 completeness”与“撤除 completeness、诚实定位为 heuristic”之间选择；审稿人认为若目标是严格的 IEEE 机器人期刊，仅撤除理论主张但保留 correctness 缺口，通常仍不足以进入可接收区间。

## 3. 当前论证链的重构与断点

当前文本试图建立如下链条：

1. 多机器人任务具有时间依赖和多机器人协作要求（第 75 行）。
2. LTL-MRTA 随机器人数量与公式复杂度增加而快速变难（第 81 行）。
3. 实际应用需要尽早获得较高质量可行解，并在额外时间内继续改进（第 81、93 行）。
4. 现有方法通常将完整自动机构造与 robot assignment 分离，因而推迟首解（第 83 行）。
5. 结构化公式和学习式方法虽缓解负担，但分别依赖特定结构或训练过程（第 85–86 行）。
6. 本文将规划信息前移到 GBA/NBA 构造过程，得到首解后继续 BnB 优化，并复用图处理机器人失效（第 95 行）。
7. Related Work 最后将 gap 总结为“快速首解 + 后续优化 + 高效修复”难以兼得（第 114 行）。

主要断点有三处：

- **断点 A：瓶颈未被精确定义。** “使用自动机”不等于“必须等待完整 NBA”。Sampling、planning tree 和 on-the-fly poset product 都具有某种增量性。第 83 行需要比较的是各方法的 allocation 起点和 `T_first` 计时边界，而不是笼统说是否使用自动机。
- **断点 B：repair 没有 motivation—prior work—gap 闭环。** 第 75–93 行几乎只论证首解与持续优化；repair 在第 95 行突然进入方法概览，并在第 114 行被纳入核心 gap。第 106 行反而已经承认 bottom-up 方法存在 online reconfiguration/replanning。
- **断点 C：理论边界没有在引言暴露。** 第 93 行称 “general LTL”，摘要称 sound and complete，但问题模型和算法含有严格 action/可达性假设、单次 greedy matching 和 execution-state merge。读者会自然把“语言层一般性”误解为“整个 MRTA 模型与求解器均一般且完备”。

## 4. 投稿阻断级问题（P0）

### P0-1：当前 completeness 证明受到两个独立反例威胁

#### 反例一：GreedyAssign 可能把存在可行匹配的 subtask 判为失败

相关位置：

- 每台机器人可以有不同的可达区域，且距离可为 `+∞`：第 261–262 行。
- 同一 subtask 中不同 action 的机器人集合必须互斥：第 307–308 行。
- GreedyAssign 按 action index 顺序，为每个 action 选择预计最早到达的机器人：第 712–729 行。
- 一旦 greedy 失败，该 automaton extension 被直接丢弃：第 663–665 行。
- completeness 证明却使用了“可行 run 的每个 subtask 存在 valid assignment，因此 construction 会生成 successor”：第 1239 行。

可构造的最小反例：同型机器人 `r1` 可达 `L1,L2`，`r2` 只可达 `L1`；同一 transition 中 `a1@L1` 和 `a2@L2` 各需一台机器人；`r1` 到 `L1` 更快。顺序贪心先把 `r1` 给 `a1`，随后 `a2` 无人可达而失败，但 `r2→a1, r1→a2` 明明是可行匹配。

因此，“某 subtask 存在 assignment”并不能推出当前 GreedyAssign 一定成功。这不是引言措辞问题，而是 Lemma `initial-completeness` 的关键推理缺口。

可选处理路径：

- 将本步可行性判断改成完备的 bipartite/b-matching 或回溯匹配；或
- 增加足够强、与现有模型一致的假设并严格证明贪心完备；或
- 撤除原问题层面的 completeness，只保留 soundness/经验可行性，并把构图明确标为 heuristic。

#### 反例二：较小当前 makespan 不支配不同机器人位置带来的未来可行性

相关位置：

- 同一 NBA state 可以由不同任务分配历史到达，并产生不同 `X,Θ`：第 526–539 行。
- compatible node 的判定只使用 NBA state、progress 和 subtask：第 661、692–693 行。
- 已有节点时仅在新 `J` 更小时替换代表 predecessor 和存储的 `X,Θ`：第 667–675 行。
- 已展开 NBA state 的后继结构被复用，而不是基于每个新 execution state 完整重新生成：第 747–792 行。

较小的当前 `J` 不意味着更好的未来位置、可达性或后续完成时间。一个当前稍慢、但机器人位于关键区域或拥有唯一后续可达路径的状态，可能是完成后续任务的唯一历史；只按标量 `J` 选代表会覆盖其 execution semantics。保留结构 parent edge 本身不足以修复，因为 BnB 只能枚举已经存在于 plan graph 的结构，无法恢复从未生成的 accepting branch。

可选处理路径：

- 定义并证明真正安全的 dominance relation；或
- 对每个 automaton/progress 状态保留关于位置、时间和可达性的 Pareto 非支配 execution labels；或
- 取消该 merge/reuse；并增加定向可达、异速机器人和非交换同型机器人反例测试。

#### 对引言的直接影响

在上述问题解决前，下列说法均属高风险：

- 摘要第 63 行和理论第 1235–1248 行的 unconditional “sound and complete”；
- 第 93 行的 “general LTL specifications”；
- 第 95 行把 greedy construction 描述成普遍可返回首解的完整求解框架。

另外还需单独核查：无限 suffix 是否可由一次 suffix 的分配与末端 execution state 无限重复，以及 GBA decomposition pruning 保持的是 language、feasibility 还是 cost optimality。当前第 310–317 行只用一次 `prefix + suffix` 定义 makespan，容易引发这一追问。

### P0-2：核心 gap 对最近邻工作覆盖不完整

第 83 行称 planning-tree、poset 以及“most existing LTL-MRTA methods”在 automaton 完成后才开始 robot assignment；第 95 行又用 “Unlike existing methods” 建立对立。该论证至少要正面处理以下例外：

- `research0337` 明确提出避免把 complete task formula 直接转换成 Büchi automaton，并 on-the-fly 计算 R-poset products、同时进行 subtask assignment。它与本文并不相同，但属于“避免完整表示预处理、尽早生成方案”的直接竞争范式，不能只作为结构化公式旁支带过。
- planning-decision-tree 方法也增量表示 task progression 与 allocation。若其 temporal representation 仍需预构造，应明确“预构造的到底是什么、何时完成、耗时是否计入 `T_first`”，而不是把“增量规划”与“完整自动机后规划”同时陈述却不解释。

本文更可防守的差异可能是以下特定组合，而不是泛化的 “first on-the-fly method”：

1. team-conditioned feasibility pruning 发生在 GBA 构造阶段；
2. robot assignment 发生在 GBA→NBA degeneralization 期间；
3. plan graph 与 NBA 同步生成；
4. robot-state/planning score 改变 NBA successor expansion order；
5. 完整 plan graph 后再以 BnB 改进 incumbent。

需要一张 component-level pipeline/capability matrix 才能判断其中哪些是新机制、哪些是已知组件的组合。未完成这一步前，第 160 行 “the first LTL-MRTA framework ...” 风险很高。

### P0-3：repair 不能作为当前文献空白

Liu et al. 2024 已明确提出在 agent failures 后重新分配 unfinished subtasks，并给出在线适配与硬件示例。因此第 114 行把 “efficient plan repair” 放进现有方法共同缺失的三联 gap，会被熟悉该工作的审稿人直接质疑。

本文仍可强调不同机制：从最后确认的 execution state 重根，并复用 retained plan graph 搜索 surviving team 的分配。但在没有同条件 baseline 与 `reuse vs. rebuild` 消融时，只能说“本文展示了这种 graph-reuse repair capability”，不能说现有方法不支持 repair，也不能说本文更快或更优。

建议定位：

- Introduction 方法概览中保留一句；
- Contributions 中若保留，应标为统一数据结构派生的次级能力；
- 从第 114 行 central gap 中移除；
- 实验结论使用 “demonstrated”，而不是 “outperforms / efficient relative to existing work”。

### P0-4：引用与事实定位错误会直接伤害 novelty 可信度

- 第 85 行把 `yalcinkaya2024compositional` 写成把 global LTL 分解为较小 subformulas conjunction 的工作。原文实际是 goal-conditioned reinforcement learning 中的 compositional deterministic finite automata embeddings，不是 LTL-MRTA formula decomposition。应删除该处引用、换成真正支持该论断的来源，或将其准确归入学习式 temporal-goal representation。
- `li2025task` 与 `2025Task` 是同一篇 TASE 论文的重复 bib key，却分别出现在第 83、112 行。需合并，避免看似重复计数 prior work。
- 第 112 行 “As illustrated in the paper” 指代不清，必须给出具体 reference/table/case。

## 5. 严重但可通过范围和证据修复的问题（P1）

### P1-1：“before the complete NBA”被写成必然结果

第 95 行写的是 first feasible plan “becomes available ... before the complete NBA has been constructed”。最坏情况下接受分支可能最后才生成，首次 accepting plan node 与 NBA completion 同时发生。因此普遍成立的只能是：

> once a feasible accepting plan node is discovered, a plan can be returned without requiring prior completion of the remaining NBA construction.

也就是说，算法提供 event-triggered capability，而非所有实例的 strict-early guarantee。实验可报告：多少实例严格提前、提前多少秒/比例、哪些公式结构未提前。

### P1-2：“general LTL”混淆了公式语法与整个 MRTA 模型的一般性

第 93 行的 “under general LTL specifications” 容易被读成整体问题模型一般。实际上：

- action 被限定为 `(one robot type, fixed cardinality, one region)`：第 267–276 行；
- 每台机器人有离散区域图、恒定速度和预计算最短距离：第 261–262 行；
- 同一 action 目前不表达跨类型联合要求、持续时间、一般资源冲突等；
- 目标只计 `prefix + one suffix traversal`：第 310–317 行。

如果作者想强调相对 hierarchical/conjunctive 输入的差异，更安全的边界是 “standard, non-hierarchical/non-predecomposed LTL specifications under the stated action and motion model”。同时应列出支持的算子、否定 action、recurrence、simultaneous actions 与 suffix 重复条件。

### P1-3：“rapid / high-quality”没有操作化，并与正文数据存在修辞张力

当前反复使用 rapid、early、high-quality、effective，却未定义：

- rapid 是绝对实时阈值，还是相对 complete-first baseline 的改善；
- high-quality 是相对 `Π_plan` 还是真正全局最优；
- anytime 是否意味着任意时刻都可返回 incumbent，且 incumbent 单调改进。

正文第 1362–1365 行显示复杂消融中 `m=15` 的 `T_first=723.6905 s`，虽然比 Case I 的 `1037.2168 s` 快约三分之一，但不宜无条件称为 rapid。更准确的主张是“relative reduction in end-to-end first-plan latency for the tested instances”。

第 1500–1507 行的四个例子中，score-guided first plan 相对所报 global optimum 的 gap 约为 22.0%、9.3%、1.8% 和 20.4%。这可以支持“优于 discovery order”的经验趋势，但不足以在没有阈值和统计分布时笼统称所有首解 close/high-quality。

最低证据要求：预先定义 relative optimality gap、报告多实例统计/区间，并给 incumbent cost–time curve，而不是只列 first/best/final 三个点。

### P1-4：对 planning-tree 的批评会反弹到本文

第 112 行批评 planning-tree 因 greedy decisions 易陷入局部最优；本文首解同样使用 greedy assignment。真正的区别应是：本文随后保留 plan graph 并用 BnB 改进，而不是本文避免了 greedy 局限。

公平比较应使用同一时间预算下的 quality–time curve；不能拿竞争方法的 greedy 首解与本文 BnB 后结果比较。若无法加入 PDT/TB-PDT+ baseline，至少要明确共同可表达子集、不可比原因和 stage mismatch。

### P1-5：Related Work 的分类轴与创新轴不匹配

第 106 行的 bottom-up/local 与 top-down/global 可以保留为一至两句问题范围说明，但不宜继续承担主要 taxonomy。第 108–112 行目前混合 product search、sampling、STAP、decomposition、MILP、planning tree、poset、hierarchical logic 与 RL，类别相互重叠，无法自然推出第 114 行。

更合适的主轴是：**task-allocation/planning information 在 temporal-representation pipeline 的哪个阶段进入，以及在首解前必须完成什么表示。**

建议分类：

1. **完整 automaton/product 后规划**：回答完整表示是什么、allocation 何时开始、translation 是否计入 `T_first`。
2. **结构提取/decomposition/poset**：回答输入结构限制、first usable structure 的时点，以及经典 poset 与 on-the-fly poset product 的区别。
3. **增量 progression/planning-tree/lazy 方法**：回答增量生成的是 task structure、product 还是 NBA，以及 planning state 是否反向影响 automaton generation。
4. **MILP/BnB 等优化层**：回答 first incumbent、继续改进、终止/最优性范围，避免只比较 total solve time。
5. **execution adaptation**：回答 failure 后复用什么、重算什么、是否改变 task sequence，以及 repair 的正确性/最优性边界。

学习式方法与本文正交，最多用短段落比较 deployment-time speed、offline training、guarantee 和 team-size generalization，不能用单智能体 RL 论文直接支撑异构 MRTA 训练困难。

### P1-6：相关工作的 blanket claims 需要逐条限定

- 第 108 行：sampling methods 是否都要求在公式中显式绑定机器人，以及枚举 workaround 是否必然造成指数长度，需要用所引论文的 AP 定义和组合数推导支撑。
- 第 110 行：STAP “不处理 tightly coupled collaborative tasks” 需要形式化定义，并与本文 cardinality-action model 逐项比较；否则容易形成不公平否定。
- 第 110 行：MILP 在“大规模且只求首解时也慢”应限定到具体 formulation/solver/instance，而不是作为普遍性质。
- 第 86 行：学习法在复杂异构团队上“更难训练”目前是推测，应补直接证据或改成待验证的 trade-off。

## 6. 次要但影响完成度的问题（P2）

- 第 81 行末与第 93 行重复同一设计问题。
- 第 83、85–86 行对 planning tree、poset、结构化公式的评价在第 112 行再次出现，造成 Introduction 与 Related Work 重复。
- 第 95 行已详细列 pipeline，第 156–160 行 Contributions 又重复一次；应让前者解释“如何回应 gap”，后者只列可验证的新组件/保证/证据。
- robot planning、task planning、task allocation、mission planning 混用。正文实际是区域级 task allocation 加 travel-time prediction，并非一般 joint task-and-motion planning。
- first feasible solution、initial feasible solution、first executable plan、high-quality first solution 应统一，并区分 `Π_init`、`Π_plan`、BnB incumbent/global optimum。
- global LTL、general LTL、standard LTL、structured LTL、sc-LTL 应明确包含关系。
- 第 75 行 “Formal languages ... provides” 主谓不一致；第 83 行 “exiting” 应为 “existing”。
- 注释中仍保留大量中文修订提示。它们不影响编译，但投稿版本需要清理。

## 7. 第 83–114 行 claim—evidence 审计表

| 位置与 claim | 判定 | 最小可接受证据/动作 | 主要风险 |
|---|---|---|---|
| 83：planning-tree、poset 都需完整 automaton 后才规划 | 限定 | 逐论文 pipeline，区分 complete NBA、task automaton、incremental task tree | 把不同中间表示一概称为完整自动机 |
| 83：“most existing methods”分离 translation/allocation | 补证据或删 `most` | 代表性 capability matrix，标 allocation 起点 | 少数引用支撑数量性概括 |
| 85：Yalcinkaya 将 global LTL 分解成 conjunction | 删除/换源/重分类 | 使用真正的 LTL-MRTA decomposition 来源 | 已核验为 goal-conditioned RL/cDFA embedding |
| 86：学习法部署时避免 automaton，复杂团队更难训练 | 限定 | 分开证明 deployment pipeline 与 multi-robot training claim | 从单智能体工作外推异构 MRTA |
| 93：general LTL + early high-quality plan | 限定 | 公式/模型范围表；预定义首解质量指标 | 语言一般性偷换为模型一般性 |
| 95：“Unlike existing methods” | 限定为 complete-first 类 | 与 `research0337`、PDT、STAP、Liu 的组件表 | 忽视已有 on-the-fly 表示与 assignment |
| 95：必然在完整 NBA 前得到首解 | 改为 can/may | 报告 event、NBA completion 和提前比例 | 接受分支可能最后出现 |
| 108：sampling 通常预绑定机器人，枚举导致指数公式 | 补证据/限定 | 原论文 AP 模型与组合数分析 | 对全部 sampling 方法过度概括 |
| 110：STAP 不处理 tightly coupled collaboration | 定义后再比较 | 两种 collaboration semantics 形式化对照 | 术语未定义、本文模型也受限 |
| 112：PDT greedy 易局部最优 | 对称表述 | 承认本文首解也 greedy；比较同预算 refinement | 双重标准 |
| 112：数百状态的 poset 首结构可能很慢 | 仅精确引用实例 | 分开报 pruning/first/best poset/first plan | 混淆阶段并把状态数当因果 |
| 112：`research0337` 仅为结构化方法 | 保留输入限制，但升为直接竞争者 | 比较 sc-LTL conjunction、online product 与 GBA→NBA 耦合 | 用“结构化”标签淡化其 on-the-fly 能力 |
| 114：快速首解 + 优化 + repair 是现有共同空白 | 删除或重证 | competitor matrix、anytime 曲线、repair baseline | Liu 2024 已有 failure adaptation |

## 8. 建议的 Introduction 六段逻辑骨架（不是逐句改写）

1. **问题与范围。** 从 global LTL-MRTA 的实际任务进入，同时明确本文处理标准非层次 LTL，但 action/capability/region 和 motion model 受既定假设约束。
2. **评价目标。** 明确区分端到端首解时间 `T_first`、首解质量和后续优化；说明大团队/复杂公式为什么让三者产生权衡。
3. **精确瓶颈。** 聚焦 complete-automaton-first pipeline 会推迟 allocation 起点，不再声称所有使用自动机的方法都如此。
4. **最近邻与剩余问题。** 正面承认 PDT、经典 poset 和 on-the-fly poset product 已提供早解/增量能力，再以输入结构、preprocessing object、planning information 注入时点做差异化。
5. **因果对应的方法概览。** team-conditioned GBA pruning 减少传播结构；joint NBA/plan graph construction 让 feasible accepting node 一经出现即可输出；score 只负责探索顺序；BnB 负责后续 improvement。
6. **边界化总结。** 只总结可验证贡献；不承诺所有实例严格提前，不无条件写 high-quality/general/complete；repair 标为 retained-plan-graph 的扩展能力。

这样安排后，每段只完成一个功能，避免第 81/93 行问题陈述重复、第 83/112 行 prior-work 重复，以及第 95/156–160 行方法与贡献重复。

## 9. 六轮讨论纪要

### 第 1 轮：独立审阅

- 博士生重构了“应用—规模难点—首解需求—complete-first 瓶颈—联合构造—继续优化/repair”的论证树，并首先指出 completeness 的 GreedyAssign 和 merge 反例。
- 审稿人给出 Major Revision 倾向，重点攻击最近邻遗漏、`general/first/high-quality/complete` 的过宽边界和三联 gap。
- 初步共识：问题是实质逻辑与技术边界，不是简单语言润色。

### 第 2 轮：作者最强辩护与审稿交叉质询

- 作者侧认为仍可区分本文与 Liu repair、`research0337`：本文复用 plan graph，并在 GBA→NBA degeneralization 时注入 assignment/score。
- 审稿侧接受这种机制差异可能成立，但要求 component-level 证据；同时确认两个 completeness 反例不能靠文字绕过。
- 共识：novelty 应从“首次 on-the-fly”收窄为具体组件组合；repair 不再作为普遍空白。

### 第 3 轮：重建叙事

- 博士生提出六段 Introduction 骨架，以及以“allocation 前必须完成何种表示”为 Related Work 主轴。
- 审稿人进一步压缩为唯一主线：“planning-aware automaton generation advances incumbent availability”；optimization 是延伸，repair 是案例。
- 共识：local/global 只保留范围说明；主体按 planning information 进入 pipeline 的阶段分类。

### 第 4 轮：原始文献核验与事实纠错

- 核验确认：Liu 2024 包含 failure 后 unfinished-task reassignment；`research0337` on-the-fly 计算 R-poset products 并 assignment；Yalcinkaya 2024 是 cDFA-conditioned RL。
- 同时纠正了审稿人首轮的数字误判：Liu 表 IV 的 216-state first/best poset 是 8.4/37.9 s，970-state 是 136.4/552.5 s；另一个 707-state 案例是 pruning 30.43 s 后 0.14 s 得到 first poset。
- 共识：第 112 行不是完全无数据支撑，但必须精确绑定实例和阶段，不能写成“数百状态通常需要数十/数百秒”的普遍因果。

### 第 5 轮：投稿优先级

- 博士生给出 P0 correctness/文献事实/novelty/repair，P1 端到端计时与 early-event/范围，P2 结构与术语。
- 审稿人区分哪些只需改 Introduction/Related Work，哪些必须改算法/定理/实验；裁定“仅重写引言仍不足以解决 correctness”。
- 分歧：撤除 completeness 是否能形成最低可投稿版本；双方均认为不能继续保留现有 unconditional theorem。

### 第 6 轮：最终签署

- 双方逐项签署八项共识。
- 博士生最终结论：投稿前必须技术修复或撤除 completeness。
- 审稿人最终结论：在 correctness 修复、直接先验工作审计和公平实验前，事件触发机制只能作为叙事核心，尚不能预先认定为完整可发表贡献。

## 10. 投稿前行动清单

### P0：先于任何引言润色

1. **决定 completeness 路径。**
   - 完成判据：GreedyAssign 对本步 matching 完备；execution-state merge 有严格 dominance 或保留全部非支配状态；证明覆盖无限 suffix 和 pruning 保持性质。
   - 若做不到：撤掉 unconditional completeness，并同步修改摘要、Contributions、理论与结论，而不是只改 Introduction。

2. **完成最近邻 component audit。**
   - 至少覆盖：LTL2BA/on-the-fly automata、STAP、PDT/TB-PDT+、Liu 2024、`research0337`、主要 MILP/sampling 方法。
   - 表格维度：输入语言、robot identity 是否预绑定、collaboration semantics、完整 automaton 是否预构造、allocation 起点、first-plan event、后续优化、failure adaptation、理论范围。

3. **锁定唯一中心 claim。**
   - 若没有 component audit，删除 “first/most/unlike existing methods” 等宽泛表述，只陈述本文具体组合。

4. **把 repair 从 central gap 降级。**
   - 除非增加 Liu 2024 同条件 baseline 和 reuse-vs-rebuild 消融。

5. **修正文献事实。**
   - 删除或重分类 Yalcinkaya；合并重复 bib key；精确引用 Liu 时延口径；提升 `research0337` 为直接对比。

### P1：支撑主要性能主张

1. **统一端到端 `T_first`。** 从原始 LTL 输入开始，分别记录 parsing/translation、GBA pruning、first accepting automaton event、first feasible plan、NBA completion、plan-graph completion、best incumbent。
2. **增加 early-event 消融。** 比较 discovery order、score order、complete-first；报告严格提前的实例比例、提前量、首解质量 gap 和内存。
3. **给 anytime quality–time curve。** 所有方法用同硬件、线程、初始化和停止规则；在共同可表达任务上比较。
4. **定义 high-quality。** 预先给 relative gap 阈值或统计指标，不使用事后形容词。
5. **列公式与模型范围。** 明确支持算子、recurrence、negative labels、simultaneous actions、可达性和 suffix 重复假设。

### P2：结构和表达

1. 按第 8 节重排段落，消除 Introduction—Related Work—Contributions 三处重复。
2. 统一 task allocation/planning 与 `Π_init/Π_plan/optimum` 术语。
3. 清理语法、重复 bib key、模糊指代及投稿前注释。

## 11. 两种可行路线

### 路线 A：最低风险的诚实收缩版

- 修正文献事实与 taxonomy；
- 删除或严格限定 completeness、general-LTL、repair-gap、first-of-kind 和 unconditional rapid/high-quality；
- 以同一 pipeline 的 complete-first 消融只证明“结构上允许在 NBA 完成前事件触发返回”；
- repair 仅作为案例能力。

优点是修改范围相对可控；缺点是理论贡献和高水平期刊说服力会明显下降，而且 correctness 问题仍可能使审稿人拒稿。

### 路线 B：面向严格期刊的完整修复版

- 技术上修复 GreedyAssign、状态合并和 suffix/pruning 保证；
- 重做 soundness/completeness 证明与复杂度；
- 对 `research0337`、PDT/STAP、Liu 2024 做统一 pipeline 与端到端实验；
- 加入 anytime 曲线、多个公式族、随机实例统计和 repair baselines。

优点是能够保留更强的理论与性能主张；代价是已超出单纯 Introduction/Related Work 修改，涉及算法、理论和实验的系统性修订。

## 12. 需作者先作出的五个决定

在开始逐句改写前，建议先明确：

1. completeness 是要修复并保留，还是撤除并将首解构图定位为 heuristic？
2. “general LTL”是否只想表达 standard/non-hierarchical input？
3. 唯一 novelty 是 allocation timing、score-guided NBA generation，还是四组件组合？
4. repair 是核心贡献还是次级能力？若是核心，是否愿意补 baseline？
5. rapid/high-quality 分别采用什么可检验指标和阈值？

这些决定会改变 Introduction 的论证结构；在它们未确定前，直接逐句润色只会让尚未闭合的 claim 看起来更流畅，无法降低审稿风险。

## 13. 本轮事实核验来源

- [Liu et al., *Time Minimization and Online Synchronization for Multi-agent Systems under Collaborative Temporal Tasks*](https://arxiv.org/abs/2208.07756)：确认 anytime poset/BnB、agent-failure adaptation，以及表 IV 的分阶段时延。
- [Liu et al., *Fast and Adaptive Multi-agent Planning under Collaborative Temporal Logic Tasks via Poset Products*](https://arxiv.org/abs/2308.11373)：确认避免 complete task-formula-to-Büchi translation、on-the-fly R-poset product 和同步 assignment。
- [Yalcinkaya et al., *Compositional Automata Embeddings for Goal-Conditioned Reinforcement Learning*](https://proceedings.neurips.cc/paper_files/paper/2024/hash/858fc542b70d3b39067f7d3b1cd77635-Abstract-Conference.html)：确认其主题是 goal-conditioned RL 与 cDFA embeddings，而非 LTL-MRTA decomposition。

上述核验只覆盖讨论中出现的三项关键事实争议，不等同于完整 systematic literature review。正式改稿前仍需逐篇核查所有 blanket claims 和 “first/most” 表述。
