# CASEVAC — Plan-Semantics Walk (module validation)

Purpose: instantiate the contributed CASEVAC scenario end-to-end in the
**ASX plan-semantics module** vocabulary (`ASX-PlanSemantics-Draft.ttl` v0.0.2)
to test whether the module expresses what the scenario demands. Follows the
InstantiationReview walk conventions: **[Q]** = open question, **[!]** = gap /
not-yet-defined, findings get IDs (`PC#`). This is review input, not a decision.

Scenario source: `Subgroups/ASX/ContributedScenarios/CASEVAC.md` (Hyssos).
Prior walk: `InstantiationReview/CASEVAC-Walk.md` (against ASX v0.0.1) — its
findings X1–X6 are re-checked here against the module.

## Scenario recap

Two coordinating UGVs. The **scout** plans a route to the evacuation point,
drives it to verify safety, replans autonomously on obstacle/threat (fallen
bridge, suspected IED report), and publishes the verified route on arrival. The
**transport** awaits the published route, loads the casualty at the collection
point, and follows the scout's route. A soldier stays on-the-loop: mission
updates in, status/position/"explainable reasons" out.

## Plan structure proposed

```
Goal G1 "Casualty at evacuation point"        (AchieveOnce)
Scout plan  (AutonomousPlanBody, execute now, goal G1)
  S1  Verify route            — recon movement; guard: route clear; on-failure -> S2
  S2  Replan and continue     — OnPhaseFailureTrigger(S1); publishes Route-1 on success
Transport plan  (AutonomousPlanBody, execute now, goal G1)
  T1  Load casualty           — move to collection point, load
  T2  Transport via published route — CompositeTrigger ALL [route advertised, casualty aboard, comms up]
```

## 1. Goal (transmitted inline in the scout plan — `hasGoal`)

```turtle
:G1-CasualtyAtEvac a asx:Goal ;
    c2sim:hasUUID "UUID-G1" ;
    asx:hasGoalCommitmentCode asx:AchieveOnce ;
    asx:hasAchievementCondition [ a asx:Condition ;
        asx:hasConditionPredicateCode asx:EntityAtLocation ;
        asx:hasConditionSubjectReference "UUID-casualty" ;
        asx:hasConditionObjectReference "UUID-evac-point" ;
        asx:hasThresholdValue 25.0 ] .        # tolerance, meters
```

Covered cleanly. The WHY of the whole mission is now data (v0.0.1 had no way to
say it at all).

## 2. Scout phase S1 — verify route, replan on hazard

```turtle
:S1-VerifyRoute a asx:AutonomousPlanPhase ;
    c2sim:hasUUID "UUID-S1" ;
    c2sim:hasTaskReference "UUID-task-scout-recon-move" ;    # move along Route-0
    lox:hasPlanPhaseTrigger [ a lox:OnOrderTrigger ;
        c2sim:hasTaskReference "UUID-task-execute-plan" ] ;
    lox:hasPlanPhaseCompletionCondition lox:AllTasksComplete ;
    asx:hasGuardCondition [ a asx:Condition ;
        c2sim:hasUUID "UUID-guard-route0-clear" ;
        asx:hasConditionPredicateCode asx:HazardOnRoute ;
        asx:isNegated true ;
        asx:hasConditionSubjectReference "UUID-Route-0" ;
        asx:hasConditionText "Active route free of obstacle/IED reports" ] ;
    asx:hasOnFailurePhaseReference "UUID-S2" ;
    asx:hasPhaseProductReference "UUID-Route-1" ;            # published on success
    asx:hasGoalReference "UUID-G1" .
```

Notes:
- The scenario's two replan causes map to one guard: a *sensed* obstacle and a
  *received* IED report both surface as hazard state intersecting the route —
  the guard is agnostic to how the world model learned it. That matches the
  scenario's "suspected IED **reported** along the original route".
- Route computation stays onboard ("handled by autonomy"); the module carries
  the **control flow** (guard → fail → S2) and the **reporting** (below), not
  the planner. Recorded as design intent, not a gap.

## 3. Scout phase S2 — the fallback

```turtle
:S2-ReplanContinue a asx:AutonomousPlanPhase ;
    c2sim:hasUUID "UUID-S2" ;
    c2sim:hasTaskReference "UUID-task-scout-continue-move" ; # self-planned alternate
    lox:hasPlanPhaseTrigger [ a asx:OnPhaseFailureTrigger ;
        lox:hasTriggerPhase "UUID-S1" ] ;                    # fires ONLY on S1 failure (R7)
    lox:hasPlanPhaseCompletionCondition lox:AllTasksComplete ;
    asx:hasGuardCondition [ a asx:Condition ;
        asx:hasConditionPredicateCode asx:HazardOnRoute ;
        asx:isNegated true ] ;
    asx:hasOnFailurePhaseReference "UUID-S3-hold-report" ;   # chain: next alternative
    asx:hasPhaseProductReference "UUID-Route-1" ;
    asx:hasGoalReference "UUID-G1" .
```

The v0.0.1 walk could not express this at all (X6 "re-tasking mid-mission
semantics" was an open question). Under v0.0.2 rules: S1's failure activates S2
(R7); if S2 succeeds, S1 counts as succeeded for the parent (R7), so the plan
proceeds; the transport is never aware the failure happened except via reports.

**Deviation report the scout sends when this path activates:**

```turtle
:Dev1 a asx:PlanDeviationReportContent ;
    asx:hasDeviationTypeCode asx:FallbackActivated ;
    asx:hasDeviationCondition [ a asx:Condition ;
        c2sim:hasUUID "UUID-guard-route0-clear" ;
        asx:hasConditionPredicateCode asx:HazardOnRoute ;
        asx:isNegated true ] ;
    lox:hasPlanPhaseReference "UUID-S1" ;
    asx:hasRationaleText "Suspected IED reported on Route-0 at bridge crossing; replanning via northern ford, transport clearance verified." ;
    smx:hasConfidenceLevel 0.85 .
```

This is CASEVAC step 8 ("explainable reasons … why did it change its expected
route") **as a structured message** — the v0.0.1 walk's headline gap X2.

## 4. Route publication (scout → transport)

- **Plan side: covered.** S1/S2 declare `hasPhaseProductReference "UUID-Route-1"`;
  the transport's task references the same UUID (§5).
- **[!] PC2 — late-bound product convention.** `UUID-Route-1` names a route that
  does not exist at plan-authoring time; the plan works because the UUID is
  **pre-allocated** and the scout fills it at runtime. This convention works but
  is nowhere stated normatively — candidate sentence for the module header
  (or rule R15). **LOW** (pattern is sound, needs writing down).
- **[!] PC3 — the advertisement message itself is still missing.** The module
  gives the trigger side (`EventTrigger` on the advertisement event) and the
  product reference, but the message that *carries* Route-1 from scout to
  transport remains undefined — v0.0.1 finding **X1 persists at the message
  layer** (no robot-to-robot route-advertisement content type; SMX `Route`
  exists but has no payload wrapper, old X3). The plan semantics are ready and
  waiting for it. **HIGH** (inherited, not new).

## 5. Transport phase T2 — the composite departure gate

```turtle
:T2-Transport a asx:AutonomousPlanPhase ;
    c2sim:hasUUID "UUID-T2" ;
    c2sim:hasTaskReference "UUID-task-transport-move" ;      # follows Route-1
    lox:hasPlanPhaseTrigger [ a asx:CompositeTrigger ;
        asx:hasLogicalOperatorCode asx:AllSubTriggers ;
        asx:hasSubTrigger [ a lox:EventTrigger ;
            lox:hasEvent :RouteAdvertisedEvent ] ;
        asx:hasSubTrigger [ a asx:StateConditionTrigger ;
            asx:hasCondition [ a asx:Condition ;
                asx:hasConditionPredicateCode asx:EntityWithinRange ;
                asx:hasConditionSubjectReference "UUID-casualty" ;
                asx:hasConditionObjectReference "UUID-transport-ugv" ;
                asx:hasThresholdValue 2.0 ] ] ;              # casualty aboard (proxy)
        asx:hasSubTrigger [ a asx:StateConditionTrigger ;
            asx:hasCondition [ a asx:Condition ;
                asx:hasConditionPredicateCode asx:CommsAvailable ;
                asx:hasConditionSubjectReference "UUID-transport-ugv" ] ] ] ;
    lox:hasPlanPhaseCompletionCondition lox:AllTasksComplete ;
    asx:hasGoalReference "UUID-G1" .
```

- R9 does real work here: comms must **hold** at departure (state condition),
  while the route advertisement **latches** (discrete event). Correct by rule.
- **[!] PC1 — no embarkation predicate.** "Casualty loaded on stretcher" is
  modeled above as `EntityWithinRange(casualty, transport, 2 m)` — a proxy, and
  a wrong one (a casualty lying next to the vehicle satisfies it). The predicate
  vocabulary lacks payload/embarkation state. Candidate: `PayloadOnBoard`
  (subject = carrier, object = payload entity). **MED** — proposed v0.0.3 delta.

## 6. On-the-loop supervision

| Scenario requirement | Module element | Status |
|---|---|---|
| status/position throughout | core `PositionReportContent` + `asx:PlanExecutionStatusContent` (phase, outcome, active goal, **ETA**) | covered — ETA was the open bit of old X5 |
| mission update commands | `SuspendPlanExecution` → amended plan (`IMO`) → `ResumePlanExecution` | covered — the X6 mechanism |
| explainable reasons | `PlanDeviationReportContent` (§3) | covered — old X2 |
| human-understandable | `hasRationaleText` + `hasConditionText` (display-only by rule) | covered |

## Findings summary

| ID | Sev | Verdict | One-line |
|---|---|---|---|
| PC1 | MED | gap | No embarkation/payload-state predicate; `EntityWithinRange` is a false proxy. Propose `PayloadOnBoard`. |
| PC2 | LOW | convention gap | Late-bound product references work via pre-allocated UUIDs — the convention must be stated normatively. |
| PC3 | HIGH | inherited | Route-advertisement *message* still undefined (v0.0.1 X1/X3); plan side is ready for it. |
| — | — | covered | Replan-on-hazard control flow + rationale reporting (old X2, X6); phased ETA (old X5); goal as data; composite departure gating; guard polarity. |

**Net:** the module expresses every CASEVAC behavior requirement except the
robot-to-robot *message payload* (which was never a plan-semantics problem), and
the walk surfaced one genuine vocabulary gap (PC1) plus one convention to write
down (PC2).

## v0.0.3 addendum - constructs exercised (2026-07-12)

PC1 is resolved by `PayloadOnBoard` (the departure gate now states the actual
embarkation fact, not a 2 m proximity proxy); PC2 is now normative rule R15.
PC3 (the route-advertisement message payload) remains inherited/open - but the
route the scout advertises can now itself be a `StructuredRoute`, which closes
most of the payload question: the "verified safe route" is an object with
ordered waypoints, speeds, and a sensor task at the chokepoint, not a bare
polyline.

```turtle
:DepartureGate-v3 a asx:StateConditionTrigger ;                # PC1 resolved
    asx:hasCondition [ a asx:Condition ;
        asx:hasConditionPredicateCode asx:PayloadOnBoard ;
        asx:hasConditionSubjectReference "UUID-transport-ugv" ;
        asx:hasConditionObjectReference "UUID-casualty-1" ] .

:EvacRoute-1 a asx:StructuredRoute ;                           # the scout's product, R15 UUID
    c2sim:hasUUID "UUID-Route-1" ;                             # binds the PRE-ALLOCATED product UUID
    asx:hasRouteWaypoint [ a asx:RouteWaypoint ;
        asx:hasWaypointSequenceNumber 1 ;
        c2sim:hasLocation [ a c2sim:Location ] ;
        asx:hasTransitSpeed 8.0 ] ;                            # m/s, leg into WP1
    asx:hasRouteWaypoint [ a asx:RouteWaypoint ;
        asx:hasWaypointSequenceNumber 2 ;
        c2sim:hasLocation [ a c2sim:Location ] ;
        asx:hasTransitSpeed 3.0 ;                              # slow through the chokepoint
        asx:hasWaypointTaskReference "UUID-task-sensor-sweep" ; # R19: sweep on arrival
        asx:hasLoiterDuration [ a c2sim:Duration ] ] ;         # fixed post-sweep hold (R19: the sweep itself blocks until terminal status)
    asx:hasRouteWaypoint [ a asx:RouteWaypoint ;
        asx:hasWaypointSequenceNumber 3 ;
        c2sim:hasLocation [ a c2sim:Location ] ;
        asx:hasWaypointArrivalTime [ a c2sim:TimeInstant ] ] . # CCP arrival commitment

:TransportMovePhase-v3 a asx:AutonomousPlanPhase ;             # keep-out enforcement added
    c2sim:hasUUID "UUID-transport-move-v3" ;
    asx:hasGuardCondition [ a asx:Condition ;
        asx:hasConditionPredicateCode asx:EntityInsideArea ;
        asx:hasConditionSubjectReference "UUID-transport-ugv" ;
        asx:hasConditionObjectReference "UUID-ied-exclusion-zone" ;
        asx:isNegated true ] ;                                 # never inside the exclusion zone
    asx:hasOnFailurePhaseReference "UUID-replan-route-phase" .

:TransportAccepts a asx:TaskDispositionReportContent ;         # the tasking handshake
    c2sim:hasCurrentTask "UUID-task-move-to-casualty" ;
    c2sim:hasTaskStatusCode asx:TASKACPT .
```

The X6 amendment loop also completes here: suspend, transmit the amended plan
with `hasPlanID` new / `hasSupersededPlanReference` old (R16, the IMO relation
made executable), resume - the transport can now be re-routed mid-evacuation
with the supersession explicit in data.
