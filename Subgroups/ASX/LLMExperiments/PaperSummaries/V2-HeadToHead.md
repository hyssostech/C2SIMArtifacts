# V2 Prompt Head-to-Head and Iteration Evidence

This document records the test that drove the V1 -> V2 prompt revision (see
[PromptV2.md](./PromptV2.md)). It shows the new prompt run against real source
text, compared to the original V1 output already in the library.

## Method

- The extraction prompt was executed by a current frontier reasoning model
  (Claude Opus 4.x), the class of model V2 targets - not by `gpt-4-turbo-preview`.
- To make the test fair (not circular), the model was fed the ACTUAL source text
  of each paper, retrieved fresh, NOT the existing V1 summary in this folder.
- Two papers were used:
  1. Brutzman & Fitzpatrick 2020 (NPS-MV-20-001, DTIC AD1127315). Chosen because
     it is the documented V1 failure case: its existing summary notes that the
     extracted goals "are broader concerns of the paper, rather than the
     scenario". Open access; full text retrieved.
  2. Roucek et al. 2019, DARPA Subterranean Challenge (MESAS 2019). Chosen as a
     DIFFERENT domain (subterranean search-and-rescue, no adversary, live
     robotics) to check that the prompt generalizes and is not overfit to
     Brutzman. Open access; full text retrieved.
- Source access note: Corona & Biagini 2019 (Springer) and Langerwisch 2013
  (IEEE) are paywalled and could not be retrieved in full for this pass; they
  remain open follow-ups.

---

## Case 1: Brutzman & Fitzpatrick 2020

### What V1 got wrong (from the existing summary)

- **Goal leak.** V1's "Specific Goals" were the authors' research aims -
  "Illustrate Time of Day Effects", "Explore Player Perspectives", "Analyze
  Sensor Responses" - not the goals the force pursues in the scenario.
- **Vague steps.** V1's steps were "Deployment and Setup" and "Scenario
  Variations a-d" - presentation variants, not an operational sequence.
- **Missed the tactical passage.** V1 keyed only on the "Exemplar Mission" box
  (Section E) and never used the later passage that actually describes the
  movement-to-contact and fire coordination.

### V2 (v2.1) extraction

Source text used (verbatim excerpts): Section E "Exemplar Mission Design and
Portrayal" (p. 21-22) and the MCWL visualization subsection (p. 33-34).

> ### Scenario 1: Kilo 2 village/urban MUM-T ISR and movement to contact
>
> **Domain / mission type:** urban (land); ISR + movement-to-contact / fire coordination.
>
> **Source location:** Section E "Exemplar Mission Design and Portrayal"
> (p. 21-22, Figures 2-5); MCWL visualization subsection (p. 33-34).
>
> **Purpose (why the authors present it):** A simple exemplar to demonstrate
> virtual-environment and agent-based assessment of Manned-Unmanned Teaming
> (MUM-T), and to show that portraying one situation multiple ways yields
> comparative insight. (Research/demo intent - not the in-world objective.)
>
> **Summary narrative:** On the Kilo 2 range at Camp Pendleton, CA, a
> platoon-sized blue force (Marines) teamed with unmanned systems defends a small
> village model against a fire-team-sized hostile red force. The red force is
> emplaced on the northwest corner with small arms and rifles, without supporting
> arms or ISR. The blue force, on the east side, is assigned a single UAS and two
> UGVs for ISR. The unmanned systems conduct initial reconnaissance to establish
> situational awareness; the blue platoon then conducts a movement to contact to
> the northwest, using real-time UAS and UGV feeds of red-force disposition to
> plan and coordinate air, naval, and ground fires against the red force. The
> mission is portrayed in four variations (day/night x UAS/UGV viewpoint,
> including a night version with flare illumination in which the UGVs engage).
>
> **In-world objectives:**
> - Establish situational awareness of red-force disposition using UAS and UGV ISR.
> - Conduct movement to contact and engage the red force.
> - Plan and coordinate air, naval, and ground fires using real-time robotic intelligence.
>
> **Autonomous systems employed:**
> - Single UAS (UAV) - aerial ISR/overwatch; entity-viewpoint video feed of red disposition. Level of autonomy: Not specified in source.
> - Two UGVs (UGV) - forward ground ISR; video feed; in the fourth variation, engage the red force. Level of autonomy: Not specified in source.
>
> **Measures of Performance:**
> - Number of red and blue kills.
> - Comparative insight across the four portrayals (time-of-day and viewpoint effects).
> - [inferred] Timeliness/quality of situational awareness and fire coordination enabled by the robotic feeds.
>
> **Scenario steps:**
> 1. Red fire-team emplaces on the NW corner with small arms; no ISR, no supporting arms.
> 2. Blue platoon positions on the east side; assigned 1 UAS and 2 UGVs for ISR.
> 3. UAS and UGVs conduct initial reconnaissance of the area -> establish situational awareness.
> 4. UAS and UGVs generate entity-viewpoint video -> provide actual red-force disposition data.
> 5. Blue platoon conducts movement to contact to the northwest -> to engage the red force.
> 6. Blue force uses real-time robotic intelligence -> plans and coordinates air, naval, and ground fires -> initially engages red force.
> 7. Red and blue entities search, acquire, target, and engage -> outcomes adjudicated from internal parametric data (open-loop run).
> 8. (Fourth variation, night) UGVs engage the red force under flare illumination.
>
> **Environment and constraints:** Urban/village terrain, Kilo 2 range, Camp
> Pendleton, CA. Execution context: virtual (VT MAK VR Forces, DIS protocol),
> agent-based, run open-loop to stay reactive to robotic surveillance.
> Same-mission variations: (1) day/UAS view, (2) day/UGV view, (3) night/UAS with
> illumination, (4) night/UAS with UGVs engaging. Constraint: red force fielded no
> robotic systems and could not target blue units - the authors note this would
> have changed the outcome.
>
> #### Conceptual model (ontology seed)
> - **Domain and scope:** Manned-unmanned teaming (MUM-T) in small-unit urban combat, assessed in a virtual environment.
> - **Concepts (classes):** Blue force (Marine platoon), Red force (hostile fire-team), UAS, UGV, ISR operation, Movement to contact, Fire coordination, Portrayal/viewpoint, Environmental condition.
> - **Taxonomy (IS-A):**
>   - Autonomous system -> UAS
>   - Autonomous system -> UGV
>   - Force -> Blue force
>   - Force -> Red force
>   - Operation -> ISR operation
>   - Operation -> Movement to contact
> - **Relationships (triples):**
>   - Blue force | employs | UAS
>   - Blue force | employs | UGV
>   - UAS | conducts | ISR operation
>   - UGV | conducts | ISR operation
>   - UAS | provides | red-force disposition data
>   - Blue force | conducts | Movement to contact
>   - Blue force | coordinates | air/naval/ground fires
>   - Blue force | engages | Red force
>   - UGV | engages | Red force (fourth variation)
> - **Properties:**
>   - Blue force: size (platoon), position (east), assets (1 UAS, 2 UGVs)
>   - Red force: size (fire-team), position (NW corner), armament (small arms/rifles), ISR (none), supporting arms (none)
>   - UAS: role (ISR), viewpoint (aerial)
>   - UGV: role (ISR/engage), count (2)
>   - Environmental condition: time of day (day/night), illumination (flares)
> - **Constraints/rules:**
>   - Red force deployed no robotic systems and could not target blue units.
>   - Simulation run open-loop to remain reactive to robotic surveillance.
>   - Engagement outcomes adjudicated from internal parametric data.
>
> **Grounding check:** MoP item 3 is [inferred]; levels of autonomy "Not
> specified in source". All other fields grounded in source.

### What improved, concretely

1. **Goal leak fixed.** "Time-of-day effects" and "player perspectives" now sit
   correctly in Purpose and Environment; the In-world objectives are the force's
   actual aims (SA, movement to contact, fire coordination).
2. **Concrete temporal steps** replacing V1's "Deployment / Variations a-d",
   drawn from the tactical passage V1 ignored.
3. **Merge, not split.** The four portrayals are recorded once as variations
   (rule A), rather than as four scenarios.
4. **Grounding visible.** LoA marked "Not specified"; one MoP marked [inferred].
5. **Execution context = virtual** captured explicitly - absent from V1.

---

## Case 2: DARPA SubT (generality check, different domain)

Run to confirm the prompt is not overfit to a combat/virtual paper. Source text
used: Abstract, Section 3 (Contest Environment, Artifacts and Scoring), Section 4
(Robots).

> ### Scenario 1: Heterogeneous multi-robot subterranean artifact search
>
> **Domain / mission type:** subterranean; autonomous exploration / search-and-rescue (artifact detection and report).
>
> **Source location:** Abstract; Section 3.1 Contest Environment; 3.2 Artifacts and Scoring; Section 4 Robots.
>
> **Purpose (why the authors present it):** To describe and evaluate the CTU-CRAS
> team's heterogeneous multi-robot exploration system entered in the DARPA
> Subterranean Challenge, and share lessons learned. (Research/demo intent.)
>
> **Summary narrative:** A heterogeneous team of unmanned robots is deployed into
> a GPS-denied, radio-limited underground environment (a mine for the Tunnel
> round) to autonomously explore, detect and localize specified artifacts
> (backpacks, fire extinguishers, drills, human survivors, cell phones), and
> report each artifact's type and position to a DARPA-provided interface, then
> return to the control station. Because communication is intermittent, the wheeled
> robot deploys communication relays to maintain a low-bandwidth link to the
> control station. The mission recurs across four rounds (Tunnel, Urban, Cave, and
> a combined final) with different environments and artifact sets.
>
> **In-world objectives:**
> - Autonomously explore the underground environment without GPS.
> - Detect and localize specified artifacts within the allowed error bound.
> - Report artifact type and position to the control station and return.
>
> **Autonomous systems employed:**
> - Wheeled UGV, Husky A200 (x1) - fast traversal; carries and deploys communication relays. Autonomous (comms-denied operation required).
> - Tracked UGV, Absolem (x2) - difficult-terrain search of areas the Husky cannot reach. Autonomous.
> - Legged UGV, PhantomX hexapod (x2) - narrow/constrained-passage traversal. Autonomous (approx. 1 h endurance).
> - Quadrotor UAV (x2) - terrain-independent access; short endurance, reduced sensor payload. Autonomous.
>
> **Measures of Performance:**
> - Points for each artifact reported with correct type and position within the DARPA error bound.
> - Score decremented for false-positive detection or mislocalization.
>
> **Scenario steps:**
> 1. Team deploys at the environment entrance -> begins autonomous exploration (no GPS).
> 2. Ground and aerial robots distribute by capability -> tracked/legged robots take difficult or constrained terrain, wheeled robot takes faster open runs, UAVs take terrain-independent access.
> 3. Husky deploys communication relays -> maintains low-bandwidth link to control station.
> 4. Robots run onboard SLAM/mapping and object detection -> detect artifacts.
> 5. Robot sends message (artifact type + position) to DARPA interface -> scoring.
> 6. Robots return to the control station to report.
>
> **Environment and constraints:** Underground - mine (Tunnel), parking
> lot/subway (Urban), natural caverns (Cave); little or no GPS, very limited
> radio, fog/smoke/mud/water/reflective surfaces. Execution context:
> field-experiment (live robots), with a preceding integration exercise (STIX).
> Rules of engagement: Not applicable (no adversary). Same-mission variations: the
> four competition rounds. Time limit per run.
>
> #### Conceptual model (ontology seed)
> - **Domain and scope:** Autonomous heterogeneous multi-robot exploration and artifact reporting in GPS-denied underground environments.
> - **Concepts (classes):** Robot team, Wheeled UGV, Tracked UGV, Legged UGV, Quadrotor UAV, Artifact, Control station, Communication relay, Environment round, Score.
> - **Taxonomy (IS-A):**
>   - Autonomous system -> UGV
>   - Autonomous system -> UAV
>   - UGV -> Wheeled UGV
>   - UGV -> Tracked UGV
>   - UGV -> Legged UGV
>   - UAV -> Quadrotor UAV
> - **Relationships (triples):**
>   - Robot team | explores | Environment round
>   - Robot | detects | Artifact
>   - Robot | reports | Artifact position
>   - Wheeled UGV | deploys | Communication relay
>   - Communication relay | links | Robot team | to | Control station
>   - Score | increases_with | correct Artifact report
>   - Score | decreases_with | false positive
> - **Properties:**
>   - Wheeled UGV (Husky A200): speed (<=3 m/s), payload (<=50 kg), sensors (3D lidar, 5 RGB cameras), carries relays
>   - Tracked UGV (Absolem): flippers, pivoting lidar, difficult-terrain role
>   - Legged UGV (hexapod): speed (~0.2 m/s), endurance (~1 h), constrained-passage role
>   - Quadrotor UAV: terrain-independent, short endurance, reduced payload
>   - Artifact: type, position, error bound
> - **Constraints/rules:**
>   - No GPS and limited radio -> robots must operate autonomously.
>   - A report scores only if type is correct and position is within the error bound.
>   - False positives and mislocalizations reduce the score.
>
> **Grounding check:** Rules of engagement "Not applicable" (no adversary). All
> other fields grounded in source.

### What the generality check confirmed / added

- Confirmed rule **(A)**: the four SubT rounds are correctly one scenario, not four.
- Confirmed **(B)**: execution context here is field-experiment/live, contrasting
  cleanly with Brutzman's virtual - the field earns its place.
- Motivated **(D)**: "rules of engagement: Not applicable" is correct for a SAR
  mission; forcing "Not specified" would be misleading.
- No new defects surfaced. The template held for a non-combat, multi-platform,
  scoring-based mission with no human-in-the-loop confirmation step.

---

## Conclusion

Across a combat/virtual paper and a SAR/live paper, V2.1 fixed the documented V1
failure (goal leak), produced concrete grounded steps, correctly handled
same-mission variation, and emitted an ontology-ready conceptual model. The
refinements (A)-(E) are folded into [PromptV2.md](./PromptV2.md) v2.1.

### Residual limitations / assumptions

- Only two of the library's papers were exercised; both open access. Corona &
  Biagini (the primary V1 benchmark) and Langerwisch (the schema-drift case)
  are paywalled and were not re-run - the strongest remaining test of the goal
  fix and schema enforcement is still pending on those two.
- The extraction here was performed by the assistant reasoning over retrieved
  text, which is the intended use but is a single run; production use should
  still sample multiple runs per paper, as the V1 methodology did.
