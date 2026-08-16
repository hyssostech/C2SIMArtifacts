# Scenario extracted from paper (v2.2 prompt)

Langerwisch, M., Wittmann, T., Thamke, S., Remmersmann, T., Tiderko, A. & Wagner,
B. (2013). Heterogeneous teams of unmanned ground and aerial robots for
reconnaissance and surveillance - A field experiment. 2013 IEEE International
Symposium on Safety, Security, and Rescue Robotics (SSRR 2013). Source read in
full (local References PDF).

Standalone v2.2 record for a library paper (original V1 output:
[../Langerwisch_et_al2013.md](../Langerwisch_et_al2013.md), the documented
schema-drift case). The V1-vs-V2 comparison is in
[../V2-HeadToHead.md](../V2-HeadToHead.md) Case 4. Two distinct tasks (MOVE,
OBSERVE) are emitted as two records.

### Scenario 1: Coordinated formation MOVE of a heterogeneous UGV/UAV team

**Domain / mission type:** land (off-road field); coordinated relocation / convoy movement.

**Source location:** Sec. V.A "Scenarios" (MOVE), Sec. VI.B "MOVE Scenario".

**Purpose (why the authors present it):** To demonstrate the ROS/BML-over-3G
interfaces and autonomous coordinated movement of an arbitrary-size heterogeneous
team. (Research/demo intent.)

**Summary narrative:** An operator sets a destination; the team moves there in a
coordinated fashion. By design the UAVs take a constant formation escorting the
leading ground vehicle while the leading UGV (HANNA) follows a pre-known road
network and the remaining UGVs convoy one by one. A central planner on the leading
vehicle computes each vehicle's follow-target and following distance. In the
reported field run the four-UGV team reached the destination in convoy; the UAVs
were not part of that particular MOVE test.

**In-world objectives:** Relocate the whole multi-robot team to a specified destination in coordinated escort/convoy formation.

**Autonomous systems employed:**
- Lead UGV HANNA (UGV; Kawasaki Mule 3010) - hosts the central planner; follows road network.
- UGV LONGCROSS (UGV, wheeled), UGV GARM (UGV, tracked) - convoy followers.
- UGV AMOR (UGV; Yamaha quad) - convoy follower.
- UAV PSYCHE 1000 x2 (UAV; MD4-1000 quadrocopter) - escort formation by design; absent in the MOVE run.
- Autonomy: autonomous navigation; each vehicle self-responsible for following exactly one vehicle.

**Measures of Performance:**
- Successful arrival of the UGV team at the destination in convoy formation (stated).
- [inferred] Formation/convoy maintenance and real-time position reporting over ROS/BML/3G.

**Scenario steps:**
1. Operator sets a destination point on the GUI map.
2. Task transmitted to lead UGV HANNA -> initializes task distribution and planners.
3. Central planner computes a convoy order (follow-target + following distance) -> submits to active vehicles.
4. (By design) UAVs form a constant escort formation around the lead UGV via decentral coordination.
5. Lead UGV approaches the destination on the pre-known road network; other UGVs convoy one by one.
6. UGV team reaches the destination in convoy formation.

**Environment and constraints:** Field camp with gravel roads, fences, buildings,
and obstacles; OSM road network available; comms ROS/BML over 3G mobile radio
(200+ ms RTT deemed negligible). Execution context: field-experiment (live). Rules
of engagement: Not applicable. As-designed vs as-run: MOVE design includes a UAV
escort formation, but the reported MOVE test used UGVs only.

#### Conceptual model (ontology seed)
- **Concepts (classes):** Multi-robot team, Lead UGV, Follower UGV, Escort UAV, Central planner, Convoy order, Road network, Destination.
- **Taxonomy (IS-A):** Autonomous system -> UGV, UAV; UGV -> Lead UGV, Follower UGV.
- **Relationships (triples):** Central planner | assigns | Convoy order; Follower UGV | follows | Lead UGV; Escort UAV | escorts | Lead UGV; Lead UGV | traverses | Road network.
- **Properties:** Lead UGV: hosts planner, road-constrained; Follower UGV: follow-target, following distance; Escort UAV: formation shape (depends on active UAV count).
- **Constraints/rules:** Lead UGV stays on the pre-known road network; each vehicle follows exactly one vehicle; planner adapts to the number of active vehicles.

**Grounding check:** MoP item 2 [inferred]; ROE Not applicable; as-run deviation from design noted. Others grounded.

---

### Scenario 2: OBSERVE - autonomous POI surveillance and moving-object detection

**Domain / mission type:** land + air; point-of-interest observation / reconnaissance-surveillance.

**Source location:** Sec. V.A (OBSERVE), Sec. VI.C "OBSERVE Scenario".

**Purpose (why the authors present it):** To show autonomous reconnaissance and surveillance of a POI by a heterogeneous ground/air team. (Research/demo intent.)

**Summary narrative:** An operator marks a point of interest (a switch box on a
lamp post) in the GUI aerial image; the team of four UGVs and two UAVs approaches
the POI as in the MOVE scenario. On arrival the UGVs distribute evenly around the
POI with sensors focused on it, one UAV holds position directly above the POI with
its camera pointed down, and the remaining UAVs orbit the POI with cameras fixed on
it. The team performs continuous moving-object detection; pedestrians and an
unknown vehicle entering the area are detected and tagged, the operator is alarmed
and can request imagery (e.g. an aerial photo from the overhead UAV).

**In-world objectives:** Observe an operator-designated POI and autonomously detect and tag moving objects (pedestrians, vehicles) around it; alert the operator.

**Autonomous systems employed:** Same team as Scenario 1. Roles: UGVs distribute
around the POI with focused sensors (Velodyne HDL-64E); one UAV overhead (downward
14.7 MP zoom camera); other UAVs orbit with cameras on the POI.

**Measures of Performance:**
- Vehicles autonomously take their assigned observation positions (stated).
- Successful detection and classification of moving objects - pedestrians and an unknown vehicle (stated).
- Operator alerted and able to request pictures (stated).

**Scenario steps:**
1. Operator marks the POI in the GUI aerial image -> team task transmitted.
2. Team approaches the POI (via the MOVE behavior).
3. At proximity, the planner computes observation poses on a circular path of predefined radius around the POI (optionally constrained to the road network).
4. UGVs distribute evenly around the POI with sensors focused; one UAV positions directly above (camera down); other UAVs orbit with cameras on the POI.
5. Team performs continuous moving-object detection.
6. Moving objects detected and tagged (pedestrian = cross icon, vehicle = circle icon) in the GUI.
7. Operator is alarmed -> requests pictures -> overhead UAV supplies an aerial image.

**Environment and constraints:** Same field camp; POI = switch box on a lamp post;
comms ROS/BML/3G. Execution context: field-experiment (live). Rules of engagement:
Not applicable (observation task).

#### Conceptual model (ontology seed)
- **Concepts (classes):** Multi-robot team, UGV, UAV, Point of interest (POI), Observation pose, Moving-object detection, Pedestrian, Vehicle, Operator alert.
- **Taxonomy (IS-A):** Autonomous system -> UGV, UAV; Detected object -> Pedestrian, Vehicle.
- **Relationships (triples):** Operator | designates | POI; UGV | observes | POI; UAV | observes | POI; Team | detects | Moving object; Team | alerts | Operator.
- **Properties:** POI: position; Observation pose: circular radius, orientation-to-POI; UAV: overhead vs orbiting role; Detected object: type (pedestrian/vehicle).
- **Constraints/rules:** One UAV directly overhead, remaining UAVs orbit; observation poses may be constrained to road segments; detection runs continuously.

**Grounding check:** All fields grounded in source.
