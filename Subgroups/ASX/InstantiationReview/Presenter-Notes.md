# Presenter Notes - ASX Instantiation Review

Talking points for presenting `ASX-Instantiation-Findings.pptx` (22 slides) to
the sub-group. Grouped by section, not one line per slide. Keep the framing
**constructive**: this is a review that *builds on* the proposed extension and
Elizabeth's message work - it is not a critique of incomplete work. Everything is
a proposal; nothing has been applied to the model or the workbooks.

## Opening (title + method)
- "We checked the proposed ASX extension bottom-up: for each scenario we tried to
  write the actual messages it needs, using the proposed elements. Where a
  message won't build cleanly, that's a concrete gap."
- One sentence on scope: converted the sample-message workbooks to a diff-able
  format so instantiations can be reviewed in git; the original `.xlsx` are
  untouched.

## State of play + coverage (lead with the numbers - this is the contribution)
- Started from **4** worked instantiations (2 Reports, 2 Orders, **0
  Initialization**) - Elizabeth's baseline. This review drafted **~29 more, to
  ~33** across Init / Order / Report. Slide 3 shows the before/after; slide 4
  ("Scenarios analyzed") shows the 20+ scenarios behind it.
- Say it plainly: Initialization went 0 -> 6, Orders 2 -> 14, Reports 2 -> 13.
  That breadth - not any single message - is what surfaced the to-define items.
- Walked scenarios across Init/Order/Report; then integrated a parallel
  scenario-sourcing effort (Cooperative MCM, SubT, sustainment + nine documented
  missions) that grounded every gap in a real mission.
- The one contributed, human-authored scenario (CASEVAC) had no messages; we
  walked it end to end (Init -> Orders -> Reports).

## The two tracks are at different stages (say this early - it explains a lot)
- The OWL model (`CSIM_ASX.rdf`, last updated Jan) and the spreadsheets
  (updated Jun) evolved separately, so autonomy and sensors are each defined
  three different ways. Reconciling them is one of the first decisions.

## The three foundational decisions (the core of the talk)
- **P1 - a UAV/UGV is typed two incompatible ways.** The proposed `Robot` class
  tree runs parallel to the existing SMX `Platform` tree, both under
  `ActorEntity`. Pick `Robot` and you lose the Platform machinery; pick
  `Aircraft`/`Vehicle` and the ASX classes go unused.
- **P7 - a swarm isn't yet taskable or able to report.** `Swarm` derives from
  `PhysicalEntity` (an inert object), but orders and reports need an
  `ActorEntity`. The fix is already in the base standard: derive from
  `CollectiveEntity`.
- **P2 - a sensor has no agreed representation** (class vs enum vs equipment).
- Land the point: "all three are entity-typing decisions - so Initialization,
  not Reports, is where the model has to be settled."

## Why so much is still to define: the model has a taxonomy, attributes just starting
- The v0.0.1 baseline is 15 classes, 1 object property, **0 datatype properties**.
  It is a taxonomy of *things*; the layer that says what you actually *send*
  hadn't been built yet. v0.0.3 begins it (datatype properties for the Video
  Detection Report). Most "gaps" are simply not-yet-built - which is why writing
  messages surfaces them.

## The good news (say this - it lowers the temperature)
- Much of what's "missing" is **re-adopt, not invent**:
  - The sensor-measurement report is prior art in C2SIM's own **BML** lineage -
    `WhoMeasuredType` (value + unit + phenomenon + sensor + time + place).
  - Rules of engagement, desired effects, routes, resources, maritime vessels,
    and a neutral hostility value (`smx#NEUTRL`) **already exist** in the base
    standard - we verified this against the RDF, not from memory. (Command
    authorization of an engagement does *not* exist - that is the W1 gap;
    `AuthorizationHeader` is only message-sender authentication.)
  - The **task-verb vocabulary already exists**: LOX has 446 `TaskActionCode`
    verbs (engage, attack, breach, construct, clear, transport, resupply,
    rescue, recover, neutralize, escort, follow, recce, patrol, sweep, deceive).
    So the task/effect work is not "invent verbs" - it is the payload/effector/
    weapon *typing* plus a couple of residual semantics.

## Decisions (the ask)
- ~22 decisions, listed in the log. Present the grouping, not all 22:
  - **Structure first:** UAV/robot typing (Q-A), swarm -> CollectiveEntity (Q-B),
    one sensor model (Q-C), one autonomy vocabulary (Q-D).
  - **Then content types:** generic detection report (re-adopt BML), rationale
    report, robot-to-robot, engagement authority, payload/effector/weapon typing
    (the task verbs already exist in LOX), area as a task/report subject, and
    the rest.

## Close: where the ball is
- Sourcing is essentially complete - every proposed concept is now grounded in a
  real mission (one nice-to-have left: a dedicated autonomous-CASEVAC mission).
- The remaining work - build the attribute layer, reconcile the tracks, make the
  ~22 decisions - is ours. More scenarios won't fill it.

## Things to say carefully (avoid overclaiming)
- Don't say "the model is wrong" - say "these are decisions the model defers, and
  instantiation forces them."
- The MUTT-derived scenarios are LLM-generated; the CASEVAC scenario is
  human-authored; the sourced missions are from real papers (two carry fidelity
  caveats - EW and the robotic breach - noted in the records).
- If asked whether we changed anything: **no** - `.xml` copies only, `.xlsx`
  untouched, nothing applied to the OWL. All proposals.
