import qualyspy.qualysapi as qualysapi
import qualyspy.vm_scans as vm_scans


if __name__ == "__main__":
    conn = qualysapi.Connection()
    scans = vm_scans.launch_scan(conn)
    print("Success!")
