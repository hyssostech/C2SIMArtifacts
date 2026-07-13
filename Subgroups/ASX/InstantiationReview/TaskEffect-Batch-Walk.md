# Task/Effect Batch Walk: Logistics, Engineering, USV Rescue

Purpose: cover three more task/effect scenarios in one pass to test what
autonomous systems *do* beyond movement and sensing - carry-and-deliver,
physically manipulate, and recover. Batched because they share a shape: the
gaps are task verbs and payload/effector typing, not entity structure.

Layout mirrors the workbook columns:
`Model | C2SIM Object | Parent Type | Field | Type | Value | Notes`.
**[Q]** = open question, **[!]** = not-yet-defined item / gap. Proposals only; nothing applied.

Grounding done first (and it narrowed the findings a lot). LOX carries 446
`TaskActionCode` verbs, so almost every action verb already exists - the gaps
are about *typed things carried/wielded* and a few autonomy-specific semantics,
not verbs:
- Logistics: delivery/transport verbs **exist** (`TRANS` Transport, `RESUPL`
  Resupply, `LIFT`, `ARDROP`); `Resource` / `ResourceObservation` / quantities
  exist too. The gaps are the cargo *manifest* and a delivery-confirmation
  report, not the verb.
- Engineering: the verbs **exist** too - `CONSTR` (build/dig/create), `CLROBS`
  (clear obstacle), `CLRLND` (clear land), `MINLAY` (emplace), `BREACH`. The gap
  is the effector/manipulator *equipment* concept (E2), not the action verb.
- Maritime: `SurfaceVessel` / `SubsurfaceVessel` **exist** (SMX) - USV typing is
  the same P1 conflict; `lox#RESCUE` and `lox#RECOVR` **exist**, so only a
  general-purpose tow/salvage verb is absent (closest: `lox#TOWTGT`, scoped to
  gunnery targets; the broadly-defined `RECOVR` may already cover salvage).
- `DesiredEffectCode`, `hasAffectedEntity`, `Person` all exist and are reused.

## 1. Logistics - Delivery Order + Confirmation

### Logistics Delivery Order (Order)

| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| C2SIM | OrderBody | DomainMessageBody | isToReceiver | UUIDBase | (transport UGV UUID) | |
| C2SIM / ASX | Deliver Task | Task | hasTask | TaskActionCode | TRANS / RESUPL | Works - `TRANS` (Transport) and `RESUPL` (Resupply) exist in LOX. |
| C2SIM | (task) | Task | hasLocation | Location | (FOB destination) | Works. |
| SMX | (cargo) | Resource / Equipment | (manifest) | ??? | Ammunition, Water, Medical | [!] L1: no cargo/payload manifest (what a platform carries). Resource exists but not "load carried"; ConceptMapping Payload absent from OWL. |
| SMX | (cargo item) | Resource | hasOnHandQuantity | quantity | 500 rounds | Partial - resource quantities exist. |
| SMX or ASX | Vehicle or UGV | Platform / Robot | hasEntityType | EntityType | UGV-Transport | [!] P1 (again): SMX Vehicle vs ASX UGV/Robot. |

### Delivery Confirmation Report (Report)

| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| C2SIM | ReportBody | DomainMessageBody | hasReportContent | ??? | (delivery confirmation) | [!] L2: no delivery-confirmation ReportContent - what was delivered, and received by whom. |
| C2SIM | TaskStatus | ReportContent | task outcome | TaskStatus | Complete | Says the task ran, not what/how much was delivered or who received it. |
| SMX | (received) | ResourceObservation | hasObservation | Observation | (received: 500 rounds) | Partial - `ResourceObservation` can report resources; handover/receipt semantics unclear. |

## 2. Engineering - Manipulation Task (Order)

| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| C2SIM | OrderBody | DomainMessageBody | isToReceiver | UUIDBase | (engineer UGV UUID) | |
| C2SIM / ASX | Engineering Task | Task | hasTask | TaskActionCode | CONSTR / CLROBS / MINLAY | E1: use existing LOX verbs (`CONSTR` build/dig, `CLROBS` clear, `MINLAY` emplace, `BREACH`); the gap is effector typing (E2), not the verb. |
| C2SIM | (task) | Task | hasAffectedEntity | UUIDBase | (obstacle / site) | Partial - target of manipulation via hasAffectedEntity. |
| C2SIM | (task) | Task | hasDesiredEffectCode | DesiredEffectCode | (site cleared) | Partial - effect code exists. |
| ASX | effector | Equipment / Payload | (manipulator) | ??? | dozer blade / excavator / arm | [!] E2: no effector/manipulator equipment concept. Ties to P2/D3. |
| C2SIM | (obstacle) | ? | hasEntityType | EntityType | Obstacle / Rubble | [Q] X4: obstacle typing (same as CASEVAC). |

## 3. USV Downed-Pilot Rescue (Order)

| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| C2SIM | OrderBody | DomainMessageBody | isToReceiver | UUIDBase | (USV UUID) | [!] R1/P1: USV is an SMX `SurfaceVessel` vs ASX `USV subClassOf Robot` - the P1 conflict, now maritime. |
| SMX | USV | SurfaceVessel (SMX) | hasEntityType | EntityType | USV | Maritime platform type exists (`SurfaceVessel`) - reuse vs the ASX Robot tree. |
| C2SIM / ASX | Rescue Task | Task | hasTask | TaskActionCode | Recover / Rescue | R2: use `lox#RESCUE` or `lox#RECOVR` (both exist); only a general-purpose tow/salvage verb is absent (closest: `TOWTGT`, gunnery targets only). |
| C2SIM | (task) | Task | hasAffectedEntity | UUIDBase | (downed pilot) | Rescue subject; `Person` entity exists. |
| C2SIM | (task) | Task | hasLocation | Location | (last-known position) | Works. |

---

## Findings summary

| ID | Sev | Status | One-line |
|---|---|---|---|
| L1 | MED | gap | No cargo/payload manifest (what a platform carries); Resource + quantities exist, "load carried" does not. |
| L2 | MED | gap | No delivery-confirmation ReportContent (what delivered, received by whom). |
| E1 | LOW | mostly covered | Engineering verbs exist in LOX (`CONSTR`, `CLROBS`, `CLRLND`, `MINLAY`, `BREACH`); folds into E2 (effector typing). |
| E2 | MED | gap | No effector/manipulator equipment concept (arm, blade, excavator). |
| R1 | - | reconfirms P1 | USV typing conflict (SMX SurfaceVessel vs ASX USV/Robot), now maritime. |
| R2 | LOW | minor gap | `lox#RESCUE` and `lox#RECOVR` exist; only a general-purpose tow/salvage verb is absent (`TOWTGT` is gunnery-target towing only; `RECOVR` may already cover salvage). |

Partially covered / reused (checked): `Resource` + quantities,
`ResourceObservation`, `DesiredEffectCode`, `hasAffectedEntity`, `Person`,
`SurfaceVessel`/`SubsurfaceVessel`.

## Headline: the task/effect axis has one recurring shape

Across engagement, delivery, manipulation, rescue, search, and escort, LOX
already carries the action vocabulary - 446 `TaskActionCode` verbs, including
`ENGAGE`, `ATTACK`, `BREACH`, `CONSTR`, `CLROBS`, `MINLAY`, `TRANS`, `RESUPL`,
`RESCUE`, `RECOVR`, `NTRCOM`/`NTREXP` (neutralize), `ESCRT`, `FOLASS`, `RECCE`,
`PATROL`, `SWEEP`, `DECEIV`/`DAZZLE`. So the task/effect axis is **not** a
missing-verb problem. The genuine ASX gaps are:
1. **Payload / effector / weapon typing** - cargo (L1), manipulators (E2), and
   weapons (W2) are the same gap: no typed thing-carried-or-wielded.
2. **A few autonomy-specific semantics** - an area-coverage / exploration
   *goal* (explore-until-covered, tied to N1), and a general-purpose tow/salvage; plus
   the autonomy-to-engagement-authority link (W1).
Entity structure (P1), addressing, effects, targets, resources, and the whole
task-verb vocabulary are already there. The residual task/effect work is the
payload/effector/weapon typing (Q-L), not the verbs.
