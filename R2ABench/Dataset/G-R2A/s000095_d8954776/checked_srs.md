# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines the software requirements for the `mendhak/gpslogger` repository at commit `ab894229de5ef1fec726b8a9588e98089b9564c6`. It describes supported behavior, interfaces, data handling, and operational constraints for the Android GPS logging application and its documented integrations.

### Product scope
GPSLogger is an Android-based GPS logging application and service. It acquires location updates, records GPS information to user-enabled log outputs, distributes location and status information within the application, and supports optional external integrations including OpenStreetMap, Dropbox, and OpenGTS. The repository also includes Android build and import setup and functionality that depends on Google Play Services for at least one feature.

### Intended audience
This document is intended for:
- Maintainers and contributors implementing or modifying GPSLogger behavior
- Test engineers validating logging, integration, and platform compatibility behavior
- Integrators configuring supported external services

### References
- Repository: `mendhak/gpslogger`
- Commit: `ab894229de5ef1fec726b8a9588e98089b9564c6`

## 2. Overall Description

### Product perspective
The product is an Android application composed of several main components including an event bus, a GPS logging service, location listeners, loggers, uploaders or upload jobs, main activity or fragments, and session or application settings components. The GPS logging service is responsible for location handling and logging-related processing, while fragments consume published location changes for display and in-application behavior. Optional external services require separately provisioned credentials.

### Product functions summary
The product shall support the following functions:
- Acquire location updates and publish them for in-application consumption
- Record GPS location information to enabled log output formats, including GPX, KML, and text files
- Support optional OpenStreetMap credential-based setup
- Support optional Dropbox credential-based setup
- Send OpenGTS messages to a configured endpoint using UDP
- Encode location data as GPRMC string data for OpenGTS interoperability

### User classes
- End users who run the Android application and enable or configure logging and optional service integrations
- Developers who build, import, and debug the Android project

### Operating environment
- Android phones version 2.2 and above for the documented Google Play Services-dependent feature, where the Google Play Services framework is installed
- Android emulator version 4.2.2 (API level 17) or greater for the same feature
- Android development environment with the SDK components required by the project setup

### Assumptions and dependencies
- Optional OpenStreetMap integration depends on user-provided consumer key and consumer secret
- Optional Dropbox integration depends on user-provided app key and app secret
- Some functionality depends on Google Play Services
- Android project import may require a valid `local.properties` file containing `sdk.dir`
- OpenGTS integration depends on configured server, port, communication method, and device identifier values

## 3. External Interface Requirements

### User interfaces
The repository supports the following user-facing or configuration-facing interfaces:
- Application fragments that consume published location events
- Configuration steps for obtaining OpenStreetMap and Dropbox credentials through their respective developer services
- Project setup files used during Android development and build

### Software/API interfaces
- OpenStreetMap integration shall use configuration entries `GPSLOGGER_OSM_CONSUMERKEY` and `GPSLOGGER_OSM_CONSUMERSECRET`
- Dropbox integration shall use configuration entries `GPSLOGGER_DROPBOX_APPKEY` and `GPSLOGGER_DROPBOX_APPSECRET`
- OpenStreetMap and Dropbox credentials shall be supplied through documented Gradle configuration entries and injected into application configuration at build time
- The application shall use Android SDK and Google Play Services dependencies required by the project
- OpenGTS integration shall use a configured server, port, communication method, device identifier, and optional path

### Communication interfaces
- OpenGTS message transmission shall use UDP when the configured communication method is UDP

### Data exchange formats
- OpenGTS location payloads shall be encoded as GPRMC string data
- External integration credentials shall be provided as named Gradle properties
- Development configuration may include Android SDK path data through `local.properties`

## 4. Functional Requirements

| ID | Description | Trigger/Input | System Behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | Publish obtained location updates for in-application consumption | A location is obtained | The system shall place the obtained location on the event bus so that consuming fragments can receive it | A location event is available to listening fragments or components | High | Demonstration |
| FR-002 | Accept OpenStreetMap integration credentials | OpenStreetMap setup is enabled and credentials are provided | The system shall accept `GPSLOGGER_OSM_CONSUMERKEY` and `GPSLOGGER_OSM_CONSUMERSECRET` from the documented Gradle properties file and generate OpenStreetMap configuration values available to the application at build time | OpenStreetMap credential values are incorporated into application configuration | Medium | Inspection |
| FR-003 | Accept Dropbox integration credentials | Dropbox setup is enabled and credentials are provided | The system shall accept `GPSLOGGER_DROPBOX_APPKEY` and `GPSLOGGER_DROPBOX_APPSECRET` from the documented Gradle properties file and generate Dropbox configuration values available to the application at build time | Dropbox credential values are incorporated into application configuration | Medium | Inspection |
| FR-004 | Construct OpenGTS transmission configuration | An OpenGTS transmission target is needed | The system shall use server, port, communication method, device identifier, and optional path to construct the OpenGTS transmission configuration | An OpenGTS transmission target configuration is available for message sending | Medium | Inspection |
| FR-005 | Send OpenGTS messages over UDP | The OpenGTS communication method is UDP and a message is available for transmission | The system shall package the account, device, and GPRMC message data as a UDP datagram and send it to the configured server and resolvable port | A UDP packet containing the OpenGTS message is transmitted to the target endpoint | High | Test |
| FR-006 | Encode location data as GPRMC for OpenGTS interoperability | A serializable location must be prepared for OpenGTS transmission | The system shall encode a serializable location as a GPRMC string with fields including the `$GPRMC` prefix, UTC time, valid status, latitude, north/south hemisphere, longitude, east/west hemisphere, speed in knots, heading, UTC date, and an appended NMEA checksum | A GPRMC-formatted string representation of the location | High | Test |
| FR-007 | Log GPS location information to enabled output formats | A logging session is active and valid locations are acquired | The system shall acquire valid locations and write them to enabled log outputs according to user configuration, including at least GPX, KML, and text-file outputs | Logged GPS location records are written to the enabled output formats | High | Demonstration |

## 5. Non-Functional Requirements

| ID | Quality Attribute | Requirement | Priority | Verification |
|---|---|---|---|---|
| NFR-001 | Compatibility | For the feature that requires Google Play Services, the system shall be operable on an Android emulator running Android 4.2.2 (API level 17) or greater | High | Demonstration |
| NFR-002 | Compatibility | For the same feature, the system shall be operable on Android phones version 2.2 and above where the Google Play Services framework is installed | High | Demonstration |
| NFR-003 | Configurability | OpenStreetMap and Dropbox external service credentials shall be supplied through named Gradle configuration entries documented by the project and injected into application configuration at build time | Medium | Inspection |

## 6. Data Requirements

| ID | Data item/entity | Requirement | Verification |
|---|---|---|---|
| DR-001 | Location event data | Obtained location data shall be representable as an event that can be placed on the event bus and consumed by fragments | Demonstration |
| DR-002 | Serializable location data | OpenGTS encoding shall accept a `SerializableLocation` input object for conversion to GPRMC string data | Test |
| DR-003 | GPRMC message data | OpenGTS-compatible location output shall be represented as a GPRMC string containing the required prefix, comma-delimited fields, UTC time and date values, speed converted to knots, and a trailing checksum | Test |
| DR-004 | OpenGTS transmission configuration | OpenGTS endpoint configuration shall include server, port, communication method, and device identifier, and may additionally include a path | Inspection |
| DR-005 | External integration credentials | Credentials for optional OpenStreetMap and Dropbox integrations shall be stored as named Gradle properties in `~/.gradle/gradle.properties` and mapped to build-generated application configuration values | Inspection |
| DR-006 | Android SDK path configuration | The project shall support a `local.properties` entry named `sdk.dir` for Android SDK location when environment detection does not occur | Inspection |

## 7. System Constraints

| ID | Constraint | Verification |
|---|---|---|
| C-001 | The development environment shall include Android SDK Build Tools `19.0.3` | Inspection |
| C-002 | The development environment shall include Android Support Repository, Android Support Library, Google Play services, and Google Repository | Inspection |
| C-003 | Use of the Google Play Services-dependent feature requires an emulator running Android 4.2.2 (API level 17) or greater, or a phone environment with the required framework installed | Demonstration |
| C-004 | OpenGTS transmission requires server, port, communication method, and device identifier to be configured; path is optional | Inspection |

## 8. Verification and Acceptance Criteria

| Requirement ID | Verification method | Acceptance criterion |
|---|---|---|
| FR-001 | Demonstration | In a compatible Android runtime, when a location is obtained it is published on the event bus and can be received by consuming fragments or components. |
| FR-002 | Inspection | Project configuration and build logic show `GPSLOGGER_OSM_CONSUMERKEY` and `GPSLOGGER_OSM_CONSUMERSECRET` being read from the documented Gradle properties source and mapped into application configuration. |
| FR-003 | Inspection | Project configuration and build logic show `GPSLOGGER_DROPBOX_APPKEY` and `GPSLOGGER_DROPBOX_APPSECRET` being read from the documented Gradle properties source and mapped into application configuration. |
| FR-004 | Inspection | The OpenGTS configuration logic uses server, port, communication method, and device identifier as required inputs and supports an optional path value. |
| FR-005 | Test | With UDP selected and valid server and port configuration present, the system sends a UDP datagram containing the OpenGTS message to the configured endpoint. |
| FR-006 | Test | A test confirms that output begins with `$GPRMC`, contains the expected comma-delimited fields, represents time and date in UTC, converts speed from meters per second to knots, and ends with `*` followed by a two-character checksum. |
| FR-007 | Demonstration | During an active logging session, valid acquired locations are written to enabled user-configured outputs including GPX, KML, and text-file outputs. |
| NFR-001 | Demonstration | The Google Play Services-dependent feature operates on an Android emulator running version 4.2.2 (API level 17) or greater. |
| NFR-002 | Demonstration | The Google Play Services-dependent feature operates on Android phones version 2.2 and above when the required framework is installed. |
| NFR-003 | Inspection | Project documentation and build configuration show OpenStreetMap and Dropbox credentials supplied through named Gradle configuration entries and injected into application configuration at build time. |
| DR-001 | Demonstration | Location data can be represented and observed as an event consumed by application fragments. |
| DR-002 | Test | GPRMC encoding accepts a `SerializableLocation` instance and produces string output. |
| DR-003 | Test | Generated GPRMC data includes the required structure, UTC time and date, knot-based speed value, and checksum. |
| DR-004 | Inspection | OpenGTS configuration supports required server, port, communication method, and device identifier values, with optional path support. |
| DR-005 | Inspection | OpenStreetMap and Dropbox credentials are defined as named properties in `~/.gradle/gradle.properties` and mapped into generated application configuration. |
| DR-006 | Inspection | The build/import process supports `local.properties` with `sdk.dir` for Android SDK location. |
| C-001 | Inspection | Development setup documentation specifies Android SDK Build Tools `19.0.3`. |
| C-002 | Inspection | Development setup documentation specifies the listed Android support and Google repositories or libraries. |
| C-003 | Demonstration | The constrained feature operates only in the documented compatible emulator or phone environments. |
| C-004 | Inspection | OpenGTS configuration validation requires server, port, communication method, and device identifier, while treating path as optional. |
