# What an agent can actually complete

546 drops classified on 546 rows of extracted steps. Buckets are decided by what the steps themselves demand, not by optimism.

| Bucket | Drops | Share | Who finishes it |
|---|---|---|---|
| no identity step detected - reading and form fields only | 65 | 12% | agent alone (no identity) |
| ('email', 'e-mail', 'waitlist') | 31 | 6% | agent prepares, human clicks the confirmation link in their inbox |
| ('telegram', 'discord', 'x post', 'tweet', 'follow @') | 73 | 13% | human logs in once, agent continues in that session |
| ('connect', 'sign the message', 'sign a message', 'approve') | 151 | 28% | human approves one wallet signature, agent continues |
| ('deposit', 'minimum', 'fund your', 'purchase', 'buy ') | 146 | 27% | human decides whether to spend; usually skip |
| ('kyc', 'passport', 'proof of address', 'identity verification') | 43 | 8% | human only - legal identity step |
| no usable steps extracted | 37 | 7% | needs manual reading |

**Agent-completable without any human**: 96 of 546 (18%).
**One human touch unlocks**: 224 more (41%) - a login or a signature, then the agent continues.
**Human-only by law or by money**: 189.

Caveats that keep this honest:

- Many of these sites forbid automation in their terms. A bucket says what is *possible*, not what is *permitted* - check the project's terms before letting an agent act.
- "Agent alone" means no identity step is described in the source. The live page can still ask for one; `tools/auto_apply.py` checks that before doing anything.
- Nothing here creates accounts. Registering as a person is a person's act.

Regenerate: `python tools/capability_matrix.py`.