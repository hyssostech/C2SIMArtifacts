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

## Source of truth

- Proposed OWL model: `Subgroups/ASX/Proposed Extension/CSIM_ASX.rdf`
  (last updated 2026-01-20).
- Attribute concepts: `Subgroups/ASX/Proposed Extension Working Materials/ASX Concept Mapping.xlsx`.
- Worked message examples: the three `ASX Sample * Messages.xlsx` workbooks
  (created 2026-06-10).
- Base standard classes: `Ontology/C2SIM.rdf`, `Ontology/C2SIM_SMX.rdf`,
  `Ontology/C2SIM_LOX.rdf`.

Status: uncommitted working-tree notes. Prepared by Paulo Barthelmess (Hyssos).
