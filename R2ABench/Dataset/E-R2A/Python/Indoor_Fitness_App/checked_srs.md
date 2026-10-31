# Indoor Fitness App Software Requirements Specification (Standard SRS Extract)

## 1. Introduction

### Product Scope

Indoor Fitness App is an indoor exercise and health application based on pose estimation. It targets exercise scenarios with available activity space, such as homes, offices, gyms, and outdoor playgrounds. The system provides professional posture evaluation, intelligent training plan recommendation, training poster and professional report generation, and exercise screen casting. Its goal is to let users receive guidance similar to a personal trainer during indoor exercise.

### Intended Audience

This document is intended for application users, developers, testers, architects, and project stakeholders. The specification explicitly expects users and developers to fully understand the software requirements.

## 2. Overall Description

### Product Perspective

The system consists of a mobile App, camera video capture capability, server-side processing capability, training plan and report generation capability, and Android screen casting within the same LAN. The specification does not specify the database product, model deployment location, API protocol, map service, or third-party service dependency. The requirement to prevent SQL injection indicates implementation risk related to SQL queries, but the concrete data storage solution is not expanded in the Markdown body.

### Product Functions Summary

| Capability | Summary |
| --- | --- |
| Professional posture evaluation | Uses the mobile phone camera to capture exercise video, extracts skeleton information in real time, compares it with standard skeleton movements, and scores the posture. |
| Intelligent recommendation | Recommends or adjusts exercise plans based on training goals, physical condition, restrictions, real-time exercise state, and training results. |
| Fun sharing | Generates exercise posters and training reports from training materials for users to save and share. |
| Exercise screen casting | Searches for Android devices in the same LAN and casts the exercise interface in real time after connection. |
| History and personal management | Displays exercise history and monthly exercise overview, and supports completing personal information and exercise preferences. |
| Security and permissions | Performs user information verification, distinguishes administrator and ordinary user permissions, and prevents user data leakage and SQL injection. |

### User Classes

| User Class | Responsibilities / Needs |
| --- | --- |
| Amateur exercise enthusiast | Includes students, office workers, and fitness enthusiasts who use the application for exercise guidance and training feedback anytime and anywhere. |
| Professional exerciser | Includes fitness coaches who may use posture evaluation, training plans, and report capabilities to support professional exercise guidance. |
| Logged-in user | Can execute use cases such as professional evaluation, plan recommendation, fun sharing, and exercise screen casting. |
| Administrator user | Has different permissions from ordinary users; the concrete permission scope is not expanded in the specification. |

### Operating Environment

| Environment | Requirement |
| --- | --- |
| Usage scenario | Available 24 hours a day, with no restriction on usage time, duration, or location as long as activity space is available. |
| Server hardware | CPU Pentium 900M, recommended Pentium 4 1.2G; at least 256 MB RAM. |
| PC hardware | CPU Pentium 133M or higher; at least 64 MB RAM. |
| Mobile hardware | Octa-core 2.45 GHz CPU, 4 GB RAM + 32 GB ROM or above. |
| PC software | Windows operating system. |
| Mobile software | Android 8.0 or iOS 11.0 and above. |

### Assumptions and Dependencies

| ID | Assumption / Dependency |
| --- | --- |
| AD-001 | Professional evaluation depends on a mobile phone camera and video recording capability of at least 30 fps. |
| AD-002 | Exercise screen casting depends on the current Android device and target Android device being in the same LAN. |
| AD-003 | The system depends on server-side participation for use cases such as plan recommendation and poster/report material processing. |
| AD-004 | The system includes static data, dynamic data, a data dictionary, and an E-R diagram, but the Markdown body does not expand the fields in the images. |
| AD-005 | SQL injection protection implies SQL query or SQL-style data access risk; the concrete database product is not specified. |

## 3. External Interface Requirements

### User Interfaces

| UI Area | Requirement Summary |
| --- | --- |
| App main interface | Displays the user's exercise plan preview for today and allows viewing the complete exercise plan. |
| Exercise interface | Displays the user's camera-captured movement, standard movement, real-time posture evaluation, posture stick diagram, and remaining action time. |
| Professional report interface | Uses charts to intuitively display body information and exercise conditions. |
| Exercise history interface | Displays overall exercise history through a calendar and shows an overview of the current month's exercise. |
| Personal interface | Supports completing personal information, selecting exercise preferences, and viewing historical training records. |
| Casting operation interface | Guides users to search for Android devices in the same LAN, connect, and start real-time screen casting. |

### Software/API Interfaces

| Interface | Requirement Summary |
| --- | --- |
| Camera capture interface | The App uses a fixed mobile phone camera to monitor body posture in real time and capture video during exercise. |
| Posture evaluation processing interface | The terminal device feeds back skeleton extraction information in real time and compares it with standard skeleton movements for scoring. |
| Server-side processing interface | Plan recommendation and poster/report material collection and processing involve server-side participation. |
| Inter-module data exchange interface | The project adopts a modular design concept, and modules rely on interfaces for data exchange. |
| SQL data access interface | The specification requires SQL injection prevention but does not specify the database product, table structure, or access protocol. |

### Communication Interfaces

| Communication | Requirement Summary |
| --- | --- |
| Casting video stream | The exercise interface video stream is transmitted between Android devices, with video stream latency not exceeding 100 ms. |
| Android server-to-client commands | After the Android server sends a command to the Android client, client response latency does not exceed 50 ms. |
| Same-LAN device discovery and connection | Before casting, Android devices in the same LAN must be searched and connected successfully. |
| App-server interaction | The RUCM table lists the server side as an actor; concrete protocol, authentication token, and message format are not specified. |

### Data Exchange Formats

| Data Group | Fields / Content |
| --- | --- |
| Standard videos / standard movements | The user selects a series of standard videos to form a custom exercise plan, and the system compares the user's skeleton with standard skeleton movements. |
| User body and exercise input | User health information, training goals, physical condition, restrictions, and real-time exercise state. |
| Video and skeleton data | Camera-captured video, skeleton extraction information, posture similarity score, and posture evaluation result. |
| Training plan data | User custom exercise plan, system training plan, next exercise set plan, rest plan, and plan completion degree. |
| Training material and report data | Posture-, state-, and plan-related images, text, data, statistical charts, textual explanations, training posters, and training reports. |
| Exercise history and personal preferences | Exercise history, monthly exercise overview, personal information, exercise preferences, and historical training records. |
| Casting data | Exercise interface video stream, Android device discovery/connection information, and server-to-client control commands. |
| Static/dynamic data model | The specification references images for static data, dynamic data, data dictionary, and E-R diagram; the Markdown body does not include field details. |

## 4. Functional Requirements

| ID | Description | Trigger / Input | System Behavior | Output | Priority | Verification |
| --- | --- | --- | --- | --- | --- | --- |
| FR-001 | The system shall display a preview of the user's exercise plan for today on the App main interface and support viewing the full exercise plan. | The user opens the App main interface or clicks to view more. | The system reads and displays today's exercise plan preview; when the user requests the full plan, it displays the complete exercise plan. | Today's plan preview and complete exercise plan. | High | Demonstration |
| FR-002 | The system shall allow the user to select standard videos to form a custom exercise plan. | A logged-in user selects a series of standard videos. | The system combines the selected standard videos into the user's custom exercise plan. | User custom exercise plan. | High | Test |
| FR-003 | The system shall allow the user to turn on the camera and capture fitness video during exercise. | The user starts professional evaluation and turns on the camera. | The system uses the mobile phone camera to capture the user's exercise video. | User fitness video input stream. | High | Demonstration |
| FR-004 | The system shall extract skeleton information in real time and compare it with standard skeleton movements for scoring. | The exercise video stream enters the professional evaluation process. | The terminal device feeds back skeleton extraction information in real time and compares the user's skeleton with standard skeleton movements. | Posture similarity score and skeleton evaluation result. | High | Test |
| FR-005 | The system shall display the user movement, standard movement, real-time posture evaluation, posture stick diagram, and remaining action time on the exercise interface. | The user enters the exercise interface and starts training. | The system synchronously displays camera-captured user movement, standard movement, posture evaluation information, posture stick diagram, and remaining time. | Real-time exercise evaluation interface. | High | Demonstration |
| FR-006 | The system shall monitor exercise state data and evaluate actual training completion. | The user performs exercise training. | The system monitors exercise state data and combines physical fitness standards and camera detection to determine exercise start, exercise end, and plan completion degree. | Training completion evaluation. | High | Test |
| FR-007 | The system shall create a system training plan based on user training goals, physical condition, and restrictions. | The user provides training goals, physical condition, and restrictions. | The system synthesizes the input information to create a training plan. | System training plan. | High | Test |
| FR-008 | The system shall recommend or adjust exercise plans after the user completes professional evaluation. | The user completes A001 professional evaluation or a training session ends. | The system combines the user's exercise situation, voice prompts, real-time state, and training result to recommend or adjust the exercise plan, next exercise set plan, and rest plan. | Recommended or adjusted exercise plan. | High | Test |
| FR-009 | The system shall generate a training summary poster that can be saved and shared. | The user completes at least one training session and clicks the generate button. | The server collects and processes training materials, and the system generates a training summary poster from posture-, state-, and plan-related images, text, and data. | Training summary poster. | Medium | Demonstration |
| FR-010 | The system shall generate a professional training report. | The user completes at least one training session and requests report generation. | The server collects and processes materials, and the system displays professional statistical data using charts and textual explanations based on monitoring and evaluation results. | Professional training report. | High | Demonstration |
| FR-011 | The system shall allow the user to view exercise history and monthly exercise overview. | The user enters the exercise history interface. | The system displays overall exercise history through a calendar and displays an overview of the current month's exercise. | Exercise history calendar and monthly overview. | Medium | Demonstration |
| FR-012 | The system shall allow the user to complete personal information, select exercise preferences, and view historical training records. | The user enters the personal interface. | The system allows the user to maintain personal information and exercise preferences and enter historical training records. | Updated personal information, preferences, and historical training records. | Medium | Test |
| FR-013 | The system shall verify user identity and distinguish permissions between administrator users and ordinary users. | A user logs in, registers, or accesses permission-controlled functions. | The system checks user identity and applies different usage permissions according to user type. | Login/registration verification result and permission-control result. | High | Test |
| FR-014 | The system shall search for Android casting devices in the same LAN and establish a connection. | A logged-in Android user starts exercise, selects casting, and follows instructions to search for devices. | The system searches for Android devices in the same LAN and connects after a successful search. | Connected casting target device. | High | Demonstration |
| FR-015 | The system shall cast the exercise interface to the connected Android device in real time. | The user completes casting device connection and starts exercise. | The system records the exercise interface in real time and casts it to the target Android device. | Real-time exercise interface on the target Android device. | High | Demonstration |

## 5. Non-Functional Requirements

| ID | Quality | Requirement | Fit Criterion | Priority | Verification |
| --- | --- | --- | --- | --- | --- |
| NFR-001 | User Satisfaction | The final user survey satisfaction for the system shall reach the target value. | Satisfaction reaches above 90%. | Medium | Analysis |
| NFR-002 | Pose Recognition Accuracy | Under normal scenarios, system pose recognition shall achieve high accuracy. | When lighting, background, person size are normal and no occlusion or missing parts exist, pose recognition accuracy is above 95%. | High | Test |
| NFR-003 | Occlusion Robustness | Under occlusion or missing-part scenarios, the system shall maintain recognition accuracy for visible parts. | Accuracy for unoccluded and non-missing parts is above 90%; accuracy for occluded parts reaches 50%. | High | Test |
| NFR-004 | Model Runtime Performance | Pose estimation model runtime speed shall satisfy real-time evaluation needs. | Model runtime speed reaches above 20 fps. | High | Test |
| NFR-005 | Pose Evaluation Accuracy | When pose estimation has no errors, user posture evaluation shall achieve high accuracy. | Posture evaluation accuracy is above 95%. | High | Test |
| NFR-006 | Pose Error Tolerance | When pose estimation contains errors, the evaluation algorithm shall identify errors and maintain accuracy. | The algorithm can identify errors most of the time and guarantee accuracy no lower than 95%; "most of the time" must be quantified in the test plan. | High | Test |
| NFR-007 | Body-Proportion Robustness | Posture similarity estimation shall reduce the impact of user body shape and body proportion on scoring. | The specification only requires "eliminating the impact to a certain extent" and does not provide a quantitative threshold. | Medium | Analysis |
| NFR-008 | Recommendation Latency | Recommended plan generation shall meet the response-time constraint. | Each recommended plan is generated within 1 second. | High | Test |
| NFR-009 | Report Generation Latency | Exercise report generation shall meet the response-time constraint. | Exercise report generation time does not exceed 3 seconds. | High | Test |
| NFR-010 | Casting Video Latency | Casting video stream transmission latency shall meet real-time display requirements. | Video stream transmission latency between devices does not exceed 100 ms. | High | Test |
| NFR-011 | Casting Command Latency | Response latency after the Android server sends a command to the client shall meet real-time control requirements. | Android client response latency does not exceed 50 ms. | High | Test |
| NFR-012 | Data Leakage Protection | The system shall take leakage-protection measures to prevent user data leakage. | Leakage risk is reduced through clipboard control, drag-and-drop control, screen copy/screenshot control, memory theft control, and related techniques. | High | Inspection |
| NFR-013 | SQL Injection Protection | The system shall prevent SQL injection. | Variable data types and formats are checked, special symbols are filtered, variables are bound, and precompiled statements are used. | High | Inspection |
| NFR-014 | Portability | The system shall support a certain degree of module portability. | It adopts a modular design concept, and modules rely on interfaces for data exchange. | Medium | Inspection |

## 6. Data Requirements

| ID | Data Object | Requirement | Privacy / Integrity Notes | Verification |
| --- | --- | --- | --- | --- |
| DR-001 | Standard videos and standard movements | The system shall save or access a series of standard videos and standard skeleton movements for user custom exercise plans and posture comparison. | The version and quality of standard movement data affect scoring consistency; the specification does not provide version management requirements. | Inspection |
| DR-002 | User body and training profile | The system shall use user health information, training goals, physical condition, restrictions, personal information, and exercise preferences. | This is personal health and preference data and shall be constrained by leakage protection and identity verification requirements. | Inspection |
| DR-003 | Exercise video data | The system shall capture user exercise video for posture evaluation and exercise interface display. | Video may contain personal images and shall be constrained by user data leakage protection. | Test |
| DR-004 | Skeleton and posture evaluation data | The system shall generate skeleton extraction information, posture similarity scores, professional evaluations, and posture stick diagrams. | Evaluation data integrity directly affects training feedback and reports. | Test |
| DR-005 | Training plans and completion degree | The system shall maintain user custom exercise plans, system training plans, next exercise set plans, rest plans, and plan completion degree. | Training plans shall be consistent with user goals, physical condition, and restrictions. | Test |
| DR-006 | Training report and poster materials | The system shall process posture-, state-, and plan-related images, text, data, and statistical charts for generating posters and professional reports. | Server material collection must follow user data leakage protection requirements. | Test |
| DR-007 | Historical training records | The system shall save and display overall exercise history, monthly exercise overview, and previous training records. | Historical records are bound to user identity and shall be constrained by identity verification and permission control. | Test |
| DR-008 | Casting session data | The system shall process Android device discovery, connection, exercise interface video stream, and control command data. | The target device must be in the same LAN; the specification does not specify encryption or authentication mechanisms. | Test |
| DR-009 | Static/dynamic data model | The system data model shall include the static data, dynamic data, data dictionary, and E-R diagram contents described in the specification. | The Markdown body only references images, and field-level details must be further extracted from images or the original model. | Inspection |

## 7. Constraints

| ID | Constraint |
| --- | --- |
| C-001 | A precondition for professional evaluation is that the user's mobile phone supports video recording at 30 fps or above. |
| C-002 | Exercise screen casting requires the current Android device and searched Android device to be in the same LAN. |
| C-003 | Server hardware shall satisfy CPU Pentium 900M, recommended Pentium 4 1.2G, and at least 256 MB RAM. |
| C-004 | PC hardware shall satisfy CPU Pentium 133M or higher and at least 64 MB RAM. |
| C-005 | Mobile hardware shall reach an octa-core 2.45 GHz CPU and 4 GB RAM + 32 GB ROM or above. |
| C-006 | The PC operating system shall be Windows. |
| C-007 | The mobile operating system shall be Android 8.0 or iOS 11.0 and above; the casting target is limited to Android devices in the specification. |
| C-008 | User exercise location is not restricted to a specific place, but activity space must be available. |
| C-009 | The system shall prepare and verify software requirements according to the software requirements, testing, life-cycle, and measurement standards listed in the specification. |

## 8. Verification and Acceptance

| ID | Verification Method | Acceptance Focus |
| --- | --- | --- |
| FR-001 | Demonstration | The main interface displays today's plan preview, and the complete exercise plan is displayed after viewing more. |
| FR-002 | Test | After multiple standard videos are selected, the system forms a user custom exercise plan. |
| FR-003 | Demonstration | After the user starts evaluation and turns on the camera, the system captures exercise video. |
| FR-004 | Test | The system outputs skeleton extraction results in real time and generates scores after comparison with standard movements. |
| FR-005 | Demonstration | The exercise interface simultaneously displays user movement, standard movement, posture evaluation, posture stick diagram, and remaining time. |
| FR-006 | Test | The system can detect exercise start/end and output training completion evaluation. |
| FR-007 | Test | After training goals, physical condition, and restrictions are entered, the system generates a training plan. |
| FR-008 | Test | After professional evaluation is completed or training ends, the system generates a recommended or adjusted exercise plan. |
| FR-009 | Demonstration | After at least one training session is completed and the generate button is clicked, the system outputs a training poster that can be saved or shared. |
| FR-010 | Demonstration | After at least one training session is completed and a report is requested, the system outputs a professional report containing charts and textual explanations. |
| FR-011 | Demonstration | The exercise history interface displays training history and monthly overview through a calendar. |
| FR-012 | Test | The user can edit personal information and exercise preferences and view historical training records. |
| FR-013 | Test | In login, registration, and permission scenarios, the system completes identity checks and distinguishes administrator/ordinary user permissions. |
| FR-014 | Demonstration | Android devices in the same LAN can be searched and connected. |
| FR-015 | Demonstration | After successful connection, the exercise interface is cast to the target Android device in real time. |
| NFR-001 | Analysis | User survey satisfaction reaches above 90%. |
| NFR-002 | Test | Pose recognition accuracy in normal scenarios reaches above 95%. |
| NFR-003 | Test | In occlusion/missing scenarios, accuracy for unoccluded parts reaches above 90%, and occluded parts reach 50%. |
| NFR-004 | Test | Pose estimation model runtime speed reaches above 20 fps. |
| NFR-005 | Test | When pose estimation has no errors, posture evaluation accuracy reaches above 95%. |
| NFR-006 | Test | When pose estimation has errors, the algorithm identifies errors and maintains accuracy no lower than 95%. |
| NFR-007 | Analysis | The test plan defines how to evaluate body-shape and body-proportion impact and proves that the impact is reduced. |
| NFR-008 | Test | Each recommended plan is generated within 1 second. |
| NFR-009 | Test | Exercise report generation time does not exceed 3 seconds. |
| NFR-010 | Test | Casting video stream latency between devices does not exceed 100 ms. |
| NFR-011 | Test | Response latency from Android server command to client does not exceed 50 ms. |
| NFR-012 | Inspection | Leakage-protection design or implementation artifacts exist for clipboard, drag-and-drop, screen copy/screenshot, memory theft, and related controls. |
| NFR-013 | Inspection | SQL input checking, special symbol filtering, variable binding, and precompiled statement mechanisms exist. |
| NFR-014 | Inspection | Modular design and module interface data exchange mechanisms exist. |
| DR-001 | Inspection | Standard video and standard movement data can be referenced by the system. |
| DR-002 | Inspection | User body, goal, restriction, personal information, and preference fields are defined and protected. |
| DR-003 | Test | Camera video data can be captured and enter the posture evaluation process. |
| DR-004 | Test | Skeleton, score, professional evaluation, and posture stick diagram data can be generated and displayed. |
| DR-005 | Test | Training plan and completion data can be created, adjusted, and read. |
| DR-006 | Test | Materials required for posters and reports can be collected, processed, and output. |
| DR-007 | Test | Historical training records, monthly overview, and previous training records can be displayed. |
| DR-008 | Test | Device discovery, connection, video stream, and control commands can complete a casting session. |
| DR-009 | Inspection | Field details for static data, dynamic data, data dictionary, and E-R diagram are supplemented or extracted from images. |
| C-001 | Inspection | The evaluation flow checks or documents the mobile phone requirement of recording at 30 fps or above. |
| C-002 | Demonstration | Casting devices in the same LAN are searched and connected. |
| C-003 | Inspection | Server deployment environment satisfies hardware requirements. |
| C-004 | Inspection | PC environment satisfies hardware requirements. |
| C-005 | Inspection | Mobile environment satisfies hardware requirements. |
| C-006 | Inspection | PC runtime environment is Windows. |
| C-007 | Inspection | Mobile version satisfies Android 8.0 or iOS 11.0 and above, and casting target is an Android device. |
| C-008 | Demonstration | The exercise flow can be entered in different scenarios with activity space. |
| C-009 | Inspection | Requirements, testing, and acceptance materials cite or satisfy related standards. |
