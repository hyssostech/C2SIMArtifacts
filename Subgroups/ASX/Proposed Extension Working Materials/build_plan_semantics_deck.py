"""Builds ASX-PlanSemantics-Briefing.pptx — walkthrough of the plan-semantics
analysis and proposed module for an audience familiar with C2SIM but new to
autonomous-system behavior semantics. Style follows InstantiationReview/build_findings_deck.py."""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

NAVY   = RGBColor(0x1F, 0x3A, 0x5F)
ACCENT = RGBColor(0x2E, 0x86, 0x9A)
GRAY   = RGBColor(0x33, 0x33, 0x33)
MGRAY  = RGBColor(0x66, 0x66, 0x66)
RED    = RGBColor(0xC0, 0x39, 0x2B)
ORANGE = RGBColor(0xC8, 0x7F, 0x0A)
GREEN  = RGBColor(0x2E, 0x7D, 0x32)
LIGHT  = RGBColor(0xEE, 0xF1, 0xF5)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def slide():
    return prs.slides.add_slide(BLANK)


def box(s, l, t, w, h):
    tb = s.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    return tb, tf


def set_run(r, text, size, color, bold=False, italic=False, font="Calibri"):
    r.text = text
    r.font.size = Pt(size)
    r.font.color.rgb = color
    r.font.bold = bold
    r.font.italic = italic
    r.font.name = font


def header(s, title, kicker=None):
    ln = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.28), Inches(2.2), Pt(3))
    ln.fill.solid(); ln.fill.fore_color.rgb = ACCENT; ln.line.fill.background()
    tb, tf = box(s, 0.55, 0.45, 12.2, 0.9)
    p = tf.paragraphs[0]; set_run(p.add_run(), title, 30, NAVY, bold=True)
    if kicker:
        tb2, tf2 = box(s, 0.6, 1.0, 12.0, 0.35)
        p2 = tf2.paragraphs[0]; set_run(p2.add_run(), kicker, 13, ACCENT, italic=True)


def footer(s):
    n = len(prs.slides._sldIdLst)
    tb, tf = box(s, 0.55, 7.02, 12.2, 0.35)
    p = tf.paragraphs[0]
    set_run(p.add_run(), "C2SIM ASX Sub-group   |   Plan-Semantics Working Brief (DRAFT)   |   July 2026", 9, MGRAY)
    tb2, tf2 = box(s, 12.4, 7.02, 0.7, 0.35)
    p2 = tf2.paragraphs[0]; p2.alignment = PP_ALIGN.RIGHT
    set_run(p2.add_run(), str(n), 9, MGRAY)


def bullets(s, items, top=1.6, left=0.7, width=12.0, height=5.2, size=15, gap=6):
    """items: list of dicts {t: text, lvl: 0/1, b: bold, c: color, i: italic, sz: size}"""
    height = min(height, 6.95 - top)
    tb, tf = box(s, left, top, width, height)
    first = True
    for it in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        lvl = it.get("lvl", 0)
        p.level = lvl
        p.space_after = Pt(it.get("gap", gap))
        prefix = "•  " if lvl == 0 else "–  "
        if it.get("noprefix"):
            prefix = ""
        set_run(p.add_run(), prefix + it["t"], it.get("sz", size - 2 * lvl),
                it.get("c", GRAY), bold=it.get("b", False), italic=it.get("i", False))
    return tb


def panel(s, l, t, w, h, fill=LIGHT, line=None):
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(l), Inches(t), Inches(w), Inches(h))
    sh.fill.solid(); sh.fill.fore_color.rgb = fill
    if line:
        sh.line.color.rgb = line; sh.line.width = Pt(1.25)
    else:
        sh.line.fill.background()
    sh.shadow.inherit = False
    return sh


def panel_text(s, l, t, w, h, title, lines, tcolor=NAVY, fill=LIGHT, size=13, tsize=15):
    panel(s, l, t, w, h, fill=fill)
    tb, tf = box(s, l + 0.15, t + 0.08, w - 0.3, h - 0.16)
    p = tf.paragraphs[0]
    set_run(p.add_run(), title, tsize, tcolor, bold=True)
    for ln in lines:
        p = tf.add_paragraph(); p.space_before = Pt(3)
        if isinstance(ln, tuple):
            txt, col = ln
        else:
            txt, col = ln, GRAY
        set_run(p.add_run(), txt, size, col)


def table(s, rows, top=1.7, left=0.7, width=12.0, col_w=None, size=12, hdr_size=12.5, row_h=0.32):
    n_rows, n_cols = len(rows), len(rows[0])
    shp = s.shapes.add_table(n_rows, n_cols, Inches(left), Inches(top), Inches(width), Inches(row_h * n_rows))
    t = shp.table
    if col_w:
        for i, w in enumerate(col_w):
            t.columns[i].width = Inches(w)
    for ri, row in enumerate(rows):
        for ci, cell_txt in enumerate(row):
            cell = t.cell(ri, ci)
            cell.margin_top = Inches(0.02); cell.margin_bottom = Inches(0.02)
            cell.margin_left = Inches(0.06); cell.margin_right = Inches(0.06)
            tfc = cell.text_frame; tfc.word_wrap = True
            p = tfc.paragraphs[0]
            color = GRAY
            if isinstance(cell_txt, tuple):
                cell_txt, color = cell_txt
            if ri == 0:
                set_run(p.add_run(), cell_txt, hdr_size, WHITE, bold=True)
                cell.fill.solid(); cell.fill.fore_color.rgb = NAVY
            else:
                set_run(p.add_run(), cell_txt, size, color)
                cell.fill.solid()
                cell.fill.fore_color.rgb = WHITE if ri % 2 else LIGHT
    return t


# ---------------------------------------------------------------- 1 TITLE
s = slide()
panel(s, 0, 0, 13.333, 7.5, fill=NAVY)
tb, tf = box(s, 1.0, 2.2, 11.3, 1.8)
p = tf.paragraphs[0]
set_run(p.add_run(), "Beyond Tasking:", 40, WHITE, bold=True)
p = tf.add_paragraph()
set_run(p.add_run(), "Extending C2SIM Plans for Autonomous-System Behavior", 34, WHITE, bold=True)
tb, tf = box(s, 1.0, 4.2, 11.3, 1.6)
p = tf.paragraphs[0]
set_run(p.add_run(), "The LOX Plan construct, behavior trees and BDI, and a proposed ASX plan-semantics module", 18, LIGHT)
p = tf.add_paragraph(); p.space_before = Pt(14)
set_run(p.add_run(), "C2SIM ASX Sub-group  —  working brief for discussion  —  DRAFT, July 2026", 14, ACCENT)
p = tf.add_paragraph(); p.space_before = Pt(4)
set_run(p.add_run(), "Companion artifacts: Plan-Semantics-Analysis.md  +  ASX-PlanSemantics-Draft.ttl (v0.0.3)", 12, MGRAY)

# ---------------------------------------------------------------- 2 THE CONCERN
s = slide()
header(s, "The concern in one slide", "Why plan semantics — and why now")
bullets(s, [
    {"t": "C2SIM tasking tells a unit WHAT to do (task verb, WHO/WHEN/WHERE). A human crew fills in every decision the order leaves open.", "sz": 16},
    {"t": "A robotic/autonomous system has no crew: every decision the order leaves open must either be transmitted, or surrendered to opaque onboard behavior.", "sz": 16},
    {"t": "The ASX scenario corpus keeps demanding the same missing pieces:", "b": True, "sz": 16},
    {"t": "CASEVAC (contributed): “replans route if threat or obstacle is encountered … handled by autonomy” — contingent behavior, explained to the operator", "lvl": 1},
    {"t": "MDARS persistent watch (fielded system): a standing patrol that is never “complete” — classic orders have no such thing", "lvl": 1},
    {"t": "Urban C-UAS (Corona & Biagini 2019): “UAVs must wait for human confirmation before taking suggested actions” — engagement authority as data", "lvl": 1},
    {"t": "The question for this brief:", "b": True, "sz": 16},
    {"t": "Can C2SIM's existing Plan construct carry the semantics autonomy frameworks actually execute — behavior trees, BDI goals — or do we need something new?", "lvl": 1, "c": NAVY, "b": True},
])
footer(s)

# ---------------------------------------------------------------- 3 REFRESHER CORE
s = slide()
header(s, "Refresher: what C2SIM tasking says today", "Core standard (SISO C2SIM 1.0.x) — no Plan class here")
bullets(s, [
    {"t": "OrderBody → Task: exactly one TaskActionCode (WHAT) and one PerformingEntity (WHO); optional times (WHEN), location (WHERE); optional DesiredEffectCode (WHY).", "sz": 15},
    {"t": "Sequencing between tasks — two idioms only:", "b": True, "sz": 15},
    {"t": "ActionTemporalRelationship: 18 Allen-style codes (STREND = “starts after end of”, concurrency, duration-offset variants)", "lvl": 1},
    {"t": "RelativeTime: anchor a start time to an Event (incl. TaskStart / TaskEnd) plus an offset", "lvl": 1},
    {"t": "Execution feedback — TaskStatus report: TASKPEND, TASKSTRT, TASKINPRG, TASKCMPLT, TASKABRT.", "sz": 15},
])
panel_text(s, 0.7, 4.5, 12.0, 1.15, "Notice what is NOT here", [
    ("No failure status (a task completes or is aborted — “tried and did not succeed” is unsayable).  No conditions over world state.  No branching.  No loops.  No goals.", RED),
], tcolor=RED, size=14)
bullets(s, [
    {"t": "Two under-used core hooks that become load-bearing later: FIPA-style CommunicativeActTypeCode (Agree, Confirm, Refuse …) and the Order-vs-Request deontic split.",
     "i": True, "c": MGRAY, "sz": 13},
], top=5.9, height=0.9)
footer(s)

# ---------------------------------------------------------------- 4 THE LOX PLAN
s = slide()
header(s, "The construct you may not know: the LOX Plan", "Land Operations Extension — and it is more than a task container")
panel_text(s, 0.7, 1.65, 5.9, 2.5, "PlanBody  (a DomainMessageBody)", [
    "hasPlanPhase 0..*  — the phases",
    "isToBeExecutedNow (exactly 1)",
    " ",
    "PlanPhase  (recursive via hasSubPhase)",
    "hasPlanPhaseTrigger — exactly 1",
    "hasPlanPhaseCompletionCondition — exactly 1",
    "hasTaskReference 0..* — the tasks",
], size=13.5)
panel_text(s, 6.85, 1.65, 5.85, 2.5, "Trigger types (when a phase starts)", [
    "EventTrigger — at the time of an Event",
    "OnOrderTrigger — on an ExecutePlanPhase task",
    "PriorPhaseCompletionTrigger — when another phase completes (→ sequences)",
    " ",
    "Completion codes (when it counts as done)",
    "AllTasksComplete   OneTaskComplete   OtherOrderReceived",
], size=13.5)
panel_text(s, 0.7, 4.4, 12.0, 1.5, "The key observation", [
    ("This is not a task list. Triggers + completion conditions + recursive decomposition = a rudimentary REACTIVE EXECUTION model.", NAVY),
    ("That makes the Plan construct — not Order/Task — the natural chassis for autonomy semantics.", ACCENT),
], tcolor=NAVY, size=15)
bullets(s, [
    {"t": "Also in LOX: ManeuverWarfareTask adds RuleOfEngagement, plus JC3IEDM task relations ALT (“is an alternative to”) and HASPRV (“provisional sub-action”) — contingency LABELS with no activation semantics.",
     "i": True, "c": MGRAY, "sz": 13},
], top=6.05, height=0.85)
footer(s)

# ---------------------------------------------------------------- 5 BT + BDI PRIMER
s = slide()
header(s, "How autonomous systems specify behavior", "Two dominant mechanisms — 60 seconds each")
panel_text(s, 0.7, 1.65, 5.9, 4.3, "Behavior Trees (ROS 2 Nav2, Spot SDK …)", [
    "A tree of control-flow nodes over primitive actions:",
    "  Sequence — children in order, halt on failure",
    "  Fallback/Selector — try alternatives until one succeeds",
    "  Parallel — concurrent, succeed-on-all / succeed-on-one",
    "  Decorators — retry N times, loop, timeout, invert",
    "  Condition leaves — guards over world state",
    " ",
    ("Every node returns Success / Failure / Running.", NAVY),
    ("FAILURE is the engine of the whole model: it is what", NAVY),
    ("selects alternatives and drives recovery.", NAVY),
], size=13.5)
panel_text(s, 6.85, 1.65, 5.85, 4.3, "BDI agents (FIPA lineage)", [
    "Beliefs — the agent's world model",
    "Desires/Goals — end states: achieve once, or MAINTAIN",
    "Intentions — goals committed to, pursued via plans",
    " ",
    "A plan library holds alternative recipes per goal;",
    "each plan carries a CONTEXT CONDITION deciding",
    "when it applies (primary / degraded / contested …).",
    " ",
    ("Goal-directed tasking: transmit the end state and", NAVY),
    ("constraints; the system chooses the procedure.", NAVY),
], size=13.5)
bullets(s, [
    {"t": "The subgroup's own standards survey (Reference Materials) recommends modeling BT/HTN concepts directly and using FIPA/BDI for the goal layer, anchored to IEEE 1872.1/.2.",
     "i": True, "c": MGRAY, "sz": 12.5},
], top=6.1, height=0.8)
footer(s)

# ---------------------------------------------------------------- 6 WHAT MAPS
s = slide()
header(s, "Correlation: a surprising amount already maps", "LOX Plan vs. behavior-tree concepts")
table(s, [
    ["Behavior-tree concept", "LOX Plan analog", "Fidelity"],
    ["Composite node", "PlanPhase with subphases (native recursion)", ("good", GREEN)],
    ["Sequence", "PriorPhaseCompletionTrigger chains", ("structural only — breaks once failure exists", ORANGE)],
    ["Parallel, succeed-on-all", "phase + AllTasksComplete", ("good (no straggler-cancel rule)", GREEN)],
    ["Parallel, succeed-on-one", "phase + OneTaskComplete", ("good (same caveat)", GREEN)],
    ["Action leaf", "Task referenced from a phase", ("good", GREEN)],
    ["Entry gating", "EventTrigger (a temporal anchor, not runtime detection)", ("partial", ORANGE)],
    ["External preemption", "OtherOrderReceived / OnOrderTrigger", ("partial — human-initiated only", ORANGE)],
], top=1.65, col_w=[4.0, 5.6, 2.4], size=12.5, row_h=0.42)
panel_text(s, 0.7, 5.35, 12.0, 1.3, "And on the BDI side", [
    "Plan recipe = PlanBody (good).  Plan triggering = EventTrigger/OnOrderTrigger (good).  Performatives already in core (good).",
    ("Beliefs: C2SIM reports are belief updates — adequate as-is; the belief store belongs to the executing system.", MGRAY),
], size=13)
footer(s)

# ---------------------------------------------------------------- 7 WHAT IS MISSING
s = slide()
header(s, "What is missing — seven precisely enumerable gaps", "Each one demanded by scenarios already in the ASX corpus")
table(s, [
    ["#", "Missing semantics", "Scenario moment that demands it"],
    ["1", ("Failure as an outcome", RED), "everything downstream: nothing can fail today, so nothing can recover"],
    ["2", ("Fallback / alternative branching", RED), "CASEVAC: replan route on IED report; CBRN: backtrack, replan, abort after 3 attempts"],
    ["3", ("Guards over world state", RED), "MUTT: maintain comms continuously; relocate if position compromised"],
    ["4", ("Loops / standing tasks", RED), "MDARS standing watch; MCM revisit every 8–24 h; route-clearance repeat"],
    ["5", ("Goals distinct from procedure", RED), "MCM: neutralize mines (achieve) vs. keep sea lane usable (maintain)"],
    ["6", ("Plan selection by context", RED), "Sustainment: routine distribution vs. contested resupply for the same goal"],
    ["7", ("Intention & rationale reporting", RED), "CASEVAC: “explainable reasons” for changes; DroneResponse explanation schema"],
], top=1.65, col_w=[0.5, 3.9, 7.6], size=12.5, row_h=0.5)
bullets(s, [
    {"t": "These align 1:1 with the sub-group's open decision-log items: W1/Q-K (engagement authority — flagged as the central policy gap), X2 (explainability), Q-N (coverage goals), Q-D (graded autonomy), N2 (standing tasks), X6 (re-tasking).",
     "c": NAVY, "sz": 13.5},
], top=5.75, height=1.0)
footer(s)

# ---------------------------------------------------------------- 8 FEASIBILITY
s = slide()
header(s, "Feasibility: extend, don't fork", "Every mechanism needed is an idiom the standard already uses on itself")
bullets(s, [
    {"t": "Open trigger hierarchy — LOX added 3 PlanPhaseTrigger subclasses; ASX can add more (same pattern).", "sz": 15},
    {"t": "Open code lists — SMX added 25 DesiredEffectCodes; LOX added 446 TaskActionCodes; adding TASKFAILD follows precedent exactly.", "sz": 15},
    {"t": "Subclass-and-restrict — ManeuverWarfareTask ⊑ Task is the sanctioned enrichment pattern; AutonomousPlanPhase ⊑ PlanPhase does the same.", "sz": 15},
    {"t": "New report contents — SMX ObservationReportContent is the template for status/rationale reports.", "sz": 15},
    {"t": "Verdict: an additive ASX module importing LOX. No core/LOX changes. No standalone ontology.", "b": True, "c": GREEN, "sz": 16},
])
panel_text(s, 0.7, 4.85, 12.0, 1.85, "The honest qualification (from our adversarial review)", [
    ("REPORTING constructs degrade gracefully — a legacy consumer that ignores them loses information, not safety.", GRAY),
    ("GATING constructs (triggers, guards, timeouts) are mandatory-to-understand: ignoring a HumanApprovalTrigger would fire an engagement phase WITHOUT its human gate.", RED),
    ("Module rule: unknown trigger ⇒ fail closed (never execute, report inability); gated plans only to consumers that negotiated the module.", NAVY),
], tcolor=ORANGE, size=13)
footer(s)

# ---------------------------------------------------------------- 9 MODULE AT A GLANCE
s = slide()
header(s, "The proposed module at a glance", "asx/plan v0.0.3 draft - OWL (Turtle) + 19 normative execution rules")
panel_text(s, 0.7, 1.65, 3.9, 4.35, "New triggers (⊑ PlanPhaseTrigger)", [
    "StateConditionTrigger — fires on a world-state predicate",
    "CompositeTrigger — ALL / ANY over sub-triggers",
    "HumanApprovalTrigger — approval gate",
    "OnPhaseFailureTrigger — fires when a named phase FAILS",
    "ParentPhasePolicyTrigger — parent-managed subphases",
], size=12.5)
panel_text(s, 4.75, 1.65, 3.9, 4.35, "Enriched plan constructs", [
    "AutonomousPlanPhase ⊑ PlanPhase:",
    "  failure policy + fallback ref",
    "  guards, timeout, repetition,",
    "  per-phase autonomy level,",
    "  phase products, goal link",
    "AutonomousPlanBody ⊑ PlanBody:",
    "  inline Goals + context conditions",
    "Condition: 16 typed, negatable predicates",
    "Goal: achieve / maintain end states",
], size=12.5)
panel_text(s, 8.8, 1.65, 3.9, 4.35, "Reports & verbs", [
    "PlanExecutionStatusContent — which phase, what outcome, which goal (intention)",
    "PlanDeviationReportContent — what changed and WHY (rationale + confidence)",
    "Code additions: TASKFAILD;",
    "ConfigureAutonomy, Suspend/Resume/AbortPlanExecution, OverrideAction, AchieveGoal",
], size=12.5)
panel_text(s, 0.7, 6.15, 12.0, 0.75, "", [
    ("Layering: C2SIM core -> SMX -> LOX -> asx/plan (owl:imports).  Everything is optional on top of a plain LOX plan; OWL vocabulary + rules R1-R19 together are the proposal.", NAVY),
], size=13)
footer(s)

# ---------------------------------------------------------------- 10 CONDITIONS & TRIGGERS
s = slide()
header(s, "Highlight 1 — Conditions and triggers", "The guard-node vocabulary, kept deliberately small")
bullets(s, [
    {"t": "Condition = predicate code + typed parameters (subject/object refs, threshold value/duration) + isNegated. Machine-checkable; free text is display-only.", "sz": 14.5},
    {"t": "Predicates from the scenario corpus: HazardOnRoute, CommsAvailable/Denied, ThreatDetectedInArea, AreaCoverageAchieved (Q-N), EstimateConfidenceAbove (belief-state gating), EntityWithinRange, WeatherLimitExceeded …", "sz": 14.5},
    {"t": "StateConditionTrigger is the runtime-reactivity primitive (level-triggered, evaluated on the tasked system's own world model — rule R11 says so out loud).", "sz": 14.5},
    {"t": "CompositeTrigger: ALL / ANY over sub-triggers, nestable. Semantics pinned by rule R9:", "sz": 14.5},
    {"t": "discrete sub-triggers (events, orders, approvals) LATCH once occurred; state conditions must HOLD at the instant of firing", "lvl": 1},
    {"t": "so “depart when route advertised AND comms up” cannot fire during a comms outage just because comms were up earlier", "lvl": 1, "c": NAVY},
])
panel_text(s, 0.7, 5.35, 12.0, 1.3, "Design discipline", [
    "No general boolean expression language: conjunction = repeated conditions (R12), disjunction = CompositeTrigger, negation = isNegated.",
    ("If richer logic is ever evidenced, a ConditionExpression subclass can be added without disturbing this base.", MGRAY),
], size=13)
footer(s)

# ---------------------------------------------------------------- 11 FAILURE & FALLBACK
s = slide()
header(s, "Highlight 2 — Failure, fallback, repetition", "The behavior-tree half: what LOX plans could not say")
bullets(s, [
    {"t": "Outcomes (R1): PhaseSucceeded / PhaseFailed / PhaseAborted / PhaseSkipped — plus TASKFAILD at task level (candidate core erratum).", "sz": 14.5},
    {"t": "Failure policy vs. failure cause (R3/R4): select AnyTaskFailed or AllTasksFailed; declared timeouts and guards are implicitly live — a declared timeout is never decorative.", "sz": 14.5},
    {"t": "Fallback (R7): hasOnFailurePhaseReference names the recovery phase, whose trigger MUST be an OnPhaseFailureTrigger — it cannot fire off the failure path. Chains give further alternatives; a chain that succeeds counts as success for the parent.", "sz": 14.5},
    {"t": "PriorityFallback policy = BT Selector as containment; SequentialInOrder + AnyTaskFailed = BT Sequence (failure halts, siblings skipped — R2/R5, no silent stalls).", "sz": 14.5},
    {"t": "Repetition (R10): RetryOnFailure (bounded), RepeatUntilCondition (loop closed by a Condition — e.g. route clear), MaintainContinuously (standing watch, N2).", "sz": 14.5},
])
panel_text(s, 0.7, 5.5, 12.0, 1.15, "Why the rules matter", [
    ("OWL restrictions alone cannot say 'failure beats completion when both are satisfiable, judged on event times' (R6). Without R1-R19, two conformant implementations disagree about the same plan.", NAVY),
], tcolor=ORANGE, size=13)
footer(s)

# ---------------------------------------------------------------- 12 APPROVAL GATE
s = slide()
header(s, "Highlight 3 — The engagement-authority gate", "Directly answers W1/Q-K, the decision log's “central ASX policy gap”")
bullets(s, [
    {"t": "HumanApprovalTrigger: the phase starts only on Agree/Confirm from a named authority; Refuse or timeout applies the fallback disposition immediately (timeout phase, else skip — and a skip cannot stall the rest of the plan, R2).", "sz": 15},
    {"t": "Compose it: (tactical trigger) ALL (human approval) — e.g. “threat inside inner bubble AND operator confirms” (the Corona & Biagini tiered-escalation pattern).", "sz": 15},
    {"t": "Per-phase autonomy: hasRequiredAutonomyLevelCode — autonomous transit, supervised engagement, in one plan (the CBRN pattern; sharpens Q-D).", "sz": 15},
    {"t": "“May this system take this action without a human?” becomes an inspectable, machine-checkable property of the transmitted plan — not an implementation detail.", "b": True, "c": NAVY, "sz": 15.5},
])
panel_text(s, 0.7, 5.15, 12.0, 1.5, "Fail-closed by rule (R13)", [
    ("A consumer that cannot interpret a phase's trigger MUST treat the phase as not triggerable, never execute it, and report the inability (ACKNOTUNDSTD).", RED),
    ("This is the one construct whose degradation mode would otherwise be catastrophic — the review made us say it normatively.", MGRAY),
], tcolor=RED, size=13)
footer(s)

# ---------------------------------------------------------------- 13 GOALS & PLAN LIBRARY
s = slide()
header(s, "Highlight 4 — Goals and the plan pre-selection library", "The BDI half: from procedural to goal-directed tasking")
bullets(s, [
    {"t": "Goal = end state, not procedure: achievement condition(s), failure conditions, commitment mode (AchieveOnce / Maintain / AchieveThenMaintain), priority. Transported inline via hasGoal on AutonomousPlanBody.", "sz": 14.5},
    {"t": "Maintain-mode goals finally express standing tasks: MDARS “continuous physical security over the depot”; MCM “keep the sea lane usable”.", "sz": 14.5},
    {"t": "Plan pre-selection library: transmit several plans for one Goal, each with context conditions — primary / degraded-comms / contested. The system selects among applicable plans and reports every switch (PlanSwitched + rationale).", "sz": 14.5},
    {"t": "Contingency plans become DATA — inspectable before the mission — instead of doctrine buried in free text. ALT/HASPRV finally get activation semantics.", "b": True, "c": NAVY, "sz": 15},
    {"t": "Goal-only tasking: an AchieveGoal task carries the end state, constraints, and ROE; the system plans. (Deliberately NOT full BDI: no subgoaling, no reconsideration strategy — those are agent internals.)", "sz": 14.5},
])
panel_text(s, 0.7, 5.6, 12.0, 1.05, "Safety rule for the library (R14)", [
    ("Variants carry isToBeExecutedNow = false and go only to module-aware consumers — to a legacy LOX consumer, three plan variants would read as three orders to execute.", RED),
], tcolor=ORANGE, size=13)
footer(s)

# ---------------------------------------------------------------- 14 REPORTING
s = slide()
header(s, "Highlight 5 — Intention transparency and explainability", "Closing X2/Q-H with constructs that degrade gracefully")
panel_text(s, 0.7, 1.65, 5.9, 3.3, "PlanExecutionStatusContent", [
    "which phase — and which GOAL is being pursued",
    "  (the system's active intention)",
    "outcome + failure cause (policy / timeout / guard)",
    "attempt number under retry (no premature",
    "  contingency firing — R10)",
    "estimated completion time (CASEVAC's phased-ETA",
    "  requirement, verbatim)",
], size=13)
panel_text(s, 6.85, 1.65, 5.85, 3.3, "PlanDeviationReportContent", [
    "sent whenever autonomy exercises an unscripted choice",
    "deviation type: RouteChanged, FallbackActivated,",
    "  PlanSwitched, GoalAbandoned, TaskReassigned",
    "the triggering event OR condition (citable by UUID)",
    "rationale text + confidence",
    ("schema adapted from the DroneResponse explainability", MGRAY),
    ("study (event, action, reasoning, change, confidence)", MGRAY),
], size=13)
bullets(s, [
    {"t": "Together these answer the CASEVAC requirement head-on: “Why did it change its expected route? Why was it unable to complete its mission?” — as structured messages, not prose.", "c": NAVY, "sz": 14.5},
    {"t": "Purely additive reporting: legacy consumers lose information, never safety.", "c": GREEN, "sz": 14},
], top=5.2, height=1.4)
footer(s)

# ---------------------------------------------------------------- 15 WORKED EXAMPLE
s = slide()
header(s, "Worked example — CASEVAC transport phase", "Two coordinating UGVs; the transport departs on the scout's published route")
panel_text(s, 0.7, 1.62, 7.4, 4.85, "TransportMovePhase  (AutonomousPlanPhase)", [
    ("TRIGGER  =  CompositeTrigger  [ALL]", NAVY),
    "   EventTrigger: scout's route-advertisement message",
    "   StateConditionTrigger: CommsAvailable  (must HOLD at departure — R9)",
    ("GUARD  =  HazardOnRoute, isNegated = true", NAVY),
    "   invariant: active route free of IED/obstacle reports;",
    "   violation fails the phase at once (R4)",
    ("ON FAILURE  →  ReplanRoutePhase", NAVY),
    "   whose trigger is OnPhaseFailureTrigger(TransportMovePhase)",
    "   — it can only fire on the failure path (R7)",
    ("GOAL  =  casualty at casualty collection point", NAVY),
    "   if the replan succeeds, the parent still succeeds (R7)",
], size=13.5)
panel_text(s, 8.35, 1.62, 4.3, 4.85, "What the operator sees", [
    "status: phase in progress, active goal,",
    "  ETA to CCP",
    " ",
    "on IED report:",
    "  deviation report —",
    "  FallbackActivated,",
    "  condition: guard UUID,",
    "  rationale: “suspected IED",
    "  on route; replanning via",
    "  alternate crossing”,",
    "  confidence 0.85",
], size=13)
bullets(s, [
    {"t": "The adversarial review corrected this very example twice: the guard's polarity (isNegated) and the fallback target's trigger. Both errors were silent under the earlier draft — exactly the class of ambiguity the module now forbids.",
     "i": True, "c": MGRAY, "sz": 12.5},
], top=6.55, height=0.5)
footer(s)

# ---------------------------------------------------------------- 16 SCENARIO BASE
s = slide()
header(s, "Where else these constructs show up", "Five sourced scenarios from the ASX corpus — the recommended validation walk set")
table(s, [
    ["Scenario (provenance)", "Constructs exercised"],
    ["DroneResponse multi-sUAS search  (Agrawal et al. 2021, arXiv)", "state triggers, fallback → request-human-assistance, deviation+rationale schema, configure/suspend/override verbs, confidence gating"],
    ["CBRN UGV recon  (Muster et al. 2024, EnRicH field trials)", "per-phase autonomy (auto mapping vs verified manipulation), retry-3-then-abort, approval gating without weapons"],
    ["MDARS persistent watch  (DTIC ADA422465 — fielded Army program)", "MaintainContinuously standing watch, ANY-composite exception triggers (intruder/trapped/fire), suspend/resume, maintain goals"],
    ["Cooperative MCM  (Ling 2020, NPS thesis)", "achieve vs maintain in one mission, repeat-on-cadence perpetual search, cross-unit state trigger (mine classified → neutralize)"],
    ["Urban C-UAS escort  (Corona & Biagini, MESAS 2019)", "human-confirmation gating, tiered non-kinetic→kinetic escalation as composite triggers, status reports proposing next actions"],
], top=1.65, col_w=[5.1, 6.9], size=12, row_h=0.62)
bullets(s, [
    {"t": "Every module construct is exercised at least twice across these five plus CASEVAC. All are sourced (non-LLM-generated), honoring the group's evidence standard.",
     "c": NAVY, "sz": 13.5},
], top=5.65, height=0.9)
footer(s)

# ---------------------------------------------------------------- 17 NOT COVERED
s = slide()
header(s, "What it deliberately does not do", "Scope discipline + honest gaps (from the adversarial pass over the corpus)")
panel_text(s, 0.7, 1.65, 5.9, 2.6, "Excluded on principle — engine internals", [
    "tick mechanics, blackboards, node memory",
    "BDI deliberation cycles, reconsideration strategy",
    "subgoaling (plans posting goals recursively)",
    ("The standard exchanges structure and intent of", MGRAY),
    ("behavior, not the execution engine.", MGRAY),
], size=13)
panel_text(s, 6.85, 1.65, 5.85, 2.6, "Known limitations — tracked as future work", [
    "reactive cross-phase preemption / trigger re-arming",
    "commanded task re-allocation, capability-based assignment",
    "report roll-up across disaggregated plans (MUM-T)",
    "quantitative control envelopes (formation keeping)",
    "resource-economy / rate conditions (counter-UAS attrition)",
], size=13)
panel_text(s, 0.7, 4.5, 12.0, 1.9, "How this was checked", [
    "Built from a structural analysis of core/SMX/LOX/ASX, then subjected to a four-way adversarial review: OWL consistency against the reference ontologies, fact-check of every claim against the repo, a BT/BDI conceptual critique, and scenario mining.",
    ("The review found (and v0.0.2 fixed): the fallback-trigger paradox, sequence stalls under failure, AND-latching, guard polarity, an untransmittable Goal, unsafe plan-library degradation, unordered condition parameters — among others.", MGRAY),
    ("Every surviving limitation above is documented in the analysis (§7) with its scenario evidence.", NAVY),
], tcolor=NAVY, size=13)
footer(s)

# ---------------------------------------------------------------- 17b V0.0.3 STATUS
s = slide()
header(s, "v0.0.3 - validation + standards verification applied",
       "Nine walk deltas + six standards-matrix additions; rules R15-R19")
bullets(s, [
    {"t": "Three validation walks (CASEVAC, DroneResponse, MDARS) instantiate end-to-end; no structural defects; all nine walk deltas are now applied in TTL v0.0.3.", "sz": 14},
    {"t": "An independent standards pass (BT/Nav2, PDDL, FlexBE, MAVLink, IEEE, JAUS, STANAG) re-derived the same construct set - convergent corroboration of the module's design, not new invention.", "sz": 14},
    {"t": "New in v0.0.3 - each with prior art:", "b": True, "sz": 14},
    {"t": "plan identity + supersession: hasPlanID / hasSupersededPlanReference, rule R16 (JAUS AS6062 mission IDs)", "lvl": 1},
    {"t": "PhaseSuspended outcome + TASKSUSP, rule R17 (JAUS Pause/Resume Mission)", "lvl": 1},
    {"t": "TASKACPT / TASKRJCT + TaskDispositionReportContent - per-task accept/reject with a machine-readable infeasibility condition", "lvl": 1},
    {"t": "lost-link failsafe floor (FailsafeBehaviorCode, rule R18) + EntityInsideArea keep-in/keep-out guards (STANAG lost-link, MAVLink fence/rally)", "lvl": 1},
    {"t": "StructuredRoute waypoints: explicit sequence, per-point speed / arrival / loiter, task-on-arrival, rule R19 (STANAG 4586 #13002-#13004)", "lvl": 1},
    {"t": "hasRepetitionInterval (revisit cadence) + predicates PayloadOnBoard, RemainingEnduranceBelow, EntityImmobilized", "lvl": 1},
], top=1.6)
panel_text(s, 0.7, 5.55, 12.0, 1.3, "Also settled", [
    "Correction: standards alignment is IEEE 1872.1-2024 only - 1872.2 verifiably defines no plan constructs.",
    ("Candidate core errata consolidated for the PDG in PDG-Change-Proposals.md (TASKFAILD, handshake/suspension codes, control verbs, event-occurrence report, LOX errata, plan identity).", MGRAY),
], size=13)
footer(s)

# ---------------------------------------------------------------- 18 EVALUATION & NEXT STEPS
s = slide()
header(s, "What we ask the group to evaluate", "And the proposed sequence if the direction holds")
bullets(s, [
    {"t": "1.  Direction — extend the LOX Plan (additive ASX module) rather than a freestanding behavior ontology. Agree?", "b": True, "sz": 15.5},
    {"t": "2.  The interop posture — fail-closed unknown triggers + capability negotiation for gating constructs. Acceptable operationally?", "b": True, "sz": 15.5},
    {"t": "3.  The condition vocabulary - right size? (typed predicates, no expression language; 16 predicates after the v0.0.3 additions, scenario-driven growth)", "b": True, "sz": 15.5},
    {"t": "4.  Core errata to raise with the PDG — TASKFAILD, task cancel/suspend verbs, runtime event-occurrence report.", "b": True, "sz": 15.5},
    {"t": "Proposed sequence: Condition + triggers (Q-D, Q-N)  →  HumanApprovalTrigger + LoA linkage (W1/Q-K)  →  Goal / plan library  →  report contents (X2, X6).", "sz": 14.5},
    {"t": "Prerequisites from the instantiation review: Swarm ⊑ CollectiveEntity (P7); attach hasAutonomousRoleCode (P3).", "sz": 14.5},
    {"t": "Next artifact: instantiation-review-style walks of CASEVAC + DroneResponse + MDARS in the module vocabulary, before advancing the OWL.", "sz": 14.5},
])
panel_text(s, 0.7, 6.0, 12.0, 0.85, "", [
    ("Artifacts: Plan-Semantics-Analysis.md (analysis, rules, limitations)  -  ASX-PlanSemantics-Draft.ttl v0.0.3 (800+ triples, validated)  -  this deck", NAVY),
], size=13)
footer(s)

OUT = "ASX-PlanSemantics-Briefing.pptx"
prs.save(OUT)
print(f"wrote {OUT} with {len(prs.slides._sldIdLst)} slides")
