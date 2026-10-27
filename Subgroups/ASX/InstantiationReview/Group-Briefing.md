# ASX Instantiation Review - Briefing for the Sub-group

One-page bearings on what this review is, what it found, and what the group needs
to decide. Detail is in the other files in this folder; the deck
(`ASX-Instantiation-Findings.pptx`, 23 slides) is the presentation version - its
last three slides ("How to use this material" / the finding-ID decoder ring /
"Where to dig deeper") are the navigation aids for everything below, and every
slide carries speaker notes with the talk track.

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
  the SME drone-warfare thread (LIRC baseline / 2024 update / OPFOR targeting),
  plus a redundancy pass.
- Integrated a parallel scenario-sourcing effort that **grounded every gap in a
  real mission** (nine sourced missions).
- Took the instantiation from **4 worked message instances (0 Initialization) to
  ~38** across Init / Order / Report (~34 drafted in this review), spanning 20+
  scenarios - all on the branch, pending group review.
- Produced a 23-slide findings deck (a one-slide summary and process +
  contributions slides up front; a reading guide by time budget, a finding-ID
  decoder ring, and a "Where to dig deeper" reference map at the end; a
  per-slide "Dig deeper" pointer to the doc behind each finding; and speaker
  notes with the talk track on every slide) and a full issues/decisions log.

## What we found (headline)

This is an early WIP ontology, so the findings are things *still to be defined*,
not defects. Three of them are foundational typing decisions worth settling
first, because Initialization is hard to build cleanly until they are settled -
**and the sub-group has now settled them** (decisions recorded 2026-10-14):
- **P1** - a UAV/UGV was typed two ways: the proposed ASX `Robot` tree ran
  parallel to the existing SMX `Platform` tree (v0.0.3/v0.0.4 declare both).
  **Decided: ASX autonomy becomes a role/facet on the existing `Platform`
  subtree.** v0.0.4 already has that shape on the Vehicle side (`hasControlMode`
  on `smx#Vehicle`); the `Robot` tree still has to be retired.
- **P7** - a swarm derived from `PhysicalEntity`, so it wasn't taskable / able to
  report. **Decided: derive the collective/Swarm from the existing
  `CollectiveEntity`.** Not yet in v0.0.4.
- **P2** - a sensor's representation wasn't settled (class vs enum vs
  equipment). **Decided in direction: sensors are being reworked based on
  existing standards** (the premise of the sensor-characterization slice);
  v0.0.4 holds placeholders (`SensorTypeCode`, `hasSensorCapability`).

Recurring themes (all normal for a v0.0.x model being built out):
- The OWL is still mostly a **taxonomy of things**; the attribute layer that says
  what you actually *send* is only just starting (v0.0.1 had 0 datatype
  properties; v0.0.3 begins it for the Video Detection Report).
- **Autonomy and sensors are each described three different ways** - the OWL and
  the spreadsheet tracks are at different stages and need reconciling.
- The **report model started from a camera**; extending it to other sensors
  (CBRN/EW/measurements) is still to do.
- Being defined: **robot-to-robot coordination**, **"explainable reasons"**, and an
  **area** as the subject of a task/report. For **autonomous engagement authority**,
  the SME drone-warfare thread now supplies a concrete candidate model - the LIRC
  weapons-control / kill-box construct (G14, decision Q-W) - rather than only naming
  the gap.

## Where the model is now (v0.0.4)

Michael's v0.0.4 (on branch `michael_d`, 2026-08-13; v0.0.3 archived) keeps the
model moving in this direction. It brings five of the spreadsheet attributes
into the OWL (Control Mode, SensorCapability, AutonomousMissionFunction,
Autonomous Parameters, PassengerCapability) plus three empty code lists
(SensorType / VehicleType / AlgorithmType), attaches a per-task autonomy level
to `Task`, fixes the circular import flagged in July, and the Concept Mapping
workbook now tracks per attribute what is "done" in 0.0.4. Against the three
decisions: P1 is half-applied (the facet exists on `Vehicle`; the `Robot` /
`UAV` / `UGV` tree is still declared, and the derived XSD still offers `Robot`
beside `Platform`); P7 is not yet applied (the collective class is still
non-actor, no `Swarm`); P2 has placeholders only. Also still to define: Payload /
Mobility / Swarm Parameters, the new content types above, and four of the six
new properties have no attachment point yet. One typo fixed, three new ones
(`hasAutonomusParameters`, a mis-naming `versionInfo`, the `Operator` comment);
all four open typos (O1, O4-O6) are now fixed in PR #9, pending merge.
(Detail in section 10 of the log; section 9 is the July v0.0.3 record.)

## The good news

Much of what is "missing" is already present or has prior art - so several
decisions are *re-adopt*, not *invent*:
- The **measurement/detection report** is prior art in C2SIM's own **BML**
  lineage (`WhoMeasuredType`: value + unit + phenomenon + sensor + time + place).
- Rules of engagement, desired effects, targets, routes, resources, maritime
  vessels, and a neutral hostility value (`smx#NEUTRL`) **already exist** in the
  base standard. (Command authorization of an engagement does *not* - that is the
  W1 gap; `AuthorizationHeader` is only message-sender authentication.)

## What the group needs to decide

The review distills to ~24 decisions (Q-A..Q-X in `Issues-And-Comments-Log.md`),
in two groups:
- **Model structure (decide first) - now decided:** UAV/robot typing (Q-A:
  autonomy as a facet on the Platform subtree), swarm -> CollectiveEntity (Q-B:
  yes), one sensor model (Q-C: rework on existing standards). One autonomy
  vocabulary (Q-D) is settled in practice by v0.0.4 (`AutonomyLevelCode` is the
  range of both new autonomy properties) and only needs stating.
- **New content types / attributes:** generic detection report with confidence,
  rationale report, robot-to-robot + cross-cue, engagement authority,
  payload/effector/weapon typing (the task verbs already exist in LOX),
  area-as-subject, area-coverage goal, denied-comms
  + relay, formation geometry, capability self-report, and more.

## Status and next step

- **Sourcing is essentially complete** - every gap this review raised is now
  grounded in a real mission (one nice-to-have remains: a dedicated
  autonomous-CASEVAC mission).
- **The structural decisions are made; the ball is on applying them in the
  OWL.** In order: re-parent (and re-spell) the collective class under
  `CollectiveEntity` (P7); retire the `Robot` tree, pick Vehicle-vs-Platform for
  the autonomy facet, and give the new properties a home (P1); run the sensor
  standards survey and re-point `hasSensorCapability` from it (P2); then re-cut
  the Initialization tabs. The remaining ~20 content-type decisions and the
  unbuilt attribute layer (Payload / Mobility / Swarm Parameters) are modeling
  work; more scenarios will not fill it.

## Where to look

| Artifact | File |
|---|---|
| Findings deck (present this) | `ASX-Instantiation-Findings.pptx` |
| Findings + decisions + evidence | `Issues-And-Comments-Log.md` |
| Per-scenario message instantiations | the three `ASX Sample *.xml` workbooks |
| Why the gaps exist / sourcing brief | log section 8; `Documents-Needed.md` / `Documents-Found.md` |
| Review branch / PR | `asx-diffable-spreadsheets` (draft PR #3 on the fork) |
