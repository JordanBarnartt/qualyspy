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

import qualyspy.certview.certificate as cert
from qualyspy.qualysapi import Connection

conn = Connection(apis=["CertView"])
api = cert.List_Certificates_V2(conn)

# api.reset(echo=True)
# api.load(echo=True)

fov = cert.Field_Operator_Value(field="certificate.id", operator="EQUALS", value=692403)
filter = cert.Filter(filters=[fov])
params = cert.List_CertView_Certificates_V2_Input(filter=filter)
api(params=params)
