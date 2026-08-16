# Scenario extracted from report (v2.2 prompt)

Overview of the Mobile Detection Assessment and Response System (MDARS). U.S. Army
PM Physical Security Equipment / SPAWAR, DTIC ADA422465 (and related MDARS reports
ADA449408, ADA305076). Source read in full (report PDF).

Sourced against `InstantiationReview/Documents-Needed.md` request #4 (persistent
surveillance / sentry / standing watch). Grounds N2 (standing/persistent task with
cadence), Q-U (station-keeping / relief hand-off), Q-N (area coverage).

### Scenario 1: Autonomous standing-watch security patrol of a depot (MDARS)

**Domain / mission type:** land; persistent surveillance / autonomous sentry (physical security and inventory) - force protection.

**Source location:** Overview (system description, CONOPS); Interior and Exterior platform sections; Multiple Robot Host Architecture.

**Purpose (why the authors present it):** To field an autonomous robotic security
and inventory system that offsets a shrinking guard force at DoD depots.
(Program/capability intent.)

**Summary narrative:** One or more autonomous MDARS platforms - Interior platforms
inside warehouses and Exterior platforms in storage yards - conduct continuous
security patrols of designated regions at a DoD depot. Each robot patrols on its
own, detecting intruders with passive-infrared and microwave motion sensors and
day/night imagers, assessing and responding (audio challenge-and-response), and
performing product and barrier inventory via interactive RF transponder tags. A
Multiple Robot Host Architecture lets a single guard oversee many platforms from
one host console. Each robot keeps its standing watch until an exceptional event
occurs - an intruder is detected, the robot becomes trapped, or a fire is found -
at which point the guard intervenes from the console and directly interacts with
the reporting platform. The system was under operational evaluation at Hawthorne
Army Depot.

**In-world objectives:**
- Maintain continuous physical security (intruder detection, assessment, response) over the depot.
- Perform product and barrier inventory to prevent loss/theft.
- Offload routine standing watch from human guards (one guard oversees many robots).

**Autonomous systems employed:**
- MDARS Interior platform (UGV) - warehouse patrol, intruder detection, RF-tag inventory. Autonomy: semi-autonomous navigation, obstacle avoidance; guard on-the-loop.
- MDARS Exterior platform (UGV) - storage-yard patrol and assessment. Autonomy: semi-autonomous.
- Host console (Multiple Robot Host Architecture) - one guard supervises many platforms (not a platform).

**Measures of Performance:**
- Probability of intruder detection.
- Inventory/barrier assessment accuracy.
- Number of platforms a single guard can oversee (MRHA supports many, up to 255 platforms/sensors).

**Scenario steps:**
1. Robot conducts an autonomous patrol of its designated region (standing watch), on a repeating cadence.
2. Robot senses continuously (passive IR + microwave motion + day/night imagers).
3. On intruder detection -> assess the contact -> respond (audio challenge-and-response) -> report the exceptional event to the host.
4. The guard at the host console intervenes and directly interacts with the reporting platform.
5. During patrol, the robot performs RF-tag product inventory and barrier assessment.
6. Patrol resumes; the standing watch continues on its revisit cadence, with relief/hand-off to the guard on exceptional events.

**Environment and constraints:** DoD warehouse interiors and storage-yard
exteriors (Camp Elliott test site; Hawthorne Army Depot operational evaluation).
Execution context: fielded operational evaluation (live). Rules of engagement:
physical-security challenge-and-response (non-lethal). Constraint: one guard
oversees many platforms via the host architecture; robot acts autonomously until
an exceptional event triggers guard intervention.

#### Conceptual model (ontology seed)
- **Domain and scope:** Persistent autonomous security patrol (standing watch) with human-on-the-loop intervention on exceptional events.
- **Concepts (classes):** Security robot, Patrol region, Standing watch, Intruder, Exceptional event, Host console, Guard, Inventory tag, Barrier.
- **Taxonomy (IS-A):**
  - Autonomous system -> UGV -> Interior security UGV, Exterior security UGV
  - Exceptional event -> Intruder detected, Robot trapped, Fire detected
  - Task -> Standing-watch patrol, Inventory assessment
- **Relationships (triples):**
  - Security robot | patrols | Patrol region
  - Security robot | detects | Intruder
  - Security robot | reports | Exceptional event to Host console
  - Guard | intervenes on | Exceptional event
  - Security robot | assesses | Inventory / Barrier
  - Host console | supervises | many Security robots
- **Properties:**
  - Standing-watch patrol: region, revisit cadence, autonomous-until-exception
  - Sensors: passive IR, microwave motion, day/night imager
  - Host console: number of platforms overseen
  - Response: audio challenge-and-response
- **Constraints/rules:**
  - The robot patrols autonomously until an exceptional event, then the guard intervenes (on-the-loop relief).
  - One guard oversees many platforms.

**Grounding check:** All fields grounded in source (CONOPS and platform
descriptions); MoP grounded (probability of detection, MRHA platform count).
