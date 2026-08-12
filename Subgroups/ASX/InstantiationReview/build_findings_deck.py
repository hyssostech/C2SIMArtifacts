"""Builds ASX-Instantiation-Findings.pptx (23 slides) - findings from
instantiating the proposed ASX extension against 20+ scenarios. Every slide
carries speaker notes with the talk track (team-facing; Presenter-Notes.md is
the section-level view of the same track).

Structure (2026-08-11 revision, per Paulo's review): one consolidated
model-state slide (was three); the method slide dropped (old news to the
group - the one-sentence version lives on slide 2 and in the process slide's
notes); a P2 slide alongside P1/P7, all three detail slides on the same
four-beat skeleton (problem / consequence / current state / decision); the
findings block organized by theme (re-adopt / content types / typing /
authority), each theme slide on the same geometry (one full-width flagship
box + tagged bullets), with scenarios cited as evidence instead of by
scenario/provenance. The old M-series and coverage-recap slides are gone -
their unique content lives on the scenario, content-types, and refinements
slides."""

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
 "Time plan for a 30-minute slot: opening (slides 1-2) ~3 min; how it was produced + deliverables (3-4) ~4 min; where the instantiation stands (5-6) ~4 min; model state + the structural block (7-11) ~7 min; findings by theme (12-15) ~6 min; the decision register (16-19) ~4 min; close (20) ~1 min. Slides 21-23 are the reading guide - point at them, do not present them.",
 "If the slot is 20 minutes: slides 1-2, 4, 7-11, the decisions grouping (16), and next steps (20); everything else is handout material.")

# ---------------- The whole review in one slide ----------------
s = slide(); header(s, "The whole review in one slide", "The 90-second version - everything after this is detail")
bullets(s, [
 {"tag":"What was done:","tagcolor":NAVY,"text":"walked 20+ scenarios into ~34 new worked messages (4 -> ~38) using C2SIM + the proposed ASX elements, in diff-able workbooks - Initialization 0 -> 7, Orders 2 -> 17, Reports 2 -> 14."},
 {"tag":"What it surfaced:","tagcolor":NAVY,"text":"three structural typing decisions come first - UAV/robot typing (P1), sensor representation (P2), a taskable swarm (P7) - and behind them an attribute layer still to be built (v0.0.1 had 0 datatype properties; v0.0.3 starts it)."},
 {"tag":"The good news:","tagcolor":GREEN,"text":"much of what is missing is re-adopt, not invent - BML WhoMeasuredType for measurements, 446 LOX task verbs, ROE / routes / resources already in the base standard."},
 {"tag":"The ask:","tagcolor":ACCENT,"text":"24 concrete decisions (Q-A..Q-X, log sec 7) - settle the four structural ones (Q-A..Q-D) first; they unblock Initialization."},
 {"tag":"Status:","tagcolor":ORANGE,"text":"everything is a proposal - nothing applied to the OWL or the .xlsx; every RDF-grounded claim was independently re-verified."},
], top=1.75, size=14.5, gap=12)
srcline(s, "Group-Briefing.md is the one-page prose version of this slide")
footer(s)
notes(s,
 "The one-slide version of the talk. If discussion takes over later, this slide plus the decision register (slides 16-18) is the minimum to land.",
 "Grounding for the numbers: the counts are the coverage rows in log sec 6 (C1-C9). The re-adopt items were verified against the RDF, not recalled: WhoMeasuredType is in C2SIM's BML lineage; LOX carries 446 TaskActionCode verbs; ROE, routes, resources, and a neutral hostility value (smx#NEUTRL) exist in the base standard.")

# ---------------- Process: three sessions + verification ----------------
s = slide(); header(s, "How this was produced: three sessions + a verification pass",
                    "LLM-assisted, human-directed - each stage grounded in the artifacts, not memory")
rbox(s, 0.7, 1.9, 3.7, 1.7, "1  -  Document mining\n\nHunt primary mission documents (theses, tech reports, AARs) for missing domains + validation holes", NAVY, size=12.5)
rbox(s, 4.8, 1.9, 3.7, 1.7, "2  -  Scenario extraction\n\nA locked v2.2 prompt distills each document into a standardized scenario record (15 records)", NAVY, size=12.5)
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
 "Section budget: slides 3-4, about 4 minutes.",
 "The method in one sentence (the dedicated method slide was dropped as familiar ground): write the messages each scenario actually needs; where an element is not yet defined enough to instantiate cleanly, that marks a concrete thing to specify next - not a defect. Scope note: the sample-message workbooks were converted to a diff-able .xml format so instantiations can be reviewed in git; the original .xlsx are untouched.",
 "Three coordinated sessions plus an independent check: document mining hunts primary mission documents; scenario extraction distills each into a standardized record with the locked v2.2 prompt; ontology application walks each scenario into concrete messages against the proposed elements. The verification pass then re-checked every RDF-grounded claim, the workbook fidelity, and the citations, with corrections logged (issues log change log, 2026-07-12).",
 "The stages iterate: the walk writes the sourcing brief (Documents-Needed), mining answers it (Documents-Found), extraction feeds the walk. Nothing rests on an LLM's memory - every claim is grounded in the RDF, the workbooks, or a named source, and was independently re-verified.")

# ---------------- What this review contributes ----------------
s = slide(); header(s, "What this review contributes", "Five deliverables - all proposals, nothing applied to the OWL or the .xlsx")
bullets(s, [
 {"tag":"1  Message instantiations:","tagcolor":NAVY,"text":"~34 new worked messages (4 -> ~38; Initialization 0 -> 7) in diff-able .xml workbooks - one tab per message, with open items flagged [!]/[Q] in the Notes column, keyed to log IDs."},
 {"tag":"2  Sourced scenario corpus:","tagcolor":NAVY,"text":"15 standardized extraction records from real missions (subterranean, maritime MCM, sustainment, explainability, CBRN, EW, persistence, counter-UAS, MUM-T, SAR, formation, breach, + the SME drone-warfare thread: LIRC baseline / update / OPFOR targeting) + the source PDFs - every gap this review raised is grounded in a documented mission."},
 {"tag":"3  Findings -> decisions:","tagcolor":NAVY,"text":"a consolidated issues log (severity / status / RDF-verified evidence per finding) distilled into 24 concrete decisions for the group (Q-A..Q-X)."},
 {"tag":"4  v0.0.3 reconciliation:","tagcolor":NAVY,"text":"how each finding moves against Michael's update - what it adopts, what it makes concrete, what remains - plus coordination notes (two ASX files, import layering)."},
 {"tag":"5  Prior art to re-adopt:","tagcolor":NAVY,"text":"the measurement report exists in C2SIM's own BML lineage (WhoMeasuredType); ROE, routes, resources, membership/command, maritime vessels, and 446 task verbs already exist in the base standard - several decisions are re-adopt, not invent."},
], top=1.7, size=14.5, gap=12)
srcline(s, "the full artifact map is on the final three slides ('How to use this material' / decoder ring / 'Where to dig deeper')")
footer(s)
notes(s,
 "Five deliverables: ~34 new message instantiations in diff-able workbooks; a 15-record sourced scenario corpus; a findings log distilled into 24 decisions; a finding-by-finding reconciliation with v0.0.3; and the prior-art discoveries (BML WhoMeasuredType first among them). All proposal-only.",
 "This slide frames the rest of the talk: each later section shows where one of these deliverables came from.")

# ---------------- State of play ----------------
s = slide(); header(s, "Where the instantiation stands", "From 4 worked messages to ~38 - this review is the bulk of that")
bullets(s, [
 {"text":"Start: 4 worked instances (2 Reports, 2 Orders, 0 Initialization) - Elizabeth's baseline. This review drafted ~34 more, to ~38 across Init / Order / Report (on the branch, pending group review).","bold":True},
 {"text":"Initialization   0 -> 7   (the 3 named scenarios + CASEVAC / MCM / SubT / LIRC) - was the least-developed; now seeded.","lvl":1},
 {"text":"Orders   2 -> 17   (CASEVAC, swarm, fire support, logistics / engineering / rescue, route clearance, MCM, explore, resupply, MUM-T, kill-box engagement, counter-UAS, OPFOR targeting).","lvl":1},
 {"text":"Reports   2 -> 14   (swarm, CASEVAC status / explainable, CBRN / EW / GPR, BDA, delivery, naval mine, generic detection, hazard area, LIRC strike BDA).","lvl":1},
 {"text":"CASEVAC - the one contributed scenario - had no messages; now walked end-to-end (Init + Orders + Reports).","bold":True},
 {"text":"The breadth is the point: each new instance exercises a proposed element and surfaces what is still to define.","lvl":1},
], top=1.75, size=15, gap=9)
srcline(s, "Message-Instantiation-Coverage.md (the pre-walk baseline)  -  log sec 6 rows C1-C9 (current state)  -  the three ASX Sample *.xml workbooks (the messages themselves)")
footer(s)
notes(s,
 "Section budget: slides 5-6, about 4 minutes.",
 "The baseline was 4 worked instances (2 Reports, 2 Orders, 0 Initialization) - Elizabeth's sample-message workbooks. This review drafted ~34 more, to ~38: Initialization 0 -> 7, Orders 2 -> 17, Reports 2 -> 14. The breadth - not any single message - is what surfaced the to-define items.",
 "CASEVAC, the one contributed (human-authored) scenario, had no messages; it is now walked end to end: Init -> tasking Order -> robot-to-robot hand-off -> status / threat / explainable Reports.")

# ---------------- Scenarios analyzed (showcase) ----------------
s = slide(); header(s, "Scenarios analyzed", "20+ scenarios walked into ~38 message instances - Init / Order / Report")
bullets(s, [
 {"text":"Named + contributed - instantiated end-to-end:","bold":True},
 {"text":"the 3 named Init scenarios (UAV video, UAV patrol, swarm) + CASEVAC, the one human-authored contributed scenario - walked Init -> tasking Order -> robot-to-robot hand-off -> status/threat + explainable Reports.","lvl":1},
 {"text":"Capability stress-tests - instantiated:","bold":True},
 {"text":"non-video sensing (CBRN, EW emitter, GPR mine); swarm detect + coordinate; the task/effect axis (fire support + BDA, logistics delivery, engineering, USV rescue, route clearance).","lvl":1},
 {"text":"Newly sourced from real missions, then analyzed:","bold":True},
 {"text":"Cooperative MCM (maritime), Subterranean SubT, contested sustainment - plus nine documented missions that grounded the validation holes: explainability (DroneResponse), CBRN (UGV), EW geolocation, persistence (MDARS), counter-UAS, human-machine teaming (MUM-T), SAR, formation, robotic breach.","lvl":1},
 {"text":"Screened for redundancy:","bold":True},
 {"text":"route-clearance / companion / urban - confirmed ~80% redundant, but still yielded N1 (an area as the subject of a task/report).","lvl":1},
 {"tag":"Evidence pedigree:","tagcolor":GREEN,"text":"every gap raised is grounded in a documented real mission - 15 sourced extraction records; the validation pass closed the asserted-but-untested holes (explainability, CBRN, EW, persistence)."},
], top=1.7, size=13, gap=7)
srcline(s, "one walk doc per scenario family (see final slide)  -  the 15 sourced records: LLMExperiments/PaperSummaries/V2Extractions/  -  ValidationEvidence-Walk.md")
footer(s)
notes(s,
 "Four groups: named + contributed scenarios instantiated end to end; capability stress-tests (non-video sensors, swarm, task/effect); missions sourced from real documents by the parallel sourcing effort (Cooperative MCM, SubT, sustainment, plus nine documented missions that closed the validation holes); and a redundancy screen that still yielded one new finding (N1).",
 "The pedigree line matters: every gap the findings slides raise is grounded in a documented mission - the 15 sourced extraction records - and the validation pass turned the asserted-but-untested holes (explainability via DroneResponse, CBRN, EW geolocation, persistence via MDARS) into evidenced ones.",
 "Provenance, stated precisely: the MUTT-derived scenarios are LLM-generated; CASEVAC is human-authored; the sourced missions come from real papers - two carry fidelity caveats (EW and the robotic breach), noted in their extraction records.")

# ---------------- Where the model stands (consolidated state) ----------------
s = slide(); header(s, "Where the model stands", "Two tracks, one early model - moving, with a known catch-up list")
rbox(s, 0.7, 1.75, 3.7, 1.35, "OWL v0.0.1  (Jan 2026)\n15 classes, 1 object property,\n0 datatype properties", NAVY, size=12)
rbox(s, 4.8, 1.75, 3.7, 1.35, "Spreadsheets  (Feb-Jun 2026)\nthe attribute layer: Payload,\nMobility, VehicleType, ...", ACCENT, size=12)
rbox(s, 8.9, 1.75, 3.7, 1.35, "OWL v0.0.3  (Jul 2026, Michael)\nfirst datatype properties, Video\nDetection Report, AutonomyLevelCode", GREEN, size=12)
arrow(s, 4.4, 2.4, 4.8, 2.4, ORANGE); arrow(s, 8.5, 2.4, 8.9, 2.4, GREEN)
bullets(s, [
 {"tag":"Outlook:","tagcolor":GREEN,"text":"an early (v0.0.x) model whose two tracks evolved separately for ~5 months - expected at this stage. v0.0.3 shows the OWL moving, and puts the key typing choice (P1) concretely in the model to settle."},
 {"tag":"Catching up - attribute layer:","tagcolor":ORANGE,"text":"Payload, PayloadCapability, Mobility/Propulsion, VehicleType, PassengerCapability, mission/swarm parameters are in the spreadsheets, not yet in the OWL (D3); v0.0.3 begins the layer, for the Video Detection Report only."},
 {"tag":"Catching up - one autonomy vocabulary:","tagcolor":ORANGE,"text":"three today - OWL {Automated, FullAuto, ReCont, Teleop} vs ControlMode {Piloted, Unpiloted-Autonomous, Swarm} vs NavigationAutonomy {FPV, Autonomous, RemoteControl} (D1 -> Q-D)."},
 {"tag":"Catching up - one sensor model:","tagcolor":ORANGE,"text":"three today - Sensor class vs SensorType enum vs SensorCapability equipment (D2 -> Q-C); this is structural decision P2, next section."},
 {"tag":"Wiring to settle deliberately:","tagcolor":MGRAY,"text":"AutonomyLevelCode is not yet the range of hasAutonomousRoleCode (still generic Code); the v0.0.3 branch adds owl:imports smx/lox to base C2SIM.rdf - a circular import (C2SIM <-> smx)."},
], top=3.35, size=13, gap=8)
srcline(s, "log secs 1-2 (S2, D1-D5)  -  sec 9 (v0.0.3 reconciliation, finding by finding)  -  Ontology/C2SIM_ASX-v003.rdf on branch michael_d")
footer(s)
notes(s,
 "Section budget: slides 7-11, about 7 minutes - the core of the talk.",
 "The outlook in one line: the OWL (v0.0.1, January) and the spreadsheets (June) evolved separately, so several findings look like drift rather than gaps; v0.0.3 (July) shows the model moving - first datatype properties (v0.0.1 had none), the Video Detection Report folded into the OWL, an AutonomyLevelCode model - and brings P1 concretely into the model by declaring both typing trees.",
 "The catch-up list is short and known: the attribute layer, one autonomy vocabulary (three today), one sensor model (three today - that is P2, next section), and two wiring items (the hasAutonomousRoleCode range, the circular owl:imports). Everything else v0.0.3 still lacks - taskable collective, generic Detection Report, rationale / robot-to-robot / area content, the two typos - appears on its own slide later. Full finding-by-finding reconciliation: log sec 9.")

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
 "The point to land: because all three are typing decisions, Initialization - not Reports - is where the model has to be settled first. The next three slides take P1, P2, and P7 one at a time.")

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
 {"text":"Type it as Robot and it loses all existing SMX Platform / LOX machinery; type it as Aircraft and the ASX Robot / UAV classes go unused.","lvl":1},
 {"tag":"Now in v0.0.3:","tagcolor":ORANGE,"text":"both trees are declared - UAV/UGV under Robot AND UnmannedAerial/Ground/Maritime/UnderwaterVehicle under SMX Vehicle - so this choice is now in the model to settle."},
 {"tag":"Decision (Q-A):","tagcolor":ACCENT,"text":"make ASX autonomy a role/facet on the existing Platform subtree instead of a parallel Robot tree?"},
], top=4.85, size=13, gap=6)
srcline(s, "Initialization-Walk.md  -  log P1 (sec 5) + sec 9 (v0.0.3 makes it concrete)  -  decision Q-A (log sec 7)")
footer(s)
notes(s,
 "The proposed Robot class tree runs parallel to the existing SMX Platform tree, both under ActorEntity - two incompatible types for the same real drone. Type it as Robot and it loses the Platform machinery; type it as Aircraft or Vehicle and the ASX classes go unused.",
 "v0.0.3 declares both trees, so the choice is now concretely in the model to settle (note: its maritime classes sit under Vehicle rather than SurfaceVessel/SubsurfaceVessel). Decision Q-A proposes autonomy as a role/facet on the existing Platform subtree.")

# ---------------- P2 diagram ----------------
s = slide(); header(s, "P2  -  A sensor is modeled three ways", "Representation decision")
rbox(s, 4.4, 1.7, 4.5, 0.75, "the same physical sensor\n(EO camera, CBRN sniffer, GPR)", NAVY, size=12)
rbox(s, 0.9, 3.3, 3.6, 0.85, "Sensor class\n(OWL)", ORANGE, size=13)
rbox(s, 4.85, 3.3, 3.6, 0.85, "SensorType enum\n(Concept Mapping)", ORANGE, size=13)
rbox(s, 8.8, 3.3, 3.6, 0.85, "SensorCapability as equipment\n(Concept Mapping)", ORANGE, size=12)
arrow(s, 5.6, 2.45, 2.7, 3.3); arrow(s, 6.65, 2.45, 6.65, 3.3); arrow(s, 7.7, 2.45, 10.6, 3.3)
bullets(s, [
 {"text":"Three incompatible representations of the same device across the two tracks (D2)."},
 {"text":"An Initialization message must declare what a platform carries - it has to pick one representation; the Report side only consumes sensor output (log P2).","lvl":1},
 {"tag":"Same pattern downstream:","tagcolor":ORANGE,"text":"weapon (W2), manipulator (E2), cargo (L1) hang off the same carried-equipment choice (Q-L); non-imaging sensor reports (Y1) need the sensor typed to say what measured (Q-I/Q-Q)."},
 {"tag":"Decision (Q-C):","tagcolor":ACCENT,"text":"is a sensor a first-class entity/equipment, a class, or an attribute? Pick one model and apply it in Init, Report, and Concept Mapping."},
], top=4.85, size=13, gap=6)
srcline(s, "Initialization-Walk.md + NonVideoSensors-Walk.md  -  log P2 (sec 5) + D2 (sec 2)  -  decision Q-C (log sec 7)")
footer(s)
notes(s,
 "The sensor has no agreed representation: an OWL Sensor class, a SensorType enum, and SensorCapability as associated equipment - three incompatible models of the same physical device (D2).",
 "Initialization is what forces the choice: an Init message must declare what a platform carries, so it has to pick one representation; the Report side only consumes sensor output (log P2). The same carried-equipment pattern returns in weapon / manipulator / cargo typing (W2/E2/L1 -> Q-L) and in non-imaging sensor reports (Y1 -> Q-I/Q-Q). Decision Q-C: pick one model and apply it everywhere.")

# ---------------- P7 diagram ----------------
s = slide(); header(s, "P7  -  A swarm is not yet taskable", "Entity-typing decision")
rbox(s, 0.9, 2.0, 3.1, 0.7, "Swarm  (ASX)", ORANGE, size=13)
rbox(s, 4.3, 2.0, 3.6, 0.7, "CollecticeRoboticSystem (sic)", ORANGE, size=12)
rbox(s, 8.2, 2.0, 3.4, 0.7, "... PhysicalEntity", RED, size=13)
arrow(s, 4.0, 2.35, 4.3, 2.35, RED); arrow(s, 7.9, 2.35, 8.2, 2.35, RED)
tb, tf = box(s, 8.2, 2.75, 3.6, 0.4); p=tf.paragraphs[0]
set_run(p.add_run(), "not yet taskable (under PhysicalEntity)", 12, ORANGE, italic=True)
rbox(s, 0.9, 3.55, 3.1, 0.7, "Swarm  (proposed)", GREEN, size=13)
rbox(s, 4.3, 3.55, 3.6, 0.7, "CollectiveEntity  (C2SIM)", GREEN, size=12)
rbox(s, 8.2, 3.55, 3.4, 0.7, "ActorEntity", GREEN, size=13)
arrow(s, 4.0, 3.9, 4.3, 3.9, GREEN); arrow(s, 7.9, 3.9, 8.2, 3.9, GREEN)
tb, tf = box(s, 8.2, 4.3, 3.6, 0.4); p=tf.paragraphs[0]
set_run(p.add_run(), "taskable - receives orders, reports", 12, GREEN, italic=True)
bullets(s, [
 {"text":"A swarm is what orders are addressed to and what sends reports - so it needs to be an ActorEntity."},
 {"text":"Membership and command already exist in the base standard (C2SIM hasSubordinate, SMX hasCommandRelation), so the residual swarm work is small.","lvl":1},
 {"tag":"Now in v0.0.3:","tagcolor":ORANGE,"text":"the Swarm class was dropped; CollecticeRoboticSystem (sic) remains under PhysicalEntity - still not taskable."},
 {"tag":"Decision (Q-B):","tagcolor":ACCENT,"text":"derive the collective/Swarm from CollectiveEntity (already an ActorEntity) rather than the device/artifact tree."},
], top=4.85, size=13, gap=6)
srcline(s, "Swarm-Walk.md  -  log P7 (secs 5, 6d)  -  decision Q-B (log sec 7)")
footer(s)
notes(s,
 "The swarm classes derive from the device/artifact side (PhysicalEntity), but orders are addressed to - and reports come from - an ActorEntity. The fix is already in the base standard: derive the collective from CollectiveEntity. Membership and command relations already exist (C2SIM hasSubordinate, SMX hasCommandRelation), so the residual swarm work is small.",
 "Note the current state: v0.0.3 dropped the Swarm class, and CollecticeRoboticSystem (the typo is in the model - O1) is still under PhysicalEntity. Decision Q-B.")

# ---------------- Findings 1: already in the standard ----------------
s = slide(); header(s, "Already in the standard - re-adopt, not invent", "Verified in the RDF - the gap list is shorter than it looks")
rbox(s, 0.8, 1.85, 11.75, 1.4, "The headline discovery: the measurement report already exists\n\nBML lineage WhoMeasuredType {value, unit, phenomenon, sensor, time, place} - flagged as missing, found in C2SIM's own lineage. Re-adopt, not invent (Q-Q).", GREEN, size=13)
bullets(s, [
 {"tag":"Task verbs:","tagcolor":GREEN,"text":"LOX already carries 446 TaskActionCode verbs - ENGAGE, ATTACK, BREACH, CONSTR, CLROBS, MINLAY, TRANS, RESUPL, RESCUE, RECOVR, ESCRT, RECCE, PATROL, COMREL + search verbs. Not a missing-verb problem."},
 {"tag":"Order machinery:","tagcolor":GREEN,"text":"effects (DesiredEffectCode), targets (hasAffectedEntity), ROE (RuleOfEngagement, WeaponRuleOfEngagementCode), resources + quantities, routes + phased planning (PlanBody/PlanPhase), position reporting."},
 {"tag":"Structure:","tagcolor":GREEN,"text":"membership + command exist (C2SIM hasSubordinate, SMX hasCommandRelation) - the swarm residual is small; platform types (Vehicle / Aircraft / SurfaceVessel); a neutral hostility value (smx#NEUTRL)."},
 {"tag":"Capability declaration:","tagcolor":GREEN,"text":"BML WhoHoldingType already covers the capability self-report pattern (Q-V)."},
 {"tag":"What this means:","tagcolor":NAVY,"text":"a large share of the 24 decisions is where to hang existing vocabulary, not what to invent."},
], top=3.45, size=13, gap=8)
srcline(s, "verified against the RDF, not recalled (log change log 2026-07-12)  -  the 'checked - already exist' rows across log sec 6  -  OntologyConceptCoverage.md")
footer(s)
notes(s,
 "Section budget: slides 12-15, about 6 minutes - one beat per theme: re-adopt, missing content types, missing typing, missing authority. Each slide's Dig deeper line names the walk docs and log sections with the full detail.",
 "Open the findings block with the good news, aggregated: the measurement report flagged as missing already exists in C2SIM's own BML lineage (WhoMeasuredType); LOX already carries 446 task verbs; effects, targets, ROE, resources, routes, phased planning, and position reporting all exist; membership and command relations exist; a neutral hostility value exists (smx#NEUTRL; an untyped NeutralSide individual too); and the capability-declaration pattern exists (WhoHoldingType). All verified in the RDF, not recalled.",
 "The framing to land: the gap list is shorter than it looks - a large share of the 24 decisions is re-adopt / where-to-hang, not invent.")

# ---------------- Findings 2: missing content types ----------------
s = slide(); header(s, "Missing content types - what a message cannot yet say", "Each gap named by every scenario that hit it")
rbox(s, 0.8, 1.85, 11.75, 1.4, "The biggest content gap: one generic Detection Report\n\nconfidence + error-bound + false-positive - needed by the video, CBRN, EW, GPR, and naval-mine walks (Y1/M3/M4/G4); one report subsumes all five (Q-I/Q-Q).", RED, size=13)
bullets(s, [
 {"tag":"Rationale / explanation report:","tagcolor":RED,"text":"systems report WHAT (TaskStatus) but not WHY a route changed or a mission failed - CASEVAC (X2) + the DroneResponse explainability mission; schema in hand {event, action, reasoning, change, confidence} (Q-H)."},
 {"tag":"Robot-to-robot coordination:","tagcolor":RED,"text":"no content type for one robot to hand a verified safe route to another (envelope addressing exists; the content does not) - CASEVAC (X1) + maritime cross-cue with a shared track (G3) + MUM-T; extends to system-to-system tasking (Q-G/Q-P)."},
 {"tag":"Effect-achieved / BDA report:","tagcolor":RED,"text":"TaskStatus says the task ran, not that the target was destroyed - fire support (W3) + LIRC strike BDA."},
 {"tag":"Capability self-report:","tagcolor":RED,"text":"a robot declares its mounted equipment so tasks can be assigned by capability - MUM-T (G13 -> Q-V)."},
 {"tag":"Inline entity definition:","tagcolor":RED,"text":"a report cannot introduce a newly-observed (uncooperative) entity it references (M1 -> Q-E)."},
 {"tag":"Media identity / modality split:","tagcolor":RED,"text":"MediaReference identity is undecided, and MediaTypeCode mixes media format with sensor modality - a 'thermal scan' rode the NOS value (M2/M5 -> Q-F)."},
], top=3.45, size=12.5, gap=6)
srcline(s, "CASEVAC-Walk.md, NonVideoSensors-Walk.md, FireSupport-Walk.md, SourcedScenarios-Walk.md, ValidationEvidence-Walk.md  -  log secs 6b/6c/6e/6h/6j  -  decisions Q-E/G/H/I/P/Q/V")
footer(s)
notes(s,
 "The content-type gaps, each named by every scenario that hit it rather than by the scenario that happened to surface it first. The generic detection report carries the most evidence - five sensor modalities converge on it. The rationale report and robot-to-robot coordination each carry two independent sources (CASEVAC plus a documented mission).",
 "Also from MUM-T: collective-task decomposition and report aggregation (Z1 -> Q-J). The CASEVAC end-to-end story itself is on slides 5-6 and in CASEVAC-Walk.md - here it appears as two evidence citations (X1, X2).")

# ---------------- Findings 3: missing typing ----------------
s = slide(); header(s, "Missing typing - what a platform is and carries", "One pattern, several instances")
rbox(s, 0.8, 1.85, 11.75, 1.4, "The core gap: nothing typed for what a platform carries or wields\n\nCargo (L1), manipulator (E2), weapon/munition (W2) are one missing piece - the typed payload / effector / weapon (Q-L). The verbs already exist in LOX.", RED, size=13)
bullets(s, [
 {"tag":"Platform-munition hybrids:","tagcolor":ORANGE,"text":"a loitering munition / FPV is platform + munition at once; counter-UAS needs the detect->defeat chain over existing air-defense verbs + an EW-vulnerability annotation (Q-X)."},
 {"tag":"Locomotion / role subtypes:","tagcolor":ORANGE,"text":"wheeled / tracked / legged UGV; detector / neutralizer USV (Q-R, extends Q-A)."},
 {"tag":"Area as a subject:","tagcolor":ORANGE,"text":"an area cannot yet be the subject of a task or report (N1 -> Q-M) - surfaced by the redundancy screen, needed by the hazard-area, kill-box, and area-coverage walks; plus an explore-until-covered goal (G2 -> Q-N, search verbs exist)."},
 {"tag":"Environment + geometry:","tagcolor":ORANGE,"text":"operating-environment conditions (GPS-denied, illumination, sea-state, terrain - G11 -> Q-T); formation / relative geometry beyond a single RelativeLocation (G12 -> Q-U)."},
 {"tag":"Small residual:","tagcolor":MGRAY,"text":"a general-purpose tow/salvage verb (TOWTGT covers gunnery targets only)."},
], top=3.45, size=13, gap=8)
srcline(s, "TaskEffect-Batch-Walk.md, RedundancyPass-Walk.md, SourcedScenarios-Walk.md  -  log secs 6f/6g/6h/6k  -  decisions Q-L/M/N/R/T/U/X")
footer(s)
notes(s,
 "The typing gaps share one pattern: the model can name the action (the verbs exist) but not the thing - what is carried or wielded (Q-L), what a hybrid platform-munition is (Q-X), what subtype of platform (Q-R), or an area as the object of tasking (Q-M). Environment and formation attributes (Q-T/Q-U) round it out.",
 "This slide is the counterpart of the re-adopt slide: the verbs and order machinery exist; the typed nouns do not. The validation pass also supplied a concrete schema here: an area map with per-cell value + variance (Q-M/Q-Q).")

# ---------------- Findings 4: missing authority semantics ----------------
s = slide(); header(s, "Missing authority semantics - who may do what", "The safety-critical block - and doctrine already supplies the answer")
rbox(s, 0.8, 1.85, 11.75, 1.4, "W1  -  No link between autonomy level and permission to engage\n\nThe standard can say WHAT effect and WHICH ROE - but not WHO authorized the engagement, nor whether a FullAuto system may take lethal action unsupervised (AuthorizationHeader is sender authentication, not command authorization of fires).", RED, size=13)
bullets(s, [
 {"tag":"The doctrine-grounded answer (Q-W):","tagcolor":GREEN,"text":"weapons-control status (hold / tight / free) + kill-box - an authorization-bearing area (geo + time window + civilian-clearance + permitted target types) gating autonomous lethal action; from the SME LIRC scenario (G14). Unifies Q-K with area-as-subject (Q-M)."},
 {"tag":"On-the-loop control:","tagcolor":ORANGE,"text":"supervision verbs - configure / suspend / acknowledge / override - as engagement authority becomes a function of autonomy level (Q-K)."},
 {"tag":"Denied-comms operation:","tagcolor":ORANGE,"text":"an operating mode + deployable relay entity for comms-denied autonomy - SubT + sustainment (G1 -> Q-O; the relay verb lox#COMREL exists)."},
 {"tag":"Deception:","tagcolor":ORANGE,"text":"decoy role + threat-aware order annotations - sustainment + OPFOR targeting (G8 -> Q-S; deception verbs exist)."},
], top=3.45, size=13, gap=8)
srcline(s, "FireSupport-Walk.md + DroneWarfare-LIRC-OPFOR-Walk.md  -  log secs 6e (W1-W3) / 6k (G14)  -  decisions Q-K/O/S/W  -  Fire Support Order + LIRC Kill-Box Engagement Order tabs")
footer(s)
notes(s,
 "The authority block: W1 is the safety-critical gap - the standard cannot express who authorized an engagement, or whether a FullAuto system may act unsupervised. AuthorizationHeader was checked: it is message-sender authentication, not command authorization of fires - so who-approved-the-engagement is part of the gap, not covered.",
 "The answer came from doctrine, not invention: the SME drone-warfare thread's LIRC scenario supplies a weapons-control status (hold/tight/free) plus the kill box - an authorization-bearing area gated by geography, a time window, a civilian-clearance state, and permitted target types (G14 -> Q-W). It unifies engagement authority (Q-K) with area-as-subject (Q-M).",
 "Around it: on-the-loop supervision verbs (configure / suspend / acknowledge / override), the denied-comms operating mode + relay entity, and the decoy / threat-aware annotations.")

# ---------------- Decisions 1: model structure ----------------
s = slide(); header(s, "Decisions (1/3): model structure", "Full register - all 24, with what each resolves: log section 7")
bullets(s, [
 {"tag":"Q-A","tagcolor":ACCENT,"text":"UAV/robot typing: a role on the existing Platform tree, or a parallel Robot tree?"},
 {"tag":"Q-B","tagcolor":ACCENT,"text":"Swarm: derive from CollectiveEntity (ActorEntity) so it can be tasked."},
 {"tag":"Q-C","tagcolor":ACCENT,"text":"Sensor: entity, class, or attribute - choose one model and apply it everywhere."},
 {"tag":"Q-D","tagcolor":ACCENT,"text":"Autonomy: choose one normative vocabulary."},
], top=1.9, size=18, gap=18)
footer(s)
notes(s,
 "Section budget: slides 16-19, about 4 minutes; the decision slides are presented as a grouping, not read row by row.",
 "The ask, part 1 - structure: Q-A UAV/robot typing, Q-B a taskable swarm, Q-C one sensor model, Q-D one autonomy vocabulary. These four settle the shape of the model and unblock Initialization.",
 "The full text of all 24 decisions, each with what it resolves, is log sec 7 - present the grouping and point at the log rather than reading the register out.")

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
 {"tag":"Q-W","tagcolor":ACCENT,"text":"Weapons-control-status + kill-box authorization area gating autonomous lethal action - unifies Q-K + Q-M (the drone-warfare headline, G14)."},
 {"tag":"Q-X","tagcolor":ACCENT,"text":"Loitering-munition/FPV platform-munition typing + counter-UAS (detect->defeat over existing air-defense verbs) + EW-vulnerability annotation."},
], top=1.5, size=12, gap=6)
footer(s)
notes(s,
 "Part 3 - decisions raised by the sourced scenarios: exploration goals, denied-comms relay, cross-cueing, the generic detection report, locomotion subtypes, decoy/deception, environment conditions, formation geometry, capability self-report, plus the SME drone-warfare thread - Q-W (weapons-control/kill-box engagement authority, the headline answer to W1) and Q-X (loitering-munition/counter-UAS typing).",
 "Several of these re-adopt existing vocabulary (search verbs, lox#COMREL, BML WhoHoldingType) rather than invent - the decision is where to hang the structure, not whether the words exist.")

# ---------------- Proposed fixes (pending buy-in) ----------------
s = slide(); header(s, "Proposed refinements", "Pending group buy-in - nothing applied to the model")
bullets(s, [
 {"tag":"Safe corrections (unambiguous):","tagcolor":GREEN,"text":"class typo CollecticeRoboticSystem -> CollectiveRoboticSystem (O1); versionInfo Extrension -> Extension (O2); file CSIM_ASX -> C2SIM_ASX (O3); hasStartTime UUIDBase -> TimeInstant (M7); unify namespace label ASX / C2SIM_ASX (M8)."},
 {"tag":"Structural (decide first):","tagcolor":ORANGE,"text":"UAV/robot typing (Q-A); Swarm -> CollectiveEntity so it is taskable (Q-B); one sensor model (Q-C); one autonomy vocabulary (Q-D)."},
 {"tag":"New content (design):","tagcolor":ACCENT,"text":"inline entity def (Q-E), MediaReference (Q-F), robot-to-robot + cross-cue (Q-G/Q-P), rationale report (Q-H), generic detection report (Q-I/Q-Q), swarm residuals (Q-J), engagement authority (Q-K), payload/effector/weapon typing (Q-L), area subject (Q-M), explore order (Q-N), denied-comms/relay (Q-O), locomotion subtypes (Q-R), decoy/threat-aware (Q-S), environment conditions (Q-T), formation geometry (Q-U), weapons-control/kill-box authority (Q-W), loitering-munition + counter-UAS typing (Q-X)."},
 {"text":"Nothing here is applied to the model - all items are proposals for group buy-in.","bold":True},
], top=1.7, size=14, gap=13)
srcline(s, "log secs 3-4 (the safe corrections)  -  sec 7 (every decision, with what it resolves)")
footer(s)
notes(s,
 "Section budget: slides 19-20, about 1 minute - the close.",
 "The same decisions, grouped by commitment level: safe corrections (typos, the UUIDBase slip) are unambiguous; structural decisions need the group; content types need design. Nothing has been applied to the model or the workbooks - all items are proposals pending buy-in.",
 "The M-series instantiation items fold in here and into the decisions: the typos and the UUIDBase slip (M7) are safe corrections; M1 and M2/M5 resolve via Q-E and Q-F. All cheapest to fix before messages are built on them.")

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
 "Where the ball is: sourcing is essentially complete - every gap this review raised is grounded in a real mission (one nice-to-have left: a dedicated autonomous-CASEVAC mission). The remaining work - the attribute layer, the reconciliation, the 24 decisions - is modeling work; more scenarios will not fill it.")

# ---------------- How to use this material (reading guide) ----------------
s = slide(); header(s, "How to use this material", "Reading paths by time budget - each level builds on the previous")
table(s, [
 ["Budget", "Read this", "You come away with"],
 ["5 minutes",
  "Group-Briefing.md - one page",
  "what this is, what was found, the ~24 decisions, where the ball is"],
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
s = slide(); header(s, "Finding-ID decoder ring - Issues-And-Comments-Log.md", "Every ID resolves to one row or section - nothing is free-floating")
table(s, [
 ["ID family", "What it names", "Where it resolves"],
 ["P1 - P7", "entity-typing findings: UAV (P1), sensor (P2), swarm (P7)", "log sec 5; Initialization-Walk.md"],
 ["D / O / M", "track alignment / OWL typos / sample-message items", "log secs 2 / 3 / 4"],
 ["S", "process + repo-sync decisions (e.g. diff-able workbooks, S4)", "log sec 1"],
 ["C1 - C9", "coverage state, scenario x message type", "log sec 6"],
 ["X", "CASEVAC walk findings", "log sec 6b; CASEVAC-Walk.md"],
 ["Y / Z", "sensor / swarm walk findings", "log secs 6c / 6d; NonVideoSensors- / Swarm-Walk.md"],
 ["W / L / E / R", "fire support / logistics / engineering / rescue findings", "log secs 6e / 6f; FireSupport- / TaskEffect-Batch-Walk.md"],
 ["N", "redundancy-pass findings", "log sec 6g; RedundancyPass-Walk.md"],
 ["G", "sourced-scenario + validation + drone-warfare findings", "log secs 6h-6k; SourcedScenarios- / ValidationEvidence- / DroneWarfare-LIRC-OPFOR-Walk.md"],
 ["Q-A .. Q-X", "the 24 decisions this review puts to the group", "log sec 7 - full text + what each resolves"],
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
 {"tag":"Master evidence log:","tagcolor":NAVY,"text":"Issues-And-Comments-Log.md - every finding, the 24 decisions (sec 7), v0.0.3 reconciliation (sec 9), why gaps remain (sec 8)."},
 {"tag":"Briefing / Q&A / talk track:","tagcolor":NAVY,"text":"Group-Briefing.md (one page); Anticipated-QA.md; Presenter-Notes.md."},
 {"tag":"Coverage + the actual messages:","tagcolor":NAVY,"text":"Message-Instantiation-Coverage.md; the three 'ASX Sample *.xml' workbooks (the ~38 instantiations, diff-able)."},
 {"tag":"Initialization & entity typing (P1/P2/P7):","tagcolor":NAVY,"text":"Initialization-Walk.md; log sec 5."},
 {"tag":"CASEVAC (X1/X2 -> Q-G/Q-H):","tagcolor":NAVY,"text":"CASEVAC-Walk.md; log sec 6b."},
 {"tag":"Sensors & swarm (Y / Z series):","tagcolor":NAVY,"text":"NonVideoSensors-Walk.md; Swarm-Walk.md; log sec 6c / 6d."},
 {"tag":"Task / effect & engagement (W / L, Q-K/Q-L):","tagcolor":NAVY,"text":"FireSupport-Walk.md; TaskEffect-Batch-Walk.md; log sec 6e / 6f."},
 {"tag":"Sourced, validation & drone-warfare missions:","tagcolor":NAVY,"text":"SourcedScenarios-Walk.md; ValidationEvidence-Walk.md; DroneWarfare-LIRC-OPFOR-Walk.md; Documents-Found.md; log sec 6h / 6j / 6k."},
 {"tag":"Redundancy screen (N1):","tagcolor":NAVY,"text":"RedundancyPass-Walk.md; log sec 6g."},
], top=1.65, size=12, gap=5)
footer(s)
notes(s,
 "The topic-to-doc map. Everything is on branch asx-diffable-spreadsheets: review docs in Subgroups/ASX/InstantiationReview, workbooks in Subgroups/ASX/Proposed Extension Working Materials. The .md files render directly on GitHub - switch branch and browse; no tooling needed.")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ASX-Instantiation-Findings.pptx")
prs.save(out)
print("saved:", out, "slides:", len(prs.slides._sldIdLst))
