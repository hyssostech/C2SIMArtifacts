# Validation-Evidence Integration: the nine sourced missions

The scavenger session sourced and extracted all nine `Documents-Needed.md`
requests (12 V2Extraction records total; response in `Documents-Found.md`). This
walk integrates them into the review. Most **move an asserted finding to
evidenced**; three supply a **concrete report schema worth adopting**; one adds a
new finding. Proposals only.

## A. Validation - findings now grounded in a real mission

| Finding / decision | was | now evidenced by |
|---|---|---|
| Explainability report (X2 / Q-H) | asserted | Explainability_Agrawal2021 (DroneResponse: pushed {event, action, reasoning, change, confidence}) |
| On-the-loop authority (W1 / Q-K) | asserted | Agrawal (operator configure / suspend / acknowledge / override; wrong-perception override) |
| Sensor measurement + generic detection (Y5 / Q-Q) | asserted | CBRN_Muster (radiation value + variance), ElectronicWarfare_EmitterGeoloc (RSS line-of-bearing + 50/95% error ellipse), Remmersmann (WhoMeasuredType) |
| Area as subject (N1 / Q-M) | asserted | CBRN radiation map (per-cell estimate + variance over an area) |
| Persistence / standing task (N2 / Q-U / Q-N) | asserted | PersistentWatch_MDARS (standing watch, one operator many platforms) |
| Engagement authority + swarm typing + coordination (Q-K / Q-B / Q-P) | asserted | CounterUAS_CNAS2025 (layered detect / soft-kill / hard-kill, graded LoA, hostile-swarm typing) |
| Robot-to-robot / cross-cue (Q-G / Q-P) | asserted | Remmersmann (disaggregation/aggregation via a planning node), MCM cross-cue |
| Neutral / no-adversary (G10), recover/rescue (R2), area search (Q-N) | asserted | SAR_Kim2021, plus CBRN and Explainability (all no-adversary SAR) |
| Formation / relative geometry (Q-U) | asserted | FormationConvoy_Hu2020 (leader-follower geometry; **civilian**), Langerwisch MOVE (military) |
| Manipulation task verbs + effector typing (E1 / E2) | asserted (from LLM MUTT text) | CBRN_Muster (valve close, grasp, sample; 4-DoF arm + end-effector), Engineering_RCBC2018 (breach) |

Net: the section-8 "validation holes" (explainability, CBRN, EW, persistence)
each now have a sourced mission; the invisible domains are covered.

## B. Design schemas the real missions supply (prior art to adopt, not invent)

1. **Measurement / detection report -> BML `WhoMeasuredType` {value, unit-of-measure,
   phenomenon, sensor, time, place}** (Remmersmann 2015, a **BML** paper).
   C2SIM descends from BML/CBML, yet the current C2SIM/ASX has no measurement
   value+unit property (only `hasSpatialMeasure` and logistics quantities). So the
   generic measurement/detection report I flagged as missing (Y5/Q-Q) is **prior
   art in C2SIM's own lineage** that appears to have been dropped - re-adopting it
   beats inventing a new one. **Highest-value input of this batch.**
2. **Media report -> BML `ResourceType` {media URL, geographic reference}**
   (Remmersmann) - aligns almost exactly with the proposed `MediaReference` (Q-F).
3. **Explanation report -> {event, action, reasoning, operational change, confidence}**
   (Agrawal DroneResponse) - a concrete schema for the rationale report (Q-H).
4. **Area / hazard map -> per-cell value + variance (confidence)** (CBRN radiation
   map) - a concrete form of area-as-report-subject (N1/Q-M) and detection
   confidence (Q-Q).
5. **On-the-loop control verbs -> configure / suspend / acknowledge / override**
   (Agrawal) - grounds authority gating (Q-K / W1).
6. **Disaggregation / aggregation -> high-level order split into robot tasks;
   low-level reports aggregated to a high-level status** (Remmersmann BML) - grounds
   swarm report aggregation (Z1) and the open "who decomposes a collective task"
   question (a planning node sits between C2 and the robots). This is the MUM-T
   tasking level (request #6).

## C. New finding

- **G13 - dynamic capability self-report (BML `WhoHoldingType`).** A reconfigurable
  robot self-reports its mounted equipment/capability, and the planning node
  assigns tasks by capability. The current Init tabs declare a fixed entity type;
  they do not model self-reported or changeable capability. New decision Q-V.

## D. Two new tabs (added to the .xml)

### Hazard Area Map Report (Report)
| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| C2SIM | ReportBody | DomainMessageBody | hasReportContent | ??? | (hazard area map) | [!] N1/Q-M: report whose subject is an AREA - a per-cell hazard map |
| SMX | area | TacticalArea / MapGraphic | (map extent) | - | - | The mapped area |
| ASX | (map cell) | ? | value + variance | ??? | radiation estimate + variance | [!] Q-Q/Y5: per-cell value + variance(confidence); grounded by CBRN radiation map (Muster2024) |
| SMX | (detected) | SubjectTypeObservation | hazard type | SubjectType | Radiation source / Chemical | Detected-hazard identity (X4) |
| ASX | (prior art) | - | measurement structure | BML WhoMeasuredType | value + UOM + phenomenon + sensor + time + place | [+] adopt the BML measurement structure (Remmersmann) |

### MUM-T High-Level Tasking (Order)
| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| C2SIM | OrderBody | DomainMessageBody | isToReceiver | UUIDBase | (planning node / team) | High-level order to a control/planning node |
| C2SIM / ASX | High-Level Task | Task | hasTask | TaskActionCode | Reconnoiter Area | Node splits into low-level robot tasks |
| ASX | (planning node) | ? | disaggregates | ??? | -> move / image / measure | [!] Z1/new: high-level -> low-level task decomposition (BML Remmersmann); grounds "who decomposes a collective task" |
| ASX | (robot) | ? | capability self-report | ??? | WhoHoldingType (mounted equipment) | [!] G13: capability self-report; assignment by capability |
| ASX | (aggregated) | ReportContent? | status aggregation | ??? | low-level -> high-level status | [!] Z1: report-aggregation construct |

## Net effect

Section-8 **bucket 3** (document/validation gaps) is essentially closed - the
concepts the model asserted are now exercised by concrete sourced missions, and
three of them (Q-Q, Q-F, Q-H) have a concrete schema or in-family prior art to
adopt. **Buckets 1-2 are unchanged** - the unbuilt property/message layer and the
~20 open typing/vocabulary decisions remain the modeling side's job. What
changed is that those decisions can now be made on evidence, and the measurement
report in particular (Q-Q) should be a *re-adoption* of BML `WhoMeasuredType`
rather than a fresh invention.
