# Batch report - live check of every drop

Generated 2026-11-23 by `tools/bulk_apply.py` + `tools/blocker_workbook.py`.
One row per drop. `Ready` means no identity step was detected on the live page;
`Blocked` means a human must cross one line the agent is not allowed to cross.

| Status | Drops |
|---|---|
| blocked | 276 |
| refused | 85 |
| no-url | 62 |
| ready | 59 |
| unknown | 54 |
| unreachable | 10 |

| Blocked on | Drops | Who unblocks it |
|---|---|---|
| wallet_signature | 112 | Connect a burner wallet and approve the signature yourself. |
| domain | 89 | Do not touch it: the domain check flagged it. Verify from the project's own X profile. |
| login | 76 | Log in / create the account in the shared profile, then the agent can continue. |
| no-official-site | 62 | No official domain was extracted. Find it from the project's own profile first. |
| none | 59 |  |
| email | 59 | Enter your email and click the confirmation link in your inbox. |
| unknown | 54 | Needs manual reading - the live page did not expose a clear step. |
| terms | 16 | Read and accept the project terms in your own name. |
| site-unreachable | 10 | The page did not load. Try the URL yourself; record 403/404 in fetch-report. |
| kyc | 9 | Pass KYC in your own name (legal step, agent cannot). Then finish the steps in apply/. |

Full registry: `data/blockers.xlsx`. Handoffs: `agent/handoffs/`.
