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

- python3 installed
- create virtualenv in `tools` directory : 
  - `cd tools`
  - `virtualenv venv`
- activate virtualenv : `source venv/bin/activate`
- install requirements : `pip install -r requirements.txt`

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
