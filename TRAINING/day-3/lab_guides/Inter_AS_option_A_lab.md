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
- Refer to the S-IRB lab guide and solution directory to quickly set it up.  

Verify it works:  
```
leaf2#sh ip route vrf tenant-blue 
host2#ping vrf vlan50 ip 10.0.40.1 source 10.0.50.2
```

Then change the configuration of devices leaf 1 and leaf 2 and host 1: 
- On the physical interface between the leaf 1/leaf 2 (local border leaves) and host 1 (external router or the border leaf of a remote data center) we will use one vlan tag for each IP VRF: 
  - `tenant-blue` is an IP VRF. The vlan tag `1234` will be used for the IP VRF `tenant-blue`  
- in each IP VRF, we will create an EBGP session between local border leaves (leaf 1 and leaf 2) and the external router or the border leaf of a remote data center (host 1).  host 1 will use it's own ASN (host 1 wont reuse an ASN that is already used in the fabric). These BGP sessions will use the address family IPv4. No need to use EVPN address family. Peerings should use physical interface IP.    
  - leaf 1 <-> host 1
  - leaf 2 <-> host 1
- in each IP VRF, we will add an IBGP session between each local border leaf. These BGP sessions will use the address family IPv4. No need to use EVPN address family. Peerings should use int vlan IP, so we need to create a vlan and an interface vlan. We will use `next-hop-self` for this IBGP neighbor.     
  - leaf 1 <-> leaf 2
- In addition to use `redistribute connected` in the IP VRF, we can also use `redistribute static` on the external router (host 1). so we need to add some static routes in the host 1
- host 1 will be configured with some loopback (/24) in the IP VRF. These routes will be redistributed. And the loopback addresses can be used in PING between host 1 (external router or the border leaf of a remote data center) and host 2 (local server) 

Then please refer to this directory [../solutions/Inter_AS_option_A_lab](../solutions/Inter_AS_option_A_lab) to see working configuration files and a validation and troubleshooting guide.  

