# EIVAS Software Requirements Specification (Standard SRS Extract)

## 1. Introduction

### Product Scope

EIVAS is a Web application for epidemiological investigation scenarios. Through formatted data entry, storage, query, and visual association display, the system assists epidemiological form fillers in collecting case information and assists epidemiological analysts in analyzing case itineraries, associated cases, overall outbreaks, and statistical characteristics.

### Intended Audience

This document is intended for software designers, developers, testers, system users, and project stakeholders.

## 2. Overall Description

### Product Perspective

The system sits between case epidemiological investigation reporting and outbreak analysis workflows: front-end pages receive operations from fillers or analysts, the back-end database stores and provides case, itinerary, and association information, and the algorithm module generates regional flow maps and case clustering graphs based on case investigation information.

### Product Functions Summary

| Capability | Summary |
| --- | --- |
| Epidemiological reporting | Provides formatted entry interfaces to collect basic case information, disease-related information, itinerary trajectory information, and imported-case information. |
| Case management | Displays basic case information and investigation report completion status, and supports query, completion, search, sorting, and filtering. |
| Individual case analysis | Displays the itinerary of a single case, queries associated cases, and generates a case relationship graph. |
| Overall analysis | Generates regional flow maps and case clustering graphs through the algorithm module. |
| Outbreak overview | Displays outbreak heat maps, temperature and humidity trends, age distribution, occupation distribution, and transportation statistics charts. |

### User Classes

| User Class | Responsibilities / Needs |
| --- | --- |
| Epidemiological form filler | Collects basic case information, travel paths, close contact information, and social relationships through questionnaires or face-to-face interviews; the primary need is accurate and convenient information entry. |
| Epidemiological analyst | Summarizes and analyzes case reports and infers key outbreak information such as infection sources and transmission chains; the primary need is accurate and intuitive access to outbreak statistics and case associations. |

### Operating Environment

The system is provided as a Web application and is required to run on various operating systems and browsers. Specific browser versions, server operating systems, database products, and deployment environments are not specified in the specification.

### Assumptions and Dependencies

| ID | Assumption / Dependency |
| --- | --- |
| AD-001 | The system depends on a back-end database to store data required for cases, itineraries, and association analysis. |
| AD-002 | The system depends on an algorithm module to generate regional flow maps and case clustering graphs. |
| AD-003 | The system needs map or equivalent geographic visualization capability to display locations and itinerary paths. |
| AD-004 | The specification does not specify identity authentication, permission model, database type, map service provider, or deployment topology. |

## 3. External Interface Requirements

### User Interfaces

| UI Area | Requirement Summary |
| --- | --- |
| Epidemiological reporting form | Collects case information by page identifier for epidemiological form fillers and submits the information. |
| Case management list | Displays case name, ID number, gender, phone number, age, residence, and investigation completion status in a list. |
| Map display interface | Displays candidate addresses, daily itinerary paths for cases, and related geographic locations. |
| Association information display | Displays associated case entries that meet time-threshold and space-threshold conditions. |
| Graph relationship display | Displays location co-occurrence and potential transmission relationships with a confirmed case as the central node. |
| Statistical charts | Displays regional flow maps, case clustering graphs, heat maps, line charts, pie charts, and bar charts. |

### Software/API Interfaces

| Interface | Requirement Summary |
| --- | --- |
| Front-end page to back-end database interface | Front-end pages transmit analyst or filler requests to the back-end database through interfaces, and the back-end database extracts information and feeds it back to front-end components. |
| Database storage interface | After the reporting form is submitted, case investigation information is sent to the back-end database for storage and analysis. |
| Algorithm module interface | The algorithm module calculates risks, clusters cases, and generates corresponding charts based on case investigation information. |

### Communication Interfaces

The system is a Web application. The specification only states that front-end pages interact with the back-end database through interfaces, and does not specify protocols, ports, message formats, authentication methods, or encrypted transport protocols. Query requests involving personal information must be encrypted.

### Data Exchange Formats

| Data Group | Fields / Content |
| --- | --- |
| Basic information | Name, gender, age, height, weight, ID number, contact information, address, occupation, and workplace. |
| Disease-related information | Disease onset and medical treatment, laboratory test results, risk factors, and exposure history. |
| Itinerary trajectory information | Date, main stay area, transportation mode between areas, arrival time, stay duration, protective measures, area location, main close contacts, departure location, destination, and transportation vehicle. |
| Imported-case information | Travel or residence country, transit country, nationality, passport ID, entry location, entry time, entry transportation mode, and vehicle/ship/flight number. |
| Associated case entry | Time, location, associated case name, association time, association location, and straight-line distance. |

## 4. Functional Requirements

| ID | Description | Trigger / Input | System Behavior | Output | Priority | Verification |
| --- | --- | --- | --- | --- | --- | --- |
| FR-001 | The system shall allow epidemiological form fillers to enter case investigation information. | A filler enters basic case information, disease-related information, itinerary trajectory information, and optional imported-case information in the outbreak reporting form and clicks submit. | The system receives and submits formatted investigation information to the back-end database for storage and analysis. | Saved case investigation record. | High | Test |
| FR-002 | The system shall provide investigation prompt information when a case cannot recall detailed activity locations in a high-risk area. | A case states that they arrived at a high-risk area but cannot recall detailed activity locations. | The system searches recorded case itinerary data in the database, filters detailed activity locations for cases that arrived at that risk area, and displays prompts on the page. | Activity location prompt list. | High | Demonstration |
| FR-003 | The system shall support visual confirmation of epidemiological path locations. | An investigator selects an address that may be ambiguous in the case description. | The system displays the selected address on a map for the case to confirm. | Candidate location display and confirmation result on the map. | High | Demonstration |
| FR-004 | The system shall support completion or correction of case information. | Case information requires multiple interviews for supplementation, or memory errors and omissions require correction. | The system provides the ability to edit or complete existing case information. | Updated case information. | High | Test |
| FR-005 | The system shall display case information in list form. | A user enters case management or executes a case information query. | The system displays case name, ID number, gender, phone number, age, residence, and investigation completion status. | Case information list. | High | Test |
| FR-006 | The system shall support searching cases by name. | A user enters a case name or name keyword. | The system quickly searches for matching cases by name. | Search result list. | High | Test |
| FR-007 | The system shall support sorting cases by age. | A user selects the age sorting operation. | The system sorts the list according to case age. | Case list sorted by age. | High | Test |
| FR-008 | The system shall support filtering cases by gender. | A user selects a gender filter condition. | The system filters the case list and displays only cases that match the gender condition. | Filtered case list. | High | Test |
| FR-009 | The system shall support querying and visually displaying case itineraries. | An analyst selects a case or a path for a specific day. | The system queries formatted path information in the database and displays the case itinerary through a visual interface and map. | Formatted path information and map path display. | High | Demonstration |
| FR-010 | The system shall support querying associated cases by spatial and temporal thresholds. | An analyst specifies a spatial threshold and a temporal threshold. | The system queries association information for all patients in the database and filters entries that meet the threshold requirements. | Information entries containing time, location, associated case, association time, association location, and straight-line distance. | High | Test |
| FR-011 | The system shall display a confirmed case relationship graph. | An analyst selects a confirmed case for individual case analysis. | The system uses the confirmed case as the central node and displays other confirmed cases with location co-occurrence relationships and potential transmission relationships. | Confirmed case relationship graph. | High | Demonstration |
| FR-012 | The system shall generate and display a regional flow map. | A user opens the regional risk interface in overall analysis. | The system retrieves case investigation information from the database; if information is missing or problematic, it returns an error and prompts case information management; if information is sufficient, the algorithm module calculates case movement and location risk levels and draws a regional flow map. | Error prompt or regional flow map. | High | Test |
| FR-013 | The system shall generate and display a case clustering graph. | A user opens the clustering outbreak analysis interface in overall analysis. | The system retrieves case investigation information from the database; if information is missing or problematic, it returns an error and prompts case information management; if information is sufficient, the algorithm module clusters cases according to thresholds and rules and draws a case clustering graph. | Error prompt or case clustering graph. | High | Test |
| FR-014 | The system shall display an outbreak heat map. | An analyst views the outbreak severity within a region. | The system displays the spatial distribution of the outbreak as a heat map and uses color depth to indicate the number of case stopovers. | Outbreak heat map. | High | Demonstration |
| FR-015 | The system shall display a temperature and humidity trend chart. | An analyst needs to compare the relationship between outbreak spread and climate changes. | The system displays temperature and humidity changes since the outbreak began as a line chart. | Temperature and humidity trend line chart. | High | Demonstration |
| FR-016 | The system shall display an age distribution chart. | An analyst needs to analyze the relationship between age and infection. | The system counts confirmed cases by age group and displays them as a pie chart. | Age distribution pie chart. | High | Demonstration |
| FR-017 | The system shall display an occupation distribution chart. | An analyst needs to identify occupations vulnerable to viral infection. | The system counts occupation distribution among confirmed cases and displays it as a pie chart. | Occupation distribution pie chart. | High | Demonstration |
| FR-018 | The system shall display a transportation statistics chart. | An analyst needs to understand the relationship between different transportation modes and viral spread. | The system counts the frequency with which confirmed cases used each transportation mode and displays it as a bar chart. | Transportation mode frequency bar chart. | High | Demonstration |

## 5. Non-Functional Requirements

| ID | Quality | Requirement | Fit Criterion | Priority | Verification |
| --- | --- | --- | --- | --- | --- |
| NFR-001 | Robustness | The system shall handle input cases outside the specified standard requirements. | Abnormal input shall not cause the system to crash. | High | Test |
| NFR-002 | Performance | The system shall support concurrent submission requests. | When 100 users submit requests simultaneously, page response time is less than 1 second. | High | Test |
| NFR-003 | Reliability / Availability | The system shall be able to run stably for long periods and support fast deployment switching. | When an unexpected event occurs, the system switches to the backup server within 20 minutes. | High | Analysis |
| NFR-004 | Security / Privacy | Query requests involving user personal information shall be encrypted. | Personal information query requests must be encrypted; the specification does not specify an encryption algorithm or protocol. | High | Inspection |
| NFR-005 | Resource Protection | The system shall cool down IP addresses that submit frequent query requests within a short period. | Frequently querying IP addresses are cooled down to avoid excessive server resource consumption and impact on normal investigation reporting and analysis. | High | Test |
| NFR-006 | Compatibility | The system shall support operation on various operating systems and browsers. | Core flows can be completed on target operating system and browser combinations; specific versions are to be defined by the project. | High | Test |
| NFR-007 | Maintainability | The system code architecture shall support later maintenance. | Supports bug fixing, function modification, and new function addition; the team uses a unified coding style and adds code comments. | Medium | Inspection |
| NFR-008 | Usability | The system interface shall be concise and clear for professional epidemiological workers. | The interface primarily targets user understanding and use and avoids excessive artistic design. | High | Inspection |
| NFR-009 | Operational Usability | The system shall provide operational assistance for grassroots workers who lack software experience. | The system includes many operation prompts, error-operation feedback, and may include user documentation. | High | Demonstration |

## 6. Data Requirements

| ID | Data Object | Requirement | Privacy / Integrity Notes | Verification |
| --- | --- | --- | --- | --- |
| DR-001 | Basic case information | The system shall record name, gender, age, height, weight, ID number, contact information, address, occupation, and workplace. | Contains personal identity and contact information and shall be constrained by personal information protection requirements. | Inspection |
| DR-002 | Disease-related information | The system shall record disease onset and medical treatment, laboratory test results, risk factors, and exposure history. | Sensitive health information that shall not be leaked. | Inspection |
| DR-003 | Itinerary trajectory information | The system shall record date, main stay area, transportation mode between areas, arrival time, stay duration, protective measures, area location, main close contacts, and related information. | Missing or problematic itinerary information affects overall analysis results. | Test |
| DR-004 | Imported-case information | The system shall support optional entry of travel or residence country, transit country, nationality, passport ID, entry location, entry time, entry transportation mode, and vehicle/ship/flight number. | Contains identity and entry information and shall be constrained by personal information protection requirements. | Inspection |
| DR-005 | Case management record | The system shall save and display case name, ID number, gender, phone number, age, residence, and investigation completion status. | List display involves personal information queries and shall follow the personal information query encryption requirement; the permission model is not specified in the specification. | Test |
| DR-006 | Associated case entry | The system shall generate or display time, location, associated case name, association time, association location, and straight-line distance. | Association information comes from case itinerary and location data, and erroneous data affects association judgment. | Test |
| DR-007 | Analytical chart data | The system shall use case investigation information, case stopover counts, temperature and humidity, age, occupation, and transportation mode data to generate statistical charts. | Statistical results depend on completeness and validity of input case data. | Analysis |
| DR-008 | Data quality state | The system shall identify missing or problematic case investigation information and return errors and case information management prompts in overall analysis. | Serves as a prerequisite data quality check for analysis. | Test |

## 7. Constraints

| ID | Constraint |
| --- | --- |
| C-001 | The system product form is a Web application. |
| C-002 | The scope of investigation reporting information shall refer to cited materials such as infectious disease information reporting management specifications. |
| C-003 | The system operating environment needs to cover various operating systems and browsers; specific target versions are not provided in the specification. |
| C-004 | Query requests involving personal information must be encrypted, and frequent query IP addresses must be cooled down. |
| C-005 | When an unexpected event occurs, the system shall switch to the backup server within 20 minutes. |
| C-006 | The user interface shall target understanding and use by professional epidemiological workers and remain concise and clear. |
| C-007 | The system shall provide operation prompts and error feedback for grassroots workers and may provide user documentation. |

## 8. Verification and Acceptance

| ID | Verification Method | Acceptance Focus |
| --- | --- | --- |
| FR-001 | Test | After submitting a complete case investigation form, the back-end database contains the corresponding formatted record. |
| FR-002 | Demonstration | In a prompt scenario for a high-risk area, the page displays detailed activity locations from historical itinerary data. |
| FR-003 | Demonstration | After an ambiguous address is selected, the map displays candidate locations and supports confirmation. |
| FR-004 | Test | After supplementing or correcting an existing case record, the record content is updated. |
| FR-005 | Test | The case management list displays the case fields and investigation completion status required by the specification. |
| FR-006 | Test | After a name keyword is entered, only matching cases are returned. |
| FR-007 | Test | After age sorting is executed, the case list order conforms to the age sorting rule. |
| FR-008 | Test | After a gender filter condition is selected, the case list contains only matching cases. |
| FR-009 | Demonstration | After selecting a case or date, the page displays formatted path information and map path. |
| FR-010 | Test | Given temporal and spatial thresholds, the system returns associated case entries that meet the thresholds. |
| FR-011 | Demonstration | After selecting a confirmed case, a relationship graph centered on that case is displayed. |
| FR-012 | Test | When data is insufficient, an error and management prompt are returned; when data is sufficient, the regional flow map is displayed. |
| FR-013 | Test | When data is insufficient, an error and management prompt are returned; when data is sufficient, the case clustering graph is displayed. |
| FR-014 | Demonstration | The outbreak heat map presents color depth according to the number of case stopovers. |
| FR-015 | Demonstration | The temperature and humidity trend chart displays changes since the outbreak began as a line chart. |
| FR-016 | Demonstration | The age distribution chart displays the proportion of confirmed cases by age group as a pie chart. |
| FR-017 | Demonstration | The occupation distribution chart displays occupation distribution among confirmed cases as a pie chart. |
| FR-018 | Demonstration | The transportation statistics chart displays the frequency of each transportation mode as a bar chart. |
| NFR-001 | Test | Abnormal input does not cause the system to crash. |
| NFR-002 | Test | When 100 users submit requests simultaneously, page response time is less than 1 second. |
| NFR-003 | Analysis | The failover plan proves that the system can switch to the backup server within 20 minutes. |
| NFR-004 | Inspection | Query requests involving personal information have encrypted-processing design or implementation artifacts. |
| NFR-005 | Test | Frequently querying IP addresses are cooled down, and normal reporting and analysis requests are not affected by excessive queries. |
| NFR-006 | Test | Core flows can run on target operating system and browser combinations. |
| NFR-007 | Inspection | Code structure, coding style, and comments satisfy maintenance requirements. |
| NFR-008 | Inspection | Core interfaces are concise and clear, without excessive decoration that affects understanding and use. |
| NFR-009 | Demonstration | The page provides operation prompts and error feedback, and user documentation or equivalent help content can be accessed. |
| DR-001 | Inspection | Basic case information fields are completely defined and constrained by privacy protection. |
| DR-002 | Inspection | Disease-related information fields are completely defined and constrained by sensitive health information protection. |
| DR-003 | Test | Itinerary trajectory fields can be entered, saved, and used for path display. |
| DR-004 | Inspection | Imported-case information fields support optional entry and are constrained by privacy protection. |
| DR-005 | Test | Case management list fields and completion status can be read and displayed. |
| DR-006 | Test | Associated case entry fields are completely generated and displayed. |
| DR-007 | Analysis | Statistical chart data sources are consistent with case investigation data, temperature and humidity, age, occupation, and transportation mode fields. |
| DR-008 | Test | Missing or abnormal case investigation information triggers errors and management prompts. |
| C-001 | Inspection | The design and implementation are delivered as a Web application. |
| C-002 | Inspection | Investigation reporting fields cover the case information scope in the standards cited by the specification. |
| C-003 | Test | Target operating system and browser compatibility tests pass. |
| C-004 | Inspection | Personal information query encryption and frequent-IP cooldown mechanisms have design or implementation artifacts. |
| C-005 | Analysis | The failover process satisfies the 20-minute constraint. |
| C-006 | Inspection | Interface style is consistent with professional epidemiological worker usage scenarios. |
| C-007 | Demonstration | Operation prompts, error feedback, and user documentation can be seen or triggered by users. |
