# Checked Software Requirements Specification: GKE Pub/Sub WebSocket Adapter

## 1. Introduction

### 1.1 Purpose

This Software Requirements Specification defines the checked requirements for a Google Kubernetes Engine deployment that distributes Google Cloud Pub/Sub topic messages to web clients over WebSockets.

The document is prepared for architecture view generation and omits review notes, provenance fields, and supporting-material identifiers.

### 1.2 Product Scope

The product is a WebSocket adapter and deployment package that:

- Mirrors messages from a configured Google Cloud Pub/Sub topic to connected WebSocket clients.
- Lets web clients receive topic data without directly using the Pub/Sub API or SDK.
- Runs as a containerized runtime in Google Kubernetes Engine.
- Exposes the adapter through a Kubernetes `LoadBalancer` service.
- Uses a Kubernetes ConfigMap value to bind a deployment instance to one Pub/Sub topic.
- Uses a `websocketd` bridge with a Node.js `pulltop` process to serve topic data to clients.
- Supports horizontal pod autoscaling through Kubernetes autoscaling configuration.

Each deployment instance binds one externally reachable WebSocket endpoint to one configured Pub/Sub topic. Multiple topics shall be served by multiple independently configured deployment instances.

### 1.3 Intended Audience

The intended audience includes deployment operators, Kubernetes operators, GCP project administrators, web-client integrators, testers, and architecture evaluators.

### 1.4 Definitions and Abbreviations

- GCP: Google Cloud Platform.
- GKE: Google Kubernetes Engine.
- HPA: Horizontal Pod Autoscaler.
- Pub/Sub: Google Cloud Pub/Sub.
- SRS: Software Requirements Specification.
- VM: Virtual machine.
- WebSocket: Full-duplex network communication protocol used by connected clients.

## 2. Overall Description

### 2.1 Product Perspective

The product sits between a configured Pub/Sub topic and browser or other web clients. A Kubernetes `LoadBalancer` service exposes a single client endpoint for one configured topic. Runtime instances consume messages from the configured topic and forward them to connected clients through WebSockets.

The runtime is composed of:

- A topic configuration value stored as a Kubernetes ConfigMap item.
- A `SYMBOL` environment variable injected into the adapter container from the configured topic value.
- An `exec.sh` entrypoint that passes the runtime topic parameter to `pulltop`.
- A Node.js `pulltop` process that pulls topic data and writes runtime output.
- `websocketd` listening on port `8080` and streaming the runtime output to WebSocket clients.

### 2.2 Product Functions

The product shall provide the following high-level functions:

- Mirror configured Pub/Sub topic messages to connected WebSocket clients.
- Expose one WebSocket endpoint for each configured deployment instance.
- Bind the endpoint to one configured Pub/Sub topic.
- Load balance client connections through Kubernetes service networking.
- Decouple Pub/Sub subscription usage from individual client WebSocket connections.
- Multiplex many client connections while consuming one Pub/Sub subscription per running instance.
- Serve a cache of the last 10 topic messages.
- Provide Kubernetes autoscaling configuration for the adapter deployment.

### 2.3 User Classes

- Deployment operators configure and deploy the adapter.
- Kubernetes operators inspect service, deployment, and autoscaling behavior.
- GCP project administrators provide billing, topic access, and subscription creation permissions.
- Web clients consume mirrored topic data through WebSocket connections.
- Testers verify endpoint behavior, runtime configuration, scaling configuration, and cached-message delivery.

### 2.4 Operating Environment

The product shall operate in a GCP project with billing enabled and a GKE cluster available. It shall run as a containerized workload exposed through a Kubernetes `LoadBalancer` service using TCP port `80` and adapter port `8080`.

The deployment shall include a Kubernetes ConfigMap for the topic identifier, a Kubernetes Deployment for adapter pods, a Kubernetes Service for external access, and an HPA for horizontal scaling of the Deployment.

### 2.5 Assumptions and Dependencies

- The configured Pub/Sub topic is readable by the deploying user or service account.
- The deployment identity can create Pub/Sub subscriptions.
- The configured topic value is injected into the runtime as the `SYMBOL` environment variable.
- Web clients can establish WebSocket connections to the exposed endpoint.
- Horizontal scaling by connected-client count is not assumed unless an explicit connection-count metric path is configured.

## 3. External Interface Requirements

### 3.1 User Interface Requirements

#### UI-001 WebSocket Endpoint

The externally visible client interface shall be a WebSocket endpoint exposed through the Kubernetes `LoadBalancer` service.

### 3.2 Software Interface Requirements

#### SI-001 Pub/Sub Topic Interface

The adapter shall consume messages from the configured Pub/Sub topic.

#### SI-002 Pub/Sub Subscription Interface

The adapter shall use Pub/Sub subscription behavior to receive topic messages.

#### SI-003 Kubernetes ConfigMap Interface

The deployment shall accept a topic identifier through a Kubernetes ConfigMap item named `topic`.

#### SI-004 Runtime Topic Parameter Interface

The deployment shall inject the configured topic value into the adapter container as the `SYMBOL` environment variable.

#### SI-005 Kubernetes Service Interface

The deployment shall expose the adapter using a Kubernetes `LoadBalancer` service.

#### SI-006 Kubernetes Autoscaling Interface

The deployment shall include an HPA targeting the adapter Deployment.

### 3.3 Communication Interface Requirements

#### CI-001 Client WebSocket Communication

Web clients shall connect to the adapter through the exposed WebSocket endpoint.

#### CI-002 Service Port Mapping

The Kubernetes service shall expose TCP port `80` and forward traffic to adapter port `8080`.

#### CI-003 Pub/Sub Message Flow

The adapter runtime shall receive configured topic messages through the `pulltop` process and stream output through `websocketd`.

### 3.4 Data Exchange Formats

#### DI-001 Topic Identifier

The topic identifier shall be represented as a string, such as `projects/<project-id>/topics/<topic-name>`.

#### DI-002 Topic Message Payload

The adapter shall forward Pub/Sub topic messages to WebSocket clients. This SRS does not specify the payload schema.

#### DI-003 Cached Message Set

The adapter shall retain and provide up to the last 10 published topic messages to clients.

## 4. Functional Requirements

### FR-001 Mirror Pub/Sub Messages to WebSocket Clients

The adapter shall distribute messages from the configured Pub/Sub topic to connected WebSocket clients without requiring those clients to use the Pub/Sub API or SDK.

**Priority:** High

**Verification:** Demonstration.

**Acceptance Criteria:**

- A client can connect to the exposed WebSocket endpoint.
- A message published to the configured topic is delivered to connected clients.
- The client does not need direct Pub/Sub API or SDK access.

### FR-002 Provide Containerized WebSocket Bridge Runtime

The adapter runtime shall compose `pulltop` and `websocketd`, invoked through `exec.sh` with the runtime topic parameter.

**Priority:** High

**Verification:** Inspection and runtime demonstration.

**Acceptance Criteria:**

- The container entrypoint invokes `exec.sh` with the `SYMBOL` runtime parameter.
- `exec.sh` starts the Node.js `pulltop` process with the provided parameter.
- `websocketd` listens on port `8080` and streams runtime output to clients.

### FR-003 Bind One Deployment Endpoint to One Topic

Each deployment instance shall expose one client endpoint and bind that endpoint to one configured Pub/Sub topic.

**Priority:** High

**Verification:** Inspection.

**Acceptance Criteria:**

- The deployment has one configured topic value.
- The exposed endpoint is associated with that configured topic value.
- Multiple topics require multiple independently configured deployment instances.

### FR-004 Inject Configured Topic into Runtime

The deployment shall map the Kubernetes ConfigMap item `topic` into the adapter container as the `SYMBOL` environment variable.

**Priority:** High

**Verification:** Inspection.

**Acceptance Criteria:**

- The ConfigMap contains a `topic` item.
- The Deployment maps the ConfigMap item into `SYMBOL`.
- The runtime entrypoint receives `SYMBOL` as the topic parameter.

### FR-005 Expose Adapter Through Load-Balanced Service

The deployment shall expose the adapter through a Kubernetes `LoadBalancer` service.

**Priority:** High

**Verification:** Inspection and demonstration.

**Acceptance Criteria:**

- The service type is `LoadBalancer`.
- The service exposes TCP port `80`.
- The service forwards to adapter port `8080`.
- Clients can reach the adapter through the exposed service endpoint.

### FR-006 Load Balance Client Connections

The Kubernetes service shall distribute client connections across running adapter instances selected by the service.

**Priority:** Medium

**Verification:** Demonstration.

**Acceptance Criteria:**

- Multiple adapter instances can be selected by the service.
- Client traffic is routed through the service to running adapter instances.

### FR-007 Multiplex Clients with One Subscription per Instance

The adapter shall decouple Pub/Sub subscription usage from individual WebSocket client connections and shall support many clients while consuming one Pub/Sub subscription per running VM or pod instance.

**Priority:** High

**Verification:** Inspection, test, and analysis.

**Acceptance Criteria:**

- With `N` running adapter instances and `M` connected clients, subscription consumption scales with `N`, not `M`.
- Pub/Sub subscription listings or adapter subscription-management records can be inspected to verify the subscription count.
- Increasing client count alone does not create one Pub/Sub subscription per client.

### FR-008 Serve Cached Recent Messages

The adapter shall serve connected clients a cache containing up to the last 10 messages published to the configured topic.

**Priority:** Medium

**Verification:** Test.

**Acceptance Criteria:**

- The adapter maintains a recent-message cache for the configured topic.
- A newly connected client can receive up to the last 10 cached messages.
- Cached-message delivery works during periods of low immediate message flow.

### FR-009 Provide Horizontal Pod Autoscaling Configuration

The deployment shall include HPA configuration for the adapter Deployment.

**Priority:** Medium

**Verification:** Inspection.

**Acceptance Criteria:**

- The HPA targets the adapter Deployment.
- The HPA has a minimum replica count of `1`.
- The HPA has a maximum replica count of `2`.
- The HPA uses a CPU utilization target of `80`.
- Scaling by connected-client count is not considered verified unless a connection-count metric path is configured.

### FR-010 Accept Deployment Preconditions

The deployment workflow shall require a GCP project with billing enabled, topic read access, and Pub/Sub subscription creation permission.

**Priority:** High

**Verification:** Inspection and deployment check.

**Acceptance Criteria:**

- The deployment project has billing enabled.
- The deployment identity can read the configured topic.
- The deployment identity can create Pub/Sub subscriptions.

## 5. Non-Functional Requirements

### NFR-001 Horizontal Scalability

The deployment shall support horizontal pod scaling through Kubernetes HPA configuration.

**Metric:** The HPA targets the adapter Deployment with min replicas `1`, max replicas `2`, and CPU utilization target `80`.

### NFR-002 Subscription Efficiency

The adapter shall support many WebSocket clients while using one Pub/Sub subscription per running VM or pod instance.

**Metric:** For `N` running instances and `M` connected clients, subscription consumption scales with `N` rather than `M`.

### NFR-003 Client Data Continuity

The adapter shall provide recent cached messages so client displays can show meaningful data during low-traffic periods.

**Metric:** A client can receive up to the last 10 cached messages for the configured topic.

### NFR-004 Deployment Compatibility

The adapter runtime shall be deployable as a container exposing port `8080` behind a Kubernetes `LoadBalancer` service exposing TCP port `80`.

**Metric:** The running service maps TCP `80` to adapter port `8080`.

### NFR-005 Client Simplicity

Web clients shall receive mirrored Pub/Sub topic data through WebSockets without direct Pub/Sub API or SDK integration.

**Metric:** Client integration requires the WebSocket endpoint and does not require Pub/Sub client credentials.

## 6. Data Requirements

### DR-001 Topic Identifier

The deployment shall maintain a configured Pub/Sub topic identifier.

### DR-002 Runtime Topic Parameter

The adapter runtime shall receive the configured topic identifier through the `SYMBOL` environment variable.

### DR-003 Topic Messages

The adapter shall process messages published to the configured Pub/Sub topic.

### DR-004 WebSocket Message Output

The adapter shall output topic message data to connected WebSocket clients.

### DR-005 Cached Message Set

The adapter shall maintain up to the last 10 messages published to the configured topic.

### DR-006 Subscription Consumption State

The adapter shall maintain subscription behavior such that subscription consumption is related to running instance count rather than connected client count.

### DR-007 Runtime Output Stream

The runtime shall provide output from the `pulltop` process to `websocketd` for client streaming.

## 7. System Constraints

### CON-001 GCP Project Constraint

Deployment requires a GCP project with billing enabled.

### CON-002 Topic Access Constraint

Deployment requires read access to the configured Pub/Sub topic. The topic may be in another project if the deployment identity can read it.

### CON-003 Subscription Permission Constraint

Deployment requires permission to create Pub/Sub subscriptions.

### CON-004 GKE Deployment Constraint

The adapter shall run in Google Kubernetes Engine.

### CON-005 LoadBalancer Service Constraint

External access shall be provided through a Kubernetes `LoadBalancer` service using TCP port `80` and adapter port `8080`.

### CON-006 Runtime Composition Constraint

The checked runtime architecture shall include `pulltop`, `exec.sh`, and `websocketd` as runtime elements.

### CON-007 Topic Configuration Constraint

The configured topic value shall be passed from Kubernetes configuration into the adapter runtime through the `SYMBOL` environment variable.

### CON-008 Autoscaling Metric Constraint

Connected-client-count autoscaling shall not be assumed unless the deployment includes an explicit metric path for connected client count.

## 8. Verification and Acceptance Criteria

| Requirement | Verification Method | Expected Result |
| --- | --- | --- |
| FR-001 | Demonstration | Connected WebSocket clients receive messages from the configured Pub/Sub topic |
| FR-002 | Inspection and demonstration | `exec.sh`, `pulltop`, and `websocketd` form the adapter runtime chain |
| FR-003 | Inspection | Each deployment instance has one endpoint bound to one configured topic |
| FR-004 | Inspection | ConfigMap `topic` is injected into `SYMBOL` and passed to the runtime |
| FR-005 | Inspection and demonstration | `LoadBalancer` service exposes TCP `80` and forwards to port `8080` |
| FR-006 | Demonstration | Client traffic is distributed to selected running adapter instances |
| FR-007 | Inspection, test, and analysis | With `N` instances and `M` clients, subscription consumption scales with `N` rather than `M` |
| FR-008 | Test | A client can receive up to the last 10 cached topic messages |
| FR-009 | Inspection | HPA targets the adapter Deployment with min `1`, max `2`, and CPU utilization target `80` |
| FR-010 | Inspection and deployment check | Billing, topic read access, and subscription creation permission are available |
| NFR-001 | Inspection | HPA horizontal scaling configuration is present |
| NFR-002 | Inspection, test, and analysis | Subscription count does not grow per client connection |
| NFR-003 | Test | Recent-message cache is available during low-traffic periods |
| NFR-004 | Inspection | Container and service ports are aligned at `8080` and TCP `80` |
| NFR-005 | Demonstration | Clients receive data through WebSockets without Pub/Sub API or SDK usage |
