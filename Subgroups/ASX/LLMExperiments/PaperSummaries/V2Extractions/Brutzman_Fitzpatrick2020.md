# Scenario extracted from paper (v2.2 prompt)

Brutzman, D.P., Fitzpatrick, C.R. (2020). Creating Virtual Environments for
Evaluating Human-Machine Teaming. Naval Postgraduate School Technical Report
NPS-MV-20-001 (DTIC AD1127315). Source read in full (report PDF).

This is the standalone v2.2 record for a paper already in the library
([../Brutzman&Fitzpatrick2020.md](../Brutzman&Fitzpatrick2020.md) is the original
V1 output). The V1-vs-V2 comparison for this paper is in
[../V2-HeadToHead.md](../V2-HeadToHead.md) Case 1 - it is the documented
goal-leak failure case.

### Scenario 1: Kilo 2 village/urban MUM-T ISR and movement to contact

**Domain / mission type:** urban (land); ISR + movement-to-contact / fire coordination.

**Source location:** Section E "Exemplar Mission Design and Portrayal" (p. 21-22, Figures 2-5); MCWL visualization subsection (p. 33-34).

**Purpose (why the authors present it):** A simple exemplar to demonstrate
virtual-environment and agent-based assessment of Manned-Unmanned Teaming (MUM-T),
and to show that portraying one situation multiple ways yields comparative insight.
(Research/demo intent - not the in-world objective.)

**Summary narrative:** On the Kilo 2 range at Camp Pendleton, CA, a platoon-sized
blue force (Marines) teamed with unmanned systems defends a small village model
against a fire-team-sized hostile red force. The red force is emplaced on the
northwest corner with small arms and rifles, without supporting arms or ISR. The
blue force, on the east side, is assigned a single UAS and two UGVs for ISR. The
unmanned systems conduct initial reconnaissance to establish situational awareness;
the blue platoon then conducts a movement to contact to the northwest, using
real-time UAS and UGV feeds of red-force disposition to plan and coordinate air,
naval, and ground fires against the red force. The mission is portrayed in four
variations (day/night x UAS/UGV viewpoint, including a night version with flare
illumination in which the UGVs engage).

**In-world objectives:**
- Establish situational awareness of red-force disposition using UAS and UGV ISR.
- Conduct movement to contact and engage the red force.
- Plan and coordinate air, naval, and ground fires using real-time robotic intelligence.

**Autonomous systems employed:**
- Single UAS (UAV) - aerial ISR/overwatch; entity-viewpoint video feed of red disposition. Level of autonomy: Not specified in source.
- Two UGVs (UGV) - forward ground ISR; video feed; in the fourth variation, engage the red force. Level of autonomy: Not specified in source.

**Measures of Performance:**
- Number of red and blue kills.
- Comparative insight across the four portrayals (time-of-day and viewpoint effects).
- [inferred] Timeliness/quality of situational awareness and fire coordination enabled by the robotic feeds.

**Scenario steps:**
1. Red fire-team emplaces on the NW corner with small arms; no ISR, no supporting arms.
2. Blue platoon positions on the east side; assigned 1 UAS and 2 UGVs for ISR.
3. UAS and UGVs conduct initial reconnaissance of the area -> establish situational awareness.
4. UAS and UGVs generate entity-viewpoint video -> provide actual red-force disposition data.
5. Blue platoon conducts movement to contact to the northwest -> to engage the red force.
6. Blue force uses real-time robotic intelligence -> plans and coordinates air, naval, and ground fires -> initially engages red force.
7. Red and blue entities search, acquire, target, and engage -> outcomes adjudicated from internal parametric data (open-loop run).
8. (Fourth variation, night) UGVs engage the red force under flare illumination.

**Environment and constraints:** Urban/village terrain, Kilo 2 range, Camp
Pendleton, CA. Execution context: virtual (VT MAK VR Forces, DIS protocol),
agent-based, run open-loop to stay reactive to robotic surveillance. Same-mission
variations: (1) day/UAS view, (2) day/UGV view, (3) night/UAS with illumination,
(4) night/UAS with UGVs engaging. Constraint: red force fielded no robotic systems
and could not target blue units - the authors note this would have changed the
outcome.

#### Conceptual model (ontology seed)
- **Domain and scope:** Manned-unmanned teaming (MUM-T) in small-unit urban combat, assessed in a virtual environment.
- **Concepts (classes):** Blue force (Marine platoon), Red force (hostile fire-team), UAS, UGV, ISR operation, Movement to contact, Fire coordination, Portrayal/viewpoint, Environmental condition.
- **Taxonomy (IS-A):**
  - Autonomous system -> UAS
  - Autonomous system -> UGV
  - Force -> Blue force
  - Force -> Red force
  - Operation -> ISR operation
  - Operation -> Movement to contact
- **Relationships (triples):**
  - Blue force | employs | UAS
  - Blue force | employs | UGV
  - UAS | conducts | ISR operation
  - UGV | conducts | ISR operation
  - UAS | provides | red-force disposition data
  - Blue force | conducts | Movement to contact
  - Blue force | coordinates | air/naval/ground fires
  - Blue force | engages | Red force
  - UGV | engages | Red force (fourth variation)
- **Properties:**
  - Blue force: size (platoon), position (east), assets (1 UAS, 2 UGVs)
  - Red force: size (fire-team), position (NW corner), armament (small arms/rifles), ISR (none), supporting arms (none)
  - UAS: role (ISR), viewpoint (aerial)
  - UGV: role (ISR/engage), count (2)
  - Environmental condition: time of day (day/night), illumination (flares)
- **Constraints/rules:**
  - Red force deployed no robotic systems and could not target blue units.
  - Simulation run open-loop to remain reactive to robotic surveillance.
  - Engagement outcomes adjudicated from internal parametric data.

**Grounding check:** MoP item 3 is [inferred]; levels of autonomy "Not specified in source". All other fields grounded in source.
