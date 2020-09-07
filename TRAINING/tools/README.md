# Sample tools for pushing configuration on the devices

## Description

- [nornir-push-config.py](nornir-push-config.py) : script for resetting the initilal IP connectivity previously backuped on the device in flash (flash:init_IP_connectivity.eos) or merging a configuration of the lab
- [config.yml](config.yml) : nornir initialization file
- [groups.yml](group.yml) : nornir group initialization file
- [inventory.yml](inventory.yml) : nornir inventory initialization file
  - devices list ==> **IP address for management should be adapted in order to stick to your lab** 
  - pointers to lab configurations in the data section
- [napalm-get-facts.py](napalm-get-facts.py) : script example for getting sample facts from the devices (warning : this is not using the napalm inventory)

## Requirements

- open a shell session on the ATD jump host 
```

*****************************************
*****Jump Host for Arista Test Drive*****
*****************************************


==========Device SSH Menu==========

Screen Instructions:

* Select specific screen - Ctrl + a <number>
* Select previous screen - Ctrl + a p
* Select next screen - Ctrl + a n
* Exit all screens (return to menu) - Ctrl + a \

Please select from the following options:
1. host1 (host1)
2. host2 (host2)
3. leaf1 (leaf1)
4. leaf2 (leaf2)
5. leaf3 (leaf3)
6. leaf4 (leaf4)
7. spine1 (spine1)
8. spine2 (spine2)
9. cvx01 (cvx01)

Other Options: 
96. Screen (screen) - Opens a screen session to each of the hosts
97. Back to Previous Menu (back)
98. Shell (shell/bash)
99. Back to Main Menu (main/exit) - CTRL + c

What would you like to do? 98
arista@devbox:~$ 
```
- python3 is installed
```
arista@devbox:~$ python3 -V
Python 3.8.1
arista@devbox:~$ python -V
Python 3.8.1
```
- clone the repository (`git clone https://github.com/krikoon73/VXLAN-EVPN.git`)
- create virtualenv in `tools` directory : 
  - `arista@devbox:~$ cd VXLAN-EVPN/TRAINING/tools/`
  - `arista@devbox:~/VXLAN-EVPN/TRAINING/tools$ python -m virtualenv venv`
- activate virtualenv : `source venv/bin/activate`
- install requirements : `pip install -r requirements.txt`
- verify the requirements in the virtual env
```
(venv) arista@devbox:~/VXLAN-EVPN/TRAINING/tools$ pip list | grep 'napalm\|netmiko\|nornir'
napalm            2.5.0
netmiko           2.4.2
nornir            2.4.0
```
- test 
```
(venv) arista@devbox:~/VXLAN-EVPN/TRAINING/tools$ python napalm-get-facts.py 
```

## how to use ?

- Reset connectivity for leaf/spine/host: `python nornir-push-config.py --action reset`
- Push EVPN infrastructure :
  - ISIS use case : `python nornir-push-config.py --action push --lab infra --option isis`
  - eBGP use case : `python nornir-push-config.py --action push --lab infra --option ebgp`
- Push a specific EVPN use case :
  - L2VPN : `python nornir-push-config.py --action push --l2vpn --option l2`
  - IRB-A : `python nornir-push-config.py --action push --l2vpn --option irb-a`
  - IRB-S : `python nornir-push-config.py --action push --l2vpn --option irb-s`
  - L3VPN : `python nornir-push-config.py --action push --l3vpn --option option-a`
