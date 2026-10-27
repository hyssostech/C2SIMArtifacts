# Scenario extracted from report (v2.2 prompt)

Rosenberg, C. (2024). Commercial sUAS in Support of Targeting. Infantry, Summer 2024,
pp. 29-31. Source read in full (article text). Local copy (full issue):
[../../References/InfantryMagazine-Summer2024-issue71417.pdf](../../References/InfantryMagazine-Summer2024-issue71417.pdf)

Source note: this is a professional-forum lessons-learned article. Unlike most library
records it is written from the RED / opposing-force (OPFOR) perspective and reports a
REAL event (a live force-on-force combat-training-center rotation), not a notional or
technical-report scenario. The unmanned systems are low-autonomy commercial
off-the-shelf (COTS) quadcopters and fixed-wing craft used as remotely piloted
observers that cue indirect fires - a reconnaissance-strike cycle, not autonomous
strike. This record was split out from the SME-directed drone-warfare update
([LIRC_MovementToContact_Updated2024.md](./LIRC_MovementToContact_Updated2024.md)),
where the same source is also used as a threat/TTP input, to give the library its first
standalone OPFOR targeting scenario.

### Scenario 1: OPFOR commercial-sUAS reconnaissance-strike targeting at JPMRC-AK 24-02

**Domain / mission type:** land; reconnaissance-strike / targeting (find - validate -
cue fires - observe/BDA) from the RED/OPFOR perspective, using COTS small UAS as the
sensor that cues indirect fires against high-payoff targets. Reciprocal counter-UAS /
survivability lessons are captured for the receiving (BLUE) side.

**Source location:** Whole article (pp. 29-31): the JPMRC-AK Rotation 24-02 OPFOR
narrative, the battalion targeting-board description, the numbered survivability
observations, and the closing force-design recommendation.

**Purpose (why the author presents it):** A lessons-learned argument that COTS sUAS
are a serious targeting threat U.S. units are neither equipped nor trained to counter;
the author uses his battalion's OPFOR experience to recommend squad-level anti-drone
equipment and a dedicated battalion sUAS section. (Advocacy/lessons-learned intent -
distinct from the in-world objective.)

**Summary narrative:** During Joint Pacific Multinational Readiness Center - Alaska
(JPMRC-AK) Rotation 24-02, 3rd Battalion, 509th Parachute Infantry Regiment acted as
the opposing force and was augmented with commercially available quadcopters and
fixed-wing systems (DJI Phantom 4 Pro, TSTORM, Mavic Air 2). The battalion integrated
these drones into its collection matrix and its targeting cycle: intelligence, cyber,
operations, and fires teams merged their collection and fires-synchronization matrices
into a single product and ran a battalion-level targeting board off the high-value and
high-payoff target lists for each battle period. COTS sUAS were cued onto suspected
targets by higher (echelons-above-brigade) collection assets, flew to validate and pull
a 10-digit grid, passed it through the S2 to the fires cell, and then loitered on
station as the observer to render immediate battle-damage assessment and adjust fire off
the live feed. The result was the destruction of dozens of high-payoff targets -
including the rotational unit's brigade tactical operations center, brigade support
area, Role 2 medical, artillery batteries, and counter-battery radars - and, the author
reports, at least one of everything on the high-value-target list. The article then
records the receiving unit's survivability failures and the countermeasures it adopted
once it recognized that sUAS overhead were a precursor to indirect fire.

**In-world objectives:**
- (OPFOR) Locate the rotational unit's high-value and high-payoff targets and destroy
  them by cueing indirect fires from COTS sUAS observation.
- Sustain observation on each target through the strike to confirm battle damage and
  adjust fire.
- Demonstrate the operational value of COTS sUAS targeting so the lesson transfers to
  training and force design.

**Autonomous systems employed:**
- DJI Phantom 4 Pro (UAV, COTS quadcopter, Group 1) - remotely piloted; reconnaissance,
  target validation/grid, on-station observation and BDA.
- Mavic Air 2 (UAV, COTS quadcopter, Group 1) - remotely piloted; same reconnaissance/
  observer role.
- TSTORM (UAV, COTS fixed-wing) - remotely piloted; reconnaissance/observation
  (longer-range/endurance than the quadcopters). [inferred] role split by platform type.
- Level of autonomy: LOW - human-operated COTS drones used as sensors/observers in the
  targeting cycle, not for autonomous or onboard-weapon engagement. Fires are delivered
  by conventional indirect-fire systems that the drones cue and adjust.

**Measures of Performance:**
- Dozens of high-payoff targets destroyed via drone-cued fires.
- "At least one of everything on our HVT list" destroyed during the rotation.
- Specific target sets defeated: brigade TOC, BSA, Role 2, artillery batteries,
  counter-battery radars.
- [inferred] Targeting-cycle timeliness: drone-on-station enabled immediate BDA and
  adjust-fire (the article states the capability; it gives no clock time).
- Reciprocal (BLUE) MoP implied by the narrative: time from "sUAS overhead" to
  reaction - initially poor (the rotational unit rarely destroyed sUAS in the first 96
  hours). [inferred] as a metric; stated qualitatively.

**Scenario steps:**
1. Battalion (OPFOR) staff builds the HVT and HPT lists for the battle period -> merges
   the collection and fires-synchronization matrices into one product -> convenes a
   battalion targeting board with warfighting-function leads to predict target
   locations.
2. Higher (EAB) collection assets cue a COTS sUAS onto a suspected target.
3. COTS sUAS flies to the location -> validates the target and pulls a 10-digit grid.
4. Drone operator relays the grid to the S2 -> S2 pushes it to the fires cell.
5. Fires cell engages the target with indirect fire while the drone remains on station
   as the observer.
6. Drone observes impact -> renders immediate BDA -> adjusts fire off the live feed and
   re-engages as needed.
7. (Reciprocal, BLUE) Once the rotational unit recognizes that sUAS overhead precede
   indirect fire, it begins to space vehicles, seek overhead cover, and employ Drone
   Buster / kinetic means against the drones.

**Environment and constraints:** JPMRC-AK Rotation 24-02, Alaska; a live force-on-force
combat-training-center rotation (subarctic/restrictive terrain [inferred]). Execution
context: field-experiment / live force-on-force training - real drones and real maneuver
with fires and kills adjudicated by exercise control (not live ordnance). The threat
modeled is COTS sUAS available on the open market; the receiving unit was largely
untrained against it (rarely destroyed sUAS in the first 96 hours). Rules of engagement:
training/exercise rules (not applicable as live-fire ROE). Force-design context: the
RQ-7 Shadow and RQ-11 Raven are sunsetting, opening a brigade capability gap; the author
recommends fielding DoD-approved COTS "Blue List" drones and standing up a sUAS section/
platoon (reconnaissance + kinetic) in each maneuver battalion's headquarters company.
Counter-targeting TTPs observed (BLUE survivability): tie camouflage to the natural
terrain (not just a net); make frequent survivability moves (displace roughly every 24 h);
operate decentralized and dispersed (avoid massing vehicles/soldiers, especially in the
BSA and rear); train against sUAS routinely; and equip every squad with drone detection
(Bal Chatri 2 class) and kinetic defeat (Drone Buster, Smart Shooter SMASH 2000L class).

#### Conceptual model (ontology seed)
- **Domain and scope:** OPFOR reconnaissance-strike targeting with low-autonomy COTS
  small UAS cueing indirect fires against high-payoff targets, plus the reciprocal
  counter-UAS survivability behavior of the targeted force.
- **Concepts (classes):** OPFOR battalion, COTS quadcopter, COTS fixed-wing UAS, Drone
  operator, Collection matrix, Fires-synchronization matrix, Targeting board, HVT/HPT
  list, 10-digit grid, S2 (intelligence cell), Fires cell, Indirect-fire system, Target
  (TOC, BSA, Role 2, artillery, counter-battery radar), Battle-damage assessment,
  Counter-UAS system, Survivability move.
- **Taxonomy (IS-A):**
  - Autonomous system -> UAV
  - UAV -> COTS quadcopter
  - UAV -> COTS fixed-wing UAS
  - Target -> Command post (TOC)
  - Target -> Sustainment node (BSA, Role 2)
  - Target -> Fires asset (artillery battery)
  - Target -> Sensor (counter-battery radar)
  - Counter-UAS system -> Detection system
  - Counter-UAS system -> Kinetic-defeat system
- **Relationships (triples):**
  - EAB collection asset | cues | COTS sUAS
  - COTS sUAS | validates | Target
  - COTS sUAS | pulls | 10-digit grid
  - Drone operator | relays | Grid to S2
  - S2 | pushes | Target to Fires cell
  - Fires cell | engages | Target with indirect fire
  - COTS sUAS | observes | Battle damage
  - COTS sUAS | adjusts | Indirect fire
  - Targeting board | prioritizes | HPT list
  - Counter-UAS system | defeats | COTS sUAS
  - Survivability move | reduces targetability of | Target
- **Properties:**
  - COTS sUAS: type (quadcopter/fixed-wing), commercial model, remotely piloted,
    on-station observation, range/endurance (varies by model)
  - Target: type, signature (physical + electromagnetic), massed vs dispersed, overhead
    cover, camouflage-terrain fit
  - Targeting cycle: cue -> validate -> grid -> fire -> BDA -> adjust; observer stays on
    station
  - Counter-UAS system: function (detect vs defeat), man-packable, kinetic vs electronic
- **Constraints/rules:**
  - A drone-cued strike needs a validated 10-digit grid and an on-station observer for
    BDA/adjust.
  - Massed or open vehicles/soldiers (esp. logistics/BSA) are easy COTS-sUAS targets;
    disperse, seek overhead cover, and tie camouflage to terrain.
  - Displace frequently (about every 24 h) to limit detection; adapt if the command post
    cannot break down/set up that fast.
  - Every squad needs organic drone detection and kinetic defeat; without it a unit
    cannot react to the sUAS threat.

**Grounding check:** Items [inferred] - the TSTORM-vs-quadcopter role split, targeting-
cycle timeliness treated as an MoP (stated as a capability, not a measured time), the
reciprocal "reaction time" metric (stated qualitatively), and the subarctic/restrictive
terrain characterization. All platforms, target sets, the targeting-cycle steps, the
survivability TTPs, and the counter-UAS equipment are grounded in the source. Execution
context is live force-on-force training (CTC rotation). Rules of engagement: "Not
applicable" as live-fire ROE (exercise-adjudicated).
