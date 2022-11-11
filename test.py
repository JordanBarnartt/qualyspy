import qualyspy.qualysapi as qualysapi
import qualyspy.vm_scans as vm_scans


if __name__ == "__main__":
    conn = qualysapi.Connection()
    scans = vm_scans.get_scan_list(conn)
    print("Success!")
