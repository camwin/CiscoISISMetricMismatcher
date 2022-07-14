import csv
import pprint
pp = pprint.PrettyPrinter(indent=4)

list_of_isis_routers = []

# Read in CSV of ISIS Metric audit (expecting hostname, interface, neighbor, metric level 1, metric level 2)
with open('isis_metric_audit.csv', 'r') as read_obj:
  
    # Return a reader object which will
    # iterate over lines in the given csvfile
    csv_reader = csv.reader(read_obj)
  
    # convert string to list
    list_of_isis_routers = list(csv_reader)
  
    #pp.pprint(list_of_isis_routers)

# For each line in the CSV, find router_a's ISIS neighbor line and compare the metrics, alerting on mismatch.
for router_a in list_of_isis_routers:
    router_a_hostname = router_a[0]
    router_a_neighbor_interface = router_a[1]
    router_a_metric_level1 = router_a[3]
    router_a_metric_level2 = router_a[4]
    # print(router_a_hostname)
    # print("Neighbor: " + router_a[2])
    # print(router_a_metric_level1)
    # print(router_a_metric_level2)
 

    for router_b in list_of_isis_routers:
        if router_b[2] == router_a_hostname and router_b[0] == router_a[2]:
            if router_a_metric_level1 == router_b[3]:
                if router_a_metric_level2 == router_b[4]:
                    continue
                else: 
                    print(router_a_hostname + " " + router_a_neighbor_interface + " " + router_a_metric_level1 + " " + router_a_metric_level2 + " metric mismatch with neighbor " + router_b[0] + " " + router_b[1] + " " + router_b[3] + " " + router_b[4])
            else:
                print(router_a_hostname + " " + router_a_neighbor_interface + " " + router_a_metric_level1 + " " + router_a_metric_level2 + " metric mismatch with neighbor " + router_b[0] + " " + router_b[1] + " " + router_b[3] + " " + router_b[4])
