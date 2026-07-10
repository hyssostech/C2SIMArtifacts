# Scenario extracted from report (v2.2 prompt)

U.S. Army, Robotic Complex Breach Concept (RCBC) demonstration, Grafenwoehr
Training Area, 6 April 2018, and follow-on combined-arms robotic breach exercise,
Yakima Training Center. Primary sources: army.mil article 203482 and DVIDS
imagery.

Source-fidelity caveat: the army.mil primary page was access-blocked at extraction
time; this record is grounded in the specific reported facts (named units,
platforms, and breach tasks) surfaced from that reporting, not the full primary
text. Platform autonomy is reported as remote-control/teleoperation. Fields not
in the reported facts are marked "Not specified in source" or "[inferred]".

Sourced against `InstantiationReview/Documents-Needed.md` request #9 (combat-
engineering / manipulation). Grounds E1 (effector/task verbs), E2 (effector
equipment typing), N1 (cleared-lane area state). Complements the CBRN manipulation
grounding (valve/sample) with breach/reduce/emplace verbs.

### Scenario 1: Combined-arms robotic complex obstacle breach

**Domain / mission type:** land; combat-engineering combined-arms breach (obstacle reduction) with robotic/remote systems.

**Source location:** RCBC demonstration reporting (Grafenwoehr 2018); follow-on Yakima combined-arms breach.

**Purpose (why the authors present it):** To demonstrate employing robotic and
autonomous systems (RAS) for the breach so soldiers are removed from the point of
breach, and to develop the tactics/procedures for unmanned breaching. (Concept-
demonstration intent.)

**Summary narrative:** A combined-arms team conducts a complex obstacle breach
using remotely-controlled systems for the most dangerous tasks. An Automated
Direct and Indirect Mortar provides suppression, an M58 Wolf smoke generator
obscures the breach site, and a UK "Terrier" armored digger reduces the obstacle,
in support of an M1 Abrams. In the follow-on Yakima exercise, a first Assault
Breacher Vehicle (ABV) fires a mine-clearing line charge to clear a lane through a
minefield and emplaces stakes marking where it is safe to drive, and a second ABV
uses its blade to fill an anti-tank trench. The robotic and autonomous systems
perform the intelligence, suppression, obscuration, and reduction tasks so that
soldiers are not exposed at the point of breach.

**In-world objectives:**
- Breach a complex obstacle (minefield plus anti-tank trench) to open a lane for maneuver.
- Keep soldiers out of the point of breach by using RAS for the dangerous tasks.

**Autonomous systems employed:**
- M58 Wolf smoke generator (UGV, remote-controlled) - obscuration of the breach site.
- "Terrier" armored digger (UGV, remote-controlled) - obstacle reduction / digging.
- Automated Direct and Indirect Mortar (remote-controlled) - suppression.
- Assault Breacher Vehicle x2 (UGV, remote-controlled) - mine-clearing line charge to clear a lane, lane-marking stakes, and blade to fill the tank trench.
- (Supported/maneuver: M1 Abrams tank.)
- Autonomy: reported as remotely controlled / teleoperated.

**Measures of Performance:**
- [inferred] A cleared, marked, and proofed lane through the obstacle.
- [inferred] Obstacle (minefield + trench) reduced.
- [inferred] Soldiers kept out of the point of breach.

**Scenario steps (SOSRA-style breach):**
1. RAS/ISR reconnoiter the complex obstacle. (Reduction planning.)
2. Automated mortar suppresses the far-side/overwatch of the obstacle.
3. M58 Wolf smoke generator obscures the breach site.
4. "Terrier" armored digger reduces the obstacle.
5. (Yakima) First ABV fires a mine-clearing line charge -> clears a lane through the minefield -> emplaces stakes marking the safe lane.
6. Second ABV uses its blade to fill the anti-tank trench.
7. The maneuver force (M1 Abrams) assaults through the cleared, marked lane.

**Environment and constraints:** Complex obstacle (minefield plus anti-tank
ditch); military training areas (Grafenwoehr, Germany; Yakima, WA). Execution
context: field demonstration/experiment (remotely controlled systems). Rules of
engagement: combat breach against an emplaced obstacle. Detailed timings, unit
sizes, and comms: Not specified in source.

#### Conceptual model (ontology seed)
- **Domain and scope:** Robotic combined-arms breach of a complex obstacle to open a maneuver lane.
- **Concepts (classes):** Breach force, Complex obstacle, Minefield, Anti-tank trench, Smoke generator, Armored digger, Assault breacher vehicle, Mine-clearing line charge, Cleared lane, Lane marker, Engineering effect.
- **Taxonomy (IS-A):**
  - Autonomous system -> UGV -> Smoke UGV, Digger UGV, Breacher UGV
  - Engineering effect -> Suppress, Obscure, Reduce, Clear lane, Mark lane, Fill trench
  - Complex obstacle -> Minefield, Anti-tank trench
- **Relationships (triples):**
  - Mortar | suppresses | far-side of obstacle
  - Smoke UGV | obscures | breach site
  - Digger UGV | reduces | Obstacle
  - Breacher UGV | clears | Lane (via mine-clearing line charge)
  - Breacher UGV | emplaces | Lane marker
  - Breacher UGV | fills | Anti-tank trench
  - Maneuver force | assaults through | Cleared lane
- **Properties:**
  - Assault breacher vehicle: mine-clearing line charge, blade, marking stakes
  - Smoke generator: obscuration
  - Digger: reduction/digging
  - Engineering effect: type (suppress/obscure/reduce/clear/mark/fill)
  - Cleared lane: marked, proofed state
- **Constraints/rules:**
  - Soldiers are removed from the point of breach (RAS perform the dangerous tasks).
  - Breach follows a suppress-obscure-reduce (SOSRA) sequence.

**Grounding check:** Source-fidelity caveat (built from reported facts, primary
page access-blocked); autonomy reported as teleoperation; three MoP items
[inferred]; some environment details "Not specified in source".
