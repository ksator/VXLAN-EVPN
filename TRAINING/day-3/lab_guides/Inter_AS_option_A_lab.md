## Inter AS option A (VRF-to-VRF or back-to-back VRF) 

Use cases examples:  
- DCI without L2 stretch between data centers. 
- connection to an external router (local border leaf <-> external router). 

## Topology description: 

![lab-topology.png](lab-topology.png) 

One fabric with:  
- 2 spines (spine 1 and spine 2) 
- 4 leaves (leaf 1, leaf 2, leaf 3, leaf 4) 
- one single host (host 2).  

In this scenario: 
- the leaves 3 and 4 are regular leaves (for local servers like host 2)   
- the host 1 is:  
  - either an external router inside the local datacenter (in that case there is one single DC with one single fabric) 
  - or a border leaf in a remote datacenter (in that case there are 2 DC in total).    
- so the leaves 1 and 2 are border leaves. 

## Instructions 

load S-IRB configuration on the devices.  

We will use one vlan tag for each IP VRF: 
- `tenant-blue` is an IP VRF. The vlan tag `1234` will be used for the IP VRF `tenant-blue`  

### Devices configuration 

The configuration of devices leaf 1 and leaf 2 (border leaves) and host 1 (external router or border leaf of a remote data center) need to be updated.  
Change their configuration to use the following: 

#### leaf 1
```
interface Ethernet5
   description host1 (external-router or remote-dc-border-leaf)
   no switchport
   no shutdown
!
interface Ethernet5.1234
   encapsulation dot1q vlan 1234
   vrf tenant-blue
   ip address 100.0.0.0/31
!
router bgp 65001
   vrf tenant-blue
      rd 123.1.1.3:12345
      route-target import 12345:12345
      route-target export 12345:12345
      redistribute connected
      router-id 123.1.1.3
      neighbor 100.0.0.1 remote-as 65101
      neighbor 100.0.0.1 maximum-routes 12000
      !
      address-family ipv4
         neighbor 100.0.0.1 activate
```

#### leaf 2 
```
interface Ethernet5
   description host1 (external-router or remote-dc-border-leaf)
   no switchport
   no shutdown
!
interface Ethernet5.1234
   encapsulation dot1q vlan 1234
   vrf tenant-blue
   ip address 100.0.0.2/31
!
router bgp 65001
   vrf tenant-blue
      rd 123.1.1.4:12345
      route-target import 12345:12345
      route-target export 12345:12345
      redistribute connected
      router-id 123.1.1.4
      neighbor 100.0.0.3 remote-as 65101
      neighbor 100.0.0.3 maximum-routes 12000
      !
      address-family ipv4
         neighbor 100.0.0.3 activate
```

#### host1 
```
vrf instance tenant-blue
ip routing vrf tenant-blue 
!
ip route vrf tenant-blue 0.0.0.0/0 200.1.0.254
!
interface Ethernet3
   description leaf1
   no switchport
   no shutd
!
interface Ethernet3.1234
   encapsulation dot1q vlan 1234
   vrf tenant-blue
   ip address 100.0.0.1/31
!
interface Ethernet4
   description leaf2
   no switchport
   no shutd
!
interface Ethernet4.1234
   encapsulation dot1q vlan 1234
   vrf tenant-blue
   ip address 100.0.0.3/31
!
interface Loopback201
   vrf tenant-blue
   ip address 200.1.0.1/24
!
interface Loopback202
   vrf tenant-blue
   ip address 200.2.0.1/24
!
router bgp 65101
   vrf tenant-blue
     router-id 45.45.45.45
     rd 45.45.45.45:12345
     route-target import 12345:12345
     route-target export 12345:12345
     local-as 65101
     neighbor 100.0.0.0 remote-as 65001
     neighbor 100.0.0.0 maximum-routes 12000
     neighbor 100.0.0.2 remote-as 65001
     neighbor 100.0.0.2 maximum-routes 12000
     redistribute connected
     redistribute static
     maximum-paths 2 ecmp 2 
     address-family IPv4
         neighbor 100.0.0.0 activate
```

## Verifications  

### Run the following commands on host 1 

Host 1 is an external router or a remote border leaf
```
host1#sh lldp neighb ethernet 3
host1#sh ip interface vrf tenant-blue brief 
host1#sh ip bgp summary vrf tenant-blue
host1#sh ip route vrf tenant-blue bgp
host1#sh ip bgp vrf tenant-blue
```
ECMP is working.  
BGP sessions are established.  
You should see some hosts (ip/32 of host 2)  
You should see the prefixes of the fabric (int vlan ip/24 in vrf tenant-blue)  
```
host1#ping vrf tenant-blue 10.0.50.2 source 200.1.0.1
``` 

PING is working. The connectivity between the 2 DC is working.   

### Run the following commands on leaf 1 

leaf 1 is a local border leaf 

```
leaf1#sh lldp neighb ethernet 5
leaf1#sh vrf tenant-blue 
leaf1#ping vrf tenant-blue 100.0.0.1 source 100.0.0.0
```
```
leaf1#sh ip bgp summary vrf tenant-blue
leaf1#sh bgp neighbors 100.0.0.1 vrf tenant-blue
```
```
leaf1#sh ip route vrf tenant-blue bgp
leaf1#sh ip route vrf tenant-blue bgp next-hop 100.0.0.1
leaf1#sh ip route vrf tenant-blue 200.1.0.0/24 bgp
leaf1#sh ip route vrf tenant-blue 200.2.0.0/24 bgp 
leaf1#sh ip route vrf tenant-blue 0.0.0.0 
```
```
leaf1#sh ip bgp vrf tenant-blue
leaf1#sh ip bgp 200.1.0.0/24 vrf tenant-blue 
```
```
leaf1#sh bgp evpn route-type ip-prefix 200.1.0.0/24 
leaf1#sh bgp neighbors 123.1.1.1 evpn advertised-routes route-type ip-prefix 200.2.0.0/24
```

### Run the following commands on leaf3 or leaf4

leaf3 and leaf4 are regular leaves (i.e to attach servers)  

```
leaf3#sh bgp neighbors 123.1.1.2 evpn received-routes route-type ip-prefix 200.1.0.0/24
leaf3#sh bgp evpn route-type ip-prefix 200.1.0.0/24 detail
leaf3#sh bgp evpn route-type ip-prefix 200.1.0.0/24 vni 12345
leaf3#sh ip route vrf tenant-blue 200.1.0.0/24 bgp
leaf3#sh ip route vrf tenant-blue 200.2.0.0/24 bgp 
leaf3#sh ip route vrf tenant-blue 0.0.0.0 
leaf3#sh ip route vrf tenant-blue bgp 
```
So leaf 3 and leaf 4 have routes to host 1 (external router or border leaf of a remote data center).  
leaf 3 and leaf 4 learnt routes advertised by host 1  

host 1 advertised IPv4 routes to leaf 1 and leaf 2. Then leaf 1 and leaf 2 generated and advertised equivalents RT5.  

### Run the following commands on host 2 

host 2 is a local sever. 

```
host2#ping vrf vlan60 200.2.0.1 source 10.0.60.2
host2#ping vrf vlan50 200.1.0.1 source 10.0.50.2
```
so host 2 can reach addresses behing host 1.  
host 1 is an external router connected to local border leaves. or host 1 is a border leaf in a remote data center.   
ip connectivity between these 2 sites is working.   
