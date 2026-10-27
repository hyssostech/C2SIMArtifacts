# Scenario extracted from report (v2.2 prompt)

Morris, Z. L. (2018). Developing a Light Infantry-Robotic Company as a System.
Military Review, July-August 2018, pp. 20-29. Source read in full (article PDF;
accessed 2026-07-17):
https://www.armyupress.army.mil/Journals/Military-Review/English-Edition-Archives/July-August-2018/Morris-Robotic/
Local copy: [../../References/Morris-2018-MilitaryReview-LightInfantryRoboticCompany.pdf](../../References/Morris-2018-MilitaryReview-LightInfantryRoboticCompany.pdf)

Source note: this is a concept-development article, not a technical report or field
experiment. Its scenario is an explicitly notional employment vignette the author
uses to illustrate a proposed unit design, so the execution context is constructive
(a concept, not a live or virtual run). The vignette is unusually detailed for this
document class - specific forces, phase lines, weapons-control transitions, and
battle-damage counts are stated - so few fields need "Not specified in source".

This is the SME-designated BASELINE scenario for the ASX drone-warfare update. The
threat and doctrine here are current as of 2018 (pre-2022 Russo-Ukrainian War); the
companion record
[LIRC_MovementToContact_Updated2024.md](./LIRC_MovementToContact_Updated2024.md)
revises the threat and the friendly TTP/equipment against four Infantry Magazine
sources (2023-2024) per the SME's guidance.

### Scenario 1: Light Infantry-Robotic Company movement to contact to secure a foothold in Columbus

**Domain / mission type:** land, with an urban objective (Columbus); movement to
contact (author's doctrinal frame), executed as a clearing attack from PL LD to PL LOA.
Sub-tasks: organic ISR, indirect and direct fires, short-range air defense, contested
logistics/resupply, and CASEVAC. Human-machine teaming (manned-unmanned) at company
scale.

**Source location:** Section "Light Infantry-Robotic Company Movement to Contact
Tactical Concept" (pp. 23-27), Figures 3-6. Unit organization from "The Future
Organization for a Light Infantry-Robotic Company" (pp. 21-23), Figures 1-2. Autonomy
policy from "Phase I and Phase II of Autonomous Weapons Development" (pp. 20-21).

**Purpose (why the authors present it):** To argue that the U.S. Army should develop
a Light Infantry-Robotic Company (LIRC) integrating controlled lethal autonomous
weapon systems (LAWS) with human capabilities, and to make that concept concrete. The
author explicitly labels the vignette "a notional employment of the LIRC to illustrate
a concept of employment." (Concept-development/advocacy intent - not an in-world goal.)

**Summary narrative:** During a crisis, an enemy force seizes Columbus, a small city
in allied "Baltenning," then repositions southward and consolidates around the city
for political leverage. A Light Infantry-Robotic Company - part of a rapidly deployable
infantry brigade - deploys within 72 hours to the Baltenning-held Fryar Drop Zone (FDZ). The LIRC (about 169 soldiers and roughly 25 unmanned ground vehicles, plus
unmanned aircraft) conducts a movement to contact from the line of departure (PL LD)
to the limit of advance (PL LOA) to secure a foothold in Columbus and protect the FDZ
for follow-on forces. The company fords the Chattahoochee River, completes a roughly
25 km approach march to a release point, saturates the objective with autonomous ISR
UAS, confirms civilian-free "kill boxes," then opens with autonomous attack UAS and
120 mm mortar-UGV fires against enemy armor, artillery, and air defense before armed
combat UGVs and dismounted infantry clear the enemy positions. The enemy is a
conventional mechanized/armor-plus-light-infantry force (T-72B3M tanks, BMP-3 IFVs,
self-propelled artillery, one air-defense vehicle); civilians are present near the
enemy main line of defense. About half the autonomous systems are lost to enemy
countermeasures over the fight, after which the company consolidates and establishes
a defensive line on PL LOA.

**In-world objectives:**
- Clear from PL LD to PL LOA to secure a foothold in Columbus.
- Protect the Fryar Drop Zone to enable arrival of follow-on units.
- Destroy/attrit the enemy armored, artillery, and air-defense assets while
  discriminating military targets from the civilians present on the battlefield.
- Reduce risk and physical load on the infantry by pushing sensing, firepower, and
  logistics onto unmanned systems.

**Autonomous systems employed:**
- ISR UAS (UAV; Puma-class per author's note) - autonomous independent recon routes,
  multi-target tracking, area-search programming; one operator can control several.
- Company quadcopter UAS (UAV) - larger company-level ISR/relay quadcopter.
- Squad quadcopter (UAV, small) - one per rifle squad; 360-degree local situational
  awareness around each platoon.
- Autonomous attack UAS (UAV, loitering munition; Switchblade-class per author) -
  antipersonnel/antiarmor/bunker-buster warheads, "fire and forget"; used from the
  three line platoons and the mortar section. Weapons-hold (human-in-the-loop) during
  movement; released against confirmed kill boxes / ISR-observed targets.
- 120 mm mortar UGV (UGV) - autonomous digital targeting and precision-guided
  munitions; two per company; ~20 km indirect-fire reach.
- Heavy-weapons UGV (UGV) - 30 mm cannon plus coaxial M240B, two Javelin-class
  antitank missiles, two Stinger-class air-defense missiles; four in the heavy-weapons
  platoon.
- Armed combat UGV (UGV) - M2/MK19/M240B plus two antitank and two air-defense
  missiles; CROWS-like stabilized accuracy; two per rifle-platoon weapons squad.
  Weapons-hold for antipersonnel fires (human operator commands "engage" or "move on").
- Equipment-carrying UGV (UGV) - carries 22 soldiers' equipment, food, water, fuel,
  ammunition (3-5 days); leader-follower autonomy behind a designated human.
- Command UGV (UGV) - blue-force tracking, radio/retrans/TACSAT, and local EW/jamming/
  direction-finding; used by HQ and the ISR team to manage video links.
- Casualty-evacuation UGV (UGV) - autonomous evacuation of four litter and two
  ambulatory casualties.
- Level of autonomy: governed by a weapons-control-status scheme (hold / tight / free)
  and by the author's "Phase II" ethical policy - fully autonomous engagement of human
  targets only inside a geographically and temporally bounded kill box confirmed clear
  of civilians; otherwise human-in-the-loop.

**Measures of Performance:**
- Soldier physical load reduced from 120-150 lb to about 50 lb (equipment-carrying
  UGVs).
- Effective ranges: indirect fire to ~20 km, direct fire to ~3 km, air defense to
  ~10 km.
- About 50 percent of autonomous systems lost to enemy countermeasures (active
  defenses, rapid movement, camouflage, decoy vehicles).
- Battle-damage progression stated in the vignette: first strike destroys 1 air-defense
  vehicle, 1 artillery piece, 2 IFVs (12 enemy casualties in kill box 1, 2 in kill box
  2); second strike destroys 1 MBT and the last artillery piece (+5 casualties); the
  UGV/infantry assault destroys 1 IFV and 1 MBT at a cost of 3 UGVs; 2 MBTs withdraw.
- CASEVAC capacity: 4 litter + 2 ambulatory, autonomously.
- [inferred] Overall mission success = foothold secured, FDZ protected, and a defensive
  line established on PL LOA (stated as the end-state reached, not as a scored metric).

**Scenario steps:**
1. Company completes preparation and information updates -> departs the assembly area
   (AA).
2. Company moves dispersed along the approach march route -> fords the Chattahoochee
   River -> passes Checkpoint 1 (CP1) -> reaches the release point (RP); equipment-
   carrying UGVs follow via leader-follower.
3. Squads fly quadcopters around each platoon -> provide 360-degree awareness; ground
   attack weapons set weapons-hold, air-defense weapons set weapons-tight (may engage
   enemy air within 10 km).
4. From AA to CP1 the company receives updates from higher; at CP1 (~15 km from the
   objective) -> the company becomes self-sufficient for ISR.
5. Autonomous ISR UAS saturate areas of interest -> pinpoint enemy positions from PL LD
   to PL Bravo; company ISR/mortar/fires assets scan deep targets between PL Bravo and
   PL LOA.
6. ISR team confirms zero civilians in kill boxes 1 and 2 -> commander establishes the
   kill boxes -> authorizes autonomous engagement of human targets inside them.
7. Company completes the ~25 km approach march, arrives at RP -> platoons disperse to
   assigned zones across PL LD.
8. Before crossing PL LD (disruption phase) autonomous weapons shift hold -> tight (may
   engage any enemy military vehicle in company boundaries; humans still in the loop for
   enemy personnel outside kill boxes).
9. Line platoons and mortar section fire multiple autonomous attack UAS -> strike kill
   boxes 1/2 and ISR-observed targets, prioritizing air-defense, indirect-fire, MBT, IFV,
   and APC targets; thermal/shape recognition discriminates military from civilian
   vehicles.
10. Mortar section simultaneously engages positions between PL Alpha and PL Bravo with
    precision-guided and conventional rounds.
11. ISR confirms first-strike BDA -> ~50 percent of autonomous systems are lost to
    countermeasures.
12. As the company crosses PL LD, a second autonomous-attack-UAS strike destroys 1 MBT
    and the last artillery piece.
13. Company conducts target handover to squad quadcopters -> XO confirms kill box 3
    civilian-free and establishes it -> autonomous attack UAS and 120 mm mortars destroy
    the enemy squad in kill box 3.
14. In the west, the company makes contact with the smallest element possible (often a
    single UGV); four armed UGVs enter kill box 1 to suppress/destroy remaining enemy
    personnel while one infantry platoon envelops.
15. Commander disables kill boxes 1 and 2 before friendly humans enter -> restricts
    autonomous engagement to enemy vehicles; UGVs scan sectors and a human commands each
    engagement (engage / move on).
16. Company crosses PL Bravo -> employs all systems to force enemy repositioning and open
    flanks; armed UGVs with infantry support engage the remaining MBTs/IFV with antitank
    missiles (3 UGVs lost; 1 IFV and 1 MBT destroyed; 2 MBTs withdraw into Columbus).
17. Company employs close-air support / close-combat attack as air-defense threat allows
    -> pursues and disrupts the withdrawing enemy.
18. Company consolidates -> moves up supply UGVs -> conducts CASEVAC -> establishes a
    defensive line along PL LOA.

**Environment and constraints:** Foreign setting ("Baltenning"; city of "Columbus"),
mixed rural-to-urban terrain, a fordable river (Chattahoochee), a ~25 km approach march;
civilians present, concentrated near the enemy main line of defense in the southern
outskirts of Columbus. [inferred] The place names (Columbus, Chattahoochee River, Fryar
Drop Zone) are Fort Benning training-area names reused for a notional overseas setting.
Enemy (conventional): two light-infantry platoons; an armor platoon of four T-72B3M MBTs;
a mechanized platoon of three BMP-3 IFVs; two self-propelled artillery vehicles; one
air-defense vehicle. Comms: available from higher until CP1, self-sufficient thereafter;
the broader concept assumes a future environment of constant maneuver, dispersion, and
degraded communications/networks (Milley). Weapons control: hold/tight/free statuses with
kill boxes as geographic-plus-temporal fire-control measures; autonomous engagement of
humans only inside confirmed civilian-free kill boxes; commander disables kill boxes
before friendly troops enter. Expected countermeasures: enemy active protection, rapid
movement, camouflage, decoy vehicles, and signal jamming / cyberattack (autonomous
fire-and-forget partly chosen to resist post-launch jamming). Execution context:
constructive / notional concept (not live, virtual, or field-experiment). Rules of
engagement: central to the scenario (target discrimination with civilians present).

#### Conceptual model (ontology seed)
- **Domain and scope:** Company-scale human-machine-teamed land offensive (movement to
  contact) employing lethal autonomous weapon systems under weapons-control-status and
  kill-box constraints, with organic ISR, fires, air defense, logistics, and CASEVAC.
- **Concepts (classes):** Light Infantry-Robotic Company, Rifle platoon, Weapons squad,
  Robotic section, Human operator, ISR UAS, Quadcopter UAS, Autonomous attack UAS, Mortar
  UGV, Heavy-weapons UGV, Armed combat UGV, Equipment-carrying UGV, Command UGV, CASEVAC
  UGV, Kill box, Phase line, Weapons-control status, Enemy vehicle, Civilian, MoP.
- **Taxonomy (IS-A):**
  - Autonomous system -> UAV
  - Autonomous system -> UGV
  - UAV -> ISR UAS
  - UAV -> Quadcopter UAS
  - UAV -> Autonomous attack UAS (loitering munition)
  - UGV -> Mortar UGV
  - UGV -> Heavy-weapons UGV
  - UGV -> Armed combat UGV
  - UGV -> Equipment-carrying UGV
  - UGV -> Command UGV
  - UGV -> CASEVAC UGV
- **Relationships (triples):**
  - Human operator | controls | Armed combat UGV
  - Equipment-carrying UGV | follows | Human operator (leader-follower)
  - ISR UAS | detects/tracks | Enemy vehicle
  - Command UGV | relays | ISR video to Command element
  - Autonomous attack UAS | engages | Enemy vehicle within Kill box
  - Commander | establishes/disables | Kill box
  - Weapons-control status | constrains | Autonomous engagement
  - CASEVAC UGV | evacuates | Casualty
  - Air-defense UGV | engages | Enemy air platform (weapons-tight, 10 km)
- **Properties:**
  - Autonomous attack UAS: warheads (AP/AT/bunker), fire-and-forget, weapons-control
    status, attrition-prone (~50%)
  - Mortar UGV: caliber (120 mm), PGM-capable, range (~20 km)
  - Armed/Heavy-weapons UGV: primary gun, antitank missiles (2), air-defense missiles (2),
    CROWS-like accuracy, direct-fire range (~3 km)
  - Equipment-carrying UGV: payload (22 soldiers' load, 3-5 days), leader-follower
  - Kill box: geographic bound, time bound, civilian-clearance state (confirmed/denied)
  - Weapons-control status: {hold, tight, free}
- **Constraints/rules:**
  - Autonomous weapons may engage human targets only inside a kill box confirmed clear of
    civilians (Phase II policy).
  - Ground attack weapons default to weapons-hold (human-in-the-loop) during movement;
    shift to weapons-tight before PL LD.
  - Air-defense autonomous weapons operate weapons-tight (autonomous engagement of enemy
    air within 10 km).
  - Commander must disable a kill box before friendly humans enter it.
  - Vehicle discrimination relies on thermal/shape recognition; expect ~50% loss to
    enemy countermeasures and decoys.

**Grounding check:** Two items [inferred] - the overall mission-success end-state
treated as a "measure" (stated as a reached end-state, not a scored metric) and the Fort
Benning origin of the place names. The "Puma-class" ISR and "Switchblade-class" attack-UAS
analogies are grounded (the author states them in notes 15-16), as is the CROWS accuracy
comparison (note 27). All forces, platforms, ranges, weapons-control transitions, and
battle-damage counts are grounded in the source. Execution context is constructive
(author-labeled notional concept). Rules of engagement are central to the scenario, so
"Not applicable"/"Not specified" do not arise.
