import inspect
import os
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import qualyspy

if __name__ == "__main__":
    conn = qualyspy.Connection()
    asset_filter = qualyspy.asset_mgmt_tagging.make_filter("id", "equals", "685629")
    asset = qualyspy.asset_mgmt_tagging.search_assets(conn, asset_filter)[0]
    
    tag_filter = qualyspy.asset_mgmt_tagging.make_filter("name", "equals", "QualysPy Test")
    tag = qualyspy.asset_mgmt_tagging.search_tags(conn, tag_filter)[0]

    asset.update(conn, tags_to_add=[tag])

    print("Here!")
