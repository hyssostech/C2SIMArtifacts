# ASX Review - Issues & Comments Log

Running log of issues, defects, and comments found while reviewing the proposed
ASX ontology elements against the scenarios and the sample-message
instantiations. This is the working source; the planned findings PowerPoint is
generated from it. Kept current as work proceeds.

Severity: **BLOCKER** (stops a message being instantiated) / **HIGH** /
**MED** / **LOW** / **TYPO**. Status: **OPEN** / **RESOLVED**, plus qualified
states used in the tables (all variants of in-progress or partially-resolved):
**PARTIAL**, **NARROWED**, **MOSTLY COVERED**, **MOSTLY REUSE**, **WALKED**,
**INSTANTIATED**, **EVIDENCED**, **DECIDED**, **DONE**, **FOLDS INTO Q-x**.
Items marked **[deck]** are candidates for the findings presentation.

## 1. Repo sync & process

| ID | Sev | Status | Item | Evidence / note |
|---|---|---|---|---|
| S1 | HIGH | RESOLVED | Local clone was 52 commits behind origin/main | Fixed by pull on 2026-07-09; now level with origin (`021e715`). |
| S2 | HIGH | OPEN | Two work tracks are out of sync: OWL/RDF vs spreadsheets | OWL `CSIM_ASX.rdf` last updated 2026-01-20; spreadsheets updated 2026-06-10. Different tools, different altitudes. **[deck]** |
| S3 | MED | DONE (branch) | Workbooks are `.xlsx` (zipped XML), git cannot merge | All 3 sample-message workbooks converted to diff-able SpreadsheetML 2003 `.xml` (fidelity verified, 0 mismatches) and committed on branch `asx-diffable-spreadsheets`. NOTE: `.xml` and `.xlsx` now coexist - see S4. |
| S4 | HIGH | DECIDED | Dual source of truth: `.xml` vs `.xlsx` | Decision (2026-07-10): the `.xml` workbooks are the working copy for this review; Elizabeth's `.xlsx` files are left untouched for now. All new instantiation work (Init rows, CASEVAC tabs) goes into the `.xml` only. The `.xlsx` will diverge by design until the group reconciles. |

## 2. Model drift: OWL vs Spreadsheet vs Deck

| ID | Sev | Status | Item | Evidence / note |
|---|---|---|---|---|
| D1 | HIGH | OPEN | Autonomy vocabulary defined three incompatible ways | OWL individuals {Automated, FullAuto, ReCont, Teleop}; ConceptMapping `Control Mode` {Piloted, Unpiloted-Autonomous, Swarm}; `NavigationAutonomy` {FPV, Autonomous, RemoteControl}. Which is normative? **[deck]** |
| D2 | HIGH | OPEN | Sensor modeled three incompatible ways | OWL `Sensor` class; ConceptMapping `SensorType` enum; `SensorCapability` equipment. Two ConceptMapping rows even disagree on values. **[deck]** |
| D3 | HIGH | OPEN | Entire attribute layer missing from OWL | Payload, PayloadCapability, Mobility/Propulsion, VehicleType, PassengerCapability, AutonomousMissionFunction/Parameters, SwarmParameters exist in ConceptMapping but not in `CSIM_ASX.rdf` (0 datatype properties, 1 object property). **[deck]** |
| D4 | MED | OPEN | Deck (June) proposes `Sensors subClassOf RobotPart`; OWL has `Sensor subClassOf ElectricDevice`, no RobotPart class | Slide 6 of 2026-06 status deck vs `CSIM_ASX.rdf`. Robotics-concept discussion not captured in model. |
| D5 | LOW | OPEN | Deck frames robotics subclass axioms as an open question, but OWL already committed them | UAV/UGV subClassOf Robot etc. asked as "Do we want to add...?" in June yet present in Jan OWL. |

## 3. OWL internal defects (`CSIM_ASX.rdf`)

| ID | Sev | Status | Item | Evidence / note |
|---|---|---|---|---|
| O1 | TYPO | OPEN | Class name misspelled `CollecticeRoboticSystem` (should be "Collective") | Line 44-45; `Swarm subClassOf` the misspelled class. Will propagate into instance data once messages exist. **[deck]** |
| O2 | TYPO | OPEN | `versionInfo` says "Autonomous Systems Extrension" | Line 13. |
| O3 | LOW | OPEN | File named `CSIM_ASX.rdf` (missing the "2") | Inconsistent with every other C2SIM artifact; expected `C2SIM_ASX.rdf`. |

## 4. Sample-message instantiation defects

| ID | Sev | Status | Item | Evidence / note |
|---|---|---|---|---|
| M1 | HIGH | OPEN | `actorReference` is `string` but must define a not-yet-known entity | Report Base Attributes note: "Observed Entity likely does not already exist... needs to be defined in the report." A string can't carry an entity definition. **[deck]** |
| M2 | MED | OPEN | `MediaReference` identity triple-defined | repositoryReference(UUID) + reportReference(string) + url(string), note "String may be better." Unresolved. |
| M3 | MED | OPEN | Same concept modeled two ways across two report sheets | media/analystComment placed on ActivityObservation/LocationObservation in one sheet vs. a new `SensorObservation` subclass in another. Which is normative? |
| M4 | MED | OPEN | `SensorObservation subClassOf ActivityObservation` is questionable | A sensor location fix is a LocationObservation; sensor output is not inherently an activity. |
| M5 | MED | OPEN | `MediaTypeEnum` conflates media format with sensor modality | Values Video/Audio/Image/Document, but note asks it to also cover "thermal scan" (a sensor type). Category error. **[deck]** |
| M6 | MED | OPEN | Order task payload not modeled | "New Route Pattern" / "New Location" appear as bare rows with no type under the UAV Change Patrol Route Task. |
| M7 | HIGH | OPEN | `hasStartTime` typed `UUIDBase` | Both Order sheets; `hasEndTime` is `TimeInstant`. Almost certainly a copy-paste error. **[deck]** |
| M8 | LOW | OPEN | Namespace label drift | `C2SIM_ASX` (Order, Report Base) vs `ASX` (Video Detection Report) for the same model. |

## 5. Initialization walk - entity-typing findings (headline)

(Note: the P-series is intentionally non-contiguous - P4 was retired/merged
during the walk. The P-IDs are stable cross-reference handles and are not
renumbered.)

| ID | Sev | Status | Item | Evidence / note |
|---|---|---|---|---|
| P1 | BLOCKER | OPEN | UAV typed twice, incompatibly: ASX `UAV subClassOf Robot subClassOf ActorEntity` vs SMX `Aircraft subClassOf Platform subClassOf ActorEntity` | Disjoint sibling trees. `Robot` orphans the drone from Platform machinery; `Aircraft` leaves ASX classes unused. **[deck]** |
| P2 | BLOCKER | OPEN | Sensor: separately-declared entity, or attribute on platform? | Init must pick one; Report side only consumed sensor output. Ties to D2. **[deck]** |
| P3 | HIGH | OPEN | `hasAutonomousRoleCode` has no attachment point on the entity | Defined in OWL, but no Init field and not on EntityDescriptor. |
| P5 | HIGH | OPEN | Patrol route/area not modeled as an init object | Order references a route to change; nothing declares the baseline. Can host as MapGraphic. Gap on both Init and Order sides. Ties to M6. |
| P6 | HIGH | OPEN | Three competing autonomy vocabularies at init time | Same as D1, surfaced concretely when declaring an entity. |
| P7 | BLOCKER | OPEN | Swarm cannot be tasked as modeled | `Swarm subClassOf CollecticeRoboticSystem -> ... -> PhysicalEntity` (inert), but swarms receive orders and send reports (need ActorEntity). Base C2SIM has `CollectiveEntity subClassOf ActorEntity`. **[deck]** |
| P8 | HIGH | NARROWED | Swarm membership + leader partially covered | `hasSubordinate`/`hasSuperior`/`hasCommandRelation` (base) cover membership + command; residual gap is network params, leader-as-role, and dynamic handover. See section 6d. |
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
| C8 | HIGH | EVIDENCED | Validation holes (explainability, CBRN, EW, persistence) unexercised by any sourced mission | Scavenger extracted all 9 `Documents-Needed` requests; integrated in `ValidationEvidence-Walk.md` (6j). Holes now grounded; Q-Q/Q-F/Q-H gain concrete schemas (BML WhoMeasuredType/ResourceType; Agrawal explanation). Added G13/Q-V; 2 tabs. **[deck]** |

## 6b. CASEVAC walk findings (from CASEVAC-Walk.md)

| ID | Sev | Status | Item | Evidence / note |
|---|---|---|---|---|
| X1 | HIGH | OPEN | No robot-to-robot coordination content type | Envelope addressing (isFromSender/isToReceiver) supports peer messages, but no ReportContent/OrderBody wraps "verified safe route, use it"; UGV-as-issuer authority unclear. CASEVAC scout->transport hand-off. **[deck]** |
| X2 | HIGH | OPEN | No rationale/explanation ReportContent | ReportContent = {ObservationReportContent, PositionReportContent, TaskStatus}. CASEVAC "explainable reasons" (why route changed / mission failed) has no element. TaskStatus gives state, not rationale. Candidate: new ASX RationaleReportContent. **[deck]** |
| X3 | MED | OPEN | Route exists but no share-payload wrapper | `Route` (SMX) exists; ASX Order sheet used free-text "New Route Pattern" instead. Refines M6/P5. |
| X4 | MED | OPEN | No obstacle/threat observation subtype | Detected IED/broken-bridge that triggers replanning would fall to ActivityObservation or a new type; hazard entity typing unclear. |
| X5 | LOW | MOSTLY COVERED | Phased tasks/ETA | Base `PlanBody`/`PlanPhase`/`PlanPhaseTrigger` exist; recommend reuse. Only an ETA/estimate attribute is open. |
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
| Y5 | HIGH | OPEN | No sensor-reading value+unit property | Concentration, dose rate, frequency, depth have no home; only logistics quantities, `hasSpatialMeasure`, and `hasConfidenceLevel` exist. **[deck]** |

Partially covered (not gaps): location (`LocationObservation`), detected-object
identity (`SubjectTypeObservation`, if the entity type exists), confidence
(`hasConfidenceLevel`).

## 6d. Swarm walk findings (from Swarm-Walk.md)

| ID | Sev | Status | Item | Evidence / note |
|---|---|---|---|---|
| P7 | BLOCKER | OPEN | Swarm cannot be tasked or report | Confirmed by both swarm messages: an OrderBody recipient and a ReportBody `hasReportingEntity` must be an ActorEntity; ASX Swarm derives from PhysicalEntity. Fix: `Swarm subClassOf CollectiveEntity` (C2SIM; re-declared in SMX). **[deck]** |
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

Partially covered (checked, NOT gaps): rules of engagement, order
authorization, desired effect (`DesiredEffectCode`), target designation
(`hasAffectedEntity`). The engagement machinery mostly exists - the missing
piece is autonomy-to-permission.

## 6f. Task/effect batch findings (from TaskEffect-Batch-Walk.md)

| ID | Sev | Status | Item | Evidence / note |
|---|---|---|---|---|
| L1 | MED | OPEN | No cargo/payload manifest | What a platform carries. `Resource` + quantities exist; "load carried" does not. ConceptMapping Payload absent from OWL. |
| L2 | MED | OPEN | No delivery-confirmation ReportContent | What was delivered and received by whom; `TaskStatus` only says the task ran. |
| E1 | LOW | mostly covered | Engineering verbs exist in LOX | `CONSTR` (build/dig), `CLROBS`/`CLRLND` (clear), `MINLAY` (emplace), `BREACH` exist; folds into E2 (effector typing). |
| E2 | MED | OPEN | No effector/manipulator equipment concept | arm / blade / excavator. Ties to P2/D3. |
| R1 | - | reconfirms P1 | USV typing (SMX `SurfaceVessel` vs ASX `USV`/Robot), now maritime. |
| R2 | LOW | OPEN | Only a general tow/salvage verb absent | `lox#RESCUE` and `lox#RECOVR` exist as TaskActionCodes (the downed-pilot task uses RESCUE); only a general tow/salvage verb is missing. |

Recurring shape of the whole task/effect axis: LOX already has 446 `TaskActionCode`
verbs (incl. BREACH, ENGAGE, ATTACK, CONSTR, CLROBS, MINLAY, RESCUE, RECOVR, NTRCOM),
so what is actually missing is narrow - **(a) payload/effector/weapon typing**
(cargo L1, manipulator E2, weapon W2 are one gap) and **(b) a general tow/salvage
verb**. Entity structure, addressing, effects, targets, resources, ROE, and the
whole task-verb vocabulary already exist. Distilled into decision Q-L.

## 6g. Redundancy-pass findings (from RedundancyPass-Walk.md)

Checked the three scenarios flagged as likely-redundant (route clearance,
companion drones, urban combat). Mostly confirmed - but the pass found one new
finding that the entity-centric walks missed.

| ID | Sev | Status | Item | Evidence / note |
|---|---|---|---|---|
| N1 | MED | OPEN | Area as the subject of a task/report | `hasAffectedEntity` has no area counterpart (no `hasAffectedArea`), and there is no area-state (cleared/contaminated/mined). Areas exist (`TacticalArea`, `MapGraphic`) but cannot be tasked or have their state reported. Recurs in route-clearance, CBRN, urban. **[deck]** |
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

The scavenger session extracted all nine `Documents-Needed.md` requests (see
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
  (Z2). Membership/command reuse base `hasSubordinate`/`hasCommandRelation`.
- **Q-K [deck]** Model engagement authority as a function of autonomy level -
  may a system at this autonomy level take this (lethal) action without a human
  in/on the loop? ROE and authorization already exist; this link does not.
  (Resolves W1.)
- **Q-L [deck]** Add typed **payload / effector / weapon** (cargo, manipulator,
  munition) - the action verbs already exist in LOX (BREACH, ENGAGE, ATTACK,
  CONSTR, CLROBS, MINLAY, RESCUE, RECOVR, NTRCOM, ESCRT/FOLASS, plus
  follow/escort over `RelativeLocation`), and only a general tow/salvage verb is
  a residual. Effects, targets, and resources already exist.
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
- **Adopt (evidence-backed), not just decide:** Q-Q should re-adopt BML
  `WhoMeasuredType` (measurement report) and Q-F align to BML `ResourceType`
  (media report) - both prior art in C2SIM's BML lineage (Remmersmann 2015).

## 8. Why the identified gaps are not yet filled

"Lacking documents" is one cause, but the minority one. The gaps fall into three
separable buckets, and only the third is about sources:

1. **Top-down model that never built its property layer (most gaps).**
   `CSIM_ASX.rdf` is v0.0.1, "work in progress": ~15 classes, **1 object
   property, 0 datatype properties**. The classes are imported robotics
   upper-ontology terms (Robot, Sensor, Actuator, Device - CORA/ORA/SUMO
   lineage), i.e. a *taxonomy of things*. The *message layer* - the attributes
   you actually need to send - was never derived. So most "gaps" are simply
   not-yet-built, not blocked. Bottom-up instantiation surfaces them because it
   does the derivation the OWL skipped. No document fills these - modeling does.

2. **Deferred decisions and track desync (information already in hand).**
   P1 (UAV double-typed vs SMX Platform), P7 (swarm typing), D1/D2 (autonomy and
   sensor each defined three ways) are unresolved *choices*, plus a drift between
   the OWL track (Jan) and Elizabeth's spreadsheet track (Jun). Cross-cutting
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
track drift, and cross-cutting abstractions (buckets 1-2) - are not document
problems and no amount of new scenarios fills them. It takes bottom-up
instantiation to see which is which.

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
  round-trip; existing sheets preserved). Reviewed Elizabeth's own annotations
  on the worked scenarios (see conversation; agree on most, disagree on
  MediaType/SensorObservation typing and flag the M3 cross-sheet inconsistency).
- 2026-07-10: Walked non-video sensors (`NonVideoSensors-Walk.md`); added 3
  report tabs (CBRN / EW Emitter / GPR Mine) to the `.xml`. Added section 6c
  (Y1-Y5) and decision Q-I; updated C4. Grounding check confirmed the gaps are
  real (no measurement/hazard Observation subtype; no sensor-reading value+unit;
  no CBRN/EW-sensing/radar classes).
- 2026-07-10: Walked swarm (`Swarm-Walk.md`); filled the `Swarm Detection` stub
  (Report) and added `Swarm Coordination` (Order). Added section 6d (Z1/Z2),
  decision Q-J; updated C5. Grounding narrowed P8 - membership/command already
  exist in the base standard (C2SIM `hasSubordinate`, SMX `hasCommandRelation`).
- 2026-07-10: Walked Fire Support (`FireSupport-Walk.md`) - opens the task/effect
  axis; added `Fire Support Order` + `BDA Report` tabs. Added section 6e (W1-W3),
  decision Q-K, coverage C6; deck gained a Fire Support slide and split decisions
  into 2 slides. Grounding narrowed the finding: ROE + authorization already
  exist (LOX/C2SIM); the real gap (W1) is the autonomy-to-engagement link.
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
- 2026-07-10: Integrated the scavenger session's nine sourced missions
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
