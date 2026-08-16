# Drone-Warfare Walk: LIRC baseline, 2024 update, OPFOR targeting

These three scenarios came from the SME-directed drone-warfare thread of the
scenario-sourcing session
(`LLMExperiments/PaperSummaries/V2Extractions/`): the Morris 2018 Light
Infantry-Robotic Company (LIRC) baseline, its 2022-2024 threat/TTP update, and the
Rosenberg JPMRC-AK 24-02 OPFOR commercial-sUAS targeting run. They were contributed
by an SME who designated Morris as a drone-warfare **baseline** and pointed to four
Infantry Magazine articles (2023-2024) for updating the threat and U.S. TTP. This
walk instantiates the messages they imply and reconciles the findings with the
existing log.

Why these matter to the review: the earlier Fire Support walk surfaced **W1** (no
link between autonomy level and engagement authority) as the single most central
ASX gap and left it open as decision **Q-K**. The LIRC baseline is the richest
real-world instantiation of W1 in the whole library - it carries a fully worked
doctrinal control mechanism for autonomous lethal authority (weapons-control status
x geographic kill box x civilian-clearance x time window x target type x
human-in-the-loop). That mechanism is a concrete candidate answer to Q-K, not just
another instance of the gap.

Layout mirrors the workbook columns:
`Model | C2SIM Object | Parent Type | Field | Type | Value | Notes`.
**[Q]** = open question, **[!]** = not-yet-defined item / gap, **[+]** = corroborates
a prior finding. Proposals for the group; nothing here is applied to the OWL model.
The message instances are applied to the diff-able `.xml` workbooks (decision S4).

Grounding recap (checked against C2SIM / SMX / LOX and ASX v0.0.1 before writing):
- Exists / reused: `lox#ENGAGE`, `lox#ATTACK`, `lox#DETECT`, `lox#JAM`, `lox#AIRDEF`
  (TaskActionCode individuals); `lox#RuleOfEngagement`, `lox#WeaponRuleOfEngagementCode`,
  `hasRuleOfEngagement`; `DesiredEffectCode`; `hasAffectedEntity`; `AuthorizationHeader`
  (C2SIM, message-sender auth only - see W1); `TacticalArea` / `MapGraphic`;
  autonomy individuals {Automated, FullAuto, ReCont, Teleop} (ASX v0.0.1).
- Absent (grep of all three ontologies returned nothing): any weapons-control-status
  (hold/tight/free); any kill box / free-fire area / no-fire area / fire-support
  coordination measure; any loiter / loitering-munition / munition class; any
  target-list / high-value-target / high-payoff-target construct; any counter-UAS
  coupling. So the engagement machinery exists; the authority-gating and the
  weapon/target typing do not.

---

## A. LIRC baseline (Morris 2018) - land, combined-arms MUM-T movement to contact

A company of ~169 soldiers and ~25 UGVs plus UAS clears from PL LD to PL LOA.
Autonomous ground-attack weapons run weapons-hold (human-in-the-loop) during movement,
shift to weapons-tight before the line of departure, and may engage human targets
only inside a geographically and temporally bounded kill box confirmed clear of
civilians. This is the authority mechanism the Fire Support walk said was missing.

### LIRC Company Init  (tab: "LIRC Company Init")
| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| ASX | armed combat UGV | Robot / Platform | hasEntityType | EntityType | Armed-UGV | [+] P1: same Robot-vs-Platform double-typing as every other platform. |
| ASX | (armed UGV) | ? | autonomy level | AutonomyLevelCode | FullAuto / Teleop | [+] D1/P6: which autonomy vocabulary; here it must also bind to engagement authority (W1). |
| ASX | weapon (30mm, Javelin, Stinger) | Equipment / Payload | (armament) | ??? | gun / ATGM / SAM | [+/!] W2: weapon/munition not typed; a single UGV carries gun + antitank + air-defense weapons. |
| ASX | autonomous attack UAS | Robot / Platform | hasEntityType | EntityType | Loitering-munition (Switchblade-class) | [!] G16: a loitering munition is a platform AND a munition (flies, senses, then is expended) - neither Robot/Platform typing nor the absent munition class captures the hybrid. |
| C2SIM | kill box 1/2/3 | TacticalArea / MapGraphic | (engagement-authorization area) | ??? | geo bound + time window + civilian-clear + weapons-status | [!] G14: no weapons-control-status and no kill-box/authorization-area construct - the core of the LIRC concept has no home. Unifies N1 (area as subject) + W1 (engagement authority). |
| ASX | weapons-control status | ? | hold / tight / free | ??? | Hold (at movement) | [!] G14: hold/tight/free is absent from the ontology (grep: none). |

### LIRC Kill-Box Engagement Order  (tab: "LIRC Kill-Box Engagement Order")
| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| C2SIM | OrderBody | DomainMessageBody | isToReceiver | UUIDBase | (autonomous attack UAS / armed UGV) | |
| C2SIM | Message | - | hasAuthorizationHeader | AuthorizationHeader | (issuer credentials) | [+] W1: message-sender auth only - NOT the commander's authorization to open the kill box. |
| C2SIM / ASX | Engage Task | Task | hasTask | TaskActionCode | ENGAGE / ATTACK | Works - `lox#ENGAGE` / `lox#ATTACK` exist. |
| C2SIM | (task) | Task | hasAffectedEntity | UUIDBase | (enemy vehicle) | Materiel target via hasAffectedEntity - works. |
| C2SIM | (task) | Task | hasDesiredEffectCode | DesiredEffectCode | Destroy / Suppress | Works. |
| LOX | (task) | Task | hasRuleOfEngagement | RuleOfEngagement | (ROE) | Works - ROE exists. |
| ASX | (kill box) | ??? | engagement authority = f(autonomy, area, time, civilian-clear) | ??? | autonomous engagement of humans ONLY inside a confirmed-clear kill box | [!] G14 (HIGH): the concrete answer to W1/Q-K. Authority is gated by weapons-control status + a bounded area + a civilian-clearance state + a time window + target type. None modeled. |
| ASX | (weapons-control transition) | ? | hold -> tight -> free by phase | ??? | Hold (move) -> Tight (pre-LD) -> humans only in kill box | [!] G15: engagement authority varies by mission PHASE - a graded/temporal authority, sharpening D1/Q-D. |
| C2SIM | (kill box) | TacticalArea | (civilian-clearance state) | ??? | zero civilians confirmed | [+] N1/Q-M: area needs a state (clear/denied) to carry authority; extends "area as subject". |
| ASX | (target discrimination) | ? | thermal/shape recognition; decoy risk | ??? | military-vs-civilian vehicle; ~50% defeated by decoys | [+] G8/Q-S: decoy vehicles defeat discrimination - a decoy/deception residual. |

### LIRC Strike BDA Report  (tab: "LIRC Strike BDA Report")
| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| C2SIM | ReportBody | DomainMessageBody | hasReportContent | ??? | (battle damage assessment) | [+] W3: no effect-achieved / BDA ReportContent; `TaskStatus` says the task ran, not that the MBT was destroyed. |
| SMX | ObservationReportContent | ReportContent | hasObservation | Observation | (post-strike: 1 ADA veh, 1 arty, 2 IFV destroyed; 12 casualties KB1) | Partial - scene observable; "effect achieved" has no home. |
| ASX | (own attrition) | ? | systems lost to countermeasures | ??? | ~50% of autonomous systems failed | [+] G7: measure-of-effectiveness / attrition attribute (also the ~7-day drone life, ~10% mission completion from the 2024 update). |

## B. 2024 threat/TTP update - counter-UAS, EW/GPS denial, loitering munitions

The update (Wilkins 2023, Rosenberg 2024, Hamilton & Egan 2023, Padalino 2024) adds
a dense small-UAS/loitering-munition/FPV threat, adversary EW that denies GPS and can
hijack a drone, and organic squad counter-UAS. See
`LLMExperiments/PaperSummaries/V2Extractions/LIRC_MovementToContact_Updated2024.md`.

### Counter-UAS Defeat Order  (tab: "Counter-UAS Defeat Order")
| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| C2SIM | OrderBody | DomainMessageBody | isToReceiver | UUIDBase | (squad counter-UAS team) | |
| C2SIM / ASX | Detect Task | Task | hasTask | TaskActionCode | DETECT | Works - `lox#DETECT` exists (cue the counter-UAS engagement). |
| C2SIM / ASX | Defeat Task | Task | hasTask | TaskActionCode | AIRDEF / ENGAGE / JAM | [+] G17: mostly REUSE - `lox#AIRDEF`, `lox#ENGAGE`, `lox#ATTACK`, `lox#JAM` exist; residual is (a) soft-kill (JAM) vs hard-kill (ENGAGE) choice and (b) the detect->defeat coupling. |
| ASX | hostile sUAS | ? | target class | ??? | FPV drone / quadcopter | [!] G17: sUAS/UAS as a TARGET class is absent; `hasAffectedEntity` carries a UUID but there is no small-UAS target type. |
| ASX | (own UAS) | ? | EW vulnerability / countermeasure | ??? | GPS-denied; control-link jam; hijack in ~25 s | [!] G18: adversary EW that denies GPS or SEIZES a friendly drone extends G1/Q-O from "my comms degraded" to "adversary defeating/hijacking my autonomy"; needs a vulnerability + countermeasure (INS fallback, encrypted FH / fiber-optic link). |

### Loitering-munition typing (Init-side; folds into "LIRC Company Init")
| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| ASX | loitering munition | Robot/Platform + Payload | tier | ??? | mini / tactical / long-range | [!] G16: platform-munition hybrid; tiers (man-packable vs vehicle-launched vs strategic) have no typing. Extends P1/G5 (platform) + W2/Q-L (munition). |
| ASX | FPV attack drone | Robot / Platform | autonomy | AutonomyLevelCode | RemoteControl / FPV | [+] D1/P6: the "FPV" autonomy value (ConceptMapping NavigationAutonomy) shows up concretely; cheap expendable strike. |

## C. OPFOR targeting (Rosenberg 2024) - RED reconnaissance-strike cycle

3-509 PIR as OPFOR flew COTS drones (DJI Phantom 4 Pro, Mavic Air 2, TSTORM) to cue
indirect fires onto the rotational unit's high-payoff targets (TOC, BSA, Role 2,
artillery, counter-battery radars). First RED-perspective and first sensor-to-shooter
targeting thread. See
`LLMExperiments/PaperSummaries/V2Extractions/OPFOR_CommercialSUAS_Targeting_Rosenberg2024.md`.

### OPFOR Targeting Handoff Order  (tab: "OPFOR Targeting Handoff")
| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| C2SIM | OrderBody | DomainMessageBody | isFromSender / isToReceiver | UUIDBase | (drone operator -> S2 -> fires cell) | [+] X1/G3: sensor-to-shooter handoff; a sensor cues a shooter via a shared target. |
| ASX | COTS quadcopter | Robot / Platform | hasEntityType | EntityType | DJI Phantom 4 Pro (COTS, low autonomy) | [+] P1/D1: COTS commercial platform, RemoteControl autonomy. |
| ASX | validated target | ??? | shared track/contact | ??? | 10-digit grid + HPT type | [!] G3/G19: no track/contact object to carry a validated target from sensor to shooter (reuses M1 inline def). |
| ASX | HPT list / target board | ??? | target nomination + priority | ??? | "at least one of everything on the HVT list" | [!] G19: no high-value/high-payoff target-list or prioritization construct (grep: absent). A C2 targeting object distinct from a single `hasAffectedEntity`. |
| SMX | (drone on station) | - | persistent observation through strike | - | observe -> BDA -> adjust fire | [+] N2: persistence - the observer stays on station through the strike to adjust; corroborates persistent tasking. |
| ASX | (rotational unit) | ? | survivability / signature | ??? | disperse; displace ~24h; terrain-tied camo; overhead cover | [!] G11/Q-T + G12/Q-U: signature-management + dispersion/displacement behavior as a constraint - environment/geometry attributes touch it but there is no survivability-posture construct. |

---

## Reconciliation with prior findings

**Corroborated (independent confirmation from the drone-warfare thread):**
- **W1/Q-K** (engagement authority) <- LIRC kill-box mechanism - the strongest instance
  in the library, and it supplies a concrete doctrinal model to answer the decision.
- **W2/Q-L** (weapon/munition typing) <- LIRC mixed armament + loitering munitions.
- **W3** (BDA ReportContent) <- LIRC strike BDA + OPFOR BDA/adjust.
- **N1/Q-M** (area as subject) <- kill box as an authorization-bearing, civilian-clearance-stated area.
- **G3/Q-P** (cross-cueing + shared track) <- OPFOR sensor-to-shooter handoff.
- **N2** (persistence) <- OPFOR drone-on-station through the strike.
- **G7** (MoE) <- ~50% attrition (Morris), ~7-day drone life / ~10% completion (2024 update).
- **G8/Q-S** (decoy) <- Morris decoy vehicles defeat discrimination; 2024 sensor-fusion counter.
- **G1/Q-O** (denied comms) <- GPS-denied operation, extended by G18 (adversary seizes autonomy).
- **G11/Q-T** (environment conditions) and **D1/Q-D** (graded autonomy) <- GPS-denied env; phase-varying authority.
- **P1** (platform typing) <- new platform types (armed UGV, loitering munition, FPV, COTS quadcopter).

**New findings this batch adds:**

| ID | Sev | One-line |
|---|---|---|
| G14 | HIGH | Weapons-control-status + kill-box construct: an authorization-bearing area (weapons-control status x geo bound x time window x civilian-clearance state x target type) that gates autonomous lethal engagement - a concrete model that ANSWERS W1/Q-K and unifies it with N1/Q-M. Absent from all three ontologies. |
| G15 | MED | Graded, phase-varying engagement authority (weapons hold during movement -> tight before LD -> autonomous-in-kill-box) - authority is temporal/graded, sharpening D1/Q-D. |
| G16 | MED | Loitering munition / FPV as a platform-munition hybrid (flies, senses, then is expended), with size tiers (mini/tactical/long-range) - extends P1/G5 (platform) and W2/Q-L (munition); neither captures the hybrid. |
| G17 | MED | Counter-UAS engagement - mostly REUSE (`AIRDEF`/`ENGAGE`/`ATTACK`/`DETECT`/`JAM` exist); residual is an sUAS target class and the detect->defeat + soft-kill/hard-kill coupling. |
| G18 | MED | Adversarial EW against own autonomy - GPS-denial, control-link jamming, and drone-hijack are threats TO friendly autonomy; extends G1/Q-O with a vulnerability + countermeasure (INS fallback, encrypted FH / fiber-optic). |
| G19 | MED | Targeting construct - a high-value/high-payoff target LIST + nomination/prioritization (targeting board) and the sensor-to-shooter cue->validate->grid->fire->BDA->adjust cycle; the list/priority object is net-new (the cross-cue part is G3). |

New decisions for section 7:
- **Q-W [deck]** Model a **weapons-control-status + engagement-authorization area** (kill
  box): an area carrying a weapons-control status (hold/tight/free), a civilian-clearance
  state, a time window, and permitted target types, that gates whether an autonomous
  system may engage inside it. Unifies Q-K (engagement authority) and Q-M (area as
  subject) and gives both a concrete, doctrine-grounded shape. (Resolves G14; sharpens
  Q-K/Q-M; relates to Q-D graded autonomy via G15.)
- **Q-X** Type **loitering munitions / FPV** as a platform-munition hybrid with size
  tiers, and add **counter-UAS** as a detect->defeat coupling over the existing
  air-defense verbs with an sUAS target class. (Resolves G16/G17; extends Q-L/Q-R.)

## Headline

The drone-warfare thread lands squarely on the review's most central open finding.
Fire Support surfaced **W1** (autonomy-to-engagement-authority) and left it as decision
**Q-K** with no proposed element. The LIRC baseline supplies exactly that element from
real doctrine: a **weapons-control-status + kill-box** mechanism (G14) in which lethal
autonomous authority is granted only inside a bounded, time-limited, civilian-cleared
area and varies by mission phase (G15). That single construct also unifies W1/Q-K with
N1/Q-M (an area that bears authorization and a clearance state). The 2024 update and the
OPFOR run add the modern edges - loitering-munition/FPV typing (G16), counter-UAS as
mostly-reuse (G17), adversarial EW that seizes your own autonomy (G18), and a
target-list/sensor-to-shooter targeting construct (G19) - and independently corroborate
W2, W3, N1, N2, G3, G7, G8, and the graded-autonomy reading. Net: one HIGH-value
proposed answer (kill box = Q-W) to the standard's hardest ASX question, plus five
supporting typing/behavior gaps.
