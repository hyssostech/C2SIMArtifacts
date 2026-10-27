# Redundancy Pass: Route Clearance, Companion Drones, Urban Combat

Purpose: before declaring these three scenarios redundant, confirm it and mine
them for anything new. Outcome: the redundancy call largely holds, but the pass
found one genuine new finding (N1 - area as the subject of a task/report) that
would have been lost by skipping the check.

Grounding done first:
- Areas are modeled: `TacticalArea`, `MapGraphic`, `Overlay`, `Boundary`.
- But the only "affected" property is `hasAffectedEntity` - there is **no**
  `hasAffectedArea`; and there is **no** area-state (cleared/contaminated).
- `RelativeLocation` and `CommunicationNetwork` **already exist** - so
  follow/escort/relay have building blocks.

## Per-scenario check

### Route Clearance & Neutralization (MUTT #6)
- Detect mine (GPR) -> already covered (Y-series, `GPR Mine Detection Report`).
- Neutralize mine -> engage an entity with an effect -> covered (W-series /
  Q-L "engage" verb; `DesiredEffectCode` exists).
- **Mark / clear the route** -> **N1**: declaring an *area* cleared, or tasking
  an effect on an *area*, has no home (only `hasAffectedEntity`; no area-state).

### Companion Drones (June deck)
- Follow / escort / station-keep -> a **task verb** (Q-L) whose payload is a
  `RelativeLocation` (exists). Persistent/continuous tasking (vs one-shot
  move-to-point) is the only nuance -> **N2**, folds into Q-L.
- Comms relay / repeater -> reuses `CommunicationNetwork` (exists) + a relay
  task verb (Q-L). Not new.

### Urban Combat Support (MUTT #10)
- Multi-role: fire support (W), recon (Y), transport (L), obstacle clearing (E)
  - all already walked.
- **Suppressive fire on an area** (not a point target) -> **N1** again: effect
  on an area, not an entity.
- GPS-denied / indoor 3D positioning -> a `Location`-representation question,
  likely outside ASX scope (noted, not pursued).

## Findings

| ID | Sev | Status | One-line |
|---|---|---|---|
| N1 | MED | **new gap** | Area as the subject of a task/report: `hasAffectedEntity` has no area counterpart, and there is no area-state (cleared/contaminated/mined). Areas exist (`TacticalArea`); tasking/reporting *on* them does not. Recurs in route-clearance, CBRN, urban. |
| N2 | LOW | folds into Q-L | Follow/escort/relay are task verbs (Q-L) over existing `RelativeLocation` / `CommunicationNetwork`; only the persistent-vs-one-shot task semantics is a nuance. |

Confirmed redundant (no new finding): neutralize = engage (W), detection = Y,
transport = L, clear = E, recon = Y, relay = CommunicationNetwork + verb.

## Verdict

The "redundant" call was ~80% right - these scenarios mostly recombine
already-found gaps. But the pass earned its keep: **N1 (area as subject)** is a
distinct, cross-cutting finding that none of the entity-centric walks surfaced,
and it would have been missed. N2 sharpens Q-L. New decision: Q-M (N1).
