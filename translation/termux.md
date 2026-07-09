# TERMUX // TRANSLATION PROTOCOL
## Version 4.0 — Living Document

---

## IDENTITY

- **Name:** Termux
- **Provider:** Open source (Android)
- **Tier:** 1 (Edge — Local only)
- **Role:** Execution Environment
- **Specialization:** Shell execution, package management, local development,
  Git operations, Python runtime

---

## CAPABILITIES

| Capability | Input | Output | Confidence |
|------------|-------|--------|------------|
| Shell execution | Bash commands | stdout, stderr, exit code | 0.99 |
| Package management | apt install | Installed packages | 0.95 |
| Git operations | git commands | Repository state | 0.95 |
| Python runtime | Python scripts | Script output | 0.95 |
| File operations | cp, mv, rm | File system state | 0.99 |

---

## CONSTRAINTS

- **RAM:** ~800MB available
- **Storage:** Limited by device
- **Network:** WiFi / mobile data
- **Battery:** Must respect power constraints
- **Heredocs:** Break on paste — use Python one-liners

---

## TRANSLATION RULES

1. **Always use Python one-liners for multiline scripts**
2. **Check available RAM before loading large models**
3. **Use `proot-distro` for isolated environments**
4. **Prefer `curl` over `wget` for API calls**
5. **Use `jq` for JSON processing**
6. **Cache downloads to `~/.picoclaw/cache/`**

---

## NATIVE → NEXUS

```
Termux command output
    ↓
Structured log (JSON)
    ↓
CMB (CAT7)
    ↓
Knowledge Block
    ↓
Git Commit
    ↓
Canonical Memory
```

---

*Generated: 2026-07-09*
*Canonical at: quillyos-nexus/translation/termux.md*
