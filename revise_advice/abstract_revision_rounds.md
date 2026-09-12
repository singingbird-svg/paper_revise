# Abstract revision log

Reviewer subagent: Plato
Student subagent: Jason

Source requirements: `revise/paper/readme.md`
Paper reference: `revise/paper/bare_jrnl_new_sample4-35.pdf`
Edited source: `distributed_ltl/bare_jrnl_new_sample4.tex`

## Round 1

Reviewer focus:
- Make the task background more concrete than "finite-region missions".
- Define resilience as avoiding permanent blocking and restoring temporal/collaborative executability after disconnection and robot removal.
- Clarify why prerequisite information becomes unavailable and what happens afterward.
- De-emphasize LTL/NBA/pruning/CBTA as the innovation.
- Explain dynamic robot removal and strengthen the experimental sentence.

Student draft:

> This paper studies resilient distributed task allocation for heterogeneous multi-robot systems executing finite-region missions specified by global syntactically co-safe linear temporal logic (sc-LTL). Such missions arise in large facilities where robots must coordinate inspection, transport, and maintenance tasks subject to temporal ordering, safety constraints, and collaborative requirements on robot types and team sizes. In range-limited networks, robot motion and failures can intermittently disconnect communication links. As a result, robots may be unable to verify that prerequisite tasks in other regions or teams have been completed, preventing safe activation of subsequent tasks. Dynamic robot removal can further invalidate existing collaborative teams, create responsibility gaps, and leave pending tasks without feasible assignees. These effects may cause temporal dependencies and collaborative subtasks to remain permanently blocked. To address this problem, we propose a resilient distributed execution framework that derives robot-level executable plans from a global sc-LTL mission specification and restores execution feasibility during runtime. The proposed method actively recovers missing prerequisite-state information, reconstructs feasible collaborative teams under communication constraints, and synchronizes failure information to trigger task reallocation when robots are removed or assignments become infeasible. Evaluation on 25 simulated mission instances and physical multi-robot experiments shows that the framework enables reliable mission completion under communication disruptions and robot loss, recovering feasible execution while preserving temporal and collaborative requirements.

## Round 2

Reviewer focus:
- Compress the problem setup and reduce repeated uses of feasible/infeasible/blocked.
- Convert the method list into a deeper contribution: recovering specification-compliant distributed execution when global dependency information and team formation become unavailable.
- Make the experiment sentence point to comparisons or ablations without inventing numbers.

Student draft:

> This paper studies resilient distributed task allocation for heterogeneous multi-robot systems executing finite-region missions specified by global syntactically co-safe linear temporal logic (sc-LTL). The target missions include inspection, transport, and maintenance operations in large facilities, where robots must satisfy temporal ordering, safety constraints, and collaborative requirements on robot types and team sizes. Under intermittent connectivity and robot loss, prerequisite-task status and team commitments may no longer propagate across regions: a robot may be unable to confirm whether a preceding task has been completed, while a removed robot may leave a collaborative subtask without a valid participant. These disruptions can prevent safe progression of temporally dependent and collaborative tasks. We propose a resilient distributed execution framework for runtime mission execution under such conditions. From a global sc-LTL specification, the framework derives robot-level executable plans, while the runtime layer restores execution by recovering hidden task-dependency information and repairing collaborative commitments despite limited communication. It also prevents isolated local failures from silently delaying downstream tasks by sharing failure-relevant state and supporting distributed reallocation. In this sense, resilience is achieved by returning the distributed execution to a state that satisfies the temporal and collaborative requirements of the original specification. Simulations on 25 mission instances, ablation studies, baseline comparisons, and physical experiments demonstrate reliable task completion under communication disruptions and robot removal.

## Round 3

Reviewer focus:
- Replace unnatural terms such as "team commitments", "hidden task-dependency information", and "repairing collaborative commitments".
- Remove the definition-like sentence "In this sense...".
- Replace informal "silently delaying" and avoid overly broad "baseline comparisons".

Student draft:

> This paper studies resilient distributed task allocation for heterogeneous multi-robot systems executing finite-region missions specified by global syntactically co-safe linear temporal logic (sc-LTL). The target missions include inspection, transport, and maintenance operations in large facilities, where robots must satisfy temporal ordering, safety constraints, and collaborative requirements on robot types and team sizes. In range-limited networks, intermittent connectivity and robot loss can interrupt the propagation of prerequisite-task status and collaborative-team status across regions. Consequently, robots may be unable to confirm whether preceding tasks have been completed, while removed robots may invalidate team membership for collaborative subtasks, causing downstream temporal and collaborative tasks to stop progressing. We propose a distributed execution framework that derives robot-level executable plans from a global sc-LTL specification and strengthens runtime execution under intermittent connectivity and robot removal. The framework restores progress by recovering unavailable prerequisite-status information, recovering valid team formations for collaborative subtasks under communication constraints, and preventing local failure information from remaining unshared and causing downstream blocking, thereby restoring specification-compliant execution. Simulations on 25 mission instances, comparisons with non-resilient and local-only recovery variants, ablation studies, and physical multi-robot experiments demonstrate reliable task completion under communication disruptions and robot removal while preserving temporal and collaborative requirements.

## Round 4

Reviewer focus:
- Remove repeated "recovering".
- Replace vague "strengthens runtime execution" with resilient/runtime progress.
- Use "comparative and ablation evaluations" to avoid overclaiming.
- Express the deeper contribution as restoring visibility and executability of global task dependencies and collaborative relations.

Student draft:

> This paper studies resilient distributed task allocation for heterogeneous multi-robot systems executing finite-region missions specified by global syntactically co-safe linear temporal logic (sc-LTL). The target missions include inspection, transport, and maintenance operations in large facilities, where robots must satisfy temporal ordering, safety constraints, and collaborative requirements on robot types and team sizes. In range-limited networks, intermittent connectivity and robot loss can interrupt the propagation of prerequisite-task status and collaborative-team status across regions. Consequently, robots may be unable to confirm whether preceding tasks have been completed, while removed robots may invalidate team membership for collaborative subtasks, causing downstream temporal and collaborative tasks to stop progressing. We propose a distributed execution framework that derives robot-level executable plans from a global sc-LTL specification and supports resilient runtime execution under intermittent connectivity and robot removal. The framework maintains runtime executability by recovering unavailable prerequisite-status information, re-establishing collaborative-team feasibility under communication constraints, and sharing failure-relevant state for distributed reallocation. These capabilities restore the visibility and executability of global task dependencies and collaborative relations during distributed execution, thereby enabling specification-compliant progress. Simulations on 25 mission instances, comparative and ablation evaluations, and physical multi-robot experiments demonstrate reliable task completion under communication disruptions and robot removal while maintaining satisfaction of temporal and collaborative requirements.

## Round 5

Reviewer focus:
- Merge repeated language around resilient runtime execution, runtime executability, and visibility/executability.
- Replace hard wording with "restores runtime progress".
- Use "prerequisite-task and team-formation information".
- Make the final result sentence shorter and more IEEE-like.

Final abstract:

> In large industrial sites and photovoltaic power stations, heterogeneous robots often perform inspection, transport, and maintenance across separated regions under ordering, safety, and collaborative-team requirements. Since reliable full-coverage communication is difficult to guarantee in such environments, robots may have to rely on short-range peer-to-peer links. This paper considers these finite-region missions specified by a global syntactically co-safe linear temporal logic (sc-LTL) formula. When robots move out of communication range or are removed after faults, completion messages and team-formation updates may fail to reach the robots that depend on them, so a robot can wait for a prerequisite that has already been completed, or a collaborative subtask can lose an assigned participant. These failures can stall downstream tasks and break global mission execution. To address this problem, we develop a resilient distributed execution framework that derives robot-level executable plans from the global specification and restores progress during runtime. The runtime layer enables robots to recover missing prerequisite status, re-establish feasible collaborative teams under sparse connectivity, and share failure information for distributed reassignment. Simulations on 25 mission instances, comparative and ablation evaluations, and physical multi-robot experiments show reliable task completion under communication disruptions and robot removal while satisfying temporal and collaborative requirements.

## Complete Abstract

In large facilities such as industrial plants and photovoltaic power stations, heterogeneous robots may need to inspect, transport, and maintain equipment across separated regions while respecting task order, safety constraints, and collaboration requirements. Such missions can be specified by a global syntactically co-safe linear temporal logic (sc-LTL) formula. In practice, however, distance, interference, and incomplete communication infrastructure may temporarily disconnect the communication network, so robots cannot always obtain complete team-state information. This paper studies resilient distributed task allocation for heterogeneous multi-robot systems under global sc-LTL specifications and intermittent communication. Without timely team-state updates, robots may not know whether prerequisite subtasks have been completed or whether a collaborative team still satisfies the required robot types and cardinalities. As a result, temporally dependent subtasks can remain blocked, and collaborative subtasks can fail to start or recover. We first translate the global sc-LTL formula into a nondeterministic Büchi automaton, prune the automaton, decompose it into subtasks with temporal relations, and generate initial robot-level plans through a consensus-based timetable algorithm. More importantly, the proposed execution framework restores progress online by recovering missing prerequisite status, re-establishing feasible collaborative teams, and propagating failure information for distributed reassignment when communication disruptions or robot removal invalidate local plans. Simulations on 25 mission instances, comparative and ablation evaluations, and physical multi-robot experiments show that the proposed framework reliably completes missions under communication disruptions and robot removal while satisfying temporal and collaborative requirements.

## Reorganized Abstract

In large facilities such as industrial plants and photovoltaic power stations, heterogeneous robots may need to inspect, transport, and maintain equipment across separated regions while respecting task order, safety constraints, and collaboration requirements. Such missions can be specified by a global syntactically co-safe linear temporal logic (sc-LTL) formula. In practice, however, distance, interference, and incomplete communication infrastructure may temporarily disconnect the communication network, so robots cannot always obtain complete team-state information. This paper studies resilient distributed task allocation for heterogeneous multi-robot systems under global sc-LTL specifications and intermittent communication. Without timely team-state updates, robots may not know whether prerequisite subtasks have been completed or whether a collaborative team still satisfies the required robot types and cardinalities. As a result, temporally dependent subtasks can remain blocked, and collaborative subtasks can fail to start or recover. We first translate the global sc-LTL formula into a nondeterministic Büchi automaton, prune the automaton, decompose it into subtasks with temporal relations, and generate initial robot-level plans through a consensus-based timetable algorithm. More importantly, the proposed execution framework restores progress online by recovering missing prerequisite status, re-establishing feasible collaborative teams, and propagating failure information for distributed reassignment when communication disruptions or robot removal invalidate local plans. Simulations on 25 mission instances, comparative and ablation evaluations, and physical multi-robot experiments show that the proposed framework reliably completes missions under communication disruptions and robot removal while satisfying temporal and collaborative requirements.

## Five-Round Abstract Revision, Second Pass

Reviewer subagent: Arendt
Student subagent: Poincare

### Round 1

Reviewer focus:
- The requested structure is present, but resilience should mean recovery of task dependencies, collaboration relations, and allocation after communication disruption or robot removal.
- The NBA/pruning/decomposition/CBTA flow should be clearer but remain secondary.
- Avoid vague claims such as preventing progress from being blocked; state what missing information causes and what is restored.
- The experiment sentence should connect back to facility inspection and maintenance.

Student draft:

> In large-scale facilities such as industrial plants and photovoltaic power stations, heterogeneous robots are often required to inspect, transport, and maintain equipment across separated regions while satisfying task order, safety rules, and collaboration requirements. This paper studies resilient distributed task allocation for heterogeneous multi-robot systems executing global syntactically co-safe linear temporal logic (sc-LTL) specifications under range-limited communication. In such missions, distance, interference, or sparse communication infrastructure can temporarily disconnect robots, making team-state information incomplete or delayed. When this happens, a robot may not know whether a prerequisite subtask has been completed, whether a required collaborator is still available, or whether a previous assignment has become infeasible after robot removal, which can leave dependent tasks waiting or invalidate collaborative execution. To obtain executable subtasks, the global sc-LTL formula is translated into a nondeterministic Büchi automaton, pruned to remove infeasible transitions, decomposed into temporally related subtasks, and assigned through a consensus-based timetable algorithm. The main contribution is a resilient execution framework that rebuilds sufficient task-execution state without relying on persistent global communication. It restores prerequisite completion status, repairs feasible collaborative teams, shares failure information when disrupted robots or subtasks are detected, and reallocates affected tasks so that execution can continue after communication loss or robot removal. Simulations and physical experiments on distributed facility inspection and maintenance missions show that the proposed method maintains temporal and collaborative requirements while recovering from communication and robot failures.

### Round 2

Reviewer focus:
- Reduce remaining AI-like abstract phrases.
- Shorten the planning flow sentence.
- Make the recovery contribution less like a list of mechanisms and more about restoring mission progress.
- Use "communication disruptions and robot removal" consistently.

Student draft:

> In large-scale facilities such as industrial plants and photovoltaic power stations, heterogeneous robots are often required to inspect, transport, and maintain equipment across separated regions while satisfying task order, safety rules, and collaboration requirements. This paper studies resilient distributed task allocation for heterogeneous multi-robot systems executing global syntactically co-safe linear temporal logic (sc-LTL) specifications under range-limited communication. In such missions, distance, interference, or sparse communication infrastructure can temporarily disconnect robots, making team-state information incomplete or delayed. When this happens, a robot may not know whether a prerequisite subtask has been completed, whether a required collaborator is still available, or whether an assignment has become infeasible after robot removal. These uncertainties can leave dependent tasks waiting and cause collaborative subtasks to fail. The global sc-LTL formula is processed through an automaton-based pipeline to extract temporally related subtasks, remove infeasible choices, and generate initial robot-level schedules using a consensus-based timetable algorithm. The main contribution is a resilient execution framework that recovers the information needed for the mission to move forward without relying on persistent global communication. After communication disruptions or robot removal, the framework helps robots confirm missing prerequisite status, re-form feasible collaboration teams, propagate detected failures, and update affected allocations as part of a unified recovery process. Simulations and physical experiments on distributed facility inspection and maintenance missions show that the proposed method completes tasks under communication disruptions and robot removal while preserving temporal order and collaboration requirements.

### Round 3

Reviewer focus:
- The automaton flow should be short but specific: NBA construction, pruning, subtask decomposition, and CBTA scheduling.
- Avoid imprecise terms such as "remove infeasible choices".
- Replace overly casual phrasing and avoid overclaiming the experimental result.

Student draft:

> In large-scale facilities such as industrial plants and photovoltaic power stations, heterogeneous robots are often required to inspect, transport, and maintain equipment across separated regions while satisfying task order, safety rules, and collaboration requirements. This paper studies resilient distributed task allocation for heterogeneous multi-robot systems executing global syntactically co-safe linear temporal logic (sc-LTL) specifications under range-limited communication. In such missions, distance, interference, or sparse communication infrastructure can temporarily disconnect robots, making team-state information incomplete or delayed. When this happens, a robot may not know whether a prerequisite subtask has been completed, whether a required collaborator is still available, or whether an assignment has become infeasible after robot removal. These uncertainties can leave dependent tasks waiting and cause collaborative subtasks to fail. The proposed method uses NBA construction, infeasible-transition pruning, subtask decomposition, and consensus-based timetable algorithm (CBTA) scheduling to derive executable robot-level plans from the global sc-LTL specification. The main contribution is a resilient execution framework that keeps the mission recoverable under communication disruptions and robot removal, without assuming persistent global communication. During execution, robots infer missing prerequisite completion status, recover feasible collaboration teams, exchange detected robot and subtask failure information when contact is restored, and update affected allocations to regain task progress. Simulations and physical experiments on distributed facility inspection and maintenance missions show that the proposed method supports mission completion under communication disruptions and robot removal while respecting temporal order and collaboration requirements.

### Round 4

Reviewer focus:
- Replace "infer" with recover/verify because the mechanism may rely on communication and synchronization, not pure inference.
- Replace "when contact is restored" with "when communication becomes available".
- Make the planning sentence begin with "To obtain initial plans" to keep the flow secondary.
- Use "satisfying temporal and collaborative requirements" in the result sentence.

Student draft:

> In large-scale facilities such as industrial plants and photovoltaic power stations, heterogeneous robots are often required to inspect, transport, and maintain equipment across separated regions while satisfying task order, safety rules, and collaboration requirements. This paper studies resilient distributed task allocation for heterogeneous multi-robot systems executing global syntactically co-safe linear temporal logic (sc-LTL) specifications under range-limited communication. In such missions, distance, interference, or sparse communication infrastructure can temporarily disconnect robots, making team-state information incomplete or delayed. When this happens, a robot may not know whether a prerequisite subtask has been completed, whether a required collaborator is still available, or whether an assignment has become infeasible after robot removal. These uncertainties can leave dependent tasks waiting and cause collaborative subtasks to fail. To obtain initial plans, the method performs NBA construction, infeasible-transition pruning, subtask decomposition, and consensus-based timetable algorithm (CBTA) scheduling from the global sc-LTL specification. The main contribution is a resilient execution framework that maintains the ability to recover mission execution under communication disruptions and robot removal, without assuming persistent global communication. During execution, robots recover or verify prerequisite completion status, rebuild feasible collaboration teams, share detected robot and subtask failure information when communication becomes available, and update affected allocations to regain task progress. Simulations and physical experiments on distributed facility inspection and maintenance missions show that the proposed method supports mission completion under communication disruptions and robot removal while satisfying temporal and collaborative requirements.

### Round 5

Reviewer focus:
- The abstract is structurally aligned with the request and readme.
- The only final issue is the phrasing "performs ... scheduling from the global sc-LTL specification".
- Use "applies ... to the global sc-LTL specification to obtain initial robot-level plans".

Final abstract:

> In large-scale facilities such as industrial plants and photovoltaic power stations, heterogeneous robots are often required to inspect, transport, and maintain equipment across separated regions while satisfying task order, safety rules, and collaboration requirements. This paper studies resilient distributed task allocation for heterogeneous multi-robot systems executing global syntactically co-safe linear temporal logic (sc-LTL) specifications under range-limited communication. In such missions, distance, interference, or sparse communication infrastructure can temporarily disconnect robots, making team-state information incomplete or delayed. When this happens, a robot may not know whether a prerequisite subtask has been completed, whether a required collaborator is still available, or whether an assignment has become infeasible after robot removal. These uncertainties can leave dependent tasks waiting and cause collaborative subtasks to fail. To obtain initial robot-level plans, the method applies NBA construction, infeasible-transition pruning, subtask decomposition, and consensus-based timetable algorithm (CBTA) scheduling to the global sc-LTL specification. The main contribution is a resilient execution framework that maintains the ability to recover mission execution under communication disruptions and robot removal, without assuming persistent global communication. During execution, robots recover or verify prerequisite completion status, rebuild feasible collaboration teams, share detected robot and subtask failure information when communication becomes available, and update affected allocations to regain task progress. Simulations and physical experiments on distributed facility inspection and maintenance missions show that the proposed method supports mission completion under communication disruptions and robot removal while satisfying temporal and collaborative requirements.

## Logic-Adjusted Final Abstract

In large-scale facilities such as industrial plants and photovoltaic power stations, heterogeneous robots may inspect, transport, and maintain equipment across separated regions while satisfying task order, safety rules, and collaboration requirements. These missions can be specified by global syntactically co-safe linear temporal logic (sc-LTL) formulas, but their distributed execution is vulnerable to communication disruptions. Distance, interference, and sparse communication infrastructure may temporarily disconnect robots, making team-state information incomplete or delayed. As a result, a robot may be unable to confirm whether a prerequisite subtask has been completed, whether a required collaborator is still available, or whether an assignment has become infeasible after robot removal. Such uncertainty can leave temporally dependent subtasks waiting and cause collaborative subtasks to fail. This paper studies resilient distributed task allocation for heterogeneous multi-robot systems under global sc-LTL specifications and range-limited communication. To obtain initial robot-level plans, the method applies NBA construction, infeasible-transition pruning, subtask decomposition, and consensus-based timetable algorithm (CBTA) scheduling to the global specification. The main contribution is a resilient execution framework that recovers mission progress when communication disruptions or robot removal invalidate the information needed for execution. During execution, robots recover or verify prerequisite completion status, rebuild feasible collaboration teams, share detected robot and subtask failure information when communication becomes available, and update affected allocations. Simulations and physical experiments on distributed facility inspection and maintenance missions show that the proposed method supports mission completion under communication disruptions and robot removal while satisfying temporal and collaborative requirements.

## Innovation-Focused Abstract

This paper studies resilient distributed task allocation for heterogeneous multi-robot systems executing global syntactically co-safe linear temporal logic (sc-LTL) missions under range-limited communication. Such missions often arise in large-scale facilities, such as industrial plants and photovoltaic power stations, where robots with different capabilities must complete temporally ordered and collaborative subtasks across separated regions. However, large distances between target regions and sparse communication infrastructure may temporarily split the communication network into disconnected components, so robots cannot always obtain complete and timely team-state information. This lack of global execution awareness can block successor subtasks whose prerequisites cannot be confirmed and can invalidate collaborative subtasks when required robots are disconnected or removed. We first derive a temporally structured subtask representation from the global sc-LTL specification through NBA construction, pruning, and decomposition, and compute initial robot-level schedules through a consensus-based timetable algorithm (CBTA). The key contribution is a resilient execution framework that closes the gap between an initially feasible schedule and reliable distributed execution under fragmented team-state information. Rather than only replanning after failures, the framework restores the execution conditions needed to satisfy the global specification. It actively recovers prerequisite-completion status to release blocked successors, reconstructs type- and cardinality-consistent teams for collaborative subtasks, and returns failed collaborations to distributed allocation when local recovery is insufficient. Simulations and physical multi-robot experiments demonstrate reliable mission completion and recovery under communication constraints and robot removal while satisfying temporal and collaborative requirements.

## Five-Round Contribution Discussion

Reviewer subagent: Noether

Student subagent: Carson

### Round 1

Reviewer focus:
- The contribution should not read as only collaborative-failure recovery.
- It should cover three unfinished-execution cases in the paper: missing prerequisite information, uncertain or failed non-collaborative assignments, and insufficient collaborators.
- The deeper point is that the framework restores executability under fragmented team-state information, not merely that it replans after a failure.

Student revision direction:

> The contribution should be framed as an execution layer that makes unfinished subtasks executable again when local robot knowledge becomes incomplete, stale, or inconsistent.

### Round 2

Reviewer focus:
- The mechanism must remain visible enough to be credible.
- Timeout-based expiry, active prerequisite-status acquisition, and collaboration repair from local recruitment to free-market reassignment should all appear, but without turning the abstract into a mechanism list.

Student revision direction:

> The proposed execution layer provides information-aware recovery for distributed plans under limited communication and robot failures, converting stale or missing execution evidence into targeted actions for abandoned individual subtasks, blocked successors, and under-staffed collaborations.

### Round 3

Reviewer focus:
- "Execution evidence" is useful but slightly abstract.
- The sentence should be split into a contribution-positioning sentence and a mechanism sentence.
- "Before successors remain blocked" is awkward and should become "to unblock successors."

Student revision direction:

> The proposed execution layer turns missing or stale execution knowledge into recovery actions. It expires uncertain non-collaborative assignments for replanning, actively recovers missing prerequisite status to unblock successors, and repairs under-staffed collaborations from local recruitment to free-market reassignment.

### Round 4

Reviewer focus:
- "Reopen uncertain assignments" is inaccurate because the paper uses timeout or expiry to trigger replanning rather than reopening the original assignment.
- "Type-constrained" and "type-compatible" should not both be used in the same phrase.
- The final wording should keep multi-hop state sharing, timeout-based replanning, active prerequisite-status recovery, and progressive collaboration repair.

Student revision direction:

> Built on multi-hop state sharing, the proposed execution layer provides information-aware recovery for distributed plans under limited communication and robot failures, turning missing or stale execution evidence into actions that make unfinished subtasks executable again. It uses timeout-based expiry to trigger CBTA replanning for uncertain non-collaborative assignments, actively acquires missing prerequisite status to unblock successors, and progressively repairs under-staffed collaborations from local type-compatible recruitment to free-market reassignment.

### Round 5

Reviewer focus:
- "Expire uncertain non-collaborative assignments" is more accurate than "reopen uncertain assignments."
- The abstract should emphasize the bridge from an initially feasible allocation to executable progress under fragmented team-state information.
- The mechanism sentence should include all three recovery targets while staying concise.

Final integrated contribution wording:

> The key contribution is a resilient execution layer that turns fragmented execution knowledge into concrete recovery actions without relying on a continuously shared team state. During execution, robots propagate task and robot states through direct and multi-hop contacts, reallocate non-collaborative subtasks when an assigned robot's state becomes outdated or the robot is removed, recover prerequisite-completion status to release blocked successors, and repair collaborative subtasks by recruiting reachable type-compatible teammates or synchronizing failure information for free-market reassignment.

Core idea:

> The framework does not simply replan whenever execution becomes inconsistent. Its deeper principle is to rebuild the missing execution support needed by each affected subtask under fragmented communication. A subtask becomes executable only when its temporal prerequisite, assignment validity, and collaboration feasibility are sufficiently supported by the information available to the relevant robots. Limited communication and robot removal break this support, so the runtime layer restores it through state propagation, reassignment, prerequisite-status recovery, and collaboration repair instead of assuming a persistent global team view.

## Contribution-Refined Abstract

This paper studies resilient distributed task allocation for heterogeneous multi-robot systems executing global syntactically co-safe linear temporal logic (sc-LTL) missions under range-limited communication. Such missions often arise in large-scale facilities, such as industrial plants and photovoltaic power stations, where robots with different capabilities must complete temporally ordered and collaborative subtasks across separated regions. However, large distances among target regions and sparse communication infrastructure may temporarily split the communication network into disconnected components, so robots cannot always obtain complete and timely team-state information. This lack of global execution awareness can block successor subtasks whose prerequisites cannot be confirmed, leave non-collaborative assignments unresolved when an assigned robot becomes unreachable or is removed, and invalidate collaborative subtasks when required robots are disconnected or removed. We first derive a temporally structured subtask representation from the global sc-LTL specification through NBA construction, pruning, and decomposition, and compute initial robot-level schedules through a consensus-based timetable algorithm (CBTA). The key contribution is a resilient execution layer that turns fragmented execution knowledge into concrete recovery actions without relying on a continuously shared team state. During execution, robots propagate task and robot states through direct and multi-hop contacts, reallocate non-collaborative subtasks when an assigned robot's state becomes outdated or the robot is removed, recover prerequisite-completion status to release blocked successors, and repair collaborative subtasks by recruiting reachable type-compatible teammates or synchronizing failure information for free-market reassignment. Simulations and physical multi-robot experiments demonstrate reliable mission completion and recovery under communication constraints and robot removal while satisfying temporal and collaborative requirements.

## Five-Round Contribution Discussion, Final Pass

Reviewer subagent: Hume

Student subagent: Halley

### Round 1

Reviewer focus:
- The current version is too close to an engineering list.
- The contribution should connect three layers: the information conditions broken by disconnection or robot removal, the execution objects to be restored, and the high-level operations that restore them.
- Avoid mechanism names such as patrol, timeout, and free market in the abstract contribution sentence.

Student draft:

> The key contribution is a resilient execution layer that keeps a global sc-LTL mission executable when range-limited communication breaks the team's shared execution record. It restores progress by recovering prerequisite evidence for temporally dependent subtasks, releasing non-collaborative assignments whose executors become unverifiable, and rebuilding collaborative subtasks around capabilities that remain reachable or can be reallocated.

### Round 2

Reviewer focus:
- "Shared execution record" sounds like a database log, so "team-state information" is more natural.
- "Prerequisite evidence" sounds legalistic and should become "prerequisite-completion status."
- Collaborative recovery should retain type and cardinality information.

Student draft:

> The key contribution is a resilient execution layer that maintains the executability of sc-LTL-derived robot schedules when range-limited communication or robot removal leaves team-state information incomplete, stale, or inconsistent. It restores the execution support needed for progress by making prerequisite completion verifiable, reintroducing unverifiable individual assignments into distributed allocation, and re-establishing collaborations with the required robot types and team sizes through communication-aware coordination.

### Round 3

Reviewer focus:
- "Incomplete, stale, or inconsistent" is a little crowded.
- "Execution support needed for progress" is still vague.
- "Individual-task accountability" should be avoided because it can sound like auditing rather than task recovery.

Student draft:

> The key contribution is a resilient execution layer that keeps sc-LTL-derived schedules executable when range-limited communication or robot removal fragments the team-state information on which the initial allocation relies. The layer restores the conditions needed for continued progress by confirming prerequisite completion before successors proceed, bringing unverifiable individual subtasks back into distributed allocation, and rebuilding collaborative teams with the required robot types and counts.

### Round 4

Reviewer focus:
- The innovation should be framed as converting an initially feasible allocation into a recoverable distributed execution process.
- This better distinguishes the work from simply computing an initial task allocation.
- The second sentence should use a few accurate operations rather than a long mechanism list.

Student draft:

> The key contribution is a resilient execution layer that turns an initially feasible sc-LTL allocation into a recoverable distributed execution process when range-limited communication or robot removal fragments the team-state information on which the allocation relies. It preserves mission progress by confirming prerequisite completion for dependent subtasks, returning unverifiable individual commitments to distributed allocation, and re-forming collaborative teams with the required robot types and counts.

### Round 5

Reviewer focus:
- The main contribution is clear enough for abstract use.
- "Leaves the team-state information needed by the allocation fragmented" is slightly awkward.
- "Individual task commitments" is clearer than "individual commitments," but "individual tasks with unverifiable executors" is even more direct.
- "Communication-aware coordination and reassignment" is enough to hint at collaborative repair without naming every mechanism.

Final integrated contribution wording:

> The key contribution is a resilient execution layer that turns an initially feasible sc-LTL allocation into a recoverable distributed execution process when range-limited communication or robot removal makes the team-state information required by the allocation incomplete or stale. Rather than passively waiting for network-wide updates, robots move and gather to recover the information needed for execution, confirming prerequisite completion for dependent subtasks, returning individual tasks with unverifiable executors to distributed allocation, and re-forming collaborative teams with the required robot types and counts through coordinated reassignment.

## Final Contribution-Refined Abstract

This paper studies resilient distributed task allocation for heterogeneous multi-robot systems executing global syntactically co-safe linear temporal logic (sc-LTL) missions under range-limited communication. Such missions often arise in large-scale facilities, such as industrial plants and photovoltaic power stations, where robots with different capabilities must complete temporally ordered and collaborative subtasks across separated regions. However, large distances among target regions and sparse communication infrastructure may temporarily split the communication network into disconnected components, so robots cannot always obtain complete and timely team-state information. This lack of global execution awareness can block successor subtasks whose prerequisites cannot be confirmed, leave non-collaborative assignments unresolved when an assigned robot becomes unreachable or is removed, and invalidate collaborative subtasks when required robots are disconnected or removed. We first derive a temporally structured subtask representation from the global sc-LTL specification through NBA construction, pruning, and decomposition, and compute initial robot-level schedules through a consensus-based timetable algorithm (CBTA). The key contribution is a resilient execution layer that turns an initially feasible sc-LTL allocation into a recoverable distributed execution process when range-limited communication or robot removal makes the team-state information required by the allocation incomplete or stale. Rather than passively waiting for network-wide updates, robots move and gather to recover the information needed for execution, confirming prerequisite completion for dependent subtasks, returning individual tasks with unverifiable executors to distributed allocation, and re-forming collaborative teams with the required robot types and counts through coordinated reassignment. Simulations and physical multi-robot experiments demonstrate reliable mission completion and recovery under communication constraints and robot removal while satisfying temporal and collaborative requirements.
