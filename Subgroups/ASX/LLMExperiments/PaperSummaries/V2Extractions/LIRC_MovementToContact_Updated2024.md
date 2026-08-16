# Scenario enhancement (v2.2 template) - threat and TTP update of the Morris 2018 baseline

This record is an ANALYST-UPDATED DERIVATIVE of the baseline extraction
[LIRC_MovementToContact_Morris2018.md](./LIRC_MovementToContact_Morris2018.md).
It keeps the baseline mission skeleton (a Light Infantry-Robotic Company movement to
contact to secure a foothold in Columbus) and revises the THREAT laydown and the
FRIENDLY equipment/TTP to reflect small-drone warfare as observed 2022-2024. It was
produced at the SME's direction: "The scenario is an excellent start, but needs
updating" - for the threat, and for U.S. doctrine/equipment/TTP.

Grounding contract for this derivative:
- The mission skeleton, forces, phase lines, and end-state come from Morris 2018
  (baseline record).
- Every real-world system, statistic, and doctrinal point in the update is grounded
  in one of the four SME-provided sources below and tagged inline as [W], [R], [HE],
  or [P].
- The APPLICATION of those facts to the notional Columbus vignette is analyst
  projection and is tagged [inferred]. This is not a source extraction; it is an
  evidence-driven variation, so it does not claim Morris's vignette actually contained
  these systems.

## Update basis (SME-provided sources)

All four are in the Infantry Magazine issues saved under
[../../References/](../../References/):
[Summer 2023](../../References/InfantryMagazine-Summer2023-issue66993.pdf) and
[Summer 2024](../../References/InfantryMagazine-Summer2024-issue71417.pdf).

- **[W]** Wilkins, D. (2023). The 2022 Russo-Ukrainian War: Current and Future
  Employment of Unmanned Platforms Supporting Infantry Operations. Infantry, Summer
  2023, pp. 46-48. (THREAT update.)
- **[R]** Rosenberg, C. (2024). Commercial sUAS in Support of Targeting. Infantry,
  Summer 2024, pp. 29-31. (THREAT + friendly-TTP update; JPMRC-AK 24-02 OPFOR
  vignette.)
- **[HE]** Hamilton, M. A. & Egan, C. J. (2023). Improving the Tactical Employment of
  SUAS for Light Infantry Battalions in Decisive Action. Infantry, Summer 2023,
  pp. 23-30. (Doctrine/equipment/TTP update.)
- **[P]** Padalino, A. R. (2024). The Army Needs to Quickly Adapt to Tactical Drone
  Warfare. Infantry, Summer 2024, pp. 32-37. (Doctrine/equipment/organization update.)

### Scenario 1 (updated): LIRC movement to contact to secure a foothold in Columbus, in a contested small-drone environment

**Domain / mission type:** land, with an urban objective; movement to contact executed
as a clearing attack from PL LD to PL LOA. Added dimensions vs baseline: pervasive
small-UAS ISR-strike threat, dense electronic warfare / GPS denial, and organic
counter-UAS. Human-machine teaming at company scale.

**Source location:** Mission skeleton from Morris 2018 (pp. 23-27). Threat and TTP
deltas from [W], [R], [HE], [P] as tagged below.

**Purpose (why it is presented):** To carry the SME-endorsed baseline forward into the
2022-2024 threat environment so the C2SIM ASX ontology captures the platform classes,
relationships, and constraints that the small-drone revolution introduced and that the
2018 concept predates. (Concept-update intent - not an in-world goal.)

**Summary narrative:** The mission is unchanged from the baseline: during a crisis an
enemy force seizes Columbus, and a Light Infantry-Robotic Company deploys within 72
hours to the Fryar Drop Zone and attacks from PL LD to PL LOA to secure a foothold and
protect the airhead. What changes is the drone environment on both sides. The enemy is
no longer only a conventional armor/mechanized/light-infantry force; it now fields a
layered small-UAS ecosystem - recon/targeting quadcopters and fixed-wing UAS
(Orlan-10-, Zala-, Forpost-class) [W], first-person-view (FPV) attack drones under
$400 that kill armored vehicles worth millions (Lancet, Pegasus class) [P], loitering
munitions and Shahed/Geran-class one-way attack drones credited with destroying
self-propelled howitzers [W][P], a fiber-optic-controlled kamikaze UGV carrying an
antitank mine [W], and breaching/demining UGVs [W] - screened
by dense electronic warfare: GPS jammers, tactical jammers with roughly 1.6 mi reach,
and a system that can identify a drone, break its control link, and hijack it in about
25 seconds [W]. In this environment the LIRC's own unmanned systems face severe
attrition (in Ukraine a drone's average life is about seven days and only about 10
percent complete their mission, with GPS jamming causing most losses) [W], and the
LIRC's dispersed command posts, mortar UGVs, logistics UGVs, and CASEVAC UGVs are
themselves high-payoff targets for adversary COTS-sUAS-cued indirect fires [R]. The
updated LIRC therefore adds organic counter-UAS at squad level [R], dedicated
battalion/company SUAS with the range, endurance, and short-take-off-and-landing and
line-of-sight-comms resilience that restrictive terrain demands [HE], jam-resistant
(inertial-navigation, encrypted frequency-hopping, fiber-optic) links and munitions
[W], multi-frequency sensor fusion to defeat decoys [W], and disciplined survivability
behavior (frequent displacement, dispersion, terrain-tied camouflage, overhead cover)
[R].

**In-world objectives:** (baseline objectives retained) plus:
- Preserve friendly unmanned systems and command posts against adversary small-UAS
  ISR-strike and electronic attack (survive to accomplish the clearing attack). [inferred from R, W]
- Deny the adversary's reconnaissance-strike cycle: detect, defeat, or spoof enemy
  small UAS before they cue fires onto LIRC assets. [inferred from R]
- Continue to discriminate military from civilian targets when both sides saturate the
  area with small UAS and decoys. [inferred from W]

**Autonomous systems employed (updated set):**
- Baseline LIRC systems retained (ISR UAS, quadcopters, autonomous attack UAS, mortar/
  heavy-weapons/armed-combat/equipment-carrying/command/CASEVAC UGVs) - see baseline
  record.
- Re-classed under current taxonomy [P]: the baseline "autonomous attack UAS
  (Switchblade-class)" is a MINI loitering munition (man-packable; e.g. Switchblade 300,
  WARMATE class). Add TACTICAL loitering munitions (vehicle/rail launched, ISTAR +
  strike; Hero-120, Skystriker, Orbiter 1K class) and, at brigade, LONG-RANGE LMs
  (Harpy/Harop class).
- Added: modified-COTS quadcopters (group 1-2) for reconnaissance and munitions drop
  [R][P], and FPV attack drones (group 1-2, payload >=1.2 kg, expendable, antiarmor)
  [P] pushed down to squad/platoon.
- Added: dedicated battalion/company SUAS section [R][HE] - man-portable,
  extended-range/endurance (10-12 km range, 90-120 min endurance, STOL, resilient LOS
  comms) [HE], distinct from the man-packable short-range squad systems.
- Added (friendly counter-UAS): man-packable drone DETECTION (Bal Chatri 2-class) and
  KINETIC/defeat systems (Drone Buster-class jammer, Smart Shooter SMASH 2000L-class
  fire-control) at squad level [R]; the baseline UGV-mounted air-defense missiles are
  retained for larger air platforms but are no longer the sole counter-air layer.
- Adversary systems now modeled as scenario actors (see Environment): recon/targeting
  UAS, FPV drones, loitering munitions, one-way attack UAS, kamikaze UGV, demining/
  breaching UGV, and EW/counter-UAS trucks [W][P].
- Level of autonomy: baseline weapons-control-status and kill-box scheme retained;
  added constraint that GPS-denied conditions force inertial/terrain-relative
  autonomous navigation and raise the human-confirmation burden when links drop [W].

**Measures of Performance (updated):**
- Baseline MoP retained (soldier-load reduction; ~20 km indirect / ~3 km direct / ~10
  km air-defense ranges; BDA counts; CASEVAC capacity).
- Friendly-UAS survivability now an explicit MoP [inferred from W]: expected attrition
  and mission-completion rate under EW/GPS jamming (baseline assumed ~50% attrition to
  countermeasures; [W] reports ~7-day average drone life and ~10% mission completion in
  Ukraine - treat the baseline 50% as optimistic for GPS-dependent platforms).
- Counter-UAS effectiveness [inferred from R]: fraction of adversary small UAS detected
  and defeated before they cue effective fires; time from "enemy drone overhead" to
  friendly reaction (at JPMRC the rotational unit initially failed to react until it
  learned that sUAS overhead preceded indirect fire).
- Cost-exchange ratio [inferred from P]: value destroyed per friendly munition, given
  sub-$400 FPV drones defeating armor worth millions - a metric the 2018 baseline did
  not consider.
- Survivability-move discipline [inferred from R]: displacement frequency of command
  posts / logistics nodes (target: displace on the order of every 24 h; disperse; tie
  camouflage to terrain; use overhead cover).

**Scenario steps (updated; baseline numbering preserved, deltas marked):**
1-5. As baseline (prep, dispersed approach march, ford, ISR saturation) WITH: the LIRC
   assumes GPS is contested and its ISR/attack UAS rely on inertial navigation and
   encrypted frequency-hopping links; launch/recovery of the dedicated battalion SUAS
   is planned around scarce short-take-off-and-landing sites in restrictive terrain,
   accepting greater standoff between launch sites and named areas of interest. [W][HE][inferred]
6. (New, folds into baseline step 5-6) Squad counter-UAS teams screen the march and the
   assembly/objective areas -> detect and defeat adversary recon/FPV drones before they
   cue fires; command posts and logistics/CASEVAC UGVs displace frequently, disperse,
   and use terrain-tied camouflage and overhead cover to defeat COTS-sUAS targeting. [R][inferred]
7-8. As baseline (arrive RP, disperse across PL LD, disruption phase, weapons hold ->
   tight) WITH multi-frequency sensor fusion added to the attack-UAS targeting chain so
   thermal/shape recognition is not defeated by decoys. [W][inferred]
9. As baseline (line platoons + mortar section release attack UAS) WITH the strike
   package now a mix of mini loitering munitions, FPV drones, and modified-COTS drop
   drones; FPV/LM engage the enemy's armor and air-defense/EW vehicles, and priority is
   given to the adversary's jammer trucks and counter-UAS systems because they threaten
   the entire friendly UAS fight. [P][W][inferred]
10-12. As baseline (mortar fires, first-strike BDA, second strike) WITH BDA now
   explicitly tracking friendly-UAS attrition and jammer-attributed losses. [W][inferred]
13-18. As baseline (kill-box handover, western assault by armed UGVs + infantry,
   disable kill boxes, cross PL Bravo, consolidate on PL LOA) WITH squad counter-UAS
   protecting the assaulting infantry and the consolidation/CASEVAC from adversary FPV
   and loitering-munition attack, and logistics/CASEVAC UGVs moving under counter-UAS
   overwatch. [R][W][inferred]

**Environment and constraints (updated):**
- Adversary UAS/UGV/EW laydown [W][P]: recon/targeting UAS (Orlan-10, Zala-421-08,
  Forpost, Eleron, Granat class); one-way attackers (Shahed-136/Geran-2 class - credited
  with destroying self-propelled howitzers and armored vehicles); loitering munitions
  (mini: Switchblade 300/WARMATE class; tactical: Hero-120/Skystriker/Orbiter 1K class;
  long-range: Harpy/Harop class); FPV attack drones (<$400, antiarmor; Lancet/Pegasus
  class per [P]); kamikaze UGV (Temerland GNOM
  class - TM-62 antitank mine, ~2 km fiber-optic control, jam-immune); demining/breaching
  UGVs (Uran-6, Prokhod-1 class). Note [W]: a heavy combat UGV (Uran-9 class) performed
  poorly in Syria - a realism check on the baseline's UGV-heavy assault concept.
- Adversary electronic warfare / counter-UAS [W]: GPS jammers (R-30Zh Zhitel class,
  Pishchal handheld); tactical jammer trucks (Repellent-1 class, ~1.6 mi); a
  drone-hijacking system (Shipovnik-Aero class) that identifies a UAV, cuts its control
  link, and can assume control in about 25 s; cell-site-simulator/EW drone (Leer-3 class).
- Friendly-UAS operating limits in restrictive terrain [HE]: limited launch/recovery
  sites, degraded surface winds, reduced line-of-sight comms, and the need for direct
  overflight to identify ground targets drive requirements for STOL, extended range
  (10-12 km), extended endurance (90-120 min), and resilient LOS comms; legacy RQ-11
  Raven / RQ-20 Puma / Black Hornet do not meet battalion needs, and RQ-7 Shadow / RQ-11
  Raven are sunsetting [R].
- Attrition/comms reality [W]: expect heavy UAS losses and low mission-completion under
  GPS jamming; mitigate with inertial navigation, encrypted frequency-hopping and
  fiber-optic links, quieter platforms, and inexpensive attributable drones used in mass.
- Cost-exchange [P]: sub-$400 FPV drones defeat armor worth millions; a light infantry
  squad with FPV/LM can halt an armored company - the LIRC's expensive armed/heavy UGVs
  must be weighed against cheap expendable strike drones.
- Retained baseline constraints: civilians present near the enemy main line of defense;
  weapons-control-status and civilian-clear kill-box rules; ford and ~25 km approach
  march. Execution context: constructive / notional concept (an evidence-updated
  projection, still not a live/virtual/field run).

#### Conceptual model (ontology seed - delta over the baseline)
New or refined classes the update introduces (baseline classes still apply):
- **Concepts (classes):** FPV attack drone, Loitering munition (Mini / Tactical /
  Long-range), Modified-COTS drone, One-way attack UAS, Kamikaze UGV, Demining/breaching
  UGV, Counter-UAS system (Detection / Kinetic-defeat), Electronic-warfare system
  (GPS jammer / Control-link jammer / Drone-hijack system), Dedicated SUAS section,
  Survivability move, Named area of interest, Reconnaissance-strike cycle.
- **Taxonomy (IS-A):**
  - UAV -> FPV attack drone
  - UAV -> Loitering munition
  - Loitering munition -> Mini LM
  - Loitering munition -> Tactical LM
  - Loitering munition -> Long-range LM
  - UAV -> Modified-COTS drone
  - UAV -> One-way attack UAS
  - UGV -> Kamikaze UGV
  - UGV -> Demining/breaching UGV
  - Counter-UAS system -> Detection system
  - Counter-UAS system -> Kinetic-defeat system
  - Electronic-warfare system -> GPS jammer
  - Electronic-warfare system -> Control-link jammer
  - Electronic-warfare system -> Drone-hijack system
- **Relationships (triples):**
  - Enemy recon UAS | cues | Indirect fire onto Friendly high-payoff target
  - Counter-UAS detection system | detects | Enemy small UAS
  - Counter-UAS kinetic-defeat system | defeats | Enemy small UAS
  - GPS jammer | denies navigation to | Friendly UAS
  - Control-link jammer | severs | UAS control link
  - Drone-hijack system | assumes control of | UAS
  - FPV attack drone | destroys | Armored vehicle
  - Mini loitering munition | strikes | Enemy vehicle
  - Kamikaze UGV | delivers | Antitank mine
  - Survivability move | reduces targetability of | Command post
  - Sensor fusion | discriminates | Real target from Decoy
  - Inertial navigation | sustains | UAS navigation under GPS jamming
- **Properties:**
  - Loitering munition: tier (mini/tactical/long-range), man-packable vs vehicle-launched,
    ISTAR-capable, recoverable, payload
  - FPV attack drone: unit cost (<$400), payload (>=1.2 kg), expendable, human-piloted
  - Counter-UAS system: function (detect vs defeat), man-packable, kinetic vs electronic
  - EW system: effect (navigation-deny / link-sever / hijack), range, reaction time (~25 s
    for hijack)
  - Friendly UAS: navigation mode (GPS vs inertial), link type (encrypted FH / fiber-optic),
    expected life (~7 d), mission-completion rate (~10%)
  - Command post / logistics node: displacement interval, dispersion, camouflage-terrain fit,
    overhead cover
- **Constraints/rules:**
  - Assume GPS-denied: UAS must navigate inertially/terrain-relative and tolerate link loss. [W]
  - Every squad requires organic counter-UAS (detection + defeat). [R]
  - Command posts and logistics/CASEVAC nodes must displace frequently, disperse, tie
    camouflage to terrain, and use overhead cover (they are high-payoff sUAS targets). [R]
  - Strike-UAS targeting must use multi-frequency sensor fusion to avoid decoys. [W]
  - Prioritize adversary jammer and counter-UAS systems as targets (they threaten the whole
    friendly UAS fight). [inferred from W]
  - Battalion-level SUAS must meet 10-12 km range / 90-120 min endurance / STOL / resilient
    LOS comms to be usable in restrictive terrain. [HE]

**Change log vs the Morris 2018 baseline (what "updating" changed):**
- THREAT: added a full adversary small-UAS/LM/FPV/kamikaze-UGV/EW-counter-UAS ecosystem
  [W][P] where the baseline enemy was conventional armor/mech/light-infantry only.
- THREAT: replaced the baseline's single "~50% attrition to countermeasures" figure with
  the harder GPS-jamming reality (short drone life, low mission completion) and made
  friendly-UAS survivability an explicit planning factor and MoP. [W]
- THREAT: recast the LIRC's dispersed HQ, mortar UGVs, and logistics/CASEVAC UGVs as
  adversary high-payoff targets requiring survivability moves, dispersion, camouflage,
  and overhead cover. [R]
- FRIENDLY EQUIPMENT: re-classed the baseline "autonomous attack UAS" as a mini loitering
  munition and added tactical/long-range LMs, modified-COTS drones, and FPV drones. [P]
- FRIENDLY EQUIPMENT: added a dedicated battalion/company SUAS section with the range/
  endurance/STOL/comms attributes restrictive terrain demands, distinct from
  short-range squad systems; noted the RQ-7/RQ-11 sunset and COTS-Blue-List bridge. [HE][R]
- FRIENDLY TTP: added organic squad counter-UAS (detection + kinetic defeat). [R]
- FRIENDLY TTP: added inertial navigation, encrypted frequency-hopping / fiber-optic links,
  quieter platforms, mass of cheap attributable drones, and multi-frequency sensor fusion. [W]
- ANALYTIC: surfaced the cost-exchange inversion (cheap FPV/LM vs expensive UGVs) as a
  design tension the 2018 concept did not weigh. [P]

**Grounding check:** All real-world systems, statistics, ranges, and doctrinal points are
grounded in the four cited sources and tagged [W]/[R]/[HE]/[P] inline. Every application of
those facts to the notional Columbus vignette is analyst projection and is tagged
[inferred]. The mission skeleton, forces, phase lines, and end-state are grounded in the
Morris 2018 baseline record. Execution context is constructive (an evidence-updated
projection, not a live/virtual/field run). No field is left unmarked as to whether it is
sourced fact or projection.
