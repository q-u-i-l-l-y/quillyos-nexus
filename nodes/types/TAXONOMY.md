# Node Type Taxonomy

> Six distinct node types for the QuillyOS mesh

## Overview

Every node in the mesh has a type. Types define responsibilities, hardware requirements, and protocol participation.

---

## Hub

**Role**: Coordination, governance, canonical memory
**Responsibilities**:
- Validate consensus records
- Arbitrate disputes between spokes
- Maintain canonical repository state
- Route context packages to appropriate spokes
- Record governance decisions

**Hardware Examples**:
- Desktop workstation
- Server (cloud or on-premise)
- High-availability Raspberry Pi cluster

**Minimum Requirements**:
- Git
- Python 3.10+
- 8GB RAM
- Persistent storage

**Protocol Participation**:
- All layers (0-4)
- Consensus arbitration
- Governance record-keeping

---

## Spoke-Compute

**Role**: Edge inference, local reasoning, skill execution
**Responsibilities**:
- Run local models (Picoclaw)
- Execute Python scripts and workflows
- Process observations into evidence
- Maintain local knowledge cache

**Hardware Examples**:
- Raspberry Pi 4/5
- Termux-enabled Android phone
- Old laptop repurposed as compute node

**Minimum Requirements**:
- Python 3.10+
- 2GB RAM
- Git
- Termux or Linux

**Protocol Participation**:
- Layers 0-2 (Observation, Evidence, Context)
- Translation to local formats

---

## Spoke-Data

**Role**: Storage, indexing, retrieval, backup
**Responsibilities**:
- Store observations, evidence, context
- Index entities for fast lookup
- Maintain backup of canonical repositories
- Serve data queries to other nodes

**Hardware Examples**:
- NAS (Network Attached Storage)
- Cloud storage instance
- Old desktop with large drives

**Minimum Requirements**:
- 500GB storage
- Git
- SQLite or similar

**Protocol Participation**:
- Layers 0-2
- Data query responses

---

## Spoke-Quantum

**Role**: Quantum-classical interface, future sensing
**Responsibilities**:
- Interface with quantum sensors (when available)
- Process quantum-enhanced observations
- Bridge classical and quantum data streams
- Research quantum communication protocols

**Hardware Examples**:
- Future: quantum dot sensors
- Future: nitrogen-vacancy center devices
- Current: classical node with quantum research context

**Minimum Requirements**:
- TBD — currently conceptual

**Protocol Participation**:
- Layers 0-1 (quantum observations)
- Research context in matrix-003

---

## Spoke-Revenue

**Role**: Financial automation, arbitrage, deal analysis
**Responsibilities**:
- Execute trading and arbitrage scripts
- Analyze real estate deals
- Track investment portfolios
- Generate revenue reports

**Hardware Examples**:
- Android phone with Termux (current)
- Dedicated trading machine
- Cloud VPS for 24/7 operation

**Minimum Requirements**:
- Python 3.10+
- Internet access
- API keys for financial services

**Protocol Participation**:
- Layers 0-2 (financial observations)
- Revenue context in matrix-001

---

## Spoke-Health

**Role**: Medical monitoring, ENDS platform, biometrics
**Responsibilities**:
- Collect biometric data from sensors
- Monitor health trends
- Interface with the Nexus ENDS device
- Generate health reports and alerts

**Hardware Examples**:
- Nexus ENDS device (future)
- Wearable health monitors (current)
- Smartphone with health apps

**Minimum Requirements**:
- Bluetooth or USB sensor interface
- Python 3.10+
- Health data privacy compliance

**Protocol Participation**:
- Layers 0-2 (health observations)
- Health context in matrix-002

---

## Node Registration

When a new node joins the mesh:

1. Clone `quillyos-nexus`
2. Run `install/install.sh`
3. Script detects hardware and assigns node type
4. Node registers with nearest Hub
5. Hub adds node to mesh registry
6. Node begins participating in protocol layers

---
*Node taxonomy steward: Chief Architect*
*Version: 4.0*
