# Network Infrastructure Automation Lab

A small two-site enterprise network lab built around Cisco IOS-style configurations and Python-based network automation.

The lab demonstrates:
- VLAN segmentation and 802.1Q trunking
- Router-on-a-stick inter-VLAN routing
- OSPF area 0 between HQ and Branch
- DHCP scopes for user VLANs
- Management addressing and SSH access
- Basic ACL examples
- Python automation with Netmiko: configuration backups, device inventory, and reachability checks

> **Important:** This repository contains the design, configuration templates, and automation code. It does not include a native Packet Tracer `.pkt` or GNS3 project file. Build the topology using the guide in `docs/topology.md`, then apply the matching configs. GNS3 device images and Packet Tracer files are vendor/tool-specific and cannot be generated reliably as plain text.

## Topology

```text
                     HQ (Cairo)                              Branch (Alexandria)
              +----------------------+                    +----------------------+
              |       HQ-R1          |                    |       BR-R1          |
              | G0/0 trunk to HQ-SW1  |                    | G0/0 trunk to BR-SW1 |
              | G0/1 WAN              |====================| G0/1 WAN              |
              +----------+-----------+    OSPF area 0     +----------+-----------+
                         |                                          |
                    802.1Q trunk                               802.1Q trunk
                         |                                          |
              +----------+-----------+                    +----------+-----------+
              |       HQ-SW1         |                    |       BR-SW1         |
              +----------------------+                    +----------------------+
              VLAN 10 IT                                      VLAN 10 Operations
              VLAN 20 HR                                      VLAN 20 Sales
              VLAN 30 Finance
              VLAN 99 Management
```

## Addressing plan

| Site | VLAN / Link | Subnet | Gateway / Address |
|---|---|---|---|
| HQ | VLAN 10 IT | `10.10.10.0/24` | `10.10.10.1` |
| HQ | VLAN 20 HR | `10.10.20.0/24` | `10.10.20.1` |
| HQ | VLAN 30 Finance | `10.10.30.0/24` | `10.10.30.1` |
| HQ | VLAN 99 Management | `10.10.99.0/24` | `10.10.99.1` |
| Branch | VLAN 10 Operations | `10.20.10.0/24` | `10.20.10.1` |
| Branch | VLAN 20 Sales | `10.20.20.0/24` | `10.20.20.1` |
| WAN | HQ-R1 to BR-R1 | `10.255.0.0/30` | HQ `10.255.0.1`, Branch `10.255.0.2` |

Switch management IPs:
- HQ-SW1: `10.10.99.2/24`, gateway `10.10.99.1`
- BR-SW1: `10.20.99.2/24`, gateway `10.20.99.1`

The Branch management VLAN 99 is included for consistency even though the initial business brief only listed two user VLANs.

## Repository layout

```text
.
├── configs/
│   ├── hq-r1.cfg
│   ├── branch-r1.cfg
│   ├── hq-sw1.cfg
│   └── branch-sw1.cfg
├── inventory/
│   └── devices.example.yaml
├── scripts/
│   ├── backup_configs.py
│   ├── check_connectivity.py
│   ├── collect_info.py
│   └── common.py
├── docs/
│   ├── topology.md
│   ├── addressing-plan.md
│   ├── design-decisions.md
│   ├── validation.md
│   └── troubleshooting.md
├── backups/.gitkeep
├── reports/.gitkeep
├── .env.example
├── .gitignore
└── requirements.txt
```

## Quick start

### 1. Build the lab

Use Packet Tracer for the initial switching/routing build, or GNS3 with Cisco IOS images (or compatible appliances). Follow `docs/topology.md`. Interface names can differ by image, so adjust the configs before pasting them.

### 2. Configure devices

Review the files in `configs/` and apply them in the correct device CLI. Replace lab credentials and secrets before using the configs outside an isolated lab.

### 3. Prepare Python

Python 3.10+ is recommended.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set the lab credentials:

```env
NET_USERNAME=labadmin
NET_PASSWORD=replace-this-password
NET_SECRET=
```

Never commit `.env` or real device credentials.

### 4. Set the inventory

Copy `inventory/devices.example.yaml` to `inventory/devices.yaml`. Update management IPs, ports, and device types to match your GNS3 nodes.

The sample inventory uses `127.0.0.1` with distinct SSH ports as an example of GNS3 port mapping. If your devices are directly reachable, use their actual management IPs and SSH port `22`.

### 5. Run automation

```bash
python scripts/collect_info.py --inventory inventory/devices.yaml
python scripts/check_connectivity.py --inventory inventory/devices.yaml
python scripts/backup_configs.py --inventory inventory/devices.yaml
```

Output is written to `reports/` and `backups/`.

## Automation behavior

- `backup_configs.py`: connects over SSH, runs `show running-config`, and stores a timestamped backup per device.
- `check_connectivity.py`: checks TCP/SSH reachability, then optionally runs device-side ping tests for configured targets.
- `collect_info.py`: collects `show version`, `show ip interface brief`, `show ip route`, and `show vlan brief` where supported.

The scripts fail with a non-zero exit code if one or more devices fail. They do not modify device configuration.

## Safety notes

- Run this only against devices you own or are authorized to administer.
- Start in an isolated lab. Do not paste sample ACLs into production without reviewing the impact.
- Use unique credentials and SSH keys where supported.
- The example configs use placeholder secrets. Change them.
- Some Packet Tracer IOS features and GNS3 images differ. Treat the configs as templates and validate commands against the selected image.

## Validation checklist

See `docs/validation.md` for the complete checklist. At minimum, verify:
1. Each switch learns the expected VLANs.
2. Trunks carry only the VLANs needed at that site.
3. Hosts receive addresses from the correct DHCP scope.
4. Each router learns remote site routes through OSPF.
5. Inter-VLAN and inter-site traffic behaves as intended.
6. Python scripts can authenticate and create backups/reports.

## License

MIT. See `LICENSE`.
