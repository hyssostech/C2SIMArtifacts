# ASX Message-Instantiation Review Notes

These are **review / analysis notes**, contributed for discussion. They are
**not** authoritative model changes, and nothing has been applied to the OWL
model. The intent is to add *coverage* (walking scenarios into concrete message
instances) and to surface *problems* that instantiation reveals in the proposed
ASX elements - phrased as questions for the sub-group, not as decisions.

How the message work is stored (decision S4 in the log): Elizabeth's binary
`.xlsx` sample-message workbooks are **left untouched** (binary workbooks cannot
be merged if two people edit them). Instead, this review works on diff-able
**SpreadsheetML `.xml` copies** of the three workbooks - in `Subgroups/ASX/
Proposed Extension Working Materials/` - and that is where all the instantiation
tabs live. The `.xml` were verified cell-for-cell against the originals; nothing
in the `.xlsx` changed.

## Start here

- [Group-Briefing.md](./Group-Briefing.md) - one-page bearings for the sub-group:
  what this is, what was found, the ~22 decisions, and where the ball is now.

## Contents

- [Message-Instantiation-Coverage.md](./Message-Instantiation-Coverage.md) -
  the pre-walk `.xlsx` baseline snapshot (2026-06-10) that motivated the review;
  the current instantiation state is tracked in the log (C1-C8).
- [Initialization-Walk.md](./Initialization-Walk.md) - a proposed walk of the
  three Initialization scenarios Elizabeth named but left empty
  (`UAV with Video Init`, `UAV Patrol Initialization`, `Swarm Initialization`),
  mirroring her sheet columns, with the problems each one exposes.
- [CASEVAC-Walk.md](./CASEVAC-Walk.md) - end-to-end walk of the CASEVAC
  contributed scenario (Init + Order + robot-to-robot coordination + Reports),
  surfacing X1 (no robot-to-robot content type) and X2 (no explainability
  element) as the highest-value gaps it exposes.
- [NonVideoSensors-Walk.md](./NonVideoSensors-Walk.md) - CBRN / EW / GPR report
  instantiations that stress the sensor model; shows the media-based
  `Video Detection Report` model does not generalize to non-imaging sensors
  (Y1-Y5).
- [Swarm-Walk.md](./Swarm-Walk.md) - swarm detection report + coordination
  order; exercises P7 (a swarm can't be tasked/report as modeled) and shows
  membership/command already exist in base C2SIM (P8 narrowed; Z1/Z2 residuals).
- [FireSupport-Walk.md](./FireSupport-Walk.md) - armed engagement + BDA;
  opens the task/effect axis and surfaces W1 (no link between autonomy level and
  authority to take a lethal action). ROE and authorization already exist.
- [TaskEffect-Batch-Walk.md](./TaskEffect-Batch-Walk.md) - Logistics, Engineering,
  and USV Rescue in one pass; the task/effect axis needs mainly payload/effector/
  weapon typing plus a few manipulation verbs - most task verbs (BREACH, ENGAGE,
  ATTACK, RESCUE, RECOVR, ...) already exist in LOX.
- [RedundancyPass-Walk.md](./RedundancyPass-Walk.md) - confirmation pass over
  route-clearance / companion / urban; mostly redundant, but extracts N1 (an
  area cannot be the subject of a task or report).
- [SourcedScenarios-Walk.md](./SourcedScenarios-Walk.md) - maritime MCM,
  subterranean SubT, and sustainment, taken from the parallel scenario-sourcing
  session (`LLMExperiments/PaperSummaries/V2Extractions/` + its
  `OntologyConceptCoverage.md` handoff). Corroborates P1/X1/N2/Y and adds G1-G10, incl. a proposed generic
  Detection Report that resolves the sensor-report (Y) series.
- [ValidationEvidence-Walk.md](./ValidationEvidence-Walk.md) - integrates the
  scavenger session's nine sourced missions (`Documents-Found.md`). Moves the
  validation holes to evidenced and captures concrete report schemas to adopt -
  most importantly BML `WhoMeasuredType`, prior art in C2SIM's lineage for the
  measurement report (Q-Q).
- [Documents-Needed.md](./Documents-Needed.md) / [Documents-Found.md](./Documents-Found.md)
  - the sourcing brief and the scavenger session's point-by-point response.
- [Issues-And-Comments-Log.md](./Issues-And-Comments-Log.md) - running,
  consolidated log of every issue/comment found, with severity and status;
  the findings deck is generated from it.
- `ASX-Instantiation-Findings.pptx` - findings presentation for the ASX
  sub-group. Regenerate/edit it via `build_findings_deck.py` (the `.pptx` is a
  zipped-XML binary git cannot merge, so the Python generator is the diff-able
  source). Requires `python-pptx`.

## Source of truth

- Proposed OWL model: `Subgroups/ASX/Proposed Extension/CSIM_ASX.rdf`
  (last updated 2026-01-20).
- Attribute concepts: `Subgroups/ASX/Proposed Extension Working Materials/ASX Concept Mapping.xlsx`.
- Worked message examples (Elizabeth's, untouched): the three
  `ASX Sample * Messages.xlsx` workbooks (created 2026-06-10).
- Review working copies (diff-able, where the instantiation tabs live): the three
  `ASX Sample * Messages.xml` in `Proposed Extension Working Materials/`.
- Base standard classes: `Ontology/C2SIM.rdf`, `Ontology/C2SIM_SMX.rdf`,
  `Ontology/C2SIM_LOX.rdf`.

Status: committed on branch `asx-diffable-spreadsheets` (draft PR #3 on the
fork). Prepared by Paulo Barthelmess (Hyssos).
