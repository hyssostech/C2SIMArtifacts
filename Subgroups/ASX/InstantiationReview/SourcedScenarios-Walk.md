# Sourced-Scenarios Walk: MCM, SubT, Sustainment

These three scenarios came from the parallel **scenario-sourcing session**
(`LLMExperiments/PaperSummaries/V2Extractions/`), which explicitly handed them
off to this review in `LLMExperiments/OntologyConceptCoverage.md`. This walk
instantiates the two new-domain threads (maritime MCM, subterranean SubT) and
validates Logistics against Sustainment, then reconciles everything with the
prior findings.

Layout mirrors the workbook columns:
`Model | C2SIM Object | Parent Type | Field | Type | Value | Notes`.
**[Q]** = open question, **[!]** = gap, **[+]** = corroborates a prior finding.
Proposals only; nothing applied.

Grounding recap (checked before writing):
- Exists / reused: `SurfaceVessel`, `SubsurfaceVessel` (SMX); `CommunicationNetwork`,
  `RelativeLocation`; `HostilityStatusCode` (neutral value `smx#NEUTRL`;
  `smx#ANT` = assumed-neutral) and an untyped `NeutralSide` individual;
  `hasConfidenceLevel`; `SubjectTypeObservation`; `DesiredEffectCode`.
- Absent: any search / explore / coverage task; decoy / deception; MoE /
  effectiveness attribute; track / cue / contact class.

---

## A. Cooperative MCM (maritime, undersea) - Ling 2020

Detector USV finds and classifies a naval mine, hands the classified track to a
neutralizer USV, which neutralizes it without re-detecting. Neutral commercial
traffic transits throughout.

### MCM Init
| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| SMX or ASX | SurfaceVessel or USV | Platform / Robot | hasEntityType | EntityType | Detector-USV | [+/!] P1 (maritime): SMX `SurfaceVessel` vs ASX `USV`/Robot. |
| ASX | Detector-USV | ? | role subtype | ??? | detector (TSAS) | [!] G5: no platform role/locomotion subtype (detector vs neutralizer vs CUSV). Extends P1. |
| SMX | commercial vessel | ActorEntity | hasHostilityStatusCode | HostilityStatusCode | smx#NEUTRL (Neutral) | [+] neutral affiliation exists (`smx#NEUTRL` hostility value; `smx#ANT` = assumed-neutral); [!] G10: but "neutral traffic constrains the search path" (behavioral constraint) is not modeled. |
| SMX | sea line of communication | TacticalArea / MapGraphic | (operating area) | - | - | Reuse area object; ties to N1 (area as subject). |

### MCM Cross-Cue & Neutralize Order (autonomy-to-autonomy)
| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| C2SIM | OrderBody | DomainMessageBody | isFromSender | UUIDBase | (detector USV) | [+] X1: robot-to-robot - detector tasks neutralizer. |
| C2SIM | OrderBody | DomainMessageBody | isToReceiver | UUIDBase | (neutralizer USV) | |
| ASX | classified contact | ??? | (shared track) | ??? | moored mine @ posn, class=high | [!] G3: no track/contact object to share a classified detection; reuses M1 (inline entity def) + X1 but has no "track" type. |
| C2SIM / ASX | Neutralize Task | Task | hasTask | TaskActionCode | NTRCOM / NTREXP | `NTRCOM` / `NTREXP` / `NTRCHM` (neutralize) exist in LOX. |
| SMX | naval mine | SubjectTypeObservation | observed type | SubjectType | Moored / Bottom mine | [+] identity via SubjectTypeObservation (like GPR); no mine class. |

### Naval Mine Detection Report
| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| SMX | ObservationReportContent | ReportContent | hasObservation | Observation | (classified mine) | [!] Y-series: another per-sensor detection report - motivates the generic one (G4, below). |
| SMX | (detection) | Observation | hasConfidenceLevel | double | 0.9 | Works. |
| ASX | (MoE) | ? | pct neutralized / active time | ??? | 85% / 6 h | [!] G7: no measure-of-effectiveness attribute for campaign reporting. |

## B. SubT subterranean multi-robot - Roucek 2019

A heterogeneous team (wheeled/tracked/legged UGV + quadrotors) explores a
GPS-denied, comms-limited underground space, deploys relays, and reports
arbitrary artifacts with an error bound. No adversary.

### SubT Team Init
| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| SMX or ASX | Vehicle or UGV | Platform / Robot | hasEntityType | EntityType | Wheeled / Tracked / Legged UGV | [!] G5: no locomotion subtype axis (wheeled/tracked/legged). Extends P1. |
| ASX | comms relay | Equipment / Entity | deployable relay | ??? | relay node | [!] G1: a relay task verb `lox#COMREL` exists, but a droppable relay ENTITY/node is not modeled (`CommunicationNetwork` is a network, not a node). |
| C2SIM | (mission) | - | force sides | - | (none hostile) | [+] G10: a mission with no hostile ForceSide - allowed (just omit), but the model tends to assume a hostile side. |

### Explore / Search Area Order
| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| C2SIM | OrderBody | DomainMessageBody | isToReceiver | UUIDBase | (robot team) | |
| C2SIM / ASX | Explore Task | Task | hasTask | TaskActionCode | RECCE / RECONS / PATROL | G2: search/recce/patrol verbs exist (`RECCE`, `RECONS`, `PATROL`, `SWEEP`, `DETECT`); the gap is an area-coverage *goal* (explore-until-covered), tied to N1. |
| SMX | search area | TacticalArea | (coverage goal) | ??? | Cave sector A | [!] N1 + G2: task an area with a coverage goal - no hasAffectedArea, no coverage-goal attribute. |
| ASX | (comms) | ? | operating mode | ??? | denied-comms / relay-linked | [!] G1: no comms-degraded operating mode. |

### Generic Detection Report (proposed consolidation - resolves Y-series)
| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| SMX | ObservationReportContent | ReportContent | hasObservation | Observation | (detected object) | [+] G4: this ONE parameterized report subsumes Video / CBRN / EW / GPR / naval-mine / artifact. |
| SMX | (detection) | SubjectTypeObservation | detected type | SubjectType | backpack / survivor / mine | Object identity. |
| SMX | (detection) | Observation | hasConfidenceLevel | double | 0.8 | Works. |
| ASX | (detection) | ? | error bound / uncertainty | ??? | +/- 1.5 m | [!] G4/Y5: position error-bound has no attribute. |
| ASX | (detection) | ? | modality + false-positive | ??? | lidar-vision; FP=false | [!] G4: sensor modality + false-positive flag - unify with Q-I sensor-reading. |

## C. Sustainment / ULTRA (land) - Dibernardo 2026 (validation)

Largely **validates** the existing Logistics tabs (`Logistics Delivery Order`,
`Delivery Confirmation Report`, `UGV Retrieve & Transport`) against a real field
vignette - no new message thread needed. Two net-new items:

### Contested Resupply Order
| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| C2SIM | OrderBody | DomainMessageBody | isToReceiver | UUIDBase | (resupply UGV) | |
| C2SIM / ASX | Deliver Task | Task | hasTask | TaskActionCode | Deliver | Validated against real vignette (L-series). |
| ASX | (2nd platform) | ? | decoy behavior | ??? | act as decoy | G8: deception verbs exist (`DECEIV`, `DAZZLE`); a distinct decoy behavior/role is the residual. |
| ASX | (order) | ? | threat-aware attrs | ??? | route-under-threat; low-signature | [!] G9: no risk/threat annotation or level-of-autonomy on a logistics order. |

---

## Reconciliation with prior findings

**Corroborated (independent confirmation from new domains):**
- **X1** (robot-to-robot) <- MCM detector->neutralizer cross-cueing.
- **N2** (persistent tasking) <- MCM 8h/24h revisit cycle.
- **P1** (platform typing) <- SubT/MCM; and *extended* with a locomotion/role
  subtype axis (G5).
- **Y-series** (sensor reports don't generalize) <- SubT/MCM detection reports;
  and *answered* by the generic Detection Report (G4).

**New findings this batch adds:**

| ID | Sev | One-line |
|---|---|---|
| G1 | MED | Denied-comms operating MODE + a deployable relay ENTITY/node (SubT); the relay verb `lox#COMREL` already exists. |
| G2 | MED | Area-coverage / exploration *goal* (explore-until-covered) - search/recce verbs (`RECCE`, `PATROL`, `SWEEP`) exist; the coverage-goal semantics + N1 area subject do not. |
| G3 | MED | Cross-cueing: system-to-system tasking with a shared classified track/contact object (MCM); reuses X1 + M1, but no Track type. |
| G4 | HIGH | Generic parameterized Detection Report (confidence + error-bound + false-positive + modality) subsuming the per-sensor reports - resolves Y1/M3/M4. |
| G5 | MED | Platform locomotion/role subtypes (wheeled/tracked/legged UGV; detector/neutralizer USV) - extends P1. |
| G6 | LOW | Maritime depth: naval mine (moored/bottom) via SubjectTypeObservation, UUV=SubsurfaceVessel, sea-lane area - mostly reuse. |
| G7 | LOW | Measure-of-effectiveness attributes on reports (% neutralized, active time). |
| G8 | LOW | Decoy as a distinct behavior/role - deception verbs (`DECEIV`, `DAZZLE`) exist; a decoy role is the residual. |
| G9 | MED | Threat-aware / contested-delivery order annotations (Sustainment). |
| G10 | LOW | Neutral-actor framing is MOSTLY COVERED (`smx#NEUTRL` hostility value; `NeutralSide` is an untyped stub); residual = neutral-as-constraint + no-adversary missions. |

## Headline

The sourcing session's two new domains (maritime, subterranean) confirm the
entity-typing (P1) and coordination (X1) findings from a fresh angle, and add a
an area-coverage/exploration goal (G2), denied-comms mode + relay entity (G1),
cross-cueing with a shared track (G3), a decoy role (G8), and MoE (G7). The
single most useful contribution is
**G4: one generic Detection Report** (confidence + error-bound + false-positive)
that subsumes the per-sensor reports and resolves the whole Y-series - a
consolidation, not just another gap.
