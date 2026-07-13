# Initialization Message Walk (proposed coverage)

Purpose: fill the three Initialization scenarios that exist as empty sheets in
`ASX Sample Initialization Messages.xlsx` (`UAV with Video Init`,
`UAV Patrol Initialization`, `Swarm Initialization`), and use the act of
instantiation to test the proposed ASX elements. Layout mirrors the workbook's
scenario-sheet columns so any of this can be pasted back in by the owner:

`Model | C2SIM Object | Parent Type | Field | Type | Value | Notes`

Everything below is anchored to real classes in `Ontology/C2SIM.rdf` and
`Ontology/C2SIM_SMX.rdf`. Open questions are marked **[Q]**; not-yet-defined
items in the current proposal are marked **[!]**. None of this is a decision - it is
input for the sub-group.

## Shared envelope (all three)

Same as the filled envelope template in the workbook: a `Message` with
`hasC2SIMHeader` -> `C2SIMHeader` and `hasMessageBody` -> `C2SIMInitializationBody`.
`C2SIMInitializationBody` (C2SIM) carries:

| Field | Type | Notes |
|---|---|---|
| hasObjectDefinitions | ObjectDefinitions | where scenario entities are declared |
| hasSystemEntityList | SystemEntityList | maps systems to the entities they own |
| hasScenarioSetting | ScenarioSetting | time/coordinate frame, force sides |
| hasInitializationDataFile | InitializationDataFile | optional external data file |

Base entity taxonomy the declarations plug into (verified from the ontology):
`Entity -> ActorEntity -> {CollectiveEntity, Person, Platform}`, and SMX
`Platform -> {Aircraft, SubsurfaceVessel, SurfaceVessel, Vehicle}`. Entity
descriptor properties available: `hasName`, `hasMarking`, `hasEntityTypeName`,
`hasEntityTypeNamespace`, `hasSuperior` (UUIDBase), `hasStrengthPercentage`.

---

## Scenario A: UAV with Video Init

Corresponds to the worked `Video Detection Report`. One UAV carrying an onboard
video sensor, a controlling C2 unit, one force side.

| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| C2SIM | ObjectDefinitions | C2SIMInitializationBody | hasActorEntity | ActorEntity | (the UAV) | container |
| SMX **or** ASX | Aircraft **or** UAV | Platform / Robot | hasEntityType | EntityType | "UAV" | **[!] typing conflict - see P1** |
| C2SIM | (UAV entity) | ActorEntity | hasName | string | "Scout-UAV-1" | |
| C2SIM | (UAV entity) | ActorEntity | hasMarking | string | "UAV1" | |
| C2SIM | (UAV entity) | ActorEntity | hasSuperior | UUIDBase | (C2 unit UUID) | who tasks it |
| ASX | (UAV entity) | ? | hasAutonomousRoleCode | Code | FullAuto | **[Q] no attach point - see P3** |
| ASX | (UAV entity) | ? | ControlMode | enum | Unpiloted-Autonomous | **[!] duplicate of autonomy code - see P6** |
| ASX | (UAV entity) | ? | VehicleType | enum | Drone-Hover | from ConceptMapping |
| ASX | (UAV entity) | ? | Mobility/Propulsion | enum | MultiRotor | from ConceptMapping |
| ASX | onboard video sensor | Sensor / Equipment | SensorCapability | enum | SensorVideo | **[!] sensor as entity vs attribute - see P2** |
| C2SIM | C2 unit | ActorEntity(Unit) | hasName | string | "HOTL-Cmd" | receives reports |
| C2SIM | ScenarioSetting | C2SIMInitializationBody | (force side, time, CRS) | - | - | standard |

Problems this exposes:

- **P1 [!] Entity-type conflict.** The proposed OWL declares
  `UAV subClassOf Robot subClassOf ActorEntity`, while SMX already declares
  `Aircraft subClassOf Platform subClassOf ActorEntity`. These are parallel
  (non-overlapping) sibling hierarchies - not declared `owl:disjointWith`, but
  no entity is typed under both. When we set `hasEntityType` for the drone, is it an SMX
  `Aircraft` or an ASX `UAV`/`Robot`? Picking `Robot` orphans the drone from all
  existing Platform machinery (SMX Platform attributes, LOX behaviors); picking
  `Aircraft` makes the ASX `Robot`/`UAV` classes unused for real platforms.
  **[Q]** Should ASX autonomy be a *facet/role* on the existing `Platform`
  subtree rather than a parallel `Robot` class tree?
- **P2 [!] Sensor: entity or attribute?** `ASX Concept Mapping` models sensors
  two ways at once - `SensorType` as an enum and `SensorCapability` as an
  "associated Equipment type" - and the OWL models `Sensor subClassOf
  ElectricDevice` as a class. Initialization needs one answer: is the video
  sensor a separately-declared Equipment entity, or an attribute on the platform?
  The Report side only consumed sensor *output*, so this decision surfaces here
  for the first time.
- **P3 [Q] Autonomy code has no home on the entity.** `hasAutonomousRoleCode`
  exists in the OWL as an object property (subPropertyOf `hasCode`) but the Init
  template has no field for it, and `EntityDescriptor` does not carry it. Where
  is it attached at declaration time?

---

## Scenario B: UAV Patrol Initialization

Corresponds to the worked `UAV Change Patrol Route` order. One UAV plus a
baseline patrol route/area that later orders will modify.

| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| SMX/ASX | (UAV entity) | Platform / Robot | ... | ... | ... | same as Scenario A (P1, P3) |
| C2SIM | PatrolRoute | MapGraphic (PhysicalEntity) | hasName | string | "Patrol-Route-A" | **[!] route as init object - see P5** |
| C2SIM | PatrolArea | MapGraphic (PhysicalEntity) | (geometry) | - | - | baseline area of operations |
| ASX | (UAV entity) | ? | NavigationAutonomy | enum | Autonomous | **[!] third autonomy vocab - see P6** |

Problems this exposes:

- **P5 [!] Route/area must be a first-class initialized object.** The Change
  Patrol Route order references "New Route Pattern" / "New Location" as free
  text with no type. For an order to *change* a route, a baseline route/area has
  to be declared at init. C2SIM can host it as a `MapGraphic` (under
  `PhysicalEntity`), so the gap is not a missing base class - it is that neither
  the Init nor the Order sheet models the route payload yet. The same gap shows
  up on both the Init and Order sides, which is a good sign it is real and not a
  sheet artifact.
- **P6 [!] Three competing autonomy vocabularies.** The same drone can be tagged
  three inconsistent ways: OWL individual `FullAuto`/`Teleop`/`ReCont`/`Automated`
  (via `hasAutonomousRoleCode`), ConceptMapping `Control Mode`
  {Piloted, Unpiloted-Autonomous, Swarm}, and ConceptMapping `NavigationAutonomy`
  {FPV, Autonomous, RemoteControl}. Instantiation forces the question: which one
  is normative at initialization, and how do the other two relate to it (are
  they orthogonal dimensions, or redundant)?

---

## Scenario C: Swarm Initialization

The hardest, and the most revealing. A swarm of N member vehicles with a
designated leader, declared as a collective that can be tasked and can report.

| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| ASX **or** C2SIM | Swarm **or** CollectiveEntity | CollecticeRoboticSystem (sic) / ActorEntity | hasEntityType | EntityType | "Swarm" | **[!] collective typing conflict - see P7** |
| C2SIM | (Swarm) | ActorEntity | hasName | string | "Swarm-1" | must be taskable |
| C2SIM | member UAV #1 | Platform/Robot | hasSuperior | UUIDBase | (Swarm UUID) | **[Q] is hasSuperior the membership link? - see P8** |
| C2SIM | member UGV #2 | Platform/Robot | hasSuperior | UUIDBase | (Swarm UUID) | heterogeneous members - see P10 |
| ASX | (Swarm) | ? | Leader | UUIDBase/Boolean | (member #1 UUID) | **[!] no such property - see P8** |
| ASX | (Swarm) | ? | Network | Network | (comms parms) | ConceptMapping "Swarm Parameters" |

Problems this exposes:

- **P7 [!] A Swarm is not yet orderable as currently modeled.** The OWL declares
  `Swarm subClassOf CollecticeRoboticSystem subClassOf RoboticSystem subClassOf
  Device subClassOf Artifact subClassOf PhysicalEntity`. That places a swarm in
  the **PhysicalEntity** tree - an inert object - not under **ActorEntity**. But
  a swarm is exactly what orders are addressed to and what sends reports
  (see `Swarm Detection`), which requires `ActorEntity`. Base C2SIM already has
  `CollectiveEntity subClassOf ActorEntity` for precisely this. As written, the
  ASX model does not yet yield a taskable swarm instance. **[Q]** Should `Swarm`
  derive from `CollectiveEntity` (ActorEntity) rather than from the
  device/artifact tree?
- **P8 [Q] Membership and leader: no ASX property yet; base hooks exist.**
  (Narrowed by the swarm walk: `hasSubordinate`/`hasSuperior` (C2SIM) and
  `hasCommandRelation` (SMX) cover membership and command.) ConceptMapping lists
  "Swarm Parameters: Leader - Boolean, Network". There is no membership or leader
  object property in the OWL. `hasSuperior` (UUIDBase) is the natural base-C2SIM
  hook for member-to-collective linkage; leader could be a role rather than a
  Boolean on the swarm. Needs a decision before a swarm can be declared.
- **P9 [!] Typo will propagate to instance data.** The class is spelled
  `CollecticeRoboticSystem` in `CSIM_ASX.rdf` (should be "Collective"). Any
  instance typed against it inherits the misspelling. Cheap to fix now, painful
  after messages exist.
- **P10 [Q] Heterogeneous swarm.** MUTT-style scenarios mix platform types (UAV +
  UGV) in one swarm. If members are typed under the ASX `Robot` tree (P1) but the
  swarm is a collective, confirm members of different platform types can belong
  to one collective and be tasked coherently.

---

## Summary of problems surfaced by the Initialization walk

| ID | Type | One-line |
|---|---|---|
| P1 | [!] | UAV/Robot (ASX) vs Aircraft/Platform (SMX) - conflicting parallel entity trees |
| P2 | [!] | Sensor modeled 3 ways (class / enum / equipment) - init needs one |
| P3 | [Q] | hasAutonomousRoleCode has no attachment point on the entity |
| P5 | [!] | Patrol route/area not modeled as an init object (also missing on Order side) |
| P6 | [!] | Three competing autonomy vocabularies |
| P7 | [!] | Swarm is under PhysicalEntity, so it is not yet taskable or able to report |
| P8 | [Q] | Swarm membership + leader - narrowed: base `hasSubordinate`/`hasSuperior`/`hasCommandRelation` cover it; residual is network params, leader-as-role, dynamic handover |
| P9 | [!] | "CollecticeRoboticSystem" misspelling will propagate to instances |
| P10 | [Q] | Heterogeneous (mixed-type) swarm membership unconfirmed |

The three to settle before a message can be built cleanly are **P1**, **P2**,
and **P7**. They are all entity-typing decisions - which is why Initialization,
not Reports, is where the proposal most needs to be exercised.
