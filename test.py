import qualyspy.qualysapi as qualysapi
import qualyspy.vm_scans as vm_scans
import ipaddress

if __name__ == "__main__":
    conn = qualysapi.Connection()
    ip = ipaddress.IPv4Address("172.25.29.137")
    scan_assets = vm_scans.Scan_Asset_Ips_Groups(ip=ip)
    output = vm_scans.launch_scan(
        conn,
        scan_assets=scan_assets,
        scan_title="qualyspy test",
        iscanner_name="iss-qg-cr-v01",
        option_title="BaselineInternal"
    )
    print("Success!")
