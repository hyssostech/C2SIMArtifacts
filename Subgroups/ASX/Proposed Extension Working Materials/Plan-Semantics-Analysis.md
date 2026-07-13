# C2SIM Plan Constructs and Autonomous-System Behavior Semantics

**Correlation with behavior trees and BDI, feasibility of extension, and a proposed ASX plan-semantics module**

*Status: working analysis for the ASX subgroup — not an adopted proposal. This revision
incorporates the results of an adversarial review pass (ontology-consistency check against
core/SMX/LOX, fact-check against the repository artifacts, and a conceptual review of the
BT/BDI mappings); §7 records what the module deliberately does not cover.*

*Verification cross-reference (2026-07-12): an independently produced
standards-matrix pass (`./PlanSemantics-Walk.md`,
sections 3 and 8) verified this document's C2SIM-side claims against the
RDF and mapped the module against JAUS AS6062, STANAG 4586, IEEE
1872.1-2024, MAVLink, FlexBE, and 4D/RCS. It corroborates the construct
choices (independent derivation converged on the same set), lists v-next
deltas (plan identifier, Suspended outcome, task-targeted acks, waypoint
schema, failsafe/geofence binding), and corrects one alignment target:
IEEE 1872.2 verifiably defines no Plan/Goal/Mission constructs - align to
IEEE 1872.1-2024 only.*

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
   additive **plan-semantics module** in the ASX layer. Feasibility comes with one honest
   qualification (§4): *gating* constructs are mandatory-to-understand and require
   capability negotiation — only *reporting* constructs degrade gracefully for free.
3. The main semantic deficits relative to BT/BDI are precisely enumerable: no failure
   status, no fallback/alternative branching, no state-predicate guards, no loop/persistence
   semantics, no goal (end-state) object distinct from procedure, no plan-selection context
   conditions, and no intention/rationale reporting. Section 5 proposes constructs for each,
   in the standard's own style; §7 lists the gaps that remain open by design.

Sources examined: `Ontology/C2SIM.rdf` (core, CWIX2025 build of SISO C2SIM 1.0.1),
`Ontology/C2SIM_SMX.rdf`, `Ontology/C2SIM_LOX.rdf`,
`Subgroups/ASX/Proposed Extension/CSIM_ASX.rdf` (v0.0.1), the ASX instantiation-review
walk documents and decision log, the contributed CASEVAC and MUTT scenarios, the sourced
scenario extractions in `LLMExperiments/PaperSummaries/V2Extractions/`, and
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
  18-member Allen-style code list (`ActionTemporalAssociationCode`): `STREND` (starts after
  end of — plain sequencing), `STRSTR`, `ENDEND`, `ENDSTR`, concurrency codes, and
  duration-augmented variants (`STRENE`, `STRENL`, …).
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
- `RequestBody` vs `OrderBody` already distinguishes deontic force (a request "is fulfilled
  at the discretion of the entity to which it is directed", while an order "is expected to
  be obeyed if it is physically possible to do so"), relevant to robot-to-robot
  coordination (review item X1/Q-G).

### 2.2 LOX: the Plan construct

The plan machinery lives entirely in the Land Operations Extension
(`Ontology/C2SIM_LOX.rdf`):

| Construct | Structure |
|---|---|
| `lox:PlanBody` ⊑ `C2SIM:DomainMessageBody` | `hasPlanPhase` 0..\*, `hasPlanPhaseReference` 0..\* (UUID), `isToBeExecutedNow` exactly 1 |
| `lox:PlanPhase` ⊑ `C2SIM:C2SIMContent` | `hasSubPhase` 0..\* (**recursive**), `hasPlanPhaseTrigger` **exactly 1**, `hasPlanPhaseCompletionCondition` **exactly 1**, `C2SIM:hasTaskReference` 0..\* |
| `lox:PlanPhaseTrigger` (superclass, three subclasses) | `EventTrigger` (exactly 1 `hasEvent`), `OnOrderTrigger` (exactly 1 `hasTaskReference`, typically a task with `TaskActionCode` = `lox:ExecutePlanPhase`), `PriorPhaseCompletionTrigger` (exactly 1 `hasTriggerPhase` UUID) |
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
delegation, or contingencies. The subgroup's instantiation review reaches the same
conclusion: its decision log leaves open, among others, the
autonomy-level-to-engagement-authority linkage (W1/Q-K — the one item the log itself flags
as "the central ASX policy gap"), rationale/explainability reporting (X2/Q-H), mid-mission
re-tasking semantics (X6), coverage/termination goal semantics (Q-N), a normative graded
autonomy vocabulary (Q-D), and persistent/standing tasking (N2, a low-severity nuance the
log folds into Q-L). This analysis is intended to serve exactly that roadmap.

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
| Sequence node | subphase chain via `PriorPhaseCompletionTrigger` | structural only — with a single "complete" outcome the chain works, but the moment failure exists the semantics must be restated (a BT Sequence *halts and reports failure*; an unmodified trigger chain would simply stall). §5's rules R2/R3 supply the restatement |
| Parallel node, success-on-all policy | phase with several tasks + `AllTasksComplete` | good, but with no cancellation rule for stragglers (rule R5 supplies one) |
| Parallel node, success-on-one policy | phase + `OneTaskComplete` | same caveat |
| Leaf action node | `Task` referenced from a phase | good |
| Entry gating on an occurrence | `EventTrigger` | partial — LOX defines it as anchored to *the time of an event*, a temporal anchor rather than a runtime detection mechanism, and no report type is defined for announcing "event X occurred" at runtime. Runtime reactivity needs the state-condition trigger of §5.3 |
| External preemption | `OtherOrderReceived` completion; `OnOrderTrigger` | partial — human-initiated only |
| **Failure status** | — | **absent**: phases and tasks complete or abort; nothing fails |
| **Fallback / Selector node** | — | **absent**: `ALT`/`HASPRV` codes name alternatives but nothing activates them |
| **Condition (leaf) node** | — | **absent**: no predicate language over entities/locations/health/comms |
| **Decorators: retry, loop, timeout** | — | **absent**: no repetition or persistence semantics; the MUTT route-clearance loop (continue along the route, repeating detection and neutralization) is not expressible |
| Running status / tick | `TASKINPRG` reports | adequate — see §3.4 on what should *not* be imported |
| Priority/reactive re-evaluation | — | absent: triggers are evaluated as one-shot start conditions, not continuously re-evaluated guards. **The proposed module does not close this gap either** (§7) |

The structural conclusion: **the trigger/completion-condition pattern is the right chassis.**
A BT's control-flow node types differ from `PlanPhase` mainly in (a) having a failure
outcome and a policy for reacting to it, and (b) allowing guards over state, not just
events. Both are additive — but the additions only mean something once the *execution
semantics* over the enriched outcome set are stated normatively; OWL restrictions alone
cannot do that, which is why §5 pairs the vocabulary with explicit rules (R1–R14).

### 3.2 BDI

BDI separates **beliefs** (world model), **desires/goals** (end states, possibly
maintained), and **intentions** (goals the agent has committed to, realized by selecting
plans from a *plan library*, where each plan has a triggering event, a *context condition*
gating applicability, and a body). Mapping against C2SIM:

| BDI concept | C2SIM analog | Fidelity |
|---|---|---|
| Beliefs | `ReportBody`/`ObservationReportContent` (SMX), position/health reports | partial — C2SIM exchanges belief *updates*; adequate as-is, since the belief store itself belongs to the executing system |
| Desire / goal | `hasDesiredEffectCode` on Task | weak — a code annotation on a *procedure*, not a first-class end state; nothing states the conditions under which the goal counts as achieved or failed |
| Achievement vs maintenance goals | — | absent — no standing "maintain comms / keep station" semantics (review item N2) |
| Plan (recipe) | `PlanBody`/`PlanPhase` | good — this is exactly a plan body |
| Plan library + context condition | — | absent — one plan per message; no way to send several alternative plans for one goal with applicability conditions |
| Triggering event of a plan | `EventTrigger`/`OnOrderTrigger` | good |
| Intention / commitment state | — | absent — no way for a subordinate to report *which* plan it has adopted, what it is pursuing, or why it deviated (review items X2, X6) |
| Communication performatives | `CommunicativeActTypeCode` (FIPA-style) | good — already present in core |
| Delegation of authority | Order vs Request deontic split | partial — no construct for whether a robot may itself issue orders, nor for approval gates as a function of autonomy level (W1/Q-K, Q-P) |

What §5 proposes should be read as a **plan *pre-selection* library**, not a full BDI
implementation: a commander transmits alternative plans with applicability conditions and
the executing system selects among them. Runtime *subgoaling* (a plan step posting a new
goal resolved against the library recursively) and the agent's *reconsideration strategy*
(when to re-deliberate about commitments) are deliberately not modeled — they are agent
internals, and §7 lists them as such.

The BDI correlation exposes the *tasking philosophy* gap: C2SIM orders are procedural
(do these tasks), whereas autonomy increasingly requires **goal-directed tasking** (achieve
this end state under these constraints, choose your own procedure). Notably, C2SIM's own
Task comment already gestures at this ("WHY may be represented by hasDesiredEffect") — the
extension direction is consistent with the standard's intent, not a departure from it.

### 3.3 HTN, briefly

`hasSubPhase` recursion is exactly HTN-style decomposition of an abstract phase into
subtasks; what HTN adds is *methods* — multiple alternative decompositions with
preconditions. That is the same missing piece as the BT Fallback node and the BDI plan
library: **alternatives + the conditions that select among them.** One construct family
(§5.3–§5.5) covers all three formalisms. The Remmersmann et al. (2015) MUM-T pattern
already summarized in `LLMExperiments/` — high-level order, machine decomposition,
threshold-triggered reassignment, report aggregation — shares the decomposition direction,
though its *reassignment* and *aggregation* halves remain future work (§7).

### 3.4 What should *not* be imported

An interoperability standard should exchange the *structure and intent* of behavior, not
its execution engine. Tick frequency, blackboard mechanics, node memory
(reactive vs. memory-sequence), and BDI deliberation cycles are properties of the executing
system and would over-constrain implementations while adding nothing to interoperability.
The subgroup's standards survey recommends modeling "the BT concepts (composite/decorator/
leaf nodes, tick semantics, success/running/failure states) rather than cite a standard,"
with IEEE 1872.1/1872.2 as backbone and FIPA/BDI for the goal/intention layer. This
proposal follows that recommendation with one deliberate departure: of the listed concepts,
tick *mechanics* are excluded as engine-internal; what the module carries instead is the
observable consequence of ticking — the success/running/failure state model and its
propagation rules. Likewise, a general-purpose logical expression language is avoided:
C2SIM's style is closed code lists with an escape hatch, and §5.4 follows it.

---

## 4. Feasibility of extending the plan construct

**Verdict: feasible, additively, in the ASX layer — no changes to core or LOX required,
and no separate standalone ontology needed.** The assessment rests on the standard's own
extension idioms, all verified in the existing artifacts:

1. **Open trigger hierarchy.** `PlanPhaseTrigger` has three subclasses and nothing prevents
   more (`StateConditionTrigger`, `HumanApprovalTrigger`, `CompositeTrigger`,
   `OnPhaseFailureTrigger`). This is the same pattern LOX itself used.
2. **Open code lists.** Extensions already populate core code classes with new individuals
   (SMX adds 25 `DesiredEffectCode`s; LOX adds 446 `TaskActionCode`s). Adding e.g.
   `TASKFAILD` to `TaskStatusCode` follows precedent exactly.
3. **Subclass-and-restrict.** LOX's `ManeuverWarfareTask` ⊑ `C2SIM:Task` shows the
   sanctioned way to enrich an existing concept: subclass it and add qualified-cardinality
   restrictions over new properties. An `asx:AutonomousPlanPhase` ⊑ `lox:PlanPhase`
   inherits all existing machinery and adds failure handling, guards, and policies.
4. **New message content by subclassing `ReportContent`.** SMX's
   `ObservationReportContent` is the template for the rationale/intention reports in §5.6.
5. **UUID-reference style.** All new cross-references (fallback phase, goal reference,
   approving entity) use datatype properties over `C2SIM:UUIDBase`, per the core
   `hasReference` subproperty tree.

**The interoperability qualification.** An earlier draft of this analysis claimed graceful
degradation "comes free" because legacy consumers can process an `AutonomousPlanPhase` as a
plain `PlanPhase`. The adversarial review showed that claim is only half true, and the half
matters:

- *Additive reporting constructs* (status/deviation report contents, new code individuals)
  do degrade gracefully — a consumer that ignores them loses information, not safety.
- *Gating and restricting constructs* do **not**: every new phase property is a
  restriction (guard, timeout, failure handling, required autonomy level), so ignoring them
  executes the phase *without its safety envelope*. Worse, a legacy consumer confronting an
  unknown trigger subclass in the mandatory `hasPlanPhaseTrigger` slot might plausibly
  default to "start when reached" — which, for a phase gated by `HumanApprovalTrigger`,
  means firing without the human gate: fail-open on precisely the construct that exists to
  prevent it. And multiple plan-library variants would read to a legacy consumer as
  multiple orders to execute (LOX defines `PlanBody` as ordering execution).

The module therefore states (normative rules R13–R14 in the TTL): unknown triggers are
**fail-closed** — a consumer that cannot interpret a phase's trigger must treat the phase
as not triggerable and report the inability; plans using gating constructs should only be
sent to consumers that negotiated the module at initialization; and plan-library variants
must carry `isToBeExecutedNow = false`. With those rules, the feasibility verdict stands.

Other frictions found, none blocking:

- `hasPlanPhaseTrigger` is **exactly 1** on `PlanPhase`. Composite (AND/OR) triggering is
  modeled as a single trigger object *containing* subtriggers (§5.3). The same constraint
  means every phase referenced as a fallback target needs a trigger that fires *only* on
  the failure path — hence `OnPhaseFailureTrigger`, the failure-side dual of LOX's
  `PriorPhaseCompletionTrigger` — and every policy-managed subphase needs
  `ParentPhasePolicyTrigger` (§5.3).
- `PlanPhaseCompletionCondition` is a bare code, not a structured object. Completion
  conditions over world state (area covered, casualty stabilized) are carried by the new
  structured `Condition` (§5.4) in dedicated roles (loop termination, goal achievement)
  rather than by redefining the LOX code.
- The absence of task *failure* is a core-vocabulary gap. It can be patched from an
  extension (new `TaskStatusCode` individual), but the subgroup should flag it to the C2SIM
  PDG as a candidate core erratum, since failure semantics benefit all users, not just
  autonomy. Same for task cancellation/suspension control verbs (§5.7) — rule R5's
  abort-stragglers semantics depends on them.
- ASX v0.0.1 currently types `Swarm` outside `ActorEntity` (review P7), which would make
  swarms untaskable by any plan construct; the fix already proposed in the review
  (`Swarm` ⊑ `CollectiveEntity`) is a prerequisite for plan semantics to reach swarms.

Because extension is feasible, the "if not, propose a new ontology" branch of the question
does not arise in its strong form. What follows is the proposed **module** — an ontology
fragment in the ASX namespace importing LOX — rather than a freestanding ontology.

---

## 5. Proposed ASX plan-semantics module

> The module is fully drafted as a machine-readable OWL file:
> [`ASX-PlanSemantics-Draft.ttl`](./ASX-PlanSemantics-Draft.ttl) (Turtle, same serialization
> conventions as `CSIM_ASX.rdf`; entities in the `asx#` namespace under a separate module
> ontology IRI importing lox, so it can be merged into the ASX ontology once reviewed).
> Because OWL cannot express execution semantics, the module's header carries **nineteen
> normative rules (R1-R19)** - outcome propagation, sequencing over failure, composite-AND
> latching, completion/failure precedence, fallback resolution, one-shot triggers,
> fail-closed interoperability, plan-library transmission, and (v0.0.3) late-bound
> products, plan identity/supersession, suspension, lost-link precedence, and waypoint
> traversal - that entity comments reference throughout. The vocabulary and the rules together are the proposal; the
> vocabulary alone would be ambiguous in exactly the ways an adversarial review found.

Design rules observed throughout: UpperCamelCase classes; `hasXxx` properties; enumerations
as `…Code` ⊑ `C2SIM:Code` with `owl:NamedIndividual` members; qualified-cardinality
restrictions; UUID datatype references for cross-links, object properties for containment;
`rdfs:comment` documentation on every entity; new file `owl:imports` lox. Every construct
is optional on top of the LOX plan — a plain LOX plan remains valid.

### 5.1 Failure as a first-class outcome

- New `TaskStatusCode` individual **`TASKFAILD`** — "attempted and did not achieve its
  purpose," distinct from `TASKABRT` (stopped by command or exception). *(Candidate core
  erratum; carried in ASX until adopted.)*
- **`asx:PhaseOutcomeCode`** ⊑ `C2SIM:Code`: `PhasePending`, `PhaseInProgress` (states) and
  `PhaseSucceeded`, `PhaseFailed`, `PhaseAborted`, `PhaseSkipped` (terminal outcomes, R1).
- **`asx:PhaseFailureCondition`** ⊑ `C2SIM:Code`, with two distinct roles the rules keep
  apart: the *selectable aggregation policies* `AnyTaskFailed` (default) and
  `AllTasksFailed` (R3), and the *implicit failure modes* `TimeoutExceeded` and
  `GuardViolated`, which are live automatically whenever a timeout or guard is declared
  (R4) and appear in reports as failure causes — so a declared timeout is never decorative,
  and task failure, timeout, and guard violation are simultaneously live, as in a BT.
- Precedence is defined (R6): conditions are evaluated against event times, not report
  arrival, and failure beats completion when both are satisfiable — so the vehicle, the C2
  node, and the log cannot legitimately disagree about a phase's terminal outcome.

### 5.2 `asx:AutonomousPlanPhase` ⊑ `lox:PlanPhase`

The workhorse. Adds, all optional:

| Property | Card. | Range | Semantics |
|---|---|---|---|
| `asx:hasPhaseFailureCondition` | max 1 | `PhaseFailureCondition` | member-aggregation failure policy (R3) |
| `asx:hasOnFailurePhaseReference` | max 1 | UUID → `PlanPhase` | fallback phase on failure — **BT Fallback; HTN alternative method; activation semantics for JC3IEDM `ALT`/`HASPRV`**. Chains (fallback-of-fallback) express further alternatives; must be acyclic; the target's trigger must be an `OnPhaseFailureTrigger` naming this phase (R7); a fallback chain that ultimately succeeds counts as success toward the parent (R7) |
| `asx:hasExecutionPolicyCode` | max 1 | `PhaseExecutionPolicyCode` | `SequentialInOrder`, `ParallelAll`, `ParallelAny`, `PriorityFallback` — explicit subphase control flow; ordering via `hasPhasePriority` (RDF is unordered) |
| `asx:hasRepetitionPolicyCode` | max 1 | `RepetitionPolicyCode` | `ExecuteOnce`, `RetryOnFailure`, `RepeatUntilCondition`, `MaintainContinuously` — **BT retry/loop decorators; BDI maintenance behavior; standing tasks (N2); MUTT patrol & route-clearance loops** |
| `asx:hasRepetitionUntilCondition` | max 1 | `Condition` | loop-termination condition: the LOX completion code closes each *iteration*, this closes the *loop* (e.g. route-clear) |
| `asx:hasRepetitionLimit` | max 1 | `xsd:nonNegativeInteger` | bound for retry/repeat; `PhaseFailed` is terminal only when exhausted (R10) |
| `asx:hasGuardCondition` | 0..\* | `Condition` | conjunctive invariants (R12); violation fails the phase at once (R4) — MUTT's *maintain communication continuously* and *relocate if the position becomes compromised* |
| `asx:hasPhaseTimeout` | max 1 | `Duration` | timeout decorator (implicitly live, R4) |
| `asx:hasRequiredAutonomyLevelCode` | max 1 | `AutonomyLevelCode` | graded, phase-dependent autonomy — the sourcing analysis (`OntologyConceptCoverage.md`) found scenarios using "graded LoA … that varies by mission phase," which sharpened review item Q-D |
| `asx:hasPhasePriority` | max 1 | `xsd:nonNegativeInteger` | explicit ordering under `SequentialInOrder`/`PriorityFallback` |
| `asx:hasPhaseProductReference` | 0..\* | UUID | data product(s) the phase publishes for other entities' consumption — the CASEVAC scout's advertised safe route, at reference level |
| `asx:hasGoalReference` | max 1 | UUID → `asx:Goal` | what this phase is *for* (§5.5) |

### 5.3 Trigger enrichment (new `lox:PlanPhaseTrigger` subclasses)

- **`asx:StateConditionTrigger`** — exactly 1 `asx:hasCondition`. Fires when a world-state
  predicate evaluates true — level-triggered, against the executing system's own world
  model (R11). This, not `EventTrigger`, is the module's runtime-reactivity primitive.
- **`asx:CompositeTrigger`** — min 2 `asx:hasSubTrigger` + exactly 1 operator
  (`AllSubTriggers`, `AnySubTrigger`; renamed from AND/OR to avoid colliding with core's
  country code `AND` and to leave room for a future k-of-n operator). The AND semantics are
  latch-for-discrete, hold-now-for-state (R9) — so "depart when the route is advertised AND
  comms are up" cannot fire during a comms outage just because comms were up earlier.
  Negation lives on `Condition` (`isNegated`), not in the operator list.
- **`asx:HumanApprovalTrigger`** — exactly 1 `asx:hasApprovingEntity`, max 1
  `asx:hasApprovalTimeout`, max 1 `asx:hasOnTimeoutPhaseReference`. Approval is an
  `Agree`/`Confirm` message from the named authority referencing the gated phase; a
  `Refuse` (or timeout) immediately applies the timeout disposition — activate the timeout
  phase if given, else skip (and a skipped phase satisfies downstream sequencing triggers,
  R2, so refusal cannot silently stall the rest of the plan). **This is the on-the-loop
  engagement-authority gate the review log calls the central ASX policy gap (W1/Q-K):** a
  lethal-effect phase in a `FullAuto` mission carries this trigger, making "may this system
  engage without a human?" an inspectable property of the *plan*. Fail-closed rule R13
  applies with full force here.
- **`asx:OnPhaseFailureTrigger`** — exactly 1 `lox:hasTriggerPhase`. Fires when the
  referenced phase fails; the failure-side dual of `PriorPhaseCompletionTrigger`, and the
  sanctioned trigger for fallback targets — without it, a fallback phase's mandatory
  trigger slot could only hold a trigger that fires independently of the failure path.
- **`asx:ParentPhasePolicyTrigger`** — no properties; fills the mandatory trigger slot of
  subphases whose activation is wholly controlled by the parent's execution policy,
  eliminating the ambiguity of policy-vs-trigger conflicts (the policy is normative).

### 5.4 `asx:Condition` — a deliberately small guard vocabulary

`asx:Condition` ⊑ `C2SIM:C2SIMContent`, with **typed** parameters (the adversarial review
killed an earlier design using ordered untyped strings — RDF preserves no order, and
untyped values defeat validation):

| Property | Card. | Range |
|---|---|---|
| `asx:hasConditionPredicateCode` | exactly 1 | `ConditionPredicateCode` |
| `asx:isNegated` | max 1 | `xsd:boolean` (default false) — guard polarity and else-branches |
| `asx:hasConditionSubjectReference` | max 1 | UUID (what the predicate is about) |
| `asx:hasConditionObjectReference` | max 1 | UUID (second participant of binary predicates) |
| `asx:hasThresholdValue` | max 1 | `xsd:double` (units defined per predicate) |
| `asx:hasThresholdDuration` | max 1 | `Duration` |
| `C2SIM:hasUUID` | max 1 | UUID — so reports can cite *which* condition fired/was violated |
| `asx:hasConditionText` | max 1 | `xsd:string` (display/escape hatch; never machine-evaluated) |

Initial `ConditionPredicateCode` individuals, drawn from the contributed and sourced
scenarios: `EntityAtLocation`, `EntityWithinRange`, `EntityHealthBelow`,
`ThreatDetectedInArea`, `HazardOnRoute`, `CommsAvailable`, `CommsDenied`,
`AreaCoverageAchieved` (the Q-N explore-until-covered terminator),
`EstimateConfidenceAbove` (belief-state gating: switch-to-tracking on detection confidence,
repeat-measurement until a geolocation confidence ellipse converges — from the
DroneResponse and EW-geolocation extractions), `PayloadCapacityAvailable`,
`TimeElapsedSince`, `WeatherLimitExceeded`. Codes-plus-typed-parameters, not a boolean
expression language: repeated conditions are conjunctive (R12), disjunction comes from
`CompositeTrigger`, negation from `isNegated`. If richer logic proves necessary later, a
`ConditionExpression` subclass can be added without disturbing this base.

### 5.5 `asx:Goal` — the BDI layer and goal-directed tasking

`asx:Goal` ⊑ `C2SIM:C2SIMContent`:

| Property | Card. | Range | Semantics |
|---|---|---|---|
| `hasUUID` | exactly 1 | UUID | identity |
| `asx:hasAchievementCondition` | min 1 | `Condition` | the end state (conjunctive, R12) |
| `asx:hasGoalFailureCondition` | 0..\* | `Condition` | goal abandoned when true |
| `asx:hasGoalCommitmentCode` | exactly 1 | `GoalCommitmentCode` | `AchieveOnce`, `Maintain`, `AchieveThenMaintain` |
| `asx:hasGoalPriority` | max 1 | `xsd:nonNegativeInteger` | deconfliction across concurrent goals |
| `hasDesiredEffectCode` | 0..\* | core code | back-link to existing WHY vocabulary |

On the plan side, **`asx:AutonomousPlanBody`** ⊑ `lox:PlanBody` adds **`asx:hasGoal`**
(0..\*, object property — the containment slot without which a Goal could never go on the
wire), `asx:hasGoalReference` (max 1) and `asx:hasContextCondition` (0..\*). The context
condition is the plan-library key: a commander (or planning node) transmits *several*
`AutonomousPlanBody` instances for the same Goal — primary route plan, degraded-comms
plan, contested plan — each gated by its applicability condition, each with
`isToBeExecutedNow = false` and only to module-aware consumers (R14). Context conditions
are re-evaluated during execution; switching is reported as a `PlanSwitched` deviation.
Contingency plans become data, not doctrine buried in free text; `HASPRV`/`ALT` gain their
missing activation semantics at plan granularity; and the CASEVAC requirement that
replanning "is handled by autonomy" stays inspectable by the on-the-loop operator.

Goal-only tasking (send a `Goal` with constraints and ROE, no plan at all) falls out of the
same construct via the existing `RequestBody`/`OrderBody` machinery — the new `AchieveGoal`
individual in `TaskActionCode` suffices.

### 5.6 Reporting: intention transparency and explainability

Two new `C2SIM:ReportContent` subclasses (template: SMX `ObservationReportContent`) —
both purely additive, so they degrade gracefully:

- **`asx:PlanExecutionStatusContent`** — exactly 1 `hasPlanPhaseReference`, exactly 1
  `asx:hasPhaseOutcomeCode`, max 1 `asx:hasPhaseFailureCauseCode` (aggregation policy met,
  timeout, or guard violation), max 1 `asx:hasAttemptNumber` (so an operator watching a
  retrying phase is not misled into firing contingencies early — R10), max 1
  `asx:hasActiveGoalReference` (the reporting system's active intention), max 1
  `asx:hasEstimatedPhaseCompletionTime` (the CASEVAC "expected time to complete phased
  tasks" requirement).
- **`asx:PlanDeviationReportContent`** — the review's X2/Q-H rationale schema, adapted from
  the DroneResponse explainability model already extracted in `LLMExperiments/`
  (`Explainability_Agrawal2021.md`: event, action, reasoning, operational change,
  confidence): exactly 1 `asx:hasDeviationTypeCode` (`RouteChanged`, `FallbackActivated`,
  `PlanSwitched`, `GoalAbandoned`, `TaskReassigned`), max 1 triggering event reference *or*
  deviation condition, max 1 affected phase reference, exactly 1 `asx:hasRationaleText`,
  max 1 `smx:hasConfidenceLevel`. Sent whenever autonomy exercises a choice the operator
  didn't script.

### 5.7 Execution control verbs

New `TaskActionCode` individuals so the on-the-loop operator can steer without re-issuing
whole orders — adapting the evidence-grounded verb set the review earmarked under Q-K
(configure / suspend / acknowledge / override, from the DroneResponse study):
**`ConfigureAutonomy`**, **`SuspendPlanExecution`**, **`ResumePlanExecution`**,
**`OverrideAction`**, **`AbortPlanExecution`** — plus **`AchieveGoal`** (§5.5). The
*acknowledge* act needs no new verb: it is already carried by `AcknowledgementBody` and the
`CommunicativeActTypeCode` performatives; *resume* and *abort* are additions the scenario
corpus demands (MDARS resume-after-intervention; CBRN abort-after-three-attempts). Together
with `HumanApprovalTrigger`, these realize the supervision loop, and give X6 (mid-mission
re-tasking) a concrete mechanism: suspend → transmit amended `AutonomousPlanBody`
(functional relation `IMO`, *is a modification of*) → resume.

### 5.8 Coverage of the correlation gaps

| Gap (from §3) | Covered by |
|---|---|
| BT failure status | `TASKFAILD`, `PhaseOutcomeCode`, failure policies + causes (R3/R4) |
| BT Sequence over failure | `SequentialInOrder` + `AnyTaskFailed` + rules R2/R3/R5 |
| BT Fallback/Selector | `hasOnFailurePhaseReference` + `OnPhaseFailureTrigger` (peer level, R7); `PriorityFallback` policy (containment level, R8) |
| BT condition/guard nodes | `Condition` (typed, negatable), `StateConditionTrigger`, `hasGuardCondition` |
| BT decorators (retry/loop/timeout) | `RepetitionPolicyCode`, `hasRepetitionUntilCondition`, `hasRepetitionLimit`, `hasPhaseTimeout` |
| BT parallel policies | LOX codes + `ParallelAll`/`ParallelAny` with straggler-abort (R5) |
| BDI goal (achieve/maintain) | `Goal`, `GoalCommitmentCode`, `hasGoal` containment |
| BDI plan pre-selection + context condition | multiple `AutonomousPlanBody` per Goal + `hasContextCondition` (R14) |
| BDI intention reporting | `PlanExecutionStatusContent` |
| Explainability (X2) | `PlanDeviationReportContent` |
| Approval gating / engagement authority (W1/Q-K) | `HumanApprovalTrigger` + `hasRequiredAutonomyLevelCode` + fail-closed R13 |
| Persistent/standing tasks (N2) | `MaintainContinuously`, `Maintain` commitment |
| Coverage-goal termination (Q-N) | `AreaCoverageAchieved` predicate |
| Graded per-phase LoA (Q-D) | `hasRequiredAutonomyLevelCode` on phase |
| Mid-mission re-tasking (X6) | §5.7 control verbs + `IMO` relation |
| Producer/consumer handoff (CASEVAC route, X1-adjacent) | `hasPhaseProductReference` (reference level only) |

**Explicitly *not* covered by this version** (see §7 for the full list with scenario
evidence): reactive cross-phase preemption and trigger re-arming; commanded task
*re-allocation* and capability-based assignment; report aggregation across disaggregated
plans; subgoaling and agent reconsideration strategies; quantitative formation envelopes;
resource-economy/rate conditions.

### 5.9 Worked micro-example (CASEVAC)

Transport UGV's movement phase, as an instance sketch (Turtle, abbreviated):

```turtle
:TransportMovePhase a asx:AutonomousPlanPhase ;
    C2SIM:hasTaskReference "UUID-move-to-casualty" ;
    lox:hasPlanPhaseTrigger [
        a asx:CompositeTrigger ;
        asx:hasLogicalOperatorCode asx:AllSubTriggers ;   # comms must HOLD at departure (R9)
        asx:hasSubTrigger [ a lox:EventTrigger ;
            lox:hasEvent :ScoutRouteAdvertisedEvent ] ;
        asx:hasSubTrigger [ a asx:StateConditionTrigger ;
            asx:hasCondition [ a asx:Condition ;
                asx:hasConditionPredicateCode asx:CommsAvailable ] ] ] ;
    lox:hasPlanPhaseCompletionCondition lox:AllTasksComplete ;
    asx:hasGuardCondition [ a asx:Condition ;
        C2SIM:hasUUID "UUID-guard-route-clear" ;
        asx:hasConditionPredicateCode asx:HazardOnRoute ;
        asx:isNegated true ;                              # invariant: NO hazard on route
        asx:hasConditionText "Active route free of IED/obstacle reports" ] ;
    asx:hasOnFailurePhaseReference "UUID-replan-route-phase" ;
    asx:hasGoalReference "UUID-goal-casualty-at-CCP" .

:ReplanRoutePhase a asx:AutonomousPlanPhase ;             # the fallback target
    C2SIM:hasUUID "UUID-replan-route-phase" ;
    lox:hasPlanPhaseTrigger [
        a asx:OnPhaseFailureTrigger ;                     # fires ONLY on the failure path (R7)
        lox:hasTriggerPhase "UUID-transport-move-phase" ] ;
    lox:hasPlanPhaseCompletionCondition lox:AllTasksComplete ;
    asx:hasGoalReference "UUID-goal-casualty-at-CCP" .
```

Note the corrections the adversarial review forced on this very example: the guard's
polarity (an earlier draft's guard was accidentally inverted — the exact silent error the
module exists to eliminate, fixed by `isNegated`); the AND semantics annotation; and the
fallback target with its `OnPhaseFailureTrigger`, without which it either could never be
validly expressed or could fire independently of the failure. If the replan phase succeeds,
the transport phase counts as succeeded for its parent (R7) — the mission proceeds.

### 5.10 v0.0.3 additions (validation-walk deltas + standards-matrix deltas)

Version 0.0.3 of the TTL applies two evidence streams onto the v0.0.2 base -
the nine deltas the validation walks demanded, and the deltas from the
independent standards-verification pass
(`./PlanSemantics-Walk.md`, section 8). Rules R15-R19
carry the added execution semantics.

**From the validation walks (PlanSemanticsWalks/):**

- Deviation vocabulary rescoped: `BehaviorAdjusted` (operating-parameter
  change) and `ExceptionRaised` (plan-anticipated exception entered its
  scripted handling) added to `DeviationTypeCode` - decision recorded: one
  explainability channel, not a sibling alert report type.
- `hasRepetitionInterval` (max 1, Duration) on `AutonomousPlanPhase`: revisit
  cadence for `RepeatUntilCondition`/`MaintainContinuously` (MDARS revisit,
  MCM repeat-on-cadence); pauses under suspension (R17).
- Predicates: `PayloadOnBoard` (embarkation state - "casualty loaded"),
  `RemainingEnduranceBelow` (battery/fuel depletion, distinct from damage;
  bingo-energy uses), `EntityImmobilized` (mobility state - "trapped").
- R15 states the late-bound product convention normatively (pre-allocated
  UUIDs bound by the producer at publication).
- `hasActionTakenReference` (max 1) on the deviation report names the task or
  phase activated in response.
- The EntityType-filter semantics of `hasConditionObjectReference` are now
  stated on the property.
- The request-human-assistance chain-end pattern is named here: fallback
  chain ends in a hold phase + deviation report + `OtherOrderReceived`
  completion - the operator's new order is the escalation's resolution.

**From the standards-matrix pass (prior art cited per construct):**

- **Plan identity and supersession** (JAUS AS6062 mission IDs;
  Remove/Replace Messages): `hasPlanID` (exactly 1 on `AutonomousPlanBody`),
  `hasSupersededPlanReference` (max 1), rule R16. Gives the IMO task relation
  its plan-granularity activation semantics and completes the mid-mission
  re-tasking mechanism of sec. 5.7.
- **Suspension as a state** (JAUS Pause/Resume Mission): `PhaseSuspended`
  outcome (non-terminal; R1 updated), `TASKSUSP` task status, rule R17
  (timeouts/cadence pause; guards re-checked at resume).
- **Task-targeted disposition** (FIPA agree/refuse; 4D/RCS "cannot do
  because"): `TASKACPT`/`TASKRJCT` task statuses +
  `TaskDispositionReportContent` (subclass of `TaskStatus`) carrying rationale and a
  machine-readable `hasInfeasibilityCondition`. Closes the per-task
  accept/reject gap that message-level acknowledgment codes cannot target.
- **Lost-link failsafe floor** (STANAG 4586 lost-link/flight termination;
  MAVLink failsafe/RTL/rally): `FailsafeBehaviorCode` {`ReturnToBase`,
  `ReturnToRallyPoint`, `LoiterInPlace`, `ContinueMission`,
  `TerminateMission`}, `hasLostLinkBehaviorCode`/`hasLostLinkTimeout`/
  `hasRallyPointReference` on the plan body, `LostLinkBehaviorActivated`
  deviation, rule R18 (precedence: applicable contingency plan (R14) >
  declared failsafe > platform default).
- **Keep-in/keep-out enforcement** (MAVLink geofence; STANAG restricted
  zones): `EntityInsideArea` predicate - as guard for keep-in, with
  `isNegated` for keep-out; violation routes to a safe-hold fallback.
- **Structured waypoints** (STANAG 4586 #13002-#13004; MAVLink mission
  items; Nav2 waypoint task executors): `StructuredRoute` (subclass of `smx:Route`)
  containing `RouteWaypoint` objects - explicit sequence number (replacing
  the fragile serialization-order convention), per-point transit speed,
  arrival time, loiter duration, and task-on-arrival reference; rule R19.

Not adopted into v0.0.3 (still open, tracked in the review log): inter-task
data flow beyond product references (PL5/Q-E), a Mission/Operation container
(PL10), and the sec. 7 items (notably reactive cross-phase preemption, commanded
re-allocation, report roll-up).

---

## 6. Recommendations

1. **Adopt the plan-extension route** (module in the ASX namespace importing LOX) rather
   than a freestanding behavior ontology. It reuses proven machinery and matches the
   standards-survey recommendation to model BT/HTN concepts directly with IEEE
   1872.1-2024 alignment (correction from the verification pass: 1872.2 verifiably
   defines no Plan/Goal/Mission constructs of its own, so it is not a plan-semantics
   alignment target) - with the interoperability qualification of sec. 4 made explicit
   (fail-closed unknown triggers, capability negotiation for gating constructs).
2. **Raise the candidate core errata with the PDG** - now consolidated as a
   six-item package in [`PDG-Change-Proposals.md`](./PDG-Change-Proposals.md):
   `TASKFAILD`; the `TASKACPT`/`TASKRJCT`/`TASKSUSP` handshake codes; the
   execution-control verbs; a runtime event-occurrence report; the two LOX
   PlanPhase errata; and PlanBody identity - all broadly useful beyond autonomy.
3. **Sequence the work** along the subgroup's decision log: `Condition` + trigger
   subclasses first (feeds Q-D and the Q-N coverage terminator), then
   `HumanApprovalTrigger` + LoA linkage (W1/Q-K — the log's flagged central gap), then
   `Goal`/plan pre-selection (Q-N, goal-directed tasking), then the two report contents
   (X2, X6).
4. **Prerequisites from the existing review:** re-type `Swarm` under `CollectiveEntity`
   (P7) and give `hasAutonomousRoleCode` an attachment point (P3), or the plan semantics
   cannot reach the platforms they are meant to task.
5. **Validate against the scenario corpus**: instantiate the full CASEVAC scenario plus at
   least one *sourced* extraction — the DroneResponse explainability scenario and the MDARS
   persistent watch are the highest-density candidates (§8) — in the module vocabulary, and
   walk them in the instantiation-review format before advancing the OWL.

---

## 7. Known limitations (adversarial findings, kept open by design or deferred)

The following are honest non-coverages, each grounded in a scenario moment from the
repository's own corpus. They are design debts to track, not oversights.

1. **Reactive cross-phase preemption / trigger re-arming.** Triggers gate initial
   activation only (R10); a recovered higher-priority alternative never interrupts a
   running lower-priority phase. MDARS-style "standing watch until exception, human
   intervenes, watch resumes" is expressible only via suspend/resume verbs, not as
   declarative preemption.
2. **Commanded task re-allocation and capability-based assignment.** The Remmersmann MUM-T
   pattern's core — "reassigns a task if a robot is slowed by obstacles," assignment by
   equipment/capability — has only its *report* here (`TaskReassigned`). Constructs for
   authorizing, constraining, or commanding reassignment (and for capability declaration,
   which is arguably ASX-core rather than plan-module) are future work.
3. **Report aggregation / plan roll-up.** "The node aggregates low-level task-status
   reports into a status report for the original high-level task" (Remmersmann): no
   construct relates a disaggregated child plan's status to its parent order's status.
4. **Subgoaling and reconsideration (BDI internals).** A plan step cannot post a goal
   resolved recursively against transmitted plans; commitment-reconsideration strategy is
   the agent's own. Deliberate scope cut — record it as such.
5. **Quantitative control envelopes.** Formation keeping "within accuracy bounds"
   (FormationConvoy, Langerwisch) reduces here to a boolean guard; the numeric envelope
   (gap, bearing, coupled two-vehicle constraints) would have to travel in a
   `ConfigureAutonomy` payload, which is opaque to validation.
6. **Resource-economy / rate conditions.** "Attrit faster than the swarm re-forms while
   conserving magazine depth" (CounterUAS): comparisons of rates and optimization over
   finite resources are neither predicates, achievement conditions, nor guards.
7. **Deception-purposed tasking.** A decoy task whose goal is an effect on enemy
   *perception* for the benefit of another unit's plan (Sustainment extraction) has no
   goal representation.
8. **Belief-correction control acts.** An operator can `OverrideAction` when a system
   tracks a ball it mistook for a person (DroneResponse), but no verb corrects the percept
   itself, so the system may re-derive the same intention. `EstimateConfidenceAbove` gives
   conditions sight of belief state; correcting belief state remains out of scope.
9. **Runtime event announcement.** `EventTrigger` anchors to an event's *time*; the message
   that announces "event X occurred" at runtime is not defined in core/LOX. The module
   routes runtime reactivity through `StateConditionTrigger` instead; a event-occurrence
   report remains a candidate core erratum (§6.2).

---

## 8. Scenario base for illustration and validation

Beyond the contributed CASEVAC (and the LLM-generated MUTT set, which the group rightly
treats as gap probes rather than evidence), the sourced extractions in
`LLMExperiments/PaperSummaries/V2Extractions/` provide strong grounding. The five with the
highest construct density:

| Scenario (source) | Constructs it exercises |
|---|---|
| **DroneResponse multi-sUAS search** (Agrawal et al. 2021, arXiv:2109.02077) | state-condition triggers (event→action loop), fallback ending in request-human-assistance, deviation reports with rationale (the schema §5.6 adapts), control verbs (configure/suspend/acknowledge/override verbatim), `EstimateConfidenceAbove` (switch-to-tracking on confidence) |
| **CBRN UGV reconnaissance** (Muster et al. 2024, arXiv:2406.14385, EnRicH field trials) | per-phase autonomy (autonomous mapping vs operator-verified manipulation), retry-with-limit then abort ("backtrack 0.3 m, clear costmap, replan; abort after three failed attempts"), approval gating without weapons |
| **MDARS persistent watch** (DTIC ADA422465 — fielded Army/SPAWAR program) | `MaintainContinuously` standing watch on a revisit cadence, OR-composite exception triggers (intruder/trapped/fire), suspend/resume around human intervention, maintain-mode goals — "a task that is never finished" |
| **Cooperative MCM** (Ling 2020, NPS thesis, DTIC AD1126497) | achieve-vs-maintain in one mission (neutralize mines vs keep the sea lane usable), repeat-on-cadence perpetual search, cross-unit state trigger (classified-mine location → neutralize) |
| **Urban C-UAS escort** (Corona & Biagini, MESAS 2019 — cite the paper, not the extraction) | human-confirmation gating before action, tiered non-kinetic→kinetic escalation as composite proximity+hostility triggers, status reports carrying proposed next actions |

These five, plus CASEVAC, cover every §5 construct at least twice and are the recommended
walk set for instantiation review (§6.5).

**Walk status:** three of these walks are done — CASEVAC, DroneResponse, and MDARS — in
[`PlanSemanticsWalks/`](./PlanSemanticsWalks/). All three scenarios instantiate end-to-end
in the module vocabulary (Turtle blocks validated against the module); the walks surfaced
no structural defects and nine vocabulary/convention deltas proposed for v0.0.3 (see the
walks' README for the consolidated list). **Update 2026-07-12:** all nine deltas are now
applied in TTL v0.0.3 (sec. 5.10), together with the standards-matrix deltas (plan identity,
suspension, task disposition, lost-link failsafe, keep-in/keep-out, structured waypoints);
each walk carries a "v0.0.3 constructs exercised" addendum.

## See also

- [`../Reference Materials/Standards-for-Autonomous-Systems-Behavior.md`](../Reference%20Materials/Standards-for-Autonomous-Systems-Behavior.md) -
  the standards survey this proposal is built on (ALFUS/4D-RCS autonomy levels,
  IEEE 1872.x, JAUS, STANAG, C2SIM/BML lineage).
- [`./PlanSemantics-Walk.md`](./PlanSemantics-Walk.md) -
  the verification and breadth pass over this proposal: capability matrix vs
  BT/Nav2, PDDL/PlanSys2, FlexBE, MAVLink, IEEE 1872.1-2024, IEEE 1872.2, JAUS
  AS6062, STANAG 4586, 4D/RCS, HTN, FIPA/BDI, every C2SIM-side claim verified
  against the RDF. Two survey corrections established there: IEEE 1872.1 is now
  **1872.1-2024** (June 2024), and IEEE 1872.2 (AuR) defines **no
  Plan/Goal/Mission constructs of its own** - so the relevant plan-semantics
  anchors are 1872.1-2024, STANAG 4586, and JAUS AS6062, not 1872.2.
