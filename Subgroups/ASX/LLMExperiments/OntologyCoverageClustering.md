# Scenario Clustering by Ontology-Coverage Contribution

Purpose: cluster the extracted scenarios by what they can contribute to the ASX
ontology work - the C2SIM base ontology (`Ontology/C2SIM.rdf`, `C2SIM_SMX.rdf`,
`C2SIM_LOX.rdf`) as extended through the ASX sample-message workbooks the parallel
session is building (`Subgroups/ASX/Proposed Extension Working Materials/ASX Sample
*.xml`). Each ASX workbook tab is a proposed Init / Order / Report message type;
together they are the current ASX coverage surface.

This is analysis to feed the ontology/spreadsheet work - it does not modify the
ontology or the workbooks.

## Current ASX coverage surface (from the sample-message tabs)

- **Initialization:** UAV with Video Init; UAV Patrol Initialization; Swarm
  Initialization; CASEVAC Init.
- **Orders:** UAV Change Patrol Route; UGV Retrieve & Transport; CASEVAC Tasking;
  CASEVAC Route Advert; Swarm Coordination; Fire Support Order; Logistics Delivery
  Order; Engineering Task Order; USV Rescue Order.
- **Reports:** Swarm Detection; Video Detection Report; CASEVAC Status+Threat;
  CASEVAC Explainable; CBRN Detection Report; EW Emitter Report; GPR Mine
  Detection Report; BDA Report; Delivery Confirmation Report.

Observation: the current surface is strong on **air ISR, swarm, CASEVAC, fire
support, and land logistics**, and on **sensor detection reports**. It is thin on
**maritime/undersea**, **denied-comms operations**, **autonomy-to-autonomy
tasking**, and **exploration/search** tasks. The clusters below are ordered by how
much *new* coverage each contributes.

## Coverage matrix (scenario x ASX message thread)

`V` = exercises/validates an existing tab; `X` = would extend it or add a new one.

| Scenario | ISR / Video | Swarm | CASEVAC | Fire Support | Logistics | USV | Mine Detect | Detection Report (generic) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SubT (subterranean) | V | V | - | - | - | - | - | X |
| Cooperative MCM (maritime) | - | - | - | - | - | X | X | X |
| Sustainment / ULTRA (land) | - | - | (adj) | - | V | - | - | - |
| *Corona/Biagini urban counter-UAxS* | V | V | - | V | - | - | - | V |
| *Langerwisch MOVE/OBSERVE* | V | V | - | - | - | - | - | V |
| *Brutzman MUM-T ISR* | V | - | - | V | - | - | - | V |

---

## Cluster A - Autonomous exploration and multi-robot coordination in denied environments

**Scenarios:** SubT (primary); Langerwisch MOVE/OBSERVE (heterogeneous team
formation/convoy) as a supporting case.

**Exercises (validates existing ASX):** Swarm Coordination (order), Swarm
Detection / Video Detection Report, UAV Patrol Initialization.

**New contributions (extend the ontology):**
1. **Platform taxonomy enrichment** - UGV subtypes by locomotion: wheeled /
   tracked / legged (crawler); explicit heterogeneous-team composition. Current
   init tabs treat UAV/UGV/Swarm without a locomotion subtype axis.
2. **Communication-relay deployment as a taskable behavior/entity** - operating
   under intermittent comms by dropping relays to hold a low-bandwidth link. No
   current tab models denied-comms relay behavior.
3. **"Explore / Search Area" order type** - autonomous area exploration to a
   coverage/exploration goal, distinct from Patrol (fixed route) and Retrieve &
   Transport (point task).
4. **Generic Object/Artifact Detection Report** - SubT reports arbitrary artifact
   type + position + error bound. This generalizes the family of specific reports
   (Video / CBRN / EW / GPR Mine) into one parameterized detection report with a
   **confidence / error-bound** attribute and a **false-positive** notion.

**Value:** highest new-coverage-per-scenario; opens the denied-comms and
exploration gaps and rationalizes the detection-report family.

## Cluster B - Maritime/undersea MCM and autonomy-to-autonomy cross-cueing

**Scenarios:** Cooperative MCM (primary).

**Exercises (validates existing ASX):** USV Rescue Order (the only current USV
message), GPR Mine Detection Report (land-mine analog), BDA Report (neutralization
outcome analog), Delivery Confirmation Report (task-complete analog).

**New contributions (extend the ontology):**
1. **USV order/report set beyond rescue** - detect, classify, and **neutralize**
   orders; a **naval-mine detection report** (maritime; distinct from the
   ground-penetrating-radar land-mine report); a **neutralization confirmation**.
2. **Maritime domain entities** - sea line of communication / operating area,
   **transiting neutral vessels** (neutral track that constrains behavior),
   moored vs bottom naval mine.
3. **Autonomy-to-autonomy cross-cueing** - a detector USV hands a classified
   target's exact location to a neutralizer USV, which acts without re-detecting.
   This is a distinctive C2 concept: **one autonomous system tasks another and
   shares a track**. The current order set is command-post-to-system; this adds
   system-to-system tasking + shared classified track.
4. **Persistent / revisit-cycle tasking** - a standing task re-executed on a
   revisit cadence (8 h / 24 h), not a one-shot order.
5. **Measure-of-effectiveness attributes on reports** - percentage neutralized,
   average mine active time (risk to neutral traffic).

**Value:** opens the maritime/undersea domain (currently near-absent) and
introduces autonomy-to-autonomy tasking - arguably the most novel C2 concept in
the batch.

## Cluster C - Autonomous sustainment / logistics (contested last tactical mile)

**Scenarios:** Sustainment / ULTRA (primary); adjacent to the CASEVAC thread.

**Exercises (validates existing ASX):** Logistics Delivery Order, UGV Retrieve &
Transport, Delivery Confirmation Report - this scenario is largely a **real-world
validation** of the logistics message set already modeled.

**New contributions (extend the ontology):**
1. **Decoy behavior** - employing a platform as a decoy to reduce risk to a
   delivery. A novel tactical behavior/order not currently modeled.
2. **Threat-aware / contested delivery attributes** - "last tactical mile",
   route-under-threat, low-signature delivery; risk/threat annotation on a
   delivery order.
3. **Tasking abstraction / level-of-autonomy on a logistics order** - "load and
   send to grid, then autonomous execution with no trailing operator."

**Value:** mostly confirms existing coverage (good for stress-testing the
logistics tabs against a real vignette); its net-new items are the decoy behavior
and threat-aware delivery attributes.

---

## Cross-cutting concepts the batch surfaces (candidate ontology additions)

These recur across clusters and are the highest-leverage additions:

1. **Autonomy-to-autonomy tasking / cross-cueing** (Cluster B) - system-to-system
   orders and shared tracks, beyond CP-to-system messaging.
2. **Communication-relay / denied-comms operation** (Cluster A) - relays as
   deployable entities; behavior under intermittent comms.
3. **Generic Detection Report with confidence/error-bound** (Clusters A, B) -
   unify Video/CBRN/EW/GPR/artifact/naval-mine detections; add uncertainty.
4. **Decoy behavior** (Cluster C) - risk-reduction tactic as a taskable behavior.
5. **Persistent/revisit-cycle tasking** (Cluster B) - standing tasks with cadence.
6. **Platform taxonomy by locomotion/domain** (Clusters A, B) - wheeled/tracked/
   legged UGV; detector/neutralizer USV subtypes.
7. **Non-combat / neutral-actor framing** (Clusters A, B) - SubT (no adversary)
   and MCM (neutral commercial traffic) stress any implicit assumption that a
   scenario has a hostile side; the ontology should represent SAR and
   neutral-traffic-constrained missions cleanly.

## Suggested handoff to the ontology/spreadsheet session

- **Cluster B (MCM)** is the strongest candidate for a *new* workbook thread: a
  USV MCM message set (detect/classify/neutralize orders, naval-mine detection
  report, neutralization confirmation) plus the cross-cueing pattern.
- **Cluster A (SubT)** motivates two additions usable across threads: a generic
  detection report with confidence, and an Explore/Search order; plus a
  comms-relay entity.
- **Cluster C (sustainment)** is best used to *validate* the existing Logistics
  Delivery / Retrieve & Transport / Delivery Confirmation tabs against a real
  vignette, adding only the decoy behavior and threat-aware attributes.
