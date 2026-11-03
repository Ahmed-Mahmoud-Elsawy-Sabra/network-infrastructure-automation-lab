# Design decisions

## Router-on-a-stick

The lab uses one 802.1Q trunk from each router to its access switch. Router subinterfaces provide the default gateway for each VLAN. This keeps the lab small and makes VLAN tagging and inter-VLAN routing visible.

## OSPF area 0

Both routers participate in a single OSPF backbone area. User and management interfaces are passive, while the WAN interface forms the adjacency. This advertises LAN prefixes without sending OSPF hellos toward end hosts.

## Dedicated management VLAN

VLAN 99 carries switch management traffic and is separate from user VLANs. In this demonstration, router subinterfaces provide the management gateway.

## Automation uses SSH

Netmiko connects to IOS devices over SSH. The inventory separates device-specific connection details from the scripts. Credentials are read from environment variables rather than committed to source control.

## Read-only automation

The supplied scripts collect state and back up running configuration. They intentionally do not push configuration changes. This reduces the risk of accidental outages and makes the first automation iteration easier to audit.

## Scope limitations

- No Internet edge or NAT is configured because the topology does not define an ISP-facing interface.
- The ACL policy is not enabled by default. Inter-VLAN policy requires an explicit business access matrix; blocking traffic arbitrarily would make the lab appear secure while breaking required services.
- The sample design is a learning lab, not a production reference architecture.
