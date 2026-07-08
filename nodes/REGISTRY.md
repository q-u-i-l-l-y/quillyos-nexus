# Node Registry

> Active nodes in the QuillyOS mesh

| Node ID | Type | Status | Hardware | Location | Last Seen |
|---------|------|--------|----------|----------|-----------|
| node-hub-01 | Hub | Planned | Desktop | TBD | — |
| node-revenue-01 | Spoke-Revenue | Active | Android/Termux | Mobile | 2026-07-08 |
| node-compute-01 | Spoke-Compute | Planned | Raspberry Pi | TBD | — |
| node-data-01 | Spoke-Data | Planned | NAS | TBD | — |
| node-health-01 | Spoke-Health | Planned | Nexus ENDS | TBD | — |
| node-quantum-01 | Spoke-Quantum | Conceptual | TBD | TBD | — |

## Registration Protocol

1. New node runs `install/install.sh`
2. Script generates `node-id` and `node-type`
3. Node creates `nodes/self.json` with metadata
4. Node pushes `nodes/self.json` to Hub via Git
5. Hub merges into `nodes/registry.json`
6. Hub broadcasts updated registry to all nodes

---
*Registry steward: Hub node (node-hub-01 when established)*
*Version: 4.0*
