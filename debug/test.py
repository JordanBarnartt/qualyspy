import inspect
import os
import sys


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from qualyspy.qualysapi import Connection
from qualyspy.certview.pydantic.certificate import list_certificates_v2, List_CertView_Certificates_v2_Input, Filter, Field_Value_Operator

if __name__ == "__main__":
    conn = Connection(apis = ["CertView"])
    fvo = Field_Value_Operator(field="certificate.serialNumber", operator="EQUALS", value="00b930ea6e650ce85c")
    filter = Filter(filters=[fvo])
    input = List_CertView_Certificates_v2_Input(filter=filter)
    cert = list_certificates_v2(conn, input)
    print("test")
