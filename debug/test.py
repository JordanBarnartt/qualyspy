# type: ignore

import inspect
import os
import sys

import sqlalchemy as sa
import sqlalchemy.orm as orm


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from qualyspy.qualysapi import Connection
import qualyspy.asset_mgmt_tagging_new.tag as tag

if __name__ == "__main__":
    conn = Connection(apis=["qps"])

    t = tag.Tag(
        name="QualysPy Test",
        color="#FFFFFF",
        description="Test tag created by QualysPy",
        children=tag.Tag_Simple_Q_List(
            set={
                "TagSimple": [
                    tag.Tag_Simple(name="QualysPy Test Child"),
                    tag.Tag_Simple(name="QualysPy Test Child 2"),
                ]
            }
        ),
    )

    api = tag.Create_Tag(conn, t).call()
    input = tag.Tag(
        name="QualysPy Test Updated",
        children=tag.Tag_Simple_Q_List(
            remove={"TagSimple": [tag.Tag_Simple(name="QualysPy Test Child 2")]}
        ),
    )
    api2 = tag.Update_Tag(conn, api.data[0]).call(input)

    print("test")
