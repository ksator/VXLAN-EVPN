# Lab Guide - Day-1 - EVPN Infrastructure

## Lab topology

![lab-topology.png](lab-topology.png)

## Notes about this lab

* This lab will help to understand how to build an EVPN-VXLAN infrastructure in the following context
  * eBGP underlay
  * eBGP overlay
  * **Notes** :
    * it is easy to translate it to an IGP underlay model by configuring RR on the spines for the overlay session. 
    * the purpose of the training is to focus on EVPN and underlay is just a "transport" method.
* This is not a “push-command” lab (except for IP addresses config. Or some basic stuff)
  * Try the commands
  * It could have some basic missing and traps
  * The goal is not to finish absolutely but more for understanding
  * Lab will be available after the training
* **Save on each box the initial-configurations for later-purposes or mistakes**
  * `copy running-config flash:init_conf_ADC.eos`
* Don’t forget to save your running-configuration frequently.
  * `copy running-config startup-configuration`
  * `wr`
* If you don’t finish the lab :
  * don’t worry about it
  * We will use pre-configured stuff for the next labs

## Lab conventions

* Contain services, addressing scheme and conventions
* Located [here](https://github.com/krikoon73/VXLAN-EVPN/blob/master/lab-conventions.md)

## ADC initial configurations

* Use this if you are going to start from here : [Initial configurations](https://github.com/krikoon73/VXLAN-EVPN/tree/master/TRAINING/day-1/initial_conf)
* Copy all these configurations to the boxes.
* Save the new configuration for later purposes or mistakes : **`copy running-config flash:init_IP_connectivity.eos`**

## EVPN Configuration steps

1. Underlay view - eBGP
![eBGP-underlay.png](eBGP-underlay.png)
2. Peerings between Leaf and Spine switches should use physical interface IP
   1. On spines
      1. Configure ecmp : max paths 2, ecmp 2
      2. Configure a peer-filter leaf-range : name => leaf-range
      3. Configure a peer group to make the config : name => underlay-leaf-sessions
      4. Associate neighbor to peer group
      5. Use “bgp listen range”
      6. Disable default IPv4 unicast address-family in global BGP configuration
      7. Activate IPv4 session on peer group (address-family)
   2. On leafs
      1. Configure ecmp : max paths 2, ecmp 2
      2. Configure a peer group to make the config : name => underlay-leaf-sessions
      3. Associate neighbor to peer group
      4. Disable default IPv4 unicast address-family in global BGP configuration
      5. Activate IPv4 session on peer group (address-family)
   3. Check BGP session between Spine and Leaf : 
      1. `show ip bgp summary`
      2. `show ip bgp neighbor w.x.y.z received-routes`
      3. `show ip bgp neighbor w.x.y.z advertised-routes`
3. Configure iBGP over the peer link (leaf only)
   1. Use a peer group : mlag-ipv4-underlay-peer
   2. Associate the mlag-peer to the peer-group
   3. Use MLAG peer-link VLAN
      1. (Shutdown the iBGP session) 
      2. (more preferable in vEOS-lab)
4. Advertise VTEP reachability
   1. Advertise all loopbacks (lo0 and lo1) to BGP using route-map
      1. Create  : ip prefix-list loopback … and route-map loopback ...
      2. In the BGP conf. : redistribute connected route-map loopback
   2. Verify if the IPv4 underlay sessions are up and loopback are reachable
      1. `show ip route`
      2. `ping` ...
5. Configure VXLAN interface
   1. Enable interface `vxlan 1` and set the source interface to loopback 1
6. Configure eBGP - EVPN for overlay
   1. Schema
![eBGP-overlay.png](eBGP-overlay.png)
   2. Use peer group to complete config (name : overlay-leaf-session)
      1. Disable maximum-routes
      2. Set the update-source
      3. Peer using the loopback0 interface
   3. On Spine switches use bgp listen range
   4. Don’t forget the EVPN bgp session are “multi-hop”
   5. Don’t forget to send the extended community
   6. Don’t forget that the spines is a route-server in case of EVPN
   7. Don’t forget to activate the EVPN neighbord in the right address-familly
   8. Don’t forget that EVPN require ArBGP enable (of course)
7. Verify if the EVPN sessions are up : `show bgp evpn summary`

## Usefull examples (try to not cut-and-paste)

* Interface vxlan example

```
interface Vxlan1
   vxlan source-interface Loopback1
```

* Access list example on vtep1

```
ip prefix-list loopback seq 10 permit 123.1.1.0/24 le 32
ip prefix-list loopback seq 20 permit 1.1.1.1/32

route-map loopback permit 10
   match ip address prefix-list loopback
```

* BGP snippet for leaf1

``` 
router bgp 65001
   router-id 123.1.1.3
   no bgp default ipv4-unicast
   maximum-paths 2 ecmp 2
   neighbor overlay-leaf-sessions peer group
   neighbor overlay-leaf-sessions remote-as 65000
   neighbor overlay-leaf-sessions update-source Loopback0
   neighbor overlay-leaf-sessions ebgp-multihop 2
   neighbor overlay-leaf-sessions send-community extended
   neighbor overlay-leaf-sessions maximum-routes 0
   neighbor underlay-leaf-sessions peer group
   neighbor underlay-leaf-sessions remote-as 65000
   neighbor underlay-leaf-sessions maximum-routes 12000
   neighbor mlag-ipv4-underlay-peer peer group
   neighbor mlag-ipv4-underlay-peer remote-as 65001
   neighbor mlag-ipv4-underlay-peer next-hop-self
   neighbor mlag-ipv4-underlay-peer send-community
   neighbor 10.0.0.0 peer group underlay-leaf-sessions
   neighbor 10.0.0.8 peer group underlay-leaf-sessions
   neighbor 123.1.1.1 peer group overlay-leaf-sessions
   neighbor 123.1.1.2 peer group overlay-leaf-sessions
   neighbor 172.16.1.1 peer group mlag-ipv4-underlay-peer
   redistribute connected route-map loopback
   !
   address-family evpn
      neighbor overlay-leaf-sessions activate
   !
   address-family ipv4
      neighbor underlay-leaf-sessions activate
      neighbor 172.16.1.1 activate
!
```

* Access list example on spine1

```
ip prefix-list loopback seq 10 permit 123.1.1.0/24 le 32

route-map loopback permit 10
   match ip address prefix-list loopback

```

* Peer filter example on spine1

```
peer-filter leaf-range
   10 match as-range 65001-65004 result accept
```

* BGP snippet for spine1

``` 
router bgp 65000
   router-id 123.1.1.1
   no bgp default ipv4-unicast
   maximum-paths 2 ecmp 2
   bgp listen range 123.0.0.0/8 peer-group overlay-leaf-sessions peer-filter leaf-range
   bgp listen range 10.0.0.0/8 peer-group underlay-leaf-sessions peer-filter leaf-range
   neighbor overlay-leaf-sessions peer group
   neighbor overlay-leaf-sessions update-source Loopback0
   neighbor overlay-leaf-sessions ebgp-multihop 2
   neighbor overlay-leaf-sessions send-community extended
   neighbor overlay-leaf-sessions maximum-routes 0
   neighbor underlay-leaf-sessions peer group
   neighbor underlay-leaf-sessions maximum-routes 12000
   redistribute connected route-map loopback
   !
   address-family evpn
      bgp next-hop-unchanged
      neighbor overlay-leaf-sessions activate
   !
   address-family ipv4
      neighbor underlay-leaf-sessions activate
```

* ArBGP Activation

```
service routing protocols model multi-agent
```

## Ip adressing scheme

<table>
  <tr>
   <td><strong>Device</strong>
   </td>
   <td><strong>Interface</strong>
   </td>
   <td><strong>IP</strong>
   </td>
  </tr>
  <tr>
   <td><strong>spine1</strong>
   </td>
   <td><strong>ma1</strong>
   </td>
   <td><strong>192.168.0.10</strong>
   </td>
  </tr>
  <tr>
   <td>spine1
   </td>
   <td>et2
   </td>
   <td>10.0.0.0/31
   </td>
  </tr>
  <tr>
   <td>spine1
   </td>
   <td>et3
   </td>
   <td>10.0.0.2/31
   </td>
  </tr>
  <tr>
   <td>spine1
   </td>
   <td>et4
   </td>
   <td>10.0.0.4/31
   </td>
  </tr>
  <tr>
   <td>spine1
   </td>
   <td>et5
   </td>
   <td>10.0.0.6/31
   </td>
  </tr>
  <tr>
   <td>spine1
   </td>
   <td>lo0
   </td>
   <td>123.1.1.1/32
   </td>
  </tr>
  <tr>
   <td><strong>spine2</strong>
   </td>
   <td><strong>ma1</strong>
   </td>
   <td><strong>192.168.0.11</strong>
   </td>
  </tr>
  <tr>
   <td>spine2
   </td>
   <td>et1
   </td>
   <td>172.16.1.0/31
   </td>
  </tr>
  <tr>
   <td>spine2
   </td>
   <td>et2
   </td>
   <td>10.0.0.8/31
   </td>
  </tr>
  <tr>
   <td>spine2
   </td>
   <td>et3
   </td>
   <td>10.0.0.10/31
   </td>
  </tr>
  <tr>
   <td>spine2
   </td>
   <td>et4
   </td>
   <td>10.0.0.12/31
   </td>
  </tr>
  <tr>
   <td>spine2
   </td>
   <td>et5
   </td>
   <td>10.0.0.14/31
   </td>
  </tr>
  <tr>
   <td>spine2
   </td>
   <td>lo0
   </td>
   <td>123.1.1.2/32
   </td>
  </tr>
  <tr>
   <td><strong>leaf1</strong>
   </td>
   <td><strong>ma1</strong>
   </td>
   <td><strong>192.168.0.14</strong>
   </td>
  </tr>
  <tr>
   <td>leaf1
   </td>
   <td>et1
   </td>
   <td>172.16.1.0/31
   </td>
  </tr>
  <tr>
   <td>leaf1
   </td>
   <td>et2
   </td>
   <td>10.0.0.1/31
   </td>
  </tr>
  <tr>
   <td>leaf1
   </td>
   <td>et3
   </td>
   <td>10.0.0.9/31
   </td>
  </tr>
  <tr>
   <td>leaf1
   </td>
   <td>lo0
   </td>
   <td>123.1.1.3/32
   </td>
  </tr>
  <tr>
   <td>leaf1
   </td>
   <td>lo1
   </td>
   <td>1.1.1.1/32
   </td>
  </tr>
  <tr>
   <td><strong>leaf2</strong>
   </td>
   <td><strong>ma1</strong>
   </td>
   <td><strong>192.168.0.15</strong>
   </td>
  </tr>
  <tr>
   <td>leaf2
   </td>
   <td>et1
   </td>
   <td>172.16.1.1/31
   </td>
  </tr>
  <tr>
   <td>leaf2
   </td>
   <td>et2
   </td>
   <td>10.0.0.3/31
   </td>
  </tr>
  <tr>
   <td>leaf2
   </td>
   <td>et3
   </td>
   <td>10.0.0.11/31
   </td>
  </tr>
  <tr>
   <td>leaf2
   </td>
   <td>lo0
   </td>
   <td>123.1.1.4/32
   </td>
  </tr>
  <tr>
   <td>leaf2
   </td>
   <td>lo1
   </td>
   <td>1.1.1.1/32
   </td>
  </tr>
  <tr>
   <td><strong>leaf3</strong>
   </td>
   <td><strong>ma1</strong>
   </td>
   <td><strong>192.168.0.16</strong>
   </td>
  </tr>
  <tr>
   <td>leaf3
   </td>
   <td>et1
   </td>
   <td>172.16.1.0/31
   </td>
  </tr>
  <tr>
   <td>leaf3
   </td>
   <td>et2
   </td>
   <td>10.0.0.5/31
   </td>
  </tr>
  <tr>
   <td>leaf3
   </td>
   <td>et3
   </td>
   <td>10.0.0.13/31
   </td>
  </tr>
  <tr>
   <td>leaf3
   </td>
   <td>lo0
   </td>
   <td>123.1.1.5/32
   </td>
  </tr>
  <tr>
   <td>leaf3
   </td>
   <td>lo1
   </td>
   <td>2.2.2.2/32
   </td>
  </tr>
  <tr>
   <td><strong>leaf4</strong>
   </td>
   <td><strong>ma1</strong>
   </td>
   <td><strong>192.168.0.17</strong>
   </td>
  </tr>
  <tr>
   <td>leaf4
   </td>
   <td>et1
   </td>
   <td>172.16.1.1/31
   </td>
  </tr>
  <tr>
   <td>leaf4
   </td>
   <td>et2
   </td>
   <td>10.0.0.7/31
   </td>
  </tr>
  <tr>
   <td>leaf4
   </td>
   <td>et3
   </td>
   <td>10.0.0.15/31
   </td>
  </tr>
  <tr>
   <td>leaf4
   </td>
   <td>lo0
   </td>
   <td>123.1.1.6/32
   </td>
  </tr>
  <tr>
   <td>leaf4
   </td>
   <td>lo1
   </td>
   <td>2.2.2.2/32
   </td>
  </tr>
</table>
