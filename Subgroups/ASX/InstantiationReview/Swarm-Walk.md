# Swarm Message Walk (proposed coverage)

Purpose: instantiate the swarm scenario - a collective of cooperating vehicles
that is tasked, coordinates internally (leader, roles, member rotation), and
reports collectively. This exercises the swarm entity-typing findings (P7, P8,
P10) concretely, filling the empty `Swarm Detection` report stub and adding a
`Swarm Coordination` order.

Layout mirrors the workbook columns:
`Model | C2SIM Object | Parent Type | Field | Type | Value | Notes`.
**[Q]** = open question, **[!]** = not-yet-defined item / gap. Anchored to the ontology.

Grounding done first (and it narrowed two findings):
- `CollectiveEntity` (base C2SIM; re-declared in SMX) is `subClassOf ActorEntity`
  - the clean target for P7 (a swarm must be taskable / able to report).
- `hasSubordinate` / `hasSuperior` (C2SIM) and `hasCommandRelation` (SMX)
  **already exist** - so membership and leader/command are *partially*
  expressible in base C2SIM. P8 is therefore narrower than "no property."
- `hasReportingEntity` exists, but only an ActorEntity can be one (P7 again).
- No aggregation construct, and no swarm-lifecycle (member rotation) construct.

## Reminder: the P7 typing decision

The proposed OWL has `Swarm subClassOf CollecticeRoboticSystem -> ... ->
PhysicalEntity` (an inert object). Both messages below need the swarm to be an
**ActorEntity** (to be ordered, and to be a ReportingEntity). As modeled it is
neither. Recommended fix: `Swarm subClassOf CollectiveEntity` (base C2SIM).

## 1. Swarm Detection Report (fills the `Swarm Detection` stub)

The swarm collectively reports targets detected by its members.

| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| C2SIM | ReportBody | DomainMessageBody | hasReportingEntity | UUIDBase | (swarm UUID) | [!] P7: a ReportingEntity must be an ActorEntity; ASX Swarm derives from PhysicalEntity -> not yet able to report as a collective. |
| C2SIM | ReportBody | DomainMessageBody | hasReportContent | ObservationReportContent | (aggregated detections) | [!] Z1: no aggregation construct - is a swarm detection one report from the collective, or N reports from members? |
| SMX | ObservationReportContent | ReportContent | hasObservation | Observation | (targets detected by members) | |
| SMX | LocationObservation | Observation | hasLocation | Location | (detected target location) | Works. |
| C2SIM | member UAV #1 | Platform / Robot | hasSuperior | UUIDBase | (swarm UUID) | Membership via hasSuperior / hasSubordinate (base) - works IF the swarm is an ActorEntity (P7). |

## 2. Swarm Coordination Order (new tab)

Tasks the swarm and covers intra-swarm coordination: leader designation and
member rotation/resupply (from the June robotics-concepts discussion).

| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| C2SIM | OrderBody | DomainMessageBody | isToReceiver | UUIDBase | (swarm UUID) | [!] P7: recipient must be an ActorEntity; ASX Swarm is PhysicalEntity -> not yet orderable. |
| C2SIM / ASX | Swarm Task | Task | hasTask | TaskActionCode | Surveil / Deliver | [Q] swarm-level task vs per-member decomposition - who decomposes, and is that modeled? |
| SMX | (leader designation) | - | hasCommandRelation | CommandRelation | (member #1 leads) | Partial - `hasCommandRelation` exists; but ConceptMapping models leader as a Boolean, and dynamic leader handover is not clean. [P8, narrowed] |
| ASX | (swarm) | ? | Network | Network | (comms params) | [!] P8: ConceptMapping SwarmParameters "Network" has no base property. |
| ASX | (member lifecycle) | ? | rotate / resupply | ??? | replace depleted member | [!] Z2: no construct for dynamic membership change (rotate / recharge / replace) that the June deck calls out. |
| C2SIM | member UGV #2 | Platform / Robot | hasSuperior | UUIDBase | (swarm UUID) | [Q] P10: heterogeneous (UAV+UGV) members in one collective. |

---

## Findings summary

| ID | Sev | Status | One-line |
|---|---|---|---|
| P7 | DECIDE-FIRST | gap | Swarm derives from PhysicalEntity - not yet orderable or a ReportingEntity. Fix: derive from `CollectiveEntity` (ActorEntity). |
| P8 | HIGH | **narrowed** | Membership + command are partially expressible via `hasSubordinate`/`hasSuperior`/`hasCommandRelation`; residual gap is network params + leader-as-role + dynamic handover. |
| P10 | MED | question | Heterogeneous (mixed UAV+UGV) membership in one collective - confirm. |
| Z1 | MED | gap | No aggregation construct for a collective report built from member observations. |
| Z2 | MED | gap | No swarm-lifecycle construct for dynamic member rotation / resupply / replacement. |

What is **partially covered** (checked, not gaps): membership and command
relations (`hasSubordinate`/`hasSuperior`/`hasCommandRelation`), the collective
entity type itself (`CollectiveEntity`), and reporting-entity linkage
(`hasReportingEntity`) - all conditional on fixing P7 so the swarm is an
ActorEntity.

## Headline

Every swarm message runs into the same wall: as modeled, a swarm is a
PhysicalEntity, so it is not yet able to receive an order or sign a report. Fixing
P7 (`Swarm subClassOf CollectiveEntity`) unlocks most of this - membership and
command relations are already in the base standard. The genuinely new swarm
needs are small: network/comms parameters, a leader role, aggregation (Z1), and
member-lifecycle (Z2).
