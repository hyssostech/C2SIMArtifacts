# ASX Message-Instantiation Review Notes

These are **review / analysis notes**, contributed for discussion. They are
**not** authoritative model changes and they do **not** modify Elizabeth's
sample-message workbooks. The intent is to add *coverage* (walking scenarios
that do not yet have message instantiations) and to surface *problems* that
instantiation reveals in the proposed ASX elements - phrased as questions for
the sub-group, not as decisions.

Why a separate folder instead of editing the workbooks: the sample-message
files are binary `.xlsx` that Elizabeth is actively editing (all three were
created 2026-06-10). Two people editing the same workbook cannot be merged, so
any concurrent edit risks silently losing her work. Keeping this as separate
Markdown avoids that collision; anything here that is useful can be folded into
the workbooks by their owner.

## Contents

- [Message-Instantiation-Coverage.md](./Message-Instantiation-Coverage.md) -
  what is instantiated today vs. still open, across every in-repo scenario.
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
  and USV Rescue in one pass; shows the task/effect axis distills to two gaps
  (task verbs + payload/effector/weapon typing) with everything else already in
  the standard.
- [RedundancyPass-Walk.md](./RedundancyPass-Walk.md) - confirmation pass over
  route-clearance / companion / urban; mostly redundant, but extracts N1 (an
  area cannot be the subject of a task or report).
- [SourcedScenarios-Walk.md](./SourcedScenarios-Walk.md) - maritime MCM,
  subterranean SubT, and sustainment, taken from the parallel scenario-sourcing
  session (`LLMExperiments/V2Extractions/` + its `OntologyCoverageClustering.md`
  handoff). Corroborates P1/X1/N2/Y and adds G1-G10, incl. a proposed generic
  Detection Report that resolves the sensor-report (Y) series.
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
- Worked message examples: the three `ASX Sample * Messages.xlsx` workbooks
  (created 2026-06-10).
- Base standard classes: `Ontology/C2SIM.rdf`, `Ontology/C2SIM_SMX.rdf`,
  `Ontology/C2SIM_LOX.rdf`.

Status: uncommitted working-tree notes. Prepared by Paulo Barthelmess (Hyssos).
