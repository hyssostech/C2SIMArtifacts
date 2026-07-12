# Plan-Semantics Validation Walks

Validation of the ASX plan-semantics module (`../ASX-PlanSemantics-Draft.ttl`,
v0.0.2) against three scenarios, in the InstantiationReview walk format:
instantiate each scenario end-to-end in the module vocabulary, record what fits,
what does not, and what convention is missing. All Turtle instance blocks in the
walks parse against the module (checked with rdflib). These walks are review
input for the subgroup — findings below are **proposed v0.0.3 deltas**, not
applied changes.

| Walk | Scenario | Why chosen |
|---|---|---|
| [CASEVAC-PlanWalk.md](./CASEVAC-PlanWalk.md) | Contributed CASEVAC (Hyssos) | the group's own scenario; re-checks v0.0.1 findings X1–X6 against the module |
| [DroneResponse-PlanWalk.md](./DroneResponse-PlanWalk.md) | Agrawal et al. 2021 (arXiv:2109.02077) | the sourced explainability scenario the module's report schema adapts — its most direct accountability test |
| [MDARS-PlanWalk.md](./MDARS-PlanWalk.md) | DTIC ADA422465 (fielded Army program) | the standing-watch case classic tasking cannot express at all |

## Outcome in one paragraph

All three scenarios instantiate end-to-end. The constructs that motivated the
module carry their weight: goals as data (achieve and maintain), fallback chains
with `OnPhaseFailureTrigger`, composite triggers (ALL with latch/hold semantics
at the CASEVAC departure gate; ANY over the MDARS exception set), loop
termination split from per-iteration completion (DroneResponse search),
per-phase autonomy levels, and the deviation/rationale reports. The walks
surfaced **no structural defects** — every finding is a vocabulary or
convention delta, which is what a validation pass at this stage should produce.

## Cross-walk findings — proposed v0.0.3 deltas

| # | From | Sev | Proposed delta |
|---|---|---|---|
| 1 | PD1 + PM4 | MED | Rescope the deviation/alert vocabulary: add `BehaviorAdjusted` (operating-parameter change) and decide whether plan-anticipated exceptions get an `ExceptionRaised` value or a sibling alert report type. One decision, two walks demand it. |
| 2 | PM1 | MED | `hasRepetitionInterval` (→ Duration) on repetition policies — revisit cadence; demanded independently by MDARS and cooperative MCM. |
| 3 | PC1 | MED | `PayloadOnBoard` predicate (embarkation state); `EntityWithinRange` is a false proxy for "casualty loaded." |
| 4 | PD2 | MED | `RemainingEnduranceBelow` predicate (battery/endurance); `EntityHealthBelow` conflates damage with depletion. |
| 5 | PM2 | MED | `EntityImmobilized` predicate (mobility state); health is the wrong axis for "trapped." |
| 6 | PC2 | LOW | State the late-bound product convention normatively (pre-allocated UUIDs for runtime-produced objects, e.g. rule R15). |
| 7 | PD4 | LOW–MED | Optional `hasActionTakenReference` on the deviation report, or state that action-taken rides in rationale text. |
| 8 | PD3 | LOW | Name the escalation pattern (hold + deviation report + `OtherOrderReceived`) for request-human-assistance chain ends. |
| 9 | PM3 | LOW | State the EntityType-filter semantics of `hasConditionObjectReference` (ties to v0.0.1 finding X4). |

Inherited (not module findings): the robot-to-robot route-advertisement
*message* (v0.0.1 X1/X3) is still the missing piece for CASEVAC — the plan side
is ready for it (PC3).

Confirmed §7 limitations, with new evidence: no declarative cross-phase
preemption (§7.1 — but MDARS shows suspend/resume verbs fully cover the
human-on-the-loop case); no belief-correction act (§7.8 — the DroneResponse
ball-track case is real); no report roll-up (§7.3 — MDARS console scale
confirms the need).

## Method note

Each walk pre-grounds against the module and the base ontologies before
claiming a gap (the InstantiationReview discipline: do not invent gaps that do
not exist), records covered items explicitly so the walk cannot overstate, and
ends with a findings table. Turtle blocks use the module's prefixes and were
parsed together with the module file plus `CSIM_ASX.rdf` v0.0.1 (source of the
`Teleop`/`ReCont`/`Automated`/`FullAuto` autonomy individuals the walks cite as
`AutonomyLevelCode` values, per the module's planned re-typing).
