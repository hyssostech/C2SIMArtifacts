# Scenario extracted from report (v2.2 prompt)

Pettyjohn, S. & Campbell, M. (2025). Countering the Swarm: Protecting the Joint
Force in the Drone Age. Center for a New American Security (CNAS). Source read in
full (report PDF), Chapter with Tabletop Exercise Vignette 1.

Sourced against `InstantiationReview/Documents-Needed.md` request #5 (counter-UAS
/ swarm-vs-swarm). Grounds Q-B, Q-K, Q-P.

### Scenario 1: Layered counter-UAS defense of a Marine expeditionary base against an autonomous drone swarm

**Domain / mission type:** air / maritime-littoral; counter-UAS (layered air defense) against a heterogeneous drone swarm.

**Source location:** Chapter 3, "Tabletop Exercise Vignette 1: Marine Littoral Regiment on Yonaguni, Japan"; Table 5; Figure 6.

**Purpose (why the authors present it):** A one-sided planning tabletop exercise
(TTX) to examine how U.S. forces posture and plan air defense to defeat Chinese
drone attacks, and to expose gaps in counter-drone operations. (Analytic/wargame
intent.)

**Summary narrative:** Set 42 days into a protracted war over Taiwan, a U.S.
Marine Littoral Regiment conducting expeditionary advanced base operations on
Yonaguni (Southern Ryukyus) must defend against three escalating Chinese (Red)
drone attacks after both sides have depleted long-range missiles. The attacks
range from salvos of preprogrammed long-range kamikaze drones, to an uncrewed
surface vessel (USV) launching loitering munitions and FPV kamikaze drones, to an
autonomous, self-healing, heterogeneous swarm of about 220 FPV drones - five
"mothership" multirotors each carrying four FPVs plus 200 high-speed FPV drones
armed with 3 lb bombs. The Marines defend with a layered active defense: a
ground/air task-oriented radar and other multimode sensors for detection, an
expeditionary high-power-microwave (HPM) directed-energy weapon for mass, medium-
range interceptors (MRIC, Roadrunner VTOL interceptor), and gun/missile systems
(MADIS, Stinger/Avenger, VAMPIRE), the small island easing the defensive problem.

**In-world objectives:**
- (Red) Suppress and destroy U.S. forces and key nodes (fuel/supply points, radars, TELs) inside the First Island Chain using massed and autonomous drones.
- (Blue) Detect, identify, and defeat or absorb the drone attacks while continuing the expeditionary mission, conserving a limited interceptor magazine.

**Autonomous systems employed:**
- (Red) Long-range propeller kamikaze drones - preprogrammed one-way attack. Autonomy: preprogrammed flight paths.
- (Red) USV carrying Group 2 loitering munitions and FPV kamikaze drones. Autonomy: [inferred] semi-autonomous launch platform.
- (Red) Autonomous self-healing heterogeneous FPV swarm (~220): 5 mothership multirotors (4 FPVs each) + 200 armed FPVs. Autonomy: autonomous, self-healing, cooperative.
- (Blue) HPM directed-energy weapon; MRIC and Roadrunner interceptors; MADIS, Stinger/Avenger, VAMPIRE effectors; G/ATOR radar and multimode passive sensors. Autonomy: [inferred] human-directed effectors with automated fire-control aids.

**Measures of Performance:**
- Percentage of the swarm/salvo defeated or absorbed before impact.
- [inferred] Interceptor magazine expended per drone killed (cost-exchange / magazine depth).
- [inferred] Key assets (fuel/supply points, radars, TELs) surviving the attacks.

**Scenario steps:**
1. Red launches Attack 1: three salvos of six long-range kamikaze drones on preprogrammed paths, two minutes apart, against fixed fuel/supply points and TEL hides.
2. Red launches Attack 2: a USV releases loitering munitions and FPV kamikaze drones that hunt U.S. forces, radars, and TELs.
3. Red launches Attack 3: an autonomous self-healing swarm of ~220 FPV drones deploys from drone boats and motherships, creating a 360-degree threat vector.
4. Blue multimode sensors / G/ATOR radar detect and track the inbound drones -> classify by type and threat.
5. Blue applies layered effects: [inferred] soft-kill/EW where possible, HPM against massed FPVs, interceptors (MRIC/Roadrunner) against higher-value drones, guns/short-range missiles (MADIS/Stinger/Avenger/VAMPIRE) at close range.
6. Because the swarm is self-healing, Blue must attrit it faster than it re-forms while conserving magazine depth.

**Environment and constraints:** Small island (Yonaguni) in a maritime-littoral
setting within the First Island Chain; depleted long-range munitions on both
sides; 360-degree threat from sea- and air-launched drones. Execution context:
constructive (tabletop planning exercise; Red attacks scripted, ranges estimated
by the authors). Rules of engagement: constrained by magazine depth and airspace;
human fire decisions [inferred].

#### Conceptual model (ontology seed)
- **Domain and scope:** Layered counter-UAS defense of an expeditionary base against massed and autonomous drone attacks.
- **Concepts (classes):** Drone swarm, Kamikaze drone, Loitering munition, FPV drone, Mothership UAS, USV launcher, Counter-UAS sensor, Directed-energy weapon, Interceptor, Gun/missile effector, Magazine.
- **Taxonomy (IS-A):**
  - Autonomous system -> UAV -> Kamikaze drone, Loitering munition, FPV drone, Mothership UAS
  - Autonomous system -> USV (launcher)
  - Counter-UAS effector -> Directed-energy weapon, Interceptor, Gun/missile effector
  - Drone swarm -> Heterogeneous self-healing swarm
- **Relationships (triples):**
  - Mothership UAS | carries/launches | FPV drone
  - USV | launches | Loitering munition
  - Drone swarm | attacks | Expeditionary base
  - Counter-UAS sensor | detects | Drone swarm
  - Effector | defeats | Drone
  - Swarm | self-heals after | attrition
- **Properties:**
  - Drone swarm: size (~220), composition (motherships + FPVs), self-healing, heterogeneous
  - FPV drone: payload (3 lb bomb), speed
  - Effector: type (DEW/interceptor/gun), range, magazine depth
  - Sensor: modality (radar/passive), range
- **Constraints/rules:**
  - Self-healing swarm must be attrited faster than it re-forms.
  - Interceptor magazine is finite -> cost-exchange matters.
  - 360-degree threat vector from sea- and air-launched drones.

**Grounding check:** Several autonomy levels, effector-automation, and two MoP
items are [inferred]; ROE/human-fire authority [inferred]. Force compositions,
attack descriptions, and effector list grounded in source.
