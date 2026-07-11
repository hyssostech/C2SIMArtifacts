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
- `AuthorizationHeader` (C2SIM) exists, but its comment scopes it to
  **message-sender authentication** (HTTP Basic/Bearer/Digest style) - it is
  **not** command authorization identifying which commander approved the fires.
  So who-approved-the-engagement is **not** modeled.
- `DesiredEffectCode` **exists** and is already used in the UAV/UGV order sheets.
- `hasAffectedEntity` (order sheets) can carry the **target** reference.
- `lox#ENGAGE` and `lox#ATTACK` **exist** as `TaskActionCode` individuals
  (LOX has 446), so the engage/attack verb is available via `hasTask`.
- **Not found:** any weapon/munition class, any target class, any battle-damage /
  effect-achieved report content, and any construct recording the authorizing
  commander of an engagement.

So the ROE constraint exists; command authorization of an engagement does not.
The real question is autonomy-specific.

## 1. Fire Support Order (engagement)

An armed UGV is tasked to engage a target with rules of engagement.

| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| C2SIM | OrderBody | DomainMessageBody | isToReceiver | UUIDBase | (armed UGV UUID) | |
| C2SIM | Message | - | hasAuthorizationHeader | AuthorizationHeader | (sender credentials) | [!] message-sender authentication (Basic/Bearer/Digest) - NOT command authorization of the engagement. |
| C2SIM / ASX | Engage Task | Task | hasTask | TaskActionCode | Engage / Attack | Works - `lox#ENGAGE` and `lox#ATTACK` exist as TaskActionCode individuals. |
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
| W1 | HIGH | **gap** | No link between autonomy level and engagement authority - the standard cannot say whether a FullAuto system may take a lethal action without human approval. ROE exists but does not cover this, and there is no construct recording the authorizing commander of the engagement. |
| W2 | MED | gap | Weapon/munition not typed (Payload Armiture/Ammunition in ConceptMapping; absent from OWL). |
| W3 | MED | gap | No effect-achieved / battle-damage-assessment ReportContent; TaskStatus reports task state, not effect on target. |

Partially covered (checked, NOT gaps): rules of engagement
(`RuleOfEngagement`, `WeaponRuleOfEngagementCode` - LOX), the engage/attack verb
(`lox#ENGAGE` / `lox#ATTACK`), desired effect (`DesiredEffectCode`), and target
designation (`hasAffectedEntity`). Note: `AuthorizationHeader` is message-sender
authentication, not command authorization of fires - so who-approved-the-
engagement is part of the W1 gap, not covered.

## Headline

Fire Support surfaces the finding most central to autonomous systems and least
touched by the rest of the standard: **W1, autonomous engagement authority.**
The standard can already express *what* effect is desired and *which* ROE
applies - but it has no way to state *who* (which commander) authorized the
engagement, nor whether an autonomous system at a given autonomy level is
permitted to execute a lethal action without a human in/on the loop. That link
between autonomy level and
engagement permission is a first-class ASX concern with no proposed element.
(W2 weapon typing and W3 BDA are ordinary coverage gaps by comparison.)
