# Translation Layer

> Agent-specific context packages

## Purpose

The translation layer converts canonical Nexus context into formats optimized for each agent type. This directory contains templates and examples.

## Directory Structure

```
translations/
├── kimi/
│   ├── context-package-template.md
│   └── example-session-brief.md
├── gpt/
│   ├── context-package-template.md
│   └── example-vision-brief.md
├── picoclaw/
│   ├── context-package-template.json
│   └── example-skill-manifest.json
├── n8n/
│   ├── context-package-template.json
│   └── example-workflow.json
└── human/
    ├── context-package-template.md
    └── example-dashboard.md
```

## Translation Rules

1. Every translation must reference its parent context_id
2. Translations are ephemeral — canonical truth lives in the consensus layer
3. Agents should pull fresh translations before each session
4. Discrepancies between translations trigger consensus review

## Kimi Context Package Template

```markdown
# Context Package for Kimi
## Session ID: {{session_id}}
## Source Context: {{context_id}}

### Mission
{{mission_statement}}

### Current Architecture
{{architecture_summary}}

### Known Evidence
{{evidence_list}}

### Open Questions
{{questions_list}}

### Constraints
{{constraints_list}}

### Dependencies
{{dependency_map}}

### Objectives
{{objectives_list}}

### Current Milestones
{{milestones_list}}

### Next Actions
{{next_actions_list}}
```

---
*Translation steward: Protocol Council*
*Version: 4.0*
