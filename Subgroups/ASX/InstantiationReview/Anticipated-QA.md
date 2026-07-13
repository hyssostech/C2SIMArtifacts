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
layer and the ~22 decisions. (The re-check also surfaced one base-standard nit
we offer upstream: `AuthorizationHeader`'s two cardinality restrictions use
`owl:onDataRange C2SIM#angle` - almost certainly unintended.)

**Q. Isn't the OWL just an early draft? Aren't you criticizing incomplete work?**
Yes, and we treat it exactly as that. It is an early v0.0.x work-in-progress, and
the findings are things *still to be defined*, not defects. The finding is not
"it's wrong" - it's "the v0.0.1 baseline is a taxonomy of things (15 classes, 0
datatype properties) whose message/attribute layer hadn't been built yet, and
here is exactly what that layer needs." Michael's v0.0.3 already starts that layer
(it adds datatype properties for the Video Detection Report), which is the model
moving in the direction this review points to. It's a to-do list derived by
instantiation, not a critique.

**Q. You say a swarm isn't yet taskable - can't we just add a property?**
It's a class-tree issue, not a missing property. `Swarm` currently derives from
`PhysicalEntity` (an inert object), and orders/reports are addressed to an
`ActorEntity`. The clean fix is to derive `Swarm` from `CollectiveEntity`, which
is already an `ActorEntity` in the base standard (C2SIM). That is decision Q-B.
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
Settle the entity-typing decisions Q-A (UAV/robot) and Q-B (swarm). They unblock
Initialization, which is the message type with zero worked examples and the one
that forces the model's hardest choices.

**Q. Why do the OWL and the spreadsheets disagree?**
They are two tracks at different stages: the OWL was last updated in January, the
spreadsheets in June. So autonomy and sensors are each defined three different
ways. Reconciling the two is part of decision Q-C / Q-D.

**Q. Is the sourcing/scenario work done?**
Essentially, yes - every gap the review raised now has at least one real sourced
mission behind it. The one worthwhile remaining hunt is a dedicated
autonomous-CASEVAC coordination mission. The rest of the remaining work is
modeling, not sourcing.

**Q. What would you need from us to move forward?**
The ~22 decisions, structure first. Once Q-A..Q-D are settled, the content-type
decisions and the attribute layer follow. We can turn any decision into concrete
message instances quickly, since the walks already show the shape.

**Q. How confident are you in the specific findings?**
The structural findings (P1, P7, the typos, "0 datatype properties" in the v0.0.1
baseline, what exists vs. doesn't) were verified directly against the RDF files
(and re-checked against v0.0.3), and the workbook
conversions were verified by round-trip. The design *recommendations* (e.g. which
way to resolve P1) are proposals for the group, not conclusions.
