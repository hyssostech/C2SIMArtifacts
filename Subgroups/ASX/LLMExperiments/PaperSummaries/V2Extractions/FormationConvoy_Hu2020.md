# Scenario extracted from report (v2.2 prompt)

Hu, X. (2020). Modeling and Development of Operation Guidelines for Leader-Follower
Autonomous Truck-Mounted Attenuator Vehicles. University of Missouri / U.S. DOT
technical report (arXiv:2104.06507). Source read in full (report PDF).

Sourced against `InstantiationReview/Documents-Needed.md` request #8 (formation /
convoy geometry). Grounds Q-U (formation/relative geometry), Q-L (escort/follow),
Q-P. Domain caveat: civilian highway work-zone, not military - included because it
grounds the leader-follower *geometry construct* concretely; the military convoy
instance is already covered by Langerwisch MOVE.

### Scenario 1: Leader-follower autonomous convoy maintaining a controlled follow-distance geometry

**Domain / mission type:** land; autonomous convoy / leader-follower formation-keeping (civilian highway maintenance).

**Source location:** Ch. 2 (Leader/Follower truck overview), Ch. 3.2.2 (Follow Distance and Accuracy), Ch. 4 (car-following and lane-changing gap models).

**Purpose (why the authors present it):** To develop operation guidelines and
spacing/gap models for a leader-follower autonomous truck-mounted-attenuator
(ATMA) system so it operates safely. (Research/guidelines intent.)

**Summary narrative:** During slow-moving mobile highway operations (striping,
sweeping, bridge flushing, pothole patching), a human-driven lead truck is trailed
by an autonomous follower truck (the attenuator) that drives autonomously to
follow the lead truck's path while maintaining a controlled following distance
within bounded accuracy. The lead-truck driver must make decisions from both
trucks' perspectives, because the follower's geometry depends on the leader. The
study models the minimum car-following distance the pair must keep and the
larger-than-normal critical gap the two-vehicle formation needs to change lanes.

**In-world objectives:**
- Keep the follower vehicle at a safe, accurate following distance behind the leader through the operation.
- Remove the human from the trailing struck-hazard vehicle while preserving the formation.

**Autonomous systems employed:**
- Follower truck / ATMA (UGV) - drives autonomously to follow the lead truck's path at a set gap. Autonomy: autonomous path-following of a designated leader.
- Lead truck (human-driven) - sets the route/pace; must account for the follower's constraints. (Manned.)

**Measures of Performance:**
- Follow-distance accuracy (error distribution around the target gap).
- Ability to hold the minimum car-following distance.
- Adequacy of the critical lane-changing gap for the two-vehicle formation.

**Scenario steps:**
1. The lead truck drives the work route at a slow operational pace.
2. The follower truck autonomously follows the lead truck's path at the set following distance.
3. The follower maintains the follow distance within accuracy bounds (bounded error).
4. For a lane change, the pair requires a larger-than-normal acceptable gap; the lead-truck driver waits for a gap sized for both vehicles before initiating.
5. The formation is preserved through the slow-moving mobile operation.

**Environment and constraints:** Public highway work zone; civilian domain;
low operational speed. Execution context: field testing plus modeling/analysis.
Rules of engagement: Not applicable. Constraint: the leader's driving decisions
must account for the follower (the geometry couples the two vehicles).

#### Conceptual model (ontology seed)
- **Domain and scope:** Leader-follower autonomous convoy formation-keeping with a controlled inter-vehicle geometry.
- **Concepts (classes):** Convoy/formation, Lead vehicle, Follower vehicle, Follow distance, Lane-changing gap, Path-following.
- **Taxonomy (IS-A):**
  - Autonomous system -> UGV -> Follower vehicle
  - Vehicle -> Lead vehicle (manned), Follower vehicle (autonomous)
  - Formation geometry -> Follow distance, Lane-changing gap
- **Relationships (triples):**
  - Follower vehicle | follows | Lead vehicle
  - Follower vehicle | maintains | Follow distance
  - Convoy | requires | Lane-changing gap
  - Lead vehicle | sets path for | Follower vehicle
- **Properties:**
  - Follow distance: target gap, accuracy / error bound
  - Lane-changing gap: required headway (larger than single-vehicle)
  - Formation: leader-follower relation, inter-vehicle spacing
- **Constraints/rules:**
  - The follower holds a bounded-error following distance behind the leader.
  - The two-vehicle formation needs a larger lane-change gap than a single vehicle.
  - The leader's decisions must account for the follower's geometry.

**Grounding check:** Domain is civilian (flagged); ROE "Not applicable". All other
fields grounded in source.
