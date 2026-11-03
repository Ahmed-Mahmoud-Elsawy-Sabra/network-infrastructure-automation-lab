from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")


class LabError(Exception):
    """Raised for invalid lab configuration or device connection failures."""


def load_inventory(path: str | Path) -> list[dict[str, Any]]:
    inventory_path = Path(path)
    if not inventory_path.is_absolute():
        inventory_path = ROOT / inventory_path

    if not inventory_path.exists():
        raise LabError(
            f"Inventory not found: {inventory_path}. "
            "Copy inventory/devices.example.yaml to inventory/devices.yaml."
        )

    data = yaml.safe_load(inventory_path.read_text(encoding="utf-8")) or {}
    devices = data.get("devices")
    if not isinstance(devices, list) or not devices:
        raise LabError("Inventory must contain a non-empty 'devices' list.")

    required = {"name", "host", "device_type"}
    for index, device in enumerate(devices, start=1):
        missing = required - device.keys()
        if missing:
            raise LabError(f"Device #{index} is missing: {', '.join(sorted(missing))}")
        device.setdefault("port", 22)
    return devices


def connection_params(device: dict[str, Any]) -> dict[str, Any]:
    username = os.getenv("NET_USERNAME")
    password = os.getenv("NET_PASSWORD")
    if not username or not password:
        raise LabError("Set NET_USERNAME and NET_PASSWORD in your .env file.")

    params = {
        "device_type": device["device_type"],
        "host": str(device["host"]),
        "port": int(device.get("port", 22)),
        "username": username,
        "password": password,
        "conn_timeout": 10,
        "auth_timeout": 10,
        "banner_timeout": 15,
        "fast_cli": False,
    }
    secret = os.getenv("NET_SECRET", "")
    if secret:
        params["secret"] = secret
    return params


def connect(device: dict[str, Any]):
    try:
        connection = ConnectHandler(**connection_params(device))
        if os.getenv("NET_SECRET"):
            connection.enable()
        return connection
    except (NetmikoAuthenticationException, NetmikoTimeoutException) as exc:
        raise LabError(f"{device['name']} ({device['host']}): {exc}") from exc
    except OSError as exc:
        raise LabError(f"{device['name']} ({device['host']}): {exc}") from exc


def safe_filename(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "-_." else "_" for ch in value)
