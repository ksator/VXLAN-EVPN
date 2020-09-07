## Topology  

![lab-topology.png](lab-topology.png)

![IRB-S-overview.png](IRB-S-overview.png)   

VLAN40 (S1) VLAN45 (S2) are only on VTEP 1.1.1.1  
VLAN50 (S3) VLAN55 (S4) are only on VTEP 2.2.2.2  
VLAN60 (S5) is stretched across all VTEPs with VNI to VLAN mapping  

## Instructions 

We will use the configuration files located in the directory [EVPN_VXLAN_troubleshooting](/TRAINING/day-2/initial_conf/EVPN_VXLAN_troubleshooting).  
There are many ways to do it. See below options.  

Note: The configuration files are not correct. So the lab wont work. The purpose of this lab is to practice EVPN-VXLAN troubleshooting.  



Option A:  
- ssh each device. Then: 
  - Run this command: `#configure replace flash:init_conf_ADC.eos` 
  - then copy and paste the configuration files located in the directory [EVPN_VXLAN_troubleshooting](/TRAINING/day-2/initial_conf/EVPN_VXLAN_troubleshooting)

Option B: 
- ssh the ATD jump host 
```
*****************************************
*****Jump Host for Arista Test Drive*****
*****************************************


==========Main Menu==========

Please select from the following options: 
1. Reset All Devices to Base ATD (reset)
2. MLAG Lab (mlag)
3. BGP Lab (bgp)
4. VXLAN Lab (vxlan) excludes leaf3 instead of leaf4
5. EVPN Type 2 Lab (l2evpn) excludes leaf3 instead of leaf4
6. EVPN Type 5 Lab (l3evpn) excludes leaf3 instead of leaf4
7. CVP lab (cvp)


97. Additional Labs (labs)
98. SSH to Devices (ssh)
99. Exit LabVM (quit/exit) - CTRL + c

What would you like to do?: 
```
and select the option `1` (Reset All Devices to Base ATD) 
- then ssh each device and copy and paste the configuration files located in the directory [EVPN_VXLAN_troubleshooting](/TRAINING/day-2/initial_conf/EVPN_VXLAN_troubleshooting)

Option C:
- open a shell session on the ATD jump host
- run this command `python nornir-push-config.py --action reset` 
- then ssh each device and copy and paste the configuration files located in the directory [EVPN_VXLAN_troubleshooting](/TRAINING/day-2/initial_conf/EVPN_VXLAN_troubleshooting)


## Run the following tests

#### L2 ping

```
host2#ping vrf vlan60 10.0.60.1 source 10.0.60.2
```
It doesnt work 

#### L3 ping

```
host2#ping vrf vlan50 ip 10.0.40.1 source 10.0.50.2
```

It doesnt work 

#### Spot the root causes and fix the issues 

Refer to the network diagramm and use the various show commands we discussed to spot and fix all issues  

Some of the issues are blocking (i.e some traffic is broken) and some other issues are not blocking (i.e the traffic passes but it is not optimal i.e think about ecmp, flooding, some bgp neighbors are not established ....). 

Try to not use the [solution](/TRAINING/day-2/solutions/Troubleshooting_lab)
