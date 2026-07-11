# CASEVAC Message Walk (proposed coverage)

Purpose: walk the CASEVAC contributed scenario end-to-end into concrete
messages, to test the proposed ASX elements against the scenario the group
actually authored. CASEVAC has no message instantiations yet, and it demands
patterns the current UAV-video examples do not exercise (robot-to-robot
coordination, explainability, autonomous replanning).

Layout mirrors the workbook scenario-sheet columns:
`Model | C2SIM Object | Parent Type | Field | Type | Value | Notes`.
**[Q]** = open question, **[!]** = suspected defect/gap. Findings anchored to
`Ontology/C2SIM.rdf`, `C2SIM_SMX.rdf`, `C2SIM_LOX.rdf`. This is review input,
not a decision.

Grounding done before writing (to avoid inventing gaps that do not exist):
- `Route` **already exists** (SMX) - so the gap is that the Order sheet used
  free text, not that a route type is missing.
- `PlanBody` / `PlanPhase` / `PlanPhaseTrigger` / `PlanPhaseCompletionCondition`
  exist - phased CASEVAC tasks and ETA likely map here, not to new ASX classes.
- `ReportContent` subclasses are only `ObservationReportContent`,
  `PositionReportContent`, `TaskStatus` - so status/position reporting is
  covered, but there is **no rationale/explanation** content type.

## Scenario recap (from ContributedScenarios/CASEVAC.md)

Two coordinating UGVs: a **scout** UGV and a **medical-transport** UGV. Scout
plans a route to the evacuation point, drives it to verify safety, replans on
encountering an obstacle (broken bridge) or threat (suspected IED), then
publishes the safe route to the transport UGV, which carries the casualty. A
soldier stays "on the loop," sending mission updates and receiving updates,
including "explainable reasons" for changes.

## Message set CASEVAC requires

| # | Message | Direction | Status in repo |
|---|---|---|---|
| 1 | Initialization | scenario setup | none |
| 2 | CASEVAC tasking Order | soldier -> team | none |
| 3 | Safe-route advertisement | scout -> transport (robot to robot) | **no pattern** |
| 4 | Status / position Report | scout -> soldier (HOTL) | base-covered |
| 5 | Threat/obstacle Report driving replan | scout -> soldier | partial |
| 6 | "Explainable reasons" Report | team -> soldier | **no element** |

---

## 1. Initialization

| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| SMX or ASX | Vehicle or UGV | Platform / Robot | hasEntityType | EntityType | "UGV-Scout" | [!] P1: SMX `Vehicle subClassOf Platform` vs ASX `UGV subClassOf Robot` - same conflict as UAV. |
| SMX or ASX | Vehicle or UGV | Platform / Robot | hasEntityType | EntityType | "UGV-Transport" | Second UGV; carries casualty. |
| C2SIM | soldier / C2 unit | ActorEntity (Unit) | hasName | string | "HOTL-Soldier" | On-the-loop tasker. |
| SMX | Route | (SMX) | hasName | string | "CASEVAC-Route-0" | [!] X3: use the existing SMX `Route` class, not free text. |
| C2SIM | CollectionPoint | MapGraphic (PhysicalEntity) | (geometry) | - | - | Casualty pickup. |
| C2SIM | EvacPoint | MapGraphic (PhysicalEntity) | (geometry) | - | - | Medical evacuation point. |
| ASX | scout sensors | Sensor / Equipment | SensorCapability | enum | (obstacle/threat sensing) | [!] P2: sensor typing unresolved; scout needs hazard-detection sensing. |
| ASX | (both UGVs) | ? | ControlMode / autonomy | enum/Code | Unpiloted-Autonomous | [!] D1/P6: three autonomy vocabularies. |

## 2. CASEVAC tasking Order (soldier -> team)

| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| C2SIM | OrderBody | DomainMessageBody | isFromSender | UUIDBase | (soldier UUID) | |
| C2SIM | OrderBody | DomainMessageBody | isToReceiver | UUIDBase | (team/UGV UUID) | |
| C2SIM/ASX | CASEVAC Task | Task | hasTask | TaskActionCode | "Evacuate" | [Q] X6: is CASEVAC a base TaskActionCode or a new ASX task? |
| C2SIM | (task) | Task | hasLocation | Location | (CollectionPoint) | Where casualties are. |
| SMX | (task) | Task | (route ref) | Route | (CASEVAC-Route-0) | Reference existing Route. |
| C2SIM | PlanBody | DomainMessageBody | hasPlanPhase | PlanPhase | (phased mission) | [Q] X5: model phased CASEVAC via base PlanBody/PlanPhase rather than new ASX elements. |

## 3. Safe-route advertisement (scout UGV -> transport UGV) -- ROBOT TO ROBOT

| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| C2SIM | (some body) | DomainMessageBody | isFromSender | UUIDBase | (scout UUID) | Envelope addressing supports peer-to-peer. |
| C2SIM | (some body) | DomainMessageBody | isToReceiver | UUIDBase | (transport UUID) | |
| SMX | Route | (SMX) | (verified safe route) | Route | (CASEVAC-Route-1) | [!] X1: no content type/body for a robot *advertising* a computed safe Route to a peer. Not a C2 Order; not a standard Report. |

Findings:
- **X1 [!] No robot-to-robot coordination content.** The envelope *addressing*
  (`isFromSender`/`isToReceiver` as UUIDBase) already allows peer messages, but
  there is no `ReportContent`/`OrderBody` content type for "here is a verified
  safe route, use it." Also unresolved: can a UGV be an order-*issuing*
  authority, or is this a Report the transport subscribes to? **[Q]**
- **X3 [!] Route sharing needs a payload wrapper.** `Route` exists, but nothing
  wraps a Route as shareable message content (the UAV Order sheet sidestepped
  this with free-text "New Route Pattern").

## 4. Status / position Report (scout -> soldier)

| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| C2SIM | ReportBody | DomainMessageBody | hasReportContent | PositionReportContent | (scout position) | Base-covered - `PositionReportContent` exists (C2SIM). |

Finding: this one is **covered by the base standard** - no new ASX element
needed. (Recorded so the walk does not overstate the gap.)

## 5. Threat / obstacle Report driving replan (scout -> soldier)

| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| SMX | ObservationReportContent | ReportContent | hasObservation | Observation | (suspected IED / broken bridge) | [!] X4: no obstacle/threat observation subtype; would fall to `ActivityObservation` or a new type. |
| C2SIM | (observed hazard) | ? | hasEntityType | EntityType | "IED" / "Obstacle" | [Q] X4: how is a detected hazard that triggers autonomous replanning typed? |

## 6. "Explainable reasons" Report (team -> soldier) -- HEADLINE GAP

| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| ASX? | (rationale) | ReportContent? | why route changed | ??? | (free text / structured?) | [!] X2 BLOCKER-for-scenario: no rationale/explanation ReportContent exists. |
| C2SIM | TaskStatus | ReportContent | task outcome | TaskStatus | "Incomplete" | Can say *that* it failed, not *why*. |

Finding:
- **X2 [!] No explainability element.** CASEVAC step 8 requires the team to send
  "explainable reasons" - why it changed route, why it could not complete, ETA
  for phased tasks. `ReportContent` offers only observation, position, and
  `TaskStatus`. `TaskStatus` reports the *state*, not the *rationale*. This is a
  first-class scenario requirement with **no proposed element** - a strong
  candidate for a new ASX `RationaleReportContent` (or similar). **[Q]**

---

## Findings summary

| ID | Sev | True gap or covered? | One-line |
|---|---|---|---|
| X1 | HIGH | gap (content, not addressing) | No robot-to-robot content type for advertising a safe route; UGV-as-issuer authority unclear. |
| X2 | HIGH | **gap** | No rationale/explanation ReportContent; CASEVAC "explainable reasons" cannot be expressed. |
| X3 | MED | partial | `Route` exists but no payload wrapper to share it; ASX Order sheet used free text. |
| X4 | MED | partial | No obstacle/threat observation subtype for hazards that trigger replanning. |
| X5 | LOW | mostly covered | Phased tasks/ETA likely map to base `PlanBody`/`PlanPhase`; ETA attribute is the open bit. |
| X6 | LOW | question | Is CASEVAC a base `TaskActionCode` or a new ASX task; re-tasking mid-mission semantics. |
| P1 | BLOCKER | gap | UGV double-typed (SMX Vehicle vs ASX UGV/Robot) - same as UAV. |
| P2 | BLOCKER | gap | Scout sensor typing unresolved. |

The two findings unique to CASEVAC and not seen in the UAV/Init walks are
**X1 (robot-to-robot coordination)** and **X2 (explainability)**. Both are
explicit requirements in the contributed scenario, and neither has any proposed
element today - they are the highest-value additions CASEVAC surfaces.

What CASEVAC did **not** break (checked, and covered by the base standard):
position/status reporting (`PositionReportContent`), routes (`Route`), and
phased planning (`PlanBody`/`PlanPhase`).
