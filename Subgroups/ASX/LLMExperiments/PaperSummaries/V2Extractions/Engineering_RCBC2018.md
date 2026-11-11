# Scenario extracted from report (v2.2 prompt)

U.S. Army, Robotic Complex Breach Concept (RCBC): the Grafenwoehr demonstration
(6 April 2018) and the follow-on combined-arms robotic breach at Joint Warfighting
Assessment 2019 (JWA 19), Yakima Training Center, 2nd Battalion, 3rd Infantry
Regiment (1st Brigade, 2nd Infantry Division SBCT); led by Fort Benning's
Cross-Domain Maneuver Battle Lab, sponsored by Army Futures Command. Corroborated
across army.mil (articles 203482, 218538, 221845), Breaking Defense, Defense News,
and DVIDS JWA19 coverage.

Source-fidelity note: this record is built from consistent, multiply-corroborated
open reporting of the demonstrations (named units, platforms, obstacle
composition, vehicle counts, and timing). The Maneuver Battle Lab compiled a
final JWA 19 assessment report, but that primary report is not openly available;
so step-level timings and internal metrics remain "Not specified in source".
Platform autonomy is reported as remote-control / teleoperation.

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
in support of an M1 Abrams. In the follow-on Yakima exercise (JWA 19), a
combined force of 10 unmanned and 6 manned vehicles attacks an obstacle layered
with a minefield, wire, and a deep anti-tank trench: a first Assault Breacher
Vehicle (ABV) fires a mine-clearing line charge to clear a lane through the
minefield and emplaces stakes marking where it is safe to drive, and a second ABV
uses its blade to fill the trench. The robotic and autonomous systems perform the
intelligence, suppression, obscuration, and reduction tasks so that soldiers are
not exposed at the point of breach; the second breach run took about 30 minutes
less than the first, roughly matching a manned operation's time.

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
- Breach time vs a manned operation (the JWA 19 second run took ~30 min less than the first, roughly matching manned timing).
- [inferred] A cleared, marked, and proofed lane through the obstacle.
- [inferred] Obstacle (minefield + wire + trench) reduced.
- [inferred] Soldiers kept out of the point of breach.

**Scenario steps (SOSRA-style breach):**
1. RAS/ISR reconnoiter the complex obstacle. (Reduction planning.)
2. Automated mortar suppresses the far-side/overwatch of the obstacle.
3. M58 Wolf smoke generator obscures the breach site.
4. "Terrier" armored digger reduces the obstacle.
5. (Yakima) First ABV fires a mine-clearing line charge -> clears a lane through the minefield -> emplaces stakes marking the safe lane.
6. Second ABV uses its blade to fill the anti-tank trench.
7. The maneuver force (M1 Abrams) assaults through the cleared, marked lane.

**Environment and constraints:** Complex obstacle layered with a minefield, wire,
and a deep anti-tank trench; military training areas (Grafenwoehr, Germany;
Yakima, WA). Force at JWA 19: 10 unmanned and 6 manned vehicles. Execution
context: field demonstration/experiment (remotely controlled systems). Rules of
engagement: combat breach against an emplaced obstacle. Internal metrics and
step-level timings from the Maneuver Battle Lab report: Not specified in source.

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

**Grounding check:** Built from multiply-corroborated open reporting (units,
platforms, obstacle composition, vehicle counts, and breach-time comparison are
consistent across sources); the primary Maneuver Battle Lab report is not open, so
internal metrics/step-timings are "Not specified in source". Autonomy reported as
teleoperation; three MoP items [inferred].
