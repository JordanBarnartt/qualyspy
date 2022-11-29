import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import qualyspy.qualysapi as qualysapi
import qualyspy.vm_scans as vm_scans
import ipaddress


def test_scan_list(conn):
    output = vm_scans.scan_list(conn)
    print("Success!")


def test_launch_scan(conn):
    ip = ipaddress.IPv4Address("172.25.29.137")
    scan_assets = vm_scans.Scan_Asset_Ips_Groups(ip=ip)
    output = vm_scans.launch_scan(
        conn,
        scan_assets=scan_assets,
        scan_title="qualyspy test",
        iscanner_name="iss-qg-cr-v01",
        option_title="BaselineInternal",
    )
    print("Success!")


def test_fetch_scan(conn):
    output = vm_scans.fetch_scan_csv(conn, "scan/1669646302.25173", "test_output.csv")
    print("Success!")


if __name__ == "__main__":
    conn = qualysapi.Connection()
    # test_scan_list(conn)
    # test_launch_scan(conn)
    f = test_fetch_scan(conn)
    print(type(f))
    print("here")
