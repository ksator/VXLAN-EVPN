from __future__ import print_function

import napalm
import sys
import os

def main():
    driver = napalm.get_network_driver("eos")
    list_devices = {"leaf1":"192.168.0.12","leaf2":"192.168.0.13","leaf3":"192.168.0.14","leaf4":"192.168.0.15","spine1":"192.168.0.10","spine2":"192.168.0.11","host1":"192.168.0.16","host2":"192.168.0.17"}
    USER="admin"
    PASSWORD="arista"
    for host,ip in list_devices.items():
        print(host)
        device=driver(hostname=ip,username=USER,password=PASSWORD,)
        print("Opening ...")
        device.open()
        print(device.get_facts())
        print("Close ...")
        device.close()
if __name__ == "__main__":
    main()
