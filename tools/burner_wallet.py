"""Create a throwaway burner wallet ON THE OPERATOR'S MACHINE. Run this yourself, not through an agent.

AGENTS.md rule 1 says an agent must never read, store, transmit or type a private key, so this script
is written for a human to run in a terminal. It prints the key once and never writes it anywhere.
The only thing it saves to disk is the public address, into agent/operator-inputs.json.

  python tools/burner_wallet.py --i-am-the-operator            # generate, show key once
  python tools/burner_wallet.py --i-am-the-operator --dry      # generate, show address only

Rules that make this safe:
  - The key prints to YOUR terminal only. Copy it into a password manager, not into a file, a chat,
    a screenshot or this repo. Anyone with the key has the money forever.
  - Fund it only with what you can afford to lose, and never move main-wallet funds through it.
  - If it ever holds a real balance, stop using it for new airdrops and generate a fresh one.
"""
import argparse
import json
import os
import secrets
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INPUTS = ROOT / "agent" / "operator-inputs.json"


def save_address(address, chain="evm"):
    data = {}
    if INPUTS.exists():
        try:
            data = json.loads(INPUTS.read_text(encoding="utf-8"))
        except Exception:
            data = {}
    data.setdefault("wallet", address)
    data.setdefault("wallet_chain", chain)
    data.setdefault("note", "public values only - never put a seed phrase or private key in this file")
    INPUTS.parent.mkdir(parents=True, exist_ok=True)
    INPUTS.write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--i-am-the-operator", action="store_true",
                    help="required: confirms a human, not an agent, is running this")
    ap.add_argument("--dry", action="store_true", help="show the address but not the key")
    ap.add_argument("--save", action="store_true", default=True,
                    help="write the public address to agent/operator-inputs.json (default on)")
    args = ap.parse_args()

    if not args.i_am_the_operator:
        print("Refusing to run: this generates a private key, and only the operator may hold one.\n"
              "Re-run with --i-am-the-operator if you are the human running this repo.")
        return 2

    try:
        from eth_account import Account
        acct = Account.from_key(secrets.token_hex(32))
        address, key = acct.address, acct.key.hex()
    except Exception as e:
        print(f"eth_account unavailable ({e}). Install it: ./.venv/Scripts/pip install eth-account")
        return 1

    save_address(address)

    print("=" * 74)
    print("BURNER WALLET CREATED")
    print(f"  address : {address}")
    print(f"  saved to: agent/operator-inputs.json (address only)")
    print("=" * 74)
    if args.dry:
        print("  --dry: key withheld on purpose. Generate a wallet you can keep the key for.")
    else:
        print("  private key (shown once, copy it to your password manager NOW):")
        print(f"  {key}")
        print()
        print("  NOT into a file. NOT into this repo. NOT into a chat or a screenshot.")
        print("  Lose it and the wallet's funds are gone; leak it and they are gone sooner.")
    print("=" * 74)
    print(f"  next: python tools/redeem_kit.py --open")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
    sys.exit(main())
