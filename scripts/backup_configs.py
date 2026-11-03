from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from common import ROOT, LabError, connect, load_inventory, safe_filename


def main() -> int:
    parser = argparse.ArgumentParser(description="Back up running configurations from lab devices.")
    parser.add_argument("--inventory", default="inventory/devices.yaml")
    args = parser.parse_args()

    try:
        devices = load_inventory(args.inventory)
    except LabError as exc:
        print(f"[ERROR] {exc}")
        return 2

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = ROOT / "backups" / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)
    failures = 0

    for device in devices:
        connection = None
        try:
            print(f"[INFO] Connecting to {device['name']}...")
            connection = connect(device)
            config = connection.send_command("show running-config", read_timeout=45)
            if not config.strip():
                raise LabError("Device returned an empty running configuration.")
            output_file = output_dir / f"{safe_filename(device['name'])}.cfg"
            output_file.write_text(config.rstrip() + "\n", encoding="utf-8")
            print(f"[OK] Saved {output_file.relative_to(ROOT)}")
        except Exception as exc:
            failures += 1
            print(f"[FAIL] {device['name']}: {exc}")
        finally:
            if connection:
                connection.disconnect()

    print(f"\nBackup complete: {len(devices) - failures}/{len(devices)} devices successful.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
