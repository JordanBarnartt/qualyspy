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
    qualyspy.knowledgebase(conn, ids=198862)
    print("Success!")
