#!/usr/bin/env python3
import json
import logging
import sys
import time
from itertools import product

import paramiko

# ─── SILENCE PARAMIKO LOGGING AND BANNER ERRORS ─────────────────────────────
logging.getLogger("paramiko").setLevel(logging.CRITICAL)
import paramiko.transport

_orig_check_banner = paramiko.transport.Transport._check_banner

def _silent_check_banner(self, timeout):
    try:
        return _orig_check_banner(self, timeout)
    except Exception:
        return

paramiko.transport.Transport._check_banner = _silent_check_banner
# ────────────────────────────────────────────────────────────────────────────

# ─── LOAD CONFIG ────────────────────────────────────────────────────────────
with open("config.json", "r") as f:
    cfg = json.load(f)

HOST = cfg.get("host")
PORT = cfg.get("port", 22)
USERNAME = cfg.get("username")
base_passwords = cfg.get("base_passwords", [])
raw_suffixes   = cfg.get("raw_suffixes", [])
# ────────────────────────────────────────────────────────────────────────────

# generate suffixes by repeating each raw entry 1×, 2×, or 6×
repeat_counts = [1, 2, 6]
suffixes = [s * n for s in raw_suffixes for n in repeat_counts]

# retry settings
MAX_NETWORK_RETRIES = 5   # on network/banner errors
NETWORK_RETRY_DELAY = 1   # seconds


def try_password(password: str) -> bool:
    for attempt in range(1, MAX_NETWORK_RETRIES + 1):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(
                HOST, PORT, USERNAME, password,
                timeout=5,
                banner_timeout=5,
                auth_timeout=5,
                look_for_keys=False,
                allow_agent=False
            )
            client.close()
            return True
        except paramiko.AuthenticationException:
            return False
        except (paramiko.SSHException, Exception):
            if attempt < MAX_NETWORK_RETRIES:
                time.sleep(NETWORK_RETRY_DELAY)
                continue
            return False
    return False


def main():
    print(f"→ Trying SSH combos to {USERNAME}@{HOST} …")
    for base, suf in product(base_passwords, suffixes):
        pwd = base + suf
        sys.stdout.write(f"\r    Testing: {pwd:<50}")
        sys.stdout.flush()
        if try_password(pwd):
            print(f"\n✅ Success! Password is: {pwd}")
            return
    print("\n❌ All combinations exhausted without success.")


if __name__ == "__main__":
    main()