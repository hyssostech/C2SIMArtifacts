# Documents Found - response to Documents-Needed.md

Sourcing session's response to the brief in `Documents-Needed.md`. For each
request: the best source located, whether it is open-access and a concrete
situated vignette (the pipeline criterion), extraction status, and the ASX
decisions it grounds. Extractions use the locked v2.2 prompt and live in
`../LLMExperiments/PaperSummaries/V2Extractions/`.

Status legend: **EXTRACTED** (record written) - **SOURCED** (verified source, not
yet extracted) - **HUNTING** (no clean open-access vignette yet).

## UPDATE - all nine requests now extracted

All nine requests (plus the optional item, partially) now have v2.2 records in
`../LLMExperiments/PaperSummaries/V2Extractions/`:

| # | Request | Record | Fidelity |
|---|---|---|---|
| 1 | Explainability / on-the-loop | Explainability_Agrawal2021.md | strong |
| 2 | CBRN reconnaissance | CBRN_Muster2024.md | strong |
| 3 | EW sensing / attack | ElectronicWarfare_EmitterGeoloc.md | **composed / low** (no open vignette; replace if a real one is found) |
| 4 | Persistent watch | PersistentWatch_MDARS.md | strong (DTIC MDARS) |
| 5 | Counter-UAS / swarm | CounterUAS_CNAS2025.md | strong (TTX vignette) |
| 6 | Human-machine teaming | MUMT_Remmersmann2015.md | strong (local BML paper) |
| 7 | Humanitarian SAR | SAR_Kim2021.md | strong (open PMC) |
| 8 | Formation / convoy geometry | FormationConvoy_Hu2020.md | strong geometry, **civilian domain** |
| 9 | Combat-engineering / EOD | Engineering_RCBC2018.md | **reported-facts** (primary page blocked) |

Two records carry fidelity caveats worth the ontology session's attention: **#3 EW**
(composed from technical descriptions, not a situated vignette) and **#9 breach**
(built from the RCBC demonstration's reported facts). Both are flagged in-file and
are the first candidates to replace if better open-access sources surface. The
sections below record the sourcing detail as originally written.

## Validation holes (top priority)

### 1. Explainability / human-on-the-loop - EXTRACTED
- **Source:** Agrawal, Cleland-Huang et al. (2021), "Explaining Autonomous
  Decisions in Swarms of Human-on-the-Loop Small Unmanned Aerial Systems",
  arXiv:2109.02077 (open access).
- **Fit:** strong. Concrete multi-sUAS SAR mission (DroneResponse), four autonomy
  events, explanations pushed to an on-the-loop operator with {event, action,
  reasoning, operational change, confidence}, plus deliberate wrong-perception
  cases and operator override.
- **Record:** [Explainability_Agrawal2021.md](../LLMExperiments/PaperSummaries/V2Extractions/Explainability_Agrawal2021.md)
- **Grounds:** Q-H (explanation-report content: event/action/reasoning/confidence),
  Q-K/W1 (on-the-loop configure/suspend/acknowledge/override), Q-D (event-driven
  behavior change; per-decision confidence).

### 2. CBRN reconnaissance - EXTRACTED
- **Source:** Muster et al. (2024), "UGV-CBRN: An Unmanned Ground Vehicle for
  Chemical, Biological, Radiological, and Nuclear Disaster Response",
  arXiv:2406.14385 (open access).
- **Fit:** strong. Concrete mission field-tested at EnRicH 2023: autonomous
  radiation mapping (Geiger + GP regression), semi-autonomous valve closure and
  substance sampling, on-site Raman analysis.
- **Record:** [CBRN_Muster2024.md](../LLMExperiments/PaperSummaries/V2Extractions/CBRN_Muster2024.md)
- **Grounds:** Q-Q (Y3 hazard/agent detection, Y5 measurement value; radiation-map
  cell estimate + variance as confidence), Q-M (N1 contaminated-area map). Bonus:
  E1/E2 manipulation verbs + effector typing (request #9) and G10 no-adversary
  framing (request #7).

### 3. Electronic-warfare sensing / attack - SOURCED (vignette-thin)
- **Best candidate (EW attack):** "Jamming and Spoofing Techniques for Drone
  Neutralization: An Experimental Study", Drones (MDPI, 2024), 8(12):743 (open
  access). Experimental engagement (SDR jamming to neutralize a UAV).
- **Best candidate (EW sensing):** "Emitter Geolocation with Multiple UAVs"
  (IEEE) - a 3-4 UAV TDOA network geolocating an emitter; **paywalled**.
- **Caveat:** open-access EW sources are technique-heavy; neither is as
  vignette-rich as requests 1-2. The MDPI jamming study is the more extractable
  of the two. Recommend extraction with the understanding that steps will be
  thinner (more "Not specified in source").
- **Grounds when extracted:** Q-Q (Y4/Y5 emitter/signal reading), effect-vs-ROE.

### 4. Persistent surveillance / sentry - SOURCED (system-description heavy)
- **Best candidate:** MDARS (Mobile Detection Assessment Response System) -
  Army/Navy autonomous sentry fielded at DoD sites (e.g. Nevada National Security
  Site); and Everett et al., "Extending mobile security robots to force protection
  missions" (SPIE). MDARS provides standing-watch, intruder detection/assessment,
  barrier/inventory checks, one operator overseeing many platforms.
- **Caveat:** MDARS sources are more system/CONOPS description than a single
  situated vignette; the force-protection SPIE paper is the more mission-shaped
  one but was not cleanly retrievable open-access (academia.edu copy blocked).
  A cleaner persistent-ISR vignette (loiter-and-report / relief cadence) would be
  worth a dedicated hunt.
- **Grounds when extracted:** N2 (standing/persistent task with cadence), Q-U
  (station-keeping/relief), Q-N (area coverage).

## Invisible-domain gaps (candidates already listed - extraction pending)

### 5. Counter-UAS / swarm-vs-swarm - candidate ready
- CNAS "Countering the Swarm" and CNA "PRC Concepts for UAV Swarms" (both open,
  in `../LLMExperiments/CandidateSources.md`). Note: the urban counter-UAxS
  scenario (Biagini/Corona 2017) is already extracted and covers layered
  kinetic/non-kinetic defeat, graded LoA, and hostile-swarm typing - so this
  domain is partially grounded already. A step-level swarm-vs-swarm vignette
  would still add value.

### 6. Human-machine teaming (C2 / tasking) - candidate ready + needs a mission
- HATOM (NATO STO) is a vocabulary model, not a mission. Pair it with a MUM-T
  mission vignette; the Brutzman village-defense MUM-T scenario (already in the
  library) partially grounds mixed human-machine task allocation. A dedicated
  human-robot task-allocation field experiment would be the ideal add.

### 7. Humanitarian SAR (non-combat) - candidate ready
- MDPI Drones (2020) UAV+ground-robot SAR (open, in CandidateSources). Note the
  two extractions above (Explainability SAR sUAS, CBRN disaster response) already
  exercise no-adversary framing (G10) and area search (Q-N), so this gap is now
  partially filled; the MDPI SAR case would consolidate it.

## Expressiveness / grounding-upgrade

### 8. Formation / convoy geometry - HUNTING
- Partially seen in Langerwisch MOVE (already extracted: convoy + escort +
  circular observation poses). For a dedicated construct (orbit, convoy spacing,
  observation-pose pattern), look at autonomous-convoy experiments (e.g. Army
  Expedient Leader-Follower / GVSC autonomous convoy) or cooperative-ISR
  formation trials. No clean open-access vignette pulled yet.
- **Grounds:** Q-U (formation/relative geometry), Q-L (escort/follow), Q-P.

### 9. Combat-engineering / EOD manipulation - partially covered
- The CBRN extraction (#2) already grounds the manipulation family: end-effector
  task verbs (valve close, grasp, sample) and manipulator/effector typing
  (E1/E2), plus area-state via the hazard map (N1). A dedicated EOD render-safe
  or combat-engineer breach/emplace AAR (DTIC) would add the defeat/emplace verbs
  specifically; recommend a targeted hunt if E-series needs more than CBRN gives.

## Optional
- **Degraded-environment (weather/terrain/illumination):** partially covered by
  SubT (GPS/comms-denied, mud/fog) and CBRN (tight indoor, narrow doors). The
  Explainability case adds weather-driven autonomy change (fly lower/slower in
  mist). A dedicated degraded-environment case (G11/Q-T) is now lower urgency.

## Summary for the ontology session

- **Extracted this pass:** explainability (#1) and CBRN (#2) - the two clearest
  validation holes, now grounded with concrete open-access vignettes.
- **Ready to extract on request:** counter-UAS (#5), SAR (#6/#7) - candidates in
  hand; EW (#3) and persistent (#4) sourced but vignette-thin (flagged).
- **Needs more hunting:** a step-level swarm-vs-swarm vignette (#5), a dedicated
  formation-geometry mission (#8), and an EOD render-safe AAR (#9) if CBRN's
  manipulation grounding is insufficient.
- Coverage side-effects worth noting: the two new extractions also partially
  close request #7 (no-adversary framing) and #9 (manipulation), and touch the
  optional degraded-environment item.
