import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import qualyspy.qualysapi as qualysapi
import qualyspy.vm_scans as vm_scans
import ipaddress

def launch_quick_scan(conn, ip):
    scan_assets = vm_scans.Scan_Asset_Ips_Groups(ip=ip)
    output = vm_scans.launch_scan(
        conn,
        scan_assets=scan_assets,
        scan_title=ip.exploded,
        iscanner_name="iss-qg-cr-v01",
        option_title="BaselineInternal",
    )
    print("Success!")

if __name__ == "__main__":
    conn = qualysapi.Connection()
    ip = ipaddress.IPv4Address("")
    launch_quick_scan(conn, ip)