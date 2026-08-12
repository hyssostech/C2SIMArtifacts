# Proposed Slice: DIS Enumerations as a Source for ASX

**Status: PROPOSED.** This is a *scoping* document for a slice of work to be
considered for the future - not a walk that has been performed, and not a
proposed model change. Nothing here has been instantiated into the sample-message
workbooks. What *has* been done is the grounding: every "already exists" and
"does not exist" claim below was checked against the ontologies, the three
instantiation workbooks, and the current SISO / ISO source documents.

**Origin.** An item suggested by Curt: look into the **DIS enumeration
materials** - extract the organizing principles behind that very large body of
data, come up with a succinct categorization, and see what it offers in terms of
enhancements to the ASX effort.

**What this slice is, and is not.** DIS is being examined as a **rich source that
might inform ASX in general** - not as an input to any one ASX question, and
**not as a proposal to use the DIS codes more directly**. The codes are already
carried: C2SIM entities have had the seven-field DIS record since long before
this review (section 1), so "should ASX carry DIS codes?" is a settled question,
not an open one.

What is *not* settled is whether ASX is learning anything from the body of work
behind those codes. SISO-REF-010 is thirty years of a standards community
answering questions ASX is answering now - how to partition the world into kinds,
when a component deserves its own type, where type ends and instance begins, how
to keep a vocabulary growing without it collapsing. **The proposition is to mine
that reasoning, and the evidence in its taxonomy about what needs modeling at
all.** Whether any specific septuplet is ever written into a message is a
separate question this slice does not raise.

Section 3 is therefore organized as a broad map across ASX's open findings, not
around a single theme.

*Companion slice:* `Sensor-Characterization-Slice.md` scopes a separate,
independent item (sensor characterization as a possible extension of its own).
The two are **not** the same slice. DIS happens to touch the sensor question in
two specific places, and those are flagged in section 3.3 and section 4 - but
that overlap is incidental to why this slice is worth running.

---

## 1. Grounding done first

| Checked | Result |
|---|---|
| **DIS entity-type machinery in base C2SIM** | **PRESENT, and complete.** `C2SIM#SISOEntityType` (a `C2SIMContent` subclass) carries all seven DIS Entity Type fields as datatype properties: `hasDISKind`, `hasDISDomain`, `hasDISCountry`, `hasDISCategory`, `hasDISSubCategory`, `hasDISSpecific`, `hasDISExtra`, all `subPropertyOf hasDISCode`. |
| How it attaches | `C2SIM#Entity` has `hasSISOEntityType` at `maxQualifiedCardinality 1` (optional); `C2SIM#Resource` requires exactly 1. The capacity to carry a DIS type is therefore **already settled standard machinery**, not something this slice proposes. |
| The alternative typing hook | `C2SIM#NamedEntityType` = `hasEntityTypeName` + `hasEntityTypeNamespace` (a namespaced string), reached via `hasNamedEntityType`. |
| Use of `hasSISOEntityType` or any `hasDIS*` field in the workbooks | **Zero occurrences**, all three workbooks. |
| Use of `hasNamedEntityType` in the workbooks | **Zero occurrences.** |
| What is used instead | `hasEntityType` / `EntityType` - 8 rows (Init), 6 (Order), 1 (Report) - carrying free text: `UAV`, `Detector-USV`, `UGV-Scout`, `Wheeled / Tracked / Legged UGV`, `Armed-UGV`. |
| Does `hasEntityType` exist in the model? | **No.** Neither `C2SIM#hasEntityType` nor a bare `EntityType` class exists in C2SIM, SMX, or LOX. It is an invented slot. |
| Provenance of those rows | **This review's own.** The first committed conversion of the Init workbook (`cb42d5a`) contains no entity-type field at all - only `SystemEntityList` / `hasSystemEntityList`. The `hasEntityType` rows came from the walk tabs. |

That last row is stated plainly because it cuts against our own work product:
when this review needed to type a platform, it invented a field rather than using
either of the two that the parent standard already defines. **That is a workbook
hygiene defect, not an argument about DIS** - the fix is to use a real C2SIM
property, and `hasNamedEntityType` (a namespaced string, closest to what the
walks actually meant) is the likelier choice of the two. It is recorded here only
because grounding this slice is what surfaced it.

---

## 2. The succinct categorization Curt asked for

SISO-REF-010 *Reference for Enumerations for Simulation Interoperability* is, in
SISO's own words, "essentially a data dictionary for distributed simulation",
maintained by the SISO Standards Activities Committee Special Working Group for
Enumerations. Despite its printed bulk, the whole body reduces to **four table
shapes plus metadata** (Oliver & Ross, 11S-SIW-067, the paper that defined the
machine-readable schema):

| # | Category | XML shape | What it is |
|---|---|---|---|
| 1 | **Value-description pairs** | `enum` / `enumrow` | Plain code lists. The most frequent table type; the direct analogue of a C2SIM `Code` list. |
| 2 | **Bitfields** | `bitmask` / `bitmaskrow` (containing `enumrow`) | Several enumerations packed into bit ranges of one field (e.g. entity appearance / damage state). |
| 3 | **Entity types** | `cet` / `entity` / `category` / `subcategory` / `specific` | The deeply-nested septuplet hierarchy. The bulk of the volume. |
| 4 | **Object types** | `cot` | Like entity types but shallower - point / linear / areal environmental objects. |
| - | *Metadata* | `revisions`, `cr` / `cr_range`, `dict` | Revision history, change-request traceability on every element, acronym dictionary. |

**That is the whole organizing principle: four shapes.** The original document
had 279 tables; the volume comes from category 3, not from structural variety.

**The entity-type record** (category 3) is a 64-bit septuplet,
`Kind.Domain.Country.Category.SubCategory.Specific.Extra`, at bit widths
8/8/16/8/8/8/8, all unsigned, written dotted with no leading zeros
(e.g. the Stryker Mobile Gun System is `1.1.225.2.5.22.0`).

- **Kind** partitions everything that exists: `0 Other, 1 Platform, 2 Munition,
  3 Life form, 4 Environmental, 5 Cultural feature, 6 Supply, 7 Radio,
  8 Expendable, 9 Sensor/Emitter`.
- **Domain**: `0 Other, 1 Land, 2 Air, 3 Surface, 4 Subsurface, 5 Space`.

### 2.1 Five governance principles worth adopting regardless of the codes

From SISO-REF-010.1 OPMAN v08. These are transferable to how ASX manages *its
own* vocabularies - D1's three competing autonomy vocabularies, `SensorType`
(Y2), `MediaTypeCode` (M5) - even if no DIS code is ever adopted.

1. **Graceful fidelity degradation.** The hierarchy lets a low-fidelity system
   say "fighter aircraft" and a high-fidelity one "F-16B" using the same record,
   by leaving trailing fields zero. A trailing zero explicitly means "this entity
   *and all its potential children*."
2. **Implicit types are legal on the wire.** The catalogue deliberately does
   *not* enumerate every combination; unlisted-but-well-formed combinations are
   valid, and only illustrative examples are published. The catalogue is a
   partial index over a generative space, not a closed list. **This is the single
   most important idea for a standards body facing the "massive amount of data"
   problem** - it is how the catalogue stays finite while the space stays open.
3. **Never delete, only deprecate.** Deprecated entries keep their description
   and are never reused; retired real-world systems are *not* deprecated, because
   replay and historical simulations still need them. Corrections are made by
   adding the right entry and linking the wrong one to it via a `Base ID`.
4. **Every entry is globally addressable and traceable.** RFC-4122 UUID on every
   entry; UID integers partition the space (1-8999 tables, 9000-9999 reserved for
   local/site use and never centrally allocated, 10000+ entity and object types);
   any element can carry a `cr` change-request link back to its justification.
5. **Protected enumerations.** Entries referenced normatively by an IEEE or SISO
   standard cannot be changed without a corresponding balloted change to that
   standard. The catalogue is extensible *and* the parts other standards depend
   on are pinned.

---

## 3. What DIS offers ASX, kind by kind

This is the substance of Curt's question. Taking each Entity Kind in turn and
asking what it maps to in the ASX findings log, **at least eight of the nine
kinds land on open ASX items** - which is the case for treating DIS as a general
source rather than a single-purpose one.

| DIS Kind | What it covers (per OPMAN 7.4.2) | Open ASX items it bears on |
|---|---|---|
| **1 Platform** | Vehicles (ships, tanks, aircraft, submarines) *and* systems/structures (SAM systems, C2 systems, facilities). Domain partitions Land / Air / Surface / Subsurface / Space. Systems decompose into heterogeneous subsystem entity types; low-fidelity users take the aggregate, high-fidelity the de-aggregated parts. | **P1** (UAV double-typed ASX `Robot` vs SMX `Aircraft`), **G5/Q-R** (wheeled/tracked/legged UGV, detector/neutralizer USV), **G6** (maritime UUV), **V1** (UnmannedMaritime mis-parented), **G16** (loitering munition), **G17** (sUAS target class). The Domain field *is* the land/air/surface/subsurface partition ASX keeps re-deriving. |
| **2 Munition** | Missiles, ballistic rounds, bullets, torpedoes - "further identified in terms of their fuse and warhead". Rule 7.4.3: weapon-system variants go in the **Extra** field; **ammunition loads shall not be specified in the Entity Type** at all. | **W2/Q-L** (typed weapon / munition / effector). The lesson is the decomposition axis - a munition is characterized by fuse and warhead, not as an atom - and the ruling that a *loadout* is state, not type, which is a line ASX must draw anyway and bears on **G13** (capability self-report). |
| **3 Life form** | Dismounted infantry, scouts, animals. Treated like platforms (they move and some fire). **The Subcategory field encodes the number of individuals, so one Entity Type can represent one or many.** | **P7/Q-B** (swarm/collective not yet taskable), **P10** (heterogeneous swarm membership), **Z1** (report aggregation). A worked precedent for one-type-many-individuals - exactly the collective-representation problem. |
| **4 Environmental** | Physical objects (clouds, icebergs) *and* "inherent characteristics of a particular environment, such as sea state or transmissivity profile". Subcategory encodes size. | **G11/Q-T** (operating-environment conditions: sea state, illumination, GPS-denied, terrain). Direct hit - DIS already treats environmental *conditions*, not just objects, as typed entities. |
| **5 Cultural feature** | "Engineering and natural effects such as craters, bridges, vehicle tracks". | **X4** (obstacle/threat observation subtype), **N1/Q-M** (area as subject; cleared/contaminated/mined area state), the **E-series** engineering findings (breach, crater, obstacle). |
| **6 Supply** | "Supplies other than munitions, such as fuel, food and personnel." The Supply Domain field assigns the **class of supply** (UID 600; values 1-10 derived from AR 710-2). | The **L-series** logistics findings and **Q-L** (cargo typing). The lesson is that *class of supply* is a typing axis in its own right, with an existing doctrinal basis (AR 710-2) ASX could point at rather than invent a cargo vocabulary. |
| **7 Radio** | "Electronic devices for the communication of both audio and data." Uses a **Radio Type** record - same shape as Entity Type, but Category/Subcategory/Specific/Extra are given radio-specific meanings. | **G1/Q-O** (denied-comms operation + **deployable relay entity/node**). The log's residual is precisely "a droppable relay ENTITY/node - `CommunicationNetwork` is a network, not a node". DIS is evidence that a mature vocabulary found it needed the radio as a first-class *entity kind*, not merely a network attribute - which is the distinction G1 is missing. Also **G18** (control-link jamming). |
| **8 Expendable** | "Devices dispensed from another entity" - active or passive countermeasures such as chaff, flares and **decoys**, plus non-countermeasures. | **G8/Q-S** (decoy as a distinct behavior/role). DIS treats "dispensed from another entity" as a kind-level distinction and puts decoys inside it - evidence that expendability is a real typing axis. Also bears on **G16** (a loitering munition is expended) and **G18** (countermeasures). |
| **9 Sensor/Emitter** | Stand-alone sensors and emitters. | The sensor question - see 3.3, and the companion `Sensor-Characterization-Slice.md`. |

### 3.1 The type-vs-instance separation (bears on M1/Q-E)

A non-obvious one, and arguably the most useful single idea here. OPMAN 7.4.5 is
explicit that **unique identification is not the entity type's job**: only naval
ships and oil platforms get uniquely identified types; life forms and most
platforms are "explicitly disallowed" because "there are too many in number and
not sufficiently distinct". Unique identification happens instead through the
Entity Marking field or a Variable Parameter record.

ASX has exactly this problem in **M1** ("`actorReference` is a string but must
define a not-yet-known entity") and **Q-E** (an inline entity-definition
mechanism for newly-observed, uncooperative entities). DIS drew the type/instance
line deliberately and documented why. Worth reading before ASX draws it
differently by accident.

### 3.2 The aggregate / de-aggregate pattern

Kind 1's rule that a system is "typically arranged as a set of heterogeneous
subsystem entity types" - with low-fidelity consumers using the aggregate
system-level type and high-fidelity consumers the subsystem types - is a
general answer to a question ASX faces in several places at once: swarms
(**P7**, **Z1**), MUM-T teams, and armed platforms with separable payloads
(**Q-L**, **G13**).

### 3.3 Two places DIS touches the sensor slice

Flagged rather than developed here; the companion slice owns the sensor argument.

- **Kind 9's boundary criterion** (OPMAN 7.4.2.1 / 7.4.2.9): "subsystems that
  strictly support only a particular platform system are enumerated within the
  respective platform system, but subsystems that can operate in a stand-alone
  manner or that can support multiple systems are enumerated elsewhere such as in
  the Sensor/Emitter kind." Worked example: the Patriot's AN/MPQ-53 radar is
  Kind 9; the ZSU-23-4's welded-in "Gun Dish" fire-control radar is not. This is
  a direct, battle-tested answer to **Q-C/P2/D2** - "is a sensor a first-class
  entity or an attribute?" - and the criterion generalizes beyond sensors to any
  component/whole typing decision (payloads, effectors, relays).
- **The emission parameter records - as a worked precedent.** DIS carries
  emission physics across four modality families (Electromagnetic Emission PDU
  23, Designator 24, IFF 28, Underwater Acoustic 29), each pairing a
  **system-level identity** with a **parameter-level record**. The
  Electromagnetic **Fundamental Parameter Data record** is ten typed 32-bit
  floats, each with a declared unit: Frequency (Hz), Frequency Range (Hz), ERP
  (dB), PRF (Hz), Pulse Width (us), Beam Azimuth Center / Sweep (rad), Beam
  Elevation Center / Sweep (rad), Beam Sweep Sync (%).

  The transferable content is the **shape**, not the record: sensing is modeled
  as identity-plus-parameters, parameters are typed values carrying declared
  units, and modality determines which parameter set applies. **Y5/Q-I** is the
  finding that ASX has no such layer at all, and this is a demonstration that one
  is both necessary and tractable - the EW Emitter Report in
  `NonVideoSensors-Walk.md` wanted "243.0 MHz / 25 kHz", which is exactly a
  frequency-plus-range parameter pair. The four modality families are evidence
  for **Y2** that modality is the right partition, and the separate
  `Emitter Function` enumeration is evidence for **Y4** that *what an emitter is
  for* is a typing axis distinct from *what it is* - the distinction Y4 is
  missing. Whether ASX ends up with these fields, SOSA's, BML's, or its own is
  downstream of the sensor slice, not settled here.

  *Verification status:* the Electromagnetic row is verified field-by-field
  against the DIS Data Dictionary. Designator / IFF / Underwater Acoustic are
  verified only as to **existence, PDU number and modality** - their field lists
  are named from the PDU descriptions, not confirmed field-by-field, and should
  be checked against IEEE 1278.1 before being quoted anywhere normative.

### 3.4 Honest limits - what DIS cannot inform

- DIS types **things**, not **behavior, authority, or intent**. It offers nothing
  for W1/Q-K (engagement authority vs autonomy), G14/Q-W (weapons-control status
  / kill box), X2/Q-H (rationale/explanation), or X1/Q-G (robot-to-robot
  coordination) - several of which are this review's highest-value findings. Its
  reach stops at the typing half of ASX.
- DIS was built to **regenerate emissions and render entities** in a simulation,
  not to **report observations** to a command system. It has no confidence, error
  bound, or false-positive rate, so it cannot inform the reporting semantics that
  G4/Q-Q needs.
- **Its purpose shapes its carve-up, and not always in ASX's direction.** DIS
  distinctions exist to let a simulation render and interact; a C2 vocabulary
  answers to a different question - what a commander must state or be told. Some
  DIS boundaries will be artifacts of rendering fidelity rather than of command
  meaning. The kind-by-kind map is a list of places to *look*, and each transfer
  has to be argued on ASX's own terms, not accepted because DIS drew a line there.
- The **country code** field is central to DIS's identity model (country of
  design or ownership) and answers a question ASX has not asked. It is a good
  illustration of the previous point rather than a problem to solve.

---

## 4. Two defects found in the base standard while grounding

Not the point of the slice, but found in the course of it and cheap to fix:

- **Mis-citation.** All seven `hasDIS*` properties in `C2SIM.rdf` carry
  `rdfs:comment` "...from the DIS standard IEEE 1516-2010". IEEE 1516 is **HLA**,
  not DIS; DIS application protocols are **IEEE 1278.1** (current revision
  1278.1-2012), and the enumerated *values* live in **SISO-REF-010**, not in the
  IEEE standard at all. Both halves of the citation are wrong. Occurrences:
  `C2SIM.rdf` lines ~916-990.
- **Range too narrow.** `hasDISKind`, `hasDISDomain`, `hasDISCategory`,
  `hasDISSubCategory`, `hasDISSpecific` and `hasDISExtra` are all typed
  `xsd:byte`. These are 8-bit **unsigned** fields with range 0-255 - ISO/IEC
  19775-1 (X3D), which carries the same DIS fields normatively, declares every
  one of them `[0,255]` and `entityCountry` `[0,65535]` - whereas `xsd:byte` is
  **signed**, -128..127. Legal DIS values from 128 to 255 cannot be represented.
  `xsd:unsignedByte` is the correct range. (`hasDISCountry` is `xsd:integer`,
  wide enough for the 16-bit field, though `xsd:unsignedShort` would be exact.)

Both are in base `C2SIM.rdf`, outside ASX's remit, so they are for the parent
group - but worth carrying upstream, and the second is a genuine interoperability
bug rather than cosmetics.

---

## 5. Proposed deliverables

1. A **one-page** DIS-enumerations primer for the sub-group - essentially
   section 2 above, expanded only where the group needs it. The item asked for a
   succinct categorization; the deliverable must itself be succinct or it has
   failed on its own terms.
2. A **kind-by-kind opportunity map** (section 3, developed): for each ASX open
   finding, whether DIS offers evidence that a concept needs first-class
   treatment, a criterion, a modeling pattern, or nothing. The "nothing" column
   matters as much as the others - section 3.4 is the first draft of it.
3. A short paper on **which lessons ASX takes up** - the three are independent
   and can be taken in any combination (see Q-Z):
   - **(a) Vocabulary governance** - apply the section 2.1 principles to ASX's
     own code lists (D1's three autonomy vocabularies, `SensorType`,
     `MediaTypeCode`). Touches no DIS content at all; it is a working practice.
   - **(b) Carving criteria as ASX modeling rules** - the component/whole
     criterion (3.3) and the type/instance line (3.1), restated in ASX's terms
     and applied to Q-C/P2/D2 and M1/Q-E.
   - **(c) Taxonomic content as evidence** - treat DIS's kinds as a checklist of
     things a mature vocabulary found it needed, and ask which ASX is missing
     (relay node, environment condition, decoy, supply class, ...).
4. A **placement exercise** on real cases - the diagnostic, not a code-assignment
   task. Take the entity types the walks actually needed - UAV, UGV-Scout,
   UGV-Transport, Detector-USV, armed UGV, loitering munition, FPV quadcopter,
   sUAS target, dropped comms relay, decoy - and ask, for each, **where DIS's
   taxonomy would place it and why**. The output is the *reasoning*, not a
   septuplet: is a loitering munition a Platform, a Munition, or an Expendable,
   what did DIS decide and on what grounds, and does that reasoning survive
   translation into a C2 vocabulary? **Deliberately include the awkward ones** -
   an exercise run only on easy cases proves nothing, and the awkward cases
   (G16's platform-munition hybrid especially) are where the criteria earn their
   keep.
5. A defect note to the parent group for section 4.

---

## 6. Findings summary (proposed IDs)

To be added to `Issues-And-Comments-Log.md` as section 6m. Status **PROPOSED**
means the *work* is proposed, not that the finding is unconfirmed - the grounding
in section 1 is verified.

| ID | Sev | Status | One-line |
|---|---|---|---|
| G23 | MED | **OPEN** | The walks type entities with an invented `hasEntityType` / `EntityType` slot that exists in **no** C2SIM/SMX/LOX file, while the standard already defines two real hooks - `hasNamedEntityType` (namespaced string) and `hasSISOEntityType` (the DIS record, already standard machinery). Self-inflicted: the original converted workbook had no entity-type field at all. A **workbook hygiene defect**, not a DIS-adoption question - the fix is to use a real property, most likely `hasNamedEntityType`. |
| G24 | HIGH | PROPOSED | DIS is a **general-purpose design source** for ASX, not a single-purpose one: at least eight of its nine Entity Kinds bear on open ASX findings - Platform (P1/G5/G6/G16/G17/V1), Munition (W2/Q-L, fuse+warhead axis and the type-vs-loadout ruling), Life form (P7/P10/Z1, one-type-many-individuals), Environmental (G11/Q-T - DIS types environmental *conditions*, not just objects), Cultural feature (X4/N1/Q-M/E-series), Supply (L-series/Q-L, class-of-supply as a typing axis), Radio (G1/Q-O - evidence the relay node is a first-class entity, not a network attribute), Expendable (G8/Q-S - expendability as a typing axis, decoys inside it). The value is the carve-up and its reasoning, not the code values. |
| G25 | HIGH | PROPOSED | DIS's component/whole criterion - stand-alone or multi-platform capability gets its own entity type; welded-in and single-platform is enumerated inside the platform (Patriot AN/MPQ-53 vs ZSU-23-4 "Gun Dish") - is a tested criterion ASX can restate in its own terms to settle Q-C/P2/D2, and it generalizes to any component typing decision (payloads, effectors, relays). Cross-ref `Sensor-Characterization-Slice.md`. |
| G26 | MED | PROPOSED | DIS's emission records are a **worked precedent** for the measurement layer Y5/Q-I says ASX lacks entirely: sensing modeled as system identity + a parameter record of typed values with declared units (Frequency, Frequency Range, ERP, PRF, Pulse Width, beam geometry), with modality selecting the parameter set. Evidence for Y2 that modality is the right partition, and - via a separate `Emitter Function` enumeration - for Y4 that *what an emitter is for* is a typing axis distinct from *what it is*. The transferable content is the shape; which vocabulary ASX adopts is the sensor slice's question. **Limits:** no confidence, error bound, or false-positive rate. Cross-ref `Sensor-Characterization-Slice.md`. |
| G27 | MED | PROPOSED | DIS deliberately separates **type from instance**: unique identification is explicitly *not* the entity type's job (only ships and oil platforms get unique types; unique ID happens via Entity Marking or a Variable Parameter record). Directly relevant to M1 and Q-E, where ASX must draw the same line. |
| G28 | LOW | OPEN | `C2SIM.rdf` mis-cites DIS as "IEEE 1516-2010" on all seven `hasDIS*` properties. IEEE 1516 is HLA; DIS is IEEE 1278.1; the values live in SISO-REF-010. Base-standard defect - for the parent group. |
| G29 | MED | OPEN | `C2SIM.rdf` types six DIS fields as `xsd:byte` (signed, -128..127); they are 8-bit **unsigned**, 0-255 (ISO/IEC 19775-1 declares them `[0,255]`). Legal values 128-255 are unrepresentable. Should be `xsd:unsignedByte`. Base-standard defect - for the parent group. |

## 6b. Proposed decision

- **Q-Z** Decide **which lessons ASX draws from DIS as a design source**. Not a
  question about using the codes - C2SIM entities already carry the DIS record,
  and nothing here proposes changing how or whether that is populated. The three
  are independent and can be taken in any combination:
  **(a) vocabulary governance** - apply the section 2.1 principles to ASX's own
  code lists (D1, `SensorType`, `MediaTypeCode`); touches no DIS content at all.
  **(b) carving criteria as ASX modeling rules** - restate the component/whole
  criterion (G25) and the type/instance line (G27) in ASX's terms and apply them
  to Q-C/P2/D2 and M1/Q-E.
  **(c) taxonomic content as evidence** - use DIS's kinds as a checklist of what
  a mature vocabulary found it needed, and ask which of those ASX is missing
  (relay node, environment condition, decoy, class of supply, ...) (G24).
  Recommended: **(a) and (b) now** - they are cheap, self-contained, and settle
  or sharpen open decisions; **(c) as the placement exercise**, since it is the
  only part that produces a testable result. Each transfer under (c) must be
  argued on ASX's own terms - DIS's boundaries answer a simulation's questions,
  not a commander's (see 3.4). (Scopes G24-G27.)

*Note: the Q-series is exhausted at Q-Z. Continue at Q-AA.*

---

## 7. Sequencing and what would shrink this slice

| Step | Work | Rough size |
|---|---|---|
| 1 | Primer (section 2) + apply the governance principles to ASX's own code lists (Q-Z a) | Small - mostly written above |
| 2 | Placement exercise on the walks' real entity types - where DIS's taxonomy puts each, and why (Q-Z c) | Small-medium - the only step producing a testable result |
| 3 | Restate the carving criteria as ASX modeling rules and apply them to Q-C/P2/D2 and M1/Q-E (Q-Z b) | Medium |
| 4 | Defect note upstream | Trivial |

**If it has to run smaller, run steps 1, 2 and 4.** They are the cheap end, they
are already grounded, and step 2 is the only item here that produces a testable
result rather than a document.

**What would kill or shrink this slice:**

- If the placement exercise (step 2) shows DIS's boundaries consistently fail to
  survive translation into a C2 vocabulary - that they track rendering fidelity
  rather than command meaning - then G24 shrinks from "eight kinds bear on ASX"
  to a much shorter list, and (c) drops out. **That is the falsifier for this
  slice's central claim, and step 2 is what tests it.**
- If P1/Q-A resolves in a way that makes the platform-tree question moot, the
  Kind 1 row loses most of its force - though the other seven kinds and the
  criteria are unaffected.
- **G23 is independent of all of this.** It is a workbook fix worth making
  whatever the sub-group decides about DIS, because the current property does not
  exist in the model.
- Nothing in section 3.4's limits list is a reason to defer steps 1, 2 and 4.

---

## 8. Headline

DIS's "massive amount of data" reduces to **four table shapes** over a
seven-field septuplet. But the codes are not the point - C2SIM entities have
carried the DIS record all along. **The point is the thirty years of reasoning
behind them**, and ASX is answering the same questions now.

Two things come out of that. First, the **carve-up itself is evidence**: at least
eight of the nine Entity Kinds bear on open ASX findings, and several tell ASX
that something it treats as an afterthought deserves first-class typing - the
comms relay is an entity kind, not a network attribute; environmental
*conditions* are typed alongside environmental objects; expendability and class
of supply are typing axes; a munition decomposes into fuse and warhead while its
loadout is state, not type. Second, the **criteria are portable**: when a
component earns its own type (G25) and where type ends and instance begins (G27)
are questions DIS settled deliberately and documented, and they map onto
Q-C/P2/D2 and M1/Q-E. On top of both sit five governance principles ASX can apply
to its own code lists without touching any DIS content - of which *implicit types
are legal on the wire* is the one that actually solves the volume problem.

The honest counterweight: DIS's boundaries were drawn to let a **simulation**
render and interact, and ASX answers to what a **commander** must state or be
told. Some of those boundaries will not survive the translation, and the
placement exercise is precisely what tests which ones do. DIS also says nothing
about authority, intent, or explanation, so it informs the typing half of ASX and
leaves the review's hardest findings (W1/Q-K, G14/Q-W, X2/Q-H) untouched.

Separately, and unrelated to any of the above: grounding this slice surfaced that
the walks type entities with a property that **does not exist in C2SIM, SMX, or
LOX** (G23). That is ours to fix regardless of what the sub-group concludes about
DIS.

---

## Sources

- SISO-REF-010.1-2019 Operations Manual (organizing principles, Kind usage, the
  component/whole criterion, UID scheme, deprecation rules, protected
  enumerations, type-vs-instance rule):
  https://cdn.ymaws.com/www.sisostandards.org/resource/resmgr/reference_documents_/siso-ref-010.1-2019_operatio.pdf
- Oliver & Ross, "Schema of the Machine Readable Enumerations Document",
  11S-SIW-067 (the four table categories; `enum` / `bitmask` / `cet` / `cot`;
  279 tables): https://pross.sdf.org/11S-SIW-067.pdf
- SISO-REF-010-2020 Reference for Enumerations for Simulation Interoperability:
  https://www.mixr.dev/assets/pages/interop/siso-ref-010-v28.pdf
- DIS Entity Type record, Kind and Domain values (NPS DIS Data Dictionary):
  https://faculty.nps.edu/brutzman/vrtp/mil/navy/nps/disEnumerations/JdbeHtmlFiles/entity/index.htm ,
  https://faculty.nps.edu/brutzman/vrtp/mil/navy/nps/disEnumerations/JdbeHtmlFiles/pdu/28.htm
- Emitter System record and Fundamental Parameter Data record:
  https://faculty.nps.edu/brutzman/vrtp/mil/navy/nps/disEnumerations/JdbeHtmlFiles/pdu/bc.htm ,
  https://faculty.nps.edu/brutzman/vrtp/mil/navy/nps/disEnumerations/JdbeHtmlFiles/pdu/c3.htm
- Designator PDU: https://faculty.nps.edu/brutzman/vrtp/mil/navy/nps/disEnumerations/JdbeHtmlFiles/pdu/d3.htm
- DIS PDU type list (EE 23, Designator 24, IFF 28, UA 29):
  https://github.com/open-dis/dis-tutorial/wiki/PDU-Types
- DIS entity-type tutorial (septuplet hierarchy, fidelity degradation):
  https://open-dis.github.io/dis-tutorial/EntityType.html
- ISO/IEC 19775-1 (X3D) DIS component - normative `[0,255]` / `[0,65535]` ranges,
  the evidence for G29:
  https://www.web3d.org/documents/specifications/19775-1/V3.3/Part01/components/dis.html
- IEEE 1278.1-2012 DIS Application Protocols (the standard mis-cited in
  `C2SIM.rdf` as IEEE 1516):
  https://www.bsbedge.com/standard/ieee-standard-for-distributed-interactive-simulation-application-protocols/IEEE1278.1 ;
  draft text: https://freewrl.sourceforge.io/tests/28_Distributed_interactive_simulation/1278.1-200X%20Draft%2016%20rev%2018.pdf

In-repo:
- `Initialization-Walk.md`, `SourcedScenarios-Walk.md`,
  `DroneWarfare-LIRC-OPFOR-Walk.md` (the entity types the placement exercise
  should use);
  `NonVideoSensors-Walk.md` (Y-series, for section 3.3).
- `Sensor-Characterization-Slice.md` - the companion, independent slice.
