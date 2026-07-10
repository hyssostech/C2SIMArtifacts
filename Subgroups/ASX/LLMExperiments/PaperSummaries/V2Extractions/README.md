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

| File | Source | New domain covered |
| --- | --- | --- |
| [SubT_Roucek2019.md](./SubT_Roucek2019.md) | Roucek et al. 2019, DARPA SubT (MESAS 2019) | Subterranean multi-robot exploration / SAR |
| [CooperativeMCM_Ling2020.md](./CooperativeMCM_Ling2020.md) | Ling 2020, NPS thesis (DTIC AD1126497) | Undersea / maritime-surface mine countermeasures |
| [Sustainment_MWI2026.md](./Sustainment_MWI2026.md) | Dibernardo 2026, Modern War Institute | Logistics / contested resupply (last tactical mile) |

Note on source type: the SubT and MCM sources are technical reports with fully
specified scenarios. The MWI source is a professional-commentary article; its
situated vignette (a contested resupply) is concrete but thinner on step-level
detail, so that record carries more "Not specified in source" marks - which is
the prompt behaving correctly, not a gap in the extraction.
