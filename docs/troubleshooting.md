# Troubleshooting

| Symptom | Likely cause | Checks |
|---|---|---|
| OSPF neighbor absent | WAN interface down, wrong /30, OSPF not enabled | `show ip int brief`, `show ip ospf neighbor`, `show run \| section ospf` |
| VLAN clients have no DHCP | Wrong access VLAN, missing subinterface, DHCP pool mismatch | `show vlan brief`, `show ip dhcp pool`, `show ip int brief` |
| Inter-VLAN ping fails | Trunk not carrying VLAN, subinterface encapsulation mismatch | `show interfaces trunk`, `show run interface g0/0.10` |
| Switch management unreachable | VLAN 99 missing or SVI down, wrong default gateway | `show ip int brief`, `show vlan brief`, `show run \| include default-gateway` |
| Netmiko timeout | Wrong SSH endpoint/port, routing/firewall issue, SSH not enabled | Test TCP port, verify `show ip ssh`, check GNS3 port mapping |
| Authentication failure | Credentials mismatch or local user missing | Verify `.env`, `show run \| section username`, `show run \| section line vty` |
| `show vlan brief` fails on router | Command is switch-specific | Expected for router; collector records command as unavailable |

## Common SSH prerequisites

On IOS devices, configure a domain name, local user, RSA key, SSH version 2, and VTY lines allowing SSH. Some images require generating the RSA key interactively; execute `crypto key generate rsa modulus 2048` in the device CLI if the pasted configuration does not generate it.
