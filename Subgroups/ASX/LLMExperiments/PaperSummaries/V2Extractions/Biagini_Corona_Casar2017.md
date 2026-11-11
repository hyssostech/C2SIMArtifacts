# Scenario extracted from paper (v2.2 prompt)

Biagini, M., Corona, F., & Casar, J. (2017). Operational Scenario Modelling
Supporting Unmanned Autonomous Systems Concept Development. International Workshop
on Modelling and Simulation for Autonomous Systems (MESAS 2017). Source read in
full (local References PDF).

Standalone v2.2 record for a library paper. This is the discussion-heavy
counter-UAxS benchmark; the V1-vs-V2 prompt-isolation control for this paper (both
prompts run on the same model) is in [../V2-HeadToHead.md](../V2-HeadToHead.md)
Case 3. The paper presents two distinct scenario variants, emitted as two records.

### Scenario 1: Terrorist micro/mini-UAAV attack on a shopping center

**Domain / mission type:** urban / air; offensive UAAV strike on a civilian soft target.

**Source location:** Section 2.5.1, "Example of 1st Scenario Variant".

**Purpose (why the authors present it):** A scenario variant built to exercise the
simulation and drive counter-UAxS capability development. (Research intent.)

**Summary narrative:** In the Archaria 2035 megacity, an organized terrorist group
employs a small number of micro-to-mini UAAVs against a large multi-floor shopping
center (three or more floors, hypermarkets, shops, and restaurants, with a gas
station a few meters away and a single restricted supply road plus customer
driveways). The attack uses the minimal number of UAAVs to accomplish the mission:
1-3 fragmentation-armed UAAVs guided through the delicate roof to detonate before
reaching the ground (mass primary casualties and panic); 1-2 multipurpose UAAVs
dispersing a poisonous substance or aerosol inside or around the building
(secondary casualties from panic and chaos); and one precision-guided incendiary
UAAV against the adjacent gas station, whose fire and destruction blocks the
emergency escape road and triggers a domino effect. The UAAVs operate at Level of
Autonomy 1, 3, or 6 depending on the mission phase.

**In-world objectives:** Inflict mass casualties and panic on a crowded soft target using expendable UAAVs.

**Autonomous systems employed:**
- 1-3 fragmentation-armed UAAVs (UAV, expendable) - roof strike.
- 1-2 multipurpose UAAVs with aerosol/chemical payload (UAV).
- 1 multipurpose UAAV with precision incendiary payload (UAV) - gas-station strike.
- Level of autonomy: LoA 1/3/6 by mission phase.

**Measures of Performance:** [inferred] casualties produced and panic/secondary effects achieved (the text frames effect, not a metric).

**Scenario steps:**
1. Attacker guides 1-3 fragmentation UAAVs through the hypermarket roof -> detonate before ground impact -> mass primary casualties.
2. 1-2 multipurpose UAAVs disperse aerosol/poison inside or around the building -> panic and secondary casualties.
3. 1 precision-incendiary UAAV strikes an adjacent gas station -> fire blocks the emergency escape road -> domino effect.

**Environment and constraints:** Dense multi-floor shopping center, single supply
road; assumed ideal weather; peacetime/growing-crisis posture. Execution context:
constructive/virtual (HLA RTI Distributed Simulation Environment under
development). Rules of engagement: Not applicable (adversary vignette).

#### Conceptual model (ontology seed)
- **Concepts (classes):** Terrorist group, UAAV (micro/mini), Fragmentation payload, Aerosol payload, Incendiary payload, Soft target, Level of Autonomy.
- **Taxonomy (IS-A):** Autonomous system -> UAV; UAV -> Micro UAAV, Mini UAAV.
- **Relationships (triples):** Terrorist group | employs | UAAV; UAAV | strikes | Shopping center; UAAV | carries | Payload.
- **Properties:** UAAV: size class, payload type, LoA (1/3/6).
- **Constraints/rules:** UAAVs are micro/mini (buyable, car-portable); operate at LoA 1/3/6 by phase.

**Grounding check:** MoP is [inferred]; ROE Not applicable. Others grounded.

---

### Scenario 2: Autonomous static-defense engagement of a multi-swarm chemical-plant attack

**Domain / mission type:** urban / air; counter-UAS / critical-infrastructure protection (with the paired attack).

**Source location:** Section 2.5.1, "Example of 2nd Scenario Variant"; Fig. 2.

**Purpose (why the authors present it):** To model the hardest defensive case - a
cooperative multi-swarm attack - so the DSE can evaluate detection and
kinetic/non-kinetic countermeasures. (Research/demo intent.)

**Summary narrative:** Three enemy UAAV swarms of five vehicles each attack a
chemical plant near an airport in the Archaria megacity. Within each swarm, three
vehicles are suicide UAAVs (precision-guided bombs), two are fully autonomous
UACAS escorts protecting the suicides; the force also includes an ISTAR UAAV for
target acquisition and two missile-armed multipurpose UAAVs tasked to block escape
roads and amplify panic. A static autonomous defense system with visual and
electromagnetic detection, radar in surveillance mode, detects the swarms,
identifies hostiles, detects their level of autonomy, and proposes a kinetic or
non-kinetic countermeasure weighing collateral damage; final target elimination
requires a human fire order.

**In-world objectives:**
- (Red) Destroy/disable the chemical plant and block escape routes to maximize casualties.
- (Blue) Detect, identify, and neutralize the hostile swarms while minimizing collateral damage.

**Autonomous systems employed:**
- Suicide UAAV (UAV), 3 per swarm - precision-guided-bomb role. LoA: [inferred] high (autonomous terminal guidance).
- UACAS escort (UAV), 2 per swarm - "fully autonomous", protect the suicide UAAVs.
- ISTAR UAAV (UAV) - target acquisition and information gathering.
- Multipurpose UAAV (UAV), 2 - missile-armed; block roads.
- Static autonomous defense system - detection (visual + electromagnetic + radar) and weapon; human-authorized fire.

**Measures of Performance:**
- Whether fire is successful and hits all targets vs. the swarm fulfilling its task (stated termination conditions).
- [inferred] Collateral damage / loss of life incurred by the chosen countermeasure.
- [inferred] Detection timeline against the ~1500 m counter-UAxS engagement range.

**Scenario steps:**
1. Three 5-vehicle UAAV swarms launch along preprogrammed routes toward the chemical plant.
2. Within each swarm, UACAS escorts protect the suicide UAAVs; ISTAR UAAV acquires targets; multipurpose UAAVs move to block escape roads.
3. Static defense radar (surveillance mode) detects UAAVs via visual/electromagnetic means -> activates weapon system.
4. System continues detection -> identifies target as hostile -> detects its level of autonomy.
5. System proposes an appropriate kinetic or non-kinetic counter-action, weighing collateral damage.
6. Responsible person issues a fire command -> weapon launches directed energy at the enemy (final elimination is NOT autonomous).
7. Defense system evaluates and reports results to the operator for consecutive action.
8. Terminate when fire hits all targets, or the swarm completes its task, or the specified time elapses.

**Environment and constraints:** Chemical plant near an airport, >100,000 people
within 1.5 km; assumed ideal weather; peacetime/growing-crisis. Execution context:
constructive/virtual (HLA RTI DSE, interoperable with real C2). Constraint: final
kinetic engagement requires human authorization; counter-UAxS detect/engage range
~1500 m; GPS-denied considerations noted.

#### Conceptual model (ontology seed)
- **Concepts (classes):** UAAV swarm, Suicide UAAV, UACAS, ISTAR UAAV, Multipurpose UAAV, Static autonomous defense system, Radar, Kinetic countermeasure, Non-kinetic countermeasure, Level of Autonomy, Fire authority, Critical infrastructure.
- **Taxonomy (IS-A):** Autonomous system -> UAV; UAV -> Suicide UAAV, UACAS, ISTAR UAAV, Multipurpose UAAV; Countermeasure -> Kinetic, Non-kinetic.
- **Relationships (triples):** Swarm | attacks | Chemical plant; UACAS | protects | Suicide UAAV; Defense system | detects | Swarm; Defense system | proposes | Countermeasure; Operator | authorizes | Fire command; Defense system | reports | results to Operator.
- **Properties:** Swarm: size (5), count (3); Suicide UAAV: precision guidance; Defense system: detection modes (visual, electromagnetic, radar), range (~1500 m); Countermeasure: type (kinetic/non-kinetic), collateral-damage weighting.
- **Constraints/rules:** Final target elimination is not autonomous (human fire order required); countermeasure selection considers level of autonomy and collateral damage.

**Grounding check:** Two MoP items and two LoA values are [inferred]; all other fields grounded in source.
