## VTEPS behavior with S-IRB when there is no host route in IP   


Host Y did not talk (so there is currently no arp entry for Y).  
Host X wants to talk to host Y.  
X and Y are not in the same subnet.  
Host X sends a packet to mac dest = IRB X on local VTEP.  
Local vtep is not configured with IRB Y.  
Local vtep has no Y/32 in it's IP VRF because host Y did not talk.  
However local VTEP has several entrees in its IP VRF to reach the subnet Y/24. Local VTEP learnt the subnet Y/24 from RT 5 coming from all VTEP that has an IRB in subnet Y/24.  
Local VTEP sends a single copy of the VXLAN packet (L3 VNI is used) to one single VTEP according to its IP VRF routing table (i.e to one of the VTEP that advertised to the local VTEP the subnet Y/24 using RT5). 
So there is no ingress replication with L3 VNI, ingress replication is only for BUM with L2 VNI communication.  
This remote VTEP has an IRB in subnet Y/24 (it sent an RT5 for this subnet) and will generate ARP request for host Y.  
The ARP request will be sent locally (all ports in VLAN Y), and the ARP request will be also ingress replicated to all VTEP according to L2 VNI flood-list.  
Then VTEP which will receive ARP reply from host Y will eat it, and will generate RT2 with both MAC and IP. Finally all VTEPs will learn Host Y /32.  
And the VTEP which received the ARP reply from host Y is now able to build the frame (mac dest = host Y, mac source = int vlan Y) and does a loockup in the mac table to know on which local port host Y is connected.   
