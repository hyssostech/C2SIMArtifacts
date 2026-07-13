"""Builds ASX-Instantiation-Findings.pptx (29 slides) - findings from
instantiating the proposed ASX extension against 20+ scenarios. Every slide
carries speaker notes with the talk track (team-facing; Presenter-Notes.md is
the section-level view of the same track). Style follows
build_orientation_deck.py / build_plan_semantics_deck.py."""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR

NAVY   = RGBColor(0x1F,0x3A,0x5F)
ACCENT = RGBColor(0x2E,0x86,0x9A)
GRAY   = RGBColor(0x33,0x33,0x33)
MGRAY  = RGBColor(0x66,0x66,0x66)
RED    = RGBColor(0xC0,0x39,0x2B)
ORANGE = RGBColor(0xC8,0x7F,0x0A)
GREEN  = RGBColor(0x2E,0x7D,0x32)
LIGHT  = RGBColor(0xEE,0xF1,0xF5)
WHITE  = RGBColor(0xFF,0xFF,0xFF)

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
SW, SH = prs.slide_width, prs.slide_height

BULLET0 = chr(0x2022) + "  "   # bullet glyph; chr() keeps this source file ASCII-only
BULLET1 = chr(0x2013) + "  "   # en dash for sub-bullets

def slide():
    return prs.slides.add_slide(BLANK)

def box(s, l, t, w, h):
    tb = s.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    return tb, tf

def set_run(r, text, size, color, bold=False, italic=False, font="Calibri"):
    r.text = text; r.font.size = Pt(size); r.font.color.rgb = color
    r.font.bold = bold; r.font.italic = italic; r.font.name = font

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
    set_run(p.add_run(), "C2SIM ASX Sub-group   |   Hyssos   |   July 2026", 9, MGRAY)
    tb2, tf2 = box(s, 12.4, 7.02, 0.7, 0.35)
    p2 = tf2.paragraphs[0]; p2.alignment = PP_ALIGN.RIGHT
    set_run(p2.add_run(), str(n), 9, MGRAY)

def srcline(s, text):
    tb, tf = box(s, 0.55, 6.70, 12.2, 0.3)
    p = tf.paragraphs[0]
    set_run(p.add_run(), "Dig deeper:  ", 10, ACCENT, bold=True, italic=True)
    set_run(p.add_run(), text, 10, MGRAY, italic=True)

def notes(s, *paras):
    """Attach speaker notes to a slide, one string per paragraph."""
    tf = s.notes_slide.notes_text_frame
    tf.text = paras[0]
    for t in paras[1:]:
        tf.add_paragraph().text = t

def bullets(s, items, top=1.6, left=0.7, width=12.0, height=5.2, size=16, gap=6):
    height = min(height, 6.95 - top)   # never hang past the footer / slide edge
    tb, tf = box(s, left, top, width, height)
    first = True
    for it in items:
        lvl = it.get("lvl", 0)
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.level = lvl; p.space_after = Pt(gap); p.space_before = Pt(2)
        prefix = BULLET0 if lvl == 0 else BULLET1
        if it.get("tag"):
            set_run(p.add_run(), prefix + it["tag"] + "  ", size, it.get("tagcolor", RED), bold=True)
            set_run(p.add_run(), it["text"], size, GRAY)
        else:
            set_run(p.add_run(), prefix + it["text"], size,
                    it.get("color", GRAY), bold=it.get("bold", False))
    return tf

def rbox(s, l, t, w, h, text, fill, line=None, tcolor=WHITE, size=13, bold=True):
    sp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(l), Inches(t), Inches(w), Inches(h))
    sp.fill.solid(); sp.fill.fore_color.rgb = fill
    if line: sp.line.color.rgb = line; sp.line.width = Pt(1.25)
    else: sp.line.fill.background()
    tf = sp.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    set_run(p.add_run(), text, size, tcolor, bold=bold)
    return sp

def arrow(s, x1, y1, x2, y2, color=NAVY):
    c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = color; c.line.width = Pt(1.5)
    return c

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

# ---------------- Slide 1: Title ----------------
s = slide()
band = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(2.35), SW, Inches(2.5))
band.fill.solid(); band.fill.fore_color.rgb = NAVY; band.line.fill.background()
tb, tf = box(s, 0.8, 2.55, 11.7, 1.4)
p = tf.paragraphs[0]; set_run(p.add_run(), "ASX Extension: Findings from Scenario Instantiation", 34, WHITE, bold=True)
tb, tf = box(s, 0.8, 3.75, 11.7, 0.7)
p = tf.paragraphs[0]
set_run(p.add_run(), "Testing the proposed ontology elements by walking scenarios into real messages", 17, RGBColor(0xCF,0xE0,0xEA))
tb, tf = box(s, 0.8, 5.15, 11.7, 0.5)
p = tf.paragraphs[0]
set_run(p.add_run(), "C2SIM ASX Sub-group    -    Hyssos    -    July 2026", 13, MGRAY)
tb, tf = box(s, 0.8, 5.75, 11.7, 0.5)
p = tf.paragraphs[0]
set_run(p.add_run(), "Reading this outside the meeting: every slide carries speaker notes with the talk track; the last three slides are the reading guide.",
        11.5, MGRAY, italic=True)
accent = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(2.35), Inches(2.4), Pt(5))
accent.fill.solid(); accent.fill.fore_color.rgb = ACCENT; accent.line.fill.background()
notes(s,
 "What this is: for each scenario, we tried to write the actual messages it needs, using C2SIM plus the proposed ASX elements. Where a message would not build cleanly, that is a concrete item to define. The review builds on the proposed extension and Elizabeth's sample-message work; everything in it is a proposal - nothing has been applied to the model or the workbooks.",
 "Time plan for a 30-minute slot: opening (slides 1-2) ~3 min; method and deliverables (3-5) ~5 min; where the instantiation stands (6-7) ~4 min; the structural block (8-12) ~7 min; findings by domain (13-19) ~6 min; v0.0.3 and the decision register (20-24) ~4 min; close (25-26) ~1 min. Slides 27-29 are the reading guide - point at them, do not present them.",
 "If the slot is 20 minutes: slides 1-2, 5, 8-12, the decisions grouping (21), and next steps (26); everything else is handout material.")

# ---------------- The whole review in one slide ----------------
s = slide(); header(s, "The whole review in one slide", "The 90-second version - everything after this is detail")
bullets(s, [
 {"tag":"What was done:","tagcolor":NAVY,"text":"walked 20+ scenarios into ~29 new worked messages (4 -> ~33) using C2SIM + the proposed ASX elements, in diff-able workbooks - Initialization 0 -> 6, Orders 2 -> 14, Reports 2 -> 13."},
 {"tag":"What it surfaced:","tagcolor":NAVY,"text":"three structural typing decisions come first - UAV/robot typing (P1), sensor representation (P2), a taskable swarm (P7) - and behind them an attribute layer still to be built (v0.0.1 had 0 datatype properties; v0.0.3 starts it)."},
 {"tag":"The good news:","tagcolor":GREEN,"text":"much of what is missing is re-adopt, not invent - BML WhoMeasuredType for measurements, 446 LOX task verbs, ROE / routes / resources already in the base standard."},
 {"tag":"The ask:","tagcolor":ACCENT,"text":"22 concrete decisions (Q-A..Q-V, log sec 7), plus four plan-semantics decisions (Q-W..Q-Z) from the standards pass - settle the four structural ones (Q-A..Q-D) first; they unblock Initialization."},
 {"tag":"Status:","tagcolor":ORANGE,"text":"everything is a proposal - nothing applied to the OWL or the .xlsx; every RDF-grounded claim was independently re-verified."},
], top=1.75, size=14.5, gap=12)
srcline(s, "Group-Briefing.md is the one-page prose version of this slide")
footer(s)
notes(s,
 "The one-slide version of the talk. If discussion takes over later, this slide plus the decision register (slides 21-23) is the minimum to land.",
 "Grounding for the numbers: the counts are the coverage rows in log sec 6 (C1-C8). The re-adopt items were verified against the RDF, not recalled: WhoMeasuredType is in C2SIM's BML lineage; LOX carries 446 TaskActionCode verbs; ROE, routes, resources, and a neutral hostility value (smx#NEUTRL) exist in the base standard.")

# ---------------- Approach ----------------
s = slide(); header(s, "The method", "Building on the sample-message work")
bullets(s, [
 {"text":"Walk each scenario and instantiate real Initialization / Order / Report messages using C2SIM + the proposed ASX elements."},
 {"text":"The ASX model is an early work-in-progress (v0.0.x) and the message instances are still being put in place - instantiation is how we build those instances and surface what is still to be defined."},
 {"text":"Where a proposed element is not yet defined enough to instantiate cleanly, that marks a concrete thing to specify next - not a defect."},
 {"text":"Everything here is decisions and to-define items for the group; the approach is working."},
], top=1.7, size=17, gap=13)
footer(s)
notes(s,
 "Section budget: slides 3-5, about 5 minutes.",
 "The method in one sentence: write the messages each scenario actually needs; where an element is not yet defined enough to instantiate cleanly, that marks a concrete thing to specify next - not a defect. The model is early (v0.0.x) and the message layer is still being built; instantiation is how those instances get built and how the to-define list surfaces.",
 "Scope note: the sample-message workbooks were converted to a diff-able .xml format so instantiations can be reviewed in git; the original .xlsx are untouched.")

# ---------------- Process: three sessions + verification ----------------
s = slide(); header(s, "How this was produced: three sessions + a verification pass",
                    "LLM-assisted, human-directed - each stage grounded in the artifacts, not memory")
rbox(s, 0.7, 1.9, 3.7, 1.7, "1  -  Document mining\n\nHunt primary mission documents (theses, tech reports, AARs) for missing domains + validation holes", NAVY, size=12.5)
rbox(s, 4.8, 1.9, 3.7, 1.7, "2  -  Scenario extraction\n\nA locked v2.2 prompt distills each document into a standardized scenario record (12 records)", NAVY, size=12.5)
rbox(s, 8.9, 1.9, 3.7, 1.7, "3  -  Ontology application\n\nWalk each scenario into concrete Init / Order / Report messages using the proposed ASX elements", NAVY, size=12.5)
arrow(s, 4.4, 2.75, 4.8, 2.75, ACCENT); arrow(s, 8.5, 2.75, 8.9, 2.75, ACCENT)
rbox(s, 0.7, 3.95, 11.9, 1.05, "4  -  Independent verification pass: every RDF-grounded claim re-checked against C2SIM / SMX / LOX and v0.0.3; workbooks re-compared cell-for-cell; citations traced; deck regenerated. Corrections logged (issues log, 2026-07-12).", GREEN, size=13)
bullets(s, [
 {"text":"The loop iterates: the ontology walk (3) writes the sourcing brief (Documents-Needed), mining (1) answers it (Documents-Found), extraction (2) turns the finds into records, and the walk integrates them - until every raised gap is grounded in a real mission."},
 {"text":"Artifacts per stage: References corpus + Documents-Needed/Found (1); PromptV2 + V2Extractions (2); the .xml workbooks, walk docs, and issues log (3).","color":MGRAY},
], top=5.25, size=13, gap=7)
srcline(s, "Documents-Needed/Found.md (mining)  -  PromptV2.md + V2-HeadToHead.md (extraction)  -  the walk docs (application)  -  log change-log 2026-07-12 (verification)")
footer(s)
notes(s,
 "Three coordinated sessions plus an independent check: document mining hunts primary mission documents; scenario extraction distills each into a standardized record with the locked v2.2 prompt; ontology application walks each scenario into concrete messages against the proposed elements. The verification pass then re-checked every RDF-grounded claim, the workbook fidelity, and the citations, with corrections logged (issues log change log, 2026-07-12).",
 "The stages iterate: the walk writes the sourcing brief (Documents-Needed), mining answers it (Documents-Found), extraction feeds the walk. Nothing rests on an LLM's memory - every claim is grounded in the RDF, the workbooks, or a named source, and was independently re-verified.")

# ---------------- What this review contributes ----------------
s = slide(); header(s, "What this review contributes", "Five deliverables - all proposals, nothing applied to the OWL or the .xlsx")
bullets(s, [
 {"tag":"1  Message instantiations:","tagcolor":NAVY,"text":"~29 new worked messages (4 -> ~33; Initialization 0 -> 6) in diff-able .xml workbooks - one tab per message, with open items flagged [!]/[Q] in the Notes column, keyed to log IDs."},
 {"tag":"2  Sourced scenario corpus:","tagcolor":NAVY,"text":"12 standardized extraction records from real missions (subterranean, maritime MCM, sustainment, explainability, CBRN, EW, persistence, counter-UAS, MUM-T, SAR, formation, breach) + the source PDFs - every gap this review raised is grounded in a documented mission."},
 {"tag":"3  Findings -> decisions:","tagcolor":NAVY,"text":"a consolidated issues log (severity / status / RDF-verified evidence per finding) distilled into 22 concrete decisions for the group (Q-A..Q-V)."},
 {"tag":"4  v0.0.3 reconciliation:","tagcolor":NAVY,"text":"how each finding moves against Michael's update - what it adopts, what it makes concrete, what remains - plus coordination notes (two ASX files, import layering)."},
 {"tag":"5  Prior art to re-adopt:","tagcolor":NAVY,"text":"the measurement report exists in C2SIM's own BML lineage (WhoMeasuredType); ROE, routes, resources, membership/command, maritime vessels, and 446 task verbs already exist in the base standard - several decisions are re-adopt, not invent."},
], top=1.7, size=14.5, gap=12)
srcline(s, "the full artifact map is on the final three slides ('How to use this material' / decoder ring / 'Where to dig deeper')")
footer(s)
notes(s,
 "Five deliverables: ~29 new message instantiations in diff-able workbooks; a 12-record sourced scenario corpus; a findings log distilled into 22 decisions; a finding-by-finding reconciliation with v0.0.3; and the prior-art discoveries (BML WhoMeasuredType first among them). All proposal-only.",
 "This slide frames the rest of the talk: each later section shows where one of these deliverables came from.")

# ---------------- State of play ----------------
s = slide(); header(s, "Where the instantiation stands", "From 4 worked messages to ~33 - this review is the bulk of that")
bullets(s, [
 {"text":"Start: 4 worked instances (2 Reports, 2 Orders, 0 Initialization) - Elizabeth's baseline. This review drafted ~29 more, to ~33 across Init / Order / Report (on the branch, pending group review).","bold":True},
 {"text":"Initialization   0 -> 6   (the 3 named scenarios + CASEVAC / MCM / SubT) - was the least-developed; now seeded.","lvl":1},
 {"text":"Orders   2 -> 14   (CASEVAC, swarm, fire support, logistics / engineering / rescue, route clearance, MCM, explore, resupply, MUM-T).","lvl":1},
 {"text":"Reports   2 -> 13   (swarm, CASEVAC status / explainable, CBRN / EW / GPR, BDA, delivery, naval mine, generic detection, hazard area).","lvl":1},
 {"text":"CASEVAC - the one contributed scenario - had no messages; now walked end-to-end (Init + Orders + Reports).","bold":True},
 {"text":"The breadth is the point: each new instance exercises a proposed element and surfaces what is still to define.","lvl":1},
], top=1.75, size=15, gap=9)
srcline(s, "Message-Instantiation-Coverage.md (the pre-walk baseline)  -  log sec 6 rows C1-C8 (current state)  -  the three ASX Sample *.xml workbooks (the messages themselves)")
footer(s)
notes(s,
 "Section budget: slides 6-7, about 4 minutes.",
 "The baseline was 4 worked instances (2 Reports, 2 Orders, 0 Initialization) - Elizabeth's sample-message workbooks. This review drafted ~29 more, to ~33: Initialization 0 -> 6, Orders 2 -> 14, Reports 2 -> 13. The breadth - not any single message - is what surfaced the to-define items.",
 "CASEVAC, the one contributed (human-authored) scenario, had no messages; it is now walked end to end: Init -> tasking Order -> robot-to-robot hand-off -> status / threat / explainable Reports.")

# ---------------- Scenarios analyzed (showcase) ----------------
s = slide(); header(s, "Scenarios analyzed", "20+ scenarios walked into ~33 message instances - Init / Order / Report")
bullets(s, [
 {"text":"Named + contributed - instantiated end-to-end:","bold":True},
 {"text":"the 3 named Init scenarios (UAV video, UAV patrol, swarm) + CASEVAC, the one human-authored contributed scenario - walked Init -> tasking Order -> robot-to-robot hand-off -> status/threat + explainable Reports.","lvl":1},
 {"text":"Capability stress-tests - instantiated:","bold":True},
 {"text":"non-video sensing (CBRN, EW emitter, GPR mine); swarm detect + coordinate; the task/effect axis (fire support + BDA, logistics delivery, engineering, USV rescue, route clearance).","lvl":1},
 {"text":"Newly sourced from real missions, then analyzed:","bold":True},
 {"text":"Cooperative MCM (maritime), Subterranean SubT, contested sustainment - plus nine documented missions that grounded the validation holes: explainability (DroneResponse), CBRN (UGV), EW geolocation, persistence (MDARS), counter-UAS, human-machine teaming (MUM-T), SAR, formation, robotic breach.","lvl":1},
 {"text":"Screened for redundancy:","bold":True},
 {"text":"route-clearance / companion / urban - confirmed ~80% redundant, but still yielded N1 (an area as the subject of a task/report).","lvl":1},
], top=1.7, size=13, gap=7)
srcline(s, "one walk doc per scenario family (see final slide)  -  the 12 sourced records: LLMExperiments/PaperSummaries/V2Extractions/")
footer(s)
notes(s,
 "Four groups: named + contributed scenarios instantiated end to end; capability stress-tests (non-video sensors, swarm, task/effect); missions sourced from real documents by the parallel sourcing effort (Cooperative MCM, SubT, sustainment, plus nine documented missions that closed the validation holes); and a redundancy screen that still yielded one new finding (N1).",
 "Provenance, stated precisely: the MUTT-derived scenarios are LLM-generated; CASEVAC is human-authored; the sourced missions come from real papers - two carry fidelity caveats (EW and the robotic breach), noted in their extraction records.")

# ---------------- Two tracks out of sync ----------------
s = slide(); header(s, "The OWL and the spreadsheets are at different stages")
rbox(s, 0.8, 1.9, 5.5, 1.5, "OWL model  (CSIM_ASX.rdf)\nlast updated  Jan 2026", NAVY, size=15)
rbox(s, 7.0, 1.9, 5.5, 1.5, "Spreadsheets  (Concept Mapping,\nsample messages)  updated  Jun 2026", ACCENT, size=15)
arrow(s, 6.3, 2.65, 7.0, 2.65, ORANGE)
bullets(s, [
 {"tag":"Where things stand:","tagcolor":ORANGE,"text":"the OWL has not yet caught up to ~5 months of attribute work in the spreadsheets - expected for a v0.0.x model that is still being built."},
 {"text":"Autonomy is currently described three different ways across the two tracks - to reconcile.","lvl":1},
 {"text":"Sensors are described three different ways - to reconcile.","lvl":1},
 {"text":"The attribute layer (Payload, Mobility, VehicleType, ...) is in the spreadsheets, not yet in the OWL.","lvl":1},
], top=3.8, size=16, gap=10)
srcline(s, "log sec 1-2 (S2, D1-D5)")
footer(s)
notes(s,
 "Section budget: slides 8-12, about 7 minutes - the core of the talk.",
 "Why several findings look like drift rather than gaps: the OWL model (last updated January) and the spreadsheets (updated June) evolved separately, so autonomy and sensors are each currently described three different ways. Reconciling the two tracks is one of the first decisions. Worth establishing early - it explains a lot of the later slides.")

# ---------------- 3 decide-first typing decisions ----------------
s = slide(); header(s, "First to settle: three structural typing decisions")
rbox(s, 0.8, 2.0, 3.8, 2.2, "P1\nUAV typing: Robot\ntree vs SMX Platform", ORANGE, size=16)
rbox(s, 4.85, 2.0, 3.8, 2.2, "P2\nSensor: one\nrepresentation to pick", ORANGE, size=16)
rbox(s, 8.9, 2.0, 3.65, 2.2, "P7\nSwarm: make it\ntaskable (ActorEntity)", ORANGE, size=16)
bullets(s, [
 {"text":"P1 and P7 are entity-typing (what a drone / a swarm IS); P2 is how a sensor is represented. All three are structural choices not yet settled - so Initialization, not Reports, is where the model gets exercised and pinned down first.","bold":True},
], top=4.7, size=17)
srcline(s, "Initialization-Walk.md  -  log sec 5 (P-series)")
footer(s)
notes(s,
 "The three foundational decisions, all entity-typing: P1 - a UAV/UGV is typed two incompatible ways (ASX Robot tree vs SMX Platform tree); P2 - a sensor has no agreed representation (class vs enum vs equipment); P7 - a swarm is not yet taskable as modeled.",
 "The point to land: because all three are typing decisions, Initialization - not Reports - is where the model has to be settled first. The next two slides take P1 and P7 one at a time.")

# ---------------- P1 diagram ----------------
s = slide(); header(s, "P1  -  A UAV is typed twice", "Entity-typing decision")
rbox(s, 5.2, 1.7, 3.0, 0.75, "ActorEntity", NAVY, size=14)
rbox(s, 2.4, 3.0, 3.0, 0.75, "Platform  (SMX)", ACCENT, size=13)
rbox(s, 2.4, 4.2, 3.0, 0.75, "Aircraft  (SMX)", ACCENT, size=13)
rbox(s, 8.0, 3.0, 3.0, 0.75, "Robot  (ASX)", ORANGE, size=13)
rbox(s, 8.0, 4.2, 3.0, 0.75, "UAV  (ASX)", ORANGE, size=13)
arrow(s, 6.2, 2.45, 3.9, 3.0); arrow(s, 3.9, 3.75, 3.9, 4.2)
arrow(s, 7.2, 2.45, 9.5, 3.0); arrow(s, 9.5, 3.75, 9.5, 4.2)
bullets(s, [
 {"text":"Two parallel sibling trees under ActorEntity model the same real drone."},
 {"text":"Type it as Robot -> it loses all existing SMX Platform / LOX machinery.","lvl":1},
 {"text":"Type it as Aircraft -> the ASX Robot / UAV classes go unused.","lvl":1},
 {"tag":"Now live in v0.0.3:","tagcolor":ORANGE,"text":"v0.0.3 declares both - UAV/UGV under Robot AND UnmannedAerial/Ground/Maritime/UnderwaterVehicle under SMX Vehicle - so this choice is now in the model to settle."},
 {"tag":"Decision (Q-A):","tagcolor":ACCENT,"text":"make ASX autonomy a role/facet on the existing Platform subtree instead of a parallel Robot tree?"},
], top=4.85, size=13, gap=5)
srcline(s, "Initialization-Walk.md  -  log P1 (sec 5) + sec 9 (v0.0.3 makes it concrete)  -  decision Q-A (log sec 7)")
footer(s)
notes(s,
 "The proposed Robot class tree runs parallel to the existing SMX Platform tree, both under ActorEntity - two incompatible types for the same real drone. Type it as Robot and it loses the Platform machinery; type it as Aircraft or Vehicle and the ASX classes go unused.",
 "v0.0.3 declares both trees, so the choice is now concretely in the model to settle. Decision Q-A proposes autonomy as a role/facet on the existing Platform subtree.")

# ---------------- P7 diagram ----------------
s = slide(); header(s, "P7  -  A swarm is not yet taskable", "Entity-typing decision")
rbox(s, 0.9, 2.0, 3.1, 0.7, "Swarm  (ASX)", ORANGE, size=13)
rbox(s, 4.3, 2.0, 3.6, 0.7, "CollecticeRoboticSystem (sic)", ORANGE, size=12)
rbox(s, 8.2, 2.0, 3.4, 0.7, "... PhysicalEntity", RED, size=13)
arrow(s, 4.0, 2.35, 4.3, 2.35, RED); arrow(s, 7.9, 2.35, 8.2, 2.35, RED)
tb, tf = box(s, 8.2, 2.75, 3.6, 0.4); p=tf.paragraphs[0]
set_run(p.add_run(), "not yet taskable (under PhysicalEntity)", 12, ORANGE, italic=True)
rbox(s, 0.9, 4.0, 3.1, 0.7, "Swarm  (proposed)", GREEN, size=13)
rbox(s, 4.3, 4.0, 3.6, 0.7, "CollectiveEntity  (C2SIM)", GREEN, size=12)
rbox(s, 8.2, 4.0, 3.4, 0.7, "ActorEntity", GREEN, size=13)
arrow(s, 4.0, 4.35, 4.3, 4.35, GREEN); arrow(s, 7.9, 4.35, 8.2, 4.35, GREEN)
tb, tf = box(s, 8.2, 4.75, 3.6, 0.4); p=tf.paragraphs[0]
set_run(p.add_run(), "taskable - receives orders, reports", 12, GREEN, italic=True)
bullets(s, [
 {"text":"A swarm is what orders are addressed to and what sends reports - so it needs to be an ActorEntity."},
 {"text":"Membership and command already exist in the base standard (C2SIM hasSubordinate, SMX hasCommandRelation), so the residual swarm work is small. (v0.0.3 dropped the Swarm class; CollecticeRoboticSystem is still under PhysicalEntity.)","lvl":1},
 {"tag":"Decision (Q-B):","tagcolor":ACCENT,"text":"derive the collective/Swarm from CollectiveEntity (already an ActorEntity) rather than the device/artifact tree."},
], top=5.3, size=13, gap=5)
srcline(s, "Swarm-Walk.md  -  log P7 (secs 5, 6d)  -  decision Q-B (log sec 7)")
footer(s)
notes(s,
 "The swarm classes derive from the device/artifact side (PhysicalEntity), but orders are addressed to - and reports come from - an ActorEntity. The fix is already in the base standard: derive the collective from CollectiveEntity. Membership and command relations already exist (C2SIM hasSubordinate, SMX hasCommandRelation), so the residual swarm work is small.",
 "Note the current state: v0.0.3 dropped the Swarm class, and CollecticeRoboticSystem (the typo is in the model - O1) is still under PhysicalEntity. Decision Q-B.")

# ---------------- Model drift detail ----------------
s = slide(); header(s, "The OWL is still catching up to the spreadsheets", "v0.0.x - expected at this stage")
bullets(s, [
 {"tag":"Autonomy - 3 vocabularies to reconcile:","tagcolor":ORANGE,"text":"OWL {Automated, FullAuto, ReCont, Teleop}  vs  ControlMode {Piloted, Unpiloted-Autonomous, Swarm}  vs  NavigationAutonomy {FPV, Autonomous, RemoteControl}."},
 {"tag":"Sensor - 3 models to reconcile:","tagcolor":ORANGE,"text":"OWL Sensor class  vs  SensorType enum  vs  SensorCapability as associated equipment."},
 {"tag":"Not yet in the OWL:","tagcolor":ORANGE,"text":"Payload, PayloadCapability, Mobility/Propulsion, VehicleType, PassengerCapability, AutonomousMissionFunction/Parameters, SwarmParameters. (v0.0.1 had 0 datatype properties; v0.0.3 begins the layer, for the Video Detection Report only.)"},
 {"tag":"Decisions (Q-C, Q-D):","tagcolor":ACCENT,"text":"pick one normative sensor model and one normative autonomy vocabulary; express the rest as derived."},
], top=1.8, size=15, gap=13)
srcline(s, "log sec 2 (D1-D3)  -  ASX Concept Mapping.xlsx (the spreadsheet-side vocabularies)")
footer(s)
notes(s,
 "The concrete reconciliation list: three autonomy vocabularies, three sensor models, and the attribute layer (Payload, Mobility, VehicleType, ...) that exists in the spreadsheets but not yet in the OWL.",
 "Why so much is still to define: the v0.0.1 baseline is 15 classes, 1 object property, 0 datatype properties - a taxonomy of things; the layer that says what you actually send had not been built yet. v0.0.3 begins it (datatype properties for the Video Detection Report). Most gaps are simply not-yet-built - which is why writing messages surfaces them. Decisions Q-C / Q-D: pick one normative sensor model and one autonomy vocabulary, express the rest as derived.")

# ---------------- Sample-message open items ----------------
s = slide(); header(s, "Open items in the current instantiations", "small things to tidy as the model firms up")
bullets(s, [
 {"tag":"M1:","tagcolor":ORANGE,"text":"actorReference is a string, but it needs to define an entity not yet in the database - an inline entity-definition mechanism for observed entities is still to be added."},
 {"tag":"M5:","tagcolor":ORANGE,"text":"MediaTypeCode {VID/AUD/IMG/DOC/TXT/NOS} mixes media format with sensor modality - the sample sheets' MediaTypeEnum already used its 'Not Otherwise Specified' value for 'thermal scan' (a sensor type) - worth separating."},
 {"tag":"M7:","tagcolor":ORANGE,"text":"in an Order sheet hasStartTime is typed UUIDBase while hasEndTime is TimeInstant - looks like a copy/paste slip."},
 {"tag":"Typos:","tagcolor":ORANGE,"text":"class 'CollecticeRoboticSystem' (should be 'CollectiveRoboticSystem') and versionInfo 'Extrension' - both still in v0.0.3; easiest to fix before messages are built on them."},
], top=1.8, size=15, gap=13)
srcline(s, "log sec 4 (M-series, sample messages)  -  sec 3 (typos & naming)")
footer(s)
notes(s,
 "Section budget: slides 13-19, about 6 minutes - one beat per domain; each slide's Dig deeper line names the walk doc and log section with the full detail.",
 "M-series: small instantiation-level items - inline entity definition for observed entities (M1), media format vs sensor modality (M5), a UUIDBase/TimeInstant copy-paste slip (M7), and two typos still in v0.0.3 (CollecticeRoboticSystem, Extrension). All cheapest to fix before messages are built on them.")

# ---------------- Coverage gaps ----------------
s = slide(); header(s, "Coverage: what is still to instantiate")
bullets(s, [
 {"text":"Initialization: 0 of 3 named scenarios were instantiated (now drafted in this review).","bold":True},
 {"text":"CASEVAC: walked end-to-end in this review - surfaces two gaps with no element (next slide).","bold":True},
 {"text":"Non-video sensors (CBRN, EW, GPR): walked - the media-based report model does not generalize; non-imaging sensors have no measurement type (Y1/Y5).","bold":True},
 {"text":"Task/effect scenarios: engagement, delivery, manipulation, rescue walked - the gap is mainly payload/effector/weapon typing (most task verbs already exist in LOX)."},
 {"text":"Redundancy pass (route-clearance, companion, urban): confirmed - plus one new finding, N1 (an area is not yet able to be the subject of a task/report)."},
 {"text":"Sourced scenarios (subterranean, maritime MCM, sustainment): integrated from the parallel scenario-sourcing effort - corroborate P1/X1/N2/Y and add G1-G10 (incl. a generic Detection Report)."},
], top=1.6, size=14.5, gap=8)
srcline(s, "log sec 6 (C1-C8) - each coverage row names the walk doc and tabs behind it")
footer(s)
notes(s,
 "The coverage map: what was still to instantiate, and what this review drafted for each row. Initialization had 0 of 3 named scenarios instantiated - now drafted. Non-video sensors show the media-based report model does not generalize (Y1/Y5). The task/effect gap is mainly payload/effector/weapon typing - the verbs already exist. The redundancy pass confirmed ~80% overlap but still yielded N1 (an area as the subject of a task/report).",
 "Each row on this slide resolves to a C-row in log sec 6, which names the walk doc and the workbook tabs behind it.")

# ---------------- CASEVAC walk ----------------
s = slide(); header(s, "CASEVAC walk: two gaps with no element", "The flagship contributed scenario")
bullets(s, [
 {"text":"Walked end-to-end: Initialization -> tasking Order -> robot-to-robot route hand-off -> status/threat Reports -> explainable-reasons Report."},
], top=1.55, size=14, height=0.85)
rbox(s, 0.8, 2.45, 5.75, 1.75, "X1  -  No robot-to-robot content\n\nScout has no content type yet to hand a verified safe Route to the transport UGV (envelope addressing exists; a content type does not)", RED, size=13)
rbox(s, 6.8, 2.45, 5.75, 1.75, "X2  -  No rationale report\n\nSystems can report WHAT (TaskStatus) but not WHY a route changed or a mission failed", RED, size=13)
bullets(s, [
 {"tag":"Decision (Q-G):","tagcolor":ACCENT,"text":"define a robot-to-robot coordination content type (safe-route advertisement) and the issuing-authority model."},
 {"tag":"Decision (Q-H):","tagcolor":ACCENT,"text":"add a rationale/explanation ReportContent so systems can report why, not just what."},
 {"tag":"Checked:","tagcolor":GREEN,"text":"Route, phased planning (PlanBody/PlanPhase), and position reporting already exist - not gaps."},
], top=4.5, size=14, gap=9)
srcline(s, "CASEVAC-Walk.md  -  log sec 6b (X1-X6)  -  5 CASEVAC tabs in the .xml workbooks")
footer(s)
notes(s,
 "The flagship contributed scenario, walked end to end. Two gaps have no element at all: X1 - no content type for one robot to hand a verified safe route to another (envelope addressing exists; the content does not); X2 - systems can report WHAT (TaskStatus) but not WHY a route changed or a mission failed. Decisions Q-G / Q-H.",
 "Also checked, and not gaps: Route, phased planning (PlanBody/PlanPhase), and position reporting already exist in the base standard.")

# ---------------- Fire Support / engagement authority ----------------
s = slide(); header(s, "Fire Support: autonomous engagement authority", "The task/effect axis")
rbox(s, 0.8, 1.95, 11.75, 1.6, "W1  -  No link between autonomy level and permission to engage\n\nThe standard can say WHAT effect and WHICH ROE - but not WHO (which commander) authorized the engagement, nor whether a FullAuto system may take a lethal action without a human in / on the loop.", RED, size=15)
bullets(s, [
 {"tag":"Checked - already exist (not gaps):","tagcolor":GREEN,"text":"rules of engagement (RuleOfEngagement, WeaponRuleOfEngagementCode - LOX), desired effect (DesiredEffectCode), target (hasAffectedEntity), and the engage/attack verbs (lox#ENGAGE / lox#ATTACK)."},
 {"tag":"Note:","tagcolor":ORANGE,"text":"AuthorizationHeader is message-sender authentication, not command authorization of fires - so who-approved-the-engagement is part of W1, not covered."},
 {"tag":"Also gaps:","tagcolor":ORANGE,"text":"W2 weapon/munition not typed; W3 no battle-damage / effect-achieved report (TaskStatus = the task ran, not the target destroyed)."},
 {"tag":"Decision (Q-K):","tagcolor":ACCENT,"text":"model engagement authority as a function of autonomy level - may this system take this action unsupervised?"},
], top=3.8, size=14.5, gap=11)
srcline(s, "FireSupport-Walk.md  -  log sec 6e (W1-W3)  -  Fire Support Order + BDA Report tabs")
footer(s)
notes(s,
 "W1: the standard can express WHAT effect and WHICH ROE, but not WHO authorized an engagement, nor whether a FullAuto system may take a lethal action without a human in or on the loop. AuthorizationHeader was checked: it is message-sender authentication, not command authorization of fires - so who-approved-the-engagement is part of the gap.",
 "Also W2 (weapon/munition not typed) and W3 (no battle-damage / effect-achieved report - TaskStatus says the task ran, not that the target was destroyed). Decision Q-K: engagement authority as a function of autonomy level.")

# ---------------- Task/effect summary ----------------
s = slide(); header(s, "The task/effect axis is mostly already there", "Across engagement, delivery, manipulation, rescue, search")
rbox(s, 0.8, 2.0, 5.75, 1.75, "Action verbs already exist\n\nLOX has 446 TaskActionCode verbs - ENGAGE, ATTACK, BREACH, CONSTR, CLROBS, MINLAY, TRANS, RESUPL, RESCUE, RECOVR, NTRCOM, ESCRT, RECCE, PATROL. Not a missing-verb problem.", GREEN, size=13)
rbox(s, 6.8, 2.0, 5.75, 1.75, "The real gap: payload / effector / weapon typing\n\nCargo (L1), manipulator (E2), weapon (W2) are one gap: no typed thing carried or wielded.", NAVY, size=13)
bullets(s, [
 {"tag":"Also already there (checked):","tagcolor":GREEN,"text":"effects (DesiredEffectCode), targets (hasAffectedEntity), resources + quantities, ROE, platform types (Vehicle / Aircraft / SurfaceVessel)."},
 {"tag":"Small residuals:","tagcolor":ORANGE,"text":"an area is not yet a possible task/report subject (N1 / Q-M); an area-coverage exploration goal (G2); a general-purpose tow/salvage verb (TOWTGT covers gunnery targets only); a decoy role."},
 {"tag":"Decision (Q-L):","tagcolor":ACCENT,"text":"add the typed payload / effector / weapon - the verbs are already in LOX."},
], top=4.0, size=14, gap=9)
srcline(s, "TaskEffect-Batch-Walk.md  -  RedundancyPass-Walk.md  -  log secs 6f / 6g (L, E, R, N series)")
footer(s)
notes(s,
 "The counterweight slide of the domain block: LOX already carries 446 task verbs (ENGAGE, BREACH, RESUPL, RESCUE, ...), plus effects, targets, resources, and ROE - all verified in the RDF. The task/effect work is not invent-verbs.",
 "The real gap is one pattern: nothing typed for what a platform carries or wields - cargo (L1), manipulator (E2), weapon (W2) are the same missing piece. Decision Q-L. Small residuals: area as task subject (N1/Q-M), area-coverage goal (G2), a general tow/salvage verb, a decoy role.")

# ---------------- Sourced scenarios (SubT / MCM / Sustainment) ----------------
s = slide(); header(s, "Integrated from the parallel scenario-sourcing effort", "SubT (subterranean) + Cooperative MCM (maritime) + Sustainment")
bullets(s, [
 {"tag":"Corroborated (fresh domains):","tagcolor":GREEN,"text":"platform typing P1, robot-to-robot X1 (-> cross-cueing), persistent tasking N2, and the sensor-report problem Y1."},
 {"tag":"Best contribution (G4):","tagcolor":ACCENT,"text":"one generic Detection Report (confidence + error-bound + false-positive) subsumes Video/CBRN/EW/GPR/naval-mine - resolves Y1 (and M3/M4); the measurement/taxonomy side (Y2/Y5) folds into Q-I."},
 {"tag":"New gaps:","tagcolor":ORANGE,"text":"area-coverage/exploration goal (G2, search verbs exist); denied-comms mode + relay entity (G1, the relay verb COMREL exists); decoy role (G8, deception verbs exist); maritime cross-cue with a shared track (G3); environment conditions (G11); formation geometry (G12)."},
 {"text":"Neutral-actor framing is mostly covered (smx#NEUTRL hostility value; an untyped NeutralSide individual also exists). Counter-UAS, human-machine teaming, and SAR were all extracted in the later validation pass.","color":MGRAY},
], top=1.75, size=15, gap=13)
srcline(s, "SourcedScenarios-Walk.md  -  OntologyConceptCoverage.md  -  log secs 6h / 6i (G-series)  -  7 tabs in the .xml workbooks")
footer(s)
notes(s,
 "The parallel sourcing effort grounded this review's gaps in real missions and added its own findings (the G-series). Best contribution: one generic Detection Report (confidence + error bound + false positive) that subsumes the video / CBRN / EW / GPR / naval-mine reports - it resolves Y1 and folds into Q-I / Q-Q.",
 "New gaps from fresh domains: area-coverage goal, denied-comms mode + relay entity, decoy role, maritime cross-cueing with a shared track, environment conditions, formation geometry. Several re-use existing verbs (search verbs, lox#COMREL) - the gap is the surrounding structure, not the vocabulary.")

# ---------------- Validation evidence ----------------
s = slide(); header(s, "Validation: the gaps are now evidenced", "Nine sourced missions closed the document holes")
bullets(s, [
 {"tag":"Now grounded by a real mission:","tagcolor":GREEN,"text":"explainability (Agrawal DroneResponse), CBRN (UGV-CBRN), EW (UAV emitter geolocation), persistence (MDARS) - all previously asserted-but-untested."},
 {"tag":"Prior art, not invention (Q-Q):","tagcolor":ACCENT,"text":"the measurement report flagged as missing already existed in C2SIM's BML lineage - WhoMeasuredType {value, unit, phenomenon, sensor, time, place}. Re-adopt it."},
 {"tag":"Concrete schemas:","tagcolor":ORANGE,"text":"explanation report {event, action, reasoning, change, confidence} (Q-H); area map w/ per-cell value+variance (Q-M/Q-Q); on-the-loop verbs configure/suspend/ack/override (Q-K)."},
 {"text":"New: capability self-report (G13/Q-V) and collective-task decomposition + report aggregation (Z1), from BML MUM-T tasking.","color":MGRAY},
], top=1.75, size=14.5, gap=12)
srcline(s, "ValidationEvidence-Walk.md  -  Documents-Needed/Found.md  -  log sec 6j  -  the 12 records in V2Extractions/")
footer(s)
notes(s,
 "The validation holes are now evidenced: explainability (DroneResponse), CBRN, EW geolocation, and persistence (MDARS) are each grounded in a documented mission rather than asserted.",
 "The headline discovery is prior art: WhoMeasuredType, in C2SIM's own BML lineage, already defines the measurement report this review flagged as missing - value, unit, phenomenon, sensor, time, place. Re-adopt rather than invent (Q-Q).")

# ---------------- v0.0.3 status ----------------
s = slide(); header(s, "Where the OWL is now (v0.0.3)", "Michael's update - the model is moving")
bullets(s, [
 {"tag":"Started (good):","tagcolor":GREEN,"text":"v0.0.3 begins the attribute layer (first datatype properties - v0.0.1 had none; plus further object properties) and folds the Video Detection Report into the OWL (MediaReference, MediaTypeCode, SensorObservation, VideoDetectionReportContent) + an AutonomyLevelCode model."},
 {"tag":"Brings a decision to a head:","tagcolor":ORANGE,"text":"P1 is now in the model, not yet settled - v0.0.3 declares both UAV/UGV (under Robot) and UnmannedAerial/Ground/Maritime/UnderwaterVehicle (under SMX Vehicle), so the group still picks one; the maritime ones sit under Vehicle rather than SurfaceVessel/SubsurfaceVessel."},
 {"tag":"Still to define:","tagcolor":ACCENT,"text":"the broader attribute set, a taskable collective (Swarm was removed; CollecticeRoboticSystem still non-actor), the generic Detection Report, and the rationale / robot-to-robot / area content - plus the two typos."},
 {"tag":"Coordination notes:","tagcolor":ORANGE,"text":"the branch also adds owl:imports smx/lox to base C2SIM.rdf - a circular import (C2SIM <-> smx) worth a deliberate decision; and AutonomyLevelCode is not yet wired as the range of hasAutonomousRoleCode (still generic Code)."},
], top=1.8, size=14, gap=11)
srcline(s, "log sec 9 (full reconciliation, finding by finding)  -  Ontology/C2SIM_ASX-v003.rdf on branch michael_d")
footer(s)
notes(s,
 "Section budget: slides 20-24, about 4 minutes; the decision slides are presented as a grouping, not read row by row.",
 "v0.0.3 moves the model: first datatype properties, the Video Detection Report folded into the OWL, an AutonomyLevelCode model. It also brings P1 to a head by declaring both trees - the group still picks one.",
 "Coordination notes worth a deliberate decision: the branch adds owl:imports smx/lox to base C2SIM.rdf (a circular import C2SIM <-> smx), and AutonomyLevelCode is not yet wired as the range of hasAutonomousRoleCode. The full finding-by-finding reconciliation is log sec 9.")

# ---------------- Decisions 1: model structure ----------------
s = slide(); header(s, "Decisions (1/3): model structure", "Full register - all 22, with what each resolves: log section 7")
bullets(s, [
 {"tag":"Q-A","tagcolor":ACCENT,"text":"UAV/robot typing: a role on the existing Platform tree, or a parallel Robot tree?"},
 {"tag":"Q-B","tagcolor":ACCENT,"text":"Swarm: derive from CollectiveEntity (ActorEntity) so it can be tasked."},
 {"tag":"Q-C","tagcolor":ACCENT,"text":"Sensor: entity, class, or attribute - choose one model and apply it everywhere."},
 {"tag":"Q-D","tagcolor":ACCENT,"text":"Autonomy: choose one normative vocabulary."},
], top=1.9, size=18, gap=18)
footer(s)
notes(s,
 "The ask, part 1 - structure: Q-A UAV/robot typing, Q-B a taskable swarm, Q-C one sensor model, Q-D one autonomy vocabulary. These four settle the shape of the model and unblock Initialization.",
 "The full text of all 22 decisions, each with what it resolves, is log sec 7 - present the grouping and point at the log rather than reading the register out.")

# ---------------- Decisions 2: new content ----------------
s = slide(); header(s, "Decisions (2/3): new content types needed", "continued - full text + grounding in log section 7")
bullets(s, [
 {"tag":"Q-E","tagcolor":ACCENT,"text":"Inline entity definition for newly-observed entities in reports."},
 {"tag":"Q-F","tagcolor":ACCENT,"text":"MediaReference identity; separate media-format from sensor-modality."},
 {"tag":"Q-G","tagcolor":ACCENT,"text":"Robot-to-robot coordination content type + issuing authority (CASEVAC)."},
 {"tag":"Q-H","tagcolor":ACCENT,"text":"Rationale/explanation ReportContent - report why, not just what (CASEVAC)."},
 {"tag":"Q-I","tagcolor":ACCENT,"text":"Media-independent sensor-reading (value+unit+modality) + full SensorType taxonomy."},
 {"tag":"Q-J","tagcolor":ACCENT,"text":"Swarm residuals: network params, leader role, aggregation, member lifecycle."},
 {"tag":"Q-K","tagcolor":ACCENT,"text":"Engagement authority as a function of autonomy level (Fire Support)."},
 {"tag":"Q-L","tagcolor":ACCENT,"text":"Typed payload/effector/weapon (the action verbs already exist in LOX; only tow/salvage is a residual)."},
 {"tag":"Q-M","tagcolor":ACCENT,"text":"Let an area be the subject of a task/report (hasAffectedArea + area-state)."},
], top=1.6, size=13.5, gap=8)
footer(s)
notes(s,
 "Part 2 - new content types, mostly report and order payloads: inline entity definition, media identity, robot-to-robot coordination, rationale reports, media-independent sensor readings, swarm residuals, engagement authority, payload/effector/weapon typing, area as subject.",
 "Each of these traces back to a walk finding on an earlier slide - the CASEVAC pair (Q-G, Q-H) and the sensor pair (Q-I with Q-Q) carry the most scenario evidence.")

# ---------------- Decisions 3: from sourced scenarios ----------------
s = slide(); header(s, "Decisions (3/3): from the sourced scenarios", "continued - full text + grounding in log section 7")
bullets(s, [
 {"tag":"Q-N","tagcolor":ACCENT,"text":"Area-coverage / exploration goal (explore-until-covered) - search verbs already exist."},
 {"tag":"Q-O","tagcolor":ACCENT,"text":"Denied-comms operating mode + deployable relay entity (the relay verb lox#COMREL already exists)."},
 {"tag":"Q-P","tagcolor":ACCENT,"text":"Cross-cueing: system-to-system tasking + shared classified track/contact (extends Q-G)."},
 {"tag":"Q-Q","tagcolor":ACCENT,"text":"One generic Detection Report (confidence + error-bound + false-positive) - resolves Y1/M3/M4 (extends Q-I)."},
 {"tag":"Q-R","tagcolor":ACCENT,"text":"Platform locomotion/role subtypes: wheeled/tracked/legged UGV; detector/neutralizer USV (extends Q-A)."},
 {"tag":"Q-S","tagcolor":ACCENT,"text":"Decoy/deception behavior + threat-aware order annotations."},
 {"tag":"Q-T","tagcolor":ACCENT,"text":"Operating-environment condition attributes (GPS-denied, illumination, sea-state, terrain)."},
 {"tag":"Q-U","tagcolor":ACCENT,"text":"Formation / relative-geometry construct (orbit, convoy spacing) beyond single RelativeLocation."},
 {"tag":"Q-V","tagcolor":ACCENT,"text":"Capability self-report (robot declares mounted equipment; assign by capability) - BML WhoHoldingType."},
], top=1.55, size=13, gap=7)
footer(s)
notes(s,
 "Part 3 - decisions raised by the sourced scenarios: exploration goals, denied-comms relay, cross-cueing, the generic detection report, locomotion subtypes, decoy/deception, environment conditions, formation geometry, capability self-report.",
 "Several of these re-adopt existing vocabulary (search verbs, lox#COMREL, BML WhoHoldingType) rather than invent - the decision is where to hang the structure, not whether the words exist.")

# ---------------- Plan semantics vs standards (6k) ----------------
s = slide(); header(s, "Plan semantics vs robotic behavior standards (6k)",
                    "Independent standards pass + module verification - decisions Q-W..Q-Z")
bullets(s, [
 {"tag":"Compared:","tagcolor":NAVY,"text":"base C2SIM plan machinery vs BT/Nav2, PDDL, FlexBE, MAVLink, IEEE 1872.1-2024, JAUS AS6062, STANAG 4586 - every C2SIM-side claim verified against the RDF."},
 {"tag":"Base standard:","tagcolor":GREEN,"text":"strong on classical planning (sequencing, hierarchy, an 18-code temporal algebra incl. 6 concurrency codes) - absent on the autonomy-execution half (failure, state conditions, goals, loops, authority)."},
 {"tag":"Module draft:","tagcolor":GREEN,"text":"already covers the core of that half (fallback, state conditions, goals, repetition, authority gate) - the standards pass independently re-derived the same construct set (corroboration, not invention)."},
 {"tag":"v0.0.3 adds:","tagcolor":ACCENT,"text":"plan identity/supersession, suspension state, task accept/reject, lost-link failsafe, keep-in/keep-out areas, structured waypoints - each with JAUS / STANAG / MAVLink prior art."},
 {"tag":"Decisions:","tagcolor":ACCENT,"text":"Q-W review/adopt the module (resolves PL1-PL4, PL6); Q-X plan-lifecycle v-next deltas; Q-Y failsafe/geofence binding; Q-Z STANAG-grade waypoints - plus a consolidated PDG errata package (PL11 + the module's core errata)."},
], top=1.8, size=14, gap=11)
srcline(s, "PlanSemantics-Walk.md  -  log sec 6k (PL1-PL11)  -  decisions Q-W..Q-Z (log sec 7)")
footer(s)
notes(s,
 "An independent pass compared the base standard's plan machinery with ten robotic/agent standards (BT/Nav2, PDDL, FlexBE, MAVLink, IEEE 1872.1-2024, JAUS AS6062, STANAG 4586, 4D/RCS, HTN, FIPA/BDI); every C2SIM-side claim was verified in the RDF. Result: a strong classical-planning core, and an absent autonomy-execution half - failure, state conditions, goals, loops, authority.",
 "The plan-semantics module draft (branch asx-plan-semantics) already covers the core of that half, and the standards pass independently re-derived the same construct set - corroboration, not invention. Findings PL1-PL11 in log sec 6k; decisions Q-W..Q-Z.")

# ---------------- Proposed fixes (pending buy-in) ----------------
s = slide(); header(s, "Proposed refinements", "Pending group buy-in - nothing applied to the model")
bullets(s, [
 {"tag":"Safe corrections (unambiguous):","tagcolor":GREEN,"text":"class typo CollecticeRoboticSystem -> CollectiveRoboticSystem (O1); versionInfo Extrension -> Extension (O2); file CSIM_ASX -> C2SIM_ASX (O3); hasStartTime UUIDBase -> TimeInstant (M7); unify namespace label ASX / C2SIM_ASX (M8)."},
 {"tag":"Structural (decide first):","tagcolor":ORANGE,"text":"UAV/robot typing (Q-A); Swarm -> CollectiveEntity so it is taskable (Q-B); one sensor model (Q-C); one autonomy vocabulary (Q-D)."},
 {"tag":"New content (design):","tagcolor":ACCENT,"text":"inline entity def (Q-E), MediaReference (Q-F), robot-to-robot + cross-cue (Q-G/Q-P), rationale report (Q-H), generic detection report (Q-I/Q-Q), swarm residuals (Q-J), engagement authority (Q-K), payload/effector/weapon typing (Q-L), area subject (Q-M), explore order (Q-N), denied-comms/relay (Q-O), locomotion subtypes (Q-R), decoy/threat-aware (Q-S), environment conditions (Q-T), formation geometry (Q-U)."},
 {"text":"Nothing here is applied to the model - all items are proposals for group buy-in.","bold":True},
], top=1.7, size=14, gap=13)
srcline(s, "log secs 3-4 (the safe corrections)  -  sec 7 (every decision, with what it resolves)")
footer(s)
notes(s,
 "Section budget: slides 25-26, about 1 minute - the close.",
 "The same decisions, grouped by commitment level: safe corrections (typos, the UUIDBase slip) are unambiguous; structural decisions need the group; content types need design. Nothing has been applied to the model or the workbooks - all items are proposals pending buy-in.")

# ---------------- Next steps ----------------
s = slide(); header(s, "Recommended next steps")
bullets(s, [
 {"text":"Settle the two entity-typing decisions (Q-A, Q-B) - this unblocks Initialization.","bold":True},
 {"text":"Complete the Initialization instantiations (drafts provided for the 3 named scenarios)."},
 {"text":"Add the two CASEVAC content types (Q-G robot-to-robot, Q-H rationale) - both are explicit scenario requirements."},
 {"text":"Reconcile the OWL model with the June spreadsheet decisions; fix the typos."},
 {"text":"Optional: adopt the diff-able (.xml) workbooks so edits can be reviewed and merged in git."},
], top=1.8, size=16.5, gap=12)
srcline(s, "Group-Briefing.md ('Status and next step')  -  log sec 7 for the full decision register")
footer(s)
notes(s,
 "The recommended order: settle Q-A / Q-B first (they unblock Initialization), complete the Initialization instantiations, add the two CASEVAC content types, reconcile the two tracks and fix the typos, and optionally adopt the diff-able workbooks so message edits can be reviewed in git.",
 "Where the ball is: sourcing is essentially complete - every gap this review raised is grounded in a real mission (one nice-to-have left: a dedicated autonomous-CASEVAC mission). The remaining work - the attribute layer, the reconciliation, the 22 decisions - is modeling work; more scenarios will not fill it.")

# ---------------- How to use this material (reading guide) ----------------
s = slide(); header(s, "How to use this material", "Reading paths by time budget - each level builds on the previous")
table(s, [
 ["Budget", "Read this", "You come away with"],
 ["5 minutes",
  "Group-Briefing.md - one page",
  "what this is, what was found, the ~22 decisions, where the ball is"],
 ["30 minutes",
  "this deck - the speaker notes on each slide carry the talk track; the ask is the three Decisions slides, structure first (Q-A..Q-D)",
  "the full findings picture and what the group is asked to settle"],
 ["1-2 hours",
  "the walk doc for your topic (map on the final slide), then the log section it feeds - every ID resolves to one row with severity, status, and evidence",
  "a reviewer-grade view of one finding family, with its evidence"],
 ["Half a day",
  "Issues-And-Comments-Log.md end to end, with the three ASX Sample *.xml workbooks and Anticipated-QA.md beside it",
  "command of the full evidence trail - every claim, message, and decision"],
], top=1.65, col_w=[1.5, 6.5, 4.0], size=12, row_h=0.78)
bullets(s, [
 {"tag":"Seeing the actual messages:","tagcolor":ACCENT,"text":"open the three ASX Sample *.xml workbooks in Excel - one tab per message, same columns as the originals; the Notes column flags open items [!] and questions [Q], keyed to log IDs."},
 {"tag":"Challenging a claim:","tagcolor":ORANGE,"text":"the log's evidence column cites the exact RDF entity (C2SIM / SMX / LOX / v0.0.3) - grep it; every claim was independently re-verified (log change log, 2026-07-12)."},
], top=5.75, size=12, gap=5)
footer(s)
notes(s,
 "Reading paths by time budget. The 5-minute path (Group-Briefing.md) is the default pointer for anyone who missed the meeting; the half-day path is for reviewers who want to challenge the evidence.",
 "Every ID on these slides resolves to exactly one log row - the decoder ring on the next slide maps each family.")

# ---------------- Finding-ID decoder ring ----------------
s = slide(); header(s, "Finding-ID decoder ring", "Every ID resolves to one row or section - nothing is free-floating")
table(s, [
 ["ID family", "What it names", "Where it resolves"],
 ["P1 - P7", "entity-typing findings: UAV (P1), sensor (P2), swarm (P7)", "log sec 5; Initialization-Walk.md"],
 ["D / O / M", "track alignment / OWL typos / sample-message items", "log secs 2 / 3 / 4"],
 ["S", "process + repo-sync decisions (e.g. diff-able workbooks, S4)", "log sec 1"],
 ["C1 - C8", "coverage state, scenario x message type", "log sec 6"],
 ["X", "CASEVAC walk findings", "log sec 6b; CASEVAC-Walk.md"],
 ["Y / Z", "sensor / swarm walk findings", "log secs 6c / 6d; NonVideoSensors- / Swarm-Walk.md"],
 ["W / L / E / R", "fire support / logistics / engineering / rescue findings", "log secs 6e / 6f; FireSupport- / TaskEffect-Batch-Walk.md"],
 ["N", "redundancy-pass findings", "log sec 6g; RedundancyPass-Walk.md"],
 ["G", "sourced-scenario + validation findings", "log secs 6h-6j; SourcedScenarios- / ValidationEvidence-Walk.md"],
 ["PL1 - PL11", "plan-semantics standards findings", "log sec 6k; PlanSemantics-Walk.md"],
 ["Q-A .. Q-V", "the 22 decisions this review puts to the group", "log sec 7 - full text + what each resolves"],
 ["Q-W .. Q-Z", "plan-semantics decisions (module, lifecycle, failsafe, routes)", "log sec 7"],
], top=1.6, col_w=[1.9, 5.8, 4.3], size=11.5, hdr_size=12, row_h=0.385)
bullets(s, [
 {"text":"An unfamiliar ID in any document is a pointer, not jargon - the right column lands on its definition, evidence, and status.","color":NAVY},
], top=6.62, size=11.5)
footer(s)
notes(s,
 "Every ID family, what it names, and where it resolves. An unfamiliar ID in any document is a pointer, not jargon - each one lands on a definition, its evidence, and its current status.",
 "This slide plus the next one are the handout scaffolding: leave them with the group.")

# ---------------- Where to dig deeper (reference map) ----------------
s = slide(); header(s, "Where to dig deeper", "Branch asx-diffable-spreadsheets: docs in ASX/InstantiationReview, workbooks in ASX/Proposed Extension Working Materials")
bullets(s, [
 {"tag":"Master evidence log:","tagcolor":NAVY,"text":"Issues-And-Comments-Log.md - every finding, the 22 decisions (sec 7), v0.0.3 reconciliation (sec 9), why gaps remain (sec 8)."},
 {"tag":"Briefing / Q&A / talk track:","tagcolor":NAVY,"text":"Group-Briefing.md (one page); Anticipated-QA.md; Presenter-Notes.md."},
 {"tag":"Coverage + the actual messages:","tagcolor":NAVY,"text":"Message-Instantiation-Coverage.md; the three 'ASX Sample *.xml' workbooks (the ~33 instantiations, diff-able)."},
 {"tag":"Initialization & entity typing (P1/P2/P7):","tagcolor":NAVY,"text":"Initialization-Walk.md; log sec 5."},
 {"tag":"CASEVAC (X1/X2 -> Q-G/Q-H):","tagcolor":NAVY,"text":"CASEVAC-Walk.md; log sec 6b."},
 {"tag":"Sensors & swarm (Y / Z series):","tagcolor":NAVY,"text":"NonVideoSensors-Walk.md; Swarm-Walk.md; log sec 6c / 6d."},
 {"tag":"Task / effect & engagement (W / L, Q-K/Q-L):","tagcolor":NAVY,"text":"FireSupport-Walk.md; TaskEffect-Batch-Walk.md; log sec 6e / 6f."},
 {"tag":"Sourced & validation missions:","tagcolor":NAVY,"text":"SourcedScenarios-Walk.md; ValidationEvidence-Walk.md; Documents-Found.md; log sec 6h / 6j."},
 {"tag":"Plan semantics (PL series, Q-W..Q-Z):","tagcolor":NAVY,"text":"PlanSemantics-Walk.md; log sec 6k."},
 {"tag":"Redundancy screen (N1):","tagcolor":NAVY,"text":"RedundancyPass-Walk.md; log sec 6g."},
], top=1.65, size=12, gap=5)
footer(s)
notes(s,
 "The topic-to-doc map. Everything is on branch asx-diffable-spreadsheets: review docs in Subgroups/ASX/InstantiationReview, workbooks in Subgroups/ASX/Proposed Extension Working Materials. The .md files render directly on GitHub - switch branch and browse; no tooling needed.",
 "The plan-semantics module itself (TTL draft, analysis, validation walks) lives on branch asx-plan-semantics; PlanSemantics-Walk.md here is the independent standards pass that checked it.")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ASX-Instantiation-Findings.pptx")
prs.save(out)
print("saved:", out, "slides:", len(prs.slides._sldIdLst))
