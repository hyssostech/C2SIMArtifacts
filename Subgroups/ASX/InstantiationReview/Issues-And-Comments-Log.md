# ASX Review - Issues & Comments Log

Running log of issues, defects, and comments found while reviewing the proposed
ASX ontology elements against the scenarios and the sample-message
instantiations. This is the working source; the planned findings PowerPoint is
generated from it. Kept current as work proceeds.

Severity: **BLOCKER** (stops a message being instantiated) / **HIGH** /
**MED** / **LOW** / **TYPO**. Status: **OPEN** / **RESOLVED**.
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

| ID | Sev | Status | Item | Evidence / note |
|---|---|---|---|---|
| P1 | BLOCKER | OPEN | UAV typed twice, incompatibly: ASX `UAV subClassOf Robot subClassOf ActorEntity` vs SMX `Aircraft subClassOf Platform subClassOf ActorEntity` | Disjoint sibling trees. `Robot` orphans the drone from Platform machinery; `Aircraft` leaves ASX classes unused. **[deck]** |
| P2 | BLOCKER | OPEN | Sensor: separately-declared entity, or attribute on platform? | Init must pick one; Report side only consumed sensor output. Ties to D2. **[deck]** |
| P3 | HIGH | OPEN | `hasAutonomousRoleCode` has no attachment point on the entity | Defined in OWL, but no Init field and not on EntityDescriptor. |
| P5 | HIGH | OPEN | Patrol route/area not modeled as an init object | Order references a route to change; nothing declares the baseline. Can host as MapGraphic. Gap on both Init and Order sides. Ties to M6. |
| P6 | HIGH | OPEN | Three competing autonomy vocabularies at init time | Same as D1, surfaced concretely when declaring an entity. |
| P7 | BLOCKER | OPEN | Swarm cannot be tasked as modeled | `Swarm subClassOf CollecticeRoboticSystem -> ... -> PhysicalEntity` (inert), but swarms receive orders and send reports (need ActorEntity). Base C2SIM has `CollectiveEntity subClassOf ActorEntity`. **[deck]** |
| P8 | HIGH | OPEN | Swarm membership + leader have no property | ConceptMapping "Leader-Boolean, Network" has no OWL property; `hasSuperior` is the natural base hook. |
| P9 | TYPO | OPEN | Misspelling O1 propagates into swarm instance data | Same root as O1. |
| P10 | MED | OPEN | Heterogeneous (mixed UAV+UGV) swarm membership unconfirmed | MUTT-style mixed swarms; confirm members of different platform types can share one collective. |

## 6. Coverage gaps (scenario x message type)

| ID | Sev | Status | Item | Evidence / note |
|---|---|---|---|---|
| C1 | HIGH | PARTIAL | Initialization entirely un-instantiated (0 of 3 named scenarios) | Draft instantiations for all 3 named scenarios now applied to the `.xml` on branch (pending group review). **[deck]** |
| C2 | HIGH | INSTANTIATED | CASEVAC (flagship contributed scenario) has no messages of any type | Walked in `CASEVAC-Walk.md`; 5 tabs added to the `.xml` workbooks (CASEVAC Init; CASEVAC Tasking + Route Advert; CASEVAC Status+Threat + Explainable). Surfaced X1/X2 (section 6b). **[deck]** |
| C3 | MED | OPEN | 8 of 10 MUTT scenarios have no instantiations | Only Recon->video and Logistics->UGV transport partly covered. |
| C4 | MED | INSTANTIATED | Non-video sensors not covered | Walked in `NonVideoSensors-Walk.md`; 3 report tabs added to the `.xml` (CBRN / EW Emitter / GPR Mine). Surfaced Y1-Y5 (section 6c). **[deck]** |
| C5 | LOW | OPEN | Swarm Detection report + swarm coordination order not done | Stubs only. |

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
