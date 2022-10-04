import qualysapi
import modules.vm_scans


if __name__ == "__main__":
    conn = qualysapi.Connection()
    scans = conn.run(modules.vm_scans.get_scans)
    print("Success!")
