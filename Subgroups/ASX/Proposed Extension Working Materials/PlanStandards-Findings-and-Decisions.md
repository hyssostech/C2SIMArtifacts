# Plan-semantics: standards findings + decisions

Self-contained record of the plan-semantics standards-verification pass:
the PL-series findings (gap matrix vs robotic behavior standards) and the
decisions they put to the sub-group. This is the plan-semantics counterpart to
the instantiation review's own findings log; it was moved here (out of that
review log) so the review baseline stays purely about message instantiation.

Companion artifacts in this folder: `./PlanSemantics-Walk.md` (the full
standards gap matrix and verification notes), `./Plan-Semantics-Analysis.md`
(the proposal and BT/BDI/HTN correlation), `./ASX-PlanSemantics-Draft.ttl`
(the OWL module), and `./PlanSemanticsWalks/` (three validation walks).

## Findings: standards gap matrix + module verification

From `./PlanSemantics-Walk.md`: an independent verification-and-breadth pass
over plan semantics, produced against base C2SIM + LOX + the main-tree ASX
files (a stale clone hid this branch's module - see S5 below), then reconciled
with the module proposal (`./Plan-Semantics-Analysis.md` +
`./ASX-PlanSemantics-Draft.ttl`). Standards compared, all citation-backed:
BT/Nav2, PDDL/PlanSys2, FlexBE/SMACH, MAVLink, IEEE 1872.1-2024, IEEE 1872.2,
JAUS AS6062, STANAG 4586, 4D/RCS, HTN, FIPA/BDI. Every C2SIM-side claim was
adversarially verified against the RDF (15 refutation passes; corrections
listed in the walk's section 7).

**Headline:** base C2SIM+LOX is strong on classical planning (sequencing,
hierarchy, an 18-code temporal algebra incl. 6 concurrency codes - better
than most robotic messaging standards there) and absent on the
autonomy-execution half. The module draft on this branch already covers
most of that half; the walk independently re-derived the same construct
set (fallback, state conditions, goals, repetition, authority gate) -
convergent evidence for the module's design. Statuses below are AFTER
module reconciliation ("MODULE (draft)" = resolved once the module is
adopted). **Update 2026-07-12 (later same day):** module TTL v0.0.3 applied
the walks' nine deltas AND decisions Q-X/Q-Y/Q-Z (rules R15-R19,
adversarially verified, all instance blocks rdflib-validated) - PL7/PL8/PL9
moved to MODULE (draft v0.0.3) and PL10's plan-ID half is closed; statuses
in the table are updated accordingly.

| ID | Sev | Status | Item | Evidence / note |
|---|---|---|---|---|
| PL1 | HIGH | MODULE (draft) | Automatic on-failure contingency | Base: no failure trigger/completion; `EventCode` {GenericEvent, TaskStart, TaskEnd} cannot express failure; TASKABRT is report-only; dormant phase + `ExecutePlanPhase` is human-triggered and pre-wired. Module: `TASKFAILD` + `OnPhaseFailureTrigger` + `hasOnFailurePhaseReference` + R2-R7. Vs BT Fallback / Nav2 recovery / STANAG Contingency A/B + Define Contingency / 4D-RCS contingency libraries. |
| PL2 | MED | MODULE (draft) | Loop/retry | Module `RepetitionPolicyCode` + until-condition + limit + timeout. Vs BT Retry/Repeat, MAVLink DO_JUMP, STANAG Loop WP (laps/time/fuel), JAUS iterative missions. |
| PL3 | HIGH | MODULE (draft) | World-state triggers/completion | Base triggers fire on time/order/phase-completion only; completion = 3 codes. Module `Condition`/`StateConditionTrigger`/`CompositeTrigger`/guards; `AreaCoverageAchieved` covers Q-N. Residual: reactive cross-phase preemption (module's own 7.1). |
| PL4 | HIGH | MODULE (draft) | Goal/end-state layer | No Goal/EndState class in base (DesiredEffectCode = weakest form). Module `Goal` (achieve/maintain, achievement+failure conditions). Full PDDL pre/effects deliberately out of scope at interchange altitude. |
| PL5 | MED | PARTIAL | Inter-task data flow | All base task references are authoring-time UUIDs. Module `hasPhaseProductReference` = reference-level only; blackboard-grade binding (BT ports, FlexBE userdata) open. Extends M1/Q-E to tasking. |
| PL6 | HIGH | MODULE (draft) | Autonomy-gated progression | Base has the vocabulary unlinked (AutonomyLevelCode, Operator, ROE, ack codes). Module `HumanApprovalTrigger` + `hasRequiredAutonomyLevelCode` + fail-closed R13; FlexBE required-autonomy-per-transition independently corroborates. Sharpens W1/Q-K. |
| PL7 | MED | MODULE (draft v0.0.3) | Plan lifecycle | v0.0.3 adds `hasPlanID`/`hasSupersededPlanReference` (R16), `PhaseSuspended`+`TASKSUSP` (R17), and `TaskDispositionReportContent` with `TASKACPT`/`TASKRJCT` (task-targeted accept/reject). JAUS AS6062 = prior art. Extends X6. |
| PL8 | MED | MODULE (draft v0.0.3) | Waypoint enrichment | v0.0.3 adds `StructuredRoute`/`RouteWaypoint` (R19): explicit ordering, per-point speed/arrival-time/loiter, task-on-arrival. STANAG 4586 #13002-#13004 alignment. Refines P5/X3. |
| PL9 | MED | MODULE (draft v0.0.3) | Failsafe/geofence binding | v0.0.3 adds `EntityInsideArea` (keep-in/keep-out guards) and the lost-link disposition (`FailsafeBehaviorCode`, `hasLostLinkBehaviorCode`/`Timeout`, R18). Vs MAVLink fence/rally, STANAG. Extends Q-S/Q-M. |
| PL10 | LOW | PARTIAL | Mission container / priority | Plan-ID half closed by v0.0.3 `hasPlanID`; residual: no Mission/Operation class, no preemption-priority model between plans. |
| PL11 | LOW | OPEN | LOX-internal defects (upstream PDG) | (a) PlanPhase comment promises isActive/isComplete Boolean flags that do not exist as properties; (b) the hasTaskReference axiom cites a `hasTask` property PlanPhase never declares (inline tasks comment-only). Package with the module's three candidate core errata (TASKFAILD, cancel/suspend verbs, runtime event-occurrence report). |

Covered, NOT gaps (verified in base): sequencing, hierarchy (recursive
subphases), temporal algebra (18 codes + lags, `RelativeTime` H-hour), plan
staging (`isToBeExecutedNow`) and pre-positioning (ObjectDefinitions
references), structural waypoint routes, FIPA-style performatives in the
header.

## Decisions for the sub-group

- **Q-W** Review and **adopt the plan-semantics module draft**
  (`./Plan-Semantics-Analysis.md` + `./ASX-PlanSemantics-Draft.ttl` + three
  validated walks, this branch). Adoption resolves PL1-PL4 and PL6; the
  standards matrix independently corroborates its construct choices.
- **Q-X** [DRAFTED in module v0.0.3, pending review] Plan identifier,
  Suspended phase outcome, task-targeted accept/reject acks (JAUS AS6062
  precedent); IEEE alignment corrected to 1872.1-2024 only (1872.2
  verifiably has no plan constructs). (Resolves PL7 and PL10's plan-ID
  half; implemented as rules R16/R17 + TaskDispositionReportContent.)
- **Q-Y** [DRAFTED in module v0.0.3, pending review] Failsafe/geofence
  binding: lost-link/RTH default-behavior declaration + keep-in/keep-out
  condition predicates (MAVLink fence/rally, STANAG 4586 prior art).
  (Resolves PL9; implemented as FailsafeBehaviorCode + EntityInsideArea +
  rule R18; extends Q-S/Q-M.)
- **Q-Z** [DRAFTED in module v0.0.3, pending review] STANAG-4586-grade
  waypoints on Route: explicit ordering, per-point speed/arrival-time/
  loiter, optional per-waypoint task reference (STANAG #13002-#13004).
  (Resolves PL8; implemented as StructuredRoute/RouteWaypoint + rule R19.)
- PL5 folds into **Q-E** in the instantiation review (runtime entity binding
  for tasking, not just reports); PL11 + the module's three candidate core
  errata form one consolidated **PDG package** (see `./PDG-Change-Proposals.md`).

## S5 - process lesson

Stale local refs hid `origin/asx-plan-semantics` (module + walks) from a
follow-on session, which re-derived the gap analysis against base+LOX only.
Same failure shape as a repo-sync issue at branch granularity: a conclusion
of absence requires a `git fetch` first. Caught by the user 2026-07-12;
reconciled in `./PlanSemantics-Walk.md` section 8 - the independent
re-derivation converged on the module's construct set, so the cost bought
corroboration.
