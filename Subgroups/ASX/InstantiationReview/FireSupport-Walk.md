# Fire Support Message Walk (proposed coverage)

Purpose: instantiate an **armed** autonomous system engaging a target. This
exercises the task/effect axis - which the earlier walks (typing, sensing,
coordination) did not touch - and, most importantly, the question of
**autonomous engagement authority**: may an autonomous system take a lethal
action, and under what approval?

Layout mirrors the workbook columns:
`Model | C2SIM Object | Parent Type | Field | Type | Value | Notes`.
**[Q]** = open question, **[!]** = gap/defect. Anchored to the ontology. All
findings are proposals for the group; nothing here is applied to the model.

Grounding done first - and it narrowed the findings a lot:
- `RuleOfEngagement` and `WeaponRuleOfEngagementCode` / `MipWeaponUseROE`
  **already exist** (LOX), with `hasRuleOfEngagement` / `hasWeaponROECode`.
- `AuthorizationHeader` (C2SIM) with `hasAuthorizationCredentials` /
  `hasAuthorizationType` **already exists** - order authorization is modeled.
- `DesiredEffectCode` **exists** and is already used in the UAV/UGV order sheets.
- `hasAffectedEntity` (order sheets) can carry the **target** reference.
- **Not found:** any weapon/munition class, any target class, any
  battle-damage / effect-achieved report content, and any TaskActionCode
  individuals (could not enumerate the task verbs from RDF - see Q below).

So ROE and authorization are NOT gaps. The real question is autonomy-specific.

## 1. Fire Support Order (engagement)

An armed UGV is tasked to engage a target with rules of engagement.

| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| C2SIM | OrderBody | DomainMessageBody | isToReceiver | UUIDBase | (armed UGV UUID) | |
| C2SIM | Message | - | hasAuthorizationHeader | AuthorizationHeader | (issuer credentials) | Works - authorization is modeled (C2SIM). |
| C2SIM / ASX | Engage Task | Task | hasTask | TaskActionCode | Engage / Attack | [Q] confirm an engage/attack TaskActionCode value exists (could not enumerate from RDF). |
| C2SIM | (task) | Task | hasAffectedEntity | UUIDBase | (target UUID) | Target via hasAffectedEntity - partial (target is a plain entity ref). |
| C2SIM | (task) | Task | hasDesiredEffectCode | DesiredEffectCode | Destroy / Suppress | Works - DesiredEffectCode exists. |
| LOX | (task) | Task | hasRuleOfEngagement | RuleOfEngagement | (ROE) | Works - ROE exists (LOX). |
| LOX | (task) | - | hasWeaponROECode | WeaponRuleOfEngagementCode | (weapon ROE) | Works - weapon ROE exists (LOX). |
| ASX | (armed UGV) | ? | autonomy vs engagement | ??? | may engage without human approval? | [!] W1: nothing links the autonomy level (FullAuto / Teleop) to permission for a lethal action. ROE constrains WHAT/WHEN; it does not say whether the AUTONOMOUS system may pull the trigger unsupervised. |
| ASX | weapon / munition | Equipment / Payload | (armament) | ??? | machine gun / ATGM | [!] W2: weapon/munition not typed (ConceptMapping Payload = Armiture/Ammunition; absent from OWL). Ties to D3/P2. |

## 2. BDA Report (effect achieved)

The armed UGV reports the result of the engagement.

| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| C2SIM | ReportBody | DomainMessageBody | hasReportContent | ??? | (battle damage assessment) | [!] W3: no effect-achieved / battle-damage-assessment ReportContent. TaskStatus says the task ran; it does not say the target was destroyed. |
| SMX | ObservationReportContent | ReportContent | hasObservation | Observation | (post-strike observation) | Partial - the post-strike scene can be observed, but "desired effect achieved: yes/no" has no home. |
| C2SIM | TaskStatus | ReportContent | task outcome | TaskStatus | Complete | Reports task state, not effect on the target. |

---

## Findings summary

| ID | Sev | Status | One-line |
|---|---|---|---|
| W1 | HIGH | **gap** | No link between autonomy level and engagement authority - the standard cannot say whether a FullAuto system may take a lethal action without human approval. ROE/authorization exist but do not cover this. |
| W2 | MED | gap | Weapon/munition not typed (Payload Armiture/Ammunition in ConceptMapping; absent from OWL). |
| W3 | MED | gap | No effect-achieved / battle-damage-assessment ReportContent; TaskStatus reports task state, not effect on target. |

Partially covered (checked, NOT gaps): rules of engagement
(`RuleOfEngagement`, `WeaponRuleOfEngagementCode` - LOX), order authorization
(`AuthorizationHeader`, `hasAuthorizationCredentials`), desired effect
(`DesiredEffectCode`), and target designation (`hasAffectedEntity`).

## Headline

Fire Support surfaces the finding most central to autonomous systems and least
touched by the rest of the standard: **W1, autonomous engagement authority.**
The standard can already express *what* effect is desired, *which* ROE applies,
and *who* authorized the order - but it has no way to state whether an
autonomous system at a given autonomy level is permitted to execute a lethal
action without a human in/on the loop. That link between autonomy level and
engagement permission is a first-class ASX concern with no proposed element.
(W2 weapon typing and W3 BDA are ordinary coverage gaps by comparison.)
