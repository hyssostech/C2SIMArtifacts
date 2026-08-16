# Proposed Slice: Sensor Characterization

**Status: PROPOSED.** This is a *scoping* document for a slice of work to be
considered for the future - not a walk that has been performed, and not a
proposed model change. Nothing here has been instantiated into the sample-message
workbooks. What *has* been done is the grounding: every "already exists" and
"does not exist" claim below was checked against the ontologies and the current
OGC / W3C source documents.

**Origin.** An item suggested by Curt: look into the **characterization of
sensors** - he thinks this might be a whole extension worth on its own, and one
that could be based on existing standards rather than invented.

Both halves of that suggestion hold up under grounding, and this document sets
out the evidence for each so the sub-group can judge the slice rather than take
it on faith.

*Companion slice:* `DIS-Enumerations-Slice.md` scopes a separate, independent
item (what the DIS enumeration materials offer ASX in general). The two are
**not** the same slice and can be run in either order or alone. Where the DIS
material genuinely bears on sensors, it is cross-referenced in section 4.3 -
that overlap is a bonus, not the reason either slice exists.

---

## 1. Grounding done first

Verified before proposing anything, to avoid inventing gaps or overselling reuse.

| Checked | Result |
|---|---|
| A `Sensor` class in base C2SIM / SMX / LOX | **Absent.** Only `asx#Sensor` (v0.0.1), `subClassOf ElectricDevice`, carrying **no properties at all**. |
| Observation subtypes | Exactly six: {Activity, Health, Location, Name, Resource, SubjectType}Observation. Confirms the `NonVideoSensors-Walk.md` grounding. |
| Emitter / radar / acoustic / thermal / optical observation classes | **Absent** from all three base files. |
| Generic measurement value+unit property | **Absent.** Only `hasSpatialMeasure`, `hasCoordinateValue`, logistics quantities, and `smx#hasConfidenceLevel`. |
| Sensor capability / performance properties | **Absent.** No range, accuracy, resolution, field-of-view, detection limit, or operating-condition property anywhere. |
| Proposed enums | `SensorType` (ConceptMapping) = {Visual, EW, Counter EW, Audio}; `MediaTypeEnum` / v0.0.3 `MediaTypeCode` = {VID, AUD, IMG, DOC, TXT, NOS}. |

So the sensing half of ASX is currently a bare class, a four-value enum, and one
media-based report. Everything else a sensor model needs has yet to be built.

---

## 2. Is it actually extension-sized? (testing Curt's framing)

Two independent arguments say yes.

### 2.1 The finding count

Sensor-related open items already in `Issues-And-Comments-Log.md`, before any new
work:

**Core sensor findings (11):** D2 (sensor modeled three incompatible ways),
P2 (sensor: declared entity or attribute on a platform?), M3 (same concept
modeled two ways across report sheets), M4 (`SensorObservation subClassOf
ActivityObservation` questionable), M5 (`MediaTypeCode` conflates media format
with sensor modality), Y1 (media-based report model does not generalize),
Y2 (`SensorType` enum incomplete), Y3 (no detection/hazard Observation subtype),
Y4 (EW sensing has no report content type), Y5 (no sensor-reading value+unit
property), G4 (generic parameterized Detection Report).

**Adjacent findings a sensor model would carry (4):** X4 (obstacle/threat
observation subtype), G3 (cross-cueing + shared track/contact object),
G13 (dynamic capability self-report), G18 (adversarial EW against own autonomy).

**Open decisions it would resolve or absorb (6):** Q-C, Q-F, Q-I, Q-P, Q-Q, Q-V.

Fifteen findings and six decisions is not a property or two bolted onto the
report model. It is comparable in weight to everything the ASX OWL currently
contains (v0.0.1: 15 classes, 1 object property, 0 datatype properties; v0.0.3:
26 ASX classes, 4 object + 2 datatype properties).

### 2.2 The structural argument

A sensor model has to answer **four separable questions**, and ASX currently
conflates them - which is itself the root of D2/P2/M3/M4/M5:

| Question | What it types | Current ASX state |
|---|---|---|
| **(a) What is the device?** | The sensor as a thing: modality, model, mount | `asx#Sensor` class + `SensorType` enum + `SensorCapability` equipment - three competing models, no properties (D2/P2) |
| **(b) What can it do?** | Performance envelope: range, accuracy, resolution, FOV, detection limit, operating conditions | **Nothing.** No capability layer at all (G13) |
| **(c) What did it observe?** | The observation event: value, unit, phenomenon, time, place, confidence | **Nothing generic.** Only the media-based `Video Detection Report` (Y1/Y5) |
| **(d) How is it configured / tasked?** | Modes, cueing, slew, collection tasking | **Nothing.** Cross-cueing has no element (G3) |

Every mature sensor standard separates (a)-(d). ASX has a partial (a) and nothing
else. That four-way separation is the extension's backbone, and it is what makes
this too big to fold into the report model as a patch.

**Conclusion: Curt's framing holds. This is extension-sized, not
attribute-sized.** Whether it becomes a *separate extension* or a *large section
inside ASX* is a real fork and should be decided explicitly - see Q-Y.

---

## 3. Curt's second point: build on existing standards

Also supported, and by unusually strong evidence. Three independent lineages
converge on the same shape for question (c):

| Lineage | The observation shape it defines | Status in this review |
|---|---|---|
| **BML `WhoMeasuredType`** {value, UOM, phenomenon, sensor, time, place} | C2SIM's own ancestry (Remmersmann 2015) | Already identified in `ValidationEvidence-Walk.md` as the highest-value input to Q-Q; flagged "re-adopt, do not invent" |
| **W3C/OGC SOSA** `Observation` {hasResult, observedProperty, madeBySensor, resultTime, phenomenonTime, hasFeatureOfInterest, usedProcedure} | Joint W3C Recommendation + OGC Implementation Standard | Not previously considered by this review |
| **DIS emission parameter records** (frequency, PRF, ERP, pulse width, beam geometry - each a typed float with a declared unit) | IEEE 1278.1 / SISO-REF-010 | Not previously considered by this review; see `DIS-Enumerations-Slice.md` |

Three vocabularies, built by different communities for different purposes, landed
on {value, unit, property observed, by what sensor, when, where}. **Re-deriving it
a fourth time inside ASX would be a modeling error.**

---

## 4. Candidate standards to survey (the proposed work)

Not a recommendation - a survey list, with what each is expected to contribute
and why it is on the list. Precedent format:
`Reference Materials/Standards-for-Autonomous-Systems-Behavior.md`, which did the
same job for the autonomy-behavior axis.

### 4.1 Tier 1 - directly importable, already axiomatized

- **W3C/OGC SOSA/SSN (Semantic Sensor Network Ontology, 2023 Edition).** Already
  an OWL ontology, so ASX can align or import rather than restate. Covers (a),
  (c) and part of (d): `Sensor`, `Observation`, `ObservableProperty`,
  `FeatureOfInterest`, `Procedure`, `Platform`, `Actuator`, `Sampler`, with
  `observes`, `madeObservation`, `hasResult`, `observedProperty`, `resultTime`,
  `phenomenonTime`, `isHostedBy`. Directly addresses Y1/Y3/Y5/Q-I/Q-Q, and
  `isHostedBy` gives P2/Q-C the sensor-on-platform *relation* without inventing
  anything.
- **SSN-System module** - this is the **characterization** vocabulary
  specifically, and the closest match to Curt's phrasing. Classes:
  `SystemCapability`, `SystemProperty`, `MeasurementRange`, `Accuracy`,
  `Precision`, `Resolution`, `DetectionLimit`, `Frequency`, `Latency`,
  `Sensitivity`, `Selectivity`, `ResponseTime`, `Drift`, `OperatingRange`,
  `SurvivalRange`, `Condition`; properties `hasSystemCapability`,
  `hasOperatingRange`, `hasSurvivalRange`, `hasSystemProperty`. **This is
  column (b) of the 2.2 table, off the shelf** - the layer ASX has nothing for -
  and it supplies the vocabulary G13 (capability self-report) needs.

### 4.2 Tier 2 - richer sensor description, heavier commitment

- **OGC SensorML (Sensor Model Language).** A sensor *description document*
  standard rather than an ontology. Its section list is a ready-made checklist
  for what "characterizing a sensor" even means: identification, classification,
  characteristics, capabilities, contacts, documentation, legal/security
  constraints, validTime, position / local reference frame, inputs, outputs,
  parameters, modes, history, configuration. Its component types -
  `PhysicalComponent` (atomic transducer) vs `PhysicalSystem` (assembly) vs
  `SimpleProcess` / `AggregateProcess` (non-physical) vs `Deployment` - draw a
  distinction ASX needs and lacks. It depends on SWE Common for data typing and
  ISO 19115 for metadata, so adopting it wholesale is a large commitment;
  **mining its section list as evaluation criteria is cheap, and is the
  recommended use.**
- **ISO 19156 / OGC Observations, Measurements and Samples.** The conceptual
  model beneath SOSA. Relevant if the sub-group wants the abstract model rather
  than an OWL artifact.

### 4.3 Tier 3 - military-specific, for vocabulary alignment rather than import

- **NATO STANAG 4586 / AEP-84** (UAV Control System interfaces). Already cited in
  `Standards-for-Autonomous-Systems-Behavior.md` as a C2SIM-adjacent constraint.
  Its Data Link Interface separates payload control and payload status from
  air-vehicle control - the same (d)/(c) split. Worth checking for the
  payload/sensor *description* fields specifically; the public literature
  describes the message classes but not the field lists, so this needs the actual
  STANAG.
- **MISB ST 0601 (UAS motion-imagery metadata) / STANAG 4609 / STANAG 4607
  (GMTI).** Relevant to Y1/M5 specifically: these already separate "the imagery"
  from "the sensor metadata about the imagery", which is the exact category error
  M5 records.
- **IEEE 1451 / TEDS** (transducer electronic data sheets) - self-describing
  sensors; relevant to G13 if the sub-group wants the machine-discovery angle.
- **DIS / SISO-REF-010 - as a design precedent, not a code source.** The DIS
  codes are already carried by C2SIM entities and are not what is interesting
  here. Two pieces of DIS *reasoning* bear on sensors, and both are set out in
  `DIS-Enumerations-Slice.md` rather than duplicated:
  - its **Sensor/Emitter entity kind** rests on a tested criterion for *when a
    sensor is an entity in its own right versus a part of its platform*, which is
    exactly the open Q-C/P2/D2 question (that slice's G25);
  - its **emission parameter records** are a worked precedent for the shape of a
    media-independent measurement layer - system identity plus a parameter record
    of typed values with declared units, modality selecting the parameter set -
    which is the layer Y5/Q-I says ASX lacks entirely, with the modality split
    as evidence for Y2 and the separate emitter-function axis as evidence for Y4
    (that slice's G26). The shape is the transferable part; which vocabulary ASX
    adopts is this slice's question, not DIS's.

  **Honest limit:** DIS was built to regenerate *emissions* in a simulation, not
  to report *observations* to a command system. It has no confidence, error
  bound, or false-positive rate - all of which G4/Q-Q requires - and it types the
  *emitting* side far better than the *sensing* side. It is a strong source for
  (a) and the physics of (c), a weak source for (b), and no source for the
  reporting semantics ASX actually needs. SOSA/SSN and BML cover what DIS does
  not.

**Deliberately excluded:** IEEE 1872.2 (AuR) and the rest of the CORA family are
already surveyed in `Standards-for-Autonomous-Systems-Behavior.md` and cover the
autonomy axis, not the sensing axis. Do not re-survey them here.

---

## 5. Proposed deliverables

1. A survey document (`Reference Materials/Standards-for-Sensor-Characterization.md`),
   same shape as the existing autonomy-standards survey: grouped by how directly
   each candidate is reusable, with a recommended priority order and sources.
2. A **four-column mapping** - (a) device / (b) capability / (c) observation /
   (d) configuration - showing for each candidate standard what it supplies and
   what it leaves open, so the sub-group can pick a spine rather than a pile.
3. A recommendation on scope: **own extension** vs **ASX section** (Q-Y).
4. If and only if (3) lands on "own extension": a one-page charter - name, scope
   boundary against ASX, and the list of ASX findings that transfer to it.

**Acceptance test for the survey**, so it does not become an open-ended reading
project: it is done when it can answer, for each of Y1-Y5, D2, P2, M3-M5, G4 and
G13, "which existing standard already has this, and what is the term?" - with
"nothing found, must invent" being an acceptable and useful answer.

---

## 6. Findings summary (proposed IDs)

To be added to `Issues-And-Comments-Log.md` as section 6l. Status **PROPOSED**
means the *work* is proposed, not that the finding is unconfirmed - the grounding
in section 1 is verified.

| ID | Sev | Status | One-line |
|---|---|---|---|
| G20 | HIGH | PROPOSED | Sensor characterization is extension-sized: 15 open findings (D2, P2, M3-M5, X4, Y1-Y5, G3, G4, G13, G18) + 6 open decisions (Q-C, Q-F, Q-I, Q-P, Q-Q, Q-V) already cluster on it - comparable in weight to the entire current ASX OWL. Structurally it must answer four separable questions (device / capability / observation / configuration); ASX has a partial first and nothing else. Supports Curt's "own extension" framing. |
| G21 | MED | PROPOSED | Three independent lineages - BML `WhoMeasuredType` {value, UOM, phenomenon, sensor, time, place}, W3C/OGC SOSA `Observation`, and the DIS emission parameter records - converge on the same observation shape. Adopt, do not re-derive a fourth time. |
| G22 | MED | PROPOSED | The capability layer (question (b): range, accuracy, resolution, detection limit, operating conditions) is **entirely absent** from ASX and has an off-the-shelf vocabulary in the SSN-System module (`SystemCapability`, `MeasurementRange`, `Accuracy`, `Resolution`, `DetectionLimit`, `OperatingRange`, `SurvivalRange`, ...). This is also what G13 (capability self-report) needs. |

## 6b. Proposed decision

- **Q-Y [deck]** Decide whether **sensor characterization becomes its own
  extension** (a sibling to ASX) or stays a section inside ASX. For: the finding
  count (G20) and the four-question structure that no single current ASX element
  addresses. Against: it fragments the standard, and the sensor model's main
  consumer is ASX itself. Decide **explicitly and early**, because the answer
  changes *where* Y1-Y5, D2, P2, M3-M5, G4, G13, Q-C, Q-F, Q-I, Q-P, Q-Q and Q-V
  get resolved. (Scopes G20-G22.)

---

## 7. Sequencing and what would shrink this slice

| Step | Work | Rough size |
|---|---|---|
| 1 | Tier-1 survey only (SOSA/SSN + SSN-System) and the four-column mapping | Medium - highest yield per unit effort |
| 2 | Tier-2 mining: SensorML section list as evaluation criteria | Small |
| 3 | Tier-3 military alignment (STANAG 4586 field lists, MISB) | Medium, needs document access |
| 4 | Scope recommendation + charter if applicable | Small |

**If it has to run smaller, run step 1 alone.** SOSA/SSN plus SSN-System covers
three of the four questions and is the only candidate that is already an OWL
artifact ASX can align to directly.

**What would kill or shrink this slice** (stated so the sub-group can check
rather than take it on faith):

- If the sub-group decides ASX will not carry sensor *readings* at all - only
  media references and analyst comment - then this collapses to a taxonomy fix
  (Y2 alone) and **G20 is wrong**.
- If the sensor extension is chartered separately (Q-Y), most of these findings
  leave this review's scope entirely and this document becomes a handoff rather
  than a work plan.
- If STANAG 4586 / MISB documents cannot be obtained, tier 3 shrinks to
  DIS-only alignment; tiers 1 and 2 are unaffected (all public).

---

## 8. Headline

Curt is right on both counts. Sensor characterization is extension-sized by the
log's own count - 15 findings and 6 decisions, comparable to the whole current
ASX OWL - and it should be **assembled** from existing standards rather than
designed: SSN-System for the capability envelope ASX has nothing for, SOSA plus
BML `WhoMeasuredType` for the observation event, SensorML's section list as the
checklist of what characterizing a sensor even means. The strongest single piece
of evidence for "adopt, don't invent" is that three unrelated lineages already
agree on the observation shape.

The one decision that should not drift is Q-Y: whether this is its own extension
or an ASX section changes where a dozen open findings get resolved.

---

## Sources

- W3C/OGC Semantic Sensor Network Ontology, 2023 Edition (SOSA core + the
  SSN-System capability module): https://w3c.github.io/sdw-sosa-ssn/ssn/
- SSN/SOSA as an OGC standard:
  https://www.ogc.org/standards/semantic-sensor-network-ontology/
- Janowicz et al., "SOSA: A Lightweight Ontology for Sensors, Observations,
  Samples, and Actuators": https://arxiv.org/pdf/1805.09979
- OGC SensorML Encoding Standard (description sections; PhysicalComponent vs
  PhysicalSystem vs SimpleProcess / AggregateProcess / Deployment):
  https://docs.ogc.org/is/23-000/23-000.html
- STANAG 4586 overview (NATO STO educational note; Data Link Interface, payload
  control vs status): https://publications.sto.nato.int/publications/STO%20Educational%20Notes/STO-EN-SCI-271/EN-SCI-271-03.pdf

In-repo:
- `NonVideoSensors-Walk.md` (Y1-Y5), `SourcedScenarios-Walk.md` (G4),
  `ValidationEvidence-Walk.md` (BML `WhoMeasuredType`, G13),
  `DroneWarfare-LIRC-OPFOR-Walk.md` (G18),
  `Reference Materials/Standards-for-Autonomous-Systems-Behavior.md` (survey
  precedent; IEEE 1872.x already covered there).
- `DIS-Enumerations-Slice.md` - the companion, independent slice; section 4.3
  above names the two places it genuinely bears on sensors.
