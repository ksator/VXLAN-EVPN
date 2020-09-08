from __future__ import print_function
import os
import sys
import argparse

from nornir import InitNornir
from nornir.plugins.tasks import networking, text
from nornir.plugins.functions.text import print_title, print_result
from nornir.plugins.tasks.files import write_file

def device_get_facts(task):
    # Save the compiled configuration into a host variable)
    task.run(task=networking.napalm_get,getters=["config"],retrieve="all")

def device_merge_conf(task,configuration):
    config_filename = task.host.data[configuration]
    f = open(config_filename,"r")
    task.host["config"] = f.read()
    task.run(task=networking.napalm_configure,name="Loading Configuration on the device",replace=False,configuration=task.host["config"])

def device_replace_conf(task,configuration):
    my_command="configure replace flash:"+configuration
    my_command_list = [my_command]
    task.run(task=networking.napalm_cli,commands=my_command_list)

# Inialize parser
parser = argparse.ArgumentParser()
parser.add_argument("-action","--action",help="\'push\' or \'reset\' to initial configuration")
parser.add_argument("-lab","--lab",help="\'infra\' or \'l2vpn\' or \'l3vpn\'")
parser.add_argument("-underlay","--underlay",help="\'isis\' or \'ebgp\")
parser.add_argument("-option","--option",help="\'l2\' or \'irb-a\' or \'irb-b\' for \'l2vpn\', \'option-a\' for l3vpn")
args = parser.parse_args()

# Initialize nornir Filter
nr = InitNornir(config_file="config.yml", dry_run=False)
ALL = nr.filter(type="network_device")
spine = nr.filter(type="network_device", role="spine")
leaf = nr.filter(type="network_device", role="leaf")
host = nr.filter(type="network_device", role="host")

print(args.action)
print(args.lab)
print(args.option)

if args.action == "push":
    if args.lab == "underlay":
        if args.underlay == "isis" or args.underlay == "ebgp":
            config_name = args.underlay
            result_spine=spine.run(task=device_merge_conf,configuration=config_name)
            print_result(result_spine)
            result_leaf=leaf.run(task=device_merge_conf,configuration=config_name)
            print_result(result_leaf)
        else:
            print('ERROR : Bad underlay')
    elif args.lab == "l2vpn":
        if args.underlay == "ebgp" or args.underlay == "ebgp":
            if args.option == "l2" or args.option == "irb-a" or args.option == "irb=s"
                config_name = args.underlay+"-"+args.option
                result_leaf=leaf.run(task=device_merge_conf,configuration=config_name)
                print_result(result_leaf)
            else:
                print(f"Lab {args.lab} eith {args.option} is not yet implemented for {args.underlay} ")
        else:
            print('ERROR : Bad underlay')
    elif args.lab == "l3vpn":
        if args.underlay == "ebgp" or args.underlay == "ebgp":
            if args.option == "option-a":
                result_leaf=leaf.run(task=device_merge_conf,configuration=config_name)
                print_result(result_leaf)
            else:
                print(f"Lab {args.lab} eith {args.option} is not yet implemented for {args.underlay} ")
        else:
            print('ERROR : Bad underlay')
    else:
        print(f"ERROR : Bad lab")
elif args.action == "reset":
    conf_file="init_conf_ADC.eos"
    result_spine=spine.run(task=device_replace_conf,configuration=conf_file)
    print_result(result_spine)
    result_leaf=leaf.run(task=device_replace_conf,configuration=conf_file)
    print_result(result_leaf)
    result_host=host.run(task=device_replace_conf,configuration=conf_file)
    print_result(result_host)
else:
    print(f"Only \'push\' or \'reset\' action are allowed")










