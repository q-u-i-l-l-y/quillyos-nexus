# OLLAMA // TRANSLATION PROTOCOL
## Version 4.0 — Living Document

---

## IDENTITY

- **Name:** Ollama
- **Provider:** Ollama (open source)
- **Tier:** 1 (Edge — Local only)
- **Role:** Persistent Cognition Node
- **Specialization:** Local reasoning, document ingestion, skill execution,
  knowledge synthesis, memory retrieval, local automation

---

## CAPABILITIES

| Capability | Input | Output | Confidence |
|------------|-------|--------|------------|
| Local inference | Prompt, context | Generated text | 0.75 |
| Document ingestion | Files, directories | Structured knowledge | 0.80 |
| Skill execution | Skill name, parameters | Skill output | 0.85 |
| Health monitoring | Biometric data | Probabilistic mapping | 0.70 |
| Mesh sync | GitHub API, local state | Synchronized memory | 0.82 |

---

## MODELS

| Model | Size | Use Case | Tool Support |
|-------|------|----------|--------------|
| TinyLlama | 1.1B | Fast inference, low RAM | No |
| Qwen 2.5 0.5B | 0.5B | Tool calling, agent mode | Yes |
| Qwen 2.5 3B | 3B | Balanced performance | Yes |
| DeepSeek-R1 1.5B | 1.5B | Reasoning, reflection | Limited |

---

## TRANSLATION RULES

1. **Always check model availability before routing**
2. **Prefer Qwen 2.5 0.5B for tool calling**
3. **Use TinyLlama for fast, simple queries**
4. **Keep context under 512 tokens for edge models**
5. **Cache responses to reduce API calls**

---

## NATIVE → NEXUS

```
Ollama output
    ↓
CMB (CAT7)
    ↓
Knowledge Block
    ↓
Git Commit (via github_sync skill)
    ↓
Canonical Memory
```

---

*Generated: 2026-07-09*
*Canonical at: quillyos-nexus/translation/ollama.md*
