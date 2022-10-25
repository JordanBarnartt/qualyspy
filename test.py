import qualyspy.qualysapi as qualysapi
import qualyspy.vm_scans


if __name__ == "__main__":
    conn = qualysapi.Connection()
    scans = conn.run(qualyspy.vm_scans.get_scans)
    print("Success!")
