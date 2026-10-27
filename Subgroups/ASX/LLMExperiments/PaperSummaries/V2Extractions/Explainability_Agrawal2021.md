# Scenario extracted from report (v2.2 prompt)

Agrawal, A., Cleland-Huang, J., et al. (2021). Explaining Autonomous Decisions in
Swarms of Human-on-the-Loop Small Unmanned Aerial Systems. arXiv:2109.02077.
Source read in full (arXiv PDF).

Sourced to fill ASX validation hole #1 (explainability / human-on-the-loop) from
`InstantiationReview/Documents-Needed.md`. Grounds decisions Q-H, Q-K (W1), Q-D.

### Scenario 1: Human-on-the-loop multi-sUAS search with explained autonomy (DroneResponse)

**Domain / mission type:** air; human-on-the-loop multi-sUAS search-and-rescue with explainable autonomous decisions.

**Source location:** Sections "DroneResponse: Multi-sUAS Search", "sUAS Autonomy", "Prototype Design"; scenarios V1-V5.

**Purpose (why the authors present it):** To study how a human-on-the-loop
operator is best given explanations of autonomous sUAS decisions (UI-design study
of situational awareness and automation bias). (Research intent.)

**Summary narrative:** Four autonomous small UAS conduct a coordinated aerial
search for a victim under a single human-on-the-loop operator, using the
DroneResponse platform. Each sUAS senses its environment (camera, GPS, LiDAR) and
autonomously adjusts its behavior in response to recognized events; when it does,
it pushes an explanation to the operator's interface stating the event that
occurred, the action taken, the reasoning ("why"), any operational/flight-mode
change, and the sUAS's confidence in its AI-driven decision. The operator keeps
situational awareness and can configure, suspend, acknowledge, or override the
autonomous behavior. The study deliberately injects wrong perceptions (e.g. an
sUAS mistakes a ball for a person and begins tracking it) to test whether the
operator can detect and correct them.

**In-world objectives:**
- Locate a victim through coordinated autonomous aerial search.
- Keep the on-the-loop operator's situational awareness sufficient to intervene before a wrong autonomous action has consequences.

**Autonomous systems employed:**
- Small UAS x4 (UAV) - autonomous flight and perception (weather-recognition CV, person detection via YOLO); each explains its own decisions. Level of autonomy: human-on-the-loop (acts autonomously; human supervises and can override).

**Measures of Performance:**
- Operator situational awareness while supervising multiple sUAS.
- Automation bias (operator accepting wrong autonomous decisions uncritically).
- Correct operator interpretation of pushed explanations.
- [inferred] Search success (victim located) - the mission goal, not the study's measured variable.

**Scenario steps (the autonomy + explanation loop):**
1. The sUAS execute an assigned area search.
2. An sUAS's onboard CV recognizes an event: adverse weather (mist/rain), a detected person, low battery / signal loss, or a no-fly zone / obstacle.
3. The sUAS autonomously adjusts behavior: fly lower and slower (weather); switch from search to tracking (person detected with sufficient confidence); return-to-launch or land at the nearest pad (battery/signal); replan a path, or request human assistance if no viable path exists.
4. The sUAS pushes an explanation to the operator UI, co-located with its icon: {event, action taken, reasoning/why, operational change, confidence}.
5. The operator maintains situational awareness and may configure, suspend, acknowledge, or override the autonomous behavior.
6. On a wrong perception (e.g. a ball tracked as a person), the operator detects it from the explanation plus the video stream and overrides.

**Environment and constraints:** Aerial search-and-rescue (ice/river/fire
surveillance domains referenced); time-constrained; intermittent connectivity;
explanations are pushed automatically (not requested on demand). Execution
context: mixed - simulated sUAS in Gazebo and physical sUAS; identical UI for
both. Rules of engagement: Not applicable (SAR, no adversary).

#### Conceptual model (ontology seed)
- **Domain and scope:** Explaining autonomous sUAS decisions to a human-on-the-loop supervisor during multi-UAV aerial search.
- **Concepts (classes):** sUAS, Human-on-the-loop operator, Autonomous event, Autonomous action, Explanation, Confidence, Flight-mode change, Override.
- **Taxonomy (IS-A):**
  - Autonomous system -> UAV -> sUAS
  - Autonomous event -> Weather event, Person-detected event, Low-battery/Signal-loss event, Path-obstruction event
  - Autonomous action -> Adjust flight, Switch to tracking, Return-to-launch, Replan / Request assistance
- **Relationships (triples):**
  - sUAS | detects | Autonomous event
  - Autonomous event | triggers | Autonomous action
  - sUAS | emits | Explanation of action
  - Explanation | states | reasoning and confidence
  - Operator | supervises | sUAS
  - Operator | overrides / suspends / acknowledges | Autonomous action
- **Properties:**
  - Explanation: event, action, reasoning, operational change, confidence
  - sUAS: level of autonomy (on-the-loop), sensors (camera/GPS/LiDAR), CV models
  - Operator: situational awareness, intervention options
- **Constraints/rules:**
  - Explanations are pushed automatically when an event occurs.
  - Return-to-launch is a fail-safe on low battery/signal, overridable to land at the nearest pad.
  - An sUAS requests human assistance if it cannot find a viable path.
  - Manual override is always available to the on-the-loop operator.

**Grounding check:** Search-success MoP is [inferred]; ROE "Not applicable". All other fields grounded in source.
