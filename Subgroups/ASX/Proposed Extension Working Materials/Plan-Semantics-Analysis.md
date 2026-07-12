# C2SIM Plan Constructs and Autonomous-System Behavior Semantics

**Correlation with behavior trees and BDI, feasibility of extension, and a proposed ASX plan-semantics module**

*Status: working analysis for the ASX subgroup — not an adopted proposal.*

---

## 1. Purpose and scope

This document examines the "plan" entities of the C2SIM ontology family, correlates them
with the semantic mechanisms used by autonomous systems to represent executable behavior —
principally **behavior trees (BT)** and **belief–desire–intention (BDI)** agent models, with
hierarchical task networks (HTN) as a connecting formalism — and assesses whether the
existing plan constructs can be extended to carry that richer semantics.

**Summary of conclusions:**

1. C2SIM's plan construct (`lox:PlanBody` / `lox:PlanPhase`) is not merely a task container:
   it is a rudimentary *reactive execution* model (triggers + completion conditions +
   recursive decomposition) and is structurally much closer to a behavior-tree skeleton than
   its "phased land-operations plan" framing suggests.
2. Extension **is feasible** without modifying core C2SIM or LOX. Every mechanism needed
   (subclassing triggers, adding code-list individuals, subclassing `PlanPhase`, adding new
   `ReportContent` types) is an idiom the standard already uses for its own extensions.
   A separate, standalone ontology is therefore *not* required; what is required is an
   additive **plan-semantics module** in the ASX layer.
3. The main semantic deficits relative to BT/BDI are precisely enumerable: no failure
   status, no fallback/alternative branching, no state-predicate guards, no loop/persistence
   semantics, no goal (end-state) object distinct from procedure, no plan-selection context
   conditions, and no intention/rationale reporting. Section 5 proposes constructs for each,
   in the standard's own style.

Sources examined: `Ontology/C2SIM.rdf` (core, CWIX2025 build of SISO C2SIM 1.0.1),
`Ontology/C2SIM_SMX.rdf`, `Ontology/C2SIM_LOX.rdf`,
`Subgroups/ASX/Proposed Extension/CSIM_ASX.rdf` (v0.0.1), the ASX instantiation-review
walk documents and decision log, the contributed CASEVAC and MUTT scenarios, and
`Subgroups/ASX/Reference Materials/Standards-for-Autonomous-Systems-Behavior.md`.

---

## 2. What C2SIM can say today about plans and control flow

### 2.1 Core: Order → Task, and two temporal idioms

Core C2SIM has **no Plan class**. Tasking is carried by `OrderBody` (a
`DomainMessageBody`), which defines tasks inline (`hasTask`, 0..\*) or references
previously defined ones (`hasTaskReference`, 0..\*). A `Task` (⊑ `Action`) answers
WHO/WHAT/WHEN/WHERE: exactly one `hasTaskActionCode` and `hasPerformingEntity`, optional
start/end/duration, location, affected entities, and optionally WHY via
`hasDesiredEffectCode`.

Control flow between tasks is expressible only through two temporal idioms:

- **`ActionTemporalRelationship`** — a reified pairwise relation on any `Action`, with an
  18-member Allen-style code list (`ActionTemporalAssociationCode`, JC3IEDM-derived):
  `STREND` (starts after end of — plain sequencing), `STRSTR`, `ENDEND`, `ENDSTR`,
  concurrency codes, and duration-augmented variants (`STRENE`, `STRENL`, …).
- **`RelativeTime`** — a `TimeInstant` defined as an `Event` reference plus a
  `TimeReferenceCode` (`IntervalStartTime`/`IntervalEndTime`) and a `hasDelayTimeAmount`
  offset. Since `EventCode` includes `TaskStart`/`TaskEnd`, a task's start can be anchored
  to another task's lifecycle.

Execution feedback is `ReportBody` → `TaskStatus` (⊑ `ReportContent`) with exactly one
`hasTaskStatusCode` and `hasCurrentTask`. The `TaskStatusCode` list is:
`TASKPEND`, `TASKSTRT`, `TASKINPRG`, `TASKCMPLT`, `TASKABRT`. **There is no failure
status** — a task completes or is aborted; "attempted and did not succeed" is not sayable.

Two core features worth flagging because they become load-bearing later:

- `CommunicativeActTypeCode` on the message header already carries FIPA-style performatives
  (`Accept`, `Agree`, `Confirm`, `Inform`, `Propose`, `Refuse`, `Request`) — a BDI/FIPA
  hook that exists today.
- `RequestBody` vs `OrderBody` already distinguishes deontic force ("fulfilled at the
  discretion of the receiver" vs "expected to be obeyed"), relevant to robot-to-robot
  coordination (review item X1/Q-G).

### 2.2 LOX: the Plan construct

The plan machinery lives entirely in the Land Operations Extension
(`Ontology/C2SIM_LOX.rdf`):

| Construct | Structure |
|---|---|
| `lox:PlanBody` ⊑ `C2SIM:DomainMessageBody` | `hasPlanPhase` 0..\*, `hasPlanPhaseReference` 0..\* (UUID), `isToBeExecutedNow` exactly 1 |
| `lox:PlanPhase` ⊑ `C2SIM:C2SIMContent` | `hasSubPhase` 0..\* (**recursive**), `hasPlanPhaseTrigger` **exactly 1**, `hasPlanPhaseCompletionCondition` **exactly 1**, `C2SIM:hasTaskReference` 0..\* |
| `lox:PlanPhaseTrigger` (abstract) | subclasses: `EventTrigger` (exactly 1 `hasEvent`), `OnOrderTrigger` (exactly 1 `hasTaskReference`, typically a task with `TaskActionCode` = `lox:ExecutePlanPhase`), `PriorPhaseCompletionTrigger` (exactly 1 `hasTriggerPhase` UUID) |
| `lox:PlanPhaseCompletionCondition` ⊑ `C2SIM:Code` | individuals: `AllTasksComplete`, `OneTaskComplete`, `OtherOrderReceived` |

LOX additionally provides `ManeuverWarfareTask` ⊑ `Task` with `hasRuleOfEngagement` 0..\*
and `hasTaskFunctionalRelation` 0..\* — the latter a reified relation whose JC3IEDM code
list includes genuinely contingency-flavored values: `ALT` (*is an alternative to*),
`HASPRV` (*has as a provisional sub-action*), `ISAPRQ` (*is a prerequisite for*), `INRSTO`
(*in response to*), `IMO` (*is a modification of*). These codes *label* contingency
relationships but carry no activation semantics — nothing states *when* the alternative
becomes the active branch.

### 2.3 ASX v0.0.1: no behavior layer yet

The proposed ASX ontology (`Subgroups/ASX/Proposed Extension/CSIM_ASX.rdf`) is a
platform/device taxonomy (Artifact/Device/Sensor/Actuator/RoboticSystem/Robot/UAV/UGV/
Swarm, 15 classes) plus one dangling property (`hasAutonomousRoleCode`) and an
undocumented four-value autonomy code list (`Teleop`, `ReCont`, `Automated`, `FullAuto`).
It contains **nothing** for behavior specification, conditional execution, triggers,
delegation, or contingencies. The subgroup's own instantiation review says as much: the
central unaddressed items in the decision log include autonomy-level-to-engagement-authority
linkage (W1/Q-K), rationale/explainability reporting (X2/Q-H), mid-mission re-tasking
semantics (X6), coverage/termination goal semantics (Q-N), graded phase-dependent autonomy
(Q-D), and persistent/standing tasking (N2). This analysis is intended to serve exactly
that roadmap.

---

## 3. Correlation with autonomous-system behavior formalisms

### 3.1 Behavior trees

A behavior tree is a directed tree whose internal nodes are *composites* (Sequence,
Fallback/Selector, Parallel), possibly wrapped by *decorators* (inverters, retry loops,
guards, timeouts), and whose leaves are *actions* and *conditions*; execution proceeds by
ticking the root, and every node returns one of **Success / Failure / Running**.

The LOX plan model already covers a surprising share of this:

| BT concept | LOX plan analog | Fidelity |
|---|---|---|
| Composite node | `PlanPhase` with `hasSubPhase` children | good — recursion is native |
| Sequence node | subphase chain via `PriorPhaseCompletionTrigger` | good, though encoded pairwise rather than as an ordered container |
| Parallel node, success-on-all policy | phase with several tasks + `AllTasksComplete` | good |
| Parallel node, success-on-one policy | phase + `OneTaskComplete` | good |
| Leaf action node | `Task` referenced from a phase | good |
| Reactive guard on entry | `EventTrigger` | partial — fires on an *Event occurrence*, not on an evaluable predicate over world state |
| External preemption | `OtherOrderReceived` completion; `OnOrderTrigger` | partial — human-initiated only |
| **Failure status** | — | **absent**: phases and tasks complete or abort; nothing fails |
| **Fallback / Selector node** | — | **absent**: `ALT`/`HASPRV` codes name alternatives but nothing activates them |
| **Condition (leaf) node** | — | **absent**: no predicate language over entities/locations/health/comms |
| **Decorators: retry, loop, timeout** | — | **absent**: no repetition or persistence semantics; MUTT route-clearance "repeat detection–neutralization along route" is not expressible |
| Running status / tick | `TASKINPRG` reports | adequate — see §3.4 on what should *not* be imported |
| Priority/reactive re-evaluation | — | absent: triggers are evaluated as one-shot start conditions, not continuously re-evaluated guards |

The structural conclusion: **the trigger/completion-condition pattern is the right chassis.**
A BT's control-flow node types differ from `PlanPhase` mainly in (a) having a failure
outcome and a policy for reacting to it, and (b) allowing guards over state, not just
events. Both are additive.

### 3.2 BDI

BDI separates **beliefs** (world model), **desires/goals** (end states, possibly
maintained), and **intentions** (goals the agent has committed to, realized by selecting
plans from a *plan library*, where each plan has a triggering event, a *context condition*
gating applicability, and a body). Mapping against C2SIM:

| BDI concept | C2SIM analog | Fidelity |
|---|---|---|
| Beliefs | `ReportBody`/`ObservationReportContent` (SMX), position/health reports | partial — C2SIM exchanges belief *updates*; adequate as-is, since the belief store itself belongs to the executing system |
| Desire / goal | `hasDesiredEffectCode` on Task | weak — a code annotation on a *procedure*, not a first-class end state; nothing states the conditions under which the goal counts as achieved or failed |
| Achievement vs maintenance goals | — | absent — no standing "maintain comms / keep station" semantics (review item N2: persistent vs one-shot tasking) |
| Plan (recipe) | `PlanBody`/`PlanPhase` | good — this is exactly a plan body |
| Plan library + context condition | — | absent — one plan per message; no way to send several alternative plans for one goal with applicability conditions |
| Triggering event of a plan | `EventTrigger`/`OnOrderTrigger` | good |
| Intention / commitment state | — | absent — no way for a subordinate to report *which* plan it has adopted, what it is pursuing, or why it deviated (review items X2, X6) |
| Communication performatives | `CommunicativeActTypeCode` (FIPA-style) | good — already present in core |
| Delegation of authority | Order vs Request deontic split | partial — no construct for whether a robot may itself issue orders, nor for approval gates as a function of autonomy level (W1/Q-K, Q-P) |

The BDI correlation exposes the *tasking philosophy* gap: C2SIM orders are procedural
(do these tasks), whereas autonomy increasingly requires **goal-directed tasking** (achieve
this end state under these constraints, choose your own procedure). Notably, C2SIM's own
Task comment already gestures at this ("WHY may be represented by hasDesiredEffect") — the
extension direction is consistent with the standard's intent, not a departure from it.

### 3.3 HTN, briefly

`hasSubPhase` recursion is exactly HTN-style decomposition of an abstract phase into
subtasks; what HTN adds is *methods* — multiple alternative decompositions with
preconditions. That is the same missing piece as the BT Fallback node and the BDI plan
library: **alternatives + the conditions that select among them.** One construct
(§5.3–§5.4) covers all three formalisms. This also matches the Remmersmann et al. (2015)
MUM-T pattern already summarized in `LLMExperiments/`: high-level order, machine
decomposition, capability-based assignment, threshold-triggered reassignment.

### 3.4 What should *not* be imported

An interoperability standard should exchange the *structure and intent* of behavior, not
its execution engine. Tick frequency, blackboard mechanics, node memory
(reactive vs. memory-sequence), and BDI deliberation cycles are properties of the executing
system and would over-constrain implementations while adding nothing to interoperability.
The proposal below therefore models BT/BDI *concepts* (as recommended by the subgroup's own
standards survey: "model the BT concepts … rather than cite a standard", with IEEE 1872.1/
1872.2 as backbone and FIPA/BDI for the goal/intention layer) and deliberately excludes
execution-engine semantics. Likewise, a general-purpose logical expression language is
avoided: C2SIM's style is closed code lists with an escape hatch, and §5.4 follows it.

---

## 4. Feasibility of extending the plan construct

**Verdict: feasible, additively, in the ASX layer — no changes to core or LOX required,
and no separate standalone ontology needed.** The assessment rests on the standard's own
extension idioms, all verified in the existing artifacts:

1. **Open trigger hierarchy.** `PlanPhaseTrigger` is an abstract collection class with
   three subclasses; nothing prevents a fourth (`StateConditionTrigger`,
   `HumanApprovalTrigger`, `CompositeTrigger`). This is the same pattern LOX itself used.
2. **Open code lists.** Extensions already populate core code classes with new individuals
   (SMX adds 25 `DesiredEffectCode`s; LOX adds 446 `TaskActionCode`s). Adding e.g.
   `TASKFAILD` to `TaskStatusCode` and failure-oriented individuals to
   `PlanPhaseCompletionCondition` follows precedent exactly.
3. **Subclass-and-restrict.** LOX's `ManeuverWarfareTask` ⊑ `C2SIM:Task` shows the
   sanctioned way to enrich an existing concept: subclass it and add qualified-cardinality
   restrictions over new properties. An `asx:AutonomousPlanPhase` ⊑ `lox:PlanPhase`
   inherits all existing machinery and adds failure handling, guards, and policies. Legacy
   consumers can process such a phase as a plain `PlanPhase`, ignoring the additions —
   graceful degradation comes free.
4. **New message content by subclassing `ReportContent`.** SMX's
   `ObservationReportContent` is the template for the rationale/intention reports in §5.6.
5. **UUID-reference style.** All new cross-references (fallback phase, goal reference,
   approving entity) use datatype properties over `C2SIM:UUIDBase`, per the core
   `hasReference` subproperty tree.

Frictions found, none blocking:

- `hasPlanPhaseTrigger` is **exactly 1** on `PlanPhase`. Composite (AND/OR) triggering
  therefore must be modeled as a single trigger object that *contains* subtriggers
  (§5.3) rather than as multiple trigger properties. This is arguably cleaner anyway.
- `PlanPhaseCompletionCondition` is a bare code, not a structured object. Completion
  conditions over world state (area covered, casualty stabilized) need a parallel
  *structured* condition construct; §5.4 adds one and ties it in via a new subclass of
  `PlanPhaseTrigger`/new phase properties rather than redefining the LOX code.
- The absence of task *failure* is a core-vocabulary gap. It can be patched from an
  extension (new `TaskStatusCode` individual), but the subgroup should flag it to the C2SIM
  PDG as a candidate core erratum, since failure semantics benefit all users, not just
  autonomy. Same for a `CancelTask`/`SuspendTask` system of control verbs (§5.7).
- ASX v0.0.1 currently types `Swarm` outside `ActorEntity` (review P7), which would make
  swarms untaskable by any plan construct; the fix already proposed in the review
  (`Swarm` ⊑ `CollectiveEntity`) is a prerequisite for plan semantics to reach swarms.

Because extension is feasible, the "if not, propose a new ontology" branch of the question
does not arise in its strong form. What follows is the proposed **module** — an ontology
fragment in the ASX namespace importing LOX — rather than a freestanding ontology.

---

## 5. Proposed ASX plan-semantics module (sketch)

> The module described in this section is fully drafted as a machine-readable OWL file:
> [`ASX-PlanSemantics-Draft.ttl`](./ASX-PlanSemantics-Draft.ttl) (Turtle, same serialization
> conventions as `CSIM_ASX.rdf`; entities in the `asx#` namespace under a separate module
> ontology IRI importing lox, so it can be merged into the ASX ontology once reviewed).

Design rules observed throughout: UpperCamelCase classes; `hasXxx` properties; enumerations
as `…Code` ⊑ `C2SIM:Code` with `owl:NamedIndividual` members; qualified-cardinality
restrictions; UUID datatype references for cross-links, object properties for containment;
`rdfs:comment` documentation; new file `owl:imports` lox. Every construct is optional on
top of the LOX plan — a plain LOX plan remains valid.

### 5.1 Failure as a first-class outcome

- New `TaskStatusCode` individual **`TASKFAILD`** — "Task was attempted and did not achieve
  its purpose; distinct from TASKABRT (execution stopped by command or exception)."
  *(Candidate core erratum; carried in ASX until adopted.)*
- New class **`asx:PhaseOutcomeCode`** ⊑ `C2SIM:Code`, individuals `PhaseSucceeded`,
  `PhaseFailed`, `PhaseAborted`, `PhaseSkipped` — reportable per phase (§5.6).
- New class **`asx:PhaseFailureCondition`** ⊑ `C2SIM:Code`, individuals `AnyTaskFailed`,
  `AllTasksFailed`, `TimeoutExceeded`, `GuardViolated` — the failure-side dual of
  `lox:PlanPhaseCompletionCondition`.

### 5.2 `asx:AutonomousPlanPhase` ⊑ `lox:PlanPhase`

The workhorse. Adds, all optional:

| Property | Card. | Range | Semantics |
|---|---|---|---|
| `asx:hasPhaseFailureCondition` | max 1 | `PhaseFailureCondition` | when the phase counts as failed |
| `asx:hasOnFailurePhaseReference` | 0..\* | UUID → `PlanPhase` | fallback phase(s) to trigger on failure, in priority order — **BT Fallback/Selector; HTN alternative method; activation semantics for JC3IEDM `ALT`/`HASPRV`** |
| `asx:hasExecutionPolicyCode` | max 1 | `PhaseExecutionPolicyCode` | `SequentialInOrder`, `ParallelAll`, `ParallelAny`, `PriorityFallback` — makes subphase ordering explicit instead of pairwise trigger chains |
| `asx:hasRepetitionPolicyCode` | max 1 | `RepetitionPolicyCode` | `ExecuteOnce`, `RetryOnFailure`, `RepeatUntilCondition`, `MaintainContinuously` — **BT retry/loop decorators; BDI maintenance goals; standing/persistent tasks (N2); MUTT patrol & route-clearance loops** |
| `asx:hasRepetitionLimit` | max 1 | `xsd:nonNegativeInteger` | bound for retry/repeat |
| `asx:hasGuardCondition` | 0..\* | `asx:Condition` | invariant that must hold while the phase runs; violation ⇒ `GuardViolated` — **BT guard/condition node; MUTT "relocate if position compromised", "maintain comms continuously"** |
| `asx:hasPhaseTimeout` | max 1 | `C2SIM:Duration` | timeout decorator |
| `asx:hasRequiredAutonomyLevelCode` | max 1 | autonomy code | graded, phase-dependent level of autonomy (review Q-D: "LoA 1/3/6 varying by mission phase") |
| `asx:hasGoalReference` | max 1 | UUID → `asx:Goal` | what this phase is *for* (§5.5) |

### 5.3 Trigger enrichment (new `lox:PlanPhaseTrigger` subclasses)

- **`asx:StateConditionTrigger`** — exactly 1 `asx:hasCondition` (→ `asx:Condition`).
  Fires when a world-state predicate becomes true, rather than when a discrete Event is
  reported. This is the guard-node primitive.
- **`asx:CompositeTrigger`** — min 2 `asx:hasSubTrigger` (→ `PlanPhaseTrigger`) + exactly 1
  `asx:hasLogicalOperatorCode` (`AND`, `OR`). Works within the exactly-1
  `hasPlanPhaseTrigger` cardinality by containment. Example: CASEVAC transport departs on
  (`EventTrigger`: scout's route-advertisement message) AND (`StateConditionTrigger`:
  casualty loaded).
- **`asx:HumanApprovalTrigger`** — exactly 1 `asx:hasApprovingEntity` (UUID →
  `ActorEntity`), max 1 `asx:hasApprovalTimeout` (`Duration`), max 1
  `asx:hasOnTimeoutPhaseReference` (UUID). The phase starts only when the named authority
  sends approval (a `CommunicativeActTypeCode` = `Agree`/`Confirm` message referencing the
  phase). **This is the on-the-loop engagement-authority gate the review names as the
  central ASX policy gap (W1/Q-K):** a lethal-effect phase in a `FullAuto` mission simply
  carries this trigger, making "may this system engage without a human?" a property of the
  *plan*, machine-checkable against ROE and LoA.

### 5.4 `asx:Condition` — a deliberately small guard vocabulary

`asx:Condition` ⊑ `C2SIM:C2SIMContent`:

| Property | Card. | Range |
|---|---|---|
| `asx:hasConditionSubjectReference` | max 1 | UUID (entity/task/location the predicate is about) |
| `asx:hasConditionPredicateCode` | exactly 1 | `asx:ConditionPredicateCode` |
| `asx:hasConditionParameter` | 0..\* | `xsd:string` (typed per predicate) |
| `asx:hasConditionText` | max 1 | `xsd:string` (human-readable escape hatch, per `lox:hasText` precedent) |

Initial `ConditionPredicateCode` individuals, drawn from the contributed scenarios:
`EntityAtLocation`, `EntityWithinRange`, `EntityHealthBelow`, `ThreatDetectedInArea`,
`HazardOnRoute`, `CommsAvailable`, `CommsDenied`, `AreaCoverageAchieved` (the Q-N
explore-until-covered terminator), `PayloadCapacityAvailable`, `TimeElapsedSince`,
`WeatherLimitExceeded`. Codes-plus-parameters, not a boolean expression language: composite
logic comes only from `CompositeTrigger` AND/OR, keeping conditions machine-checkable and
translator-friendly. If richer logic proves necessary later, a `ConditionExpression`
subclass can be added without disturbing this base — the same open-hierarchy trick used
throughout.

### 5.5 `asx:Goal` — the BDI layer and goal-directed tasking

`asx:Goal` ⊑ `C2SIM:C2SIMContent`:

| Property | Card. | Range | Semantics |
|---|---|---|---|
| `hasUUID` | exactly 1 | UUID | identity |
| `asx:hasAchievementCondition` | min 1 | `asx:Condition` | the end state; goal achieved when true |
| `asx:hasGoalFailureCondition` | 0..\* | `asx:Condition` | goal abandoned when true |
| `asx:hasGoalCommitmentCode` | exactly 1 | `GoalCommitmentCode` | `AchieveOnce`, `Maintain`, `AchieveThenMaintain` |
| `asx:hasGoalPriority` | max 1 | `xsd:nonNegativeInteger` | deconfliction across concurrent goals |
| `hasDesiredEffectCode` | 0..\* | core code | back-link to existing WHY vocabulary |

Plus, on the plan side: **`asx:AutonomousPlanBody`** ⊑ `lox:PlanBody` adding
`asx:hasGoalReference` (max 1) and `asx:hasContextCondition` (0..\*, → `Condition`). The
context condition is the BDI plan-library key: a commander (or planning node) may transmit
*several* `AutonomousPlanBody` instances for the same Goal — primary route plan, degraded-
comms plan, contested plan — each gated by its applicability condition. The executing
system selects among them autonomously; **contingency plans become data, not doctrine
buried in free text.** This also gives `HASPRV`/`ALT` their missing activation semantics at
plan granularity, and directly supports the CASEVAC requirement that replanning "is handled
by autonomy" while remaining inspectable by the on-the-loop operator.

Goal-only tasking (send a `Goal` with constraints and ROE, no plan at all) falls out of the
same construct via the existing `RequestBody`/`OrderBody` machinery and needs no additional
classes — a candidate `AchieveGoal` individual in `TaskActionCode` suffices.

### 5.6 Reporting: intention transparency and explainability

Two new `C2SIM:ReportContent` subclasses (template: SMX `ObservationReportContent`):

- **`asx:PlanExecutionStatusContent`** — exactly 1 `hasPlanPhaseReference`, exactly 1
  `asx:hasPhaseOutcomeCode` (or in-progress), max 1 `asx:hasActiveGoalReference`, max 1
  `asx:hasEstimatedPhaseCompletionTime` (→ CASEVAC "expected time to complete phased
  tasks"). The BDI *intention report*: which plan/phase the system is committed to now.
- **`asx:PlanDeviationReportContent`** — the review's X2/Q-H rationale schema, lifted from
  the Agrawal et al. explainability model already extracted in `LLMExperiments/`:
  exactly 1 `asx:hasTriggeringEventReference` (or Condition), exactly 1
  `asx:hasDeviationTypeCode` (`RouteChanged`, `PhaseAborted`, `FallbackActivated`,
  `GoalAbandoned`, `TaskReassigned`), min 1 `asx:hasRationaleText`, max 1
  `hasConfidenceLevel` (reusing the SMX property). Sent whenever autonomy exercises a
  choice the operator didn't script: fallback activation, context-condition plan switch,
  guard-violation replan.

### 5.7 Execution control verbs

New `TaskActionCode` individuals so the on-the-loop operator can steer without re-issuing
whole orders — adopting the evidence-grounded verb set the review already earmarked
(Q-K): **`ConfigureAutonomy`**, **`SuspendPlanExecution`**, **`ResumePlanExecution`**,
**`OverrideAction`**, **`AbortPlanExecution`** — complementing the existing
`lox:ExecutePlanPhase`. Together with `HumanApprovalTrigger`, these realize the
configure/suspend/acknowledge/override supervision loop, and give X6 (mid-mission
re-tasking) a concrete mechanism: suspend → transmit amended `AutonomousPlanBody`
(functional relation `IMO`, *is a modification of*) → resume.

### 5.8 Coverage of the correlation gaps

| Gap (from §3) | Covered by |
|---|---|
| BT failure status | `TASKFAILD`, `PhaseOutcomeCode`, `PhaseFailureCondition` |
| BT Fallback/Selector | `hasOnFailurePhaseReference`, `PriorityFallback` policy |
| BT condition/guard nodes | `Condition`, `StateConditionTrigger`, `hasGuardCondition` |
| BT decorators (retry/loop/timeout) | `RepetitionPolicyCode`, `hasRepetitionLimit`, `hasPhaseTimeout` |
| BT parallel policies | already in LOX (`AllTasksComplete`/`OneTaskComplete`); made explicit by `PhaseExecutionPolicyCode` |
| BDI goal (achieve/maintain) | `Goal`, `GoalCommitmentCode` |
| BDI plan library + context condition | multiple `AutonomousPlanBody` per Goal + `hasContextCondition` |
| BDI intention reporting | `PlanExecutionStatusContent` |
| Explainability (X2) | `PlanDeviationReportContent` |
| Approval gating / engagement authority (W1/Q-K) | `HumanApprovalTrigger` + `hasRequiredAutonomyLevelCode` |
| Persistent/standing tasks (N2) | `MaintainContinuously`, `Maintain` commitment |
| Coverage-goal termination (Q-N) | `AreaCoverageAchieved` predicate |
| Graded per-phase LoA (Q-D) | `hasRequiredAutonomyLevelCode` on phase |
| Mid-mission re-tasking (X6) | §5.7 control verbs + `IMO` relation |

### 5.9 Worked micro-example (CASEVAC)

Transport UGV's movement phase, as an instance sketch (Turtle, abbreviated):

```turtle
:TransportMovePhase a asx:AutonomousPlanPhase ;
    C2SIM:hasTaskReference "UUID-move-to-casualty" ;
    lox:hasPlanPhaseTrigger [
        a asx:CompositeTrigger ;
        asx:hasLogicalOperatorCode asx:AND ;
        asx:hasSubTrigger [ a lox:EventTrigger ;
            lox:hasEvent :ScoutRouteAdvertisedEvent ] ;
        asx:hasSubTrigger [ a asx:StateConditionTrigger ;
            asx:hasCondition [ a asx:Condition ;
                asx:hasConditionPredicateCode asx:CommsAvailable ] ] ] ;
    lox:hasPlanPhaseCompletionCondition lox:AllTasksComplete ;
    asx:hasPhaseFailureCondition asx:GuardViolated ;
    asx:hasGuardCondition [ a asx:Condition ;
        asx:hasConditionPredicateCode asx:HazardOnRoute ;
        asx:hasConditionText "No IED/obstacle report on active route" ] ;
    asx:hasOnFailurePhaseReference "UUID-replan-route-phase" ;
    asx:hasGoalReference "UUID-goal-casualty-at-CCP" .
```

Every element a legacy LOX consumer does not understand is an optional addition to a valid
`PlanPhase`; every element an ASX consumer understands maps to a specific BT/BDI mechanism.

---

## 6. Recommendations

1. **Adopt the plan-extension route** (module in the ASX namespace importing LOX) rather
   than a freestanding behavior ontology. It reuses proven machinery, degrades gracefully
   for legacy consumers, and matches the standards-survey recommendation to model BT/HTN
   concepts directly with IEEE 1872.1/1872.2 alignment.
2. **Raise two candidate core errata with the PDG:** a `TASKFAILD` task status, and
   plan-execution control verbs — both broadly useful beyond autonomy.
3. **Sequence the work** along the subgroup's decision log: `Condition` + trigger
   subclasses first (unlocks Q-D, Q-N, G10), then `HumanApprovalTrigger` + LoA linkage
   (W1/Q-K — the flagged central gap), then `Goal`/plan-library (Q-N, goal-directed
   tasking), then the two report contents (X2, X6).
4. **Prerequisites from the existing review:** re-type `Swarm` under `CollectiveEntity`
   (P7) and give `hasAutonomousRoleCode` an attachment point (P3), or the plan semantics
   cannot reach the platforms they are meant to task.
5. **Validate against the contributed scenarios**: instantiate the full CASEVAC and one
   MUTT scenario (security patrol, for its assess-then-branch structure) in the sketch
   vocabulary, and walk them in the instantiation-review format before drafting OWL.
