#!/usr/bin/env python3
"""
acr_manager.py
--------------
Lists all images and tags in ACR, identifies old images
that should be cleaned up.

Usage:
    python acr_manager.py --registry acreshoponwebdev
    python acr_manager.py --registry acreshoponwebdev --days 30
    python acr_manager.py --registry acreshoponwebdev --verbose
"""

import subprocess
import json
import argparse
import logging
from datetime import datetime, timezone


# ─── ARGUMENT PARSER ────────────────────────────────────────────────────────
def get_args():
    parser = argparse.ArgumentParser(
        description="Manage and inspect Azure Container Registry images"
    )
    parser.add_argument(
        "--registry",
        required=True,
        help="ACR registry name (e.g. acreshoponwebdev)"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="Flag images older than this many days (default: 30)"
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
def list_repositories(registry_name: str) -> list:
    """Returns list of all repositories in the ACR."""
    logging.debug(f"Fetching repositories from {registry_name}")

    result = run_command([
        "az", "acr", "repository", "list",
        "--name", registry_name,
        "--output", "json"
    ])

    if result["returncode"] != 0:
        logging.error(f"Failed to list repositories: {result['stderr']}")
        return []

    try:
        repos = json.loads(result["stdout"])
        logging.debug(f"Found {len(repos)} repositories")
        return repos
    except json.JSONDecodeError:
        logging.error("Failed to parse repository list")
        return []


def list_tags(registry_name: str, repository: str) -> list:
    """Returns list of all tags for a given repository with metadata."""
    logging.debug(f"Fetching tags for {repository}")

    result = run_command([
        "az", "acr", "repository", "show-tags",
        "--name", registry_name,
        "--repository", repository,
        "--detail",
        "--output", "json"
    ])

    if result["returncode"] != 0:
        logging.error(f"Failed to list tags: {result['stderr']}")
        return []

    try:
        tags = json.loads(result["stdout"])
        return tags
    except json.JSONDecodeError:
        logging.error("Failed to parse tag list")
        return []


def find_old_images(registry_name: str, repository: str, days: int) -> list:
    """Returns list of images older than the specified number of days."""
    tags = list_tags(registry_name, repository)
    old_images = []
    now = datetime.now(timezone.utc)

    for tag in tags:
        try:
            # Parse last update time
            last_updated_str = tag.get("lastUpdateTime", "")
            if not last_updated_str:
                continue

            # Handle timezone format
            last_updated = datetime.fromisoformat(
                last_updated_str.replace("Z", "+00:00")
            )

            age_days = (now - last_updated).days

            if age_days >= days:
                old_images.append({
                    "repository": repository,
                    "tag": tag.get("name", "unknown"),
                    "last_updated": last_updated_str[:10],
                    "age_days": age_days
                })

        except (ValueError, TypeError) as e:
            logging.debug(f"Could not parse date for tag: {e}")
            continue

    return old_images


def format_table(headers: list, rows: list) -> str:
    """Formats data as a simple text table."""
    if not rows:
        return "  No data found."

    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))

    # Build header
    header_line = "  " + "  ".join(
        h.ljust(col_widths[i]) for i, h in enumerate(headers)
    )
    separator = "  " + "  ".join("-" * w for w in col_widths)

    # Build rows
    data_lines = []
    for row in rows:
        line = "  " + "  ".join(
            str(val).ljust(col_widths[i]) for i, val in enumerate(row)
        )
        data_lines.append(line)

    return "\n".join([header_line, separator] + data_lines)


# ─── MAIN ───────────────────────────────────────────────────────────────────
def main():
    args = get_args()
    setup_logging(args.verbose)

    print("\n" + "=" * 60)
    print(f"   ACR Manager — {args.registry}")
    print("=" * 60)

    # ── List repositories
    print("\n[ Repositories ]")
    repos = list_repositories(args.registry)

    if not repos:
        logging.error("No repositories found or ACR not accessible")
        return

    for repo in repos:
        logging.info(f"  Repository: {repo}")

    # ── List tags per repository
    print("\n[ Images & Tags ]")
    all_tag_rows = []

    for repo in repos:
        tags = list_tags(args.registry, repo)

        for tag in tags:
            name = tag.get("name", "unknown")
            last_updated = tag.get("lastUpdateTime", "")[:10]
            digest = tag.get("digest", "")[:20]
            all_tag_rows.append([repo, name, last_updated, digest])

    headers = ["REPOSITORY", "TAG", "LAST UPDATED", "DIGEST"]
    print(format_table(headers, all_tag_rows))

    # ── Find old images
    print(f"\n[ Images Older Than {args.days} Days ]")
    old_image_rows = []

    for repo in repos:
        old = find_old_images(args.registry, repo, args.days)
        for img in old:
            old_image_rows.append([
                img["repository"],
                img["tag"],
                img["last_updated"],
                str(img["age_days"]) + " days"
            ])

    old_headers = ["REPOSITORY", "TAG", "LAST UPDATED", "AGE"]
    print(format_table(old_headers, old_image_rows))

    if old_image_rows:
        print(f"\n  ⚠️  {len(old_image_rows)} image(s) older than {args.days} days found")
        print("  Run image_cleanup.py to remove them")
    else:
        print(f"\n  ✅  No images older than {args.days} days")

    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()