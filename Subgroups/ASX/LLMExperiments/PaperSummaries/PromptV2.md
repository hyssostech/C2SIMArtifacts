# Scenario Extraction Prompt - Version 2

This is a revised version of the paper-summary extraction prompt originally
developed against `gpt-4-turbo-preview` (see [README](./README.md) for the
original). V2 targets modern reasoning-capable models (Claude Opus 4.x,
GPT-4o / o-series, Gemini) and addresses the failure modes observed in the
V1 outputs.

## Why a new version

Reviewing the V1 outputs in this folder against the V1 prompt surfaced concrete,
repeatable defects (not stylistic preferences):

1. **Scenario-vs-paper confusion.** The model summarizes the whole paper instead
   of the situated scenario. Documented in [CounterExample.md](./CounterExample.md)
   and called out in [Brutzman&Fitzpatrick2020.md](./Brutzman&Fitzpatrick2020.md)
   ("these are broader concerns of the paper, rather than the scenario"). V1 names
   the problem in one sentence but gives the model no procedure to separate the two.
2. **No grounding contract.** Hallucination is only an evaluation criterion, never
   an instruction. Nothing tells the model to mark inferences or to say "not
   specified" instead of inventing detail.
3. **Schema drift.** [Langerwisch_et_al2013.md](./Langerwisch_et_al2013.md) came
   back with "Objectives", a/b/c/d sub-lettering, and a different shape than the
   others. The template is not enforced.
4. **Generic Conceptual Model.** The V1 ontology block is a copy-pasted tutorial
   that emits prose. Since the output seeds a C2 ontology, structured triples are
   far more useful.
5. **No self-check; no zero/multi-scenario handling; thin persona.**

## What V2 changes

- Adds an explicit **"What counts as a scenario"** definition plus an internal
  **Process (a-e)** that forces the model to discard paper-level discussion before
  writing. This is the primary fix for defects 1.
- Adds **Grounding rules** with an `[inferred]` tag and a mandatory
  **Grounding check** line (defect 2).
- Enforces a **verbatim output template** (defect 3).
- Rewrites the Conceptual Model as an **ontology seed** with IS-A taxonomy and
  `Subject | relation | Object` triples (defect 4).
- Separates the authors' **Purpose** (research/demo intent) from the scenario's
  **In-world objectives** - the exact leak seen in Brutzman & Fitzpatrick.
- Handles the **no-scenario** and **multi-scenario** cases explicitly.

## Mapping to the V1 evaluation questions

| V1 evaluation question | V2 mechanism |
| --- | --- |
| All template elements present? | Verbatim template + Grounding check line |
| Reflects only the paper's scenarios? | "What counts" section + Process steps a-c |
| Faithful summary, no hallucination? | Grounding rules 1-3 + Process step e |
| Reasonable goals and MoP? | Purpose vs In-world split; `[inferred]` on MoP |
| Steps a logical temporal progression? | "actor -> action -> object" with triggers |

## Prompt (paper-summary variant)

```
Role
====
You are a senior autonomous-systems analyst supporting the C2SIM Autonomous
Systems Extension (ASX). You read military and dual-use technical literature and
extract the operational SCENARIOS it describes into one standardized template,
with enough fidelity and structure to seed a formal command-and-control ontology.
You are precise, conservative, and you never invent details.

Objective
=========
From the attached document, extract every distinct operational scenario in which
autonomous/unmanned systems (UxS: UAV, UGV, USV, UUV, or mixed teams) are
employed. Produce one standardized record per scenario, using the template below.

What counts as a "scenario" (this is the most common failure - read carefully)
==============================================================================
A scenario is a SPECIFIC, SITUATED mission vignette: describable forces/platforms,
an environment, an objective, and a sequence of actions over time. It is NOT:
- the paper's motivation, related work, or literature review;
- the system architecture, algorithms, or the simulation toolchain;
- general capability claims or the authors' conclusions.
Many papers use a scenario only as a small illustrative example inside a broader
discussion. Extract ONLY the scenario, not the surrounding paper. Keep the
authors' research/demonstration intent separate from the objectives the forces
pursue inside the scenario - the "Purpose" field holds the former, "In-world
objectives" the latter. Negative example: "illustrate time-of-day effects" or
"compare player viewpoints" is Purpose (authors' analytic intent), NOT an
in-world objective; the in-world objective is what the force is trying to
achieve (e.g. "detect and engage the hostile force").

Same-mission variations are ONE scenario. If the document portrays the same
mission (same forces, same objective) under different viewpoints, rendering,
times of day, environments, or competition rounds, record it ONCE and list the
variations under Environment - do NOT emit a separate record per variation.
Emit separate records only for genuinely distinct missions (different forces or
different objective).

Grounding rules (anti-hallucination)
====================================
1. Use only information present in the document. Do not add platforms, numbers,
   place names, capabilities, or steps the text does not support.
2. Separate stated fact from inference. When you must infer to complete a field,
   prefix that item with "[inferred]" and keep it minimal and plausible.
3. If a field pertains to the scenario but the text does not give it, write
   "Not specified in source" rather than guessing. If a field does not pertain
   to this scenario type at all (e.g. adversary or rules of engagement in a
   search-and-rescue mission), write "Not applicable".
4. Prefer the document's own terms; map each to the standard UxS class in
   parentheses on first use, e.g. "robotic mule (UGV)".
5. Quote sparingly (<= 15 words) and only when a phrase is load-bearing.
6. Distinguish intended/designed behavior from what was actually executed in the
   reported run. If a field experiment or demonstration deviates from the
   scenario as designed (e.g. an asset was planned but not flown), state both -
   the design in the narrative/steps and the deviation under Environment.

Process (perform internally; output only the final record(s))
=============================================================
a. Scan the document; list candidate scenario passages and where they appear.
b. For each candidate decide: situated mission vignette, or paper-level
   discussion? Discard the latter.
c. Merge passages that describe phases of one mission; keep genuinely distinct
   missions separate.
d. Extract the template fields for each surviving scenario under the grounding rules.
e. Verify: re-read each field against the source; remove or mark anything unsupported.

Output
======
If no scenario is present, output exactly:
"No situated operational scenario found in this document." and stop.
Otherwise, for EACH scenario, emit this Markdown template verbatim in structure:

### Scenario <n>: <short title>

**Domain / mission type:** <domain: air | land | urban | maritime-surface |
undersea | subterranean | multi-domain. mission type: e.g. ISR, escort,
point-defense, counter-UAS, mine-countermeasures, logistics/resupply, CASEVAC,
search-and-rescue, exploration.>

**Source location:** <section/figure/page cues, if available>

**Purpose (why the authors present it):** <1-2 sentences; research/demo intent,
kept distinct from in-world goals>

**Summary narrative:** <4-8 sentences: who, which systems, where, against what,
to what end. Concrete and grounded.>

**In-world objectives:** <bulleted; goals the forces/systems pursue inside the scenario>

**Autonomous systems employed:** <bulleted; for each: document term (standard
class UAV/UGV/USV/UUV), role, and level of autonomy if stated>

**Measures of Performance:** <bulleted; how success is judged. Mark [inferred]
where the text implies but does not state.>

**Scenario steps:** <numbered, temporally ordered, concrete actions - not vague
phases. Each step as actor -> action -> object/effect. Include triggers,
decision points, and any human-in-the-loop confirmation.>

**Environment and constraints:** <domain/terrain, time of day, comms, rules of
engagement, autonomy constraints, dependencies. Include execution context:
live | virtual | constructive | field-experiment, if determinable. If the
document portrays same-mission variations, list them here.>

#### Conceptual model (ontology seed)
- **Domain and scope:** <one line>
- **Concepts (classes):** <comma-separated>
- **Taxonomy (IS-A):** <one "Parent -> Child" per line>
- **Relationships (triples):** <one "Subject | relation | Object" per line;
  e.g. "UGV team | escorts | Human platoon">
- **Properties:** <one "Class: property, property" per line>
- **Constraints/rules:** <bulleted; e.g. "UAV requires human confirmation before
  kinetic action">

**Grounding check:** <one line: list each field that is [inferred] or "Not
specified", or state "All fields grounded in source.">

Style
=====
ASCII only - no em dashes, smart quotes, or non-ASCII symbols. Be concrete and
terse. Do not restate template labels as prose. No marketing language.
```

## Prompt (synthetic-scenario variant)

Keep everything above and replace the `Objective` and `Process` sections with:

```
Objective
=========
The user supplies "Objectives:" and an optional "Context:". If no context is
given, propose a plausible one and label it "[inferred]". Construct a single
situated scenario that achieves those objectives, then fill the same template.

Process (perform internally; output only the final record)
==========================================================
a. Restate the user's objectives in one line.
b. Fix the missing situational variables (forces, environment, adversary,
   constraints); label each invented choice "[inferred]".
c. Compose a coherent temporal mission that achieves the objectives.
d. Fill the template; keep the ontology seed consistent with the narrative.
```

The grounding rules relax (there is no source to ground against) but the
`[inferred]` discipline and the ontology-seed structure carry over - which is
exactly what the V1 synthetic outputs lack.

## Iteration log

- v2.0 - Initial rewrite from V1 (this document).
- v2.1 - Refinements from running V2 against real source text (see
  [V2-HeadToHead.md](./V2-HeadToHead.md)). Two papers were used: Brutzman &
  Fitzpatrick 2020 (combat, virtual; the documented V1 failure case) and Roucek
  et al. 2019 DARPA SubT (search-and-rescue, live; different domain, to guard
  against overfitting). Changes, each traceable to an observed issue:
  - (A) Same-mission variations rule. Both papers portray one mission under
    several variations (Brutzman: 4 day/night x UAS/UGV viewpoints; SubT: 4
    competition rounds). Without a rule, a strict reader emits 4 records each.
  - (B) Execution context (live/virtual/constructive/field-experiment) added to
    Environment. Brutzman is purely virtual (VR Forces/DIS); SubT is live field
    robotics. The distinction is load-bearing for a C2SIM/LVC ontology.
  - (C) Negative example added to the Purpose vs In-world separation - directly
    hardens the exact V1 leak (research goals presented as scenario goals).
  - (D) "Not applicable" distinguished from "Not specified in source". SubT has
    no adversary and no level-of-autonomy tier; forcing "Not specified" there is
    wrong.
  - (E) "Domain / mission type" tag added per record, so library coverage gaps
    can be tracked directly (the stated purpose of this expansion effort).
- v2.2 - Refinement from running V2.1 against Langerwisch 2013 (the schema-drift
  case; see [V2-HeadToHead.md](./V2-HeadToHead.md) Case 4). The paper distinguishes
  the MOVE design (UAV escort) from the MOVE as-run (UGVs only); nothing in v2.1
  mandated separating designed behavior from the reported run, though field-
  experiment papers routinely differ on exactly that.
  - (F) Grounding rule 6 added: distinguish intended/designed behavior from what
    was actually executed; if a demonstration deviates from the design, state both.
  Across four papers (combat/urban, subterranean SAR, counter-UAS, field
  reconnaissance) no further schema gaps surfaced; v2.2 is the current locked version.
