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
    output = qualyspy.host_list(
        conn,
        ips=ipaddress.ip_address("129.97.3.12"),
        show_asset_ids=True,
        all_details=True,
        show_ag_info=True,
        show_tags=True,
        show_ars=True,
        show_ars_factors=True,
    )
    print("Success!")
