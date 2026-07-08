# Layer 3 — Translation

> Context rendered into agent-specific formats. One truth, many dialects.

## Purpose

Different agents need different representations of the same truth:

- **Kimi** needs architectural context and code structures
- **GPT** needs reasoning chains and narrative context
- **Picoclaw** needs local execution context and file paths
- **n8n** needs workflow triggers and API schemas
- **Human collaborators** need readable summaries and decision points

## Translation Schema

```json
{
  "translation_id": "trn-UUID",
  "parent_context_id": "ctx-UUID",
  "target_agent": "kimi|gpt|picoclaw|n8n|human",
  "format": "markdown|json|yaml|workflow_json|natural_language",
  "payload": "<translated content>",
  "back_reference": "ctx-UUID",
  "agent_notes": "specific instructions for this agent type"
}
```

## Agent Translation Profiles

### Kimi (Systems Architect & Integrator)
- Prefers: Markdown with code blocks, architectural diagrams, file trees
- Needs: Repository structure, dependency maps, implementation plans
- Receives: Structured briefs with next-action sequences

### GPT (Reasoning & Synthesis)
- Prefers: Narrative context with evidence chains
- Needs: Historical reasoning, philosophical alignment, strategic analysis
- Receives: Expanded North Star documents, vision briefs

### Picoclaw (Local Execution)
- Prefers: JSON configs, shell scripts, file paths
- Needs: Local environment state, skill manifests, automation triggers
- Receives: Context packages with executable artifacts

### n8n (Workflow Execution)
- Prefers: Workflow JSON, API schemas, trigger conditions
- Needs: Event routing, approval pipelines, scheduling
- Receives: Workflow definitions with embedded context

### Human Collaborators
- Prefers: Readable prose, visual summaries, decision trees
- Needs: Status updates, risk assessments, next steps
- Receives: Session briefs, handoff documents, dashboards

---
*Layer steward: Protocol Council*
*Version: 4.0*
