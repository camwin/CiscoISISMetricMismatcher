# Python script utilizing PyATS library to audit Cisco IOS-XR ISIS metrics. 
# The devices that will be audited are contained in yaml/my_testbed.yaml. 
# The output is a CSV of the following type:
# 'hostname, interface, ISIS neighbor, level 1 ISIS metric, level 2 ISIS metric'
    

import pprint
pp = pprint.PrettyPrinter(indent=4)

from genie.testbed import load
tb = load('yaml/all_brcr_testbed.yaml')


all_routers_isis_interfaces_neighbors_metrics = {}

# Open file that we want to output to at the end
f = open("isis_metric_audit.csv", "w")

# For each router in the testbed file, connect to it and run "show isis neighbors", storing the output in a dictionary
for name, dev in tb.devices.items():
    # Initial Vars
    show_isis_neighbors = {}
    isis_neighbors_dict = {}
    isis_metrics_dict = {}
    show_isis_interface = {}
    dev.connect(init_exec_commands=[], init_config_commands=[])
    show_isis_neighbors[name] = dev.parse('show isis neighbors')

    # For each interface on this router with an isis neighbor, store those interfaces in a variable to save in the CSV
    for interface in show_isis_neighbors[name]["isis"]['isp']['vrf']['default']['interfaces']:
        show_isis_interface_var = "show isis interface " + interface
        show_isis_interface[interface] = dev.parse(show_isis_interface_var)

    # Optional console debug
    #print(name + " has the following ISIS neighbors and metrics")
    #print("")

    # For each ISIS neighbor on this router, store their hostname and the level 1 and level 2 metrics this router currently has configured for that neighbor
    for name in show_isis_neighbors:
        for isis_interface in show_isis_interface:
            pp.pprint(show_isis_neighbors[name])
            isis_neighbors_dict[name] = show_isis_neighbors[name]["isis"]['isp']['vrf']['default']['interfaces'][isis_interface]['neighbors']
            isis_neighbors = isis_neighbors_dict[name].keys()

            isis_metrics_dict[name] = show_isis_interface[isis_interface]['instance']['default']['interface'][isis_interface]['topology']['ipv4 unicast']['metric']
            isis_metrics = isis_metrics_dict[name].values()

            #write to file and console
            for neighbor in isis_neighbors:
                 for metric in isis_metrics:
                     print(name + "," + isis_interface + "," + neighbor + "," + "Level 1: " + str(metric[1]) + "," + "Level 2: " + str(metric[2]))
                     f.write(name + "," + isis_interface + "," + neighbor + "," + "Level 1: " + str(metric[1]) + "," + "Level 2: " + str(metric[2]) + "\n")

f.close()