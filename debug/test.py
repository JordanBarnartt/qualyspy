import inspect
import os
import sys


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from qualyspy.qualysapi import Connection
from qualyspy.certview.certificate import list_certificates
from qualyspy.qutils import Filter

if __name__ == "__main__":
    conn = Connection(apis = ["CertView"])
    filter = Filter("asset.name", "EQUALS", "lib10zigprd02.lib.private.uwaterloo.ca")
    certs = list_certificates(conn, filter=filter)
    print("test")
