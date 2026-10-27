# ASX Message-Instantiation Review Notes

These are **review / analysis notes**, contributed for discussion. They are
**not** authoritative model changes; the proposed ASX OWL (`CSIM_ASX.rdf` /
v0.0.4, now on `main`) is not changed by these notes - the only model edits
are the typo fixes in PR #9. The intent is to add
*coverage* (walking scenarios into concrete message instances) and to surface
*problems* that instantiation reveals in the proposed ASX elements - phrased
as questions for the sub-group, not as decisions.

How the message work is stored (decision S4 in the log): Elizabeth's binary
`.xlsx` sample-message workbooks are **left untouched** (binary workbooks cannot
be merged if two people edit them). Instead, this review works on diff-able
**SpreadsheetML `.xml` copies** of the three workbooks - in `Subgroups/ASX/
Proposed Extension Working Materials/` - and that is where all the instantiation
tabs live. The `.xml` were verified cell-for-cell against the originals; nothing
in the `.xlsx` changed.

## Start here

- [Group-Briefing.md](./Group-Briefing.md) - one-page bearings for the sub-group:
  what this is, what was found, the ~24 decisions, and where the ball is now.

**Status (2026-10-14).** The sub-group has decided the three structural items
the review put first: **P1** - ASX autonomy is a role/facet on the existing
`Platform` subtree; **P7** - the collective/Swarm derives from
`CollectiveEntity`; **P2** - sensors are being reworked on existing standards.
The live model is now **v0.0.4** (`Ontology/C2SIM_ASX-v004.rdf`, merged from `michael_d` into `main` in #11,
2026-08-13), which already carries the P1 shape on the Vehicle side
(`hasControlMode` on `smx#Vehicle`) and placeholders for P2, but not yet P7.
The log's section 10 has the v0.0.4 reconciliation, the decisions, and the
implementation order they imply; the deck's structural slides show the decided
state and the residual.

## Contents

- [Message-Instantiation-Coverage.md](./Message-Instantiation-Coverage.md) -
  the pre-walk `.xlsx` baseline snapshot (2026-06-10) that motivated the review;
  the current instantiation state is tracked in the log (C1-C9).
- [Initialization-Walk.md](./Initialization-Walk.md) - a proposed walk of the
  three named-but-not-yet-filled Initialization scenarios
  (`UAV with Video Init`, `UAV Patrol Initialization`, `Swarm Initialization`),
  mirroring the sheet columns, with the problems each one exposes.
- [CASEVAC-Walk.md](./CASEVAC-Walk.md) - end-to-end walk of the CASEVAC
  contributed scenario (Init + Order + robot-to-robot coordination + Reports),
  surfacing X1 (no robot-to-robot content type) and X2 (no explainability
  element) as the highest-value gaps it exposes.
- [NonVideoSensors-Walk.md](./NonVideoSensors-Walk.md) - CBRN / EW / GPR report
  instantiations that stress the sensor model; shows the media-based
  `Video Detection Report` model does not generalize to non-imaging sensors
  (Y1-Y5).
- [Swarm-Walk.md](./Swarm-Walk.md) - swarm detection report + coordination
  order; exercises P7 (a swarm not yet taskable/able to report as modeled) and shows
  membership/command already exist in the base standard (P8 narrowed; Z1/Z2 residuals).
- [FireSupport-Walk.md](./FireSupport-Walk.md) - armed engagement + BDA;
  opens the task/effect axis and surfaces W1 (no link between autonomy level and
  authority to take a lethal action). ROE already exists; command authorization
  of fires is part of the W1 gap.
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
  sourcing track's nine sourced missions (`Documents-Found.md`). Moves the
  validation holes to evidenced and captures concrete report schemas to adopt -
  most importantly BML `WhoMeasuredType`, prior art in C2SIM's lineage for the
  measurement report (Q-Q).
- [DroneWarfare-LIRC-OPFOR-Walk.md](./DroneWarfare-LIRC-OPFOR-Walk.md) - the
  SME-directed drone-warfare thread (Morris 2018 LIRC baseline, its 2022-2024
  threat/TTP update, and the Rosenberg JPMRC-AK 24-02 OPFOR commercial-sUAS targeting
  run). Lands on W1/Q-K: the LIRC kill-box / weapons-control mechanism is a concrete
  candidate answer to autonomous engagement authority (G14, decision Q-W), unifying it
  with N1/Q-M; adds G15-G19 (graded/phase authority, loitering-munition typing,
  counter-UAS, adversarial EW, target-list). 5 tabs added to the `.xml`.

Proposed slices (future work - scoped and grounded, but **not** performed; no
workbook tabs). Three independent items, kept as separate documents because
the items are independent - the first two suggested by Curt, the third from a
question raised in October:

- [Sensor-Characterization-Slice.md](./Sensor-Characterization-Slice.md) - is
  sensor characterization worth an extension of its own, built on existing
  standards? Both halves hold up: 15 open findings + 6 decisions already cluster
  here, and a sensor model must answer four separable questions (device /
  capability / observation / configuration) where ASX has a partial first and
  nothing else. Candidates surveyed: SOSA/SSN + the SSN-System capability module
  (tier 1), SensorML and ISO 19156 (tier 2), STANAG 4586 / MISB / IEEE 1451 and
  DIS (tier 3). Adds G20-G22, decision Q-Y (log section 6l).
- [DIS-Enumerations-Slice.md](./DIS-Enumerations-Slice.md) - what the DIS
  enumeration materials offer ASX **in general, as inspiration rather than as
  codes to use**. C2SIM entities already carry the seven-field DIS record, so
  that question is settled; what is open is whether ASX learns from the reasoning
  behind it. The mass of data reduces to four table shapes over a septuplet; at
  least eight of the nine Entity Kinds bear on open ASX findings (several telling
  ASX that something it treats as an afterthought - the comms relay, environment
  *conditions*, expendability, class of supply - deserves first-class typing);
  and five vocabulary-governance principles apply to ASX's own code lists without
  touching any DIS content. Counterweight recorded: DIS boundaries were drawn for
  a simulation, not a commander, and not all will survive translation. Adds
  G23-G29, decision Q-Z (log section 6m).
- [STANAG4817-CATL-Slice.md](./STANAG4817-CATL-Slice.md) - what the NATO
  multi-domain unmanned-systems C2 standard (STANAG 4817) and its public basis
  CATL (CMRE's Collaborative Autonomy Tasking Layer) offer ASX's *coordination*
  content. Caveat first: AEP-4817 is not public, so the concrete claims are
  CATL claims. Grounding: C2SIM already has the request / acknowledge / status
  triad and lacks exactly the multi-node machinery - control handover, a
  control-station entity, allocation among candidates, state synchronization.
  Bears on X1/Q-G, G3/Q-P, Z1/Q-J, G13/Q-V, Q-O; does not touch P1 / P2 or the
  engagement-authority thread. States the layering point (commander-to-system vs
  station-to-vehicle) as a round-trip requirement. Adds G30-G33, decision Q-AA
  (log section 6n).

- [Documents-Needed.md](./Documents-Needed.md) / [Documents-Found.md](./Documents-Found.md)
  - the sourcing brief and the sourcing track's point-by-point response.
- [Issues-And-Comments-Log.md](./Issues-And-Comments-Log.md) - running,
  consolidated log of every issue/comment found, with severity and status;
  the findings deck is generated from it. Section 9 = the v0.0.3 reconciliation
  (July); section 10 = the v0.0.4 reconciliation + the P1 / P2 / P7 decisions
  (October).
- `ASX-Instantiation-Findings.pptx` - findings presentation for the ASX
  sub-group. Regenerate/edit it via `build_findings_deck.py` (the `.pptx` is a
  zipped-XML binary git cannot merge, so the Python generator is the diff-able
  source). Requires `python-pptx`.

## Source of truth

- Proposed OWL model: **v0.0.4** on `main` (Michael Dembach's `michael_d`
  branch, merged in #11 on 2026-10-27; the branch is kept locked read-only as
  the record of his work, tagged `archive/michael_d-v0.0.4`)
  (`Ontology/C2SIM_ASX-v004.rdf`, 2026-08-13; v0.0.3 archived at
  `Ontology/Archive/C2SIM_ASX-v003.rdf`; derived `Derived products/ASX_Schema.xsd`).
  Applied on top of it: PR #9 (merged into `main` 2026-10-27) fixes
  the typos O1 / O3-O6 (e.g. `CollectiveRoboticSystem`, `hasAutonomousParameters`)
  and removes two duplicate Concept Mapping rows; the review docs already use the
  corrected names where they refer to the live model.
  The v0.0.1 file `Subgroups/ASX/Proposed Extension/CSIM_ASX.rdf` (2026-01-20)
  still exists on every branch and is the one the early walks cite.
- Attribute concepts: `Subgroups/ASX/Proposed Extension Working Materials/ASX Concept Mapping.xlsx`
  (the v0.0.4 copy, now on `main`, carries an "ASX 0.0.4" status column per attribute).
- Worked message examples (Elizabeth's, untouched): the three
  `ASX Sample * Messages.xlsx` workbooks (created 2026-06-10).
- Review working copies (diff-able, where the instantiation tabs live): the three
  `ASX Sample * Messages.xml` in `Proposed Extension Working Materials/`.
- Base standard classes: `Ontology/C2SIM.rdf`, `Ontology/C2SIM_SMX.rdf`,
  `Ontology/C2SIM_LOX.rdf`.

Status: instantiation review committed on branch `asx-diffable-spreadsheets`
(draft PR #3 on the fork). Prepared by Paulo Barthelmess (Hyssos).
