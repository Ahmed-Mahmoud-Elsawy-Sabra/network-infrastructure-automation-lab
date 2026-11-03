from __future__ import annotations

import argparse
import json
from datetime import datetime

from common import ROOT, LabError, connect, load_inventory

COMMANDS = {
    "show_version": "show version",
    "interfaces": "show ip interface brief",
    "routing_table": "show ip route",
    "vlans": "show vlan brief",
    "ospf_neighbors": "show ip ospf neighbor",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect operational information from Cisco lab devices.")
    parser.add_argument("--inventory", default="inventory/devices.yaml")
    args = parser.parse_args()

    try:
        devices = load_inventory(args.inventory)
    except LabError as exc:
        print(f"[ERROR] {exc}")
        return 2

    report = {
        "collected_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "devices": [],
    }
    failures = 0

    for device in devices:
        connection = None
        record = {"name": device["name"], "host": device["host"], "commands": {}}
        try:
            print(f"[INFO] Collecting from {device['name']}...")
            connection = connect(device)
            for key, command in COMMANDS.items():
                try:
                    record["commands"][key] = connection.send_command(command, read_timeout=30)
                except Exception as exc:
                    record["commands"][key] = f"Command unavailable: {exc}"
            print(f"[OK] Collected {device['name']}")
        except Exception as exc:
            failures += 1
            record["error"] = str(exc)
            print(f"[FAIL] {device['name']}: {exc}")
        finally:
            if connection:
                connection.disconnect()
        report["devices"].append(record)

    report_dir = ROOT / "reports"
    report_dir.mkdir(exist_ok=True)
    output = report_dir / f"device-inventory-{datetime.now():%Y%m%d-%H%M%S}.json"
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nReport: {output.relative_to(ROOT)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
