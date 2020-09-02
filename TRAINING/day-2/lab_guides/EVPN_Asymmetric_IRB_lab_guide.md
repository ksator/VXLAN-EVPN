## Topology 

![IRB-A-overview.png](IRB-A-overview.png)    

## Instructions  

This scenario is meant to be built on top of Scenario A.  

Configure VLAN and trunks  
- Use the diagram and do the VLAN and trunk config  

Configure VXLAN mappings  
- Configure VLAN-to-VNI mappings using the format VLAN = VNI  
- Verify the data-plane configuration  

Configure MAC-VRF  
- You use Vlan-based for VLAN 25  
- Vlan-based  
   - RD should be VTEP:VNI
   - RT should be VNI:VLAN
   - Redistribute learned MACs
- Vlan-aware bundle for 20 and 30
   - RD should be VTEP:2030
   - RT should be 2030:2030
   - Redistribute learned MACs
- Verify Type-3 exchange
- Verify BGP for Type-2 routes
- VLAN-aware bundle do we need ETID?
	
Configure IRB
- Based on the diagram enable the IRB
- Configure address virtual .254 on all
- Verify MAC+IP presence in EVPN
- Verify ARP/MAC table

Verify the following
- Host to host reachability within same VLAN
- Host to Gateway reachability
- Host to host reachability inter VLAN
- Do we have ECMP

## Configuration templates

- VLAN-to-VNI mappings  
```
vlan {{ vlan_id }} 
!
interface Vxlan1
   vxlan vlan {{ vlan_id }} vni {{ l2_vni }}
```
- IRB configuration 
```
ip virtual-router mac-address {{ virtual_mac_address }}
!
interface Vlan{{ vlan_id }} 
   ip address virtual {{ virtual_ip }}/{{ subnet }}
```
- Vlan-based service interface 
```
router bgp {{ asn }}
   vlan {{ vlan_id }}
  	rd {{ router_id }}:{{ vlan_id }} 
  	route-target both {{ vlan_id }}:{{ vlan_id }} 
  	redistribute learned
```
- Vlan-aware bundle service interface 
```
router bgp {{ asn }}
   vlan-aware-bundle {{ bundle_name }} 
  	rd {{ router_id }}:2030
  	route-target both 2030:2030
  	redistribute learned
  	vlan {{ vlan_id }},{{ vlan_id }}
```

