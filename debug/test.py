# type: ignore

import inspect
import os
import sys
import time

import sqlalchemy as sa
import sqlalchemy.orm as orm


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from qualyspy.qualysapi import Connection
import qualyspy.asset_mgmt_tagging.tag as tag
import qualyspy.asset_mgmt_tagging.asset as asset
import qualyspy.asset_mgmt_tagging.api_input as api_input

if __name__ == "__main__":
    conn = Connection(apis=["qps"])

    asset_fvo = api_input.Field_Operator_Value(field="id", operator="EQUALS", value=3084303)
    asset_filter = api_input.Filter(criteria=[asset_fvo])
    a = asset.Search_Assets(conn)(filter=asset_filter).data[0]

    new_tag = tag.Tag(name="QualysPy Test", description="test")
    create_tag = tag.Create_Tag(conn)(new_tag).data[0]

    asset_update = asset.Asset(tags=tag.Tag_Simple_Q_List(add={"TagSimple": [create_tag]}))
    add_tag = asset.Update_Asset(conn, a)(asset_update)

    print("test")
