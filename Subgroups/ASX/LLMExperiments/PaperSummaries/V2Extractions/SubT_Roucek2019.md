# Scenario extracted from report (v2.2 prompt)

Roucek, T., et al. (2019). DARPA Subterranean Challenge: Multi-robotic
Exploration of Underground Environments. Modelling and Simulation for Autonomous
Systems (MESAS 2019). Source read in full:
`References/` (comrob.fel.cvut.cz/papers/mesas19subt.pdf).

### Scenario 1: Heterogeneous multi-robot subterranean artifact search

**Domain / mission type:** subterranean; autonomous exploration / search-and-rescue (artifact detection and report).

**Source location:** Abstract; Sec. 3.1 Contest Environment; 3.2 Artifacts and Scoring; Sec. 4 Robots.

**Purpose (why the authors present it):** To describe and evaluate the CTU-CRAS
team's heterogeneous multi-robot exploration system entered in the DARPA
Subterranean Challenge, and to share lessons learned. (Research/demo intent.)

**Summary narrative:** A heterogeneous team of unmanned robots is deployed into a
GPS-denied, radio-limited underground environment (a mine for the Tunnel round)
to autonomously explore, detect, and localize specified artifacts (backpacks,
fire extinguishers, drills, human survivors, cell phones) and report each
artifact's type and position to a DARPA-provided interface, then return toward
the control station. Because communication is intermittent, the wheeled robot
deploys communication relays to maintain a low-bandwidth link. The same mission
recurs across four rounds (Tunnel, Urban, Cave, and a combined final) with
different environments and artifact sets.

**In-world objectives:**
- Autonomously explore the underground environment without GPS.
- Detect and localize specified artifacts within the allowed error bound.
- Report artifact type and position to the control station and return.

**Autonomous systems employed:**
- Wheeled UGV, Husky A200 (x1) - fast traversal; carries and deploys communication relays. Autonomous (comms-denied operation required).
- Tracked UGV, Absolem (x2) - difficult-terrain search of areas the Husky cannot reach. Autonomous.
- Legged UGV, PhantomX hexapod (x2) - narrow/constrained-passage traversal. Autonomous (~1 h endurance).
- Quadrotor UAV (x2) - terrain-independent access; short endurance, reduced sensor payload. Autonomous.

**Measures of Performance:**
- Points for each artifact reported with correct type and position within the DARPA error bound.
- Score decremented for false-positive detection or mislocalization.

**Scenario steps:**
1. Team deploys at the environment entrance -> begins autonomous exploration (no GPS).
2. Robots distribute by capability -> tracked/legged robots take difficult or constrained terrain, wheeled robot takes faster open runs, UAVs take terrain-independent access.
3. Husky deploys communication relays -> maintains a low-bandwidth link to the control station.
4. Robots run onboard SLAM/mapping and object detection -> detect artifacts.
5. Robot sends a message (artifact type + position) to the DARPA interface -> scoring.
6. Robots return toward the control station.

**Environment and constraints:** Underground - mine (Tunnel), parking lot/subway
(Urban), natural caverns (Cave); little or no GPS, very limited radio,
fog/smoke/mud/water/reflective surfaces. Execution context: field-experiment
(live robots), preceded by an integration exercise (STIX). Rules of engagement:
Not applicable (no adversary). Same-mission variations: the four competition
rounds (Tunnel, Urban, Cave, Final). Time limit per run.

#### Conceptual model (ontology seed)
- **Domain and scope:** Autonomous heterogeneous multi-robot exploration and artifact reporting in GPS-denied underground environments.
- **Concepts (classes):** Robot team, Wheeled UGV, Tracked UGV, Legged UGV, Quadrotor UAV, Artifact, Control station, Communication relay, Environment round, Score.
- **Taxonomy (IS-A):**
  - Autonomous system -> UGV
  - Autonomous system -> UAV
  - UGV -> Wheeled UGV
  - UGV -> Tracked UGV
  - UGV -> Legged UGV
  - UAV -> Quadrotor UAV
- **Relationships (triples):**
  - Robot team | explores | Environment round
  - Robot | detects | Artifact
  - Robot | reports | Artifact position
  - Wheeled UGV | deploys | Communication relay
  - Communication relay | links | Robot team to Control station
  - Score | increases_with | correct Artifact report
  - Score | decreases_with | false positive
- **Properties:**
  - Wheeled UGV (Husky A200): speed (<=3 m/s), payload (<=50 kg), sensors (3D lidar, 5 RGB cameras), carries relays
  - Tracked UGV (Absolem): flippers, pivoting lidar, difficult-terrain role
  - Legged UGV (hexapod): speed (~0.2 m/s), endurance (~1 h), constrained-passage role
  - Quadrotor UAV: terrain-independent, short endurance, reduced payload
  - Artifact: type, position, error bound
- **Constraints/rules:**
  - No GPS and limited radio -> robots must operate autonomously.
  - A report scores only if type is correct and position is within the error bound.
  - False positives and mislocalizations reduce the score.

**Grounding check:** Rules of engagement "Not applicable" (no adversary). All other fields grounded in source.
