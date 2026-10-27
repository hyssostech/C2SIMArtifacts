# Anticipated Q&A - ASX Instantiation Review

Likely questions from the sub-group, with grounded answers. Ordered roughly by
how likely / how pointed. Answers are defensible against the artifacts; where a
claim was verified against the RDF, that is noted.

**Q. Did you actually check the base standard, or just assume these are gaps?**
Checked. Before asserting any gap we grep'd the C2SIM / SMX / LOX RDF. That is why
several things came back as "already exists" (rules of engagement,
`DesiredEffectCode`, `Route`, `Resource`, `SurfaceVessel` /
`SubsurfaceVessel`, `CollectiveEntity`, `RelativeLocation`, `HostilityStatusCode`
(neutral value `smx#NEUTRL`; `smx#ANT` = assumed-neutral), an untyped `NeutralSide` individual, and the LOX
task verbs BREACH / ENGAGE / ATTACK / RESCUE / RECOVR) and two would-be gaps were
withdrawn (Route and phased
planning already exist). The genuinely-missing items are the message/attribute
layer and the ~24 decisions. (The re-check also surfaced one base-standard nit
we offer upstream: `AuthorizationHeader`'s two cardinality restrictions use
`owl:onDataRange C2SIM#angle` - almost certainly unintended.)

**Q. Isn't the OWL just an early draft? Aren't you criticizing incomplete work?**
Yes, and we treat it exactly as that. It is an early v0.0.x work-in-progress, and
the findings are things *still to be defined*, not defects. The finding is not
"it's wrong" - it's "the v0.0.1 baseline is a taxonomy of things (15 classes, 0
datatype properties) whose message/attribute layer hadn't been built yet, and
here is exactly what that layer needs." Michael's v0.0.3 already started that
layer (datatype properties for the Video Detection Report) and v0.0.4 extends it
(five platform attributes from the Concept Mapping, a per-task autonomy level),
which is the model moving in the direction this review points to. It's a to-do
list derived by instantiation, not a critique.

**Q. The group already decided P1 / P7 / P2 - why are they still in the deck?**
Because the decisions are not yet in the OWL. The three structural slides now
show the decided state and what remains to apply: P7 (collective from
`CollectiveEntity`) is not in v0.0.4 at all; P1 (autonomy as a facet on the
Platform subtree) is half there - `hasControlMode` sits on `smx#Vehicle`, but the
`Robot` / `UAV` / `UGV` tree is still declared and the derived XSD still offers
`Robot` beside `Platform`; P2 (sensors reworked on existing standards) has
placeholders only. The slides are the implementation checklist now, not the
ask.

**Q. You say a swarm isn't yet taskable - can't we just add a property?**
It's a class-tree issue, not a missing property. `Swarm` currently derives from
`PhysicalEntity` (an inert object), and orders/reports are addressed to an
`ActorEntity`. The clean fix is to derive `Swarm` from `CollectiveEntity`, which
is already an `ActorEntity` in the base standard (C2SIM). That is decision Q-B -
**now decided by the group**; the residual is applying it (re-parent the collective class; its re-spelling
to `CollectiveRoboticSystem` is in PR #9).
Membership and command already exist (`hasSubordinate` / `hasCommandRelation`).

**Q. Strictly speaking, `hasReportingEntity` is a UUID datatype property - a
reasoner wouldn't reject a swarm-signed report. Is P7 really a defect?**
Correct, and we phrase it as a semantic mismatch, not a logical inconsistency:
the properties carry UUID references, and their annotations state the referenced
individual must be "of the ActorEntity class". So nothing fails mechanically -
but instance data would violate the standard's stated semantics, and any
consumer that resolves the reference against the entity's type breaks. Fixing
the class tree (Q-B) is still the right move.

**Q. How many of these gaps are real vs. things we already have?**
Three categories. (1) Already present - re-use it (ROE, routes, vessels, etc.).
(2) Prior art we should re-adopt - the measurement report is BML `WhoMeasuredType`
from C2SIM's own lineage. (3) Genuinely unbuilt - the datatype/attribute layer and
the cross-cutting content types (rationale report, area-as-subject, engagement
authority). The deck's "good news" slide makes this split explicit.

**Q. Are these scenarios real, or made up by an LLM?**
A mix, and we label it. CASEVAC is human-authored (a contributed scenario). The
MUTT use cases are LLM-generated (flagged). The recent additions (subterranean,
maritime MCM, sustainment, explainability, CBRN, EW, persistence, counter-UAS,
MUM-T, SAR, formation, breach) are extracted from real open-access papers/reports;
two carry fidelity caveats (EW and the robotic breach) that are noted in the
records.

**Q. Did you change our model or Elizabeth's workbooks?**
No. We converted copies of the three sample-message workbooks to a diff-able
`.xml` format and added instantiation tabs there; the original `.xlsx` are
untouched, and nothing was applied to the OWL. Every finding is a proposal.

**Q. Why convert to .xml? What did we lose?**
Only to make the message instantiations diffable/mergeable in git (`.xlsx` is a
zip that git treats as opaque). The conversion was verified cell-for-cell against
the originals (no data lost). Elizabeth can keep authoring in Excel - the format
is Excel's own "XML Spreadsheet 2003".

**Q. What is the single first thing to do?**
Apply the decided entity-typing decisions in the OWL - Q-B first (re-parent the
collective under `CollectiveEntity`; one axiom plus the spelling fix), then Q-A
(retire the `Robot` tree and give the new v0.0.4 properties a home on the
Platform subtree). They unblock Initialization, which is the message type that
forces the model's hardest choices; the Init tabs get re-cut once they land.

**Q. Why do the OWL and the spreadsheets disagree?**
They were two tracks at different stages: the OWL was last updated in January,
the spreadsheets in June. So autonomy and sensors were each defined three
different ways. v0.0.4 (August) started reconciling from the OWL side - five
spreadsheet attributes are now properties, Control Mode takes the OWL's
`AutonomyLevelCode` values, and the Concept Mapping tracks per attribute what is
done. What is left is stating the one autonomy vocabulary (Q-D) and the sensor
rework (Q-C, direction decided).

**Q. Is the sourcing/scenario work done?**
Essentially, yes - every gap the review raised now has at least one real sourced
mission behind it. The one worthwhile remaining hunt is a dedicated
autonomous-CASEVAC coordination mission. The rest of the remaining work is
modeling, not sourcing.

**Q. What would you need from us to move forward?**
The structural ones are settled (Q-A..Q-C decided, Q-D settled in practice);
next is applying them in the OWL, then the ~20 content-type decisions and the
rest of the attribute layer. We can turn any decision into concrete
message instances quickly, since the walks already show the shape.

**Q. How confident are you in the specific findings?**
The structural findings (P1, P7, the typos, "0 datatype properties" in the v0.0.1
baseline, what exists vs. doesn't) were verified directly against the RDF files
(and re-checked against v0.0.3 and v0.0.4), and the workbook
conversions were verified by round-trip. The design *recommendations* (e.g. which
way to resolve P1) are proposals for the group, not conclusions.
