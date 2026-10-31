# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines evidence-backed requirements for the `earth-defender` product at commit `5d4d8f0832fc74882a701d6a0dedee23fd494648`, focusing on the observable behavior of its distributed client/server multiplayer game functions and interfaces.

### Product scope
`Earth Defender` is a distributed soft real-time 3D game built with Erlang/OTP and Three.js and supports single-player and multiplayer play. The available evidence primarily describes multiplayer room-based play, client/server startup, and the WebSocket-based runtime interface between browser clients and the game server. [E001][E002]

### Intended audience
This document is intended for:
- Developers maintaining the game client/server behavior
- Testers verifying multiplayer and connection behavior
- Operators starting the server or fault-tolerant replica
- Integrators working with the browser client/server interface

### References
- Repository: `alexprut/earth-defender`
- Repository URL: <https://github.com/alexprut/earth-defender>
- Snapshot: <https://github.com/alexprut/earth-defender/tree/5d4d8f0832fc74882a701d6a0dedee23fd494648>
- Primary evidence: `README.md`, `client/js/gameClient.js` [E001][E002][E003][E004][E005][E006]

## 2. Overall Description

### Product perspective
The product is a distributed game with separate client and server components. In multiplayer mode, communication uses WebSocket over HTTP between browser clients and the server. Browser clients initiate server connections; browser-to-browser peer-to-peer connectivity is not supported by this design. [E001][E002]

### Product functions summary
The evidence supports the following product functions:
- Start and run separate client and server components [E001]
- Support multiplayer room workflows, including creating and joining a room [E001]
- Exchange game and control messages over WebSocket [E002][E003][E004]
- Maintain connection liveness using `ping`/`pong` messages [E003][E006]
- Reconnect after connection closure and resume game state on `game_reconnect` [E004]
- Provide server list information and redirect behavior to clients [E006]
- Support a slave/replica server deployment for fault-tolerant purposes [E002]

### User classes
- Player: uses the browser client to play the game in single-player or multiplayer modes [E001]
- Room host/player creating a room: initiates a new multiplayer room [E001]
- Room participant joining a room: joins an existing multiplayer room [E001]
- Server operator: builds, starts, and configures the game server and optional slave/replica [E001][E002]

### Operating environment
- Browser-based client environment using Three.js [E001]
- Server environment using Erlang/OTP [E001]
- Network environment supporting HTTP and WebSocket connectivity between browser client and server [E002]

### Assumptions and dependencies
- The browser client can initiate, but not accept, WebSocket connections. [E002]
- Multiplayer operation depends on server availability at a configured address and port. [E002]
- Fault-tolerant replica behavior depends on a separate slave/replica deployment. [E002]

## 3. External Interface Requirements

### User interfaces
The product provides a 3D game client and supports multiplayer user flows for creating a room and joining a room. Detailed screen layouts are not supported by the available evidence. [E001]

### Software/API interfaces
| Interface | Requirement |
|---|---|
| Client-server session | The browser client shall communicate with the game server using WebSocket over HTTP. [E002] |
| Outbound message format | The client shall encode outbound messages as JSON arrays of the form `[event, data]`. [E003] |
| Inbound message format | The client shall parse inbound WebSocket messages as JSON arrays where element `0` is the action and element `1` is optional data. [E004][E005] |
| Runtime actions | Supported inbound actions evidenced in the client include `game_reconnect`, `room_players_number`, `servers_list`, `servers_list_redirect`, `server_error`, and `pong`. [E004][E006] |

### Communication interfaces
| Interface aspect | Requirement |
|---|---|
| Transport | Communication shall use WebSocket running over HTTP. [E002] |
| Directionality | Browser clients shall initiate connections to the server; client-to-client P2P communication is not supported in the documented architecture. [E002] |
| Liveness | The client shall send periodic `ping` messages while connected and process `pong` responses. [E003][E006] |

### Data exchange formats
| Data | Format | Evidence |
|---|---|---|
| Outbound client message | JSON array `[event, data]` | [E003] |
| Inbound server message | JSON array `[action, data?]` | [E004][E005] |
| Reconnect context | Array including room ID, player ID, and an index during reconnect flow | [E004][E005] |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | The system shall support multiplayer room-based play, including creating a new room and joining a room. | Player selects a multiplayer room workflow. | The system enables the documented room creation and room joining use cases. | Player enters a multiplayer room session. | High | Demonstration | [E001] |
| FR-002 | The client shall communicate with the server over WebSocket over HTTP for multiplayer operation. | Client starts a multiplayer session and opens a server connection. | The client establishes asynchronous communication with the server using WebSocket over HTTP. | Active client-server communication channel. | High | Test | [E002] |
| FR-003 | The client shall encode each outbound application message as a JSON array containing an event name and associated data. | Client sends an event to the server. | The client serializes the message as `[event, data]` before transmission. | JSON-formatted outbound message. | High | Inspection | [E003] |
| FR-004 | While connected, the client shall maintain connection liveness by sending `ping` messages at the heartbeat interval. | Heartbeat timer expires while the WebSocket is open. | The client sends `ping` with `null` data and restarts the heartbeat timer. | Repeated `ping` messages during an active session. | High | Test | [E003] |
| FR-005 | When the WebSocket connection closes, the client shall initiate reconnection behavior. | WebSocket close event. | The client invokes its reconnect flow after closure. | Reconnection attempt. | High | Test | [E004] |
| FR-006 | When the client receives a `game_reconnect` action, it shall restore the ship in the scene and restart the game. | Inbound message action `game_reconnect` with data. | The client re-adds the ship from the provided data and starts the game. | Resumed gameplay after reconnect. | High | Test | [E004] |
| FR-007 | When the client receives `room_players_number`, it shall update the displayed or tracked player count for the room. | Inbound message action `room_players_number` with data. | The client applies the received player-count data to the game state. | Updated room player count. | Medium | Test | [E004] |
| FR-008 | When the client receives `servers_list`, it shall update its server list from the provided data. | Inbound message action `servers_list` with data. | The client stores or applies the server list data. | Updated server list. | Medium | Test | [E006] |
| FR-009 | When the client receives `servers_list_redirect`, it shall update the server list and then disconnect the current connection. | Inbound message action `servers_list_redirect` with data. | The client updates the server list and closes the current WebSocket connection. | Refreshed server list and disconnected session. | Medium | Test | [E006] |
| FR-010 | When the client receives `server_error`, it shall reload the browser page. | Inbound message action `server_error`. | The client triggers a page reload. | Reloaded client page. | Medium | Demonstration | [E006] |
| FR-011 | The client shall ignore `pong` as a non-state-changing heartbeat response. | Inbound message action `pong`. | The client accepts the response without additional game-state handling. | Connection remains active without gameplay changes. | Low | Test | [E006] |

## 5. Non-Functional Requirements

| ID | Quality attribute | Requirement | Priority | Verification | Source evidence | Evidence type |
|---|---|---|---|---|---|---|
| NFR-001 | Real-time behavior | The system shall support soft real-time gameplay behavior. Exact latency bounds are not specified in the evidence. | High | Analysis | [E001] | explicit |
| NFR-002 | Fault tolerance | The deployment shall support running a slave/replica server for fault-tolerant purposes. | Medium | Demonstration | [E002] | explicit |
| NFR-003 | Availability | The client shall attempt to recover from connection closure by initiating reconnection behavior. | High | Test | [E004] | inferred |
| NFR-004 | Interoperability | Multiplayer communication shall use standards-based HTTP and WebSocket protocols between browser client and server. | High | Inspection | [E002] | explicit |
| NFR-005 | Concurrency | The communication mechanism shall support asynchronous communication that can occur concurrently. | Medium | Analysis | [E002] | explicit |

## 6. Data Requirements

| ID | Data entity/object | Requirement | Source evidence |
|---|---|---|---|
| DR-001 | Outbound message | Outbound client messages shall consist of a JSON array with two positions: event identifier and event data. | [E003] |
| DR-002 | Inbound message | Inbound server messages shall consist of a JSON array where the first element is the action name and the second element, when present, is action data. | [E004][E005] |
| DR-003 | Heartbeat data | Heartbeat requests shall use event `ping` with `null` data, and the client shall accept `pong` responses. | [E003][E006] |
| DR-004 | Reconnect context | Reconnect-related data shall include room ID, player ID, and an index in the reconnect flow supported by the client. | [E004][E005] |
| DR-005 | Server list data | The system shall exchange server list data in messages for `servers_list` and `servers_list_redirect`. | [E006] |
| DR-006 | Room player count | The system shall exchange room player count data in `room_players_number` messages. | [E004] |

## 7. Constraints

| ID | Constraint | Source evidence |
|---|---|---|
| C-001 | The product is constrained to a distributed client/server architecture with separate client and server setup/start procedures. | [E001] |
| C-002 | Multiplayer browser communication is constrained to WebSocket over HTTP. | [E002] |
| C-003 | Browser clients cannot accept inbound WebSocket connections; therefore client-to-client P2P communication is not supported in the documented architecture. | [E002] |
| C-004 | The implementation technologies evidenced are Erlang/OTP for the server side and Three.js for the client side. | [E001] |

## 8. Verification and Acceptance

| Requirement ID | Verification method | Acceptance basis |
|---|---|---|
| FR-001 | Demonstration | A tester can create a room and join a room using the multiplayer flows. |
| FR-002 | Test | A browser client successfully exchanges messages with the server over WebSocket over HTTP. |
| FR-003 | Inspection | Outbound client messages are serialized as JSON arrays `[event, data]`. |
| FR-004 | Test | During an active session, `ping` messages are sent repeatedly at the configured heartbeat interval. |
| FR-005 | Test | Closing the WebSocket causes the client to initiate reconnection behavior. |
| FR-006 | Test | Receiving `game_reconnect` restores the ship and restarts gameplay. |
| FR-007 | Test | Receiving `room_players_number` updates the room player count. |
| FR-008 | Test | Receiving `servers_list` updates the server list. |
| FR-009 | Test | Receiving `servers_list_redirect` updates the server list and disconnects the current session. |
| FR-010 | Demonstration | Receiving `server_error` causes the client page to reload. |
| FR-011 | Test | Receiving `pong` does not alter gameplay state and does not fail the session. |
| NFR-001 | Analysis | Product evidence identifies the game as soft real-time. |
| NFR-002 | Demonstration | A slave/replica server can be run for fault-tolerant purposes. |
| NFR-003 | Test | Connection closure leads to a reconnect attempt. |
| NFR-004 | Inspection | The documented communication protocols are HTTP and WebSocket. |
| NFR-005 | Analysis | The architecture description identifies asynchronous concurrent communication support. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Support room creation and room joining for multiplayer | Functional | E001 | explicit | Demonstration | High |
| FR-002 | Use WebSocket over HTTP for multiplayer client-server communication | Functional | E002 | explicit | Test | High |
| FR-003 | Serialize outbound messages as `[event, data]` JSON arrays | Functional | E003 | explicit | Inspection | High |
| FR-004 | Send periodic `ping` heartbeats while connected | Functional | E003 | explicit | Test | High |
| FR-005 | Reconnect on WebSocket close | Functional | E004 | explicit | Test | High |
| FR-006 | Restore ship and restart game on `game_reconnect` | Functional | E004 | explicit | Test | High |
| FR-007 | Update room player count on `room_players_number` | Functional | E004 | explicit | Test | High |
| FR-008 | Update server list on `servers_list` | Functional | E006 | explicit | Test | High |
| FR-009 | Update server list and disconnect on `servers_list_redirect` | Functional | E006 | explicit | Test | High |
| FR-010 | Reload page on `server_error` | Functional | E006 | explicit | Demonstration | High |
| FR-011 | Accept `pong` as heartbeat response without extra handling | Functional | E006 | explicit | Test | Medium |
| NFR-001 | Support soft real-time gameplay behavior | Non-functional | E001 | explicit | Analysis | Medium |
| NFR-002 | Support slave/replica deployment for fault tolerance | Non-functional | E002 | explicit | Demonstration | High |
| NFR-003 | Attempt recovery after connection closure | Non-functional | E004 | inferred | Test | Medium |
| NFR-004 | Interoperate through HTTP and WebSocket | Non-functional | E002 | explicit | Inspection | High |
| NFR-005 | Support asynchronous concurrent communication | Non-functional | E002 | explicit | Analysis | Medium |
