# Task/Effect Batch Walk: Logistics, Engineering, USV Rescue

Purpose: cover three more task/effect scenarios in one pass to test what
autonomous systems *do* beyond movement and sensing - carry-and-deliver,
physically manipulate, and recover. Batched because they share a shape: the
gaps are task verbs and payload/effector typing, not entity structure.

Layout mirrors the workbook columns:
`Model | C2SIM Object | Parent Type | Field | Type | Value | Notes`.
**[Q]** = open question, **[!]** = gap/defect. Proposals only; nothing applied.

Grounding done first (and it narrowed the findings):
- Logistics: no cargo/payload/manifest/delivery class, but `Resource` /
  `ResourceObservation` and quantity properties (`hasOnHandQuantity` etc.)
  **exist** - so supplies are partly modelable; manifest + delivery are gaps.
- Engineering: **nothing** for manipulation / effector / excavate / clear /
  emplace / construct - no physical-manipulation task verbs exist.
- Maritime: `SurfaceVessel` / `SubsurfaceVessel` **exist** (SMX) - USV typing is
  the same P1 conflict; no recover / rescue / tow task verb exists.
- `DesiredEffectCode`, `hasAffectedEntity`, `Person` all exist and are reused.

## 1. Logistics - Delivery Order + Confirmation

### Logistics Delivery Order (Order)

| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| C2SIM | OrderBody | DomainMessageBody | isToReceiver | UUIDBase | (transport UGV UUID) | |
| C2SIM / ASX | Deliver Task | Task | hasTask | TaskActionCode | Transport / Deliver | [Q] confirm a transport/deliver TaskActionCode exists. |
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
| C2SIM / ASX | Engineering Task | Task | hasTask | TaskActionCode | Excavate / Clear / Emplace | [!] E1: no manipulation/effector task verbs (dig / clear / breach / construct) in the standard. |
| C2SIM | (task) | Task | hasAffectedEntity | UUIDBase | (obstacle / site) | Partial - target of manipulation via hasAffectedEntity. |
| C2SIM | (task) | Task | hasDesiredEffectCode | DesiredEffectCode | (site cleared) | Partial - effect code exists. |
| ASX | effector | Equipment / Payload | (manipulator) | ??? | dozer blade / excavator / arm | [!] E2: no effector/manipulator equipment concept. Ties to P2/D3. |
| C2SIM | (obstacle) | ? | hasEntityType | EntityType | Obstacle / Rubble | [Q] X4: obstacle typing (same as CASEVAC). |

## 3. USV Downed-Pilot Rescue (Order)

| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| C2SIM | OrderBody | DomainMessageBody | isToReceiver | UUIDBase | (USV UUID) | [!] R1/P1: USV is an SMX `SurfaceVessel` vs ASX `USV subClassOf Robot` - the P1 conflict, now maritime. |
| SMX | USV | SurfaceVessel (SMX) | hasEntityType | EntityType | USV | Maritime platform type exists (`SurfaceVessel`) - reuse vs the ASX Robot tree. |
| C2SIM / ASX | Rescue Task | Task | hasTask | TaskActionCode | Recover / Rescue | [!] R2: no recovery / rescue / tow / salvage task verb in the standard. |
| C2SIM | (task) | Task | hasAffectedEntity | UUIDBase | (downed pilot) | Rescue subject; `Person` entity exists. |
| C2SIM | (task) | Task | hasLocation | Location | (last-known position) | Works. |

---

## Findings summary

| ID | Sev | Status | One-line |
|---|---|---|---|
| L1 | MED | gap | No cargo/payload manifest (what a platform carries); Resource + quantities exist, "load carried" does not. |
| L2 | MED | gap | No delivery-confirmation ReportContent (what delivered, received by whom). |
| E1 | HIGH | gap | No manipulation/effector task verbs (dig, clear, breach, construct). |
| E2 | MED | gap | No effector/manipulator equipment concept (arm, blade, excavator). |
| R1 | - | reconfirms P1 | USV typing conflict (SMX SurfaceVessel vs ASX USV/Robot), now maritime. |
| R2 | MED | gap | No recovery/rescue/tow task verb. |

Partially covered / reused (checked): `Resource` + quantities,
`ResourceObservation`, `DesiredEffectCode`, `hasAffectedEntity`, `Person`,
`SurfaceVessel`/`SubsurfaceVessel`.

## Headline: the task/effect axis has one recurring shape

Across engagement (Fire Support), delivery, manipulation, and rescue, the same
two things are missing and nothing else is:
1. **Task verbs** for what autonomous systems do - deliver, dig/clear/emplace,
   recover/rescue (engage is uncertain). The standard has generic
   `DesiredEffectCode` and `hasAffectedEntity`, but not the action vocabulary.
2. **Payload / effector / weapon typing** - cargo (L1), manipulators (E2), and
   weapons (W2) are all the same gap: no typed thing-carried-or-wielded.
Entity structure (P1), addressing, effects, targets, and resources are already
there. This distills the whole task/effect axis into one decision (Q-L).
