# CiscoISISMetricMismatcher
PyATS script to find Cisco ISIS Router Neighborship Metric Mismatches 

From my blog post on this process: https://chefwear.wordpress.com/2022/07/14/network-automation-project-isis-metric-mismatch-finder/

Step 1: Get list of devices to audit from Netbox
I like Netbox because its so easy to use but also I am so used to it.

I used the API and python to output a list in the proper format PyATS wants to generate a YAML Testbed file (the list of the devices your PyATS script will run against).

I did this with the following script. You can change those filters to your liking with help from the netbox API docs:

import pynetbox
import csv

nb = pynetbox.api(url='https:netboxURL(no need for /API/...)/', token='token')

#fetch all devices. I used the "Roles" to filter on specific tribal meanings
nb_br_devicelist = nb.dcim.devices.filter(role='br')
nb_lr_devicelist = nb.dcim.devices.filter(role='lr')

all_routers_list = []

for device in nb_br_devicelist:
    #print(device.name)
    if device.primary_ip4 is None:
        continue
    else:
        all_routers_list.append([str(device.name),str(device.primary_ip4).replace('/32',''),"service-account-username","service-account-password","ssh", str(device.platform)])

for device in nb_lr_devicelist:
    #print(device.name)
    if device.primary_ip4 is None:
        continue
    else:
        all_routers_list.append([str(device.name),str(device.primary_ip4).replace('/32',''),"service-account-username","service-account-password","ssh", str(device.platform)])

#debug print
print(all_routers_list)


# The expected heading for the import process in PyATS CSV->Yaml Generator 
netbox_import_template_heading = ['hostname', 'ip', 'username', 'password', 'protocol','os']

# (Over)Write the compiled dictionary to a CSV called all_br_lr_netbox.csv 
with open('all_br_lr_netbox.csv', 'w') as f: 
    write = csv.writer(f) 
    write.writerow(netbox_import_template_heading) 
    write.writerows(all_routers_list)
You should get something in the console and CSV like:

[[‘br1-buh1’, ‘11.23.4.1’, ‘service-account-username’, ‘service-account-password’, ‘ssh’, ‘iosxr’], [‘br1-buh2’, ‘12.1.3.111’, ‘service-account-username’, ‘service-account-password’, ‘ssh’, ‘iosxr’],

Step 2: Generate the YAML Testbed file
With the CSV in the router format above:

“‘hostname’, ‘ip’, ‘username’, ‘password’, ‘protocol’, ‘os'” format
No empty lines at end
If you can, prune out unreachable hosts (you probably should go fix them too haha)
execute this command to generate the PyATS Testbed YAML:

pyats create project interactive --output yaml/my_testbed.yml --encode-password
Make sure you have full PyATS installed to be able to execute the above command! (pip install pyats[full])

Step 3: Audit the network with PyATS script
https://github.com/camwin/CiscoISISMetricMismatcher/blob/main/PyATS_Cisco_ISIS_Metric_Audit.py

The above script will output a CSV that looks like this:

br1-buh1,Bundle-Ether10,cr1-buh1-b,Level 1: 10001,Level 2: 10001
br1-buh1,Bundle-Ether12,lr1-buh1-a,Level 1: 10001,Level 2: 10001
br1-buh1,Bundle-Ether11,cr1-buh1-a,Level 1: 10001,Level 2: 10001
br1-buh1,Bundle-Ether13,lr1-buh1-b,Level 1: 10001,Level 2: 10001
br1-buh2,Bundle-Ether10,cr1-buh2-a,Level 1: 10001,Level 2: 10001
br1-buh2,Bundle-Ether11,cr1-buh2-b,Level 1: 10001,Level 2: 10001
br1-buh2,Bundle-Ether12,br1-buh300,Level 1: 10001,Level 2: 10001
Note there are two(?) level metrics? I only see us configure one in the Cisco global ISIS protocol configuration, but I guess you can set them individually. Regardless, my script checks them both.

Step 4: Audit the audit
The last script is just an algorithm that looks for matches amongst the mesh and compares the configured metric from each router’s perspective.

https://github.com/camwin/CiscoISISMetricMismatcher/blob/main/find_isis_metric_mismatches.py

A mismatch will produce something like:

br1-buh1 Bundle-Ether10 Level 1: 10004 Level 2: 10004 metric mismatch with neighbor br1-buh2 Bundle-Ether13 Level 1: 10001 Level 2: 10001
br1-buh2 Bundle-Ether13 Level 1: 10001 Level 2: 10001 metric mismatch with neighbor br1-buh1 Bundle-Ether10 Level 1: 10004 Level 2: 10004
Since our end goal was to find these discrepancies, we have reduced the problem down to an ingestible format a simple Python algorithm and look through and pick out mismatches for us, every time, without fail. And best yet, since we did this all programmatically (remember go take care of those unresponsive devices in netbox haha), this can be run routinely by cron and alert you when it finds an issue.

Ahhh, network policy automation.
