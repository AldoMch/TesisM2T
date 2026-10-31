# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines the software requirements for the `earth-defender` product, focusing on the observable behavior of its distributed client/server multiplayer game functions and interfaces.

### Product scope
`Earth Defender` is a distributed soft real-time 3D game built with Erlang/OTP and Three.js. The product supports game modes described as single-player and multiplayer, while the detailed behavior specified in this document primarily covers multiplayer room-based play, client/server startup, and the WebSocket-based runtime interface between browser clients and the game server.

### Intended audience
This document is intended for:
- Developers maintaining the game client/server behavior
- Testers verifying multiplayer and connection behavior
- Operators starting the server or replica deployment
- Integrators working with the browser client/server interface

## 2. Overall Description

### Product perspective
The product is a distributed game with separate client and server components. In multiplayer mode:
- The browser client obtains the web server address through DNS/load balancing and downloads static game assets.
- The web server serves static assets such as HTML, CSS, JavaScript, and images.
- The browser client then connects to the Erlang game server through WebSocket over HTTP.
- The server side includes a master/slave structure, with slave or replica nodes used for fault tolerance.
- Browser clients initiate server connections; browser-to-browser peer-to-peer connectivity is not supported by this design.

### Product functions summary
The product supports the following functions:
- Start and run separate client and server components
- Support multiplayer room workflows, including creating and joining a room
- Exchange game and control messages over WebSocket
- Maintain connection liveness using `ping` and `pong` messages
- Reconnect after connection closure
- Re-add the corresponding ship to the scene and continue gameplay flow on `game_reconnect`
- Provide server list information and redirect behavior to clients
- Support a replica server deployment for fault-tolerant purposes

### User classes
- Player: uses the browser client to play the game; documented interaction behavior primarily covers multiplayer room creation and joining
- Room host/player creating a room: initiates a new multiplayer room
- Room participant joining a room: joins an existing multiplayer room
- Server operator: builds, starts, and configures the game server and optional replica

### Operating environment
- Browser-based client environment using Three.js
- Server environment using Erlang/OTP
- Network environment supporting HTTP and WebSocket connectivity between browser client and server

### Assumptions and dependencies
- The browser client initiates WebSocket connections to the server.
- Multiplayer operation depends on server availability at a reachable address and port.
- Fault-tolerant behavior depends on deployment of a separate replica node.

## 3. External Interface Requirements

### User interfaces
The product provides a 3D game client and supports multiplayer user flows for creating a room and joining a room.

### Software/API interfaces
| Interface | Requirement |
|---|---|
| Client-web-server interface | The browser client shall retrieve static game assets from a web server before multiplayer runtime interaction begins. |
| Client-game-server session | The browser client shall communicate with the game server using WebSocket over HTTP. |
| Outbound message format | The client shall encode outbound messages as JSON arrays of the form `[event, data]`. |
| Inbound message format | The client shall parse inbound WebSocket messages as JSON arrays where element `0` is the action and element `1` is optional data. |
| Runtime actions | Supported inbound actions include `game_reconnect`, `room_players_number`, `servers_list`, `servers_list_redirect`, `server_error`, and `pong`. |

### Communication interfaces
| Interface aspect | Requirement |
|---|---|
| Transport | Multiplayer runtime communication shall use WebSocket over HTTP. |
| Directionality | Browser clients shall initiate connections to the server; client-to-client P2P communication is not supported. |
| Liveness | While the connection remains open, the client shall send periodic `ping` messages and process `pong` responses. |

### Data exchange formats
| Data item | Format |
|---|---|
| Outbound client message | JSON array `[event, data]` |
| Inbound server message | JSON array `[action, data?]` |
| Reconnect context | Array containing room ID, player ID, and client or ship index during reconnect flow |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | Multiplayer room workflows | Player selects a multiplayer room workflow | The system shall support multiplayer room-based play, including creating a new room and joining a room. | Player enters a multiplayer room session. | High | Demonstration |
| FR-002 | Multiplayer transport | Client starts a multiplayer session and opens a server connection | The client shall communicate with the server over WebSocket over HTTP for multiplayer operation. | Active client-server communication channel. | High | Test |
| FR-003 | Outbound message serialization | Client sends an event to the server | The client shall serialize each outbound application message as `[event, data]` before transmission. | JSON-formatted outbound message. | High | Inspection |
| FR-004 | Heartbeat ping behavior | The client heartbeat timer expires while the WebSocket is open | While the connection remains open, the client shall send a `ping` message at the 60-second client heartbeat interval, with message data set to `null`, and reset the next heartbeat timer. | Repeated `ping` messages during an active session. | High | Test |
| FR-005 | Reconnection on close | WebSocket close event | When the WebSocket connection closes, the client shall initiate reconnection behavior. After the connection reopens, if existing room and player context is available, the client shall send reconnect context containing room ID, player ID, and index. | Reconnection attempt and reconnect context submission. | High | Test |
| FR-006 | Reconnect gameplay continuation | Inbound message action `game_reconnect` with data | When the client receives a `game_reconnect` action, it shall re-add the corresponding ship to the scene according to the returned data and continue the gameplay flow. | Continued gameplay after reconnect. | High | Test |
| FR-007 | Room player count update | Inbound message action `room_players_number` with data | When the client receives `room_players_number`, it shall update the displayed or tracked player count for the room. | Updated room player count. | Medium | Test |
| FR-008 | Server list update | Inbound message action `servers_list` with data | When the client receives `servers_list`, it shall update its server list from the provided data. | Updated server list. | Medium | Test |
| FR-009 | Redirected server list handling | Inbound message action `servers_list_redirect` with data | When the client receives `servers_list_redirect`, it shall update the server list and then disconnect the current connection. | Refreshed server list and disconnected session. | Medium | Test |
| FR-010 | Server error recovery | Inbound message action `server_error` | When the client receives `server_error`, it shall reload the browser page. | Reloaded client page. | Medium | Demonstration |
| FR-011 | Pong handling | Inbound message action `pong` | The client shall accept `pong` as a heartbeat response without additional gameplay-state handling. | Connection remains active without gameplay changes. | Low | Test |

## 5. Non-Functional Requirements

| ID | Quality attribute | Requirement | Priority | Verification |
|---|---|---|---|---|
| NFR-001 | Real-time behavior | The system shall support soft real-time gameplay behavior. Exact latency bounds are not specified. | High | Analysis |
| NFR-002 | Fault tolerance | The deployment shall support running a replica server for fault-tolerant purposes. | Medium | Demonstration |
| NFR-003 | Availability | The client shall attempt recovery from connection closure by initiating reconnection behavior. | High | Test |
| NFR-004 | Interoperability | Multiplayer communication shall use HTTP and WebSocket protocols between browser client and server. | High | Inspection |
| NFR-005 | Concurrency | The communication mechanism shall support asynchronous communication that can occur concurrently. | Medium | Analysis |

## 6. Data Requirements

| ID | Data entity/object | Requirement |
|---|---|---|
| DR-001 | Outbound message | Outbound client messages shall consist of a JSON array with two positions: event identifier and event data. |
| DR-002 | Inbound message | Inbound server messages shall consist of a JSON array where the first element is the action name and the second element, when present, is action data. |
| DR-003 | Heartbeat data | Heartbeat requests shall use event `ping` with `null` data at a 60-second client heartbeat interval, and the client shall accept `pong` responses. |
| DR-004 | Reconnect context | When the connection reopens and the client already has a room ID and player ID, the client shall send a reconnect context array containing the room ID, player ID, and client or ship index to restore the multiplayer room session. |
| DR-005 | Server list data | The system shall exchange server list data in messages for `servers_list` and `servers_list_redirect`. |
| DR-006 | Room player count | The system shall exchange room player count data in `room_players_number` messages. |

## 7. System Constraints

| ID | Constraint |
|---|---|
| C-001 | The product is constrained to a distributed architecture with separate browser client, web server, and game server roles. |
| C-002 | Multiplayer browser communication is constrained to WebSocket over HTTP. |
| C-003 | Browser clients cannot accept inbound WebSocket connections; therefore client-to-client P2P communication is not supported. |
| C-004 | The implementation technologies are constrained to Erlang/OTP for the server side and Three.js for the client side. |
| C-005 | The server-side multiplayer topology includes master and replica roles for fault-tolerant deployment. |

## 8. Verification and Acceptance Criteria

| Requirement ID | Verification method | Acceptance criterion |
|---|---|---|
| FR-001 | Demonstration | A tester can create a room and join a room using the multiplayer flows. |
| FR-002 | Test | A browser client successfully exchanges messages with the server over WebSocket over HTTP. |
| FR-003 | Inspection | Outbound client messages are serialized as JSON arrays `[event, data]`. |
| FR-004 | Test | During an active session, `ping` messages with `null` data are sent every 60 seconds while the WebSocket remains open. |
| FR-005 | Test | Closing the WebSocket causes the client to initiate reconnection behavior; after the connection reopens, if room and player context already exist, the client sends reconnect context containing room ID, player ID, and index. |
| FR-006 | Test | After receiving `game_reconnect`, the client re-adds the corresponding ship to the scene and continues the gameplay flow. |
| FR-007 | Test | Receiving `room_players_number` updates the room player count used by the client. |
| FR-008 | Test | Receiving `servers_list` updates the server list. |
| FR-009 | Test | Receiving `servers_list_redirect` updates the server list and disconnects the current session. |
| FR-010 | Demonstration | Receiving `server_error` causes the client page to reload. |
| FR-011 | Test | Receiving `pong` does not alter gameplay state and does not fail the session. |
| NFR-001 | Analysis | The product is defined and implemented as a soft real-time game system. |
| NFR-002 | Demonstration | A replica server can be run for fault-tolerant purposes. |
| NFR-003 | Test | Connection closure leads to a reconnect attempt. |
| NFR-004 | Inspection | The documented communication protocols are HTTP and WebSocket. |
| NFR-005 | Analysis | The architecture supports asynchronous communication that can occur concurrently. |
