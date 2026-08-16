# Scenario extracted from report (v2.2 prompt)

Remmersmann, T., Schade, U., Rein, K. & Tiderko, A. (2015). BML for Communicating
with Multi-Robot Systems. Fall Simulation Interoperability Workshop (Fall SIW
2015). Source read in full (local copy in `../../References/`).

Sourced against `InstantiationReview/Documents-Needed.md` request #6 (human-machine
teaming at the C2/tasking level). Grounds Q-G, Q-P; also directly informs the
report design (its measurement/media/equipment reports map onto ASX SensorObservation
and MediaReference).

### Scenario 1: Tasking a multi-robot system with high-level BML orders (human-machine teaming at the C2 level)

**Domain / mission type:** land; human-machine teaming - C2 tasking of a multi-robot system for reconnaissance and image/measurement reporting.

**Source location:** Sections 4 (disaggregation/tasking), 5 (reporting/aggregation); Listings 1-3.

**Purpose (why the authors present it):** To show how Battle Management Language
(BML) lets a human operator command a multi-robot system with high-level orders
that a planning node disaggregates into robot-level tasks, and how robot reports
are aggregated back. (Research/demo intent.)

**Summary narrative:** A human operator (working like a commander) issues a
high-level task in BML - for example, reconnoiter an area - to a control/planning
node that sits between the C2 system and a multi-robot system. The node
disaggregates the high-level order into simple robot tasks (move to a road, take a
picture of an observed object), assigns robots to tasks according to their current
positions, equipment, and capabilities, and tasks them to move to their assigned
roads to begin the reconnaissance. During execution it continuously checks whether
the robot-to-task assignment is still efficient and reassigns if a robot is slowed
by obstacles. Robots report upward: image/video availability (a "ResourceType"
report with a media URL and a geographic reference), sensor measurements (a
"WhoMeasuredType" report with value, unit of measure, phenomenon, sensor, time and
place), and their own mounted equipment ("WhoHoldingType"). The node aggregates
low-level task-status reports into a status report for the original high-level task.

**In-world objectives:**
- Reconnoiter the assigned area with the multi-robot system.
- Let the operator focus on mission-critical tasks while the planning node handles detailed task allocation.
- Return aggregated status, imagery, and measurement reports to the C2 system.

**Autonomous systems employed:**
- Multi-robot system (heterogeneous UGVs/UAVs) - execute disaggregated move / observe / image-gathering / measurement tasks. Autonomy: autonomous task execution under BML tasking; capability self-reported (reconfigurable robots report mounted equipment).
- Control/planning node - disaggregates high-level BML orders, assigns robots by capability, aggregates reports. (Software agent, not a platform.)

**Measures of Performance:**
- Aggregated high-level task completion (derived from all low-level task-status reports).
- [inferred] Task-assignment efficiency maintained under changing conditions (reassignment when a robot is slowed).

**Scenario steps:**
1. Operator issues a high-level BML order (e.g. reconnoiter an area) to the control/planning node.
2. Node disaggregates the order into simple robot tasks (move, take picture / image-intelligence).
3. Node assigns robots to tasks by current position, equipment, and capability (robots self-report equipment via "WhoHoldingType").
4. Node tasks the selected robots to move to their assigned roads -> begin reconnaissance.
5. During execution, node continuously re-checks assignment efficiency -> reassigns a task if a robot is slowed by obstacles.
6. Robots report: imagery/video via "ResourceType" (URL + geographic reference); sensor measurements via "WhoMeasuredType" (value, UOM, phenomenon, sensor, time, place).
7. Node aggregates low-level task-status reports -> emits a status report for the original high-level task to the C2 system.

**Environment and constraints:** Outdoor reconnaissance over a road network;
BML/CBML message exchange between C2, planning node, and robots. Execution
context: field/experimental multi-robot system (also usable in C2-to-simulation).
Rules of engagement: Not applicable (reconnaissance). Constraint: high-level orders
are capability-agnostic; the node must know robot equipment/capabilities to
disaggregate and assign.

#### Conceptual model (ontology seed)
- **Domain and scope:** C2-level tasking and reporting for a multi-robot system via BML, with human-level orders disaggregated to robot tasks.
- **Concepts (classes):** Operator, Control/planning node, Multi-robot system, Robot, High-level task, Low-level task, Task assignment, Status report, Resource (media) report, Measurement report, Equipment report.
- **Taxonomy (IS-A):**
  - Autonomous system -> Robot (UGV/UAV)
  - Task -> High-level task, Low-level task (move, observe, image, measure)
  - Report -> Status report, Resource report, Measurement report, Equipment report
- **Relationships (triples):**
  - Operator | issues | High-level task
  - Planning node | disaggregates | High-level task into Low-level tasks
  - Planning node | assigns | Low-level task to Robot
  - Planning node | reassigns | task when Robot slowed
  - Robot | reports | Resource (media URL + geo)
  - Robot | reports | Measurement (value, UOM, phenomenon)
  - Robot | reports | mounted Equipment
  - Planning node | aggregates | Low-level reports into High-level status
- **Properties:**
  - Robot: position, mounted equipment/capability (self-reported)
  - Measurement report: value, unit of measure, phenomenon, sensor, time, place
  - Resource report: media URL, geographic reference / bounding box
  - Task assignment: efficiency, follow/road assignment
- **Constraints/rules:**
  - Disaggregation depends on number of robots, their equipment/capabilities, and scenario specifics.
  - Assignment is re-evaluated continuously and changed if inefficient.
  - Capability must be known (self-reported) before a robot can be assigned a task.

**Grounding check:** One MoP item [inferred]; ROE "Not applicable". All other
fields grounded in source (including the three report structures from Listings 1-3).
