# Documents Needed to Close the ASX Coverage Gaps

A sourcing brief for the scenario-scavenger session. It lists the source
documents that would fill the **document-shaped** gaps found by the
instantiation review - i.e. the gaps in section 8 bucket 3 of
`Issues-And-Comments-Log.md` (invisible-domain gaps + validation holes). It does
**not** ask for sources for the model-internal gaps (missing property layer,
typing decisions, track drift) - those are not fixed by documents.

## Extraction criteria (unchanged from the current pipeline)

Match what the scavenger already uses (`CandidateSources.md`, `PromptV2.md`):
a **concrete, situated mission vignette** in a technical report, thesis, or
after-action review - **not** a survey, doctrine overview, or news item. The
source must be readable in full and describe an actual (or simulated/experiment)
mission with units, steps, and constraints. Open-access strongly preferred.

## Two kinds of need

- **Validation holes** - concepts the ASX model already asserts/intends, but
  which **no sourced scenario exercises** (per the sourcing session's own
  "Reading 1"). Sourcing these grounds concepts that are currently
  asserted-but-untested.
- **Invisible-domain gaps** - mission types absent from the library, whose
  requirements the ontology never saw.

Already sourced (do **not** re-request): maritime MCM, subterranean, land
sustainment. Already have a candidate listed in `CandidateSources.md` but **not
yet extracted**: counter-UAS/swarm, human-machine teaming (HATOM), humanitarian
SAR - these need extraction, and a more vignette-rich source is welcome.

## Priority requests

Ordered by ontology leverage and how clearly the hole is confirmed.

### 1. Explainability / human-on-the-loop decision mission  (validation hole - clearest)
- **Why:** the ASX design explicitly carries "explainable reasons" reports and
  on-the-loop status, but **zero** sourced scenarios exercise them. This is the
  single clearest hole.
- **Find a mission where:** an autonomous system must justify or explain a
  decision (why it re-planned, why it aborted), or a human on-the-loop
  approves / overrides an autonomous action (esp. an engagement).
- **Source types:** MUM-T / human-autonomy-teaming field experiments; AFRL/DARPA
  autonomy-trust or explainable-autonomy studies; trust-in-automation AARs.
- **Extract for:** rationale/explanation report content (Q-H), on-the-loop
  approval gating and engagement authority as a function of autonomy level
  (Q-K/W1), graded/phase-dependent level of autonomy (Q-D).

### 2. CBRN reconnaissance mission  (validation hole + sensor-reading)
- **Why:** the model has a CBRN detection report tab, but no sourced CBRN
  mission grounds it; also exercises the sensor-reading gap.
- **Find a mission where:** an unmanned system detects/maps a chemical,
  biological, radiological, or nuclear hazard.
- **Source types:** DTIC CBRN-defense experiments; NATO CBRN robotics trials;
  service CBRN reconnaissance AARs.
- **Extract for:** hazard/agent detection observation (Y3), measurement value +
  unit (Y5), contaminated-**area** marking (N1/Q-M), generic detection report
  with confidence (Q-Q).

### 3. Electronic-warfare sensing / attack mission  (validation hole)
- **Why:** EW emitter-report tab exists but is ungrounded; EW *sensing* has no
  report content type today.
- **Find a mission where:** an unmanned system geolocates/intercepts an emitter
  or conducts electronic attack (jamming) with a described engagement.
- **Source types:** DTIC EW reports; naval/army EW experiment writeups.
- **Extract for:** emitter/signal observation and frequency/bandwidth reading
  (Y4/Y5), effect vs ROE (LOX already has weapon ROE), generic detection (Q-Q).

### 4. Persistent surveillance / sentry / standing-watch mission  (validation hole)
- **Why:** persistence/standing-tasking is exercised by only one case (MCM
  revisit); barely tested.
- **Find a mission where:** an autonomous system holds a standing watch or
  persistent ISR with a revisit/relief cadence (perimeter security, sentry,
  loiter-and-report).
- **Source types:** base/force-protection experiments; persistent-ISR CONOPS with
  a concrete vignette.
- **Extract for:** standing/persistent task with cadence (N2), station-keeping
  and relief (formation geometry Q-U), area coverage (Q-N).

### 5. Counter-UAS / swarm-vs-swarm engagement  (invisible domain - most novel)
- **Why:** absent from the library; swarm-vs-swarm and layered defeat are the
  most novel C2 concepts unaddressed.
- **Candidates already listed** (need extraction): CNAS "Countering the Swarm";
  CNA "PRC Concepts for UAV Swarms." A more step-level vignette would be ideal.
- **Extract for:** collective/swarm typing under engagement, layered
  detect/soft-kill/hard-kill task/effect, graded LoA under time pressure,
  coordination as a relation (Q-B/Q-K/Q-P).

### 6. Human-machine teaming mission (C2 / tasking level)  (invisible domain)
- **Why:** teaming at the C2/ontology level is absent; needed to ground
  machine-to-machine and on-the-loop constructs.
- **Candidate listed:** HATOM (NATO STO) - but that is a vocabulary model, so
  **also** find a MUM-T *mission* vignette (human + robot task allocation).
- **Extract for:** mixed human-machine task allocation and roles, on-the-loop
  status, cross-cueing (Q-G/Q-P).

### 7. Humanitarian / disaster-response SAR (non-combat, dual-use)  (invisible domain)
- **Why:** every sourced mission assumes a hostile side; a no-adversary SAR
  mission stresses neutral-actor framing and SAR tasks.
- **Candidate listed:** MDPI Drones (2020) UAV+ground-robot SAR. Extract it.
- **Extract for:** no-adversary mission framing and neutral actors (G10), survivor
  detection + recovery/rescue tasks (R2), area search (Q-N).

### 8. Formation / convoy-geometry mission  (expressiveness - G12)
- **Why:** relative/formation geometry (orbit, convoy spacing, observation-pose
  patterns) has no construct; only partially seen (Langerwisch MOVE).
- **Find a mission where:** vehicles hold an explicit formation/convoy geometry or
  coordinated observation pattern (one overhead, others orbiting).
- **Source types:** convoy-automation or cooperative-ISR experiments with
  described geometry.
- **Extract for:** formation/relative-geometry construct (Q-U), escort/follow
  (Q-L), coordination relations (Q-P).

### 9. Combat-engineering / EOD manipulation mission  (grounding upgrade - E-series)
- **Why:** engineering/manipulation was walked from an LLM-generated MUTT text,
  not a real sourced report; the manipulation task family is otherwise ungrounded.
- **Find a mission where:** an unmanned system digs/breaches/emplaces or an EOD
  robot manipulates/neutralizes a device.
- **Source types:** combat-engineer or EOD experiment/AAR; DTIC.
- **Extract for:** manipulation/effector task verbs (E1/Q-L), effector/manipulator
  equipment typing (E2), area-cleared state (N1).

## Optional / lower priority

- **Degraded-environment mission** emphasizing weather / terrain / illumination
  effects on autonomy - grounds environment-condition attributes (G11/Q-T). SubT
  and MCM partially cover this; a dedicated case would strengthen it.

## What each request ultimately grounds (traceability)

| Request | Primary decisions it grounds |
|---|---|
| 1 Explainability / on-the-loop | Q-H, Q-K (W1), Q-D |
| 2 CBRN recon | Q-Q (Y3/Y5), Q-M (N1) |
| 3 EW sensing | Q-Q (Y4/Y5) |
| 4 Persistent watch | N2, Q-U, Q-N |
| 5 Counter-UAS / swarm | Q-B, Q-K, Q-P |
| 6 Human-machine teaming | Q-G, Q-P |
| 7 SAR (non-combat) | G10, R2, Q-N |
| 8 Formation geometry | Q-U, Q-L, Q-P |
| 9 Engineering / EOD | Q-L (E1), E2, Q-M |

The first four (explainability, CBRN, EW, persistence) are the **validation
holes** - highest priority, because they ground concepts the model already
claims. The rest extend into domains the library has not yet seen.
