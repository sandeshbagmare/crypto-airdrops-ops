# What an agent can actually complete

546 drops classified on 546 rows of extracted steps. Buckets are decided by what the steps themselves demand, not by optimism.

| Bucket | Drops | Share | Who finishes it |
|---|---|---|---|
| agent_live | 116 | 21% | agent alone - confirmed on the live page |
| no identity step detected - reading and form fields only | 43 | 8% | agent alone (no identity) |
| ('email', 'e-mail', 'waitlist') | 22 | 4% | agent prepares, human clicks the confirmation link in their inbox |
| ('telegram', 'discord', 'x post', 'tweet', 'follow @') | 44 | 8% | human logs in once, agent continues in that session |
| ('connect', 'sign the message', 'sign a message', 'approve') | 88 | 16% | human approves one wallet signature, agent continues |
| ('deposit', 'minimum', 'fund your', 'purchase', 'buy ') | 87 | 16% | human decides whether to spend; usually skip |
| ('kyc', 'passport', 'proof of address', 'identity verification') | 34 | 6% | human only - legal identity step |
| refused | 86 | 16% | nobody - domain failed the safety check |
| unreachable | 9 | 2% | nobody until the source is re-checked |
| no usable steps extracted | 17 | 3% | needs manual reading |

**Agent-completable without any human**: 181 of 546 (33%).
**One human touch unlocks**: 132 more (24%) - a login or a signature, then the agent continues.
**Human-only by law or by money**: 121.

Caveats that keep this honest:

- Many of these sites forbid automation in their terms. A bucket says what is *possible*, not what is *permitted* - check the project's terms before letting an agent act.
- "Agent alone" means no identity step is described in the source. The live page can still ask for one; `tools/auto_apply.py` checks that before doing anything.
- Nothing here creates accounts. Registering as a person is a person's act.

Regenerate: `python tools/capability_matrix.py`.