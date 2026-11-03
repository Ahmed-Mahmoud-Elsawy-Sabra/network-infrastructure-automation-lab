from __future__ import annotations

import argparse
import json
import socket
from datetime import datetime
from pathlib import Path

from common import ROOT, LabError, connect, load_inventory


def tcp_check(host: str, port: int, timeout: float = 3.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Check management reachability and configured lab targets.")
    parser.add_argument("--inventory", default="inventory/devices.yaml")
    args = parser.parse_args()

    try:
        devices = load_inventory(args.inventory)
    except LabError as exc:
        print(f"[ERROR] {exc}")
        return 2

    results = []
    failed = False

    for device in devices:
        name, host, port = device["name"], str(device["host"]), int(device.get("port", 22))
        reachable = tcp_check(host, port)
        item = {
            "device": name,
            "host": host,
            "ssh_port": port,
            "ssh_reachable": reachable,
            "ping_targets": [],
        }
        print(f"[{'OK' if reachable else 'FAIL'}] {name}: TCP/{port} {host}")
        if not reachable:
            failed = True
            results.append(item)
            continue

        connection = None
        try:
            connection = connect(device)
            for target in device.get("ping_targets", []):
                output = connection.send_command(f"ping {target}", read_timeout=20)
                success = "!!!!" in output or "Success rate is 100 percent" in output
                item["ping_targets"].append({"target": target, "reachable": success})
                print(f"  [{'OK' if success else 'FAIL'}] ping {target}")
                if not success:
                    failed = True
        except Exception as exc:
            item["error"] = str(exc)
            failed = True
            print(f"  [FAIL] Device-side checks: {exc}")
        finally:
            if connection:
                connection.disconnect()
        results.append(item)

    report_dir = ROOT / "reports"
    report_dir.mkdir(exist_ok=True)
    report_path = report_dir / f"connectivity-{datetime.now():%Y%m%d-%H%M%S}.json"
    report_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nReport: {report_path.relative_to(ROOT)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
