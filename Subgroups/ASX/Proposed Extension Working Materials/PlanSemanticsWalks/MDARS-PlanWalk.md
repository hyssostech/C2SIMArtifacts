# MDARS Persistent Watch — Plan-Semantics Walk (module validation)

Purpose: instantiate the MDARS depot standing-watch scenario in the
**ASX plan-semantics module** vocabulary (`ASX-PlanSemantics-Draft.ttl` v0.0.2).
MDARS is the corpus's strongest provenance (a fielded Army/SPAWAR program,
operational evaluation at Hawthorne Army Depot) and the sharpest test of the
one construct classic tasking lacks entirely: **a task that is never finished**.
Grounds N2 (standing task with cadence), Q-U (relief hand-off), Q-N (coverage).
**[Q]** / **[!]** / `PM#` conventions as in the InstantiationReview walks.
Review input, not a decision.

Scenario source:
`LLMExperiments/PaperSummaries/V2Extractions/PersistentWatch_MDARS.md`
(DTIC ADA422465 and related, read in full).

## Scenario recap

Autonomous UGVs patrol designated depot regions continuously, on a revisit
cadence, performing RF-tag inventory as they go. Each robot keeps its standing
watch until an **exceptional event** — intruder detected, robot trapped, fire
found — at which point it reports and the guard at a host console (one guard,
up to 255 platforms) intervenes and interacts with that platform directly.
Afterwards, the patrol resumes on its cadence. Response to intruders is
non-lethal challenge-and-response.

## Plan structure proposed

```
Goal G1 "Depot region secure"                  (Maintain — never terminal)
Per-robot plan (AutonomousPlanBody, execute now, goal G1)
  M1  Standing patrol + inventory   — MaintainContinuously; completion OtherOrderReceived
  M2  Assess & challenge            — ANY-composite exception trigger; approval-gated response
```

## 1. The maintain-goal — what "secure" means as data

```turtle
:G1-RegionSecure a asx:Goal ;
    c2sim:hasUUID "UUID-G1" ;
    asx:hasGoalCommitmentCode asx:Maintain ;
    asx:hasAchievementCondition [ a asx:Condition ;
        asx:hasConditionPredicateCode asx:ThreatDetectedInArea ;
        asx:hasConditionSubjectReference "UUID-region-A" ;
        asx:isNegated true ] .            # maintain: no unresolved threat in region
```

`Maintain` reads correctly against the CONOPS: the condition ("no threat
detected in the region") is *kept* true; an intruder makes it false; assessment
and response restore it; commitment never ends. This is MDARS's "continuous
physical security" objective — unsayable in v0.0.1 or in core tasking.

## 2. Phase M1 — the standing watch

```turtle
:M1-StandingPatrol a asx:AutonomousPlanPhase ;
    c2sim:hasUUID "UUID-M1" ;
    c2sim:hasTaskReference "UUID-task-patrol-region-A" ;      # LOX PATROL verb
    c2sim:hasTaskReference "UUID-task-rf-inventory" ;          # core UseCapability
    lox:hasPlanPhaseTrigger [ a lox:OnOrderTrigger ;
        c2sim:hasTaskReference "UUID-task-execute-plan" ] ;
    lox:hasPlanPhaseCompletionCondition lox:OtherOrderReceived ;  # per module guidance
    asx:hasRepetitionPolicyCode asx:MaintainContinuously ;
    asx:hasGuardCondition [ a asx:Condition ;
        asx:hasConditionPredicateCode asx:CommsAvailable ;
        asx:hasConditionSubjectReference "UUID-mdars-1" ;
        asx:hasConditionObjectReference "UUID-host-console" ] ;
    asx:hasGoalReference "UUID-G1" .
```

- The patrol and inventory tasks ride together in one phase — MDARS does
  inventory *during* patrol, so no sequencing construct is needed. Covered.
- The comms guard reflects the host-architecture constraint (a platform out of
  contact is an exception, not routine).
- **[!] PM1 — no cadence slot.** MDARS patrols on a **revisit cadence**;
  cooperative-MCM (same corpus) revisits "every 8 h or 24 h".
  `MaintainContinuously` says *that* the behavior persists but not its
  **period**. Candidate v0.0.3 property: `hasRepetitionInterval` (→ `Duration`,
  max 1, meaningful under `MaintainContinuously` / `RepeatUntilCondition`).
  Without it, cadence rides in the task's own timing or in free text. **MED —
  two independent corpus scenarios demand it.**

## 3. Phase M2 — the exception path

```turtle
:M2-AssessChallenge a asx:AutonomousPlanPhase ;
    c2sim:hasUUID "UUID-M2" ;
    c2sim:hasTaskReference "UUID-task-assess-contact" ;
    c2sim:hasTaskReference "UUID-task-audio-challenge" ;
    lox:hasPlanPhaseTrigger [ a asx:CompositeTrigger ;
        asx:hasLogicalOperatorCode asx:AnySubTrigger ;         # exception = OR
        asx:hasSubTrigger [ a asx:StateConditionTrigger ;
            asx:hasCondition [ a asx:Condition ;
                asx:hasConditionPredicateCode asx:ThreatDetectedInArea ;
                asx:hasConditionSubjectReference "UUID-region-A" ] ] ;
        asx:hasSubTrigger [ a asx:StateConditionTrigger ;
            asx:hasCondition [ a asx:Condition ;
                asx:hasConditionPredicateCode asx:EntityHealthBelow ;   # PM2: "trapped" proxy
                asx:hasConditionSubjectReference "UUID-mdars-1" ;
                asx:hasThresholdValue 0.5 ] ] ;
        asx:hasSubTrigger [ a asx:StateConditionTrigger ;
            asx:hasCondition [ a asx:Condition ;
                asx:hasConditionPredicateCode asx:ThreatDetectedInArea ;  # PM3: "fire" as threat?
                asx:hasConditionSubjectReference "UUID-region-A" ;
                asx:hasConditionObjectReference "UUID-entitytype-fire" ] ] ] ;
    lox:hasPlanPhaseCompletionCondition lox:AllTasksComplete ;
    asx:hasRequiredAutonomyLevelCode asx:ReCont ;              # guard takes direct control
    asx:hasGoalReference "UUID-G1" .
```

- The ANY-composite over the three exceptional events (intruder / trapped /
  fire) is a clean fit — the extraction's ontology seed even models them as an
  explicit disjunction.
- **[!] PM2 — "robot trapped" has no predicate.** Immobilization is a mobility
  state, not health; `EntityHealthBelow` is a proxy that conflates battle damage
  with being wedged against a pallet. Candidate: `EntityImmobilized` (or widen
  a future platform-state predicate family). **MED.**
- **[!] PM3 — hazard typing rides on an object reference.** "Fire detected" is
  expressed as `ThreatDetectedInArea` filtered by an EntityType reference —
  legal, but the filter semantics ("object reference may name an EntityType")
  is only implied by the predicate comment. Same typing question the v0.0.1
  review logged as X4 (how is a detected hazard typed?). **LOW here**, but the
  module should state the filter convention explicitly when X4 resolves.

## 4. Guard intervention — preemption honestly examined

The CONOPS: the robot acts autonomously **until** the exception; then the guard
"intervenes from the console and directly interacts"; then "patrol resumes."

Known limitation §7.1 (no declarative cross-phase preemption) is exactly on
point here, so the walk tests whether MDARS actually needs it:

- M2's trigger firing does **not** declaratively suspend M1 — the module cannot
  say "M2 preempts M1." (Confirmed limitation.)
- But the **fielded CONOPS never asks for that**: on exception, the robot
  reports (deviation report below) and the *guard* takes over — which is the
  module's verb loop verbatim: `SuspendPlanExecution` (guard) → direct
  interaction / `OverrideAction` / teleoperation at `ReCont` autonomy →
  `ResumePlanExecution` → `MaintainContinuously` re-establishes the watch.
- **Verdict:** for human-on-the-loop exception handling, suspend/resume verbs
  substitute fully for declarative preemption. The limitation stands for
  robot-internal priority arbitration (no human in the loop), and should stay
  on the §7 list for that case — but MDARS does not break.

**The exception report the guard sees:**

```turtle
:DevIntruder a asx:PlanDeviationReportContent ;
    asx:hasDeviationTypeCode asx:FallbackActivated ;           # [Q] PM4 — fits poorly
    asx:hasDeviationCondition [ a asx:Condition ;
        asx:hasConditionPredicateCode asx:ThreatDetectedInArea ;
        asx:hasConditionSubjectReference "UUID-region-A" ] ;
    lox:hasPlanPhaseReference "UUID-M1" ;
    asx:hasRationaleText "Motion + IR contact at warehouse 7 NE corner; commencing audio challenge; awaiting console." ;
    smx:hasConfidenceLevel 0.9 .
```

- **[Q] PM4 — is an exception a "deviation"?** M2 activating is the plan working
  as designed, not a deviation from it; `FallbackActivated` (used above) is
  wrong in spirit, and `PlanExecutionStatusContent` carries state but not the
  alerting condition. DroneResponse walk PD1 proposed `BehaviorAdjusted`; the
  MDARS case suggests the real need is one step more general — an
  **exception/alert report value** (e.g. `ExceptionRaised`) for
  plan-anticipated events that demand human attention. **MED** — merges with
  PD1 into one v0.0.3 decision about the `DeviationTypeCode` list's scope.

## 5. What one guard : 255 platforms means here

Organizational span, not plan semantics: each platform holds its own plan and
reports; the console aggregates. The module deliberately has no aggregation
construct (§7.3, the Remmersmann roll-up gap) — MDARS confirms the *need* is
real at console scale but also that per-platform plans remain individually
well-formed without it. No new finding; evidence for §7.3's priority.

## Findings summary

| ID | Sev | Verdict | One-line |
|---|---|---|---|
| PM1 | MED | gap | No cadence/period on repetition policies; propose `hasRepetitionInterval` (MDARS + MCM both demand it). |
| PM2 | MED | gap | No immobilized/mobility-state predicate; `EntityHealthBelow` conflates damage with entrapment. |
| PM3 | LOW | convention | EntityType-filter semantics of `hasConditionObjectReference` must be stated (ties to v0.0.1 X4). |
| PM4 | MED | scope question | Plan-anticipated exceptions are not "deviations"; `DeviationTypeCode` needs an alert value or a sibling report type (merge with PD1). |
| — | — | confirmed limit, tolerable | No declarative preemption (§7.1) — suspend/resume verbs cover the human-on-the-loop case; limitation stands for robot-internal arbitration only. |
| — | — | covered | Maintain-goal as data; MaintainContinuously standing watch; ANY-composite exception triggers; per-phase autonomy drop (`ReCont`) on the response phase; comms guard; resume-after-intervention. |

**Net:** the module expresses the fielded CONOPS end-to-end, including the part
classic tasking cannot say at all (the never-finished watch). The walk's real
catches: no cadence slot (PM1) and the deviation/exception scope question (PM4)
— both cheap, both evidenced twice in the corpus.
