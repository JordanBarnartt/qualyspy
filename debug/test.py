# type: ignore

import inspect
import os
import sys


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from qualyspy.qualysapi import Connection
import qualyspy.certview.certificate as cert

if __name__ == "__main__":
    conn = Connection(apis = ["CertView"])
    #fvo = cert.Field_Value_Operator(field="certificate.serialNumber", operator="EQUALS", value="00b930ea6e650ce85c")
    #filter = cert.Filter(filters=[fvo])
    #input = cert.List_CertView_Certificates_v2_Input(filter=filter)
    #cert = cert.list_certificates_v2(conn, input)

    cert.init_db()
    input = cert.List_CertView_Certificates_v2_Input(pageSize=200)
    cert.list_certificates_v2(conn, input, load_db = True)

    print("test")
