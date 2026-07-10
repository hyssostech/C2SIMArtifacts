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

def bullets(s, items, top=1.6, left=0.7, width=12.0, height=5.2, size=16, gap=6):
    height = min(height, 6.95 - top)   # never hang past the footer / slide edge
    tb, tf = box(s, left, top, width, height)
    first = True
    for it in items:
        lvl = it.get("lvl", 0)
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.level = lvl; p.space_after = Pt(gap); p.space_before = Pt(2)
        marker = "-  " if lvl > 0 else ""
        indent = "      " * lvl
        if it.get("tag"):
            set_run(p.add_run(), indent + it["tag"] + "  ", size, it.get("tagcolor", RED), bold=True)
            set_run(p.add_run(), it["text"], size, GRAY)
        else:
            set_run(p.add_run(), indent + marker + it["text"], size,
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
accent = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(2.35), Inches(2.4), Pt(5))
accent.fill.solid(); accent.fill.fore_color.rgb = ACCENT; accent.line.fill.background()

# ---------------- Approach ----------------
s = slide(); header(s, "The method", "Building on the sample-message work")
bullets(s, [
 {"text":"Walk each scenario and instantiate real Initialization / Order / Report messages using C2SIM + the proposed ASX elements."},
 {"text":"Where a proposed element cannot be instantiated cleanly, a concrete problem surfaces - that is the signal we want."},
 {"text":"This review focused on Initialization (which had zero worked examples) and the CASEVAC scenario, and cross-checked the OWL model against the spreadsheets."},
 {"text":"Findings are framed as decisions for the group, not as objections to the approach - the approach is working."},
], top=1.7, size=18, gap=14)
footer(s)

# ---------------- State of play ----------------
s = slide(); header(s, "Where the instantiation stands")
bullets(s, [
 {"text":"4 worked instantiations so far: 2 Reports, 2 Orders, 0 Initialization.","bold":True},
 {"text":"Reports are the mature track (Video Detection Report); Orders are partial; every Initialization sheet is still a stub.","lvl":1},
 {"text":"Coverage is concentrated on a single UAV video-surveillance thread plus one UGV transport order.","lvl":1},
 {"text":"CASEVAC - the one human-authored contributed scenario - had no messages of any type (now walked in this review).","bold":True},
 {"text":"Initialization is the biggest hole and the highest-signal place to test the model (drafted in this review).","lvl":1},
], top=1.7, size=17, gap=12)
footer(s)

# ---------------- Two tracks out of sync ----------------
s = slide(); header(s, "Two tracks have drifted apart")
rbox(s, 0.8, 1.9, 5.5, 1.5, "OWL model  (CSIM_ASX.rdf)\nlast updated  Jan 2026", NAVY, size=15)
rbox(s, 7.0, 1.9, 5.5, 1.5, "Spreadsheets  (Concept Mapping,\nsample messages)  updated  Jun 2026", ACCENT, size=15)
arrow(s, 6.3, 2.65, 7.0, 2.65, RED)
bullets(s, [
 {"tag":"Consequence:","tagcolor":RED,"text":"the model does not reflect ~5 months of attribute decisions made in the spreadsheets."},
 {"text":"Autonomy is defined three different ways across the two tracks.","lvl":1},
 {"text":"Sensors are defined three different ways.","lvl":1},
 {"text":"The whole attribute layer (Payload, Mobility, VehicleType, ...) exists only in the spreadsheets, not the OWL.","lvl":1},
], top=3.8, size=16, gap=10)
footer(s)

# ---------------- 3 blockers ----------------
s = slide(); header(s, "Instantiating one entity hits three blockers")
rbox(s, 0.8, 2.0, 3.8, 2.2, "P1\nA UAV is typed two\nincompatible ways", RED, size=16)
rbox(s, 4.85, 2.0, 3.8, 2.2, "P2\nA sensor has no\nagreed representation", RED, size=16)
rbox(s, 8.9, 2.0, 3.65, 2.2, "P7\nA swarm cannot be\ntasked as modeled", RED, size=16)
bullets(s, [
 {"text":"All three are entity-typing decisions - so Initialization, not Reports, is where the proposed model must be exercised and settled.","bold":True},
], top=4.7, size=17)
footer(s)

# ---------------- P1 diagram ----------------
s = slide(); header(s, "P1  -  A UAV is typed twice", "BLOCKER")
rbox(s, 5.2, 1.7, 3.0, 0.75, "ActorEntity", NAVY, size=14)
rbox(s, 2.4, 3.0, 3.0, 0.75, "Platform  (SMX)", ACCENT, size=13)
rbox(s, 2.4, 4.2, 3.0, 0.75, "Aircraft  (SMX)", ACCENT, size=13)
rbox(s, 8.0, 3.0, 3.0, 0.75, "Robot  (ASX)", ORANGE, size=13)
rbox(s, 8.0, 4.2, 3.0, 0.75, "UAV  (ASX)", ORANGE, size=13)
arrow(s, 6.2, 2.45, 3.9, 3.0); arrow(s, 3.9, 3.75, 3.9, 4.2)
arrow(s, 7.2, 2.45, 9.5, 3.0); arrow(s, 9.5, 3.75, 9.5, 4.2)
bullets(s, [
 {"text":"Two disjoint sibling trees under ActorEntity model the same real drone."},
 {"text":"Type it as Robot -> it loses all existing SMX Platform / LOX machinery.","lvl":1},
 {"text":"Type it as Aircraft -> the ASX Robot / UAV classes go unused.","lvl":1},
 {"tag":"Decision (Q-A):","tagcolor":ACCENT,"text":"make ASX autonomy a role/facet on the existing Platform subtree instead of a parallel Robot tree?"},
], top=5.05, size=14, gap=6)
footer(s)

# ---------------- P7 diagram ----------------
s = slide(); header(s, "P7  -  A swarm cannot receive orders", "BLOCKER")
rbox(s, 0.9, 2.0, 3.1, 0.7, "Swarm  (ASX)", ORANGE, size=13)
rbox(s, 4.3, 2.0, 3.6, 0.7, "CollectiveRoboticSystem", ORANGE, size=12)
rbox(s, 8.2, 2.0, 3.4, 0.7, "... PhysicalEntity", RED, size=13)
arrow(s, 4.0, 2.35, 4.3, 2.35, RED); arrow(s, 7.9, 2.35, 8.2, 2.35, RED)
tb, tf = box(s, 8.2, 2.75, 3.6, 0.4); p=tf.paragraphs[0]
set_run(p.add_run(), "inert object - cannot be tasked", 12, RED, italic=True)
rbox(s, 0.9, 4.0, 3.1, 0.7, "Swarm  (proposed)", GREEN, size=13)
rbox(s, 4.3, 4.0, 3.6, 0.7, "CollectiveEntity  (C2SIM)", GREEN, size=12)
rbox(s, 8.2, 4.0, 3.4, 0.7, "ActorEntity", GREEN, size=13)
arrow(s, 4.0, 4.35, 4.3, 4.35, GREEN); arrow(s, 7.9, 4.35, 8.2, 4.35, GREEN)
tb, tf = box(s, 8.2, 4.75, 3.6, 0.4); p=tf.paragraphs[0]
set_run(p.add_run(), "taskable - receives orders, reports", 12, GREEN, italic=True)
bullets(s, [
 {"text":"A swarm is exactly what orders are addressed to and what sends reports - it must be an ActorEntity."},
 {"text":"Once fixed, membership and command already exist in base C2SIM (hasSubordinate, hasCommandRelation); the residual swarm needs are small.","lvl":1},
 {"tag":"Decision (Q-B):","tagcolor":ACCENT,"text":"derive Swarm from CollectiveEntity (already an ActorEntity) rather than from the device/artifact tree."},
], top=5.3, size=13.5, gap=6)
footer(s)

# ---------------- Model drift detail ----------------
s = slide(); header(s, "The model lags the spreadsheets")
bullets(s, [
 {"tag":"Autonomy - 3 vocabularies:","tagcolor":ORANGE,"text":"OWL {Automated, FullAuto, ReCont, Teleop}  vs  ControlMode {Piloted, Unpiloted-Autonomous, Swarm}  vs  NavigationAutonomy {FPV, Autonomous, RemoteControl}."},
 {"tag":"Sensor - 3 models:","tagcolor":ORANGE,"text":"OWL Sensor class  vs  SensorType enum  vs  SensorCapability as associated equipment."},
 {"tag":"Missing from OWL:","tagcolor":ORANGE,"text":"Payload, PayloadCapability, Mobility/Propulsion, VehicleType, PassengerCapability, SwarmParameters. The OWL has 0 datatype properties."},
 {"tag":"Decisions (Q-C, Q-D):","tagcolor":ACCENT,"text":"pick one normative sensor model and one normative autonomy vocabulary; express the rest as derived."},
], top=1.8, size=15.5, gap=14)
footer(s)

# ---------------- Sample-message defects ----------------
s = slide(); header(s, "Defects in the existing instantiations")
bullets(s, [
 {"tag":"M1 (HIGH):","tagcolor":ORANGE,"text":"actorReference is a string, but it must define an entity not yet in the database - no inline entity-definition mechanism exists for observed (uncooperative) entities."},
 {"tag":"M5 (MED):","tagcolor":ORANGE,"text":"MediaTypeEnum conflates media format (Video/Audio/Image/Document) with sensor modality (a note asks it to also cover 'thermal scan')."},
 {"tag":"M7 (HIGH):","tagcolor":ORANGE,"text":"hasStartTime is typed UUIDBase while hasEndTime is TimeInstant - almost certainly a copy/paste error."},
 {"tag":"Typos:","tagcolor":RED,"text":"class 'CollecticeRoboticSystem' (should be Collective) and versionInfo 'Extrension' - cheap to fix now, painful after messages exist."},
], top=1.8, size=15.5, gap=13)
footer(s)

# ---------------- Coverage gaps ----------------
s = slide(); header(s, "Biggest coverage gaps")
bullets(s, [
 {"text":"Initialization: 0 of 3 named scenarios were instantiated (now drafted in this review).","bold":True},
 {"text":"CASEVAC: walked end-to-end in this review - surfaces two gaps with no element (next slide).","bold":True},
 {"text":"Non-video sensors (CBRN, EW, GPR): walked - the media-based report model does not generalize; non-imaging sensors have no measurement type (Y1/Y5).","bold":True},
 {"text":"Task/effect scenarios: engagement, delivery, manipulation, rescue walked - the gap is consistent (task verbs + payload/effector typing)."},
 {"text":"Redundancy pass (route-clearance, companion, urban): confirmed - plus one new finding, N1 (an area cannot be the subject of a task/report)."},
], top=1.7, size=16.5, gap=12)
footer(s)

# ---------------- CASEVAC walk ----------------
s = slide(); header(s, "CASEVAC walk: two gaps with no element", "The flagship contributed scenario")
bullets(s, [
 {"text":"Walked end-to-end: Initialization -> tasking Order -> robot-to-robot route hand-off -> status/threat Reports -> explainable-reasons Report."},
], top=1.55, size=14, height=0.85)
rbox(s, 0.8, 2.45, 5.75, 1.75, "X1  -  No robot-to-robot content\n\nScout cannot hand a verified safe Route to the transport UGV (envelope addressing exists; a content type does not)", RED, size=13)
rbox(s, 6.8, 2.45, 5.75, 1.75, "X2  -  No rationale report\n\nSystems can report WHAT (TaskStatus) but not WHY a route changed or a mission failed", RED, size=13)
bullets(s, [
 {"tag":"Decision (Q-G):","tagcolor":ACCENT,"text":"define a robot-to-robot coordination content type (safe-route advertisement) and the issuing-authority model."},
 {"tag":"Decision (Q-H):","tagcolor":ACCENT,"text":"add a rationale/explanation ReportContent so systems can report why, not just what."},
 {"tag":"Checked:","tagcolor":GREEN,"text":"Route, phased planning (PlanBody/PlanPhase), and position reporting already exist - not gaps."},
], top=4.5, size=14, gap=9)
footer(s)

# ---------------- Fire Support / engagement authority ----------------
s = slide(); header(s, "Fire Support: autonomous engagement authority", "The task/effect axis")
rbox(s, 0.8, 1.95, 11.75, 1.6, "W1  -  No link between autonomy level and permission to engage\n\nThe standard can say WHAT effect, WHICH ROE, and WHO authorized the order - but not whether a FullAuto system may take a lethal action without a human in / on the loop.", RED, size=15)
bullets(s, [
 {"tag":"Checked - already exist (not gaps):","tagcolor":GREEN,"text":"rules of engagement (RuleOfEngagement, WeaponROECode - LOX), order authorization (AuthorizationHeader), desired effect (DesiredEffectCode), target (hasAffectedEntity)."},
 {"tag":"Also gaps:","tagcolor":ORANGE,"text":"W2 weapon/munition not typed; W3 no battle-damage / effect-achieved report (TaskStatus = the task ran, not the target destroyed)."},
 {"tag":"Decision (Q-K):","tagcolor":ACCENT,"text":"model engagement authority as a function of autonomy level - may this system take this action unsupervised?"},
], top=3.8, size=14.5, gap=11)
footer(s)

# ---------------- Task/effect summary ----------------
s = slide(); header(s, "The task/effect axis distills to two gaps", "Across engagement, delivery, manipulation, rescue")
rbox(s, 0.8, 2.0, 5.75, 1.75, "1.  Task verbs\n\nNo vocabulary for what systems DO: deliver, dig / clear / emplace, recover / rescue (engage uncertain).", NAVY, size=14)
rbox(s, 6.8, 2.0, 5.75, 1.75, "2.  Payload / effector / weapon typing\n\nCargo (L1), manipulator (E2), weapon (W2) are one gap: no typed thing carried or wielded.", NAVY, size=14)
bullets(s, [
 {"tag":"Already there (checked):","tagcolor":GREEN,"text":"effects (DesiredEffectCode), targets (hasAffectedEntity), resources + quantities, ROE, authorization, and platform types (Vehicle / Aircraft / SurfaceVessel)."},
 {"tag":"Also (N1):","tagcolor":ORANGE,"text":"an area cannot be the subject of a task or report - no hasAffectedArea, no area-state (cleared/contaminated). See Q-M."},
 {"tag":"Decision (Q-L):","tagcolor":ACCENT,"text":"define the task-verb vocabulary and the typed payload / effector / weapon - that is the whole axis."},
], top=4.0, size=14, gap=9)
footer(s)

# ---------------- Decisions 1: model structure ----------------
s = slide(); header(s, "Decisions (1/2): model structure")
bullets(s, [
 {"tag":"Q-A","tagcolor":ACCENT,"text":"UAV/robot typing: a role on the existing Platform tree, or a parallel Robot tree?"},
 {"tag":"Q-B","tagcolor":ACCENT,"text":"Swarm: derive from CollectiveEntity (ActorEntity) so it can be tasked."},
 {"tag":"Q-C","tagcolor":ACCENT,"text":"Sensor: entity, class, or attribute - choose one model and apply it everywhere."},
 {"tag":"Q-D","tagcolor":ACCENT,"text":"Autonomy: choose one normative vocabulary."},
], top=1.9, size=18, gap=18)
footer(s)

# ---------------- Decisions 2: new content ----------------
s = slide(); header(s, "Decisions (2/2): new content types needed")
bullets(s, [
 {"tag":"Q-E","tagcolor":ACCENT,"text":"Inline entity definition for newly-observed entities in reports."},
 {"tag":"Q-F","tagcolor":ACCENT,"text":"MediaReference identity; separate media-format from sensor-modality."},
 {"tag":"Q-G","tagcolor":ACCENT,"text":"Robot-to-robot coordination content type + issuing authority (CASEVAC)."},
 {"tag":"Q-H","tagcolor":ACCENT,"text":"Rationale/explanation ReportContent - report why, not just what (CASEVAC)."},
 {"tag":"Q-I","tagcolor":ACCENT,"text":"Media-independent sensor-reading (value+unit+modality) + full SensorType taxonomy."},
 {"tag":"Q-J","tagcolor":ACCENT,"text":"Swarm residuals: network params, leader role, aggregation, member lifecycle."},
 {"tag":"Q-K","tagcolor":ACCENT,"text":"Engagement authority as a function of autonomy level (Fire Support)."},
 {"tag":"Q-L","tagcolor":ACCENT,"text":"Task-verb vocabulary (deliver, manipulate, recover) + typed payload/effector/weapon."},
 {"tag":"Q-M","tagcolor":ACCENT,"text":"Let an area be the subject of a task/report (hasAffectedArea + area-state)."},
], top=1.6, size=13.5, gap=8)
footer(s)

# ---------------- Proposed fixes (pending buy-in) ----------------
s = slide(); header(s, "Proposed fixes", "Pending group buy-in - nothing applied to the model")
bullets(s, [
 {"tag":"Safe corrections (unambiguous):","tagcolor":GREEN,"text":"class typo CollecticeRoboticSystem -> Collective (O1); versionInfo Extrension -> Extension (O2); file CSIM_ASX -> C2SIM_ASX (O3); hasStartTime UUIDBase -> TimeInstant (M7); unify namespace label ASX / C2SIM_ASX (M8)."},
 {"tag":"Structural (decide first):","tagcolor":ORANGE,"text":"UAV/robot typing (Q-A); Swarm -> CollectiveEntity so it is taskable (Q-B); one sensor model (Q-C); one autonomy vocabulary (Q-D)."},
 {"tag":"New content (design):","tagcolor":ACCENT,"text":"inline entity def (Q-E), MediaReference (Q-F), robot-to-robot (Q-G), rationale report (Q-H), sensor-reading (Q-I), swarm residuals (Q-J), engagement authority (Q-K), task verbs + payload (Q-L), area subject (Q-M)."},
 {"text":"Nothing here is applied to the model - all items are proposals for group buy-in.","bold":True},
], top=1.7, size=14, gap=13)
footer(s)

# ---------------- Next steps ----------------
s = slide(); header(s, "Recommended next steps")
bullets(s, [
 {"text":"Settle the two entity-typing decisions (Q-A, Q-B) - this unblocks Initialization.","bold":True},
 {"text":"Complete the Initialization instantiations (drafts provided for the 3 named scenarios)."},
 {"text":"Add the two CASEVAC content types (Q-G robot-to-robot, Q-H rationale) - both are explicit scenario requirements."},
 {"text":"Reconcile the OWL model with the June spreadsheet decisions; fix the typos."},
 {"text":"Optional: adopt the diff-able (.xml) workbooks so edits can be reviewed and merged in git."},
], top=1.8, size=16.5, gap=12)
footer(s)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ASX-Instantiation-Findings.pptx")
prs.save(out)
print("saved:", out, "slides:", len(prs.slides._sldIdLst))
