# SSH Brute-Force Utility

A simple Python script that iterates over combinations of base passwords and repeated suffixes, attempting SSH login until a valid credential is found. Sensitive data (host, username, password lists) are kept in a separate `config.json`.

## Features

- Config-driven: hosts and password patterns live in `config.json`.
- Silent banner-error handling to avoid skipping attempts.
- Retry logic on network/protocol errors to ensure no combos are skipped.

## Usage

1. **Clone this repo**
   ```bash
   git clone https://github.com/<your-username>/ssh-brute.git
   cd ssh-brute
   ```

# SSH Brute-Force Utility

A simple Python script that iterates over combinations of base passwords and repeated suffixes, attempting SSH login until a valid credential is found. Sensitive data (host, username, password lists) are kept in a separate `config.json`.

## Features

- Config-driven: hosts and password patterns live in `config.json`.
- Silent banner-error handling to avoid skipping attempts.
- Retry logic on network/protocol errors to ensure no combos are skipped.

## Usage

1. **Clone this repo**

   ```bash
   git clone https://github.com/<your-username>/ssh-brute.git
   cd ssh-brute

   ```

2. Install dependencies
   `pip install paramiko`

3. Edit `config.json` Populate with your target host, SSH port, username, and password patterns.

4. Run the script
   `python3 brute_ssh.py`

Security Note

This tool is for authorized testing on systems you own or have permission to audit. Do not use on unauthorized targets.

License

Distributed under the MIT License. See LICENSE for details.
