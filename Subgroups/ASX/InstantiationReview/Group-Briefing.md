# ASX Instantiation Review - Briefing for the Sub-group

One-page bearings on what this review is, what it found, and what the group needs
to decide. Detail is in the other files in this folder; the deck
(`ASX-Instantiation-Findings.pptx`, 22 slides) is the presentation version.

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
- Took the instantiation from **4 worked message instances (0 Initialization) to
  ~33** across Init / Order / Report (~29 drafted in this review), spanning 20+
  scenarios - all on the branch, pending group review.
- Produced a 22-slide findings deck and a full issues/decisions log.

## What we found (headline)

This is an early WIP ontology, so the findings are things *still to be defined*,
not defects. Three of them are foundational typing decisions worth settling
first, because Initialization is hard to build cleanly until they are settled:
- **P1** - a UAV/UGV is currently typed two ways: the proposed ASX `Robot` tree
  runs parallel to the existing SMX `Platform` tree (v0.0.3 declares both).
- **P7** - a swarm derives from `PhysicalEntity`, so it isn't yet taskable / able
  to report; deriving it from the existing `CollectiveEntity` would fix that.
- **P2** - a sensor's representation isn't settled yet (class vs enum vs equipment).

Recurring themes (all normal for a v0.0.x model being built out):
- The OWL is still mostly a **taxonomy of things**; the attribute layer that says
  what you actually *send* is only just starting (v0.0.1 had 0 datatype
  properties; v0.0.3 begins it for the Video Detection Report).
- **Autonomy and sensors are each described three different ways** - the OWL and
  the spreadsheet tracks are at different stages and need reconciling.
- The **report model started from a camera**; extending it to other sensors
  (CBRN/EW/measurements) is still to do.
- Not yet defined: **autonomous engagement authority**, **robot-to-robot
  coordination**, **"explainable reasons"**, and an **area** as the subject of a
  task/report.

## Where the model is now (v0.0.3)

Michael's v0.0.3 shows the model moving in this direction: it begins the
attribute layer and folds the Video Detection Report into the OWL. It also brings
the P1 typing question to a head rather than settling it - v0.0.3 now declares
*both* the Robot-tree and the SMX-Vehicle-tree names, so the group still has to
pick one. Still to define: a taskable collective (the `Swarm` class was dropped;
`CollecticeRoboticSystem` is still non-actor), the broader attribute set, and the
new content types above - plus two typos to fix. (Detail in section 9 of the log.)

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
  property/message layer, reconciling the two tracks, and making the ~22
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
