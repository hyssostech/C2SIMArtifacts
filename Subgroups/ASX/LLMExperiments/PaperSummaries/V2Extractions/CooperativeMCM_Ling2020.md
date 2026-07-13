# Scenario extracted from report (v2.2 prompt)

Ling, Tong H. (2020). Use of Cooperative Unmanned Systems for Mine
Countermeasures. Naval Postgraduate School thesis (DTIC AD1126497). Source read
in full from the web (apps.dtic.mil/sti/trecms/pdf/AD1126497.pdf); no local copy
in the repo.

### Scenario 1: Around-the-clock cooperative USV mine countermeasures on a sea line of communication

**Domain / mission type:** maritime-surface / undersea; defensive mine countermeasures (MCM) - detect, classify, neutralize.

**Source location:** Ch. III.A "Introducing the Scenario" (Region, Units Involved); III.B Measures of Effectiveness; III.C Model Assumptions.

**Purpose (why the authors present it):** To build an agent-based simulation
(MANA) and design-of-experiments study that compares MCM concepts of operations
(CONOPS) - i.e. to find which factors drive mine-neutralization performance and
risk. (Research intent - not the in-world objective.)

**Summary narrative:** In the Straits of Malacca and Singapore - a ~113 km long,
~19 km wide sea line of communication (SLOC) with 200+ transiting vessels daily -
hostile terrorist boats plant stationary moored or bottom naval mines. Because
the mine-layers cannot all be stopped, a minehunting force of cooperative
unmanned surface vehicles is deployed around the clock to detect, classify, and
neutralize the mines after they are laid, while commercial traffic continues to
transit. The friendly force comprises unmanned detectors (USV with TSAS),
unmanned neutralizers (USV with EMDS), and single-sortie CUSVs that both detect
and neutralize, launched from a manned host ship that stays out of the search
area. The study runs 60,000 simulated missions varying detector count/revisit
rate, sensor-range overlap, path deviation, and neutralizer sectorization.

**In-world objectives:**
- Detect and classify naval mines along the SLOC after they are planted.
- Neutralize as many mines as possible within the allocated time frame.
- Keep the sea lane usable for transiting commercial vessels (minimize active-mine risk).

**Autonomous systems employed:**
- USV with TSAS (USV) - unmanned detector/classifier. Autonomous; cooperative info-sharing.
- USV with EMDS (USV) - unmanned neutralizer. Autonomous; receives classified-mine locations from detectors.
- CUSV, Common Unmanned Surface Vehicle (USV) - single-sortie detector-and-neutralizer. Autonomous.
- Manned host ship - launches/recovers the unmanned units; stays out of the search area (not autonomous).

**Measures of Performance:**
- MOE1: percentage of mines neutralized (mines neutralized / mines planted).
- MOE2: average mine active time (neutralization time minus deployment time) - a risk indicator for transiting vessels.

**Scenario steps:**
1. Terrorist boats transit the SLOC and plant stationary moored/bottom mines at arbitrary points -> mines are armed once deployed.
2. Manned host ship, outside the search area, deploys detector USVs, neutralizer USVs, and/or CUSVs.
3. Detector USVs run a parallel-track search pattern over the operational area -> detect and classify mines (probability of success as a function of range).
4. Detector shares the exact classified-mine location with a neutralizer USV (cooperative, negligible delay).
5. Neutralizer USV proceeds to the location -> neutralizes the mine (no re-detection/re-classification needed).
6. Force revisits the area on a set cycle (every 8 h or 24 h) -> repeats detection/neutralization for newly laid mines (perpetual search).
7. Throughout, commercial vessels transit the lanes and may obstruct search paths.

**Environment and constraints:** Congested international strait, ~113 km x ~19 km,
200+ daily transits; neutral commercial traffic (5-60 m beam) obstructs search
paths. Execution context: constructive (MANA agent-based simulation; 60,000 runs;
design of experiments). Constraints/assumptions (stated): all USVs cooperative
and share information; detection+classification abstracted to a range-dependent
probability; mines are idle (do not detonate in-model); USV reliability/endurance
not modeled; revisit rate modeled as 3 detectors (8 h) or 1 detector (24 h).
Same-mission variations: the experiment factors (detector count/revisit rate,
sensor-range overlap, path deviation, neutralizer sectorization).

#### Conceptual model (ontology seed)
- **Domain and scope:** Defensive mine countermeasures on a sea line of communication using cooperative unmanned surface vehicles.
- **Concepts (classes):** Minehunting force, Detector USV, Neutralizer USV, CUSV, Manned host ship, Naval mine, Commercial vessel, Sea line of communication, Search pattern, Revisit cycle, MOE.
- **Taxonomy (IS-A):**
  - Autonomous system -> USV
  - USV -> Detector USV (TSAS)
  - USV -> Neutralizer USV (EMDS)
  - USV -> CUSV (single-sortie)
  - Naval mine -> Moored mine
  - Naval mine -> Bottom mine
- **Relationships (triples):**
  - Manned host ship | deploys | Detector USV
  - Manned host ship | deploys | Neutralizer USV
  - Detector USV | detects | Naval mine
  - Detector USV | classifies | Naval mine
  - Detector USV | shares location with | Neutralizer USV
  - Neutralizer USV | neutralizes | Naval mine
  - CUSV | detects and neutralizes | Naval mine
  - Commercial vessel | obstructs | Detector USV search path
  - Terrorist boat | plants | Naval mine
- **Properties:**
  - Detector USV: sensor (TSAS), detection range, speed, revisit rate
  - Neutralizer USV: neutralization payload (EMDS), sectorization
  - CUSV: single-sortie detect+neutralize
  - Naval mine: type (moored/bottom), position, active time, stationary once armed
  - Sea line of communication: length (~113 km), width (~19 km), traffic density
- **Constraints/rules:**
  - Detectors share exact classified-mine locations with neutralizers (cooperative, negligible delay).
  - Neutralizers do not re-detect/re-classify before neutralizing.
  - Search is perpetual; revisit cycle every 8 h or 24 h.
  - Commercial traffic may block search paths and constrains coverage.

**Grounding check:** All fields grounded in source; "Model assumptions" recorded
as constraints (they define the in-model scenario).
