# DroneResponse (Agrawal 2021) — Plan-Semantics Walk (module validation)

Purpose: instantiate the sourced DroneResponse human-on-the-loop multi-sUAS
search scenario in the **ASX plan-semantics module** vocabulary
(`ASX-PlanSemantics-Draft.ttl` v0.0.2). This is the scenario the group sourced
specifically to fill the explainability validation hole (grounds Q-H, Q-K/W1,
Q-D), and the one whose explanation schema §5.6 of the analysis adapts — so it
is the module's most direct accountability test. **[Q]** / **[!]** / `PD#`
conventions as in the InstantiationReview walks. Review input, not a decision.

Scenario source:
`LLMExperiments/PaperSummaries/V2Extractions/Explainability_Agrawal2021.md`
(Agrawal, Cleland-Huang et al. 2021, arXiv:2109.02077, read in full).

## Scenario recap

Four autonomous sUAS conduct a coordinated area search for a victim under one
on-the-loop operator. Each sUAS reacts to recognized events — adverse weather
(fly lower/slower), person detected with sufficient confidence (switch to
tracking), low battery / signal loss (return-to-launch fail-safe), path
obstruction (replan, or request human assistance if no viable path) — and
pushes an explanation to the operator: {event, action taken, reasoning,
operational change, confidence}. The operator may configure, suspend,
acknowledge, or override. The study injects wrong perceptions (ball tracked as
a person) to test operator correction.

## Plan structure proposed

```
Goal G1 "Victim located"                      (AchieveOnce; confidence-based)
Per-sUAS plan (x4, identical shape; per-vehicle tasks — Task has exactly one performer)
  D1  Area search      — RepeatUntilCondition(victim confidence); sweep iterations
  D2  Track victim     — StateConditionTrigger(EstimateConfidenceAbove)
  D3  Replan path      — OnPhaseFailureTrigger(D1)
  D4  Request assistance / hold — OnPhaseFailureTrigger(D3)   [end of chain]
```

## 1. Goal — confidence-based achievement

```turtle
:G1-VictimLocated a asx:Goal ;
    c2sim:hasUUID "UUID-G1" ;
    asx:hasGoalCommitmentCode asx:AchieveOnce ;
    asx:hasAchievementCondition [ a asx:Condition ;
        asx:hasConditionPredicateCode asx:EstimateConfidenceAbove ;
        asx:hasConditionObjectReference "UUID-victim-track" ;
        asx:hasThresholdValue 0.7 ] .
```

`EstimateConfidenceAbove` (added in v0.0.2 from this very scenario) carries the
paper's "person detected **with sufficient confidence**" — the goal is achieved
by *belief state*, which is exactly right for a search mission. The victim-track
UUID is pre-allocated (same late-bound convention as CASEVAC walk PC2).

## 2. Phase D1 — search as a bounded loop

```turtle
:D1-AreaSearch a asx:AutonomousPlanPhase ;
    c2sim:hasUUID "UUID-D1" ;
    c2sim:hasTaskReference "UUID-task-search-sector-A" ;
    lox:hasPlanPhaseTrigger [ a lox:OnOrderTrigger ;
        c2sim:hasTaskReference "UUID-task-execute-plan" ] ;
    lox:hasPlanPhaseCompletionCondition lox:AllTasksComplete ;   # closes each sweep
    asx:hasRepetitionPolicyCode asx:RepeatUntilCondition ;
    asx:hasRepetitionUntilCondition [ a asx:Condition ;
        asx:hasConditionPredicateCode asx:EstimateConfidenceAbove ;
        asx:hasConditionObjectReference "UUID-victim-track" ;
        asx:hasThresholdValue 0.7 ] ;
    asx:hasOnFailurePhaseReference "UUID-D3" ;
    asx:hasRequiredAutonomyLevelCode asx:FullAuto ;
    asx:hasGoalReference "UUID-G1" .
```

- The v0.0.2 split between per-iteration completion (LOX code) and loop
  termination (`hasRepetitionUntilCondition`) is what makes this expressible at
  all — under v0.0.1 the loop terminated after one sweep (review finding C5).
- Coordination across the four sUAS (sector assignment) is initialization data,
  not plan semantics; each sUAS gets its own sector task. Fine.

## 3. The event → action → explanation loop

The paper's four event classes, walked against the module:

| Paper event | Autonomous action | Module expression | Status |
|---|---|---|---|
| Adverse weather | fly lower and slower | behavior adjustment internal; **deviation report** announces it | **[!] PD1** — no fitting deviation type |
| Person detected (confident) | switch search → tracking | D2 with `StateConditionTrigger(EstimateConfidenceAbove)`; D1 loop terminates on the same condition | covered |
| Low battery / signal loss | return-to-launch fail-safe | guard on D1/D2; violation → RTL fallback phase | **[!] PD2** — predicate is a stretch |
| Path obstruction | replan; if no path, request assistance | D1 → D3 (replan) → D4 (assistance) fallback chain | covered structurally; **[!] PD3** on D4's task verb |

**PD1 — deviation vocabulary too narrow.** "Flying lower and slower due to
mist" changes no route, activates no fallback, switches no plan, abandons no
goal, reassigns no task: none of the five `DeviationTypeCode` values fits, yet
the paper requires an explanation push for exactly this case. Candidate v0.0.3
individual: **`BehaviorAdjusted`** (operating-parameter change within the same
task). **MED**, and cheap.

**PD2 — no endurance predicate.** Low battery is modeled here as
`EntityHealthBelow(self, 0.2)` — battery is not "health", and signal loss is
`CommsDenied` (fine). Candidate v0.0.3 predicate: **`RemainingEnduranceBelow`**
(threshold = fraction or duration). **MED.**

```turtle
:D2-Track a asx:AutonomousPlanPhase ;
    c2sim:hasUUID "UUID-D2" ;
    c2sim:hasTaskReference "UUID-task-track-victim" ;
    lox:hasPlanPhaseTrigger [ a asx:StateConditionTrigger ;
        asx:hasCondition [ a asx:Condition ;
            asx:hasConditionPredicateCode asx:EstimateConfidenceAbove ;
            asx:hasConditionObjectReference "UUID-victim-track" ;
            asx:hasThresholdValue 0.7 ] ] ;
    lox:hasPlanPhaseCompletionCondition lox:OtherOrderReceived ;  # tracks until relieved
    asx:hasGuardCondition [ a asx:Condition ;
        asx:hasConditionPredicateCode asx:EntityHealthBelow ;     # PD2: battery proxy
        asx:hasConditionSubjectReference "UUID-suas-1" ;
        asx:hasThresholdValue 0.2 ;
        asx:isNegated true ] ;                                    # invariant: NOT low
    asx:hasOnFailurePhaseReference "UUID-D5-RTL" ;
    asx:hasGoalReference "UUID-G1" .
```

## 4. The explanation push — schema accountability check

Paper schema: **{event, action taken, reasoning, operational change, confidence}**.
Module: `PlanDeviationReportContent` {deviation type, triggering event/condition,
affected phase, rationale text, confidence}.

| Paper field | Module field | Verdict |
|---|---|---|
| event | `hasTriggeringEventReference` / `hasDeviationCondition` | covered |
| reasoning | `hasRationaleText` | covered |
| operational change | `hasDeviationTypeCode` | covered *given* PD1's `BehaviorAdjusted` |
| confidence | `smx:hasConfidenceLevel` | covered |
| **action taken** | — (implied by deviation type + phase ref) | **[!] PD4** |

**PD4 — no explicit "action taken" slot.** For `FallbackActivated` the action is
recoverable from the fallback phase reference, but for `BehaviorAdjusted` (PD1)
the *new behavior* ("now flying at 40 ft, 5 kt") has no structured home and
falls into rationale text. Candidate v0.0.3: optional
`hasActionTakenReference` (UUID → task/phase) **or** accept rationale-text
carriage and say so. **LOW–MED** — the operator-facing content survives either
way; structure is what's at stake.

## 5. Escalation end of the fallback chain

```turtle
:D4-RequestAssistance a asx:AutonomousPlanPhase ;
    c2sim:hasUUID "UUID-D4" ;
    c2sim:hasTaskReference "UUID-task-hold-position" ;            # HoldInPlace (core)
    lox:hasPlanPhaseTrigger [ a asx:OnPhaseFailureTrigger ;
        lox:hasTriggerPhase "UUID-D3" ] ;
    lox:hasPlanPhaseCompletionCondition lox:OtherOrderReceived .  # waits for the human
```

**PD3 — "request human assistance" has no task verb.** The walk models D4 as
core `HoldInPlace` + the deviation report that R7's chain exhaustion implies,
with completion `OtherOrderReceived` (the operator's response is the exit). That
*works* — the request itself rides on `RequestBody`, which core already scopes
as discretionary — but the pattern (hold + report + await) is a convention, not
a construct. Candidate: either a `RequestAssistance` TaskActionCode or a stated
escalation pattern in the module header. **LOW** — expressible today, worth
naming.

## 6. Operator control loop

| Paper verb | Module element | Status |
|---|---|---|
| configure | `ConfigureAutonomy` | covered (payload opacity = known limitation §7.5) |
| suspend | `SuspendPlanExecution` | covered |
| acknowledge | `AcknowledgementBody` + performatives (no new verb, by design) | covered |
| override | `OverrideAction` | covered — stops the action |
| *(correct the percept)* | — | confirmed limitation §7.8: overriding the ball-track stops the tracking, but nothing corrects the world model, so the sUAS may re-derive the same intention. The walk **confirms** this is real, not theoretical. |

## Findings summary

| ID | Sev | Verdict | One-line |
|---|---|---|---|
| PD1 | MED | gap | `DeviationTypeCode` lacks a behavior-adjustment value; propose `BehaviorAdjusted`. |
| PD2 | MED | gap | No endurance/battery predicate; propose `RemainingEnduranceBelow`. |
| PD3 | LOW | convention | Request-assistance escalation expressible as hold+report+await; pattern should be named. |
| PD4 | LOW–MED | partial | Explanation schema's "action taken" has no structured slot; propose optional `hasActionTakenReference` or accept text carriage. |
| — | — | confirmed limit | Belief correction (§7.8) is real: override stops the act, not the percept. |
| — | — | covered | Confidence-gated goal + loop termination; search→track transition; fallback chain; all four operator verbs; per-phase autonomy level. |

**Net:** the module carries the scenario's structure and its explanation loop;
the walk caught the deviation vocabulary being one value too narrow (PD1) and
sharpened three smaller deltas — exactly what a validation walk is for.

## v0.0.3 addendum - constructs exercised (2026-07-12)

All four PD findings are resolved in TTL v0.0.3: PD1 -> `BehaviorAdjusted`;
PD2 -> `RemainingEnduranceBelow`; PD3 -> the escalation pattern is named in
the analysis doc (5.10; hold + deviation report + `OtherOrderReceived`);
PD4 -> `hasActionTakenReference`. Two standards-matrix additions are exercised
below: the lost-link floor (the paper's sUAS fly beyond reliable link range)
and the task-disposition handshake (a vehicle declining a task it cannot
finish - the refusal the paper's operators today infer from silence).

```turtle
:SearchPlan-1 a asx:AutonomousPlanBody ;
    asx:hasPlanID "UUID-plan-search-1" ;                       # R16
    asx:hasLostLinkBehaviorCode asx:ReturnToBase ;             # R18: RTL floor
    asx:hasLostLinkTimeout [ a c2sim:Duration ] .              # 60 s

:DevAltitudeChange a asx:PlanDeviationReportContent ;          # PD1 resolved
    asx:hasDeviationTypeCode asx:BehaviorAdjusted ;
    lox:hasPlanPhaseReference "UUID-D2" ;
    asx:hasActionTakenReference "UUID-task-track-victim" ;     # PD4 resolved
    asx:hasRationaleText "Descended 40->25 m for victim confirmation imagery; track geometry unchanged." ;
    smx:hasConfidenceLevel 0.83 .

:SUASDeclinesLeg a asx:TaskDispositionReportContent ;          # the 4D/RCS 'cannot do because'
    c2sim:hasCurrentTask "UUID-task-search-sector-7" ;
    c2sim:hasTaskStatusCode asx:TASKRJCT ;
    asx:hasInfeasibilityCondition [ a asx:Condition ;
        asx:hasConditionPredicateCode asx:RemainingEnduranceBelow ;   # PD2 resolved
        asx:hasConditionSubjectReference "UUID-suas-3" ;
        asx:hasThresholdValue 0.25 ] ;
    asx:hasRationaleText "Sector 7 round trip exceeds remaining endurance at current winds." .

:DevLostLink a asx:PlanDeviationReportContent ;                # reported on link restoration
    asx:hasDeviationTypeCode asx:LostLinkBehaviorActivated ;
    asx:hasRationaleText "Link lost 14:02:10Z-14:05:35Z; executed ReturnToBase per plan floor; link restored on approach." .
```

The belief-correction limitation (7.8) stands - `TASKRJCT` lets the vehicle
say "cannot", and `BehaviorAdjusted` lets it say "changed how", but nothing
yet corrects the percept behind a wrong intention.
