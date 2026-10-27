# Scenario extracted from report (v2.2 prompt)

Dibernardo, M. (2026). Autonomous Ground Vehicles and the Sustainment Problem:
One Brigade's Experiment and What the Army Should Do Next. Modern War Institute at
West Point. Source read in full (article text; accessed 2026-07-10):
https://mwi.westpoint.edu/autonomous-ground-vehicles-and-the-sustainment-problem-one-brigades-experiment-and-what-the-army-should-do-next/

Source note: this is a professional-commentary article, not a technical report.
Its situated vignette is concrete but thin on step-level detail, so this record
carries several "Not specified in source" marks by design.

### Scenario 1: Autonomous last-tactical-mile team resupply under threat (ULTRA UGV)

**Domain / mission type:** land; logistics / contested resupply (last tactical mile), with a CASEVAC-adjacent risk-reduction role (decoy).

**Source location:** Paragraphs on the Panther Avalanche / JRTC rotation of 3rd Brigade, 82nd Airborne Division; the contested-resupply vignette.

**Purpose (why the authors present it):** To argue from a brigade's field
experiment that autonomous ground vehicles have immediate operational value for
sustainment and should be scaled. (Advocacy/lessons-learned intent - not the
in-world objective.)

**Summary narrative:** During Panther Avalanche, a large-scale live-fire training
event, and a Joint Readiness Training Center rotation, 3rd Brigade, 82nd Airborne
Division employed four ULTRA autonomous ground vehicles (Overland AI) for
sustainment. Soldiers loaded a vehicle, entered a grid, and it departed and
executed the distribution task autonomously with no operator following it. Across
the rotation the systems executed 50+ autonomous runs, several exceeding nine
kilometers. In one contested case, an autonomous ground vehicle ran an
eight-kilometer resupply to a sniper team that had gone thirty-six hours without
food, and one platform was used as a decoy to reduce risk during the mission.

**In-world objectives:**
- Deliver critical supplies to forward teams (drop-zone distribution and team resupply) without exposing soldiers.
- Sustain a stranded/forward team under threat (the contested eight-kilometer resupply).
- Reduce risk to the delivery (use of a platform as a decoy).

**Autonomous systems employed:**
- ULTRA autonomous ground vehicle (UGV; Overland AI), 4 systems - autonomous point-to-point transport; loaded by soldiers, tasked to a grid, then self-navigates. One platform used as a decoy in the contested mission.

**Measures of Performance:**
- Distribution time on the drop zone reduced by 52 percent.
- Bundle-recovery timeline reduced from 24 hours to 8 hours.
- 50+ autonomous runs completed; several exceeding 9 km.
- [inferred] Reduced soldier exposure and driver burden (stated as an effect, not a metric).
- [inferred] Successful delivery to the sniper team in the contested vignette (implied, not stated as an outcome metric).

**Scenario steps:**
1. Soldiers load supplies onto the ULTRA UGV and assign it a destination grid.
2. UGV departs and self-navigates to the destination autonomously (no operator following).
3. UGV delivers supplies to the forward team / drop zone.
4. (Contested vignette) A second platform is employed as a decoy to reduce risk while the resupply UGV runs the eight-kilometer route to the sniper team.
5. Detailed en-route steps, route selection, and hand-off procedure: Not specified in source.

**Environment and constraints:** Expansive training area (Panther Avalanche live-fire event; JRTC rotation). Contested conditions in the eight-kilometer vignette. Execution context: field-experiment (live, in training). Open constraints stated by the author: payload, transportability, substitution ratio with legacy platforms, and performance in heavily wooded, muddy, or deeply rutted terrain. Rules of engagement: Not applicable (sustainment task). Terrain specifics for the contested mission: Not specified in source.

#### Conceptual model (ontology seed)
- **Domain and scope:** Autonomous ground-vehicle sustainment (resupply) for tactical formations, including contested last-tactical-mile delivery.
- **Concepts (classes):** Autonomous ground vehicle (ULTRA), Supported team, Supply/bundle, Drop zone, Decoy platform, Distribution task, Sustainment mission.
- **Taxonomy (IS-A):**
  - Autonomous system -> UGV
  - UGV -> Resupply UGV
  - Sustainment mission -> Routine distribution
  - Sustainment mission -> Contested resupply
- **Relationships (triples):**
  - Soldier | loads | Resupply UGV
  - Resupply UGV | delivers | Supply to Supported team
  - Resupply UGV | navigates to | Destination grid
  - Decoy platform | reduces risk to | Resupply UGV
- **Properties:**
  - Resupply UGV (ULTRA): autonomous navigation, payload (Not specified), run distance (>9 km observed), quantity fielded (4)
  - Sustainment mission: routine vs contested, distance, threat level
  - Supported team: type (e.g. sniper team), forward/stranded status
- **Constraints/rules:**
  - UGV operates autonomously after tasking (no trailing operator).
  - Open performance questions: payload, terrain (wooded/muddy/rutted), transportability, substitution ratio.

**Grounding check:** Two MoP items [inferred]; en-route steps, terrain specifics,
and payload "Not specified in source"; ROE "Not applicable". Narrative and stated
metrics grounded in source.
