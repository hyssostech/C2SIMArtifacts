# Candidate Source Reports to Expand Scenario Coverage

The current library (see [PaperSummaries](./PaperSummaries)) is narrow: every
extracted scenario is a UAV/UGV air-ground team doing reconnaissance, escort, or
point-defense in a land or urban setting. The candidates below extend coverage
into domains and mission types the library does not yet touch. Priority is given
to documents with concrete, extractable scenarios (situated mission vignettes),
because the extraction pipeline needs described missions, not surveys or news.

## Coverage gaps in the current library

- Maritime surface (USV) - absent
- Undersea (UUV) - absent
- Subterranean multi-robot - absent
- Logistics / resupply and CASEVAC grounded in a real report - only a synthetic
  CASEVAC exists today
- Counter-UAS / swarm-vs-swarm as a mission type - absent
- Human-machine teaming at the C2 / ontology level - absent
- Humanitarian / disaster response (dual-use, non-combat) - absent

## Candidates by gap

### Maritime surface (USV)
- Boretti, A. (2024). Unmanned surface vehicles for naval warfare and maritime
  security. Journal of Defense Modeling and Simulation.
  https://journals.sagepub.com/doi/10.1177/15485129241283056
  Peer-reviewed, mission-oriented (patrol, decoy, screening, swarm interception).
- A Swarm Paradigm for Uncrewed Surface Vessels. USNI Proceedings (2026).
  https://www.usni.org/magazines/proceedings/2026/may/swarm-paradigm-uncrewed-surface-vessels
  CONOPS-level swarm vignettes.

### Undersea (UUV)
- Use of Cooperative Unmanned Systems for Mine Countermeasures. DTIC AD1126497.
  https://apps.dtic.mil/sti/trecms/pdf/AD1126497.pdf
  Open access. Describes a defensive MCM vignette (round-the-clock USV/UUV
  neutralizing mines along a sea line of communication). Strong extraction
  candidate; pairs naturally with anti-submarine warfare.

### Subterranean multi-robot
- Roucek et al. (2019). DARPA Subterranean Challenge: Multi-robotic Exploration
  of Underground Environments. MESAS 2019.
  https://comrob.fel.cvut.cz/papers/mesas19subt.pdf
  Open access. Verified concrete scenario: heterogeneous team (wheeled Husky,
  tracked Absolem, hexapod crawlers, quadrotors), find-and-report artifacts
  underground, explicit scoring/MoP, clear operational steps. Same MESAS 2019
  volume as the Corona & Biagini benchmark - consistent source pedigree.

### Logistics / resupply and CASEVAC
- Autonomous Ground Vehicles and the Sustainment Problem: One Brigade's
  Experiment and What the Army Should Do Next. Modern War Institute.
  https://mwi.westpoint.edu/autonomous-ground-vehicles-and-the-sustainment-problem-one-brigades-experiment-and-what-the-army-should-do-next/
  Contains a concrete field vignette (contested 8 km resupply to a stranded
  sniper team, one platform used as a decoy) - extractable, unlike most news items.

### Counter-UAS / swarm-vs-swarm
- Pettyjohn, S. & Campbell, M. (2025). Countering the Swarm. CNAS.
  https://s3.us-east-1.amazonaws.com/files.cnas.org/documents/Report_CUAS_Defense_Sep-2025_final.pdf
  Layered detect / soft-kill / hard-kill framework; scenario-shaped.
- PRC Concepts for UAV Swarms in Future Warfare. CNA (2025).
  https://www.cna.org/reports/2025/07/PRC-Concepts-for-UAV-Swarms-in-Future-Warfare.pdf

### Human-machine teaming (C2 / ontology level)
- HATOM: Human-AI Teaming Ontology Model in Military Operations. NATO STO.
  https://www.sto.nato.int/document/hatom-human-ai-teaming-ontology-model-in-military-operations/
  Less a scenario source, more a cross-check for the Conceptual Model vocabulary.

### Humanitarian / disaster response (dual-use)
- Aerial and Ground Robot Collaboration for Autonomous Mapping in Search and
  Rescue Missions. Drones (MDPI, 2020).
  https://www.mdpi.com/2504-446X/4/4/79
  Concrete UAV + ground-robot SAR mission.

## Recommended first three

Open access, genuinely extractable, and each fills a distinct gap:

1. DARPA SubT MESAS paper - subterranean multi-robot.
2. DTIC AD1126497 cooperative MCM - undersea / maritime.
3. MWI sustainment experiment - logistics / CASEVAC.

Adding these three alone extends the library into subterranean, undersea, and
logistics/CASEVAC missions while keeping the same source pedigree as the existing
set.

## Added since drafting (SME-directed, 2026-07)

An SME provided a baseline scenario plus four update sources, now extracted/enhanced in
[PaperSummaries/V2Extractions](./PaperSummaries/V2Extractions) and saved under
[References](./References). These fill coverage the gap list above did not name:

- **Company-scale combined-arms manned-unmanned movement to contact** (Morris 2018 LIRC)
  - a full offensive with integrated autonomous fires, short-range air defense,
  contested logistics, and CASEVAC under kill-box weapons-control. The library's prior
  land scenarios were ISR/escort/point-defense/breach/convoy, not a combined-arms
  assault. Record:
  [LIRC_MovementToContact_Morris2018.md](./PaperSummaries/V2Extractions/LIRC_MovementToContact_Morris2018.md).
- **Small-drone-warfare threat environment** (FPV drones, loitering munitions, modified
  COTS, one-way attackers, kamikaze UGV) with **dense EW / GPS denial** and **organic
  counter-UAS** - modeled as an explicit scenario constraint, plus the cost-exchange
  inversion (cheap drones vs expensive platforms). This partially closes the
  counter-UAS and human-machine-teaming gaps above from the receiving/red side. Record:
  [LIRC_MovementToContact_Updated2024.md](./PaperSummaries/V2Extractions/LIRC_MovementToContact_Updated2024.md).

- **RED / OPFOR reconnaissance-strike targeting** (Rosenberg JPMRC-AK 24-02) - the
  library's first red-perspective scenario and first find-fix-target-BDA targeting
  cycle: COTS sUAS cueing indirect fires against high-payoff targets, plus the
  reciprocal counter-UAS survivability behavior. Record:
  [OPFOR_CommercialSUAS_Targeting_Rosenberg2024.md](./PaperSummaries/V2Extractions/OPFOR_CommercialSUAS_Targeting_Rosenberg2024.md).
