# Scenario extracted from paper

Biagini, M., Corona, F., & Casar, J. (2017). Operational Scenario Modelling Supporting Unmanned Autonomous Systems Concept Development. International Workshop on Modelling and Simulation for Autonomous Systems.

## GPT-4 Results

### Summary narrative

The paper presents the development and experimentation of an air operational scenario focusing on dealing with the threat posed by an antagonistic swarm of Unmanned Autonomous Aerial Vehicles (UAAVs) targeting critical infrastructure within a highly populated mega-city environment. The scenarios are conceptualized under the premise of both unmanned autonomous systems serving as a force multiplier for friendlies and posing new challenges as potential threats.

### Specific goals to be achieved by the systems given the objectives

- Identify and exploit vulnerabilities in hostile UAAV functionalities to protect specific areas of interest from aerial threats.
- Determine the most effective defense methods against a swarm of hostile UAAVs in a future highly populated mega-city.
- Examine and push forward the capabilities of current and future urban defense systems in detecting, identifying, engaging, and neutralizing small and low-altitude UAAVs.

### Measures of Performance

- Effectiveness in fragmentation and chemical dispersal of payloads by UAAVs for enemy objectives.
- Efficiency in defending critical infrastructure and populated areas from hostile UAAV attacks.
- Capability in detecting, identifying, and engaging UAAVs within specified ranges and environmental conditions.
- Impact of defense actions on minimizing casualties and maintaining operational integrity of the state.

### Scenario steps

1. **Scenario Setup**: The urban environment is modeled based on the NATO ACT's Urbanization Project, considering future urbanization impacts and military operations within a 2035 metropolitan city model named "Archaria". The environment incorporates high-density, populated areas and critical infrastructures like power plants, airports, and embassies.
   
2. **Unmanned Aerial Vehicle Classification**: UAAVs are classified according to size, application area (e.g., Combat UAAV, Reconnaissance UAAV, Multipurpose UAAV), and functionality, focusing on their use for both reconnaissance and deploying lethal payloads.
   
3. **Defense Scenario Development**: Detailed scenarios describe potential enemy attacks using UAAVs against non-military targets within the mega-city, including shopping centers and chemical plants. Attack strategies involve guided weapons, deployment of poisonous substances, and precision-guided weapons aimed at causing extensive damage, panic, and casualties.
   
4. **Countermeasure Strategy Formulation**: Based on the UAAV threat model, counter-strategy involves deploying urban defense systems capable of detecting, identifying, and engaging UAAVs with a focus on minimizing collateral damage and casualties through both kinetic and non-kinetic actions.

5. **Simulation Execution and Analysis**: The scenario is executed within a Distributed Simulation Environment (DSE), employing a combination of simulators, AI modules, real C2 systems, and defense system models to analyze defense strategies' effectiveness against the hypothesized UAAV threats.

6. **Scenario Refinement and Experimentation**: Continuous development and experimentation aim to refine urban defense capabilities, including integrating real and virtual UAV platforms into the DSE to enhance control and situation awareness.

### Conceptual Model

**Domain and Scope**:
- Domain: Military Urban Operations, Unmanned Aerial Systems.
- Scope: Defense against hostile UAAV swarms in future mega-city environments.

**Concept Identification**:
- Concepts: UAAV, Defense System, Mega-City Environment, Critical Infrastructure.

**Define the Hierarchy**:
- UAAV -> Micro UAAV, Mini UAAV, Combat UAAV, Reconnaissance UAAV.
- Defense System -> Detection Systems, Engagement Systems, Command and Control (C2) Systems.
- Environment -> Urban, Littoral.

**Relationship Identification**:
- Defense System *protects* Critical Infrastructure.
- UAAV *attacks* Critical Infrastructure.
- C2 Systems *control* Defense Systems.

**Property Identification**:
- UAAV: Size, Payload Type, Level of Interoperability, Level of Autonomy.
- Defense System: Detection Range, Engagement Range, System Type (Kinetic/Non-Kinetic).

**Identify the Constraints/Rules**:
- UAAVs must obey engagement rules based on their level of autonomy.
- Defense systems must minimize collateral damage while effectively neutralizing UAAV threats.