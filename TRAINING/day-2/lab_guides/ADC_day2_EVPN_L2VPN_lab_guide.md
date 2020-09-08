# Lab Guide - Day-1 - EVPN Infrastructure

## Lab topology

![lab-topology.png](lab-topology.png)

## Notes about this lab

* This is not a “push-command” lab (except for IP addresses config. Or some basic stuff)
  * Try the commands
  * It could have some basic missing and traps
  * The goal is not to finish absolutely but more for understanding
  * Lab will be available
* **If it is a new training session (different from day-1 and day-2) : Save on each box the initial-configurations for later-purposes**
  * `copy running-configuration flash:init_conf_ADC.eos`
* **If it is the same training session from day-1 and day-2 : Restore the initial configuration on Spine1, Spine2, Leaf1, Leaf2, Leaf3, Leaf4**
  * `Configuration replace flash:init_conf_ADC.eos`
* Don’t forget to save your running-configuration frequently.
  * `copy running-configuration startup-configuration`
  * or `wr`
* If you don’t finish the lab :
  * don’t worry about it
  * You’ll have the lab to practice later on

## Lab conventions

* Contain services, addressing scheme and conventions
* Located [here](https://github.com/krikoon73/VXLAN-EVPN/blob/master/lab-conventions.md)

## ADC initial configurations

* Use this if you are going to start from day-1 only
* Copy to each devices the configurations localized in day-1/solutions

## L2VPN configuration

1. Overview

![l2vpn-overview.png](l2vpn-overview.png)

2. Configure VLAN and trunks
   1. Use diagram to understand what VLANs need to be created
   2. Verify MAC learning and ports

3. Configure MAC-VRF
   1. Check the ASN for sure (iBGP or eBGP overlay use case)
   2. VLAN based
      1. RD should be RID:VNI
      2. RT should be VTEP:VLAN
   3. Verify Type-3 exchange
   4. Verify BGP for Type-2 routes
   5. Verify VXLAN and MAC tables

* Test reachability from Host1 to Host2 and vice versa
* Test failover by disabling uplink of a leaf pair to Spine
* Make sure there is no packet loss

## Configuration templates

* vlan configuration

```
vlan {{ vlan_id }}
```

* L2 VNI configuration

```
interface vxlan 1
  vxlan vlan {{ vlan_id }} vni {{ l2_vni }}
```

* MAC VRF configuration (vlan based)

```
router bgp {{ asn }}
  vlan {{ vlan_id }}
    rd {{ router_id }}:{{ vlan_id }} 
    route-target both {{ vlan_id }}:{{ vlan_id }} 
    redistribute learned
```
