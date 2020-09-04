# Lab Guide - Day-1 - EVPN Infrastructure

## Lab topology

![lab-topology.png](lab-topology.png)

## Notes about this lab

* This lab will help to understand how to build an EVPN-VXLAN infrastructure in the following contexts
  * Use case 1 : eBGP for underlay and overlay
  * Use case 2 : ISIS for underlay and iBGP for overlay 
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

## Use case 1 : EVPN configuration guide (**under development**)

1. Underlay - ISIS
   1. On spines
   2. On leafs
2. Overlay - iBGP
   1. On spines
   2. On leaves

## Use case 2 : EVPN Configuration steps

1. Underlay view - eBGP
![eBGP-underlay.png](eBGP-underlay.png)
2. Peerings between Leaf and Spine switches should use physical interface IP
   1. On spines
      1. Configure router-id
      2. Configure ecmp : max paths 2, ecmp 2
      3. Disable default IPv4 unicast address-family in global BGP configuration
      4. Configure a peer group to make the config easy : name => underlay-leaf-sessions
      5. Use “bgp listen range” (Use a peer-filter leaf-range : name => leaf-range)
      6. Activate IPv4 session on peer group (address-family)
   2. On leafs
      1. Configure router-id
      2. Configure ecmp : max paths 2, ecmp 2
      3. Configure a peer group to make the config : name => underlay-leaf-sessions
      4. Associate neighbor (correct address) to peer group
      5. Disable default IPv4 unicast address-family in global BGP configuration
      6. Activate IPv4 session on peer group (address-family)
   3. Check BGP session between Spine and Leaf :
      1. `show ip bgp summary`
      2. `show ip bgp neighbor w.x.y.z received-routes`
      3. `show ip bgp neighbor w.x.y.z advertised-routes`
      4. **Is ECMP Ok ?**
      5. **Should you send community?**
3. Configure iBGP over the peer link (leaf only)
   1. Use a peer group : mlag-ipv4-underlay-peer
   2. Associate the mlag-peer to the peer-group
   3. Use MLAG peer-link VLAN
   4. **Is there something to do for avoiding any traffic blackholing when spine-links are down ?** 
4. Advertise VTEP reachability
   1. Advertise all loopbacks (lo0 and lo1) to BGP using route-map
      1. Create  : ip prefix-list loopback … and route-map loopback ...
      2. In the BGP conf. : redistribute
   2. Verify if the IPv4 underlay sessions are up and all loopback are reachable
      1. `show ip route`
      2. `ping` ...
5. Configure VXLAN interface `vxlan 1`
   1. Set the source interface to the correct loopback
6. Configure eBGP - EVPN for overlay
   1. Schema
![eBGP-overlay.png](eBGP-overlay.png)
   2. Use a peer group to complete config (name : overlay-leaf-sessions)
      1. Disable maximum-routes
      2. Set the update-source
      3. Peer using the loopback0 interface
   3. On Spine switches, adapt the configuration to use bgp listen range
   4. On leaf switches, adapt the configuration 
   5. Don’t forget the EVPN bgp session are “multi-hop”
   6. **Do you need to send the 'extended communities' ?**
   7. **Should the spines rewrite the next-hop ?**
7. Verify if the EVPN sessions are up : `show bgp evpn summary`

## Usefull examples (try to not cut-and-paste)

* Interface vxlan example

```
interface Vxlan1
   vxlan source-interface {{ loopback VTEP }}
```

* Access list example on vtep1

```
ip prefix-list loopback seq 10 permit {{ loopback EVPN subnet }}
ip prefix-list loopback seq 20 permit {{ looback VTEP }}

route-map loopback permit 10
   match ip address prefix-list loopback
```

* BGP snippet for leaf1

``` 
router bgp {{ asn }}
   router-id {{ BGP router ID }}
   no bgp default ipv4-unicast
   maximum-paths {{ max links to spine }} ecmp {{ ECMP number }}
   neighbor {{ peer group name for overlay session }} peer group
   neighbor {{ peer group name for overlay session }} remote-as {{ remote asn }}
   neighbor {{ peer group name for overlay session }} update-source Loopback0
   neighbor {{ peer group name for overlay session }} ebgp-multihop 2
   neighbor {{ peer group name for overlay session }} send-community extended
   neighbor {{ peer group name for overlay session }} maximum-routes 0
   neighbor {{ peer group name for underlay session }} peer group
   neighbor {{ peer group name for underlay session }} remote-as {{ remote asn }}
   neighbor {{ peer group name for underlay session }} maximum-routes 12000
   neighbor {{ peer group name for underlay session between mlag pair }} peer group
   neighbor {{ peer group name for underlay session between mlag pair }} remote-as {{ remote mlag asn }}
   neighbor {{ peer group name for underlay session between mlag pair }} next-hop-self
   neighbor {{ peer group name for underlay session between mlag pair }} send-community
   neighbor {{ spine interface }} peer group {{ peer group name for underlay session }}
   neighbor {{ spine interface }} peer group {{ peer group name for underlay session }}
   neighbor {{ spine loopback }} peer group {{ peer group name for overlay session }}
   neighbor {{ spine loopback }} peer group {{ peer group name for overlay session }}
   neighbor {{ mlag peer interface }} peer group {{ peer group name for underlay session between mlag pair }}
   redistribute connected route-map loopback
   !
   address-family evpn
      neighbor {{ peer group name for overlay session }} activate
   !
   address-family ipv4
      neighbor {{ peer group name for underlay session }} activate
      neighbor {{ peer group name for underlay session between mlag pair }} activate
!
```

* Access list example on spine1

```
ip prefix-list loopback seq 10 permit {{ loopback EVPN subnet }}

route-map loopback permit 10
   match ip address prefix-list loopback

```

* Peer filter example on spine1

```
peer-filter leaf-range
   10 match as-range {{ as range }} result accept
```

* BGP snippet for spine1

``` 
router bgp {{ asn }}
   router-id {{ BGP router-id }}
   no bgp default ipv4-unicast
   maximum-paths {{ max links to spine }} ecmp {{ ECMP number }}
   bgp listen range {{ ip subnet range for loopback }} peer-group {{ peer group name for overlay session }} peer-filter leaf-range
   bgp listen range {{ ip subnet range for loopback }} peer-group underlay-leaf-sessions peer-filter leaf-range
   neighbor {{ peer group name for overlay session }} peer group
   neighbor {{ peer group name for overlay session }} update-source Loopback0
   neighbor {{ peer group name for overlay session }} ebgp-multihop 2
   neighbor {{ peer group name for overlay session }} send-community extended
   neighbor {{ peer group name for overlay session }} maximum-routes 0
   neighbor {{ peer group name for underlay session }} peer group
   neighbor {{ peer group name for underlay session }} maximum-routes 12000
   redistribute connected route-map loopback
   !
   address-family evpn
      bgp next-hop-unchanged
      neighbor {{ peer group name for overlay session }} activate
   !
   address-family ipv4
      neighbor {{ peer group name for underlay session }} activate
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
