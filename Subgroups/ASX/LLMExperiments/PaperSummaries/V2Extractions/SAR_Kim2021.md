# Scenario extracted from report (v2.2 prompt)

Kim, et al. (2021). Smart Search System of Autonomous Flight UAVs for Disaster
Rescue. Sensors (MDPI), PMC8537596. Source read in full (open-access article
text).

Sourced against `InstantiationReview/Documents-Needed.md` request #7 (humanitarian
SAR, non-combat). Grounds G10 (no-adversary / neutral framing), R2 (survivor
detection + approach), Q-N (area search); also touches denied-comms.

### Scenario 1: Autonomous UAV radio-signal search for a survivor in a comms/GPS-denied disaster area

**Domain / mission type:** air; humanitarian search-and-rescue (survivor localization), non-combat.

**Source location:** Sections 3.1-3.2 (architecture, communication procedure) and 4 (real-world flight tests).

**Purpose (why the authors present it):** To propose and validate an autonomous
UAV smart-search system that locates a distressed person by their radio signal in
areas without mobile-network or GPS coverage. (Research/demo intent.)

**Summary narrative:** One or more autonomous fixed-wing UAVs search a disaster
area for a survivor who cannot call for rescue because the mobile network is down
or they are in a GPS-shadow area. Each UAV takes off and flies a random search
until it detects the survivor's radio signal (from a cellular/WiFi/RF terminal);
it then accumulates received-signal-strength (RSSI) and time-of-arrival (ToA)
data, shares it with other UAVs and a ground control system (GCS) over a
self-organizing mesh network, and runs an onboard genetic-algorithm localization
to estimate the survivor's position. The UAV continuously updates its waypoints
toward the improving estimate and approaches the survivor - all without direct
control from the GCS. The system was validated in two real-world flight tests
(about 4 km x 4 km and 1 km x 1 km) that successfully located a survivor.

**In-world objectives:**
- Locate a distressed survivor by radio signal in a comms/GPS-denied area, quickly and autonomously.
- Approach the survivor to enable rescue, minimizing search time over a large area.

**Autonomous systems employed:**
- Fixed-wing UAV, single or multiple (UAV) - autonomous flight, signal detection, cooperative localization, waypoint replanning toward the survivor. Autonomy: fully autonomous search (no direct GCS control); hierarchical path planning (VIN) for large-area coverage.
- Ground Control System (GCS) - shares data, runs the same Smart Search module, publishes trajectories/estimates to a web/cloud service (not a platform).

**Measures of Performance:**
- Error between the estimated survivor position and the actual position (localization accuracy).
- Search/localization time over the target area (speed of rescue).
- [inferred] Direct-communication success rate over the mesh (~98% with up to four retransmissions, reported for the link).

**Scenario steps:**
1. Each UAV takes off and flies in a random direction ("random flight") until it catches the survivor's radio signal.
2. On detecting the signal, the UAV shares/exchanges its data (drone ID, lat/long/altitude, RSSI, ToA at time of reception) with other UAVs and the GCS over the mesh network (OLSR routing).
3. Each UAV/GCS agent runs its onboard Smart Search module -> estimates the survivor's location via the genetic-algorithm localization (RSSI + ToA, noise-filtered).
4. UAVs update their waypoints toward the estimated location and fly toward it, refining the estimate as they approach.
5. GCS uploads UAV trajectories and the estimated location to a web/cloud service for sharing with rescue applications.
6. The UAV approaches the survivor's localized position, enabling rescue.

**Environment and constraints:** Large disaster area (tested at 4 km x 4 km and
1 km x 1 km); no mobile network and/or GPS-shadow conditions; noisy RF
environment. Execution context: field-experiment (real-world flight tests) plus
the modeled algorithm. Rules of engagement: Not applicable (non-combat SAR;
survivor is a neutral actor to be located and helped). Constraints: rotary-wing
endurance is short (2-30 min) so the design favors radio-signal search over
camera close-up; localization must work without GPS/infrastructure anchors.

#### Conceptual model (ontology seed)
- **Domain and scope:** Autonomous multi-UAV radio-signal search and localization of a survivor in a comms/GPS-denied disaster area.
- **Concepts (classes):** Search UAV, Ground control system, Survivor, Radio signal, Signal measurement (RSSI/ToA), Location estimate, Search area, Mesh network.
- **Taxonomy (IS-A):**
  - Autonomous system -> UAV -> Fixed-wing search UAV
  - Detected entity -> Survivor (neutral actor)
  - Signal measurement -> RSSI, Time-of-arrival
- **Relationships (triples):**
  - Search UAV | detects | Radio signal (of Survivor)
  - Search UAV | shares measurement with | other UAV / GCS
  - UAV/GCS | estimates | Survivor location
  - Search UAV | updates waypoints toward | Location estimate
  - Search UAV | approaches | Survivor
- **Properties:**
  - Search UAV: autonomous, endurance, signal receiver, planner (hierarchical VIN)
  - Signal measurement: RSSI value, ToA, position/time of reception
  - Location estimate: lat/long, valid/invalid flag, error vs actual
  - Search area: size (e.g. 4 km x 4 km)
- **Constraints/rules:**
  - Search proceeds without direct GCS control (autonomous).
  - Localization must work without GPS/infrastructure anchors (genetic algorithm over RSSI/ToA).
  - Data shared over a mesh network with retransmission for reliability.

**Grounding check:** One MoP item [inferred, link-level figure]; ROE "Not
applicable". All other fields grounded in source.
