# Batch report - live check of every drop

Generated 2026-11-23 by `tools/bulk_apply.py` + `tools/blocker_workbook.py`.
One row per drop. `Ready` means no identity step was detected on the live page;
`Blocked` means a human must cross one line the agent is not allowed to cross.

| Status | Drops |
|---|---|
| blocked | 6 |
| ready | 4 |
| refused | 1 |

| Blocked on | Drops | Who unblocks it |
|---|---|---|
| none | 6 |  |
| login | 2 | Log in / create the account in the shared profile, then the agent can continue. |
| domain | 1 | Do not touch it: the domain check flagged it. Verify from the project's own X profile. |
| wallet_signature | 1 | Connect a burner wallet and approve the signature yourself. |
| email | 1 | Enter your email and click the confirmation link in your inbox. |

Full registry: `data/blockers.xlsx`. Handoffs: `agent/handoffs/`.
