#!/usr/bin/env python3
"""
azure_env_check.py
------------------
Validates your Azure development environment is correctly configured
before starting each working session.

Usage:
    python azure_env_check.py
    python azure_env_check.py --verbose
"""

import subprocess
import json
import sys
import argparse
import logging


# ─── ARGUMENT PARSER ────────────────────────────────────────────────────────
def get_args():
    parser = argparse.ArgumentParser(
        description="Validate Azure development environment health"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose/debug output"
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


# ─── HELPER: run a shell command ────────────────────────────────────────────
def run_command(command: list) -> dict:
    """
    Runs a shell command and returns stdout, stderr, and return code.
    Uses a list of strings — safer than shell=True.
    """
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


# ─── CHECK FUNCTIONS ────────────────────────────────────────────────────────
def check_python_version() -> bool:
    """Check Python version is 3.10 or higher."""
    major = sys.version_info.major
    minor = sys.version_info.minor
    version_str = f"{major}.{minor}.{sys.version_info.micro}"

    if major == 3 and minor >= 10:
        logging.info(f"  Python Version     : {version_str} ✅")
        return True
    else:
        logging.warning(f"  Python Version     : {version_str} ⚠️  (3.10+ recommended)")
        return False


def check_az_login() -> bool:
    """Check if Azure CLI is installed and logged in."""
    result = run_command(["az", "--version"])
    if result["returncode"] != 0:
        logging.error("  Azure CLI          : Not installed ❌")
        return False

    # Extract version from output
    first_line = result["stdout"].split("\n")[0]
    logging.info(f"  Azure CLI          : {first_line} ✅")
    return True


def get_subscription_info() -> bool:
    """Get and display current Azure subscription details."""
    result = run_command(["az", "account", "show", "--output", "json"])

    if result["returncode"] != 0:
        logging.error("  Azure Login        : Not logged in ❌  Run: az login")
        return False

    try:
        account = json.loads(result["stdout"])
        name = account.get("name", "Unknown")
        state = account.get("state", "Unknown")
        sub_id = account.get("id", "Unknown")

        # Only show last 8 chars of subscription ID for security
        masked_id = f"****-****-****-{sub_id[-8:]}"

        logging.info(f"  Azure Login        : Logged in ✅")
        logging.info(f"  Subscription Name  : {name}")
        logging.info(f"  Subscription ID    : {masked_id}")
        logging.info(f"  Account State      : {state}")
        return True

    except json.JSONDecodeError:
        logging.error("  Azure Login        : Could not parse account info ❌")
        return False


def check_tool(tool: str, version_flag: str, display_name: str) -> bool:
    """Generic tool version checker."""
    result = run_command([tool] + version_flag.split())

    if result["returncode"] != 0:
        logging.warning(f"  {display_name:<20}: Not installed ❌")
        return False

    # Get first line of version output
    version = result["stdout"].split("\n")[0]
    logging.info(f"  {display_name:<20}: {version} ✅")
    return True


def check_resource_groups() -> bool:
    """Verify the 4 project resource groups exist."""
    expected_rgs = [
        "rg-eshoponweb-infra",
        "rg-eshoponweb-aks",
        "rg-eshoponweb-acr",
        "rg-eshoponweb-monitoring"
    ]

    result = run_command([
        "az", "group", "list",
        "--query", "[].name",
        "--output", "json"
    ])

    if result["returncode"] != 0:
        logging.error("  Resource Groups    : Could not query ❌")
        return False

    try:
        existing_rgs = json.loads(result["stdout"])
        all_present = True

        for rg in expected_rgs:
            if rg in existing_rgs:
                logging.info(f"  RG: {rg:<40} ✅")
            else:
                logging.warning(f"  RG: {rg:<40} ❌ Missing")
                all_present = False

        return all_present

    except json.JSONDecodeError:
        logging.error("  Resource Groups    : Could not parse response ❌")
        return False


# ─── MAIN ───────────────────────────────────────────────────────────────────
def main():
    args = get_args()
    setup_logging(args.verbose)

    print("\n" + "=" * 60)
    print("   AZURE CLOUD CICD PLATFORM — Environment Health Check")
    print("=" * 60)

    results = []

    # ── Python
    print("\n[ Python ]")
    results.append(check_python_version())

    # ── Azure CLI + Login
    print("\n[ Azure CLI ]")
    results.append(check_az_login())
    results.append(get_subscription_info())

    # ── Tools
    print("\n[ Tools ]")
    results.append(check_tool("terraform", "version", "Terraform"))
    results.append(check_tool("kubectl", "version --client --output=yaml", "kubectl"))
    results.append(check_tool("helm", "version", "Helm"))
    results.append(check_tool("docker", "--version", "Docker"))
    results.append(check_tool("gh", "--version", "GitHub CLI"))

    # ── Resource Groups
    print("\n[ Azure Resource Groups ]")
    results.append(check_resource_groups())

    # ── Summary
    print("\n" + "=" * 60)
    passed = results.count(True)
    total = len(results)

    if all(results):
        print(f"   ✅  All {total} checks passed — environment is ready")
    else:
        failed = total - passed
        print(f"   ⚠️   {passed}/{total} checks passed — {failed} issue(s) found")
        print("   Fix the ❌ items above before proceeding")

    print("=" * 60 + "\n")

    # Exit with error code if any check failed
    sys.exit(0 if all(results) else 1)


if __name__ == "__main__":
    main()