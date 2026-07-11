# ASX Instantiation Review - Briefing for the Sub-group

One-page bearings on what this review is, what it found, and what the group needs
to decide. Detail is in the other files in this folder; the deck
(`ASX-Instantiation-Findings.pptx`, 20 slides) is the presentation version.

## What this is

An independent, bottom-up check of the proposed ASX extension. For each scenario
we tried to write the actual C2SIM Initialization / Order / Report **messages**
it requires, using the proposed ASX elements. Where a message cannot be built
cleanly, that is a concrete gap. **Everything here is a proposal** - nothing has
been applied to the OWL model or to Elizabeth's message workbooks.

## What was done

- Converted the three ASX sample-message workbooks to a **diff-able** format
  (SpreadsheetML `.xml`) so instantiations can be reviewed/merged in git;
  Elizabeth's `.xlsx` are left untouched.
- Walked scenarios into concrete message tabs across Init/Order/Report: the named
  Init cases, CASEVAC, sensing (video / CBRN / EW / GPR), swarm, fire support,
  logistics / engineering / rescue, maritime MCM, subterranean SubT, sustainment,
  plus a redundancy pass.
- Integrated a parallel scenario-sourcing effort that **grounded every gap in a
  real mission** (nine sourced missions).
- Produced a 20-slide findings deck and a full issues/decisions log.

## What we found (headline)

Three structural **blockers** - each stops a message from being built:
- **P1** - a UAV/UGV is typed two incompatible ways: the proposed ASX `Robot`
  tree runs parallel to the existing SMX `Platform` tree.
- **P7** - a swarm derives from `PhysicalEntity`, so it cannot be tasked or send a
  report; it should derive from the existing `CollectiveEntity`.
- **P2** - a sensor has no agreed representation (class vs enum vs equipment).

Recurring themes:
- The OWL is a **taxonomy of things with almost no message attributes** (0
  datatype properties); the layer that says what you actually *send* was never
  built.
- **Autonomy and sensors are each defined three different ways** - the OWL track
  (Jan) and the spreadsheet track (Jun) drifted apart.
- The **report model was built around a camera** and does not generalize to other
  sensors (CBRN/EW/measurements).
- No model yet for **autonomous engagement authority**, **robot-to-robot
  coordination**, **"explainable reasons"**, or an **area** as the subject of a
  task/report.

## The good news

Much of what is "missing" is already present or has prior art - so several
decisions are *re-adopt*, not *invent*:
- The **measurement/detection report** is prior art in C2SIM's own **BML**
  lineage (`WhoMeasuredType`: value + unit + phenomenon + sensor + time + place).
- Rules of engagement, order authorization, desired effects, targets, routes,
  resources, maritime vessels, and neutral affiliation **already exist** in the
  base standard.

## What the group needs to decide

The review distills to ~22 decisions (Q-A..Q-V in `Issues-And-Comments-Log.md`),
in two groups:
- **Model structure (decide first):** UAV/robot typing (Q-A), swarm ->
  CollectiveEntity (Q-B), one sensor model (Q-C), one autonomy vocabulary (Q-D).
- **New content types / attributes:** generic detection report with confidence,
  rationale report, robot-to-robot + cross-cue, engagement authority,
  payload/effector/weapon typing (the task verbs already exist in LOX),
  area-as-subject, area-coverage goal, denied-comms
  + relay, formation geometry, capability self-report, and more.

## Status and next step

- **Sourcing is essentially complete** - every proposed concept is now grounded in
  a real mission (one nice-to-have remains: a dedicated autonomous-CASEVAC
  mission).
- **The ball is on the modeling side.** The remaining work - building the OWL
  property/message layer, reconciling the drifted tracks, and making the ~22
  decisions - is not a document problem; more scenarios will not fill it. It needs
  the sub-group's decisions and modeling.

## Where to look

| Artifact | File |
|---|---|
| Findings deck (present this) | `ASX-Instantiation-Findings.pptx` |
| Findings + decisions + evidence | `Issues-And-Comments-Log.md` |
| Per-scenario message instantiations | the three `ASX Sample *.xml` workbooks |
| Why the gaps exist / sourcing brief | log section 8; `Documents-Needed.md` / `Documents-Found.md` |
| Review branch / PR | `asx-diffable-spreadsheets` (draft PR #3 on the fork) |
