#!/usr/bin/env python3
"""
kv_expiry_checker.py
--------------------
Lists all Key Vault secrets and calculates days until expiry.
Critical for preventing pipeline failures from expired credentials.

Usage:
    python kv_expiry_checker.py --vault kv-eshoponweb-dev
    python kv_expiry_checker.py --vault kv-eshoponweb-dev --warn-days 60
    python kv_expiry_checker.py --vault kv-eshoponweb-dev --verbose
"""

import subprocess
import json
import argparse
import logging
from datetime import datetime, timezone


# ─── ARGUMENT PARSER ────────────────────────────────────────────────────────
def get_args():
    parser = argparse.ArgumentParser(
        description="Check Key Vault secret expiry dates"
    )
    parser.add_argument(
        "--vault",
        required=True,
        help="Key Vault name (e.g. kv-eshoponweb-dev)"
    )
    parser.add_argument(
        "--warn-days",
        type=int,
        default=30,
        help="Warn if secret expires within this many days (default: 30)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    return parser.parse_args()


# ─── LOGGING SETUP ──────────────────────────────────────────────────────────
def setup_logging(verbose: bool):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        format="%(asctime)s  %(levelname)-8s  %(message)s",
        datefmt="%H:%M:%S",
        level=level
    )


# ─── HELPER: run shell command ───────────────────────────────────────────────
def run_command(command: list) -> dict:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )
        return {
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "returncode": result.returncode
        }
    except FileNotFoundError:
        return {
            "stdout": "",
            "stderr": f"Command not found: {command[0]}",
            "returncode": 1
        }


# ─── FUNCTIONS ──────────────────────────────────────────────────────────────
def list_secrets(vault_name: str) -> list:
    """Returns list of all secrets in the Key Vault."""
    logging.debug(f"Listing secrets in {vault_name}")

    result = run_command([
        "az", "keyvault", "secret", "list",
        "--vault-name", vault_name,
        "--output", "json"
    ])

    if result["returncode"] != 0:
        logging.error(f"Failed to list secrets: {result['stderr']}")
        return []

    try:
        secrets = json.loads(result["stdout"])
        logging.debug(f"Found {len(secrets)} secrets")
        return secrets
    except json.JSONDecodeError:
        logging.error("Failed to parse secrets list")
        return []


def get_secret_details(vault_name: str, secret_name: str) -> dict:
    """Returns full details of a specific secret including expiry."""
    logging.debug(f"Getting details for secret: {secret_name}")

    result = run_command([
        "az", "keyvault", "secret", "show",
        "--vault-name", vault_name,
        "--name", secret_name,
        "--output", "json"
    ])

    if result["returncode"] != 0:
        logging.debug(f"Could not get secret details: {result['stderr']}")
        return {}

    try:
        return json.loads(result["stdout"])
    except json.JSONDecodeError:
        return {}


def days_until_expiry(expiry_str: str) -> int:
    """Calculates days until expiry from ISO format date string."""
    try:
        expiry = datetime.fromisoformat(
            expiry_str.replace("Z", "+00:00")
        )
        now = datetime.now(timezone.utc)
        delta = expiry - now
        return delta.days
    except (ValueError, TypeError):
        return -1


def format_table(headers: list, rows: list) -> str:
    """Formats data as a simple text table."""
    if not rows:
        return "  No items found."

    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))

    header_line = "  " + "  ".join(
        h.ljust(col_widths[i]) for i, h in enumerate(headers)
    )
    separator = "  " + "  ".join("-" * w for w in col_widths)

    data_lines = []
    for row in rows:
        line = "  " + "  ".join(
            str(val).ljust(col_widths[i]) for i, val in enumerate(row)
        )
        data_lines.append(line)

    return "\n".join([header_line, separator] + data_lines)


def generate_report(vault_name: str, warn_days: int) -> dict:
    """Generates full expiry report for all secrets."""
    secrets = list_secrets(vault_name)

    if not secrets:
        return {"secrets": [], "warnings": [], "expired": []}

    report = {
        "secrets": [],
        "warnings": [],
        "expired": []
    }

    for secret in secrets:
        # Extract secret name from ID
        secret_id = secret.get("id", "")
        secret_name = secret_id.split("/")[-1] if secret_id else "unknown"

        # Get expiry from attributes
        attributes = secret.get("attributes", {})
        expiry_str = attributes.get("expires", None)
        enabled = attributes.get("enabled", True)

        if expiry_str:
            days_left = days_until_expiry(expiry_str)
            expiry_date = expiry_str[:10]
        else:
            days_left = None
            expiry_date = "No expiry set"

        entry = {
            "name": secret_name,
            "enabled": enabled,
            "expiry_date": expiry_date,
            "days_left": days_left
        }

        report["secrets"].append(entry)

        # Categorise
        if days_left is not None:
            if days_left < 0:
                report["expired"].append(entry)
            elif days_left <= warn_days:
                report["warnings"].append(entry)

    # Sort by days_left (most urgent first)
    report["secrets"].sort(
        key=lambda x: x["days_left"]
        if x["days_left"] is not None else 9999
    )

    return report


# ─── MAIN ───────────────────────────────────────────────────────────────────
def main():
    args = get_args()
    setup_logging(args.verbose)

    print("\n" + "=" * 60)
    print(f"   Key Vault Expiry Checker — {args.vault}")
    print("=" * 60)

    report = generate_report(args.vault, args.warn_days)

    if not report["secrets"]:
        logging.error("No secrets found or vault not accessible")
        return

    # ── All secrets table
    print(f"\n[ All Secrets ({len(report['secrets'])} total) ]")
    rows = []
    for s in report["secrets"]:
        days_display = (
            str(s["days_left"]) + " days"
            if s["days_left"] is not None
            else "No expiry"
        )
        status = "✅"
        if s["days_left"] is not None:
            if s["days_left"] < 0:
                status = "❌ EXPIRED"
            elif s["days_left"] <= args.warn_days:
                status = "⚠️  WARNING"

        rows.append([
            s["name"],
            s["expiry_date"],
            days_display,
            status
        ])

    headers = ["SECRET NAME", "EXPIRY DATE", "DAYS LEFT", "STATUS"]
    print(format_table(headers, rows))

    # ── Expired secrets
    if report["expired"]:
        print(f"\n[ ❌ Expired Secrets ({len(report['expired'])}) ]")
        for s in report["expired"]:
            logging.error(
                f"  EXPIRED: {s['name']} expired on {s['expiry_date']}"
            )

    # ── Warning secrets
    if report["warnings"]:
        print(
            f"\n[ ⚠️  Expiring Within {args.warn_days} Days "
            f"({len(report['warnings'])}) ]"
        )
        for s in report["warnings"]:
            logging.warning(
                f"  WARNING: {s['name']} expires in "
                f"{s['days_left']} days ({s['expiry_date']})"
            )

    # ── Summary
    print("\n" + "=" * 60)
    print(f"   Total secrets    : {len(report['secrets'])}")
    print(f"   Expired          : {len(report['expired'])}")
    print(
        f"   Expiring soon    : {len(report['warnings'])} "
        f"(within {args.warn_days} days)"
    )
    print(f"   Healthy          : "
          f"{len(report['secrets']) - len(report['expired']) - len(report['warnings'])}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()