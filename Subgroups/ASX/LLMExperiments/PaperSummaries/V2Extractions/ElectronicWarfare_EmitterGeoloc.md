# Scenario extracted from report (v2.2 prompt)

Primary: "Geolocation of RF Emitters Using a Low-Cost UAV-Based Approach", Air
Force Institute of Technology (AFIT) thesis, DTIC AD1054177 (open access, read in
full). Electronic-attack complement: Mears, "Cooperative Electronic Attack using
Unmanned Air Vehicles", AFRL, DTIC ADA444985 (open access).

This replaces the earlier composed EW placeholder with a real extraction from a
primary open-access experiment (the AD1054177 flight test), with the cooperative-
electronic-attack side grounded from ADA444985.

Sourced against `InstantiationReview/Documents-Needed.md` request #3 (EW sensing /
attack). Grounds Q-Q (Y4 emitter/signal observation, Y5 frequency/bearing reading;
geolocation confidence), effect-vs-ROE, generic detection.

### Scenario 1: UAV geolocation of a ground RF emitter (electronic support), with cooperative electronic attack

**Domain / mission type:** air; electronic warfare - RF emitter geolocation (electronic support), with a cooperative electronic-attack extension.

**Source location:** AD1054177 Ch. 3 (UAV Flight Test Methodology) and Ch. 4 (Flight Test Results); ADA444985 (cooperative EA concept).

**Purpose (why the authors present it):** To develop and flight-test a low-cost
(< $1000) UAV payload that geolocates a ground RF emitter, and to characterize its
accuracy. (Research/experiment intent.) The EA complement formulates coordinated
UAV suppression of networked enemy air defenses.

**Summary narrative:** A fixed-wing UAV (Sig Rascal 110) carrying a low-cost
radio-direction-finding payload flies programmed approach patterns - circular
loiter orbits and button-hook patterns - overhead, near, and far from a hidden
ground RF emitter, at low and high altitude. At each measurement point the UAV
records a received-signal-strength / line-of-bearing reading together with its GPS
position, and fuses the readings to estimate the emitter's location with 50% and
95% confidence error ellipses that tighten as the flight progresses. Ground
testing located the emitter to within 20 meters; the five real-world test flights
gave poor accuracy (errors up to about 98 meters), showing the estimate's
sensitivity to sensor uncertainty, antenna orientation, and altitude. In the
electronic-attack extension, multiple UAVs coordinate their flight paths to deliver
non-destructive suppression of a network of enemy air-defense radars.

**In-world objectives:**
- Detect and geolocate a hostile ground RF emitter from a UAV, at low cost.
- (Electronic attack) Suppress networked enemy air-defense radars with coordinated UAVs.

**Autonomous systems employed:**
- Sig Rascal 110 fixed-wing UAV (UAV) with an RF direction-finding payload (dipole/bow-tie antenna, receiver, GPS). Autonomy: flies programmed loiter/button-hook patterns; onboard/ground geolocation processing.
- (EA context) Multiple coordinated UAVs - cooperative path planning for electronic attack against a radar network.

**Measures of Performance:**
- Geolocation error (distance from the true emitter), with 50% / 95% confidence ellipses.
- Estimate convergence over the flight (error reduction over time).
- Ground-test accuracy (~20 m) vs flight-test accuracy (up to ~98 m error).

**Scenario steps:**
1. A ground RF emitter (transmitter) is emplaced at an unknown location.
2. The UAV flies a programmed approach pattern (circular loiter orbit, e.g. ~550 m standoff / set orbit radius, or a button-hook), at a set altitude.
3. At each measurement point the UAV records a signal reading (RSS / line-of-bearing) and its own GPS position/time.
4. The system fuses the readings -> estimates the emitter location with 50%/95% confidence error ellipses, refining as more measurements accumulate.
5. The estimated emitter location and confidence are reported.
6. (Electronic attack) Multiple UAVs coordinate positions/paths to suppress the networked radar emitters (subject to ROE).

**Environment and constraints:** Open-air RF test range (flight tests) plus
simulation of sensor-uncertainty and approach-path cases. Execution context:
field-experiment (five real-world test flights) and constructive simulation.
Rules of engagement: electronic attack governed by ROE (EA extension). Constraints:
accuracy is sensitive to sensor uncertainty (tested to +/-10 deg), antenna
orientation, and altitude; the UAV must fly sufficiently close to the emitter.

#### Conceptual model (ontology seed)
- **Domain and scope:** UAV electronic support (emitter geolocation) and cooperative electronic attack against RF emitters.
- **Concepts (classes):** ES-UAV, RF emitter, Emitter observation, Line-of-bearing, Geolocation estimate, Confidence ellipse, Approach pattern, Electronic attack, Radar network.
- **Taxonomy (IS-A):**
  - Autonomous system -> UAV -> Fixed-wing ES-UAV
  - RF emitter -> Radar emitter, Communications emitter
  - EW action -> Electronic support (geolocate), Electronic attack (suppress)
  - Approach pattern -> Loiter orbit, Button-hook
- **Relationships (triples):**
  - ES-UAV | measures | Emitter observation (RSS / line-of-bearing)
  - ES-UAV | flies | Approach pattern
  - ES-UAV | estimates | Geolocation of RF emitter
  - Geolocation estimate | has | Confidence ellipse (50% / 95%)
  - Coordinated UAVs | suppress | Radar network (subject to ROE)
- **Properties:**
  - Emitter observation: signal strength (RSS), line-of-bearing, frequency, UAV position/time
  - Geolocation estimate: location, error, 50%/95% confidence ellipse, convergence
  - ES-UAV: DF antenna type, receiver, GPS, approach pattern, altitude
  - RF emitter: type (radar/comms), true location, network membership
- **Constraints/rules:**
  - Geolocation accuracy depends on sensor uncertainty, antenna orientation, altitude, and standoff.
  - Electronic attack is governed by rules of engagement.
  - Cooperative EA requires coordinated multi-UAV path planning against a networked target.

**Grounding check:** ES/geolocation scenario fully grounded in AD1054177 (including
the honest negative flight-test result); the electronic-attack extension grounded
in ADA444985. ROE for EA [inferred from the SEAD framing]. No composed/synthetic
content remains.
