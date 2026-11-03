# IP addressing plan

| Device / Interface | VLAN or link | Address | Mask |
|---|---|---:|---:|
| HQ-R1 G0/0.10 | HQ IT | 10.10.10.1 | /24 |
| HQ-R1 G0/0.20 | HQ HR | 10.10.20.1 | /24 |
| HQ-R1 G0/0.30 | HQ Finance | 10.10.30.1 | /24 |
| HQ-R1 G0/0.99 | HQ Management | 10.10.99.1 | /24 |
| HQ-SW1 VLAN 99 | HQ Management | 10.10.99.2 | /24 |
| BR-R1 G0/0.10 | Branch Operations | 10.20.10.1 | /24 |
| BR-R1 G0/0.20 | Branch Sales | 10.20.20.1 | /24 |
| BR-R1 G0/0.99 | Branch Management | 10.20.99.1 | /24 |
| BR-SW1 VLAN 99 | Branch Management | 10.20.99.2 | /24 |
| HQ-R1 G0/1 | WAN | 10.255.0.1 | /30 |
| BR-R1 G0/1 | WAN | 10.255.0.2 | /30 |

DHCP excludes `.1` through `.20` in each subnet for infrastructure, statically assigned devices, and reserved addresses. Dynamic clients should receive addresses starting at `.21`.
