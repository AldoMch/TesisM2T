# Software Requirements Specification

## 1. Introduction

### 1.1 Purpose
This SRS specifies the repository-supported requirements for a system that distributes Google Cloud Pub/Sub topic messages to web clients over WebSockets using a load-balanced, autoscaled GKE deployment.

### 1.2 Product scope
The product provides infrastructure and runtime behavior to mirror messages from one Pub/Sub topic to clients connected through a single WebSocket endpoint, without requiring those clients to use the Pub/Sub API or SDK. It is intended to run in Google Kubernetes Engine (GKE) behind a load balancer and to scale based on client connections.

### 1.3 Intended audience
- Deployers and operators of the GKE-based adapter
- Integrators connecting web clients to mirrored Pub/Sub topic data
- Reviewers performing deployment and acceptance verification

### 1.4 References
- Repository: GoogleCloudPlatform/gke-pubsub-websocket-adapter
- Repository URL: https://github.com/GoogleCloudPlatform/gke-pubsub-websocket-adapter
- Commit: `575c112acd7b60c40381e4a2fba92905ce828982`
- Primary evidence: `README.md`, `Dockerfile`, `kubernetes/service.yaml`, `kubernetes/configmap.yaml`

## 2. Overall Description

### 2.1 Product perspective
The product is a WebSocket adapter and deployment package that sits between a Google Cloud Pub/Sub topic and browser or other web clients. It creates support infrastructure for a load-balanced, autoscaled GKE cluster that mirrors topic messages to connected clients. A Kubernetes Service exposes the adapter externally.

### 2.2 Product functions summary
- Mirror Pub/Sub topic messages to WebSocket-connected clients
- Expose a single client endpoint for one Pub/Sub topic
- Load balance client traffic across cluster instances
- Autoscale based on the number of connected clients
- Multiplex many client connections while consuming a single subscription per VM
- Serve a cache of the last 10 topic messages to clients

### 2.3 User classes
- Deployment operator with GCP project access and required permissions
- Web client consuming mirrored topic messages over WebSockets

### 2.4 Operating environment
- Google Cloud Platform project with billing enabled
- Google Kubernetes Engine cluster
- Kubernetes Service of type `LoadBalancer`
- Containerized runtime exposing port `8080`, with service port `80/TCP`

### 2.5 Assumptions and dependencies
- The target Pub/Sub topic is readable by the deploying user or service account. (`E002`)
- Deployment requires Pub/Sub subscription creation privileges. (`E002`)
- A topic identifier is provided as configuration. (`E005`)
- The solution depends on Google Cloud Pub/Sub, GKE, Kubernetes Service networking, and WebSocket client connectivity. (`E002`, `E003`, `E004`)

## 3. External Interface Requirements

### 3.1 User interfaces
No graphical user interface is evidenced. The externally visible user-facing interface is a WebSocket endpoint for web clients. (`E002`, `E004`)

### 3.2 Software/API interfaces
| Interface | Description | Source |
|---|---|---|
| Google Cloud Pub/Sub topic | Source of messages to be mirrored to clients | `E002`, `E005` |
| Pub/Sub subscription creation | Required deployment capability for consuming topic data | `E002` |
| Kubernetes ConfigMap | Supplies the topic identifier under key `topic` | `E005` |
| Kubernetes Service | Exposes the application through a load-balanced service | `E003` |

### 3.3 Communication interfaces
| Interface | Requirement-supported detail | Source |
|---|---|---|
| WebSocket client connection | Clients connect through a single endpoint mapped to an individual Pub/Sub topic | `E004` |
| Service network interface | Kubernetes Service shall expose `port: 80`, `protocol: TCP`, `targetPort: 8080` | `E003` |

### 3.4 Data exchange formats
| Data item | Format/detail | Source |
|---|---|---|
| Topic identifier | String in the form shown by example: `projects/pubsub-public-data/topics/taxirides-realtime` | `E005` |
| Mirrored topic messages | Pub/Sub topic messages are forwarded to WebSocket clients; payload format is not specified in evidence | `E002`, `E004` |
| Cached message set | Last 10 published messages are served to clients | `E004`, `E006` |

## 4. Functional Requirements

| ID | Description | Trigger / Input | System behavior | Output | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | Mirror Pub/Sub topic messages to WebSocket clients | Messages are published to the configured Pub/Sub topic and clients are connected | The system shall distribute Pub/Sub topic messages over WebSockets to connected web clients without requiring those clients to use the Pub/Sub SDK or Pub/Sub API | Topic messages delivered to connected WebSocket clients | High | Demonstration | `E002` |
| FR-002 | Provide infrastructure for GKE-based message mirroring | Deployment to a GCP project is initiated | The system shall support operation as a load-balanced, autoscaled GKE cluster that mirrors messages sent to a Pub/Sub topic to WebSocket clients | Running cluster capable of mirroring topic messages | High | Inspection | `E002` |
| FR-003 | Expose a single endpoint per topic | A topic is configured and the service is deployed | The system shall expose a single client endpoint that maps to an individual Pub/Sub topic | One externally reachable endpoint for the configured topic | High | Inspection | `E004`, `E005` |
| FR-004 | Load balance client access | Clients connect to the exposed endpoint | The system shall load balance client connections across VMs in the cluster | Client traffic distributed across cluster instances | Medium | Demonstration | `E004`, `E003` |
| FR-005 | Multiplex multiple clients using one subscription per VM | Multiple clients are connected to the same topic endpoint | The system shall decouple the Pub/Sub subscription from individual WebSocket client connections and multiplex many clients while consuming a single subscription per VM | Multiple clients receive mirrored data without one subscription per client | High | Analysis | `E004` |
| FR-006 | Serve cached recent messages | A client connects when immediate message flow is absent or low | The system shall serve clients a cache of the last 10 messages published to the topic | Client receives up to the last 10 topic messages | Medium | Test | `E004`, `E006` |
| FR-007 | Use configured topic value | Deployment configuration provides a `topic` value | The system shall use the configured topic identifier to determine the Pub/Sub topic associated with the exposed endpoint | Endpoint behavior is bound to the configured topic | High | Inspection | `E005`, `E004` |
| FR-008 | Expose network service ports for client access | The service is deployed | The system shall expose the application through a Kubernetes Service on TCP port 80 forwarding to container port 8080 | Network access path from clients to adapter runtime | High | Inspection | `E003`, `E001` |

## 5. Non-Functional Requirements

| ID | Quality attribute | Requirement | Priority | Verification | Evidence type | Source evidence |
|---|---|---|---|---|---|---|
| NFR-001 | Scalability | The deployed cluster shall scale up and down automatically based on the number of clients connected. | High | Demonstration | explicit | `E004` |
| NFR-002 | Resource efficiency | The system shall support many client connections while consuming only a single Pub/Sub subscription per VM. | High | Analysis | explicit | `E004` |
| NFR-003 | Availability / continuity of displayed data | The system shall provide clients with cached data consisting of the last 10 messages so that meaningful data remains available during periods of low traffic. | Medium | Test | explicit | `E004`, `E006` |
| NFR-004 | Compatibility | The runtime shall be deployable in a container that exposes port 8080 and is fronted by a Kubernetes LoadBalancer service exposing TCP port 80. | Medium | Inspection | explicit | `E001`, `E003` |

## 6. Data Requirements

### 6.1 Data entities or objects
| Data entity | Description | Source |
|---|---|---|
| Pub/Sub topic | Source stream whose messages are mirrored to clients | `E002`, `E005` |
| Topic identifier | Configured string stored as ConfigMap key `topic` | `E005` |
| Topic messages | Published messages forwarded to clients and used for cache population | `E002`, `E004`, `E006` |
| Cached message set | The last 10 messages published to the topic | `E004`, `E006` |

### 6.2 Input/output data
| Direction | Data | Requirement |
|---|---|---|
| Input | Configured topic identifier | The system shall accept a configured topic value for the topic to mirror. (`E005`) |
| Input | Published Pub/Sub messages | The system shall consume messages from the configured topic for forwarding. (`E002`) |
| Output | WebSocket-delivered mirrored messages | The system shall send topic messages to connected web clients. (`E002`, `E004`) |
| Output | Cached recent messages | The system shall provide the last 10 messages to clients. (`E004`, `E006`) |

### 6.3 Storage, integrity, retention
| Requirement | Source |
|---|---|
| The system shall retain a cache of the last 10 messages published to the topic for client delivery. | `E004`, `E006` |

## 7. Constraints

| ID | Constraint | Source |
|---|---|---|
| C-001 | Deployment requires a GCP project with billing enabled. | `E002` |
| C-002 | Deployment requires read access to the topic being mirrored; the topic may reside in a separate project if readable by the deploying user or service account. | `E002` |
| C-003 | Deployment requires Pub/Sub subscription creation privileges. | `E002` |
| C-004 | External service exposure is constrained to a Kubernetes `LoadBalancer` service with TCP port 80 targeting application port 8080. | `E003`, `E001` |
| C-005 | The runtime environment is containerized and based on the provided container behavior exposing port 8080. | `E001` |

## 8. Verification and Acceptance

| Requirement ID | Verification method | Acceptance basis |
|---|---|---|
| FR-001 | Demonstration | Connected web clients receive Pub/Sub topic messages over WebSockets |
| FR-002 | Inspection | Deployment artifacts and documented behavior show load-balanced, autoscaled GKE operation |
| FR-003 | Inspection | Externally exposed single endpoint is mapped to the configured topic |
| FR-004 | Demonstration | Client connections traverse the load-balanced service across cluster instances |
| FR-005 | Analysis | Architecture and runtime behavior show many clients are served from one subscription per VM |
| FR-006 | Test | A new or idle-period client receives cached last 10 messages |
| FR-007 | Inspection | Deployed configuration contains the configured topic and endpoint behavior aligns to it |
| FR-008 | Inspection | Service exposes TCP 80 and forwards to container port 8080 |
| NFR-001 | Demonstration | Scaling behavior changes with connected client count |
| NFR-002 | Analysis | Subscription consumption remains one per VM while serving multiple clients |
| NFR-003 | Test | Cached message behavior remains available during low-traffic periods |
| NFR-004 | Inspection | Deployment uses container port 8080 and LoadBalancer service port 80 |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Mirror Pub/Sub topic messages to WebSocket clients | Functional | `E002` | explicit | Demonstration | High |
| FR-002 | Support load-balanced, autoscaled GKE mirroring deployment | Functional | `E002` | explicit | Inspection | High |
| FR-003 | Expose a single endpoint per configured topic | Functional | `E004`, `E005` | explicit | Inspection | High |
| FR-004 | Load balance client access across cluster VMs | Functional | `E004`, `E003` | explicit | Demonstration | Medium |
| FR-005 | Multiplex many clients using one subscription per VM | Functional | `E004` | explicit | Analysis | High |
| FR-006 | Serve a cache of the last 10 messages | Functional | `E004`, `E006` | explicit | Test | High |
| FR-007 | Use configured topic identifier | Functional | `E005`, `E004` | explicit | Inspection | Medium |
| FR-008 | Expose TCP 80 to target port 8080 | Functional | `E003`, `E001` | explicit | Inspection | High |
| NFR-001 | Autoscale based on connected clients | Non-functional | `E004` | explicit | Demonstration | High |
| NFR-002 | Support many clients with one subscription per VM | Non-functional | `E004` | explicit | Analysis | High |
| NFR-003 | Maintain useful client-visible data via 10-message cache | Non-functional | `E004`, `E006` | explicit | Test | High |
| NFR-004 | Deploy as container plus LoadBalancer service on evidenced ports | Non-functional | `E001`, `E003` | explicit | Inspection | High |
