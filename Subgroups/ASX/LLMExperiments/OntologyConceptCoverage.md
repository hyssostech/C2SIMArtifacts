# Scenario Contribution to Ontology Concepts (bidirectional coverage)

Purpose: classify the examined scenarios by the ontology *concept/aspect* each one
exercises, and read the result both ways:

- **Validation** - do the cases supply enough data to validate each ontology
  concept? (concept -> which scenarios provide evidence; which concepts are
  under-tested)
- **Expressiveness** - are the concepts rich enough to represent every aspect the
  scenarios require? (scenario aspect -> is there a concept for it, or is it a gap)

This is analysis to feed the ontology/instantiation work. It is organized by
concept, not by message-workbook sheet.

## Grounding

- Current ASX ontology (`Subgroups/ASX/Proposed Extension/CSIM_ASX.rdf`, v0.0.1,
  imports LOX): classes `RoboticSystem` -> `SingleRoboticSystem`,
  `CollectiveRoboticSystem`, `Swarm`; `Robot`; `UAV`; `UGV`; `Sensor`; `Actuator`;
  `Device`/`ElectricDevice`; `Artifact`/`ArtificialSystem`; `PhysicalEnvironment`,
  `RoboticEnvironment`; object property `hasAutonomousRoleCode` with individuals
  `FullAuto`, `Automated`, `Teleop`, `ReCont`, `ComputerProcess`.
- ASX message design (from `InstantiationReview/Message-Instantiation-Coverage.md`):
  ASX `Task` with `hasAffectedEntity` / `DesiredEffectCode`; `Report Base
  Attributes` (MediaReference, AnalystComment, AnalysisConcept, MediaTypeEnum,
  SensorObservation); open concepts the team already flagged - machine-to-machine
  route hand-off, "explainable reasons" reports, on-the-loop status,
  MediaType/SensorType conflation, collective-entity typing.

## Scenarios analyzed

- **S1 SubT** - heterogeneous multi-robot subterranean artifact search (new).
- **S2 MCM** - cooperative USV mine countermeasures on a sea lane (new).
- **S3 Sustainment** - contested last-tactical-mile UGV resupply (new).
- **S4 Urban C-UAxS** - urban defense vs hostile UAAV swarms (Corona/Biagini, Biagini 2017).
- **S5 Brutzman** - village-defense MUM-T ISR and fires.
- **S6 Langerwisch** - heterogeneous UGV/UAV MOVE (formation/convoy) and OBSERVE (POI).

## Concept x scenario matrix

`S` = strong/primary demonstration; `p` = present/partial; `-` = absent or n/a.

| # | Ontology concept / aspect | S1 SubT | S2 MCM | S3 Sust | S4 C-UAxS | S5 Brutz | S6 Langer |
|---|---|---|---|---|---|---|---|
| 1 | Platform/agent typing (UAV/UGV/...) | S | S | p | p | p | S |
| 2 | Collective/swarm typing | p | p | - | S | - | p |
| 3 | Sensor & payload-device typing | S | S | - | p | p | S |
| 4 | Autonomous role / level of autonomy | S | p | p | S | p | p |
| 5 | Multi-system coordination & machine-to-machine tasking | S | S | p | p | p | S |
| 6 | Task & effect representation (incl. kinetic/non-kinetic) | p | S | p | S | p | S |
| 7 | Detection & reporting (confidence, explainability) | S | S | p | p | p | S |
| 8 | Operating environment & conditions | S | S | p | S | p | p |
| 9 | Spatial & geometric constructs | p | S | p | p | p | S |
| 10 | Temporal & persistence (revisit, phases) | p | S | - | p | - | p |
| 11 | Communications & networking (relay, denied comms) | S | p | - | p | - | p |
| 12 | Actors, sides & ROE / C2 relations | p | S | - | S | S | p |
| 13 | Measures (MOP/MOE) | p | S | p | p | - | p |

---

## Reading 1 - Do the cases validate the concepts?

**Well validated (three or more scenarios exercise it):**
- Platform/agent typing (S1,S2,S6 strong) - but see expressiveness note: the
  *evidence* exceeds what the ontology can currently type (USV, legged UGV).
- Multi-system coordination & machine-to-machine tasking (S1,S2,S6 strong).
- Sensor & payload-device typing and Detection & reporting (S1,S2,S6 strong).
- Task & effect representation (S2,S4,S6 strong).
- Operating environment & conditions (S1,S2,S4 strong).
- Autonomous role / LoA (S1,S4 strong; graded LoA in S4).

**Under-validated (thin or single-scenario evidence - needs more cases):**
- **Temporal & persistence** - essentially only S2 (revisit cycle). Standing/
  persistent tasking is barely tested; needs a persistent-surveillance or
  sentry case.
- **Communications & networking** - only S1 exercises it hard (relay drop,
  denied comms). One strong case; the concept is otherwise untested.
- **Explainability / on-the-loop status** (a concept the ASX design explicitly
  carries) - **zero** of the six scenarios exercises it. No validating data at
  all. This is the clearest coverage hole for a concept the ontology already
  intends to support.
- **CASEVAC coordination, CBRN, EW** - the ASX workbook models these, but **none**
  of the six scenarios instantiates them (S3 is only CASEVAC-adjacent). Concepts
  with no data in this set.
- **Effects - non-kinetic vs kinetic distinction** - only S4 exercises the
  distinction richly; S2 adds "neutralize". Moderate, could use one more.

**Implication:** the six cases give solid, redundant validation for entity typing,
coordination, sensing/reporting, task/effect, and environment. They do **not**
validate explainability, CBRN/EW sensing, CASEVAC coordination, or persistence -
so on those, "the concept is defined but untested." Sourcing the next scenarios
should target those, not add more ISR/coordination cases where evidence is already
redundant.

## Reading 2 - Are the concepts expressive enough for the scenarios?

Aspects the scenarios require that the current ASX ontology (v0.0.1) cannot
represent cleanly - i.e. expressiveness gaps:

1. **Maritime/undersea platform classes** (S2) - no `USV`/`UUV`; the taxonomy stops
   at `UAV`/`UGV`. S2's detector/neutralizer/CUSV cannot be typed.
2. **Locomotion/role subtypes of UGV** (S1) - wheeled/tracked/legged are all one
   `UGV`; the heterogeneity that drives S1's task allocation is not expressible.
3. **Coordination as a first-class relation, and machine-to-machine tasking**
   (S2,S6,S1) - `Swarm` exists as an *entity*, but there is no construct for
   coordination *relations* (formation, convoy, escort, orbit) nor for one
   autonomous system tasking/cueing another (S2 detector -> neutralizer hand-off).
   This matches the team's own flagged gap (machine-to-machine route hand-off).
4. **Communications link / relay entity and denied-comms condition** (S1,S6) - no
   comm-link or relay concept; S1's relay-dropping behavior and comms-limited
   operation are not representable.
5. **Operating-environment conditions as attributes** (S1,S2,S4,S5) -
   `RoboticEnvironment` is a bare class; GPS-denied, comms-limited,
   domain=subterranean/maritime, and time-of-day/illumination cannot be attached.
6. **Graded / phase-dependent level of autonomy** (S4) - the ontology's
   `hasAutonomousRoleCode` is categorical (FullAuto/Teleop/...); S4 uses graded LoA
   1/3/6 that varies by mission phase. Alignment/expressiveness gap.
7. **Detection report with confidence / error bound, and generic detection**
   (S1,S2) - reports need a confidence or error-bound attribute and a
   type-agnostic detection form (artifact, naval mine) beyond the media-typed
   video report.
8. **Task-type breadth** (S1,S2,S3) - explore/search-area, neutralize, deliver-
   under-threat, and **decoy** behaviors are not obviously expressible as ASX
   `Task` + `DesiredEffectCode`.
9. **Persistence / revisit-cycle tasking** (S2) - a standing task re-executed on a
   cadence, distinct from a one-shot order.
10. **Neutral actors and no-adversary framing** (S1,S2) - S1 has no hostile side;
    S2 has neutral commercial traffic that *constrains* behavior. If the model
    presumes a hostile side, these are not cleanly representable.
11. **Formation / relative geometry** (S6) - observation poses on a circle, one-UAV-
    overhead / others-orbiting, convoy spacing: relative/formation geometry beyond
    absolute routes and boundaries.

## Synthesis - the two questions, answered

- **Sufficient data to validate the concepts?** For the *core* ASX concepts
  (platform/sensor/swarm typing, autonomous role, coordination, task/effect,
  reporting, environment) - **yes**, with redundancy. For **explainability,
  CBRN/EW sensing, CASEVAC coordination, and persistence** - **no**; these are
  defined (or intended) but exercised by none of the six cases.
- **Concepts expressive enough for the scenarios?** **Partially.** The v0.0.1
  taxonomy covers air/ground single and collective systems and autonomous role,
  but eleven scenario aspects (above) exceed it - most importantly maritime
  platforms, coordination/ machine-to-machine tasking as relations,
  communications, environment conditions, graded LoA, and detection confidence.

## Where this points (bidirectional next steps)

- **To finish validating existing concepts** (close Reading-1 holes): source or
  extract scenarios that force **explainability / on-the-loop** decisions, **CBRN
  and EW sensor tasking**, a **full CASEVAC coordination thread**, and
  **persistent/standing tasking**. These add data where the ontology is currently
  asserted-but-untested.
- **To make the concepts expressive enough** (close Reading-2 gaps): the
  highest-leverage ontology additions are USV/UUV + UGV locomotion subtypes,
  a coordination/relationship construct with machine-to-machine tasking, a
  communications/relay concept, environment-condition attributes, graded
  autonomous role, and a detection-confidence attribute.
- The two lists are complementary: S2 (MCM) is the single richest *expressiveness*
  stressor (maritime, cross-cueing, persistence, neutral actors, measures), while
  the *validation* holes point away from more combat-ISR cases toward
  explainability, CBRN/EW, and CASEVAC sources.
