# Scenario extracted from report (v2.2 prompt)

Muster, L., et al. (2024). UGV-CBRN: An Unmanned Ground Vehicle for Chemical,
Biological, Radiological, and Nuclear Disaster Response. arXiv:2406.14385. Source
read in full (arXiv PDF).

Sourced to fill ASX validation hole #2 (CBRN reconnaissance) from
`InstantiationReview/Documents-Needed.md`. Grounds Q-Q (Y3/Y5), Q-M (N1); also
grounds manipulation (E1/E2, request #9) and no-adversary framing (G10,
request #7) as bonus overlaps.

### Scenario 1: Unmanned CBRN reconnaissance - radiation mapping, valve closure, and substance sampling

**Domain / mission type:** land (indoor disaster site); CBRN reconnaissance - hazard detection/mapping plus manipulation (leak stop, sampling).

**Source location:** Sections III (Integrated Robotic System: Mapping/Exploration, Radiation Mapping, Manipulation/Sampling/Analysis, System Operation) and IV (evaluation in three scenarios).

**Purpose (why the authors present it):** To present and field-evaluate an
integrated UGV that combines autonomous mapping with semi-autonomous manipulation
for CBRN response. (Research/demo intent.)

**Summary narrative:** A tracked UGV (Taurob Tracker) is deployed into a
radiological/CBRN disaster site to autonomously navigate, explore, and build both
a geometric map and a radiation map that localizes radiation sources, keeping
human responders out of the hazard zone. A remote operator monitors progress,
aligns the geometric and radiation maps, defines target locations, and directs
semi-autonomous manipulation - closing valves to stop contaminant leakage and
collecting substance samples that are analyzed on-site by a handheld Raman
spectrometer. High-responsibility tasks (valve closing, sampling) are kept
semi-autonomous with the operator verifying end-effector poses; manual input is
always preferred over autonomous behavior. The system was field-tested at the
European Robotics Hackathon (EnRicH) 2023 CBRN challenge and a disaster-relief
training area, across three scenarios.

**In-world objectives:**
- Autonomously locate and map radiation sources across the disaster area.
- Stop contaminant leakage by closing valves.
- Sample and identify hazardous substances on-site.
- Keep human operators out of the contaminated zone.

**Autonomous systems employed:**
- Taurob Tracker UGV (tracked UGV) - autonomous navigation/exploration and mapping; semi-autonomous manipulation. Level of autonomy: autonomous (nav/mapping) and semi-autonomous teleoperation (manipulation; operator verifies poses).
- Sensors/effectors carried: dual depth/LiDAR + IMU (geometric mapping), radiation detector / Geiger counter (radiation), 4-DoF arm with a custom 2-in-1 end-effector (valves + sampling), onboard Raman spectrometer (substance analysis).

**Measures of Performance:**
- [inferred] Accuracy/coverage of the radiation-source localization and map.
- [inferred] Successful valve closure (leak stopped).
- [inferred] Successful sample collection and correct substance identification.
- (EnRicH challenge scoring implied but not detailed in source.)

**Scenario steps:**
1. UGV deploys into the disaster area -> autonomous frontier-based exploration and navigation (2D/3D SLAM), with recovery behaviors (on collision: backtrack 0.3 m, clear costmap, replan; abort the goal after three failed attempts).
2. UGV synchronizes radiation-detector counts with its pose -> builds a radiation map via Gaussian-process regression -> localizes radiation sources.
3. Operator aligns the geometric and radiation maps and defines target locations.
4. Operator directs semi-autonomous manipulation -> end-effector closes a valve (up to 160 mm) to stop contaminant leakage (operator verifies/refines the tool-center-point pose).
5. Operator directs sampling -> end-effector grasps a probe -> collects a surface sample -> stores the probe in the on-board tray.
6. Sampled substance is analyzed on-site with the handheld Raman spectrometer -> chemical identification.
7. Throughout, the system switches between autonomous navigation and operator input by predetermined priority; manual input is always preferred.

**Environment and constraints:** Tight indoor urban-search-and-rescue spaces
(narrow doors force costmap padding down to 50 mm, raising collision risk ->
extra collision detection/recovery); radiological hazard. Execution context:
field-experiment (EnRicH 2023 CBRN challenge and a disaster-relief training area;
three scenarios). Rules of engagement: Not applicable (disaster response, no
adversary). Constraint: high-responsibility tasks require a human in the loop.

#### Conceptual model (ontology seed)
- **Domain and scope:** Autonomous/semi-autonomous CBRN reconnaissance and hazard mitigation by a single UGV with manipulation.
- **Concepts (classes):** CBRN UGV, Radiation detector, Manipulator/End-effector, Raman spectrometer, Radiation source, Valve, Substance sample, Radiation map, Geometric map, Operator.
- **Taxonomy (IS-A):**
  - Autonomous system -> UGV -> Tracked UGV
  - Sensor -> Radiation detector, LiDAR, IMU
  - Actuator -> Manipulator / End-effector
  - Detected hazard -> Radiation source, Chemical substance
- **Relationships (triples):**
  - UGV | detects and localizes | Radiation source
  - UGV | builds | Radiation map
  - End-effector | closes | Valve
  - End-effector | samples | Substance
  - Raman spectrometer | analyzes | Substance
  - Operator | directs | Manipulation
  - Operator | defines | Target location
- **Properties:**
  - Radiation detector: Geiger counts
  - Radiation map: per-cell radiation estimate + variance (confidence)
  - Valve: diameter (<= 160 mm), grip type (external/internal)
  - Substance sample: probe id, identified substance type
  - End-effector: degrees of freedom, grip
- **Constraints/rules:**
  - Manipulation is semi-autonomous; the operator verifies the end-effector pose and manual input is preferred.
  - Navigation aborts the goal after three failed recovery attempts.
  - The radiation map is aligned to the geometric map by the operator.

**Grounding check:** MoP items are [inferred] (challenge scoring not detailed);
ROE "Not applicable". All other fields grounded in source.
