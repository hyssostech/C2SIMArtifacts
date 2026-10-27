# ASX Message-Instantiation Coverage

> **NOTE - this is the pre-walk baseline (2026-06-10 `.xlsx`), now superseded.**
> It records the state of Elizabeth's `.xlsx` workbooks *before* this review's
> walks. The review's instantiation tabs (Init, CASEVAC, sensing, swarm,
> task/effect, sourced scenarios) were subsequently added to the diff-able
> `.xml` copies - see decision S4 and coverage rows C1-C8 in
> `Issues-And-Comments-Log.md`. The STUB/empty rows and the "0 Initialization"
> reading below describe the `.xlsx` baseline only; all three
> Initialization scenarios and the Swarm Detection report are now instantiated
> in the `.xml`.

Snapshot of which scenarios have concrete C2SIM message instantiations in the
`ASX Sample * Messages.xlsx` workbooks, and which are still open. Compiled by
reading every sheet in the three workbooks (created 2026-06-10) plus the
in-repo scenarios.

Legend:
- **DONE** - sheet has a worked instantiation.
- **STUB** - sheet exists in the workbook but holds only the header row.
- **none** - no sheet for this scenario/message type yet.
- **n/a** - not expected for this scenario.

## By workbook sheet (what exists today)

| Message type | Sheet | Status | Notes |
|---|---|---|---|
| Report | Report Base Attributes | DONE | Reusable ASX design: MediaReference, AnalystComment, AnalysisConcept, MediaTypeEnum, SensorObservation |
| Report | Video Detection Report | DONE | Flagship worked example (UAV, onboard AI video detection) |
| Report | Swarm Detection | STUB | empty |
| Order | UAV Change Patrol Route | DONE | ASX Task with hasAffectedEntity / DesiredEffectCode; route payload is free text |
| Order | UGV Retrieve & Transport | DONE | Parallel ASX Task |
| Init | UAV with Video Init | STUB | empty |
| Init | UAV Patrol Initialization | STUB | empty |
| Init | Swarm Initialization | STUB | empty |

Plus the generic envelope template sheet in each workbook (Header + MessageBody
skeleton), which is filled and reusable.

Tally: **4 worked instantiations** (2 Report, 2 Order, 0 Initialization),
**4 stubs**, everything else not yet created.

## By scenario (coverage gap)

Init / Order / Report columns show whether each message type is instantiated
for that scenario.

| Scenario | Source | Init | Order | Report |
|---|---|---|---|---|
| UAV onboard video detection | Video Detection Report + MUTT Recon | STUB | n/a | DONE |
| UAV patrol / change route | UAV Patrol + Change Route order | STUB | DONE | none |
| UGV retrieve & transport | MUTT Logistics; CASEVAC transport leg | none | DONE | none |
| Swarm (detect / coordinate) | Swarm sheets | STUB | none | STUB |
| **CASEVAC (full thread)** | ContributedScenarios/CASEVAC.md | none | none | none |
| MUTT: Recon & Surveillance | MUTT use cases #3 | none | none | partial via Video Detection |
| MUTT: Logistics & Supply | MUTT use cases #1 | none | partial via UGV Retrieve | none |
| MUTT: EW & Communications | MUTT use cases #5 | none | none | none |
| MUTT: Route Clearance / Mine | MUTT use cases #6 | none | none | none |
| MUTT: Force Protection / Patrol | MUTT use cases #7 | none | none | none |
| MUTT: Fire Support | MUTT use cases #8 | none | none | none |
| MUTT: CBRN Defense | MUTT use cases #9 | none | none | none |
| MUTT: Engineering / Construction | MUTT use cases #4 | none | none | none |
| MUTT: Urban Combat Support | MUTT use cases #10 | none | none | none |
| Synthetic CASEVAC | LLMExperiments/SyntheticScenarios | none | none | none |
| Synthetic Corona & Biaginni 2019 | LLMExperiments/SyntheticScenarios | none | none | none |
| Purely Synthetic | LLMExperiments/SyntheticScenarios | none | none | none |

## Reading of the gap

- Instantiation so far is concentrated on **one UAV video-surveillance thread**
  (Report done, patrol Order done) plus a **UGV transport Order**. That is the
  ~20% that is done.
- **Initialization is the least-developed area** (no worked examples yet across all
  three named scenarios). It is also the message type that most directly forces
  the entity-typing decisions in the ASX proposal (how an autonomous platform,
  its sensors, and a swarm are declared). This is why the companion
  `Initialization-Walk.md` starts there - it is pure additive coverage and the
  highest-signal place to test the proposed classes.
- **CASEVAC** - the one human-authored, GSD-structured contributed scenario - has
  no messages of any type, yet it demands message patterns the current examples
  do not cover (machine-to-machine route hand-off, "explainable reasons"
  reports, on-the-loop status). Strong candidate for the first full three-message
  walk after Initialization.
- The MUTT scenarios are LLM-generated (the file still contains a `**User**`
  prompt and citation markers), so treat them as a breadth checklist of sensor
  and effect types to stress-test against, not as authoritative requirements.

## Suggested order of additional coverage

1. Initialization for the three named scenarios (see `Initialization-Walk.md`).
2. CASEVAC full thread (Init + Orders + Reports) - exercises coordination and
   explainability the current set misses.
3. Non-video sensor reports (CBRN, EW/jammer, thermal, GPR) - stress-tests the
   MediaTypeEnum / SensorType conflation.
4. Swarm Detection report + Swarm coordination order - exercises the collective
   entity typing.
