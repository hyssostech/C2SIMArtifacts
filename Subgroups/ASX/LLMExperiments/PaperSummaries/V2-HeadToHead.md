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

- The extraction here was performed by the assistant reasoning over retrieved
  text, which is the intended use but is a single run; production use should
  still sample multiple runs per paper, as the V1 methodology did.

---

## Case 3: Prompt-isolation control (same model, two prompts)

The Case 1/2 comparison changed two variables at once - prompt (V1 -> V2.1) AND
model (`gpt-4-turbo-preview` -> Opus). This control removes the confound: BOTH
prompts are run by the SAME model (Opus) over the SAME source text, so any
difference is attributable to the prompt alone.

Source: Biagini, Corona, Casar (2017), "Operational Scenario Modelling Supporting
Unmanned Autonomous Systems Concept Development" (MESAS 2017), local copy
`References/OperationalScenarioModelling2017_Casar-Biagini-Corona.pdf`. Chosen
because it is discussion-heavy (DSEEP process, UAAV size/application taxonomies,
Level-of-Autonomy theory) with the scenario as a minor part - the structure that
induces the V1 goal-leak - and it contains TWO distinct scenario variants, which
also tests multi-scenario handling. Text used: Sections 2.4-2.5 (Operational and
Conceptual Scenario Development).

### V1 prompt, run on Opus (steelmanned)

> **Summary Narrative:** The paper develops an air operational scenario in
> "Archaria", a hypothetical 2035 megacity, addressing defense of critical
> infrastructure and crowded civilian sites against hostile swarms of Unmanned
> Autonomous Aerial Vehicles (UAAVs) operated by terrorist groups. Two variants
> are presented - an attack on a shopping center and a coordinated multi-swarm
> attack on a chemical plant - the latter countered by a static autonomous
> defense system using kinetic and non-kinetic countermeasures under human
> authorization.
>
> **Specific Goals:**
> - Find the best method(s) of defense against a swarm of hostile UAAVs.
> - Classify UAAV capabilities and vulnerabilities in order to exploit weaknesses.
> - Develop reusable, modifiable scenarios for future UAxS capability development.
> - Protect critical energy infrastructure and populated urban areas.
>
> **Measures of Performance:**
> - Detection effectiveness (visual / electromagnetic) at ranges of about 1500 m.
> - Success of kinetic / non-kinetic countermeasures against the swarm.
> - Minimization of collateral damage and loss of life.
> - Time to detect, identify, and engage targets.
>
> **Scenario Steps:**
> 1. A terrorist group launches UAAV swarm(s) toward the target.
> 2. Suicide UAAVs, protective UACAS, ISTAR reconnaissance, and missile-armed
>    multipurpose UAAVs advance along preprogrammed routes.
> 3. The static autonomous defense radar, in surveillance mode, detects the UAAVs.
> 4. The system identifies a target as hostile and detects its level of autonomy.
> 5. An appropriate kinetic or non-kinetic counter-action is proposed, weighing
>    collateral damage.
> 6. The responsible person authorizes fire; the weapon engages the target.
> 7. The system evaluates and reports results; the engagement terminates when all
>    targets are hit, the swarm completes its task, or the specified time elapses.
>
> **Conceptual Model:** Domain: defense of a future megacity against hostile
> autonomous aerial swarms. Concepts: UAAV, swarm, suicide UAAV, UACAS, ISTAR
> UAAV, static defense system, radar, countermeasure, level of autonomy, critical
> infrastructure. Hierarchy: UAAV subtypes (combat/UACAS, reconnaissance/ISTAR,
> multipurpose, special); defense system contains detection and weapon
> subsystems. Relationships: swarm attacks infrastructure; defense system detects
> and engages swarm; operator authorizes fire. Properties: UAAV size category,
> LoA, payload; defense system detection range. Constraints: final target
> elimination is not autonomous and requires human authorization.

Note the two defects the V1 prompt does not prevent, even on a strong model:
(1) **Goal leak** - the first three "Specific Goals" are the *authors' research /
simulation aims* ("find the best method of defense", "develop reusable
scenarios"), not the goals pursued inside the scenario. (2) **Two variants
collapsed** into one loose record; the shopping-center and chemical-plant
missions have different forces and objectives but are merged. Also: no grounding
marks, LoA values (1/3/6) not surfaced, execution context absent, prose ontology.

### V2.1 prompt, run on Opus (same text)

V2.1 correctly emits TWO records (distinct missions per the same-mission-variation
rule) and separates Purpose from in-world objectives. Shown in full for the more
complex variant; the first is condensed for space but is a full record.

> ### Scenario 1: Terrorist micro/mini-UAAV attack on a shopping center
> **Domain / mission type:** urban / air; offensive UAAV strike on a civilian soft target.
> **Purpose (why the authors present it):** A scenario variant built to exercise
> the simulation and drive counter-UAxS capability development. (Research intent.)
> **Summary narrative:** In the Archaria 2035 megacity, an organized terrorist
> group employs a small number of micro-to-mini UAAVs against a multi-floor
> shopping center with a single restricted supply road. [...] operating at LoA 1,
> 3, or 6 depending on mission phase.
> **In-world objectives:** Inflict mass casualties and panic on a crowded soft
> target using expendable UAAVs.
> **Autonomous systems employed:** 1-3 fragmentation-armed UAAVs (UAV, expendable);
> 1-2 multipurpose UAAVs with aerosol/chemical payload (UAV); 1 multipurpose UAAV
> with precision incendiary payload (UAV). Level of autonomy: LoA 1/3/6 by phase.
> **Measures of Performance:** [inferred] casualties produced and panic/secondary
> effects achieved (the text frames effect, not a metric).
> **Scenario steps:** 1. Attacker guides 1-3 fragmentation UAAVs through the
> hypermarket roof -> detonate before ground impact -> mass primary casualties.
> 2. 1-2 multipurpose UAAVs disperse aerosol/poison inside or around the building
> -> panic and secondary casualties. 3. 1 precision-incendiary UAAV strikes an
> adjacent gas station -> fire blocks the emergency escape road -> domino effect.
> **Environment and constraints:** Dense multi-floor shopping center, single supply
> road; assumed ideal weather; peacetime/growing-crisis posture. Execution context:
> constructive/virtual (HLA RTI DSE under development). Rules of engagement:
> Not applicable (adversary vignette).
> #### Conceptual model (ontology seed)
> - Concepts: Terrorist group, UAAV (micro/mini), Fragmentation payload, Aerosol
>   payload, Incendiary payload, Soft target, Level of Autonomy.
> - Taxonomy (IS-A): Autonomous system -> UAV; UAV -> Micro UAAV, Mini UAAV.
> - Relationships (triples): Terrorist group | employs | UAAV; UAAV | strikes |
>   Shopping center; UAAV | carries | Payload.
> - Properties: UAAV: size class, payload type, LoA (1/3/6).
> - Constraints/rules: UAAVs are micro/mini (buyable, car-portable); operate at LoA 1/3/6 by phase.
> **Grounding check:** MoP is [inferred]; ROE Not applicable. Others grounded.
>
> ### Scenario 2: Autonomous static-defense engagement of a multi-swarm chemical-plant attack
> **Domain / mission type:** urban / air; counter-UAS / critical-infrastructure protection (with the paired attack).
> **Source location:** Section 2.5.1, "Example of 2nd Scenario Variant"; Fig. 2.
> **Purpose (why the authors present it):** To model the hardest defensive case -
> a cooperative multi-swarm attack - so the DSE can evaluate detection and
> kinetic/non-kinetic countermeasures. (Research/demo intent.)
> **Summary narrative:** Three enemy UAAV swarms of five vehicles each attack a
> chemical plant near an airport in the Archaria megacity. Within each swarm, three
> vehicles are suicide UAAVs (precision-guided bombs), two are fully autonomous
> UACAS escorts protecting the suicides; the force also includes an ISTAR UAAV for
> target acquisition and two missile-armed multipurpose UAAVs tasked to block
> escape roads and amplify panic. A static autonomous defense system with visual
> and electromagnetic detection, radar in surveillance mode, detects the swarms,
> identifies hostiles, detects their level of autonomy, and proposes a kinetic or
> non-kinetic countermeasure weighing collateral damage; final target elimination
> requires a human fire order.
> **In-world objectives:**
> - (Red) Destroy/disable the chemical plant and block escape routes to maximize casualties.
> - (Blue) Detect, identify, and neutralize the hostile swarms while minimizing collateral damage.
> **Autonomous systems employed:**
> - Suicide UAAV (UAV), 3 per swarm - precision-guided-bomb role. LoA: [inferred] high (autonomous terminal guidance).
> - UACAS escort (UAV), 2 per swarm - "fully autonomous", protect the suicide UAAVs.
> - ISTAR UAAV (UAV) - target acquisition and information gathering.
> - Multipurpose UAAV (UAV), 2 - missile-armed; block roads.
> - Static autonomous defense system - detection (visual + electromagnetic + radar) and weapon; human-authorized fire.
> **Measures of Performance:**
> - Whether fire is successful and hits all targets vs. the swarm fulfilling its task (stated termination conditions).
> - [inferred] Collateral damage / loss of life incurred by the chosen countermeasure.
> - [inferred] Detection timeline against the ~1500 m counter-UAxS engagement range.
> **Scenario steps:**
> 1. Three 5-vehicle UAAV swarms launch along preprogrammed routes toward the chemical plant.
> 2. Within each swarm, UACAS escorts protect the suicide UAAVs; ISTAR UAAV acquires targets; multipurpose UAAVs move to block escape roads.
> 3. Static defense radar (surveillance mode) detects UAAVs via visual/electromagnetic means -> activates weapon system.
> 4. System continues detection -> identifies target as hostile -> detects its level of autonomy.
> 5. System proposes an appropriate kinetic or non-kinetic counter-action, weighing collateral damage.
> 6. Responsible person issues a fire command -> weapon launches directed energy at the enemy (final elimination is NOT autonomous).
> 7. Defense system evaluates and reports results to the operator for consecutive action.
> 8. Terminate when fire hits all targets, or the swarm completes its task, or the specified time elapses.
> **Environment and constraints:** Chemical plant near an airport, >100,000 people
> within 1.5 km; assumed ideal weather; peacetime/growing-crisis. Execution context:
> constructive/virtual (HLA RTI DSE, interoperable with real C2). Constraint:
> final kinetic engagement requires human authorization; counter-UAxS detect/engage
> range ~1500 m; GPS-denied considerations noted.
> #### Conceptual model (ontology seed)
> - Concepts: UAAV swarm, Suicide UAAV, UACAS, ISTAR UAAV, Multipurpose UAAV,
>   Static autonomous defense system, Radar, Kinetic countermeasure, Non-kinetic
>   countermeasure, Level of Autonomy, Fire authority, Critical infrastructure.
> - Taxonomy (IS-A): Autonomous system -> UAV; UAV -> Suicide UAAV, UACAS, ISTAR
>   UAAV, Multipurpose UAAV; Countermeasure -> Kinetic, Non-kinetic.
> - Relationships (triples): Swarm | attacks | Chemical plant; UACAS | protects |
>   Suicide UAAV; Defense system | detects | Swarm; Defense system | proposes |
>   Countermeasure; Operator | authorizes | Fire command; Defense system | reports |
>   results to Operator.
> - Properties: Swarm: size (5), count (3); Suicide UAAV: precision guidance;
>   Defense system: detection modes (visual, electromagnetic, radar), range (~1500 m);
>   Countermeasure: type (kinetic/non-kinetic), collateral-damage weighting.
> - Constraints/rules: Final target elimination is not autonomous (human fire
>   order required); countermeasure selection considers level of autonomy and
>   collateral damage.
> **Grounding check:** Two MoP items and two LoA values are [inferred]; all other
> fields grounded in source.

### What the prompt alone changed (model held constant)

| Dimension | V1 on Opus | V2.1 on Opus |
| --- | --- | --- |
| Research goals in scenario goals | Yes (leak persists) | No - moved to Purpose |
| Two variants | Merged into one record | Split into two records |
| LoA values (1/3/6) | Dropped | Captured as properties |
| Inference vs fact | Unmarked | [inferred] / Not applicable marked |
| Execution context | Absent | Constructive/virtual (HLA RTI) |
| Ontology form | Prose | IS-A + subject|relation|object triples |

Because the model is identical in both columns, these differences isolate the
prompt's contribution. The goal-leak - the defect the library documented - is
NOT fixed by model strength alone (V1-on-Opus still leaks); it is fixed by the
V2 structure (the "what counts" definition, the Purpose/in-world split, and the
internal discard step). This closes the attribution gap flagged after Cases 1-2.

### Remaining
- The full corpus (MSG-145, Remmersmann BML, ASX overview, ethics/RAS) is present
  under References/ for broader extraction once the prompt is locked.

---

## Case 4: Langerwisch 2013 (schema-drift case)

The V1 output for this paper ([Langerwisch_et_al2013.md](./Langerwisch_et_al2013.md))
is the documented schema-drift case: it used "Objectives" instead of "Specific
Goals", introduced a/b/c/d sub-lettering, and gave each of the two scenarios
(MOVE, OBSERVE) an ad hoc internal structure different from every other summary
in the library. This run checks whether V2.1 holds one uniform schema across a
two-scenario paper. Source: local `References/Heterogeneous Teams ... A Field
Experiment_2013.pdf`, Sections V-VI. The two tasks (MOVE, OBSERVE) have different
objectives and are emitted as two records (OBSERVE reuses MOVE as an approach
phase but is a distinct mission).

> ### Scenario 1: Coordinated formation MOVE of a heterogeneous UGV/UAV team
> **Domain / mission type:** land (off-road field); coordinated relocation / convoy movement.
> **Source location:** Sec. V.A "Scenarios" (MOVE), Sec. VI.B "MOVE Scenario".
> **Purpose (why the authors present it):** To demonstrate the ROS/BML-over-3G
> interfaces and autonomous coordinated movement of an arbitrary-size heterogeneous
> team. (Research/demo intent.)
> **Summary narrative:** An operator sets a destination; the team moves there in a
> coordinated fashion. By design the UAVs take a constant formation escorting the
> leading ground vehicle while the leading UGV (HANNA) follows a pre-known road
> network and the remaining UGVs convoy one by one. A central planner on the
> leading vehicle computes each vehicle's follow-target and following distance. In
> the reported field run the four-UGV team reached the destination in convoy;
> the UAVs were not part of that particular MOVE test.
> **In-world objectives:** Relocate the whole multi-robot team to a specified destination in coordinated escort/convoy formation.
> **Autonomous systems employed:**
> - Lead UGV HANNA (UGV; Kawasaki Mule 3010) - hosts the central planner; follows road network.
> - UGV LONGCROSS (UGV, wheeled), UGV GARM (UGV, tracked) - convoy followers.
> - UGV AMOR (UGV; Yamaha quad) - convoy follower.
> - UAV PSYCHE 1000 x2 (UAV; MD4-1000 quadrocopter) - escort formation by design; absent in the MOVE run.
> - Autonomy: autonomous navigation; each vehicle self-responsible for following exactly one vehicle.
> **Measures of Performance:**
> - Successful arrival of the UGV team at the destination in convoy formation (stated).
> - [inferred] Formation/convoy maintenance and real-time position reporting over ROS/BML/3G.
> **Scenario steps:**
> 1. Operator sets a destination point on the GUI map.
> 2. Task transmitted to lead UGV HANNA -> initializes task distribution and planners.
> 3. Central planner computes a convoy order (follow-target + following distance) -> submits to active vehicles.
> 4. (By design) UAVs form a constant escort formation around the lead UGV via decentral coordination.
> 5. Lead UGV approaches the destination on the pre-known road network; other UGVs convoy one by one.
> 6. UGV team reaches the destination in convoy formation.
> **Environment and constraints:** Field camp with gravel roads, fences, buildings,
> and obstacles; OSM road network available; comms ROS/BML over 3G mobile radio
> (200+ ms RTT deemed negligible). Execution context: field-experiment (live).
> Rules of engagement: Not applicable. As-designed vs as-run: MOVE design includes
> a UAV escort formation, but the reported MOVE test used UGVs only.
> #### Conceptual model (ontology seed)
> - Concepts: Multi-robot team, Lead UGV, Follower UGV, Escort UAV, Central planner, Convoy order, Road network, Destination.
> - Taxonomy (IS-A): Autonomous system -> UGV, UAV; UGV -> Lead UGV, Follower UGV.
> - Relationships (triples): Central planner | assigns | Convoy order; Follower UGV | follows | Lead UGV; Escort UAV | escorts | Lead UGV; Lead UGV | traverses | Road network.
> - Properties: Lead UGV: hosts planner, road-constrained; Follower UGV: follow-target, following distance; Escort UAV: formation shape (depends on active UAV count).
> - Constraints/rules: Lead UGV stays on the pre-known road network; each vehicle follows exactly one vehicle; planner adapts to the number of active vehicles.
> **Grounding check:** MoP item 2 [inferred]; ROE Not applicable; as-run deviation
> from design noted. Others grounded.
>
> ### Scenario 2: OBSERVE - autonomous POI surveillance and moving-object detection
> **Domain / mission type:** land + air; point-of-interest observation / reconnaissance-surveillance.
> **Source location:** Sec. V.A (OBSERVE), Sec. VI.C "OBSERVE Scenario".
> **Purpose (why the authors present it):** To show autonomous reconnaissance and
> surveillance of a POI by a heterogeneous ground/air team. (Research/demo intent.)
> **Summary narrative:** An operator marks a point of interest (a switch box on a
> lamp post) in the GUI aerial image; the team of four UGVs and two UAVs approaches
> the POI as in the MOVE scenario. On arrival the UGVs distribute evenly around the
> POI with sensors focused on it, one UAV holds position directly above the POI
> with its camera pointed down, and the remaining UAVs orbit the POI with cameras
> fixed on it. The team performs continuous moving-object detection; pedestrians
> and an unknown vehicle entering the area are detected and tagged, the operator is
> alarmed and can request imagery (e.g. an aerial photo from the overhead UAV).
> **In-world objectives:** Observe an operator-designated POI and autonomously
> detect and tag moving objects (pedestrians, vehicles) around it; alert the operator.
> **Autonomous systems employed:** Same team as Scenario 1. Roles: UGVs distribute
> around the POI with focused sensors (Velodyne HDL-64E); one UAV overhead
> (downward 14.7 MP zoom camera); other UAVs orbit with cameras on the POI.
> **Measures of Performance:**
> - Vehicles autonomously take their assigned observation positions (stated).
> - Successful detection and classification of moving objects - pedestrians and an unknown vehicle (stated).
> - Operator alerted and able to request pictures (stated).
> **Scenario steps:**
> 1. Operator marks the POI in the GUI aerial image -> team task transmitted.
> 2. Team approaches the POI (via the MOVE behavior).
> 3. At proximity, the planner computes observation poses on a circular path of predefined radius around the POI (optionally constrained to the road network).
> 4. UGVs distribute evenly around the POI with sensors focused; one UAV positions directly above (camera down); other UAVs orbit with cameras on the POI.
> 5. Team performs continuous moving-object detection.
> 6. Moving objects detected and tagged (pedestrian = cross icon, vehicle = circle icon) in the GUI.
> 7. Operator is alarmed -> requests pictures -> overhead UAV supplies an aerial image.
> **Environment and constraints:** Same field camp; POI = switch box on a lamp
> post; comms ROS/BML/3G. Execution context: field-experiment (live). Rules of
> engagement: Not applicable (observation task).
> #### Conceptual model (ontology seed)
> - Concepts: Multi-robot team, UGV, UAV, Point of interest (POI), Observation pose, Moving-object detection, Pedestrian, Vehicle, Operator alert.
> - Taxonomy (IS-A): Autonomous system -> UGV, UAV; Detected object -> Pedestrian, Vehicle.
> - Relationships (triples): Operator | designates | POI; UGV | observes | POI; UAV | observes | POI; Team | detects | Moving object; Team | alerts | Operator.
> - Properties: POI: position; Observation pose: circular radius, orientation-to-POI; UAV: overhead vs orbiting role; Detected object: type (pedestrian/vehicle).
> - Constraints/rules: One UAV directly overhead, remaining UAVs orbit; observation poses may be constrained to road segments; detection runs continuously.
> **Grounding check:** All fields grounded in source.

### What Case 4 showed

- **Schema drift fixed.** Both scenarios use the identical field set and ordering
  as every other V2 record - no "Objectives"-vs-"Goals" rename, no a/b/c/d
  lettering. Uniformity is now enforced by the template, not left to the model.
- **Two-scenario split** handled cleanly; OBSERVE reuses MOVE as a phase without
  being merged into it.
- **A new, real gap surfaced:** the source distinguishes the MOVE *design* (UAV
  escort) from the MOVE *as-run* (UGVs only). A careful v2.1 run catches this via
  the grounding rules, but nothing in the prompt *mandates* separating designed
  behavior from what was actually executed - and field-experiment papers
  (Langerwisch, SubT, Brutzman) routinely differ on exactly this. This motivates
  prompt refinement (F), added as v2.2: explicitly require distinguishing intended
  behavior from the reported run.

### Status after Case 4
- Prompt advanced to **v2.2** (refinement F). No other gaps surfaced across four
  papers spanning combat/urban, subterranean SAR, counter-UAS, and field
  reconnaissance - the schema is holding.
