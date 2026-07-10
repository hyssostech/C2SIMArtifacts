# Scenario extracted from report (v2.2 prompt)

Composed from open technical descriptions of UAV-based electronic-warfare support
and attack: multi-UAV time-difference-of-arrival emitter geolocation (e.g. "Emitter
Geolocation with Multiple UAVs", IEEE) and received-signal-strength UAV emitter
ranking for jamming prioritization.

Source-fidelity caveat: unlike the other records, no single open-access situated
EW mission vignette was retrievable (open EW sources are technique-level, and the
closest mission-shaped sources are paywalled). This record composes the reported
UAV emitter-geolocation-and-jamming workflow to give the ASX EW concepts a
grounding; it is the lowest-fidelity record in this batch and should be replaced
if a concrete open EW vignette or after-action report is obtained.

Sourced against `InstantiationReview/Documents-Needed.md` request #3 (EW sensing /
attack). Grounds Q-Q (Y4 emitter/signal observation, Y5 frequency/bandwidth
reading), effect-vs-ROE, generic detection.

### Scenario 1: UAV-network emitter geolocation and jamming prioritization

**Domain / mission type:** air; electronic warfare - emitter geolocation (electronic support) and jamming (electronic attack).

**Source location:** Composed from the cited UAV emitter-geolocation and jamming-prioritization technical descriptions.

**Purpose (why the authors present it):** To demonstrate UAV-based detection and
geolocation of hostile RF emitters and prioritized allocation of jamming.
(Technical/demo intent.)

**Summary narrative:** A small network of unmanned aerial vehicles, each carrying
an electronic-warfare support (ES) sensor, a GPS receiver, and a precision clock,
flies over an area to detect and geolocate hostile RF emitters (radar or
communications). Each UAV that hears an emitter records the signal parameters and
the time of arrival (or received signal strength) together with its own GPS
position; fusing these across the network via time-difference-of-arrival (or
RSS ranging) yields an estimated emitter location. The detected emitters are then
ranked and prioritized so that a jamming asset can allocate electronic-attack
energy against the highest-priority emitters, subject to rules of engagement.

**In-world objectives:**
- Detect, characterize, and geolocate hostile RF emitters.
- Prioritize emitters and deliver jamming (electronic attack) against the highest-priority ones.

**Autonomous systems employed:**
- ES-equipped UAVs, ~3-4 (UAV) - cooperative emitter detection and geolocation; each has an ES sensor, GPS, precision clock, and a limited-bandwidth datalink. Autonomy: [inferred] autonomous flight with cooperative geolocation.
- Jamming asset (platform not specified) - electronic attack against prioritized emitters. Autonomy: Not specified in source.

**Measures of Performance:**
- Emitter geolocation accuracy (position error).
- Number and priority of emitters detected/serviced.
- [inferred] Jamming effectiveness against the prioritized emitters.

**Scenario steps:**
1. The UAV network flies over the area of interest with ES sensors active.
2. Each UAV detects an emitter's signal -> records signal parameters (frequency, bandwidth), time-of-arrival or RSS, and its own GPS position/time.
3. The network fuses TDOA (or RSS) across UAVs -> estimates the emitter's geolocation.
4. Detected emitters are ranked and prioritized.
5. A jamming asset allocates electronic-attack energy against the top-priority emitters, subject to ROE.
6. [inferred] Effect is assessed and the emitter list updated.

**Environment and constraints:** Contested RF environment. Execution context:
[inferred] experiment/analysis (composed). Rules of engagement: electronic attack
governed by ROE. Platform/timing specifics: Not specified in source.

#### Conceptual model (ontology seed)
- **Domain and scope:** Cooperative UAV electronic-warfare support (emitter geolocation) and electronic attack (jamming) with prioritization.
- **Concepts (classes):** ES-UAV, RF emitter, Emitter observation, Geolocation estimate, Emitter priority, Jamming asset, Electronic attack.
- **Taxonomy (IS-A):**
  - Autonomous system -> UAV -> ES-UAV
  - RF emitter -> Radar emitter, Communications emitter
  - EW action -> Electronic support (geolocate), Electronic attack (jam)
- **Relationships (triples):**
  - ES-UAV | detects | RF emitter
  - ES-UAV | measures | Emitter observation (frequency, TOA/RSS, position)
  - UAV network | geolocates | RF emitter
  - Emitter | assigned | Priority
  - Jamming asset | jams | RF emitter (subject to ROE)
- **Properties:**
  - Emitter observation: frequency, bandwidth, time-of-arrival / RSS, bearing/geolocation, confidence
  - RF emitter: type (radar/comms), estimated location, priority
  - ES-UAV: ES sensor, GPS, precision clock, datalink
- **Constraints/rules:**
  - Geolocation requires multiple UAVs (TDOA/RSS across the network).
  - Electronic attack is governed by rules of engagement.

**Grounding check:** Source-fidelity caveat (composed, not a single situated
vignette); several fields [inferred] or "Not specified in source". Emitter-
observation and geolocation workflow grounded in the cited technical descriptions.
