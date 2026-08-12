# ASX Review - Issues & Comments Log

Running log of open items, decisions, and comments surfaced while reviewing the
proposed ASX ontology elements against the scenarios and the sample-message
instantiations. This is the working source; the findings PowerPoint is generated
from it. Kept current as work proceeds.

**Framing.** The ASX ontology is an early work-in-progress (v0.0.x) and the
message instances are still being put in place. Items below are things *still to
be defined or decided* as that work continues - not defects in finished work.
The point is to make them explicit and instantiable, not to grade the model.

Severity: **DECIDE-FIRST** (a foundational typing decision to settle before
messages are built on it) / **HIGH** / **MED** / **LOW** / **TYPO**. Status:
**OPEN** / **RESOLVED**, plus qualified
states used in the tables (all variants of in-progress or partially-resolved):
**PARTIAL**, **NARROWED**, **MOSTLY COVERED**, **MOSTLY REUSE**, **WALKED**,
**INSTANTIATED**, **EVIDENCED**, **DECIDED**, **DONE**, **FOLDS INTO Q-x**.
**PROPOSED** marks a *slice* item - work scoped and grounded but not yet
performed (the grounding is verified; the work is what is being proposed).
Items marked **[deck]** are candidates for the findings presentation.

## 1. Repo sync & process

| ID | Sev | Status | Item | Evidence / note |
|---|---|---|---|---|
| S1 | HIGH | RESOLVED | Local clone was 52 commits behind origin/main | Fixed by pull on 2026-07-09; now level with origin (`021e715`). |
| S2 | HIGH | OPEN | Two work tracks are out of sync: OWL/RDF vs spreadsheets | OWL `CSIM_ASX.rdf` last updated 2026-01-20; spreadsheets updated 2026-06-10. Different tools, different altitudes. **[deck]** |
| S3 | MED | DONE (branch) | Workbooks are `.xlsx` (zipped XML), git cannot merge | All 3 sample-message workbooks converted to diff-able SpreadsheetML 2003 `.xml` (fidelity verified, 0 mismatches) and committed on branch `asx-diffable-spreadsheets`. NOTE: `.xml` and `.xlsx` now coexist - see S4. |
| S4 | HIGH | DECIDED | Dual source of truth: `.xml` vs `.xlsx` | Decision (2026-07-10): the `.xml` workbooks are the working copy for this review; Elizabeth's `.xlsx` files are left untouched for now. All new instantiation work (Init rows, CASEVAC tabs) goes into the `.xml` only. The `.xlsx` will diverge by design until the group reconciles. |

## 2. Track alignment: OWL vs Spreadsheet vs Deck (at different stages)

| ID | Sev | Status | Item | Evidence / note |
|---|---|---|---|---|
| D1 | HIGH | OPEN | Autonomy vocabulary defined three incompatible ways | OWL individuals {Automated, FullAuto, ReCont, Teleop}; ConceptMapping `Control Mode` {Piloted, Unpiloted-Autonomous, Swarm}; `NavigationAutonomy` {FPV, Autonomous, RemoteControl}. Which is normative? **[deck]** |
| D2 | HIGH | OPEN | Sensor modeled three incompatible ways | OWL `Sensor` class; ConceptMapping `SensorType` enum; `SensorCapability` equipment. (ConceptMapping also has internal value disagreements - not in `SensorType`, whose two rows are identical duplicates, but in `Payload` (row 12 adds `SensorType` to the value list) and `VehicleType` (`DroneFixedWing, DroneHover` vs `Drone - Fixed Wing, Drone - Hover`).) **[deck]** |
| D3 | HIGH | OPEN | Attribute layer not yet in the OWL | Payload, PayloadCapability, Mobility/Propulsion, VehicleType, PassengerCapability, AutonomousMissionFunction/Parameters, SwarmParameters are in ConceptMapping but not yet in the OWL (v0.0.1: 0 datatype / 1 object property; v0.0.3 adds a few, for the Video Detection Report only - see section 9). **[deck]** |
| D4 | MED | OPEN | Deck (June) proposes `Sensors subClassOf RobotPart`; OWL has `Sensor subClassOf ElectricDevice`, no RobotPart class | Slide 6 of 2026-06 status deck vs `CSIM_ASX.rdf`. Robotics-concept discussion not captured in model. |
| D5 | LOW | OPEN | Deck frames robotics subclass axioms as an open question, but OWL already committed them | UAV/UGV subClassOf Robot etc. asked as "Do we want to add...?" in June yet present in Jan OWL. |

## 3. OWL typos & naming (`CSIM_ASX.rdf`)

| ID | Sev | Status | Item | Evidence / note |
|---|---|---|---|---|
| O1 | TYPO | OPEN | Class name misspelled `CollecticeRoboticSystem` (should be "Collective") | Line 44-45; `Swarm subClassOf` the misspelled class. Will propagate into instance data once messages exist. **[deck]** |
| O2 | TYPO | OPEN | `versionInfo` says "Autonomous Systems Extrension" | Line 13. |
| O3 | LOW | OPEN | File named `CSIM_ASX.rdf` (missing the "2") | Inconsistent with every other C2SIM artifact; expected `C2SIM_ASX.rdf`. |

## 4. Sample-message instantiation - open items

| ID | Sev | Status | Item | Evidence / note |
|---|---|---|---|---|
| M1 | HIGH | OPEN | `actorReference` is `string` but must define a not-yet-known entity | Report Base Attributes note: "Observed Entity likely does not already exist... needs to be defined in the report." A string can't carry an entity definition. **[deck]** |
| M2 | MED | OPEN | `MediaReference` identity triple-defined | repositoryReference(UUID) + reportReference(string) + url(string), note "String may be better." Unresolved. |
| M3 | MED | OPEN | Same concept modeled two ways across two report sheets | media/analystComment placed on ActivityObservation/LocationObservation in one sheet vs. a new `SensorObservation` subclass in another. Which is normative? |
| M4 | MED | OPEN | `SensorObservation subClassOf ActivityObservation` is questionable | A sensor location fix is a LocationObservation; sensor output is not inherently an activity. |
| M5 | MED | OPEN | `MediaTypeCode` conflates media format with sensor modality | Sample-message `MediaTypeEnum` = {Video, Audio, Image, Document, Not Otherwise Specified} - the NOS value's own note says "other sensor types, e.g. thermal scan" (a sensor modality, not a media format). v0.0.3 carries the same five values plus TXT as `MediaTypeCode` {VID/AUD/IMG/DOC/TXT/NOS}. Category error either way. **[deck]** |
| M6 | MED | OPEN | Order task payload not modeled | "New Route Pattern" / "New Location" appear as bare rows with no type under the UAV Change Patrol Route Task. |
| M7 | HIGH | OPEN | `hasStartTime` typed `UUIDBase` | Both Order sheets; `hasEndTime` is `TimeInstant`. Almost certainly a copy-paste error. **[deck]** |
| M8 | LOW | OPEN | Namespace label inconsistency | `C2SIM_ASX` (Order, Report Base) vs `ASX` (Video Detection Report) for the same model. |

## 5. Initialization walk - entity-typing findings (headline)

(Note: the P-series is intentionally non-contiguous - P4 was retired/merged
during the walk. The P-IDs are stable cross-reference handles and are not
renumbered.)

| ID | Sev | Status | Item | Evidence / note |
|---|---|---|---|---|
| P1 | DECIDE-FIRST | OPEN | UAV typed twice, incompatibly: ASX `UAV subClassOf Robot subClassOf ActorEntity` vs SMX `Aircraft subClassOf Platform subClassOf ActorEntity` | Parallel (non-overlapping) sibling trees. `Robot` orphans the drone from Platform machinery; `Aircraft` leaves ASX classes unused. **[deck]** |
| P2 | DECIDE-FIRST | OPEN | Sensor: separately-declared entity, or attribute on platform? | Init must pick one; Report side only consumed sensor output. Ties to D2. **[deck]** |
| P3 | HIGH | OPEN | `hasAutonomousRoleCode` has no attachment point on the entity | Defined in OWL, but no Init field and not on EntityDescriptor. |
| P5 | HIGH | OPEN | Patrol route/area not modeled as an init object | Order references a route to change; nothing declares the baseline. Can host as MapGraphic. Gap on both Init and Order sides. Ties to M6. |
| P6 | HIGH | OPEN | Three competing autonomy vocabularies at init time | Same as D1, surfaced concretely when declaring an entity. |
| P7 | DECIDE-FIRST | OPEN | Swarm not yet taskable as modeled | `Swarm subClassOf CollecticeRoboticSystem -> ... -> PhysicalEntity`, but swarms receive orders and send reports (need ActorEntity). Base C2SIM has `CollectiveEntity subClassOf ActorEntity`. (v0.0.3 removed the Swarm class; CollecticeRoboticSystem is still non-actor.) **[deck]** |
| P8 | HIGH | NARROWED | Swarm membership + leader partially covered | `hasSubordinate`/`hasSuperior` (C2SIM) and `hasCommandRelation` (SMX) cover membership + command; residual gap is network params, leader-as-role, and dynamic handover. See section 6d. |
| P9 | TYPO | OPEN | Misspelling O1 propagates into swarm instance data | Same root as O1. |
| P10 | MED | OPEN | Heterogeneous (mixed UAV+UGV) swarm membership unconfirmed | MUTT-style mixed swarms; confirm members of different platform types can share one collective. |

## 6. Coverage gaps (scenario x message type)

| ID | Sev | Status | Item | Evidence / note |
|---|---|---|---|---|
| C1 | HIGH | PARTIAL | Initialization entirely un-instantiated (0 of 3 named scenarios) | Draft instantiations for all 3 named scenarios now applied to the `.xml` on branch (pending group review). **[deck]** |
| C2 | HIGH | INSTANTIATED | CASEVAC (flagship contributed scenario) has no messages of any type | Walked in `CASEVAC-Walk.md`; 5 tabs added to the `.xml` workbooks (CASEVAC Init; CASEVAC Tasking + Route Advert; CASEVAC Status+Threat + Explainable). Surfaced X1/X2 (section 6b). **[deck]** |
| C3 | MED | OPEN | 8 of 10 MUTT scenarios have no instantiations | Only Recon->video and Logistics->UGV transport partly covered. |
| C4 | MED | INSTANTIATED | Non-video sensors not covered | Walked in `NonVideoSensors-Walk.md`; 3 report tabs added to the `.xml` (CBRN / EW Emitter / GPR Mine). Surfaced Y1-Y5 (section 6c). **[deck]** |
| C5 | LOW | INSTANTIATED | Swarm Detection report + swarm coordination order not done | Walked in `Swarm-Walk.md`; `Swarm Detection` stub filled (Report) and `Swarm Coordination` tab added (Order). Surfaced Z1/Z2 and narrowed P8 (section 6d). |
| C6 | HIGH | INSTANTIATED | Task/effect axis (engagement, manipulation, delivery) not walked | Walked: Fire Support (`FireSupport-Walk.md`) + Logistics/Engineering/USV Rescue (`TaskEffect-Batch-Walk.md`). Tabs: Fire Support Order, BDA Report, Logistics Delivery Order, Engineering Task Order, USV Rescue Order, Delivery Confirmation Report. Surfaced W1-W3 (6e) and L/E/R (6f). Route-clearance / companion / urban examined in the redundancy pass (6g; a Route Clearance Order tab was added). **[deck]** |
| C7 | HIGH | INSTANTIATED | Sourced scenarios (maritime MCM, subterranean SubT, sustainment) not integrated | Walked in `SourcedScenarios-Walk.md`; 7 tabs added (MCM Init, SubT Team Init, MCM Cross-Cue Neutralize, Explore Area Order, Contested Resupply Order, Naval Mine Detection Report, Generic Detection Report). Corroborated X1/N2/P1/Y; added G1-G10 (6h). (Counter-UAS, HMT, and SAR were un-extracted at this stage; all three were later extracted in the validation pass - see C8/6j.) **[deck]** |
| C8 | HIGH | EVIDENCED | Validation holes (explainability, CBRN, EW, persistence) unexercised by any sourced mission | The sourcing track extracted all 9 `Documents-Needed` requests; integrated in `ValidationEvidence-Walk.md` (6j). Holes now grounded; Q-Q/Q-F/Q-H gain concrete schemas (BML WhoMeasuredType/ResourceType; Agrawal explanation). Added G13/Q-V; 2 tabs. **[deck]** |
| C9 | HIGH | INSTANTIATED | SME drone-warfare thread (LIRC baseline, 2024 threat/TTP update, OPFOR targeting) not integrated | Walked in `DroneWarfare-LIRC-OPFOR-Walk.md`; 5 tabs added (LIRC Company Init; LIRC Kill-Box Engagement Order; Counter-UAS Defeat Order; OPFOR Targeting Handoff; LIRC Strike BDA Report). Supplies a concrete candidate answer to W1/Q-K (the kill-box / weapons-control construct); added G14-G19 (6k). Corroborated W1/W2/W3/N1/N2/G3/G7/G8/G11/D1. **[deck]** |

## 6b. CASEVAC walk findings (from CASEVAC-Walk.md)

| ID | Sev | Status | Item | Evidence / note |
|---|---|---|---|---|
| X1 | HIGH | OPEN | No robot-to-robot coordination content type | Envelope addressing (isFromSender/isToReceiver) supports peer messages, but no ReportContent/OrderBody wraps "verified safe route, use it"; UGV-as-issuer authority unclear. CASEVAC scout->transport hand-off. **[deck]** |
| X2 | HIGH | OPEN | No rationale/explanation ReportContent | ReportContent = {smx#ObservationReportContent, PositionReportContent, TaskStatus}. CASEVAC "explainable reasons" (why route changed / mission failed) has no element. TaskStatus gives state, not rationale. Candidate: new ASX RationaleReportContent. **[deck]** |
| X3 | MED | OPEN | Route exists but no share-payload wrapper | `Route` (SMX) exists; ASX Order sheet used free-text "New Route Pattern" instead. Refines M6/P5. |
| X4 | MED | OPEN | No obstacle/threat observation subtype | Detected IED/broken-bridge that triggers replanning would fall to ActivityObservation or a new type; hazard entity typing unclear. |
| X5 | LOW | MOSTLY COVERED | Phased tasks/ETA | Base `PlanBody`/`PlanPhase`/`PlanPhaseTrigger` exist; recommend reuse for phased CASEVAC tasking. The estimated-completion / ETA residual is noted for follow-up. |
| X6 | LOW | OPEN | CASEVAC task + re-tasking semantics | Is CASEVAC a base TaskActionCode or new ASX task; mid-mission order amendment semantics. |

Note: position/status reporting, routes, and phased planning are **covered by
the base standard** - CASEVAC did not break them. The genuinely new needs are
X1 and X2.

## 6c. Non-video sensor walk findings (from NonVideoSensors-Walk.md)

| ID | Sev | Status | Item | Evidence / note |
|---|---|---|---|---|
| Y1 | HIGH | OPEN | The media-based report model does not generalize | `Video Detection Report` models sensor output as `SensorObservation` + `MediaReference` + `MediaTypeEnum` (a video file). Non-video sensors emit readings, not media files - CBRN/EW/GPR have no place to put the measurement. **[deck]** |
| Y2 | MED | OPEN | SensorType enum incomplete | {Visual, EW, CounterEW, Audio} omits CBRN, radiological, nuclear, biological, GPR/radar, thermal, LIDAR, metal-detector. |
| Y3 | HIGH | OPEN | No detection/hazard Observation subtype | Observation subtypes are only {Activity, Health, Location, Name, Resource, SubjectType}; none fits a detected agent/emitter/hazard. Ties to X4. |
| Y4 | MED | OPEN | EW sensing has no report content type | `JAM` is a LOX TaskActionCode (the action), not an observation of an intercepted emitter. |
| Y5 | HIGH | OPEN | No sensor-reading value+unit property | Concentration, dose rate, frequency, depth have no home; only logistics quantities, `hasSpatialMeasure`, and `smx#hasConfidenceLevel` exist. **[deck]** |

Partially covered (not gaps): location (`LocationObservation`), detected-object
identity (`SubjectTypeObservation`, if the entity type exists), confidence
(`smx#hasConfidenceLevel`). Reuse candidates nearby (neither carries a reading):
`smx#NBC_Event` (an APP6-C tactical-graphics symbol class) and the LOX
chemical/biological/nuclear *sampling* task verbs.

## 6d. Swarm walk findings (from Swarm-Walk.md)

| ID | Sev | Status | Item | Evidence / note |
|---|---|---|---|---|
| P7 | DECIDE-FIRST | OPEN | Swarm not yet taskable or able to report | Both swarm messages show it: an OrderBody recipient and a ReportBody `hasReportingEntity` need to be an ActorEntity; ASX Swarm derives from PhysicalEntity. (Precision: `hasPerformingEntity`/`hasReportingEntity` are datatype properties carrying UUID references, so nothing fails an OWL reasoner - the ActorEntity requirement is stated in their annotations: "the unique identifier of an individual of the ActorEntity class". The semantic mismatch stands.) Proposed: `Swarm subClassOf CollectiveEntity` (C2SIM; re-declared in SMX). **[deck]** |
| Z1 | MED | OPEN | No aggregation construct | A swarm detection built from multiple members' observations - one collective report or N member reports? No aggregation model. |
| Z2 | MED | OPEN | No swarm-lifecycle construct | Dynamic member rotation / resupply / replacement (June deck) has no construct. |
| P8 | HIGH | NARROWED | Membership + command mostly covered | `hasSubordinate`/`hasSuperior`/`hasCommandRelation` exist; residual is network params, leader-as-role, dynamic handover. |
| P10 | MED | OPEN | Heterogeneous membership | Mixed UAV+UGV in one collective - confirm. |

Partially covered (checked): collective entity type (`CollectiveEntity`),
membership/command (`hasSubordinate`/`hasSuperior`/`hasCommandRelation`),
reporting linkage (`hasReportingEntity`) - all conditional on fixing P7.

## 6e. Fire Support / task-effect walk findings (from FireSupport-Walk.md)

| ID | Sev | Status | Item | Evidence / note |
|---|---|---|---|---|
| W1 | HIGH | OPEN | No link between autonomy level and engagement authority | ROE (`RuleOfEngagement`, `WeaponRuleOfEngagementCode` - LOX) and `AuthorizationHeader` (C2SIM) exist, but nothing states whether an autonomous system at a given autonomy level may take a lethal action without a human in/on the loop. The central ASX policy gap. **[deck]** |
| W2 | MED | OPEN | Weapon/munition not typed | ConceptMapping Payload = Armiture/Ammunition; absent from OWL. Ties to D3/P2. |
| W3 | MED | OPEN | No effect-achieved / BDA ReportContent | `TaskStatus` reports the task ran, not whether the target was destroyed. |

Partially covered (checked, NOT gaps): rules of engagement, desired effect
(`DesiredEffectCode`), target designation (`hasAffectedEntity`), the engage/attack
verbs. (`AuthorizationHeader` is message-sender authentication, NOT command
authorization of fires - so who-approved-the-engagement is part of W1.) The
engagement machinery mostly exists - the missing
piece is autonomy-to-permission.

## 6f. Task/effect batch findings (from TaskEffect-Batch-Walk.md)

| ID | Sev | Status | Item | Evidence / note |
|---|---|---|---|---|
| L1 | MED | OPEN | No cargo/payload manifest | What a platform carries. `Resource` + quantities exist; "load carried" does not. ConceptMapping Payload absent from OWL. |
| L2 | MED | OPEN | No delivery-confirmation ReportContent | What was delivered and received by whom; `TaskStatus` only says the task ran. |
| E1 | LOW | mostly covered | Engineering verbs exist in LOX | `CONSTR` (build/dig), `CLROBS`/`CLRLND` (clear), `MINLAY` (emplace), `BREACH` exist; folds into E2 (effector typing). |
| E2 | MED | OPEN | No effector/manipulator equipment concept | arm / blade / excavator. Ties to P2/D3. |
| R1 | - | reconfirms P1 | USV typing (SMX `SurfaceVessel` vs ASX `USV`/Robot), now maritime. |
| R2 | LOW | OPEN | Only a general-purpose tow/salvage verb absent | `lox#RESCUE` and `lox#RECOVR` exist as TaskActionCodes (the downed-pilot task uses RESCUE). The closest to tow/salvage are `lox#TOWTGT` (tow, but scoped to gunnery targets) and the broadly-defined `lox#RECOVR` ("retrieve any lost, incapacitated or captured object") - so the residual is a general-purpose tow/salvage verb, and RECOVR may already suffice. |

Recurring shape of the whole task/effect axis: LOX already has 446 `TaskActionCode`
verbs (incl. BREACH, ENGAGE, ATTACK, CONSTR, CLROBS, MINLAY, RESCUE, RECOVR, NTRCOM),
so what is actually missing is narrow - **(a) payload/effector/weapon typing**
(cargo L1, manipulator E2, weapon W2 are one gap) and **(b) a general-purpose
tow/salvage verb** (closest existing: `TOWTGT`, gunnery-target towing only, and
the broadly-defined `RECOVR`). Entity structure, addressing, effects, targets,
resources, ROE, and the whole task-verb vocabulary already exist. Distilled into
decision Q-L.

## 6g. Redundancy-pass findings (from RedundancyPass-Walk.md)

Checked the three scenarios flagged as likely-redundant (route clearance,
companion drones, urban combat). Mostly confirmed - but the pass found one new
finding that the entity-centric walks missed.

| ID | Sev | Status | Item | Evidence / note |
|---|---|---|---|---|
| N1 | MED | OPEN | Area as the subject of a task/report | `hasAffectedEntity` has no area counterpart (no `hasAffectedArea`), and there is no area-state (cleared/contaminated/mined). Areas exist (`TacticalArea`, `MapGraphic`) but are not yet taskable or able to have their state reported. Recurs in route-clearance, CBRN, urban. **[deck]** |
| N2 | LOW | FOLDS INTO Q-L | Follow / escort / relay | Task verbs (Q-L) over existing `RelativeLocation` / `CommunicationNetwork`; only persistent-vs-one-shot task semantics is a nuance. |

Confirmed redundant (no new finding): neutralize = engage (W), detection = Y,
transport = L, clear = E, recon = Y, relay = CommunicationNetwork + verb. The
"redundant" call held ~80%; N1 is the nugget that justified the pass.

## 6h. Sourced-scenarios reconciliation (MCM / SubT / Sustainment)

From the parallel scenario-sourcing session (`LLMExperiments/PaperSummaries/V2Extractions/` +
`OntologyConceptCoverage.md`), walked in `SourcedScenarios-Walk.md`. This
input was initially missed and then integrated; it corroborates several findings
and adds new ones.

**Corroborated:** X1 (robot-to-robot <- MCM cross-cueing), N2 (persistent <-
MCM revisit), P1 (typing <- SubT/MCM, + locomotion axis G5), Y-series (sensor
reports <- SubT/MCM detections, + the generic-report answer G4).

| ID | Sev | Status | Item | Evidence / note |
|---|---|---|---|---|
| G1 | MED | OPEN | Denied-comms mode + deployable relay entity | SubT. A relay task verb `lox#COMREL` exists; missing is a comms-degraded operating MODE and a droppable relay ENTITY/node (`CommunicationNetwork` is a network, not a node). **[deck]** |
| G2 | MED | OPEN | Area-coverage / exploration goal | SubT. Search/recce verbs (`RECCE`, `RECONS`, `PATROL`, `SWEEP`, `DETECT`) exist; missing is the coverage-*goal* semantics (explore-until-covered), tied to N1. **[deck]** |
| G3 | MED | OPEN | Cross-cueing: system-to-system task + shared classified track | MCM. Reuses X1 + M1; no Track/Contact object type. |
| G4 | HIGH | OPEN | Generic parameterized Detection Report | confidence + error-bound + false-positive + modality; subsumes Video/CBRN/EW/GPR/naval-mine/artifact. **Resolves Y1/M3/M4.** **[deck]** |
| G5 | MED | OPEN | Platform locomotion/role subtypes | wheeled/tracked/legged UGV; detector/neutralizer USV. Extends P1. |
| G6 | LOW | MOSTLY REUSE | Maritime depth | naval mine (moored/bottom) via SubjectTypeObservation; UUV=SubsurfaceVessel; sea-lane area. |
| G7 | LOW | OPEN | Measure-of-effectiveness attributes on reports | % neutralized, active time (MCM). |
| G8 | LOW | OPEN | Decoy as a distinct behavior/role | Deception verbs (`DECEIV`, `DAZZLE`) exist; a decoy role/behavior is the residual. |
| G9 | MED | OPEN | Threat-aware / contested-delivery order annotations | Sustainment. Risk/threat + level-of-autonomy on a logistics order. |
| G10 | LOW | MOSTLY COVERED | Neutral-actor framing | `HostilityStatusCode` neutral value `smx#NEUTRL` exists (`smx#ANT` = assumed-neutral); a `NeutralSide` individual also exists but is untyped. Residual = neutral-as-constraint + no-adversary missions. |

Un-extracted at this (6h) stage - all three were later extracted in the
validation pass (see 6j / C8): counter-UAS / swarm-vs-swarm, human-machine
teaming, humanitarian SAR - see
`CandidateSources.md`.

## 6i. Re-sync with the sourcing session's concept-coverage doc

The sourcing session revised its analysis (commit a150ffb) into a concept-centric
bidirectional read (`LLMExperiments/OntologyConceptCoverage.md`) against
`CSIM_ASX.rdf` v0.0.1 and the InstantiationReview framing. Reconciliation:

**Aligned** (their 11 expressiveness gaps <-> my findings): maritime USV/UUV
(P1/G6), locomotion subtypes (G5/Q-R), coordination + M2M tasking (X1/G3/Q-G/Q-P),
comms/relay + denied-comms (G1/Q-O), generic detection w/ confidence (G4/Q-Q),
task breadth incl. explore/neutralize/decoy (Q-L/Q-N/Q-S), persistence (N2),
graded LoA (D1/Q-D).

**Refined:** neutral actors - their doc hedges ("if the model presumes a hostile
side"); my grounding confirms the neutral `HostilityStatusCode` value
`smx#NEUTRL` exists (and an untyped `NeutralSide` individual), so the gap is only
neutral-as-constraint / no-adversary missions (G10). Graded LoA -
their #6 sharpens Q-D: autonomy is not one flat vocabulary but a graded scale
that can vary by mission phase.

**Two aspects I had under-covered (now added):**

| ID | Sev | Item | Grounding |
|---|---|---|---|
| G11 | MED | Operating-environment *conditions* as attributes (GPS-denied, illumination, sea-state, terrain, domain) | `EnvironmentalObject` / `RoboticEnvironment` exist as bare classes; no condition attributes. |
| G12 | MED | Formation / relative geometry (orbit, convoy spacing, "one overhead, others orbiting") | `RelativeLocation` exists (single relative pos); no formation pattern/geometry. |

**Their complementary "validation" reading (which I did not produce):** among the
six sourced scenarios, **explainability, CBRN/EW sensing, CASEVAC coordination,
and persistence have no scenario evidence** - the ASX model asserts/intends these
but no real sourced mission exercises them. A corpus gap, distinct from the
expressiveness gaps - see section 8.

## 6j. Validation-evidence integration (nine sourced missions)

The sourcing track extracted all nine `Documents-Needed.md` requests (see
`Documents-Found.md`, `LLMExperiments/PaperSummaries/V2Extractions/`). Walked in
`ValidationEvidence-Walk.md`. Effect: asserted findings are now **evidenced**,
and three decisions gain a concrete schema / prior art.

**Now evidenced by a real mission:** explainability X2/Q-H (Agrawal DroneResponse),
on-the-loop authority W1/Q-K (Agrawal override verbs), measurement+generic
detection Y5/Q-Q (CBRN radiation value+variance, EW RSS + error ellipse,
Remmersmann WhoMeasuredType), area-as-subject N1/Q-M (CBRN radiation map),
persistence N2 (MDARS), swarm/engagement Q-B/Q-K/Q-P (CounterUAS CNAS),
neutral/SAR G10/R2/Q-N (SAR_Kim + CBRN + Explainability), formation Q-U
(FormationConvoy_Hu, Langerwisch), manipulation E1/E2 (CBRN valve/sample, breach).

**Design schemas to adopt (prior art, not invent):**
- **Q-Q/Y5 <- BML `WhoMeasuredType` {value, UOM, phenomenon, sensor, time, place}**
  (Remmersmann - a BML paper). C2SIM descends from BML but lacks this; re-adopt
  rather than invent. Highest-value input.
- Q-F <- BML `ResourceType` {media URL, geo}; Q-H <- {event, action, reasoning,
  change, confidence} (Agrawal); N1/Q-M <- per-cell value+variance map (CBRN);
  Q-K <- configure/suspend/acknowledge/override (Agrawal); Z1 + collective-task
  decomposition <- BML disaggregation/aggregation (Remmersmann).

| ID | Sev | Status | Item | Evidence / note |
|---|---|---|---|---|
| G13 | MED | OPEN | Dynamic capability self-report | BML `WhoHoldingType`: a reconfigurable robot self-reports mounted equipment; tasking assigned by capability. Init tabs declare a fixed type only. |

Two tabs added (`.xml`): `Hazard Area Map Report` (Report), `MUM-T High-Level
Tasking` (Order).

## 6k. Drone-warfare walk findings (from DroneWarfare-LIRC-OPFOR-Walk.md)

The SME-directed drone-warfare thread - Morris 2018 LIRC baseline, its 2022-2024
threat/TTP update, and the Rosenberg JPMRC-AK 24-02 OPFOR commercial-sUAS targeting
run (`LLMExperiments/PaperSummaries/V2Extractions/`) - walked in
`DroneWarfare-LIRC-OPFOR-Walk.md`. This is the thread that lands on **W1/Q-K**
(autonomy-to-engagement-authority), the review's most central open finding: the LIRC
baseline carries a fully worked doctrinal control mechanism for autonomous lethal
authority, so it supplies a candidate *answer*, not just another instance of the gap.

**Corroborated:** W1/Q-K (engagement authority <- LIRC kill-box mechanism, strongest
instance in the library), W2/Q-L (weapon/munition typing <- mixed UGV armament +
loitering munitions), W3 (BDA ReportContent <- LIRC + OPFOR BDA), N1/Q-M (area as
subject <- kill box as authorization-bearing, civilian-cleared area), G3/Q-P
(cross-cueing + shared track <- OPFOR sensor-to-shooter handoff), N2 (persistence <-
OPFOR observer on station through the strike), G7 (MoE <- ~50% attrition; ~7-day drone
life / ~10% completion), G8/Q-S (decoy <- decoy vehicles defeat discrimination),
G1/Q-O (denied comms <- GPS-denied operation), G11/Q-T + D1/Q-D (environment
conditions + graded/phase-varying autonomy), P1 (platform typing <- armed UGV,
loitering munition, FPV, COTS quadcopter).

| ID | Sev | Status | Item | Evidence / note |
|---|---|---|---|---|
| G14 | HIGH | OPEN | Weapons-control-status + kill-box construct | An authorization-bearing area (weapons-control status hold/tight/free x geo bound x time window x civilian-clearance state x permitted target type) that gates autonomous lethal engagement. Grep of C2SIM/SMX/LOX: none of weapons-control-status, kill box, free-fire/no-fire area, FSCM exists. A concrete model that ANSWERS W1/Q-K and unifies it with N1/Q-M. **[deck]** |
| G15 | MED | OPEN | Graded, phase-varying engagement authority | LIRC shifts weapons hold (movement) -> tight (pre-LD) -> autonomous-in-kill-box; authority is temporal/graded, sharpening D1/Q-D (autonomy varies by mission phase). |
| G16 | MED | OPEN | Loitering munition / FPV as a platform-munition hybrid | Flies, senses, then is expended; size tiers (mini/tactical/long-range). Extends P1/G5 (platform) and W2/Q-L (munition); neither captures the hybrid. `loiter`/`munition` class absent (grep). |
| G17 | MED | OPEN | Counter-UAS engagement | Mostly REUSE - `lox#AIRDEF`, `lox#ENGAGE`, `lox#ATTACK`, `lox#DETECT`, `lox#JAM` exist; residual is an sUAS/UAS target class and the detect->defeat + soft-kill(JAM)/hard-kill(ENGAGE) coupling. |
| G18 | MED | OPEN | Adversarial EW against own autonomy | GPS-denial, control-link jamming, and drone-hijack (control seized in ~25 s) are threats TO friendly autonomy; extends G1/Q-O with a vulnerability + countermeasure (INS fallback, encrypted FH / fiber-optic link). Relates to Y4 (EW sensing). |
| G19 | MED | OPEN | Targeting construct (target list + sensor-to-shooter) | A high-value/high-payoff target LIST + nomination/prioritization (targeting board) and the cue->validate->grid->fire->BDA->adjust cycle (OPFOR). Target-list/priority object is net-new (grep: absent); the cross-cue part is G3. |

Grounding note: `lox#AIRDEF/ENGAGE/ATTACK/DETECT/JAM`, `RuleOfEngagement`,
`DesiredEffectCode`, `hasAffectedEntity`, `AuthorizationHeader`, `TacticalArea`/
`MapGraphic`, and the ASX autonomy individuals all exist and are reused; the
authority-gating (G14/G15), the weapon/munition and small-UAS typing (G16/G17), the
EW-vulnerability (G18), and the target-list (G19) do not.

## 6l. Sensor characterization (PROPOSED slice)

A **proposed slice** - work scoped for the future, not yet performed - from an
item suggested by Curt: look into the characterization of sensors; it may be a
whole extension worth on its own, and could be based on existing standards.
Scoped in `Sensor-Characterization-Slice.md`. Nothing instantiated; the grounding
is verified (no `Sensor` class or measurement property in base C2SIM/SMX/LOX; six
Observation subtypes only; no capability/performance property anywhere).

Both halves of the suggestion hold up. **Extension-sized:** 15 open findings and
6 open decisions already cluster here, comparable in weight to the entire current
ASX OWL; structurally a sensor model must answer four separable questions -
device / capability / observation / configuration - and ASX has a partial first
and nothing else. **Buildable from existing standards:** three independent
lineages already agree on the observation shape.

| ID | Sev | Status | Item | Evidence / note |
|---|---|---|---|---|
| G20 | HIGH | PROPOSED | Sensor characterization is extension-sized | Core (11): D2, P2, M3, M4, M5, Y1-Y5, G4. Adjacent (4): X4, G3, G13, G18. Decisions (6): Q-C, Q-F, Q-I, Q-P, Q-Q, Q-V. Compare the whole ASX OWL: v0.0.1 = 15 classes / 1 object / 0 datatype props; v0.0.3 = 26 classes / 4 object / 2 datatype. The four-question split (device / capability / observation / configuration) is what makes it too big to patch into the report model. **[deck]** |
| G21 | MED | PROPOSED | Three lineages converge on one observation shape | BML `WhoMeasuredType` {value, UOM, phenomenon, sensor, time, place} (C2SIM's own ancestry, already flagged in 6j as re-adopt-not-invent), W3C/OGC SOSA `Observation` {hasResult, observedProperty, madeBySensor, resultTime, hasFeatureOfInterest}, and the DIS emission parameter records. Three communities, three purposes, one shape - re-deriving it a fourth time inside ASX would be a modeling error. |
| G22 | MED | PROPOSED | The capability layer is entirely absent, and has an off-the-shelf vocabulary | No range / accuracy / resolution / FOV / detection-limit / operating-condition property exists anywhere in ASX or the base standard. The SSN-System module supplies exactly this: `SystemCapability`, `SystemProperty`, `MeasurementRange`, `Accuracy`, `Precision`, `Resolution`, `DetectionLimit`, `Latency`, `Sensitivity`, `ResponseTime`, `Drift`, `OperatingRange`, `SurvivalRange`, `Condition`. Also what G13 (capability self-report) needs. |

## 6m. DIS enumerations as a source for ASX (PROPOSED slice)

A separate **proposed slice**, independent of 6l - from an item suggested by
Curt: look into the DIS enumeration materials, extract the organizing principles
behind that mass of data, reduce it to a succinct categorization, and see what it
offers ASX. Scoped in `DIS-Enumerations-Slice.md`.

**Framing, stated precisely because it is easy to get wrong.** DIS is examined as
a **design source that may inform ASX in general** - not as an input to any one
ASX question, and **not as a proposal to use the DIS codes more directly**. The
codes are already carried: C2SIM entities have had the seven-field DIS record all
along, so "should ASX carry DIS codes?" is settled, not open. What is open is
whether ASX is learning anything from the thirty years of reasoning behind them -
how to partition the world into kinds, when a component earns its own type, where
type ends and instance begins, how to grow a vocabulary without it collapsing.
The proposition is to mine that reasoning, plus the evidence in DIS's taxonomy
about what needs modeling at all. Whether any septuplet is ever written into a
message is a separate question this slice does not raise.

**The succinct categorization:** SISO-REF-010 reduces to **four table shapes** -
`enum` (value-description pairs), `bitmask` (bitfields), `cet` (entity types),
`cot` (object types) - plus metadata, over a 64-bit septuplet
`Kind.Domain.Country.Category.SubCategory.Specific.Extra` (bit widths
8/8/16/8/8/8/8, unsigned). The original document had 279 tables; the volume comes
from the entity-type category, not from structural variety. Five governance
principles are adoptable for ASX's own code lists (D1, Y2, M5) without touching a
single DIS code - most usefully *implicit types are legal on the wire*, which is
how the catalogue stays finite while the space stays open.

| ID | Sev | Status | Item | Evidence / note |
|---|---|---|---|---|
| G23 | MED | **OPEN** | The walks type entities with a property that does not exist | `hasEntityType` / `EntityType` (8 rows Init, 6 Order, 1 Report, carrying free text) - and **neither `C2SIM#hasEntityType` nor a bare `EntityType` class exists in C2SIM, SMX, or LOX**. The standard already defines two real hooks: `hasNamedEntityType` (namespaced string) and `hasSISOEntityType` (the DIS record, already standard machinery on every `Entity`). Self-inflicted: the first committed conversion (`cb42d5a`) had no entity-type field at all. **A workbook hygiene defect, not a DIS-adoption question** - fix by using a real property, most likely `hasNamedEntityType`. Independent of anything the sub-group decides about DIS. |
| G24 | HIGH | PROPOSED | DIS is a general-purpose design source, not a single-purpose one | At least **eight of nine Entity Kinds** bear on open ASX findings, and the value is the carve-up and its reasoning rather than the code values: Platform -> P1/G5/G6/G16/G17/V1 (its Domain field *is* the land/air/surface/subsurface partition ASX keeps re-deriving); Munition -> W2/Q-L (fuse+warhead as the decomposition axis; loadout ruled to be state, not type); Life form -> P7/P10/Z1 (Subcategory encodes number of individuals: one-type-many-individuals); Environmental -> G11/Q-T (DIS types environmental *conditions* such as sea state, not just objects); Cultural feature -> X4/N1/Q-M/E-series; Supply -> L-series/Q-L (class of supply as a typing axis, AR 710-2); Radio -> G1/Q-O (evidence the relay node is a first-class entity, not a network attribute); Expendable -> G8/Q-S (expendability as a typing axis, decoys inside it). **[deck]** |
| G25 | HIGH | PROPOSED | DIS's component/whole criterion is portable to Q-C/P2/D2 | OPMAN 7.4.2.1/7.4.2.9: subsystems that "strictly support only a particular platform system" are enumerated inside that platform; those that "can operate in a stand-alone manner or that can support multiple systems" get their own entity type. Worked example: Patriot's AN/MPQ-53 radar is Kind 9; the ZSU-23-4's welded-in "Gun Dish" is not. A tested criterion ASX can restate in its own terms to settle "is a sensor an entity or an attribute?", generalizing to any component typing decision (payloads, effectors, relays). Cross-ref 6l. |
| G26 | MED | PROPOSED | DIS emission records are a worked precedent for the measurement layer | Sensing modeled as system identity + a parameter record of typed values with declared units - Fundamental Parameter Data record: Frequency (Hz), Frequency Range (Hz), ERP (dB), PRF (Hz), Pulse Width (us), beam azimuth/elevation center+sweep (rad), sweep sync (%) - with modality selecting the parameter set. **The transferable content is the shape**, not the record: Y5/Q-I says ASX has no such layer at all, and this demonstrates one is necessary and tractable (the EW Emitter Report in `NonVideoSensors-Walk.md` wanted "243.0 MHz / 25 kHz" - a frequency-plus-range pair). The four modality families (EE 23 / Designator 24 / IFF 28 / UA 29) are evidence for Y2 that modality is the right partition; the separate `Emitter Function` enumeration is evidence for Y4 that *what an emitter is for* is a typing axis distinct from *what it is*. Which vocabulary ASX adopts is 6l's question. **Limits:** no confidence, error bound, or false-positive rate - G4/Q-Q still needs SOSA/BML. Only the EM row is verified field-by-field. Cross-ref 6l. |
| G27 | MED | PROPOSED | DIS separates type from instance, deliberately | OPMAN 7.4.5: unique identification is explicitly *not* the entity type's job - only naval ships and oil platforms get unique types, life forms and most platforms are "explicitly disallowed"; unique ID happens via the Entity Marking field or a Variable Parameter record. ASX faces the same line in M1 (`actorReference` must define a not-yet-known entity) and Q-E (inline entity definition). Worth reading before ASX draws it differently by accident. |
| G28 | LOW | OPEN | `C2SIM.rdf` mis-cites the DIS standard | All seven `hasDIS*` properties carry `rdfs:comment` "...from the DIS standard IEEE 1516-2010". IEEE 1516 is **HLA**; DIS application protocols are **IEEE 1278.1**; the enumerated values live in **SISO-REF-010**, not in the IEEE standard at all. Both halves wrong. Base-standard defect (lines ~916-990) - for the parent group, not ASX. |
| G29 | MED | OPEN | `C2SIM.rdf` under-ranges six DIS fields | `hasDISKind/Domain/Category/SubCategory/Specific/Extra` typed `xsd:byte` (signed, -128..127); the fields are 8-bit **unsigned**, 0-255 (ISO/IEC 19775-1, which carries the same fields normatively, declares each `[0,255]` and country `[0,65535]`). Legal values 128-255 unrepresentable. Should be `xsd:unsignedByte`. A genuine interoperability bug. Base-standard defect - for the parent group. |

Honest limits (the "nothing" column, first draft): DIS types **things**, not
behavior, authority, or intent - it offers nothing for W1/Q-K (engagement
authority), G14/Q-W (weapons-control status / kill box), X2/Q-H (rationale), or
X1/Q-G (robot-to-robot coordination), several of which are this review's
highest-value findings; its reach stops at the typing half of ASX. And its
purpose shapes its carve-up: DIS boundaries exist to let a **simulation** render
and interact, while ASX answers to what a **commander** must state or be told, so
some boundaries will be artifacts of rendering fidelity rather than of command
meaning (the country-code field is the clearest example - it answers a question
ASX has not asked). The kind-by-kind map is a list of places to *look*; each
transfer must be argued on ASX's own terms. **That is also this slice's
falsifier:** if the placement exercise shows DIS's boundaries consistently fail
to survive translation, G24 shrinks to a much shorter list.

## 7. Open decisions for the sub-group (comments)

- **Q-A [deck]** Should ASX autonomy be a *role/facet on the existing Platform
  subtree* rather than a parallel `Robot` class tree? (Resolves P1, D-tree split.)
- **Q-B [deck]** Should `Swarm` derive from `CollectiveEntity` (ActorEntity)
  instead of the device/artifact tree? (Resolves P7.)
- **Q-C** Is a sensor a first-class Entity/Equipment, a class, or an attribute?
  Pick one model and apply it in Init, Report, and ConceptMapping. (Resolves D2/P2.)
- **Q-D** Choose one normative autonomy vocabulary and express the others as
  derived/orthogonal. (Resolves D1/P6.)
- **Q-E** Define an inline entity-definition mechanism for newly-observed
  (uncooperative) entities so a report can introduce an entity it references.
  (Resolves M1.)
- **Q-F** Decide MediaReference identity (repository+report vs URL) and separate
  media-format from sensor-modality. (Resolves M2/M5.)
- **Q-G [deck]** Define a robot-to-robot coordination content type (e.g. safe-route
  advertisement) and the authority model for a robot issuing it. (Resolves X1.)
- **Q-H [deck]** Add a rationale/explanation ReportContent so autonomous systems can
  report *why* (route change, mission failure), not just *what*. (Resolves X2.)
- **Q-I [deck]** Define a media-independent sensor-reading / measurement
  representation (value + unit + modality) and complete the SensorType taxonomy,
  so non-imaging sensors (CBRN, EW, GPR, thermal) can report. (Resolves Y1/Y2/Y5.)
- **Q-J** After fixing P7, add the small swarm residuals: network/comms
  parameters, a leader role, report aggregation (Z1), and member lifecycle
  (Z2). Membership/command reuse C2SIM `hasSubordinate` / SMX `hasCommandRelation`.
- **Q-K [deck]** Model engagement authority as a function of autonomy level -
  may a system at this autonomy level take this (lethal) action without a human
  in/on the loop? ROE already exists; command authorization of the engagement and
  this autonomy link do not (`AuthorizationHeader` is only message-sender auth).
  (Resolves W1.)
- **Q-L [deck]** Add typed **payload / effector / weapon** (cargo, manipulator,
  munition) - the action verbs already exist in LOX (BREACH, ENGAGE, ATTACK,
  CONSTR, CLROBS, MINLAY, RESCUE, RECOVR, NTRCOM, ESCRT/FOLASS, plus
  follow/escort over `RelativeLocation`), and only a general-purpose tow/salvage
  verb is a residual (closest: `TOWTGT`, gunnery targets only; the broad
  `RECOVR` may already cover salvage). Effects, targets, and resources already
  exist.
  (Resolves L1/L2/E2/W2/N2; E1/R2 are minor residuals.)
- **Q-M [deck]** Allow an **area** to be the subject of a task and a report -
  an `hasAffectedArea` counterpart to `hasAffectedEntity`, and an area-state
  (cleared / contaminated / mined). Areas (`TacticalArea`, `MapGraphic`) exist;
  tasking/reporting on them does not. (Resolves N1.)
- **Q-N [deck]** Add an **area-coverage / exploration goal** (explore-until-covered)
  on top of the existing search/recce verbs (`RECCE`, `PATROL`, `SWEEP`), so
  autonomous area exploration is expressible beyond a fixed patrol route.
  (Resolves G2.)
- **Q-O [deck]** Model **denied-comms operation**: a comms-degraded operating
  mode and a deployable relay entity/node (the relay verb `lox#COMREL` already
  exists). (Resolves G1.)
- **Q-P** Extend robot-to-robot (Q-G) with **cross-cueing**: system-to-system
  tasking plus a shared classified **track/contact** object. (Resolves G3.)
- **Q-Q [deck]** Define one **generic parameterized Detection Report**
  (confidence + error-bound + false-positive + modality) that subsumes the
  per-sensor reports. Extends Q-I. (Resolves G4 / Y1 / M3 / M4.)
- **Q-R** Add **platform locomotion/role subtypes** (wheeled/tracked/legged UGV;
  detector/neutralizer USV). Extends Q-A. (Resolves G5.)
- **Q-S** Add **decoy/deception** as a taskable behavior and **threat-aware**
  order annotations (risk, low-signature, level-of-autonomy). (Resolves G8/G9.)
- **Q-T** Add **operating-environment condition** attributes (GPS-denied,
  illumination, sea-state, terrain, domain) to `RoboticEnvironment`. (Resolves G11.)
- **Q-U** Add a **formation / relative-geometry** construct (orbit, convoy
  spacing, observation-pose pattern) beyond single `RelativeLocation`. (Resolves G12.)
- **Q-V** Add **capability self-report** (a robot declares its mounted/reconfigurable
  equipment; tasks assigned by capability) - BML `WhoHoldingType`. (Resolves G13.)
- **Q-W [deck]** Model a **weapons-control-status + engagement-authorization area**
  (kill box): an area that carries a weapons-control status (hold/tight/free), a
  civilian-clearance state, a time window, and permitted target types, and that gates
  whether an autonomous system may take a lethal action inside it. This unifies Q-K
  (engagement authority) and Q-M (area as subject) and gives both a concrete,
  doctrine-grounded shape; the graded/phase-varying form ties to Q-D. (Resolves G14/G15;
  sharpens Q-K/Q-M.) This is the drone-warfare thread's highest-value contribution: the
  standard's hardest ASX question (may an autonomous system take a lethal action, and
  under what approval?) gets a proposed element from real doctrine, not just a restated
  gap.
- **Q-X** Type **loitering munitions / FPV** as a platform-munition hybrid with size
  tiers (mini/tactical/long-range), and add **counter-UAS** as a detect->defeat coupling
  over the existing air-defense verbs (`AIRDEF`/`ENGAGE`/`JAM`) with an sUAS target
  class; include an **EW-vulnerability / countermeasure** annotation for adversary
  GPS-denial and control-link seizure. (Resolves G16/G17/G18; extends Q-L/Q-R/Q-O.)
- **Q-Y [deck]** Decide whether **sensor characterization becomes its own
  extension** (a sibling to ASX) or stays a section inside ASX. For: the finding
  count (G20) and the four-question structure - device / capability / observation
  / configuration - that no single current ASX element addresses. Against: it
  fragments the standard, and the sensor model's main consumer is ASX itself.
  Decide **explicitly and early**, because the answer changes *where* Y1-Y5, D2,
  P2, M3-M5, G4, G13, Q-C, Q-F, Q-I, Q-P, Q-Q and Q-V get resolved. (Scopes
  G20-G22; see `Sensor-Characterization-Slice.md`.)
- **Q-Z** Decide **which lessons ASX draws from DIS as a design source**. This is
  *not* a question about using the codes - C2SIM entities already carry the DIS
  record, and nothing proposed here changes how or whether it is populated. Three
  independent options, takeable in any combination: **(a) vocabulary governance**
  - apply the SISO-REF-010 management principles to ASX's own code lists (D1,
  `SensorType`, `MediaTypeCode`); touches no DIS content at all. **(b) carving
  criteria as ASX modeling rules** - restate the component/whole criterion (G25)
  and the type/instance line (G27) in ASX's terms, applied to Q-C/P2/D2 and
  M1/Q-E. **(c) taxonomic content as evidence** - use DIS's kinds as a checklist
  of what a mature vocabulary found it needed, and ask which ASX is missing
  (relay node, environment condition, decoy, class of supply) (G24).
  Recommended: **(a) and (b) now** - cheap, self-contained, and they sharpen open
  decisions; **(c) as the placement exercise**, the only part producing a
  testable result. Each transfer under (c) argued on ASX's own terms, since DIS's
  boundaries answer a simulation's questions, not a commander's. (Scopes G24-G27;
  see `DIS-Enumerations-Slice.md`.) G23 is separate - a workbook fix worth making
  regardless.
- *The Q-series is exhausted at Q-Z. Continue at Q-AA.*
- **Adopt (evidence-backed), not just decide:** Q-Q should re-adopt BML
  `WhoMeasuredType` (measurement report) and Q-F align to BML `ResourceType`
  (media report) - both prior art in C2SIM's BML lineage (Remmersmann 2015).
  Corroborated by the sensor slice (6l/G21): W3C/OGC SOSA `Observation` lands on
  the same shape from an independent lineage, and the DIS parameter records
  (6m/G26) supply the units.

## 8. Why the identified gaps are not yet filled

"Lacking documents" is one cause, but the minority one. The gaps fall into three
separable buckets, and only the third is about sources:

1. **The property/attribute layer is still being built (most gaps).**
   `CSIM_ASX.rdf` v0.0.1 was "work in progress": ~15 classes, **1 object
   property, 0 datatype properties** - a taxonomy of *things* whose message
   layer had not been built yet. (v0.0.3 has now begun that layer for the Video
   Detection Report - see section 9 - so this is being addressed, not a
   standing defect.) The classes are imported robotics
   upper-ontology terms (Robot, Sensor, Actuator, Device - CORA/ORA/SUMO
   lineage), i.e. a *taxonomy of things*. The *message layer* - the attributes
   you actually need to send - was never derived. So most "gaps" are simply
   not-yet-built, not blocked. Bottom-up instantiation surfaces them because it
   does the derivation the OWL skipped. No document fills these - modeling does.

2. **Deferred decisions and track desync (information already in hand).**
   P1 (UAV double-typed vs SMX Platform), P7 (swarm typing), D1/D2 (autonomy and
   sensor each defined three ways) are unresolved *choices*, plus the OWL track
   (Jan) and the spreadsheet track (Jun) being at different stages. Cross-cutting
   abstractions - generic Detection Report (G4), area-as-subject (N1),
   engagement-authority-vs-autonomy (W1) - are modeling insights reachable from
   scenarios already in hand. These need a decision or an abstraction, not a
   source.

3. **Genuine document/scenario gaps - but for DOMAINS and VALIDATION, not
   concepts.** Here "lacking documents" really bites, in two forms:
   - *Invisible-domain gaps:* the scenario library was narrow (all UAV/UGV
     air-ground recon/escort). No maritime/undersea/subterranean case existed, so
     no one saw USV/UUV (P1/G6), denied-comms/relay (G1), locomotion subtypes
     (G5), formation geometry (G12), or environment conditions (G11) were needed.
     These were unfilled *because the revealing documents were not in the
     corpus.* Sourcing them (MCM/SubT) is exactly the fix, and it worked.
   - *Validation holes:* explainability, CBRN/EW, CASEVAC coordination, and
     persistence are asserted/intended in the model but **no sourced mission
     exercises them** (sourcing session's Reading 1). Here the model ran ahead of
     the documents - the concept exists with no source to ground it. Targeted
     sourcing (a CBRN mission, an explainability/on-the-loop mission, a
     persistent-sentry mission) fills these.

**Bottom line:** the domain-coverage and validation gaps (bucket 3) do reflect a
document shortfall and are being closed by the sourcing effort; but the larger
share - the missing property/message layer, unmade typing/vocabulary decisions,
track desync, and cross-cutting abstractions (buckets 1-2) - are not document
problems and no amount of new scenarios fills them. It takes bottom-up
instantiation to see which is which.

## 9. Reconciliation with C2SIM_ASX v0.0.3 (Michael's update)

Michael committed a v0.0.3 ASX ontology on branch `michael_d` (OWL/XML,
`Ontology/C2SIM_ASX-v003.rdf`, annotated "introduces concepts for Video
Detection Report"), plus merged ontologies and a derived XSD schema, and edits
to base `C2SIM.rdf`. It is a **new file in a new location**; the v0.0.1
(`Subgroups/ASX/Proposed Extension/CSIM_ASX.rdf`) still exists too. This review's
findings were grounded on v0.0.1; here is how each moves against v0.0.3.

Counts: v0.0.1 = 15 classes / 1 object prop / **0 datatype props**; v0.0.3 =
26 ASX classes / 4 object props / **2 datatype props**, plus a `MediaTypeCode`
code list and an `AutonomyLevelCode` model. (Of the six new properties, four are
object properties over code lists / time instants - `hasMediaTypeCode`,
`hasCreationTime`, `hasLastModifiedTime`, `hasAutonomousRoleCode` - and two are
datatype - `hasAnalystName`, `hasRepositoryReference`.) So the property layer has *begun*
(for the Video Detection Report), and much of the review's direction is being
adopted - the model is moving, as expected for a WIP.

**Advanced / being adopted in v0.0.3:**
- The **attribute layer has started**: `hasMediaTypeCode`, `hasCreationTime`,
  `hasLastModifiedTime`, `hasAutonomousRoleCode`, `hasAnalystName`,
  `hasRepositoryReference`. -> requalifies D3 and section 8 (no longer "0
  datatype properties" for the current model; still only the media/report slice).
- The **Video Detection Report** is now in the OWL: `MediaReference`,
  `MediaTypeCode` {VID/AUD/IMG/DOC/TXT/NOS}, `AnalysisConcept`, `AnalysisComment`,
  `VideoDetectionReportContent subClassOf ReportContent`, `SensorObservation`.
  The Report-side spreadsheet work is being folded in.
- An **AutonomyLevelCode** class + individuals (Automated/FullAuto/ReCont/Teleop)
  - a definite OWL autonomy model (one of the three D1 vocabularies).
- **M2** partly settled for `AnalysisComment`: it carries `hasRepositoryReference`
  (UUIDBase, exact cardinality 1) - a repository-reference identity was chosen for
  the comment. Note: `MediaReference` itself still has no identity property in
  v0.0.3 (its only axioms are `subClassOf AnalysisConcept`, `hasStartTime` /
  `hasEndTime some TimeInstant`, and `hasMediaTypeCode exactly 1`), so
  MediaReference identity (decision Q-F) remains open.

**Confirmed / now concrete in v0.0.3 (the decisions are live in the model):**
- **P1** is instantiated: v0.0.3 declares *both* `UAV`/`UGV subClassOf Robot`
  AND `UnmannedAerial/Ground/Maritime/UnderwaterVehicle subClassOf smx#Vehicle`.
  Two class sets for the same things - exactly the typing decision to settle.
- **New (V1):** `UnmannedMaritimeVehicle` / `UnmannedUnderwaterVehicle` are under
  `smx#Vehicle` - a direct `Platform` sibling of `Aircraft` / `SurfaceVessel` /
  `SubsurfaceVessel` whose rdfs:comment says "most often applies to ground
  vehicle". SMX already has `SurfaceVessel`/`SubsurfaceVessel` for maritime;
  worth re-parenting the maritime pair there.
- **Y1/Y5/M5**: v0.0.3 committed to the media-based report (`MediaReference` +
  `MediaTypeCode`, with `NOS` "Not Otherwise Specified"), so the "doesn't
  generalise to non-imaging sensors / no measurement value+unit / media-type
  conflation" items now apply to the actual model; the generic Detection Report
  (G4/Q-Q) is still to define.
- **M4**: `SensorObservation subClassOf smx#ActivityObservation` is now committed
  in the OWL - the parent worth reconsidering.

**Still to define (v0.0.3 does not yet touch):**
- A taskable collective (P7): the `Swarm` class was **removed** in v0.0.3, and
  `CollecticeRoboticSystem` is still under `PhysicalEntity`.
- The broader attribute set (Payload, Mobility, VehicleType, SensorType, Swarm
  parameters); the generic Detection Report (G4); rationale (X2), robot-to-robot
  (X1), engagement authority (W1), area-as-subject (N1) content.
- **O1/O2 typos still present** in v0.0.3 (`CollecticeRoboticSystem`,
  versionInfo "Extrension").

**Additional v0.0.3 observations (added 2026-07-12, on re-verification):**
- **Import layering / circular import.** The `michael_d` edit to base
  `C2SIM.rdf` adds `owl:imports smx` and `owl:imports lox` to the *base*
  ontology header (its only substantive change; the rest of the diff is OWL-API
  re-serialization). Since `C2SIM_SMX.rdf` imports C2SIM, this creates a
  circular import (C2SIM <-> smx) and inverts the base<-extension layering -
  worth a deliberate decision. Relatedly, v0.0.3's own import set grew: v0.0.1
  imported only `lox`; v0.0.3 imports `C2SIM`, `lox`, and `smx`.
- **New `Operator` class** (`subClassOf C2SIM#Person`), not previously
  inventoried here; its comment carries a third typo ("semi,autonomous").
- **The two halves of the autonomy model are not yet wired together:**
  `hasAutonomousRoleCode` keeps its v0.0.1 declaration (range generic
  `C2SIM#Code`, no domain, no restriction attaching it to Robot or any entity -
  P3 still holds) even though `AutonomyLevelCode` now exists as its obvious
  range.
- **`MediaTypeCode` has no superclass** - unlike `AutonomyLevelCode
  subClassOf C2SIM#Code` - inconsistent with the C2SIM code-list pattern.
- **`VideoDetectionReportContent` is a bare subclass of `ReportContent`** - no
  restriction links it to `MediaReference` / `AnalysisConcept` /
  `SensorObservation`, so the Video Detection Report pieces are structurally
  disconnected from the content class itself.
- **Vacuous axioms:** `AnalysisComment`'s min-0 cardinality restrictions
  (`hasCreationTime`, `hasLastModifiedTime`, `hasAnalystName`) constrain
  nothing.
- Support files: `catalog-v001.xml` has a duplicate mapping for the smx IRI;
  the derived schema `Derived products/Schema_C2SIM_smx_lox_asx.xml` is an XSD
  misnamed `.xml`.

**Groundings intact:** Michael's `C2SIM.rdf` edits keep every base class the
review cites (`CollectiveEntity`, `PositionReportContent`, `hasSubordinate`,
`hasAffectedEntity`, `DesiredEffectCode`, `AuthorizationHeader`, ...), and SMX/LOX
are untouched - so the review's RDF-verified facts still hold. (One base-standard
nit found while re-verifying, offered upstream: `AuthorizationHeader`'s two
cardinality restrictions use `owl:onDataRange C2SIM#angle` - `C2SIM.rdf` lines
1917/1924 - almost certainly not the intended range.)

**Coordination note:** two ASX ontology files now exist (v0.0.1 in
`Subgroups/ASX/Proposed Extension/`, v0.0.3 in `Ontology/`) on two branches; the
group should converge on one canonical version/location.

## Change log

- 2026-07-09: Log created. Consolidated findings from OWL review, spreadsheet
  vs OWL drift analysis, sample-message inspection, and the Initialization walk.
- 2026-07-10: Converted the 3 sample-message workbooks to diff-able `.xml`
  (fidelity verified), applied the Initialization instantiations to the `.xml`,
  generated the findings deck. Added S4 (dual source of truth); updated S3, C1.
- 2026-07-10: Walked CASEVAC end-to-end (`CASEVAC-Walk.md`). Added section 6b
  (X1-X6) and decisions Q-G/Q-H; updated C2. Grounding check killed two false
  gaps (Route and phased-planning both already exist in the standard).
- 2026-07-10: S4 decided - `.xml` is the working copy, `.xlsx` left untouched.
  Added 5 CASEVAC tabs to the `.xml` workbooks (verified via LibreOffice
  round-trip; existing sheets preserved). Reviewed the annotations on the worked
  scenarios; most align with these findings, and the two open typing questions
  they raise (MediaType and SensorObservation parent) are logged as M5/M4, plus
  the M3 cross-sheet inconsistency.
- 2026-07-10: Walked non-video sensors (`NonVideoSensors-Walk.md`); added 3
  report tabs (CBRN / EW Emitter / GPR Mine) to the `.xml`. Added section 6c
  (Y1-Y5) and decision Q-I; updated C4. Grounding check confirmed the gaps are
  real (no measurement/hazard Observation subtype; no sensor-reading value+unit;
  no CBRN/EW-sensing/radar *sensor or observation* classes - `smx#NBC_Event` is
  a map-symbol class and LOX has CBRN *sampling* task verbs, neither carries a
  reading).
- 2026-07-10: Walked swarm (`Swarm-Walk.md`); filled the `Swarm Detection` stub
  (Report) and added `Swarm Coordination` (Order). Added section 6d (Z1/Z2),
  decision Q-J; updated C5. Grounding narrowed P8 - membership/command already
  exist in the base standard (C2SIM `hasSubordinate`, SMX `hasCommandRelation`).
- 2026-07-10: Walked Fire Support (`FireSupport-Walk.md`) - opens the task/effect
  axis; added `Fire Support Order` + `BDA Report` tabs. Added section 6e (W1-W3),
  decision Q-K, coverage C6; deck gained a Fire Support slide and split decisions
  into 2 slides. Grounding narrowed the finding: ROE already exists (LOX); the
  real gap (W1) is the autonomy-to-engagement-authority link (AuthorizationHeader
  is only message-sender authentication, not command authorization).
- 2026-07-10: Integrated the parallel scenario-sourcing session's output
  (SubT, Cooperative MCM, Sustainment + `OntologyConceptCoverage.md`), which
  had been missed earlier when its commits were wrongly filed as unrelated.
  Walked all three (`SourcedScenarios-Walk.md`), added 7 tabs, section 6h
  (G1-G10) and decisions Q-N..Q-S. Correction: the earlier "findings converged"
  call was premature - this input extended the findings (esp. G4 generic
  Detection Report, G1 denied-comms, G2 explore). Grounding narrowed G6/G10.
- 2026-07-10: Re-synced against the sourcing session's revised concept-coverage
  doc (a150ffb -> `OntologyConceptCoverage.md`). Mostly aligned; added G11
  (environment conditions) and G12 (formation geometry) that I had under-covered,
  decisions Q-T/Q-U, and section 8 ("why the gaps are not yet filled").
- 2026-07-10: Integrated the sourcing track's nine sourced missions
  (`Documents-Found.md` / V2Extractions). Section 6j, coverage C8, G13/Q-V, two
  tabs. Bucket-3 validation holes now evidenced; key result: the measurement
  report (Q-Q) is prior art in C2SIM's BML lineage (WhoMeasuredType) - re-adopt,
  don't invent. Buckets 1-2 (property layer, ~22 decisions) unaffected.
- 2026-07-10: Redundancy pass over route-clearance / companion / urban
  (`RedundancyPass-Walk.md`). Confirmed ~80% redundant; extracted N1 (area as
  subject of task/report - new) and N2 (folds into Q-L). Added section 6g,
  decision Q-M, and a `Route Clearance Order` tab demonstrating N1.
- 2026-07-10: Batched Logistics + Engineering + USV Rescue
  (`TaskEffect-Batch-Walk.md`); added 4 tabs (Logistics Delivery Order,
  Engineering Task Order, USV Rescue Order, Delivery Confirmation Report). Added
  section 6f (L/E/R), decision Q-L. Grounding: Resource/quantities and
  SurfaceVessel already exist; the task/effect axis distills to task verbs +
  payload/effector/weapon typing.
- 2026-07-11: Re-baselined the whole review against Michael's `C2SIM_ASX-v003.rdf`
  (v0.0.3, on `origin/michael_d`). Added section 9 (full reconciliation): which
  findings the update advances/adopts (attribute layer started, Video Detection
  Report folded into the OWL, P1 typing made concrete), which are confirmed by it
  (P1 dual hierarchy; new V1 - UnmannedMaritime/UnderwaterVehicle mis-parented
  under `smx#Vehicle`), which remain to define (taskable collective - `Swarm`
  class dropped, `CollecticeRoboticSystem` still non-actor; broader attribute set;
  the new content types), and that the P9 typos survive. Groundings intact; noted
  the two-ASX-file coordination point (`CSIM_ASX.rdf` vs `C2SIM_ASX-v003.rdf`).
- 2026-07-11: Tone reframe to work-in-progress across the shared artifacts (deck,
  briefing, presenter notes, Q&A, coverage, and the walk docs). Findings are
  presented as things *still to be defined* in a v0.0.x model, not as defects:
  severity legend BLOCKER -> DECIDE-FIRST (a foundational typing decision to
  settle first, not a stopper); "defect/gap" -> "not-yet-defined item / gap";
  "cannot be tasked" -> "not yet taskable"; "two tracks drifted" -> "at different
  stages"; "0 datatype properties ... never built" qualified as the v0.0.1
  baseline with v0.0.3 starting the layer. No verified fact changed - only framing;
  the genuine model bugs (typos, mis-parenting) are still called out in section 3.
- 2026-07-12: Independent verification pass over the whole review (every
  RDF-grounded claim re-checked against C2SIM/SMX/LOX and v0.0.3; `.xml`
  workbooks re-compared cell-for-cell against the `.xlsx`; deck regenerated and
  diffed; all cross-references and citations traced). Corrections applied:
  D2's "two SensorType rows disagree" was wrong (they are identical duplicates;
  the real ConceptMapping disagreements are Payload and VehicleType); M5 - the
  sample-message `MediaTypeEnum` already had five values incl. "Not Otherwise
  Specified" (so v0.0.3's NOS is not new); V1 - `smx#Vehicle` is a direct
  Platform sibling, "land" only by comment; R2/Q-L - qualified with `lox#TOWTGT`
  (gunnery-target towing) and the broadly-defined `RECOVR`; the CBRN grounding
  narrowed to "no *sensor/observation* classes" (`smx#NBC_Event` symbol class
  and LOX sampling verbs exist); namespace precision (smx# on
  ObservationReportContent / hasConfidenceLevel); stale labels aligned (X2
  severity, P8 narrowing in the Init walk, the USV-rescue R2 workbook cell);
  remaining pre-reframe phrasing swept. Section 9 gained the re-verification
  additions (import layering/circular import, `Operator` class, unwired
  AutonomyLevelCode range, bare `VideoDetectionReportContent`, vacuous min-0
  axioms, support-file nits) and the base-standard `AuthorizationHeader`
  onDataRange nit. Reference corpus: two byte-identical duplicate PDFs removed;
  two extraction records' source-location claims corrected to web-only; broken
  relative links fixed; SAR source substitution (Kim 2021 for the MDPI-2020
  candidate) noted where the candidate is listed. Deck regenerated (still 23
  slides). No headline finding changed.
- 2026-07-12: Added a process slide to the deck (slide 3): the three coordinated
  sessions - document mining, scenario extraction (locked v2.2 prompt), and
  ontology application (the instantiation walks) - plus the independent
  verification pass, with the iteration loop (walk -> sourcing brief -> mining ->
  extraction -> walk) called out. Deck is now 24 slides; briefing and presenter
  notes updated to match.
- 2026-07-12: Deck navigation/scaffolding pass (deck now 26 slides): added a
  "What this review contributes" slide (the five deliverables, stated up front),
  a "How to use this material" reading guide (paths by time budget, how to read
  the workbooks' [!]/[Q] flags, how to challenge a claim, and the finding-ID
  legend), and a per-slide "Dig deeper" line on every content slide naming the
  walk doc / log section / workbook tabs behind it. Briefing and presenter notes
  updated to match.
- 2026-07-13: Deck presenter-notes + orientation pass (deck now 29 slides,
  with a consistent onboarding style): the talk track is
  embedded as per-slide speaker notes (team-facing; includes a per-section
  time budget for a 30-minute slot and a 20-minute fallback); added a
  one-slide summary up front ("The whole review in one slide"), rebuilt "How
  to use this material" as a reading-paths-by-time-budget table, and added a
  finding-ID decoder-ring table slide. Presenter-Notes.md is now the
  section-level view of the same track (stale 26-slide count corrected).
  Also brought the InstantiationReview docs on this branch up to the
  verification-pass state so the deck's references resolve here.
- 2026-07-13: Reconciled the one lagging file with v0.0.3. The
  scenario/concept coverage analysis
  (`LLMExperiments/OntologyConceptCoverage.md`) had still been framed against
  v0.0.1 (it predated the v0.0.3 re-baseline that updated this folder). Updated
  its Grounding to note v0.0.3 as the moved-on live model (pointing here to
  section 9 for the full delta), corrected the report-attribute names to the OWL
  forms (`AnalysisComment` / `MediaTypeCode`, noting the sample-message data
  still carries the old `AnalystComment` / `MediaTypeEnum` labels pending a
  ratified rename), and annotated the Reading-2 expressiveness gaps that v0.0.3
  now closes (maritime USV/UUV) or partly touches (AutonomyLevelCode; media-based
  report). No other InstantiationReview file needed changes - the folder was
  already reconciled and verified against Michael's actual file.
- 2026-07-17: Integrated the SME-directed drone-warfare thread (Morris 2018 LIRC
  baseline + 2022-2024 Infantry Magazine threat/TTP update + Rosenberg JPMRC-AK 24-02
  OPFOR commercial-sUAS targeting), extracted in
  `LLMExperiments/PaperSummaries/V2Extractions/` and walked in
  `DroneWarfare-LIRC-OPFOR-Walk.md`. Added section 6k (G14-G19), coverage C9, decisions
  Q-W (weapons-control-status + kill-box authorization area) and Q-X (loitering-munition/
  FPV typing + counter-UAS + EW vulnerability), and 5 `.xml` tabs (LIRC Company Init;
  LIRC Kill-Box Engagement Order; Counter-UAS Defeat Order; OPFOR Targeting Handoff;
  LIRC Strike BDA Report). Headline: the LIRC kill-box / weapons-control mechanism is a
  concrete candidate answer to the review's most central open finding (W1/Q-K,
  autonomy-to-engagement-authority) and unifies it with N1/Q-M (area as subject);
  grounded against C2SIM/SMX/LOX (weapons-control-status, kill box, loiter/munition,
  target-list all absent; the air-defense/engage/jam verbs and ROE exist and are
  reused). Corroborated W1/W2/W3/N1/N2/G3/G7/G8/G11/D1. The `.xlsx` originals remain
  untouched (S4); each `.xml` file's existing line-ending convention was preserved
  (additions only).
- 2026-07-17: Reconciled the drone-warfare thread across all shared artifacts (overall
  consistency pass). Extended the sourcing session's concept bridge
  (`LLMExperiments/OntologyConceptCoverage.md`) with S7-S9 (LIRC baseline / update /
  OPFOR) - a compact concept-x-scenario matrix plus both readings updated (they close
  the task/effect + graded-LoA + ROE/C2 validation holes and add the engagement-authority
  / kill-box expressiveness gap). Synced every count that the integration changed:
  message instantiations 4 -> ~38 (Init 0 -> 7, Orders 2 -> 17, Reports 2 -> 14);
  decisions ~22 (Q-A..Q-V) -> ~24 (Q-A..Q-X); coverage C1-C8 -> C1-C9; sourced-record
  corpus 12 -> 15 - across Group-Briefing.md, this log, the InstantiationReview README,
  Presenter-Notes.md, and Anticipated-QA.md. Regenerated the findings deck from
  `build_findings_deck.py` (counts + the kill-box/Q-W candidate answer on the Fire
  Support slide + Q-W/Q-X in the decision register + decoder ring); verified it
  programmatically (still 28 slides; new anchors present, stale ones gone). Corrected a
  pre-existing stale slide count in the briefing / presenter notes (the deck is and was
  28 slides, not 29; committed and regenerated .pptx both 28) and the matching
  reading-guide slide-number references. No verified finding changed; this pass only
  propagates the drone-warfare additions and fixes the counts they touched.
- 2026-08-12: Added **two proposed slices** (scoping only; nothing instantiated)
  from two items suggested by Curt, kept as **separate, independent** documents
  because the items are independent - DIS was raised as a rich source that might
  inform ASX in general, not as an input to the sensor question:
  `Sensor-Characterization-Slice.md` (log section 6l, G20-G22, decision Q-Y) and
  `DIS-Enumerations-Slice.md` (section 6m, G23-G29, decision Q-Z). Where DIS
  genuinely bears on sensors it is cross-referenced (G25/G26), not merged. New
  status value **PROPOSED** added to the legend. The Q-series is now exhausted at
  Q-Z; continue at Q-AA.
  The DIS slice is explicitly framed as **inspiration, not code adoption**: the
  codes are already carried by C2SIM entities, so what is open is whether ASX
  learns from the reasoning and taxonomy behind them - not whether to populate
  septuplets. Q-Z is scoped accordingly (governance principles / carving criteria
  / taxonomy-as-evidence), and section 3.4 records the counterweight: DIS's
  boundaries were drawn so a simulation can render and interact, ASX answers to
  what a commander must state or be told, and some boundaries will not survive
  that translation.
  Grounding results worth recording independently of whether either slice runs:
  (a) the walks type entities with `hasEntityType` / `EntityType`, which exists
  in **no** C2SIM/SMX/LOX file, while the standard already defines
  `hasNamedEntityType` and `hasSISOEntityType` (G23 - a workbook hygiene defect,
  self-inflicted, independent of the DIS question); (b) SISO-REF-010 reduces to
  four table shapes - `enum`, `bitmask`, `cet`, `cot` - plus metadata, over a
  `Kind.Domain.Country.Category.SubCategory.Specific.Extra` septuplet, and at
  least eight of its nine Entity Kinds bear on open ASX findings (G24);
  (c) the sensor cluster is extension-sized by the log's own count - 15 findings
  and 6 decisions (G20) - and the capability layer is entirely absent with an
  off-the-shelf vocabulary available (G22); (d) two base-standard defects found
  in passing - the `hasDIS*` properties mis-cite DIS as IEEE 1516 (it is IEEE
  1278.1 / SISO-REF-010; G28) and type six unsigned 0-255 fields as signed
  `xsd:byte` (G29). Both are for the parent group, not ASX. Deck not regenerated
  - G20/G23/G24 are marked [deck] for the next deck pass.
