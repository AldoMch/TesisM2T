# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines evidence-backed software requirements for the `mendhak/gpslogger` repository at commit `ab894229de5ef1fec726b8a9588e98089b9564c6`. It covers the supported runtime behavior, integrations, data handling, and operational constraints visible in the repository evidence pack.

### Product scope
GPSLogger is an Android-based GPS logging application/service that obtains location updates, distributes them within the application, and supports optional external integrations including OpenStreetMap, Dropbox, and OpenGTS. Evidence also shows a build/import workflow for Android development and a dependency on Google Play Services for at least one feature. Sources: `E001`, `E003`, `E004`, `E005`, `E006`.

### Intended audience
This document is intended for:
- Maintainers and contributors working on repository-conformant behavior
- Testers verifying supported integrations and platform compatibility
- Integrators configuring external services referenced by the project

### References
- Repository: `mendhak/gpslogger`
- Commit: `ab894229de5ef1fec726b8a9588e98089b9564c6`
- Evidence sources: `E001`, `E002`, `E003`, `E004`, `E005`, `E006`

## 2. Overall Description

### Product perspective
The product is an Android application organized around a GPS logging service and an event bus. When a location is obtained, it is published on the event bus and consumed by multiple fragments. Optional external services require separately provisioned credentials. Sources: `E003`, `E004`.

### Product functions summary
- Obtain location updates and publish them for in-application consumption (`E003`)
- Support optional OpenStreetMap credential-based setup (`E001`, `E004`)
- Support optional Dropbox credential-based setup (`E001`, `E004`)
- Send location data to an OpenGTS endpoint using UDP (`E005`)
- Encode location data as GPRMC/NMEA-style strings for OpenGTS interoperability (`E005`)

### User classes
- End users who run the Android application and configure optional service integrations (`E001`, `E004`)
- Developers who build, import, and debug the Android project (`E002`, `E006`)

### Operating environment
- Android phones version 2.2 and above are stated to have the required Google Play Services framework installed for the referenced feature (`E003`)
- Android emulator should be Android 4.2.2 (API level 17) or greater to use the same feature (`E003`)
- Development environment requires Android SDK components listed in the README (`E002`, `E006`)

### Assumptions and dependencies
- Optional OpenStreetMap integration depends on user-provided consumer key and consumer secret (`E001`, `E004`)
- Optional Dropbox integration depends on user-provided app key and app secret (`E001`, `E004`)
- Some functionality depends on the Google Play Services framework (`E003`)
- Android project import depends on a valid `local.properties` file containing `sdk.dir` if auto-detection does not occur (`E002`, `E006`)

## 3. External Interface Requirements

### User interfaces
Evidence does not describe the full in-app UI. The repository evidence does support:
- Application fragments that consume location events (`E003`)
- External setup steps in OpenStreetMap and Dropbox developer consoles for obtaining credentials (`E001`, `E004`)

### Software/API interfaces
- OpenStreetMap integration via `GPSLOGGER_OSM_CONSUMERKEY` and `GPSLOGGER_OSM_CONSUMERSECRET` configuration values (`E001`, `E004`)
- Dropbox integration via `GPSLOGGER_DROPBOX_APPKEY` and `GPSLOGGER_DROPBOX_APPSECRET` configuration values (`E001`, `E004`)
- Android SDK and Google Play Services dependencies for development/runtime support (`E002`, `E003`, `E006`)
- OpenGTS server interface using server, optional port, and optional path (`E005`)

### Communication interfaces
- UDP transport is used to send OpenGTS messages (`E005`)

### Data exchange formats
- OpenGTS location payloads can be encoded as GPRMC string data, referencing NMEA0183 parsing expectations (`E005`)
- Configuration data is supplied through named key/value entries for external integrations and Android SDK path (`E001`, `E002`, `E004`, `E006`)

## 4. Functional Requirements

| ID | Description | Trigger/Input | System Behavior | Output | Priority | Verification | Source Evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | Publish obtained location updates for in-application consumption. | A location is obtained. | The system shall place the obtained location on the event bus so that consuming fragments can receive it. | A location event available to listening fragments/components. | High | Demonstration | `E003` |
| FR-002 | Accept OpenStreetMap integration credentials. | OpenStreetMap setup is enabled and credentials are provided. | The system shall accept `GPSLOGGER_OSM_CONSUMERKEY` and `GPSLOGGER_OSM_CONSUMERSECRET` as configuration inputs for optional OpenStreetMap integration. | OpenStreetMap credential values are available to the application configuration. | Medium | Inspection | `E001`, `E004` |
| FR-003 | Accept Dropbox integration credentials. | Dropbox setup is enabled and credentials are provided. | The system shall accept `GPSLOGGER_DROPBOX_APPKEY` and `GPSLOGGER_DROPBOX_APPSECRET` as configuration inputs for optional Dropbox integration. | Dropbox credential values are available to the application configuration. | Medium | Inspection | `E001`, `E004` |
| FR-004 | Build an OpenGTS destination URL from configured endpoint parts. | An OpenGTS transmission target is needed. | The system shall construct the destination using the server value and append the port and path when those values are present. | A destination string in the form `server[:port][path]`. | Medium | Test | `E005` |
| FR-005 | Send OpenGTS messages over UDP. | An OpenGTS message, server, and port are available for transmission. | The system shall create a datagram packet addressed to the configured server and port and send the message using UDP. | A UDP packet containing the message is transmitted to the target endpoint. | High | Test | `E005` |
| FR-006 | Encode location data as GPRMC for OpenGTS interoperability. | A serializable location must be prepared for OpenGTS transmission. | The system shall encode the location as GPRMC string data consistent with the referenced NMEA0183 parsing expectation. | A GPRMC-formatted string representation of the location. | High | Test | `E005` |

## 5. Non-Functional Requirements

| ID | Requirement | Quality Attribute | Priority | Verification | Source Evidence | Evidence Type |
|---|---|---|---|---|---|---|
| NFR-001 | For the feature that requires Google Play Services, the system shall be operable on an Android emulator running Android 4.2.2 (API level 17) or greater. | Compatibility | High | Demonstration | `E003` | explicit |
| NFR-002 | For the same feature, the system shall be operable on Android phones version 2.2 and above where the Google Play Services framework is installed as stated in the README. | Compatibility | High | Demonstration | `E003` | explicit |
| NFR-003 | External service credentials shall be supplied through named configuration values rather than embedded directly in runtime messages or endpoint strings. | Maintainability/Security | Medium | Inspection | `E001`, `E004`, `E005` | inferred |

## 6. Data Requirements

| ID | Data Requirement | Type | Description | Verification | Source Evidence | Evidence Type |
|---|---|---|---|---|---|---|
| DR-001 | Location event data | Runtime data | Obtained location data shall be representable as an event that can be placed on the event bus and consumed by fragments. | Demonstration | `E003` | explicit |
| DR-002 | Serializable location data | Runtime data | OpenGTS encoding shall accept a `SerializableLocation` input object for conversion to GPRMC string data. | Test | `E005` | explicit |
| DR-003 | GPRMC message data | Output data | OpenGTS-compatible location output shall be represented as GPRMC string data. | Test | `E005` | explicit |
| DR-004 | Endpoint configuration data | Configuration data | OpenGTS endpoint configuration shall consist of server and may additionally include port and path values. | Inspection | `E005` | explicit |
| DR-005 | External integration credentials | Configuration data | Optional OpenStreetMap and Dropbox integrations shall use named key/secret configuration values as documented. | Inspection | `E001`, `E004` | explicit |
| DR-006 | Android SDK path configuration | Development configuration data | The project shall support a `local.properties` entry named `sdk.dir` for Android SDK location when environment detection does not occur. | Inspection | `E002`, `E006` | explicit |

## 7. Constraints

| ID | Constraint | Type | Verification | Source Evidence |
|---|---|---|---|---|
| C-001 | The development environment shall include Android SDK Build Tools `19.0.3`. | Technology/Build | Inspection | `E002`, `E006` |
| C-002 | The development environment shall include Android Support Repository, Android Support Library, Google Play services, and Google Repository. | Technology/Build | Inspection | `E002`, `E006` |
| C-003 | Use of the Google Play Services-dependent feature requires an emulator running Android 4.2.2 (API level 17) or greater, or a phone environment meeting the stated framework availability. | Platform/Runtime | Demonstration | `E003` |
| C-004 | OpenGTS UDP transmission requires a resolvable server address and port. | Operational/Network | Test | `E005` |

## 8. Verification and Acceptance

| Requirement IDs | Verification Method | Acceptance Basis |
|---|---|---|
| `FR-001`, `DR-001`, `C-003`, `NFR-001`, `NFR-002` | Demonstration | A compatible Android runtime shows that obtained locations are published and available to consuming fragments. |
| `FR-002`, `FR-003`, `DR-004`, `DR-005`, `DR-006`, `C-001`, `C-002`, `NFR-003` | Inspection | Configuration names, supported endpoint fields, and documented platform/build dependencies match the repository evidence. |
| `FR-004`, `FR-005`, `FR-006`, `DR-002`, `DR-003`, `C-004` | Test | Unit or integration tests confirm URL construction, UDP transmission behavior, and GPRMC encoding behavior using representative inputs. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Publish obtained location updates on the event bus for fragment consumption. | Functional | `E003` | explicit | Demonstration | High |
| FR-002 | Accept OpenStreetMap consumer key and consumer secret configuration. | Functional | `E001`, `E004` | explicit | Inspection | High |
| FR-003 | Accept Dropbox app key and app secret configuration. | Functional | `E001`, `E004` | explicit | Inspection | High |
| FR-004 | Construct OpenGTS destination string from server, optional port, and optional path. | Functional | `E005` | explicit | Test | High |
| FR-005 | Send OpenGTS messages using UDP datagrams. | Functional | `E005` | explicit | Test | High |
| FR-006 | Encode location data as GPRMC string data for OpenGTS. | Functional | `E005` | explicit | Test | High |
| NFR-001 | Operate Google Play Services-dependent feature on emulator Android 4.2.2/API 17+. | Non-functional | `E003` | explicit | Demonstration | Medium |
| NFR-002 | Operate Google Play Services-dependent feature on Android 2.2+ phones with framework installed as stated. | Non-functional | `E003` | explicit | Demonstration | Medium |
| NFR-003 | Supply external service credentials through named configuration values. | Non-functional | `E001`, `E004`, `E005` | inferred | Inspection | Medium |
| DR-001 | Represent obtained location data as event-bus data consumable by fragments. | Data | `E003` | explicit | Demonstration | Medium |
| DR-002 | Accept `SerializableLocation` as OpenGTS encoding input. | Data | `E005` | explicit | Test | High |
| DR-003 | Represent OpenGTS output as GPRMC string data. | Data | `E005` | explicit | Test | High |
| DR-004 | Support OpenGTS endpoint data fields: server, optional port, optional path. | Data | `E005` | explicit | Inspection | High |
| DR-005 | Support named configuration data for OpenStreetMap and Dropbox credentials. | Data | `E001`, `E004` | explicit | Inspection | High |
| DR-006 | Support `local.properties` with `sdk.dir` for Android SDK location. | Data | `E002`, `E006` | explicit | Inspection | High |
| C-001 | Require Android SDK Build Tools `19.0.3` in development environment. | Constraint | `E002`, `E006` | explicit | Inspection | High |
| C-002 | Require listed Android support and Google repositories/libraries in development environment. | Constraint | `E002`, `E006` | explicit | Inspection | High |
| C-003 | Constrain Google Play Services-dependent feature to stated Android runtime environments. | Constraint | `E003` | explicit | Demonstration | Medium |
| C-004 | Require resolvable server address and port for OpenGTS UDP transmission. | Constraint | `E005` | explicit | Test | High |
