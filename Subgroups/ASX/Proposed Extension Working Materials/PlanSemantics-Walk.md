# Plan-Semantics Walk - C2SIM/ASX vs. Robotic Behavior Standards

Compares the plan/tasking machinery available to ASX (base C2SIM + LOX + SMX +
the proposed ASX v0.0.1/v0.0.3) against the plan-definition capabilities of the
robotic standards surveyed in
`../Reference Materials/Standards-for-Autonomous-Systems-Behavior.md`.
The question answered: **which plan constructs that robotic systems routinely
consume (behavior trees, PDDL, JAUS missions, STANAG 4586 routes, HTN, BDI)
are expressible in the current model, and which are not.**

Method: every claim about the C2SIM side was adversarially verified against
the RDF sources (one independent verification pass per claim, each instructed
to refute; see "Verification notes" at the end). The standards side was
researched against primary or near-primary sources; citation URLs are in the
Sources section. Findings are summarized in
`PlanStandards-Findings-and-Decisions.md` (PL-series).

**Relationship to the plan-semantics module.** This walk was produced as an
independent verification-and-breadth pass and then reconciled against the
module proposal already on this branch
(`./Plan-Semantics-Analysis.md` +
`ASX-PlanSemantics-Draft.ttl`; a stale clone initially hid the branch - see
S5 in `PlanStandards-Findings-and-Decisions.md`). The two efforts converge strongly - independent derivations
arriving at the same construct set - which is itself evidence for the
module's design. Sections 1-5 are stated against base C2SIM + LOX + the
main-tree ASX files, as originally verified; **section 8 maps each PL
finding to its module coverage status** and lists the deltas this walk
feeds back into the module. Read the matrix together with section 8.

**Framing.** Same as the rest of the review: the ASX model is v0.0.x work in
progress. Items below are things *still to be defined*, not defects - except
the two base-standard (LOX) internal defects flagged in PL11, which are
upstream C2SIM PDG material.

---

## 1. What the base standard already provides (verified in RDF)

The plan machinery ASX inherits is stronger than a first read suggests.
Everything below was verified against `Ontology/C2SIM.rdf`,
`Ontology/C2SIM_LOX.rdf`, `Ontology/C2SIM_SMX.rdf`:

- **Task = WHO/WHAT/WHEN/WHERE/WHY.** `hasPerformingEntity` (exactly 1),
  `hasTaskActionCode` (exactly 1, from 7 base + 446 LOX JC3IEDM verbs - a
  flat, unparameterized code), start/end/duration (2 of 3), location or
  map graphic, optional `DesiredEffectCode`.
- **Rich pairwise temporal constraints.** `ActionTemporalRelationship`
  (0..* per Action) with **18** `ActionTemporalAssociationCode` individuals:
  six END* codes, six STR* codes (each with no-earlier/no-later variants
  carrying a fixed `Duration` lag), and **six concurrency/overlap codes**
  (SAEAST "the two ACTIONs are concurrent", SAENDO, SASTEA, SBEAST, SDUREA,
  SDUREB). This is a partial-order plan representation with explicit
  concurrency - more expressive than the sequencing primitives of JAUS or
  MAVLink.
- **Phased plans with hierarchy.** LOX `PlanBody` (staging via mandatory
  `isToBeExecutedNow`) -> `PlanPhase` with recursive `hasSubPhase` (0..*),
  exactly one `PlanPhaseTrigger` and exactly one
  `PlanPhaseCompletionCondition` per phase.
- **Trigger vocabulary (closed, 3 subclasses):** `EventTrigger` (fires at
  the *time* of a referenced Event), `OnOrderTrigger` (fires on the start of
  an ordered task, typically `ExecutePlanPhase`), `PriorPhaseCompletionTrigger`
  (sequencing).
- **Completion vocabulary (3 individuals, comment-free):** `AllTasksComplete`
  (join-all), `OneTaskComplete` (join-any), `OtherOrderReceived` (preemption
  by new order).
- **Dormant-phase activation.** A contingency phase can be pre-planned in a
  `PlanBody` and activated at runtime by an order carrying the
  `ExecutePlanPhase` task-action code - executable branch *activation*, with
  failure detection and branch *selection* left to the commander. Note the
  binding is inverted: `OnOrderTrigger` names the activating task UUID at
  authoring time, so an order cannot dynamically select an arbitrary phase.
- **Plan pre-positioning.** `ObjectDefinitions` may define Tasks at
  initialization and LOX adds `hasPlanPhaseReference` - a rudimentary
  plan-library mechanism (STANAG 4586 upload-vs-launch analog).
- **Event-relative timing.** `RelativeTime` = Event reference + start/end
  selector + delay Duration - H-hour style scheduling.
- **Declarative task relations.** `TaskFunctionalRelation` on LOX
  `ManeuverWarfareTask` with 11 JC3IEDM codes: ALT (is-alternative-to),
  HASPRV (provisional sub-action), HASSEC (secondary), HSA (has sub-action -
  a declarative decomposition label), IMO (is-modification-of), INRSTO
  (in-response-to), IOT (in-order-that), ISAPRQ (prerequisite), ISCAUS,
  TPL (template), UAR (uses-as-reference). All are labels on a code +
  task-UUID pair; none carries a condition or executable semantics.
- **Waypoint routes, structurally.** SMX `Route` (a MapGraphic) carries
  points as repeated `hasLocation` values on its PhysicalState; a Task
  references it via `hasMapGraphicID` with verbs like `MoveToLocation` /
  `TRVRS`.
- **Status and speech acts.** `TaskStatusCode` = {TASKPEND, TASKSTRT,
  TASKINPRG, TASKCMPLT, TASKABRT}; header `CommunicativeActTypeCode` includes
  FIPA-style Propose/Accept/Agree/Refuse/Confirm/Inform/Request;
  `AcknowledgeTypeCode` has 8 codes including ACKFAIL/ACKSUCC (message-level,
  not task-targeted).
- **The main-tree ASX files add nothing plan-related.** Verified by full
  reads: v0.0.1 is entity taxonomy + autonomy codes (+ the
  `ComputerProcess` EventCode); v0.0.3 adds Video Detection Report content,
  `AutonomyLevelCode`, `Operator`, `SensorObservation`, Unmanned*Vehicle
  classes. Neither subclasses or references any LOX plan construct.
  (Scope note: the plan-semantics module draft on this branch is exactly
  the proposed missing layer - see section 8.)

## 2. What the robotic standards can say (capability exemplars)

Condensed from the sourced research (URLs in Sources). Per formalism, the
plan-representation primitives that matter for the comparison:

- **Behavior trees (BehaviorTree.CPP v4 / Nav2, the ROS 2 de facto
  standard).** Sequence / Fallback (try-alternatives-in-priority-order) /
  Parallel with success thresholds; Reactive variants that re-evaluate guard
  conditions every tick and halt RUNNING children (preemption); decorators
  Retry-N, Repeat, Loop, Timeout, Precondition; typed blackboard ports for
  dataflow between nodes; SubTrees for hierarchical reuse. Nav2 authors
  missions as BT XML with recovery subtrees (`RecoveryNode` with
  `number_of_retries`, contextual recoveries, RoundRobin recovery cycling)
  and per-waypoint task-executor plugins.
- **PDDL 2.1 (PlanSys2).** Declarative goal state; action preconditions and
  effects over typed objects; durative actions with at-start/at-end/over-all
  conditions; numeric fluents. The plan is generated, not authored; PlanSys2
  converts it to a BT whose independent flows execute in parallel.
- **FlexBE / SMACH (hierarchical state machines).** Outcome-labelled
  transitions; concurrency containers with join policies; userdata channels
  (dataflow); and - unique to FlexBE - a **required autonomy level per
  transition** (Off/Low/High/Full): below the current level, the engine
  stops and waits for operator permission. Operator can force transitions
  and edit the running behavior.
- **MAVLink mission protocol.** Ordered items; DO_JUMP with repeat count
  (loops); CONDITION_* items gating progression; separate geofence and
  rally-point plans as safety envelope/contingency landing sites.
- **IEEE 1872.1-2024 (Robot Task Representation).** Goal = "externally
  defined desired end (or continuing) state"; goal -> task -> sub-task
  decomposition; skill preconditions and expected effects; constraints
  ("complete within 10 s", "stay inside the safe zone"); platform/capability
  context. (Published June 2024 - the survey doc's priority ranking of
  1872.1/1872.2 predates the exact concept inventory confirmed here.)
- **IEEE 1872.2-2021 (AuR).** Verified negative: adds
  environment/interaction/behavior-vs-function semantics, **no Plan, Goal,
  or Mission constructs of its own** (inherits SUMO/CORA Plan). Its value to
  ASX plan semantics is the supposed-vs-actual behavior comparison, not plan
  structure.
- **JAUS (AS6062 Mission Spooling + RA 3.3).** Mission = N-ary tree of
  tasks containing ordinary JAUS command messages; per-message blocking flag
  for synchronization; parallel / sequential / iterative / conditional
  missions; Spool / Run / Pause / Resume / Abort Mission plus Remove/Replace
  Messages (in-flight amendment); mission IDs allow concurrent missions.
- **STANAG 4586 Ed. 3.** Routes typed Launch / Approach / Flight /
  **Contingency A / Contingency B**; per-waypoint speed, arrival time, turn
  type, **loop actions with limit types** (laps / time / min fuel / bingo);
  loiter patterns with durations; **payload actions attached to waypoints**;
  `Define Contingency` (#13007) binding AND/OR condition sets (lost link,
  engine out, ...) to contingency waypoints at waypoint/route/mission/area
  scope; mission upload/download with status and IDs.
- **NIST 4D/RCS.** Task command frame with **goal = "desired state to be
  achieved or maintained"**, parameters, priorities, coordination
  requirements; task frames carrying requirements (tools, resources,
  conditions) and **libraries of plans for routine contingencies**; plans as
  state graphs; job assignor allocating resources to agents; "can't do
  because of condition xyz" tasking feedback.
- **HTN.** Compound tasks + methods (alternative decompositions), ordering
  constraints, operator preconditions/effects.
- **FIPA/BDI.** Plan = triggering event + context condition + body;
  achievement and maintenance goals; request-when / request-whenever
  (condition-guarded tasking); Contract Net (cfp -> propose -> accept)
  task allocation with binding commitments; agree/refuse/failure/inform-done
  reporting.

## 3. Capability matrix

Status legend: YES / PARTIAL / NO for C2SIM+LOX+SMX+ASX as verified.

| # | Capability | C2SIM/ASX status (verified) | Where robotic standards have it |
|---|---|---|---|
| 1 | Sequencing | YES - PriorPhaseCompletionTrigger chains; 18-code temporal algebra | All (BT Sequence, JAUS blocking, STANAG Next Waypoint, HTN ordering) |
| 2 | Hierarchical decomposition | YES structurally - recursive hasSubPhase; HSA label. No alternative decompositions (methods) | BT SubTrees, HTN methods, JAUS task trees, 4D/RCS levels, 1872.1 sub-tasks |
| 3 | Parallelism + join | PARTIAL-YES - six S* concurrency codes; AllTasksComplete/OneTaskComplete joins; intra-phase concurrency implicit, not declared | BT Parallel thresholds, SMACH Concurrence, JAUS parallel missions, PDDL durative concurrency |
| 4 | Temporal constraints | YES - strong (18 codes + Duration lags, RelativeTime H-hour). Point estimates only - no windows/slack | PDDL 2.1 durative actions; STANAG arrival times; 4D/RCS schedules |
| 5 | Waypoint plans | PARTIAL - Route = bare ordered positions (ordering only by XML document order; no per-point speed/time/radius; no actions-at-waypoint) | STANAG #13002-#13004 (speed, arrival time, loiter, payload actions), MAVLink items, Nav2 waypoint executors |
| 6 | Condition-guarded start | PARTIAL - time/order/phase-completion triggers only; no world-state predicate ("when battery low", "when enemy detected") | BT Precondition/condition leaves, PDDL preconditions, BDI context, FIPA request-when, STANAG contingency conditions |
| 7 | State-based completion | PARTIAL - 3 enumerated codes; no "until covered / until threshold" predicate | BT policies, PDDL goal satisfaction, STANAG loop limit types (laps/time/fuel) |
| 8 | Fallback / contingency | PARTIAL-WEAK - dormant phase + human order (ExecutePlanPhase); declarative ALT/HASPRV; **no automatic failure-to-alternative binding** (EventCode cannot even express task failure) | BT Fallback/recovery subtrees, STANAG Contingency A/B + Define Contingency, MAVLink fence/rally, 4D/RCS contingency libraries, BDI plan failure |
| 9 | Loop / retry | NO - nothing; PATROL-style verbs loop only inside one task | BT Retry/Repeat/Loop, MAVLink DO_JUMP, STANAG Loop WP, JAUS iterative missions |
| 10 | Reactive preemption / pause | PARTIAL - OtherOrderReceived ends a phase; no pause/resume/abort verbs for plans, no in-plan event preemption semantics | BT Reactive nodes halting RUNNING subtrees; JAUS Pause/Resume/Abort Mission; FlexBE preemption |
| 11 | Preconditions / effects | NO - DesiredEffectCode carries coded end-states (DSTRYK, NUTRLD, SUPRSD) but is unparameterized, uncheckable, unconsumed | PDDL/HTN operators, 1872.1 skill pre/effects, 4D/RCS task frame conditions |
| 12 | Declarative goal state | NO - no Goal/Objective/EndState class anywhere; DesiredEffectCode is the weakest declarative form | PDDL goals, BDI achievement/maintenance goals, 1872.1 Goal, 4D/RCS task goal |
| 13 | Data flow between tasks | NO - all references are authoring-time UUIDs; a task cannot consume a prior task's runtime output (ties to M1/Q-E) | BT blackboard/ports, FlexBE/SMACH userdata |
| 14 | Operator-authority gating | NO linkage - AutonomyLevelCode + Operator (ASX v0.0.3), ROE, ack codes all exist **unlinked** to plan progression | FlexBE required-autonomy per transition; STANAG LOI levels |
| 15 | Task allocation / negotiation | NO protocol - hasPerformingEntity exactly 1; Propose/Accept/Refuse performatives + conversation IDs exist but no cfp/bid content or binding (ties to G13/Q-V) | FIPA Contract Net, 4D/RCS job assignor |
| 16 | Per-task resource requirements | NO - Resource attaches to ActorEntity only | 1872.1 platform/capability context, 4D/RCS task frame resources |
| 17 | Plan lifecycle (ID, status, amendment) | NO/PARTIAL - PlanBody has **no ID**; no FRAGO/supersede reference; no FAILED/SUSPENDED/REJECTED status; acks (ACKFAIL/ACKSUCC) untargeted; no per-task accept/reject on multi-task orders | JAUS mission IDs + Remove/Replace Messages; STANAG mission upload/download + status; FIPA agree/refuse/failure |
| 18 | Failsafe / geofence binding | NO - areas exist as symbology; nothing binds keep-in/keep-out or lost-link/RTH defaults to execution | MAVLink geofence/rally, STANAG lost-link + flight termination |
| 19 | Mission container / priority | NO - no Mission/Operation class; no priority/preemption property on Task/Order/Phase | JAUS missions, STANAG mission numbers |

**Reading of the matrix.** The model is strong exactly where classical C2
planning is strong - sequencing, hierarchy, temporal constraints, phased
multi-unit plans (rows 1-4) - and covers those *better* than most robotic
messaging standards. Everything characteristic of *autonomous execution* -
reacting to failure without a human (8, 9, 10), reasoning over state (6, 7,
11, 12), passing data between steps (13), graduated human authority (14),
and mission lifecycle management (17) - is absent or human-in-the-loop only.
The plan model assumes the executing unit supplies the intelligence; robotic
standards assume the *plan* must carry it.

## 4. Answer to the framing question

**Is what ROS (and the other standards) can express expressible in the
proposed ontology?** Mostly no, at the semantic level:

- A behavior tree that is a pure `Sequence` of action leaves maps onto a
  PlanBody with PriorPhaseCompletionTrigger-chained phases. **None of the
  other BT pillars maps**: Fallback (no failure binding, row 8),
  Retry/Repeat (row 9), reactive guards (rows 6/10), blackboard dataflow
  (row 13). Nav2's recovery-tree idiom - the single most common real-world
  robot mission pattern - is therefore not representable.
- A PDDL domain/problem is not representable at all (rows 11/12): no
  preconditions, effects, or goal states. What C2SIM *can* carry is the
  linearized *output* of a planner (the plan), not the model that lets the
  robot replan.
- JAUS missions and STANAG 4586 routes are the closest cousins - C2SIM
  expresses their happy path (ordered tasks, waypoint routes) but not their
  contingency machinery (Contingency A/B routes, Define Contingency
  conditions, pause/resume/amend, loop actions, per-waypoint actions).
- FlexBE-style shared authority (the operationally critical construct for
  ASX's human-on-the-loop concerns, W1/Q-K) has all its *vocabulary* in
  place after v0.0.3 (AutonomyLevelCode, Operator) but no linkage to plan
  progression.

The main-tree ASX files currently contribute nothing to plan semantics
(PL-N verified); the module draft on this branch is the proposal that fills
the ASX-layer share of these gaps - section 8 maps which rows it covers
(most of 6-14) and which remain open (5, 13, 17-19 in part). Given C2SIM's
BML lineage, rows 8/9/10/17 also have a base-standard (PDG) dimension the
module itself flags as candidate core errata.

## 5. Findings (PL-series; summarized in PlanStandards-Findings-and-Decisions.md)

| ID | Sev | Item |
|---|---|---|
| PL1 | HIGH | No automatic on-failure contingency binding (matrix 8): no failure trigger/completion, EventCode cannot express task failure, TASKABRT is report-only. Dormant phase + ExecutePlanPhase is human-in-the-loop only and pre-wired at authoring. |
| PL2 | MED | No loop/retry construct (matrix 9). |
| PL3 | HIGH | Trigger/completion vocabulary closed to world state (matrix 6/7); generalizes G2/Q-N (coverage goal is one instance of state-based completion). |
| PL4 | HIGH | No precondition/effect/goal-state layer (matrix 11/12); DesiredEffectCode is the hook to extend. |
| PL5 | MED | No inter-task data flow (matrix 13); extends M1/Q-E from reports to tasking. |
| PL6 | HIGH | No autonomy-level gating of plan progression (matrix 14); sharpens W1/Q-K into a concrete construct: required-authority-per-phase/transition, FlexBE-style. |
| PL7 | MED | Plan lifecycle machinery missing (matrix 10/17): no plan ID, no pause/resume/abort or amend verbs, no FAILED/SUSPENDED/REJECTED, acks untargeted; extends X6. JAUS mission-spooler verbs are the prior art. |
| PL8 | MED | Route waypoints are bare positions (matrix 5): ordering by XML document order only; no per-point speed/time/loiter; no actions-at-waypoint. STANAG 4586 #13002-#13004 is the schema to adopt/align. |
| PL9 | MED | No failsafe/geofence binding (matrix 18): lost-link/RTH defaults and keep-in/keep-out enforcement; extends Q-S/Q-M. |
| PL10 | LOW | No mission container, plan identity, or priority model (matrix 17/19). |
| PL11 | LOW | Base-standard (LOX) internal defects found during verification, upstream PDG material: (a) PlanPhase's rdfs:comment promises "Boolean flags that indicate whether the phase is active and whether it is complete" - no such properties exist; (b) the hasTaskReference axiom says undefined tasks "should be defined in the hasTask property" - PlanPhase declares no hasTask restriction, so inline tasks are comment-only. |

## 6. Proposed decisions (candidates for section 7 of the log)

Revised after reconciliation with the module (section 8): the constructs
this walk originally proposed for PL1-PL4/PL6 already exist in the module
draft, so the lead decision is adoption, not invention. **Update
2026-07-12: Q-X, Q-Y, and Q-Z below were implemented in module v0.0.3 the
same day (rules R16-R19); they remain listed as decisions because the
module itself is pending sub-group review (Q-W).**

- **Q-W [deck]** Review and **adopt the plan-semantics module draft**
  (`Plan-Semantics-Analysis.md` + `ASX-PlanSemantics-Draft.ttl` + three
  validated walks, this branch). Adoption resolves PL1, PL2, PL3, PL4, and
  PL6; this walk's standards matrix independently corroborates the module's
  construct choices (see section 8 convergence note).
- **Q-X** Module v-next deltas from the standards matrix: a
  PlanBody/AutonomousPlanBody identifier, a Suspended phase outcome, and
  task-targeted accept/reject acknowledgments (JAUS AS6062 precedent);
  IEEE alignment corrected to 1872.1-2024 only (1872.2 verifiably has no
  plan constructs). (Resolves PL7, PL10.)
- **Q-Y** Failsafe/geofence binding: a lost-link/RTH default-behavior
  declaration and keep-in/keep-out condition predicates. Prior art: MAVLink
  geofence/rally, STANAG 4586 lost-link + flight termination. (Resolves
  PL9; extends Q-S/Q-M.)
- **Q-Z** Enrich Route to STANAG-4586-grade waypoints: explicit ordering,
  per-point speed/arrival-time/loiter, optional per-waypoint task reference.
  (Resolves PL8.)
- Extensions to existing decisions, no new letter: PL5 -> Q-E (runtime
  entity binding for tasking, not just reports; the module's
  `hasPhaseProductReference` is the reference-level half). PL11 plus the
  module's three candidate core errata (TASKFAILD, cancel/suspend verbs,
  runtime event-occurrence report) -> one consolidated PDG package.

## 7. Verification notes (adversarial pass)

Fifteen claims were independently verified against the RDF, each by a
dedicated refutation attempt. Material corrections the pass forced:

- "No contingency at all" was **too strong**: the dormant-phase +
  ExecutePlanPhase mechanism is executable (human-triggered) branch
  activation, and ALT/HASPRV/INRSTO/ISAPRQ + smx ALTFOR are declarative
  near-misses. PL1 is now scoped to *automatic failure binding*.
- "About a dozen temporal codes" undercounted: **18**, including six
  concurrency codes - which *upgraded* the parallelism row from PARTIAL to
  PARTIAL-YES.
- "Tasks within a phase execute concurrently" is not what LOX says: the
  PlanPhase comment allows "implicit sequencing such as task time";
  concurrency within a phase is the absence of ordering, not a semantic.
- "No goal construct" was qualified: SMX's DesiredEffectCode individuals
  include genuine coded end-states (DSTRYK, NUTRLD, SUPRSD, CAPTRD) -
  the weakest declarative form, and the natural extension point for Q-X.
- "No authority construct" became "no authority *linkage*": v0.0.3 already
  has AutonomyLevelCode and Operator; what is missing is attaching them to
  plan progression.
- IEEE 1872.1 is **2024**, not 2022 as commonly cited; IEEE 1872.2 verifiably
  contains no plan/goal/mission constructs (a common misassumption).
- JAUS sequencing is a per-message *blocking flag*; the "execution times"
  characterization circulating in secondary sources did not survive
  verification.

Residual assumptions worth flagging: IEEE 1872.1-2024 and SAE AS6062
normative texts are paywalled - their concept inventories are sourced from
the working group's published papers, official abstracts, and an
implementing paper, not the standards' clause text. STANAG 4586 facts are
from the Ed. 3 full text.

## 8. Reconciliation with the ASX plan-semantics module draft

> **Update 2026-07-12 (module v0.0.3).** This section was written against
> module v0.0.2 and drove a v0.0.3 revision the same day: the deltas listed
> at the end of this section, and decisions Q-X/Q-Y/Q-Z, are now
> IMPLEMENTED in `ASX-PlanSemantics-Draft.ttl` v0.0.3 (rules R15-R19). The
> table below is kept as the v0.0.2 reconciliation record; read PL5/PL7/
> PL8/PL9/PL10 with the updated statuses in PlanStandards-Findings-and-Decisions.md (PL7/PL8/PL9 now MODULE
> (draft v0.0.3); PL10's plan-ID half closed; PL5 still the open residual).
> Note on version numbering: "ASX v0.0.1/v0.0.3" elsewhere in this doc
> refers to the main-tree ASX RDF files; the module has its own v0.0.x
> series - the two v0.0.3s are different artifacts.

This branch carries a full plan-semantics proposal, produced in a prior
session: `Plan-Semantics-Analysis.md` (BT/BDI/HTN correlation, feasibility
verdict, module design with normative rules R1-R14, extended to R1-R19 in
v0.0.3), `ASX-PlanSemantics-Draft.ttl` (the machine-readable module), three
validation walks (CASEVAC, DroneResponse, MDARS - all instantiate
end-to-end), a briefing deck, and a Sample Plan Messages workbook. This
walk was produced independently and reconciled afterward. **The
convergence is itself evidence:** both efforts, working from different
source sets, derived the same required constructs - fallback-on-failure,
state-condition triggers and guards, goals with achieve/maintain modes,
repetition policies, and a human-approval authority gate.

Per-finding status against the module (as of v0.0.2; see update note above):

| Finding | Module coverage |
|---|---|
| PL1 contingency | ADDRESSED: `TASKFAILD`, `PhaseOutcomeCode`/`PhaseFailureCondition`, `hasOnFailurePhaseReference` + `OnPhaseFailureTrigger`, rules R2-R7 |
| PL2 loop/retry | ADDRESSED: `RepetitionPolicyCode`, `hasRepetitionUntilCondition`/`-Limit`, `hasPhaseTimeout` |
| PL3 state conditions | ADDRESSED: `Condition` (typed predicates incl. `AreaCoverageAchieved`), `StateConditionTrigger`, `CompositeTrigger`, guards. The module's own known limit stands: no reactive cross-phase preemption / trigger re-arming (its section 7.1 = matrix row 10 residual) |
| PL4 goals / pre-effects | ADDRESSED at interchange altitude: `Goal` (achievement/failure conditions, commitment modes). Full PDDL-grade per-task pre/effects deliberately excluded (module section 3.4) - matching this walk's own altitude recommendation |
| PL5 data flow | PARTIAL: `hasPhaseProductReference` is reference-level only (module concedes); blackboard-grade parameter binding still open -> Q-E extension stands |
| PL6 authority gating | ADDRESSED: `HumanApprovalTrigger` + `hasRequiredAutonomyLevelCode` + fail-closed rule R13. FlexBE's required-autonomy-per-transition is independent corroboration of the same design |
| PL7 lifecycle | PARTIAL: suspend/resume/abort/override verbs exist (module 5.7); still missing a PlanBody/AutonomousPlanBody identifier, a Suspended phase outcome, and task-targeted accept/reject acks |
| PL8 waypoints | NOT COVERED - Q-Z stands (STANAG #13002-#13004 schema) |
| PL9 failsafe/geofence | LARGELY OPEN: guards + `CommsDenied`/`HazardOnRoute` express fragments; no lost-link/RTH default declaration, no keep-in/keep-out area binding |
| PL10 container/priority | PARTIAL: `hasPhasePriority`/`hasGoalPriority` exist; no Mission container, no plan ID |
| PL11 LOX defects | UNAFFECTED - combine with the module's three candidate core errata (TASKFAILD, cancel/suspend verbs, runtime event-occurrence report) into one PDG package |

Deltas this walk feeds into the module (v-next):

1. **Align to IEEE 1872.1-2024 only.** Module Recommendation 1 says "IEEE
   1872.1/1872.2 alignment"; 1872.2 verifiably defines no plan constructs
   (and 1872.1 published June 2024).
2. **JAUS AS6062 is direct prior art for module section 5.7**: Spool / Run /
   Pause / Resume / Abort Mission, Remove/Replace Messages (= amendment),
   and mission IDs (= the missing plan identifier).
3. **STANAG 4586 Define Contingency** (AND/OR condition sets at
   waypoint/route/mission/area scope) corroborates `CompositeTrigger`; its
   loop-limit types (laps / time / min fuel / bingo energy) suggest
   resource-based repetition limits the module lacks (its section 7.6).
4. **Runtime event-occurrence report** (module 7.9): corroborated here by
   PL-A evidence (EventCode cannot express failure) and the JAUS Report
   Mission Status precedent - strengthens the PDG erratum case.
5. **Plan identity + task-targeted acks** (PL7 residuals), **waypoint
   schema** (PL8/Q-Z), and **failsafe/geofence binding** (PL9) as module or
   SMX additions.

## Sources

C2SIM side: `Ontology/C2SIM.rdf`, `Ontology/C2SIM_LOX.rdf`,
`Ontology/C2SIM_SMX.rdf`, `Subgroups/ASX/Proposed Extension/CSIM_ASX.rdf`,
`origin/michael_d:Ontology/C2SIM_ASX-v003.rdf`,
`Derived products/C2SIM_SMX_LOX.rdf` (+ .xsd for Route ordering).
Module side: `./Plan-Semantics-Analysis.md`, `ASX-PlanSemantics-Draft.ttl`,
`PlanSemanticsWalks/` (same branch).

Standards side (primary/near-primary):

- BehaviorTree.CPP v4: https://github.com/BehaviorTree/BehaviorTree.CPP ;
  https://behaviortree.github.io/BehaviorTree.CPP/index.html ;
  tutorials at behaviortree.dev (ports, subtrees, reactive nodes)
- Nav2 BTs: https://docs.nav2.org/behavior_trees/index.html ;
  https://docs.nav2.org/behavior_trees/trees/nav_to_pose_recovery.html ;
  https://docs.nav2.org/configuration/packages/configuring-waypoint-follower.html
- PlanSys2 / PDDL 2.1: https://plansys2.github.io/design/index.html ;
  Fox and Long, JAIR 20 (2003),
  https://www.cs.cmu.edu/afs/cs/project/jair/pub/volume20/fox03a-html/JAIRpddl.html
- FlexBE: https://github.com/FlexBE/flexbe_behavior_engine ;
  https://flexbe.readthedocs.io/en/latest/fbetut_3.html (autonomy levels)
- SMACH: https://github.com/ros/executive_smach
- MAVLink missions: https://mavlink.io/en/services/mission.html
- IEEE 1872.1-2024: https://standards.ieee.org/ieee/1872.1/6993/ ;
  Balakirsky/Schlenoff et al., "Towards a Robot Task Ontology Standard"
  (MSEC 2017), https://www.nist.gov/publications/towards-robot-task-ontology-standard ;
  implementing paper https://arxiv.org/abs/2506.10093
- IEEE 1872.2-2021: https://ieeexplore.ieee.org/document/9774339/ ;
  WG article http://www.iri.upc.edu/files/scidoc/2526-IEEE-Standard-for-autonomous-robotics-ontology-[Standards].pdf
- JAUS: NATO STO EN-SCI-271-02 (Introduction to JAUS),
  https://publications.sto.nato.int/publications/STO%20Educational%20Notes/STO-EN-SCI-271/EN-SCI-271-02.pdf ;
  JAUS RA v3.3 sec. 5.6.2; SAE AS6062 https://www.sae.org/standards/as6062-jaus-mission-spooling-service-set/
- STANAG 4586 Ed. 3 full text (Annex B App 1 sec. 4.12, messages
  #13000-#13007, #14000): via everyspec.com
- NIST 4D/RCS v2.0 (NISTIR 6910) sec. 4.1,
  https://www.robotictechnologyinc.com/images/upload/file/4DRCS.pdf
- HTN: Georgievski and Aiello, https://arxiv.org/abs/1403.7426
- FIPA ACL / Contract Net: http://www.fipa.org/specs/fipa00037/SC00037J.html ;
  http://www.fipa.org/specs/fipa00029/SC00029H.html ;
  Rao, AgentSpeak(L) (1996)
