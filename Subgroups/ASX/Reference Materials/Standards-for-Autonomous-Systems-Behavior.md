# Standards Relevant to Autonomous Systems Behavior for an ASX Ontology

A survey of external standards and formalisms that address autonomous
systems behavior - behavior trees, task-decomposition modeling,
cognitive agents, and related areas - that could be considered for
inclusion in, or alignment with, an ASX ontology.

The landscape is uneven. Formal ontology standards for autonomy exist
and are directly importable. Behavior trees and cognitive-agent
architectures are largely de facto: well formalized in the literature
but not ratified as standards. Each item below is grouped by how
directly it could feed an ASX ontology.

## 1. Formal ontology standards (most directly reusable)

These are the strongest candidates because they are already expressed as
axiomatized ontologies, so an ASX ontology can import or align to them
rather than reinvent the concepts.

- **IEEE 1872-2015 - CORA (Core Ontology for Robotics and Automation).**
  The foundational upper ontology for the domain, built on SUMO. This is
  the anchor that the other IEEE robotics ontologies extend.
- **IEEE 1872.1 - Robot Task Representation.** A standard ontology
  specifically for representing robot tasks - directly relevant if ASX
  needs to model tasking and mission decomposition formally.
- **IEEE 1872.2-2021 - Autonomous Robotics (AuR) Ontology.** Extends CORA
  to autonomous systems across aerial, ground, surface, underwater, and
  space domains; provides concepts and axioms for autonomous system
  architectures. Arguably the single most relevant external ontology for
  ASX.
- **IEEE 7007-2021 - Ontological Standard for Ethically Driven Robotics
  and Automation Systems.** Ontologies for ethics, transparency,
  responsibility, and accountability, expressed in Common Logic
  Interchange Format. Relevant to ASX's ethical-control concerns.

## 2. Behavior formalization and execution models

- **Behavior Trees.** No ratified ISO/OMG standard - a de facto standard
  with strong academic formalization (Colledanchise and Ogren's
  graph-theoretic and logic treatment; linear-temporal-logic and
  model-checking approaches; stateful-BT formalizations). Widely used in
  ROS 2 (Nav2, BehaviorTree.CPP) and the Boston Dynamics Spot SDK. For an
  ontology, model the BT concepts (composite/decorator/leaf nodes, tick
  semantics, success/running/failure states) rather than cite a standard.
- **OMG behavioral standards.** UML state machines, SysML activity
  diagrams, and OMG robotics specifications are ratified and give a
  standardized vocabulary for state-machine and activity-based behavior -
  a natural alternative or complement to behavior trees.
- **HTN / task-decomposition planning.** Hierarchical Task Networks are
  the canonical formal model for decomposing missions into subtasks. Not
  an ISO standard, but a well-defined formalism that maps cleanly onto
  IEEE 1872.1's task representation.

## 3. Cognitive-agent standards and architectures

- **FIPA (Foundation for Intelligent Physical Agents).** The closest
  thing to a standard for agents: Agent Communication Language (ACL),
  interaction protocols, and agent management. FIPA specifications are
  now stewarded under IEEE-SA; JADE is the reference implementation.
  Relevant if ASX models agent communication and coordination.
- **BDI (Belief-Desire-Intention).** A formal agent model, implementable
  within FIPA; a good source of ontology concepts for goal, intention,
  and plan.
- **Soar and ACT-R.** Mature symbolic cognitive architectures. Not
  standards, but they define stable, well-documented concept
  vocabularies (working memory, operators, problem spaces, procedural
  and declarative memory) that can be mined for a cognitive layer.

## 4. Autonomy and unmanned-systems reference architectures

Not ontologies, but standardized concept sources for autonomy levels and
system structure - useful for anchoring ASX terms.

- **NIST 4D/RCS.** Reference model architecture for unmanned vehicles
  (mission decomposition, planning, and execution hierarchy).
- **ALFUS (Autonomy Levels for Unmanned Systems).** NIST-originated,
  migrated to SAE AS-4D; characterizes autonomy via Human Independence,
  mission complexity, and environmental complexity.
- **SAE J3016.** The widely cited driving-automation levels - useful as a
  levels-of-autonomy pattern even outside road vehicles.
- **JAUS (SAE AS-4)**, **NATO STANAG 4586 / AEP-84** (standard interfaces of
  the UAV/UA control system), and **STANAG 4817** (multi-domain C2 of unmanned
  systems, in development). Interoperability and
  messaging architectures. Relevant because ASX lives inside SISO C2SIM,
  so alignment with the military-standard interoperability vocabulary is
  a real design constraint.

## Suggested priority for ASX

For ontology inclusion or alignment, a reasonable priority order:

1. **IEEE 1872.2 (AuR)** and **IEEE 1872.1 (task representation)** as the
   backbone.
2. **IEEE 7007** for the ethical-control dimension.
3. **FIPA / BDI** for the agent-communication and goal/intention layer.
4. **Behavior trees and HTN as modeled concept sets** (not citations) for
   the executable-behavior layer.

Anchor autonomy-level terms to **ALFUS / 4D/RCS**, and keep the whole
ontology consistent with **C2SIM / STANAG** naming, since C2SIM is ASX's
parent standard.

## See also

- `../Proposed Extension Working Materials/Plan-Semantics-Analysis.md` -
  the ASX plan-semantics proposal built on this survey: BT/BDI/HTN
  correlation with the LOX plan model plus a draft OWL module
  (`ASX-PlanSemantics-Draft.ttl`) and three validation walks.
- `../InstantiationReview/PlanSemantics-Walk.md` - verification and
  breadth pass over that proposal: capability matrix vs BT/Nav2,
  PDDL/PlanSys2, FlexBE, MAVLink, IEEE 1872.1-2024, IEEE 1872.2, JAUS
  AS6062, STANAG 4586, 4D/RCS, HTN, FIPA/BDI, with every C2SIM-side claim
  verified against the RDF. Two survey updates established there:
  IEEE 1872.1 published as **1872.1-2024** (June 2024), and IEEE 1872.2
  (AuR) verifiably defines **no Plan/Goal/Mission constructs of its own** -
  for plan semantics the relevant anchors are 1872.1-2024, STANAG 4586,
  and JAUS AS6062, not 1872.2.

## Sources

- IEEE 1872.2-2021 AuR Ontology:
  https://standards.ieee.org/ieee/1872.2/7094/ ,
  https://ieeexplore.ieee.org/document/9774339/ ,
  http://www.iri.upc.edu/files/scidoc/2526-IEEE-Standard-for-autonomous-robotics-ontology-[Standards].pdf
- IEEE 7007-2021 Ethically Driven R&A Ontology:
  https://standards.ieee.org/ieee/7007/7070/ ,
  https://ieeexplore.ieee.org/document/9611206/
- Behavior Trees in Robotics and AI: An Introduction (Colledanchise and
  Ogren): https://arxiv.org/abs/1709.00084 ; A survey of Behavior Trees
  in robotics and AI:
  https://www.sciencedirect.com/science/article/pii/S0921889022000513 ;
  Formalizing Stateful Behavior Trees:
  https://arxiv.org/pdf/2411.14165
- JADE - a FIPA-compliant agent framework:
  https://jmvidal.cse.sc.edu/library/jade.pdf ; Semantics of FIPA's Agent
  Communication Language:
  https://link.springer.com/article/10.1023/A:1010016503852
- An Analysis and Comparison of ACT-R and Soar:
  https://arxiv.org/pdf/2201.09305
- NIST 4D/RCS Version 2.0 Reference Model Architecture:
  https://www.nist.gov/publications/4drcs-version-20-reference-model-architecture-unmanned-vehicle-systems ;
  NIST SP 1011 ALFUS:
  https://www.nist.gov/system/files/documents/el/isd/ks/NISTSP_1011_ver_1-1.pdf
- Introduction to JAUS (NATO STO):
  https://publications.sto.nato.int/publications/STO%20Educational%20Notes/STO-EN-SCI-271/EN-SCI-271-02.pdf ;
  STANAG 4586 and JAUS comparison:
  https://novaresearch.unl.pt/en/publications/two-major-architectures-for-unmanned-systems-stanag-4586-and-jaus/
