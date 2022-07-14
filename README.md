# CiscoISISMetricMismatcher
PyATS script to find Cisco ISIS Router Neighborship Metric Mismatches 

This script is devoted to finding instances in your ISIS routing domain where two router's that are neighbors with one another have mismatched metrics.
Mismatched metrics in ISIS (and OSPF) can cause asymetric or otherwise sub-optimal routing. 

Run this process on a job and adapt it to your alerting mechanism to keep a lid on metric mismatches. 
