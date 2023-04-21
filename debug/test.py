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

    fvo = api_input.Field_Operator_Value(field="tagName", operator="EQUALS", value="Science Cloud Agent")
    f = api_input.Filter(criteria=[fvo])
    test = asset.Count_Assets(conn)(filter=f)

    print("test")
