# Validation and acceptance tests

Run these checks after applying the configs.

## Layer 2

On each switch:
```text
show vlan brief
show interfaces trunk
show spanning-tree summary
```
Expected:
- HQ VLANs 10, 20, 30, 99 exist.
- Branch VLANs 10, 20, 99 exist.
- The router-facing uplink is trunking and allows only the site VLANs.

## Layer 3

On each router:
```text
show ip interface brief
show ip route
show ip ospf neighbor
show ip protocols
```
Expected:
- Router subinterfaces and WAN interface are up/up.
- One OSPF neighbor is FULL on the WAN link.
- HQ learns `10.20.10.0/24`, `10.20.20.0/24`, and `10.20.99.0/24`.
- Branch learns the HQ VLAN networks.

## DHCP

On clients, request DHCP and verify:
- Correct subnet for the access VLAN.
- Correct default gateway.
- DNS servers `1.1.1.1` and `8.8.8.8`.

On routers:
```text
show ip dhcp binding
show ip dhcp pool
```

## End-to-end tests

From an HQ IT PC:
- Ping `10.10.10.1`.
- Ping a host in another HQ VLAN if the chosen policy allows it.
- Ping `10.20.10.1` and a Branch client.

From a Branch Operations PC:
- Ping `10.20.10.1`.
- Ping `10.10.10.1` and an HQ client.

## Python automation

1. Confirm SSH works manually from the automation host.
2. Run `collect_info.py` and inspect the JSON report.
3. Run `check_connectivity.py` and inspect reachability results.
4. Run `backup_configs.py` and verify a config file exists for each device.
5. Confirm no credentials appear in the generated reports or backups.

A test is not passed merely because a command ran. Record actual output/screenshots in your project evidence.
