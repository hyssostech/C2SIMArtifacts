# Proposed Slice: STANAG 4817 / CATL as a Source for ASX Coordination Content

**Status: PROPOSED.** A *scoping* document for a slice of work to be considered
for the future - not a walk that has been performed, and not a proposed model
change. Nothing here has been instantiated into the sample-message workbooks.
What *has* been done is the grounding: every "already exists" / "does not exist"
claim about C2SIM / SMX / LOX below was checked against the ontologies, and
every claim about STANAG 4817 and CATL is attributed to a named public source.

**Origin.** A question raised 2026-10-14: what can the STANAG 4817 work
contribute to ASX? This document answers it in the same shape as the two
earlier slices (`Sensor-Characterization-Slice.md`, `DIS-Enumerations-Slice.md`):
a design source to learn from, cross-referenced to the open findings, with the
limits stated.

**The caveat, stated first.** The ratifying text (AEP-4817) is **not public**.
The most recent reporting (Janes, Euro-SD, Seapower, 2024-2025) describes the
standard as in final development ahead of ratification, used operationally at
REPMUS 24 and Task Force X Baltic; an earlier Fraunhofer INTERACT report
describes it as unavailable and stalled. Everything below about 4817 itself is
therefore second-hand. The one *publicly documented* artifact in its lineage is
**CATL** (Collaborative Autonomy Tasking Layer), the CMRE message model that
its authors describe as "a basis for STANAG 4817". Where this slice makes a
concrete claim, it is a CATL claim, and the two CATL papers (Furfaro et al.
2021; Van Riet et al. 2023) are the sources to obtain in full.

*Companion slices:* the sensor slice (6l) and the DIS slice (6m) are independent
of this one. Where 4817 touches them it is cross-referenced (section 3.4); the
overlap is small.

---

## 1. Grounding done first

### 1.1 What C2SIM / SMX / LOX already have (checked in the RDF)

| Checked | Result |
|---|---|
| A *task request* content | **Exists.** `C2SIM#TaskRequestContent subClassOf RequestContent`, "a request for an Actor to perform a Task", carrying `hasTask`. |
| Accept / reject of a request | **Exists.** `AcknowledgementBody` + `AcknowledgeTypeCode` {ACKRCVD, ACKSUCC, ACKFAIL, ACKNOTEXEC, ACKNOTRECGNZ, ACKNOTUNDSTD, ACKREQGRT, ACKREQDEN}, with `isInReplyToMessageID` / `hasReplyToSystem` for threading. |
| Task status reporting | **Exists.** `TaskStatus` (ReportContent) with `TaskStatusCode` {TASKPEND, TASKSTRT, TASKINPRG, TASKCMPLT, TASKABRT} over `hasCurrentTask`. |
| Command authority between actors | **Exists.** SMX `CommandRelation` (`hasActorReference` + `hasCommandRelationCode`) with a NATO-lineage code list (COMD, OPCON, ADMCON, ATTACH, DETACH, DIRSUP, CLSSUP, COAUTH, ...). Comments are written for ORGANISATIONs. |
| Peer-to-peer addressing | **Exists.** `isFromSender` / `isToReceiver` (already noted under X1). |
| A *handover / transfer of control* construct (message, event, or state change) | **Absent.** No IRI in any of the three files matches handover, transfer, relief, or release; a change of `CommandRelation` can be *stated* in a new report, but nothing names the transfer itself, its acceptance, or its timing. |
| A *control station* entity | **Absent.** No class for the station / operator node that holds control; ASX v0.0.4 has `Operator` (a Person) only. |
| Task *allocation* among candidate performers (offer / bid / assign) | **Absent.** `TaskRequestContent` names one performer; there is no construct for choosing among several. |
| Data synchronization between nodes (what each node knows; reconcile) | **Absent.** Reports are one-way; no state-exchange or reconciliation content. |
| Federation / multi-vehicle addressing of one task | **Absent** as a construct; `CollectiveEntity` (P7, decided) gives the addressee, not the fan-out semantics. |

So C2SIM already has the *request / accept / status* triad that a tasking
layer needs. What it lacks is exactly the multi-node machinery: handover, a
station entity, allocation among candidates, synchronization, and federation
semantics. Those are the five places 4817 / CATL can inform.

### 1.2 What is publicly known about STANAG 4817

- **Scope.** NATO's standard for multi-domain C2 of unmanned systems: one
  control architecture for air, surface, underwater, and ground vehicles,
  spanning "from NATO's high-level command structures down to vehicle ground
  control stations" (Janes). Originally "architecture standards to enable
  high-level C2 interoperability", later extended to "lower-level C2 including
  MUS vehicle reporting and tasking" (Janes).
- **Lineage.** Successor to NIAG studies SG-157 and SG-202; compatible with
  STANAG 4586 (the single-UAV control-station interface, already in the sensor
  slice's tier 3); developed through CMRE under ACT sponsorship.
- **Structure (unverified).** One secondary source describes three volumes:
  encodings for high / medium / low bandwidth; selecting the most suitable node
  for a task; tasking logic. Treat as a pointer, not a fact, until the AEP is
  in hand.
- **Two 4817-compliant message families exercised at REPMUS:** **CATL**
  (CMRE; task-centric messaging for federated autonomous collaboration - task
  allocation, status reporting, data synchronization, handover of control
  between stations) and **I2I** (UK/US "Interoperability to
  Interchangeability"; connecting C2 nodes and national networks). Sources
  disagree on whether 4817 *blends* the two or sits above them.
- **Operational use.** At Task Force X Baltic, "commonality in format and
  language for C2 messages relating to positioning and contacts being passed
  from UUVs and USVs" via CWIX into MARCOM's Mainsail tool (Janes).

### 1.3 What is publicly known about CATL

- A lightweight **application-layer** protocol for coordination and task
  allocation among autonomous systems, with emphasis on AUVs in
  communications-limited environments; **not** a transport - it defines
  structured message formats in **JSON** and **DCCL** (Dynamic Compact Control
  Language, the low-bandwidth encoding).
- Developed in NATO STO **SCI-288** and **SCI-343** ("Enabling Federated,
  Collaborative Autonomy"); "represents a basis for STANAG 4817".
- The first message set has **four message types** "to handle task
  administration and data synchronization" (Furfaro et al. 2021 abstract).
  **The four names and their fields are not in any source this slice could
  reach** - obtaining the paper is step 1 of section 5.
- Demonstrated in simulation (2019) and at sea at REPMUS 22 / Dynamic
  Messenger 22 (vehicle locations and track data relayed to the Maritime
  Operations Centre over CATL; the CMRE network "fully integrated with the
  REPMUS22-DYMS22 C2 centre" using it); still developing in 2024 (CMRE
  drifting-mine work).

---

## 2. The layering point, stated once

C2SIM / ASX is the **commander-to-system** language: what a commander states
to an autonomous system and what the system tells the commander back. STANAG
4817 / CATL is the **station-to-vehicle** (and station-to-station) language:
how a control node tasks vehicles, hands them to another node, and keeps the
nodes' pictures in step. The two meet at the control station, which is a
*C2SIM actor* on one side and a *4817 node* on the other.

The ASX question is therefore **not** "import 4817" but: **should the same
task and status concepts round-trip between the two layers?** If a C2SIM
Order becomes a CATL task and a CATL status becomes a C2SIM TaskStatus, then
the vocabularies must at least be *mappable* - task identity, status values,
performer identity, and handover state must survive the translation. That is
a translation requirement on ASX, and it is the practical reason to look at
4817 at all. (The same point was made for DIS codes in 6m: the question is
what ASX learns, not what it copies.)

---

## 3. What 4817 / CATL offers, finding by finding

### 3.1 Where it bears directly on open findings

| Open finding | What 4817 / CATL supplies | Confidence |
|---|---|---|
| **X1 / Q-G** robot-to-robot coordination content; **G3 / Q-P** system-to-system tasking | CATL *is* task-centric messaging between autonomous nodes - task allocation, status, synchronization. Prior art for the content type the CASEVAC and MCM walks found missing. C2SIM's `TaskRequestContent` + `AcknowledgementBody` are the commander-layer analogue; what is missing is the node-to-node use and the allocation step. | High that it is relevant; message detail unverified |
| **G13 / Q-V** capability self-report, tasking by capability | 4817's reported "selecting the most suitable node for a task" volume and CATL's allocation step presuppose that nodes advertise capability. This is the consumer of Q-V's self-report (BML `WhoHoldingType`). | Medium (volume structure unverified) |
| **P7 / Z1 / Q-J** collective tasking, aggregation, member lifecycle | A task addressed to a federation with per-member status roll-up is how a federated tasking layer handles a group. Gives Q-J's aggregation and handover residuals a tested shape once the collective is under `CollectiveEntity` (decided). | Medium |
| **G1 / Q-O** denied-comms operation | DCCL encoding and the reported bandwidth-tiered volumes are the comms-degraded case made first-class. Also a *new* residual for Q-O: **handover of control between stations** when a link degrades - absent from C2SIM entirely (1.1). | High for the gap; medium for the mechanism |
| **G3 / G19** shared track / contact; targeting hand-off | The Task Force X Baltic use was exactly positions-and-contacts in a common format from UUVs/USVs. The shared track object the cross-cueing finding needs has a fielded precedent. | Medium |
| **N2** persistent tasks | Federated tasking with status and re-allocation is how a standing task is kept alive across nodes and relief. | Low-medium |

### 3.2 Three constructs C2SIM lacks that this source makes visible

These are the slice's own candidates (G30-G32 in section 6):

1. **Control handover.** Who holds control of a vehicle, the transfer of that
   control to another station (offer / accept / effective time), and the
   vehicle's behaviour in between. C2SIM can *state* a command relation
   (`CommandRelation`, OPCON-style codes, written for organisations) but has no
   transfer event, no acceptance, no control-station entity to transfer
   between. CATL names handover of control between stations as a core
   function.
2. **Task allocation among candidates.** `TaskRequestContent` asks one named
   actor. A federated layer asks "who can?", collects answers, and assigns -
   the capability-matching step that Q-V's self-report exists to feed. C2SIM's
   request / `ACKREQGRT` / `ACKREQDEN` pair is a usable *shape* for the
   offer-and-answer; what is absent is the one-to-many solicitation and the
   assign step.
3. **Data synchronization.** Two nodes agreeing on what they both know (tasks,
   tracks, status) after a comms gap. Absent from C2SIM, which is one-way
   reporting; CATL lists it among its four message purposes.

### 3.3 Where it does **not** help

- **P1 / P2 (typing).** 4817 is a control-architecture and interface standard,
  not an entity taxonomy. Its sensor content is payload *control* in the 4586
  lineage, not characterization - the sensor slice already files 4586 in tier
  3 for that reason. Nothing here moves the typing decisions.
- **W1 / Q-K / Q-W (engagement authority).** Nothing. The one critical
  commentary on 4817 makes the same observation this review makes about ASX:
  it standardizes how machines take orders, not the rules under which they
  may act. The kill-box / weapons-control construct (G14, Q-W) remains ASX's
  own contribution.
- **X2 / Q-H (rationale).** No evidence CATL carries explanation content.

### 3.4 Where it touches the other two slices

- **Sensor slice (6l):** none beyond 4586 already being there. If AEP-4817
  carries payload-descriptor fields, they belong in 6l's tier 3 survey; this
  slice does not pursue them.
- **DIS slice (6m):** complementary, not overlapping. DIS informs *what things
  are*; 4817 / CATL informs *how nodes task each other*. The only shared point
  is G23 (entity identity on the wire), where a 4817 vehicle identifier would
  need to map to a C2SIM UUID - a translation-table question for section 2.

### 3.5 Honest limits

- The AEP is unavailable; the volume structure is a single secondary claim;
  the four CATL message names are unobtained. **Everything in 3.1-3.2 is a
  list of places to look, argued on ASX's terms**, exactly as 6m said of DIS.
- CATL's emphasis is AUVs in acoustic-comms environments. Its allocation and
  synchronization choices may be shaped by that (very low bandwidth, long
  latency) in ways that do not transfer to a land UGV on a radio link.
- 4817 answers a *control station's* questions. Some of its boundaries
  (station roles, link management) will be artifacts of that layer rather than
  of command meaning - the same counterweight 6m recorded for DIS.
- The status of 4817 is disputed between sources; a stalled standard is a
  weaker anchor than a ratified one. The CATL papers do not depend on
  ratification and are the safer citation.

---

## 4. Relation to the group's decisions (2026-10)

- **P7 decided** (collective from `CollectiveEntity`) is what makes the
  federated-tasking reading *applicable*: a task addressed to a
  `CollectiveEntity` is the C2SIM side of a CATL federation task. Without P7
  this slice would have had no addressee.
- **P1 decided** (autonomy as a facet on the Platform subtree) means a
  handover construct attaches to a Platform, with `hasControlMode` as the
  state that changes hands - not to a separate Robot class.
- **P2** is untouched by this slice.

---

## 5. Proposed deliverables (the slice, if run)

1. **Obtain and read the two CATL papers** (Furfaro et al. 2021, UComms; Van
   Riet et al. 2023) and, if any member has NATO document access, the
   **AEP-4817 draft**. Record the four CATL message types with their fields.
   Until this is done, the slice cannot go further than this document.
2. **Map the CATL message set against C2SIM's existing triad**
   (`TaskRequestContent` / `AcknowledgementBody` / `TaskStatus`) - a
   four-column table: CATL message, nearest C2SIM content, what C2SIM already
   carries, what is missing - and against Q-G, Q-P, Q-J, Q-V. The same
   reuse-or-align exercise that found BML `WhoMeasuredType` for Q-Q.
3. **Draft the three absent constructs** (section 3.2) as ASX candidates:
   `ControlHandover` (content type), task solicitation / assignment over the
   existing request-acknowledge pair, and a minimal state-synchronization
   report. Each grounded on a scenario already in the library (MCM cross-cue
   for allocation; SubT denied comms for handover; swarm for federation).
4. **State the round-trip requirement** (section 2) as one paragraph in the
   log, with the identifier-mapping note from 3.4, so that whoever later
   builds a 4817 gateway finds the constraint written down.
5. **Instantiate one handover and one allocation message** in the `.xml`
   workbooks (Order side), only after P7 is applied in the OWL.

**Acceptance test:** the slice is done when, for each of X1/Q-G, G3/Q-P,
Z1/Q-J, G13/Q-V, and the Q-O handover residual, it can answer "which CATL (or
4817) message carries this, and what does C2SIM already have for it?" - with
"nothing, must invent" an acceptable answer.

---

## 6. Findings summary (proposed IDs)

To be added to `Issues-And-Comments-Log.md` as section 6n. Status **PROPOSED**
means the *work* is proposed; the RDF grounding in section 1.1 is verified, the
4817 / CATL claims are attributed and second-hand.

| ID | Sev | Status | One-line |
|---|---|---|---|
| G30 | HIGH | PROPOSED | **No control-handover construct.** C2SIM can state a command relation (SMX `CommandRelation`, OPCON-style codes written for organisations) but has no transfer event, acceptance, effective time, or control-station entity to transfer between. CATL lists handover of control between stations as a core function; the SubT denied-comms and MCM scenarios need it. New residual for Q-O. |
| G31 | MED | PROPOSED | **No task allocation among candidates.** `TaskRequestContent` names one performer; there is no one-to-many solicitation or assign step. The existing request / `ACKREQGRT` / `ACKREQDEN` pair is a usable shape for offer-and-answer. This is the consumer of Q-V's capability self-report and the node-to-node half of Q-G/Q-P. |
| G32 | MED | PROPOSED | **No data-synchronization content.** Reporting is one-way; nothing lets two nodes reconcile tasks / tracks / status after a comms gap. CATL names synchronization among its four message purposes. |
| G33 | MED | PROPOSED | **Round-trip (translation) requirement with the station-to-vehicle layer.** If a C2SIM Order becomes a 4817/CATL task and a CATL status a C2SIM `TaskStatus`, then task identity, status values, performer identity, handover state, and vehicle identifiers (cf. G23) must be mappable. A design constraint on ASX's coordination content, not an import. |

## 6b. Proposed decision

- **Q-AA** Decide **what ASX learns from STANAG 4817 / CATL** - as a design
  source for the *coordination* content (Q-G, Q-P, Q-J, Q-V, Q-O), not as
  messages to adopt. Three options, takeable in any combination: **(a)** adopt
  the *shape* of CATL's task-administration set over C2SIM's existing
  request / acknowledge / status triad (G31, G33); **(b)** add the two
  constructs C2SIM has no shape for at all - control handover (G30) and
  state synchronization (G32); **(c)** write the round-trip requirement into
  ASX as a stated constraint (G33) so a later 4817 gateway is buildable.
  Recommended: **(c) now** (one paragraph, no model change), **(a)** once the
  CATL papers are in hand, **(b)** after P7 is applied. Nothing in this
  decision touches P1 / P2 or the engagement-authority thread.
- *The Q-series continues at Q-AB.*

---

## 7. Sequencing and what would shrink this slice

| Step | Work | Rough size |
|---|---|---|
| 1 | Obtain the two CATL papers (+ AEP-4817 if any member has access); record the four message types | Small, but gating |
| 2 | Four-column mapping CATL x C2SIM triad x Q-G/Q-P/Q-J/Q-V | Small-medium |
| 3 | Draft the three absent constructs on library scenarios | Medium |
| 4 | Round-trip requirement paragraph in the log | Small - can run first |
| 5 | Two workbook messages (after P7 is applied) | Small |

**If it has to run smaller, run step 4 alone**, then step 1. Step 4 costs one
paragraph and is the part with lasting value whatever happens to 4817.

**What would kill or shrink this slice:**

- If the CATL papers show the four messages are vehicle-level control
  (waypoints, abort) rather than task-level, 3.1's first two rows weaken to
  "precedent only" and G31 loses its source - G30 and G32 stand on the RDF
  grounding regardless.
- If the sub-group decides ASX stops at the commander-to-system layer and
  never addresses station-to-station coordination, G30-G32 leave ASX scope
  and only G33 (the translation constraint) survives.
- If 4817 does not ratify, nothing in sections 1.1 or 3.2 changes; only the
  citations move from "4817" to "CATL / SCI-343".

---

## 8. Headline

STANAG 4817 cannot be read, but its public basis CATL can, and the RDF
grounding stands on its own: C2SIM already has the request / acknowledge /
status triad a tasking layer needs, and is missing exactly the multi-node
machinery - **control handover, allocation among candidates, state
synchronization, and a control-station entity** - that a federated tasking
layer provides. Those three constructs (G30-G32) are the contribution; the
fourth (G33) is a one-paragraph constraint that should be written down now so
the commander-to-system and station-to-vehicle layers can round-trip later.
Where 4817 does *not* help is just as clear: the typing decisions (P1 / P2) and
the engagement-authority thread (W1 / Q-W), which stay ASX's own. Treat it as 6m
treated DIS - a design source argued on ASX's terms, never codes to copy.

---

## Sources

Reachable only as search-indexed summaries from this session (the proxy blocked
the full pages); all URLs recorded so they can be read in full.

- Janes, "STANAG 4817: final piece of NATO MUS jigsaw puzzle?":
  https://www.janes.com/defence-intelligence-insights/defence-and-national-security-analysis/stanag4817-nato-maritime-unmanned-systems-jigsaw
- Fraunhofer IOSB, INTERACT project, "Interoperability of armed forces
  unmanned systems" (4817 "under development, not publicly available"):
  https://www.iosb.fraunhofer.de/content/dam/iosb/iosbtest/documents/projekte/interact/Interoperability%20of%20Armed%20Forces%20Unmanned%20Systems_korr.pdf
- Euro-SD, "From lab to ship: Portuguese Navy charts course towards integrated
  MUS operations" (CATL vs I2I under 4817):
  https://euro-sd.com/2025/03/articles/43365/from-lab-to-ship-portuguese-navy-charts-course-towards-integrated-mus-operations/
- Seapower, "A MUSt DO: REPMUS is primary means for NATO to develop maritime
  uncrewed capability" (4817 used for MUS C2 at REPMUS 24):
  https://seapowermagazine.org/a-must-do-repmus-is-primary-means-for-nato-to-develop-maritime-uncrewed-capability/
- MDPI J. Mar. Sci. Eng. 13(1):51 (2025), "Evaluation and Testing in
  Operational Environments: Accelerating Development Cycles for Maritime
  Unmanned Systems" (REPMUS network, status publication, handover of control):
  https://www.mdpi.com/2077-1312/13/1/51
- Furfaro, T. et al. (2021), "A Task-Centric Messaging Model for Federated
  Autonomous Collaboration", UComms 2021 - the CATL definition paper (four
  message types; "basis for STANAG 4817"):
  https://www.researchgate.net/publication/356279927_A_Task-Centric_Messaging_Model_for_Federated_Autonomous_Collaboration
- Van Riet, D. et al. (2023), "Experimental Demonstrations of CATL, the
  Collaborative Autonomy Tasking Layer" (REPMUS22 / DYMS22 integration):
  https://www.researchgate.net/publication/373889017_Experimental_Demonstrations_of_CATL_the_Collaborative_Autonomy_Tasking_Layer ;
  TNO record: https://resolver.tno.nl/uuid:7fa49df9-4744-488e-a267-865aa12eb365
- NATO ACT, "Dynamic Messenger 22" (track data relayed to the MOC over CATL):
  https://www.act.nato.int/articles/dynamic-messenger-22
- NATO STO CMRE newsletter Jan-Jun 2024 (CATL as "a data model and family of
  messaging protocols, designed in the SCI-343 RTG"):
  https://www.cmre.nato.int/wp-content/uploads/2024/09/v2%20NATO%20STO%20CMRE%20Newsletter_1_20240712_114854_0000_EDITED_4PAGES%20(002).pdf
- Krog, G. P., "NATO Taught Machines to Take Orders. It Forgot to Teach Them
  the Rules." (commentary; the authority gap):
  https://georgphilipkrog.substack.com/p/nato-taught-machines-to-take-orders
- Revolve, "NATO's Unmanned Systems Standard: Right Problem, Wrong Model?"
  (commentary): https://revolveteam.com/blog/standards-problem/
- Vendor statements of 4817 alignment (evidence of industry uptake only):
  Kongsberg Geospatial MDCS https://www.kongsberggeospatial.com/products/mdcs ;
  Navantia NAIAD https://www.navantia.es/en/product/naiad/
- STANAG 4586 background (the predecessor; levels of interoperability):
  https://publications.sto.nato.int/publications/STO%20Educational%20Notes/STO-EN-SCI-271/EN-SCI-271-03.pdf
