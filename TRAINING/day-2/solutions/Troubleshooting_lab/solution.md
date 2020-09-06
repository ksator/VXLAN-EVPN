## host2 interfaces are op down

```
leaf3(config-router-bgp)#interface ethernet 4
leaf3(config-if-Et4)#no shutdown 
```
```
leaf4(config-router-bgp)#interface ethernet 4
leaf4(config-if-Et4)#no shutdown 
```
```
host2#sh lldp neighbors
```

## ecmp is broken on leaf 1 and leaf 2

```
sh ip bgp vrf all
sh ip route vrf all bgp
```

```
router bgp  65001 
   maximum-paths 2 ecmp 2
```
   

## mac vrf issues 

### `redistribute learned` is not configured on leaf 3/leaf 4

So there is no mac learning via evpn so it works only with flooding
 
```
leaf3(config-macvrf-60)#sh active 
router bgp 65001
   vlan 60
      rd 123.1.1.3:60
      route-target both 60:60
leaf3(config-macvrf-60)#
```

Add `redistribute learned` to this mac vrf on leaf 3 and leaf 4

### RT mismatch (leaf 1/leaf 2 vs leaf 3/leaf 4)

#### leaf 1/leaf 2 use 1060:1060 

```
leaf1(config-macvrf-60)#sh active 
router bgp 65001
   vlan 60
      rd 123.1.1.3:60
      route-target both 1060:1060
      redistribute learned
leaf1(config-macvrf-60)#
```

#### leaf 3/leaf 4 use 60:60  
```
leaf3(config-macvrf-60)#sh active 
router bgp 65001
   vlan 60
      rd 123.1.1.5:60
      route-target both 60:60
leaf3(config-macvrf-60)#
```

so there is no flood list for the vni 60 (and there are many other issues ...)   
Use the same RT for all devices for this mac vrf 

### l2 vni is not defined for vlan 60 on leaf 3/leaf 4

```
leaf3(config-if-Vx1)#sh active
interface Vxlan1
   vxlan source-interface Loopback1
   vxlan udp-port 4789
   vxlan vlan 50 vni 50
   vxlan vlan 55 vni 55
   vxlan vrf tenant-blue vni 12345
```

```
sh vxlan vni 
sh run int vxlan 1
```

Add the l2vni 60 for the vlan 60 on these 2 devices 


#### extended community is not configured for the overlay neighbors on leaf 4 

By default the devices dont send ext communities.  

```
leaf4#sh run section bgp
leaf4#sh bgp neighbors 123.1.1.1 | grep comm 
leaf4#sh bgp neighbors 123.1.1.2 | grep comm 
```

so the ext community RT (as well as the other communities) are not sent   
leaf 1 doesnt receive ext communities (RT ...) from leaf 4, so leaf 1 doesnt learn from leaf4 mac addresses and arp entries.   

```
leaf1#sh bgp evpn route-type mac-ip 10.0.60.2 detail 
leaf1#sh mac address-table address 001c.734b.97ec 
leaf1#sh ip arp vrf all 10.0.60.2
```
```
leaf4#configure 
leaf4(config)#router bgp 65002 
leaf4(config-router-bgp)#neighbor overlay-leaf-sessions send-community extended
```





