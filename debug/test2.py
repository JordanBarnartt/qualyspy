import inspect
import os
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import qualyspy

import ipaddress

if __name__ == "__main__":
    conn = qualyspy.Connection()
    output = qualyspy.host_list_detection(
        conn,
        ips=ipaddress.ip_address("129.97.3.12"),
        severities=5
    )
    print("Success!")
