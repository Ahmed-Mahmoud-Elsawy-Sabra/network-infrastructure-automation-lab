# Topology build guide

## Nodes

Create four network devices:
- `HQ-R1`: Cisco IOS router
- `BR-R1`: Cisco IOS router
- `HQ-SW1`: Layer 2 Cisco switch
- `BR-SW1`: Layer 2 Cisco switch

Add at least one test PC in each user VLAN. A single PC per VLAN is enough for initial validation.

## Links

| From | Interface | To | Interface | Purpose |
|---|---|---|---|---|
| HQ-R1 | G0/0 | HQ-SW1 | G0/1 | 802.1Q trunk |
| HQ-R1 | G0/1 | BR-R1 | G0/1 | Routed WAN |
| BR-R1 | G0/0 | BR-SW1 | G0/1 | 802.1Q trunk |

If your router image uses `e0/0`, `g0/0/0`, or another interface naming scheme, update the config files accordingly.

## GNS3 SSH access

For each node, enable SSH in the IOS configuration and configure a reachable management path. In GNS3, configure the console/auxiliary or node adapter access as appropriate for your appliance. If using GNS3's built-in TCP console/SSH mapping, record the mapped host and port in `inventory/devices.yaml`.

The example inventory uses:
- HQ-R1: `127.0.0.1:5001`
- BR-R1: `127.0.0.1:5002`
- HQ-SW1: `127.0.0.1:5003`
- BR-SW1: `127.0.0.1:5004`

These are placeholders, not guaranteed GNS3 defaults. Replace them with the actual SSH endpoints exposed by your setup. Netmiko requires an SSH service, not a raw GNS3 console TCP port.

## Packet Tracer alternative

Use equivalent router and switch models, connect the links above, then paste the configuration snippets. Packet Tracer's supported commands vary by device model. Save your own `.pkt` file locally and optionally add it to a separate release if licensing and repository size permit.
