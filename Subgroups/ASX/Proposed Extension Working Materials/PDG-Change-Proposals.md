# Candidate C2SIM PDG Change Proposals (from the ASX plan-semantics track)

Consolidated package of base-standard items surfaced by the ASX plan-semantics
work (module `ASX-PlanSemantics-Draft.ttl` + the standards verification pass
`./PlanSemantics-Walk.md`). These are items that benefit
ALL C2SIM users, not only autonomy, and therefore belong upstream with the
C2SIM Product Development Group rather than in the ASX layer. Each is carried
in the ASX module in the interim (items 1-3 and 6) or is purely a
base-standard fix (items 4-5).

Status: DRAFT for ASX sub-group review before anything goes to the PDG.
Prepared 2026-07-12 on branch `asx-plan-semantics`.

## 1. TaskStatusCode: add a failure value (TASKFAILD)

- **Problem.** `TaskStatusCode` = {TASKPEND, TASKSTRT, TASKINPRG, TASKCMPLT,
  TASKABRT}. "Attempted and did not achieve its purpose" is not sayable -
  a task completes or is aborted. Any consumer of task reports (simulation
  scoring, C2 monitoring, after-action review) loses the distinction between
  "stopped by command" and "tried and failed".
- **Proposal.** Add individual `TASKFAILD` ("Task failed: attempted and did
  not achieve its purpose; distinct from TASKABRT, execution stopped by
  command or exception.") to `C2SIM#TaskStatusCode`.
- **Evidence.** `Ontology/C2SIM.rdf` TaskStatusCode individuals (5 total);
  every robotic execution standard surveyed distinguishes failure from abort
  (behavior-tree FAILURE status; FIPA `failure` act; JAUS mission status).

## 2. TaskStatusCode: add handshake and suspension values
   (TASKACPT / TASKRJCT / TASKSUSP)

- **Problem.** (a) Acknowledgment codes (`ACKFAIL`/`ACKSUCC`/`ACKREQGRT`/
  `ACKREQDEN`) are message-level: on a multi-task order there is no way to
  accept task 1 and decline task 2. (b) There is no suspended state - JAUS
  Pause/Resume Mission has no reportable counterpart.
- **Proposal.** Add `TASKACPT` (commitment to perform; FIPA agree), `TASKRJCT`
  (declined / cannot perform; FIPA refuse, the 4D/RCS "cannot do because"
  reply), and `TASKSUSP` (paused with state retained) to
  `C2SIM#TaskStatusCode`. `TaskStatus` already targets a single task via
  `hasCurrentTask`, so no structural change is needed - only code values.
- **Evidence.** `C2SIM.rdf` AcknowledgeTypeCode individuals (8, all
  message-scoped, no task reference in either acknowledgment body);
  FIPA Communicative Act Library (agree/refuse); JAUS AS6062 mission
  lifecycle; NISTIR 6910 sec. 4.1 (task feedback).

## 3. TaskActionCode: task/plan execution-control verbs

- **Problem.** No standard verbs exist to suspend, resume, or abort an
  in-flight task or plan; re-tasking today means issuing a whole new order
  with undefined semantics for the old one (review item X6).
- **Proposal.** Add control verbs to the core or LOX `TaskActionCode` list:
  suspend / resume / abort (the ASX module carries `SuspendPlanExecution`,
  `ResumePlanExecution`, `AbortPlanExecution`, `OverrideAction`,
  `ConfigureAutonomy` in the interim; the first three are domain-neutral).
- **Evidence.** JAUS AS6062 Spool/Run/Pause/Resume/Abort Mission message set;
  STANAG 4586 mission-control modes; DroneResponse operator verb set
  (configure/suspend/acknowledge/override).

## 4. Runtime event-occurrence report

- **Problem.** `lox:EventTrigger` fires "at the time of an event", but no
  message is defined for announcing at runtime that an event has occurred;
  `EventCode` = {GenericEvent, TaskStart, TaskEnd} cannot even express task
  failure (TaskEnd does not distinguish completion from abort).
- **Proposal.** Define an event-occurrence ReportContent (event reference,
  occurrence time, optional observed parameters), and consider extending
  `EventCode`. This makes `EventTrigger` usable for runtime reactivity by any
  federation member, not only pre-scheduled occurrences.
- **Evidence.** `C2SIM.rdf` Event class restrictions (mandatory
  hasStartTime - structurally a scheduled occurrence); JAUS Report Mission
  Status ("Message Finished") precedent.

## 5. LOX PlanPhase internal defects (errata)

- **(a) Phantom Boolean flags.** The `lox:PlanPhase` rdfs:comment promises
  "Boolean flags that indicate whether the phase is active and whether it is
  complete" - no such properties exist anywhere in LOX. Either add
  `isActive`/`isComplete` (as reportable state, not authored data) or correct
  the comment.
- **(b) Comment-only inline tasks.** The `hasTaskReference` annotation axiom
  on PlanPhase says undefined tasks "should be defined in the hasTask
  property" - but PlanPhase declares no `hasTask` restriction; `hasTask`
  never appears in LOX. Either add the restriction or correct the axiom
  comment.
- **Evidence.** `Ontology/C2SIM_LOX.rdf` PlanPhase class (comment at the
  class, axiom on hasTaskReference); repo-wide grep confirms no
  isActive/isComplete/hasTask on PlanPhase in any merged artifact.

## 6. PlanBody identity

- **Problem.** `lox:PlanBody` has no identifier (OrderBody has `hasOrderID`,
  ReportBody has `hasReportID`). A transmitted plan cannot be referenced,
  superseded, reported against, or held concurrently with others.
- **Proposal.** Add a plan identifier to `lox:PlanBody` (the ASX module adds
  `hasPlanID` on its `AutonomousPlanBody` subclass in the interim; the need
  is not autonomy-specific).
- **Evidence.** `C2SIM_LOX.rdf` PlanBody restrictions (hasPlanPhase /
  hasPlanPhaseReference / isToBeExecutedNow only); JAUS AS6062 mission IDs;
  STANAG 4586 Mission ID field in the Mission Transfer Command.

## Suggested handling

Items 1-2 are single-code-list errata (lowest cost, highest shared value);
item 5 is a documentation/consistency erratum; items 3, 4, and 6 are small
feature proposals. Recommend the sub-group review this package alongside the
module (decision Q-W) and submit 1, 2, and 5 first.
