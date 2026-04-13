#!/usr/bin/env python3
"""
aks_health.py
-------------
Polls AKS node and pod status, flags pods with high
restart counts for investigation.

Usage:
    python aks_health.py --namespace eshoponweb-dev
    python aks_health.py --namespace eshoponweb-dev --threshold 5
    python aks_health.py --all-namespaces
    python aks_health.py --verbose
"""

import subprocess
import json
import argparse
import logging


# ─── ARGUMENT PARSER ────────────────────────────────────────────────────────
def get_args():
    parser = argparse.ArgumentParser(
        description="Check AKS node and pod health status"
    )
    parser.add_argument(
        "--namespace",
        default="eshoponweb-dev",
        help="Kubernetes namespace to check (default: eshoponweb-dev)"
    )
    parser.add_argument(
        "--all-namespaces",
        action="store_true",
        help="Check all project namespaces"
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=5,
        help="Restart count threshold to flag a pod (default: 5)"
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
def get_nodes() -> list:
    """Returns list of all nodes with their status."""
    logging.debug("Fetching node status")

    result = run_command([
        "kubectl", "get", "nodes",
        "--output", "json"
    ])

    if result["returncode"] != 0:
        logging.error(f"Failed to get nodes: {result['stderr']}")
        return []

    try:
        data = json.loads(result["stdout"])
        nodes = []

        for item in data.get("items", []):
            name = item["metadata"]["name"]
            conditions = item["status"].get("conditions", [])

            # Find Ready condition
            status = "Unknown"
            for condition in conditions:
                if condition["type"] == "Ready":
                    status = "Ready" if condition["status"] == "True" else "NotReady"
                    break

            # Get node info
            node_info = item["status"].get("nodeInfo", {})
            k8s_version = node_info.get("kubeletVersion", "unknown")
            os_image = node_info.get("osImage", "unknown")

            nodes.append({
                "name": name,
                "status": status,
                "k8s_version": k8s_version,
                "os_image": os_image
            })

        return nodes

    except (json.JSONDecodeError, KeyError) as e:
        logging.error(f"Failed to parse node data: {e}")
        return []


def get_pods(namespace: str) -> list:
    """Returns list of all pods in a namespace with restart counts."""
    logging.debug(f"Fetching pods in namespace: {namespace}")

    result = run_command([
        "kubectl", "get", "pods",
        "--namespace", namespace,
        "--output", "json"
    ])

    if result["returncode"] != 0:
        logging.error(f"Failed to get pods: {result['stderr']}")
        return []

    try:
        data = json.loads(result["stdout"])
        pods = []

        for item in data.get("items", []):
            name = item["metadata"]["name"]
            phase = item["status"].get("phase", "Unknown")

            # Sum restart counts across all containers
            container_statuses = item["status"].get("containerStatuses", [])
            total_restarts = sum(
                cs.get("restartCount", 0)
                for cs in container_statuses
            )

            # Get ready status
            ready_containers = sum(
                1 for cs in container_statuses
                if cs.get("ready", False)
            )
            total_containers = len(container_statuses)

            pods.append({
                "name": name,
                "namespace": namespace,
                "phase": phase,
                "ready": f"{ready_containers}/{total_containers}",
                "restarts": total_restarts
            })

        return pods

    except (json.JSONDecodeError, KeyError) as e:
        logging.error(f"Failed to parse pod data: {e}")
        return []


def check_high_restarts(pods: list, threshold: int) -> list:
    """Returns pods with restart count above threshold."""
    return [p for p in pods if p["restarts"] >= threshold]


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


# ─── MAIN ───────────────────────────────────────────────────────────────────
def main():
    args = get_args()
    setup_logging(args.verbose)

    # Determine namespaces to check
    if args.all_namespaces:
        namespaces = [
            "eshoponweb-dev",
            "eshoponweb-staging",
            "eshoponweb-prod"
        ]
    else:
        namespaces = [args.namespace]

    print("\n" + "=" * 60)
    print("   AKS Health Check — Azure Cloud CICD Platform")
    print("=" * 60)

    # ── Node status
    print("\n[ Nodes ]")
    nodes = get_nodes()

    if nodes:
        node_rows = [
            [n["name"], n["status"], n["k8s_version"]]
            for n in nodes
        ]
        headers = ["NAME", "STATUS", "K8S VERSION"]
        print(format_table(headers, node_rows))

        not_ready = [n for n in nodes if n["status"] != "Ready"]
        if not_ready:
            logging.warning(f"  ⚠️  {len(not_ready)} node(s) not ready")
        else:
            logging.info(f"  ✅  All {len(nodes)} node(s) ready")
    else:
        logging.error("  ❌  Could not retrieve node information")

    # ── Pod status per namespace
    all_flagged = []

    for namespace in namespaces:
        print(f"\n[ Pods — {namespace} ]")
        pods = get_pods(namespace)

        if not pods:
            print("  No pods found in this namespace.")
            continue

        pod_rows = [
            [p["name"], p["phase"], p["ready"], str(p["restarts"])]
            for p in pods
        ]
        headers = ["NAME", "PHASE", "READY", "RESTARTS"]
        print(format_table(headers, pod_rows))

        # Check for high restarts
        flagged = check_high_restarts(pods, args.threshold)
        all_flagged.extend(flagged)

    # ── Flagged pods summary
    print(f"\n[ Pods with Restarts >= {args.threshold} ]")
    if all_flagged:
        flagged_rows = [
            [p["namespace"], p["name"], str(p["restarts"])]
            for p in all_flagged
        ]
        flagged_headers = ["NAMESPACE", "POD NAME", "RESTARTS"]
        print(format_table(flagged_headers, flagged_rows))
        logging.warning(
            f"  ⚠️  {len(all_flagged)} pod(s) flagged — investigate with: "
            f"kubectl logs <pod-name> -n <namespace>"
        )
    else:
        print(f"  ✅  No pods with restart count >= {args.threshold}")

    # ── Overall summary
    print("\n" + "=" * 60)
    total_pods = sum(
        len(get_pods(ns)) for ns in namespaces
    )
    print(f"   Nodes checked    : {len(nodes)}")
    print(f"   Namespaces checked: {len(namespaces)}")
    print(f"   Total pods       : {total_pods}")
    print(f"   Flagged pods     : {len(all_flagged)}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()