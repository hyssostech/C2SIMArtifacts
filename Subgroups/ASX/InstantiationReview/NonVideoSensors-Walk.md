# Non-Video Sensor Report Walk (proposed coverage)

Purpose: stress-test the sensor half of the proposed ASX model. The one worked
Report example (`Video Detection Report`) models sensor output as a
`SensorObservation` carrying a `MediaReference` (a video file) plus a
`MediaTypeEnum`. That works for cameras. This walk instantiates reports for
**non-video** sensors - CBRN, EW, and ground-penetrating radar - to see whether
that model generalizes. It does not.

Layout mirrors the workbook columns:
`Model | C2SIM Object | Parent Type | Field | Type | Value | Notes`.
**[Q]** = open question, **[!]** = not-yet-defined item / gap. Anchored to the ontology.

Grounding done first (to avoid inventing gaps):
- `Observation` subtypes are exactly {Activity, Health, Location, Name,
  Resource, SubjectType}Observation - **no measurement / detection / hazard**
  subtype.
- There are **no** CBRN / chemical / radiological / emitter / signal / radar /
  thermal / mine **sensor or observation** classes anywhere in C2SIM, SMX, or
  LOX. (What does exist nearby: `smx#NBC_Event` - an APP6-C tactical-graphics
  *symbol* class, not an observation - and LOX *task* verbs for chemical /
  biological / nuclear sampling; both are reuse candidates but neither carries
  a sensor reading.)
- The only measure-like datatype properties are logistics quantities,
  `hasSpatialMeasure`, `hasCoordinateValue`, and `smx#hasConfidenceLevel` - **no**
  generic sensor-reading value+unit.
- `JAM` exists but as a `TaskActionCode` (LOX) - the jamming *action*, not EW
  *sensing*.
- Proposed enums: `SensorType` (ConceptMapping) = {Visual, EW, Counter EW,
  Audio}; `MediaTypeEnum` (Video Detection Report) = {Video, Audio, Image,
  Document, NOS}.

## 1. CBRN Detection Report

A chemical sensor detects an agent at a location with a concentration reading.

| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| C2SIM | ReportBody | DomainMessageBody | hasReportContent | ObservationReportContent | (CBRN detection) | |
| SMX | LocationObservation | Observation | hasLocation | Location | (contamination location) | Works - where is expressible. |
| ??? | (agent detection) | Observation? | detected agent | ??? | Chemical agent (e.g. GB) | [!] Y3: no hazard/detection Observation subtype fits (only Activity/Health/Location/Name/Resource/SubjectType). |
| ASX? | (reading) | ? | concentration | value + unit | 5 mg/m3 | [!] Y5: no sensor-reading value+unit property exists. |
| ASX | (sensor) | ? | SensorType | enum | CBRN-Chemical | [!] Y2: SensorType enum has no CBRN / radiological / nuclear / biological. |
| ASX | SensorObservation | ActivityObservation | media | MediaReference | (none) | [!] Y1: the media-based model does not apply - a CBRN reading is not a media file; MediaTypeEnum {Video/Audio/Image/Document/NOS} cannot represent a measurement. |

## 2. EW Emitter Report

An EW sensor intercepts and locates a hostile radio emitter.

| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| C2SIM | ReportBody | DomainMessageBody | hasReportContent | ObservationReportContent | (emitter intercept) | |
| SMX | LocationObservation | Observation | hasLocation | Location | (emitter bearing/location) | Works - direction-finding location. |
| ??? | (emitter/signal) | Observation? | detected emitter | ??? | Hostile radio, 243.0 MHz | [!] Y3/Y4: no emitter/signal observation type; `JAM` is a LOX TaskActionCode (the action), not a sensing report. |
| ASX? | (reading) | ? | frequency / bandwidth | value + unit | 243.0 MHz / 25 kHz | [!] Y5: no measurement value+unit property. |
| ASX | (sensor) | ? | SensorType | enum | EW | SensorType has EW - the *sensor* is typable; the *observation* of an intercept is not. |

## 3. GPR Mine Detection Report

Ground-penetrating radar detects a buried mine during route clearance.

| Model | C2SIM Object | Parent Type | Field | Type | Value | Notes |
|---|---|---|---|---|---|---|
| C2SIM | ReportBody | DomainMessageBody | hasReportContent | ObservationReportContent | (mine detection) | |
| SMX | LocationObservation | Observation | hasLocation | Location | (mine location) | Works. |
| SMX | SubjectTypeObservation | Observation | observed type | SubjectType | Mine / IED | Partial - identity is expressible IF a Mine/IED entity type exists (ties to X4). |
| SMX | SubjectTypeObservation | Observation | hasConfidenceLevel | double | 0.85 | Works - confidence exists. |
| ASX? | (reading) | ? | depth / burial | value + unit | 0.3 m | [!] Y5: no measurement value+unit for subsurface depth. |
| ASX | (sensor) | ? | SensorType | enum | GPR / Radar | [!] Y2: SensorType enum has no GPR / radar / metal-detector. |

---

## Findings summary

| ID | Sev | True gap or covered? | One-line |
|---|---|---|---|
| Y1 | HIGH | **gap** | The Video Detection report model (`SensorObservation` + `MediaReference` + `MediaTypeEnum`) does not generalize - non-video sensors emit readings, not media files. |
| Y2 | MED | **gap** | `SensorType` enum {Visual, EW, CounterEW, Audio} omits CBRN, radiological, nuclear, biological, GPR/radar, thermal, LIDAR, metal-detector. |
| Y3 | HIGH | **gap** | No Observation subtype for a detected hazard/agent/emitter; existing six subtypes do not fit. |
| Y4 | MED | **gap** | EW *sensing* has no report content type (`JAM` is a LOX task = the action, not the observation). |
| Y5 | HIGH | **gap** | No generic sensor-reading value+unit property (concentration, dose rate, frequency, depth). Only logistics quantities and `hasConfidenceLevel` exist. |

What is **partially covered**: location (`LocationObservation`), identity of a
detected object (`SubjectTypeObservation`, if the object's entity type exists),
and confidence (`hasConfidenceLevel`). What is **not** covered: the sensor
reading itself, the sensor modality taxonomy, and any non-camera observation
subtype.

## Headline

The proposed report model was designed around a camera (media file + analyst
comment). The moment a non-imaging sensor is instantiated, the model has no
place for the measurement. **The core need is a sensor-reading / measurement
representation (value + unit + modality) that is independent of media**, plus a
completed sensor-type taxonomy. This generalizes M5 (MediaType conflates format
and modality) and D2 (three sensor models) from "inconsistent" to "does not
cover the domain."
