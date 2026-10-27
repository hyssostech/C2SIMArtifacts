# V2.2 Scenario Extractions (coverage expansion)

Scenario records produced with the locked v2.2 extraction prompt
([../PromptV2.md](../PromptV2.md)) from newly added source reports. These expand
the library beyond its original UAV/UGV air-ground reconnaissance/escape set into
domains it did not previously cover. Candidate sources and the coverage-gap
rationale are in [../../CandidateSources.md](../../CandidateSources.md); the
prompt's development and validation are in [../V2-HeadToHead.md](../V2-HeadToHead.md).

Each record follows the v2.2 template: Domain/mission-type tag, Purpose (authors'
intent) kept separate from In-world objectives, grounded narrative/steps with
[inferred] and "Not applicable"/"Not specified" marks, and an ontology-seed
Conceptual Model. Sources were read in full (verbatim text), not summarized by a
third party.

| File | Source | New domain / concept covered |
| --- | --- | --- |
| [SubT_Roucek2019.md](./SubT_Roucek2019.md) | Roucek et al. 2019, DARPA SubT (MESAS 2019) | Subterranean multi-robot exploration / SAR |
| [CooperativeMCM_Ling2020.md](./CooperativeMCM_Ling2020.md) | Ling 2020, NPS thesis (DTIC AD1126497) | Undersea / maritime-surface mine countermeasures |
| [Sustainment_MWI2026.md](./Sustainment_MWI2026.md) | Dibernardo 2026, Modern War Institute | Logistics / contested resupply (last tactical mile) |
| [Explainability_Agrawal2021.md](./Explainability_Agrawal2021.md) | Agrawal, Cleland-Huang et al. 2021, arXiv:2109.02077 | Explainability / human-on-the-loop (validation hole #1) |
| [CBRN_Muster2024.md](./CBRN_Muster2024.md) | Muster et al. 2024, UGV-CBRN, arXiv:2406.14385 | CBRN reconnaissance + manipulation (validation hole #2) |
| [CounterUAS_CNAS2025.md](./CounterUAS_CNAS2025.md) | Pettyjohn & Campbell 2025, CNAS Countering the Swarm | Counter-UAS / swarm-vs-swarm (request #5) |
| [MUMT_Remmersmann2015.md](./MUMT_Remmersmann2015.md) | Remmersmann et al. 2015, BML for Multi-Robot Systems | Human-machine teaming at C2/tasking level (request #6) |
| [SAR_Kim2021.md](./SAR_Kim2021.md) | Kim et al. 2021, Sensors (PMC8537596) | Humanitarian SAR, non-combat (request #7) |
| [FormationConvoy_Hu2020.md](./FormationConvoy_Hu2020.md) | Hu 2020, DOT/arXiv:2104.06507 | Formation/convoy geometry (request #8; civilian domain) |
| [Engineering_RCBC2018.md](./Engineering_RCBC2018.md) | U.S. Army RCBC / JWA 19 breach (multi-source) | Combat-engineering robotic breach (request #9) |
| [PersistentWatch_MDARS.md](./PersistentWatch_MDARS.md) | MDARS overview, DTIC ADA422465 | Persistent surveillance / sentry (validation hole #4) |
| [ElectronicWarfare_EmitterGeoloc.md](./ElectronicWarfare_EmitterGeoloc.md) | AFIT thesis DTIC AD1054177 + ADA444985 | EW emitter geolocation + electronic attack (validation hole #3) |
| [Brutzman_Fitzpatrick2020.md](./Brutzman_Fitzpatrick2020.md) | Brutzman & Fitzpatrick 2020, NPS-MV-20-001 | Village-defense MUM-T ISR (original library paper) |
| [Biagini_Corona_Casar2017.md](./Biagini_Corona_Casar2017.md) | Biagini, Corona & Casar 2017, MESAS | Urban counter-UAxS, 2 variants (original library paper) |
| [Langerwisch2013.md](./Langerwisch2013.md) | Langerwisch et al. 2013, SSRR | Heterogeneous MOVE/OBSERVE, 2 tasks (original library paper) |
| [LIRC_MovementToContact_Morris2018.md](./LIRC_MovementToContact_Morris2018.md) | Morris 2018, Military Review | Company-scale manned-unmanned combined-arms movement to contact w/ LAWS, kill-box weapons-control (SME baseline) |
| [LIRC_MovementToContact_Updated2024.md](./LIRC_MovementToContact_Updated2024.md) | Morris 2018 baseline + 4 Infantry Magazine sources (2023-2024) | Small-drone warfare update: FPV/loitering-munition/COTS threat, EW/GPS denial, organic counter-UAS (SME-directed enhancement) |
| [OPFOR_CommercialSUAS_Targeting_Rosenberg2024.md](./OPFOR_CommercialSUAS_Targeting_Rosenberg2024.md) | Rosenberg 2024, Infantry (JPMRC-AK 24-02) | RED/OPFOR reconnaissance-strike: COTS sUAS cueing indirect fires vs HPTs; first red-perspective + first targeting-cycle record |

### SME-directed baseline + update (Morris 2018 LIRC)

The last two rows are a matched pair added at an SME's request. Morris 2018 is a
detailed notional company scenario the SME designated as the drone-warfare BASELINE;
its threat and friendly concept predate the 2022 Russo-Ukrainian War.
`LIRC_MovementToContact_Updated2024.md` is an analyst-updated derivative (not a fresh
source extraction) that revises the baseline's threat and U.S. equipment/TTP against
four SME-provided Infantry Magazine articles - Wilkins 2023 (Russo-Ukrainian unmanned
platforms), Rosenberg 2024 (commercial sUAS targeting), Hamilton & Egan 2023 (SUAS for
light infantry battalions), and Padalino 2024 (tactical drone warfare). Every
real-world fact in the update is tagged to its source and every application to the
notional vignette is tagged [inferred]; see that file's grounding contract. The two
Infantry issues (source PDFs) are in [../../References/](../../References/).

The Rosenberg JPMRC-AK 24-02 OPFOR COTS-targeting run is also extracted as its own
standalone record,
[OPFOR_CommercialSUAS_Targeting_Rosenberg2024.md](./OPFOR_CommercialSUAS_Targeting_Rosenberg2024.md)
- the library's first RED/OPFOR perspective and first reconnaissance-strike / targeting
scenario. (The Wilkins "possible scenario" remains folded into the update as threat
context; it could be minted separately if the group wants it.)

The three rows above the pair promote the original library papers (Brutzman, Biagini/Corona 2017,
Langerwisch) - whose v2 extractions previously lived only inside
[V2-HeadToHead.md](../V2-HeadToHead.md) - into first-class standalone records, so
the whole library now has uniform v2.2 coverage. Their content matches the
head-to-head extractions; the head-to-head retains them for the V1-vs-V2 comparison.

Source-fidelity notes (after the "hunt harder" pass): `ElectronicWarfare_EmitterGeoloc`
is now a real extraction from a primary open-access UAV emitter-geolocation flight
experiment (AD1054177), with the electronic-attack side from ADA444985 - the earlier
composed placeholder is gone. `Engineering_RCBC2018` is now built from multiply-
corroborated open reporting of the RCBC/JWA-19 breach (the primary Maneuver Battle
Lab report is not openly available). Both remain flagged in-file.

Records after CBRN were sourced against the ontology session's brief
[`../../InstantiationReview/Documents-Needed.md`](../../InstantiationReview/Documents-Needed.md);
the sourcing response is
[`../../InstantiationReview/Documents-Found.md`](../../InstantiationReview/Documents-Found.md).

Note on source type: the SubT and MCM sources are technical reports with fully
specified scenarios. The MWI source is a professional-commentary article; its
situated vignette (a contested resupply) is concrete but thinner on step-level
detail, so that record carries more "Not specified in source" marks - which is
the prompt behaving correctly, not a gap in the extraction.
