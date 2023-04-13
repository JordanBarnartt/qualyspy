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
import qualyspy.certview.certificate as cert

if __name__ == "__main__":
    conn = Connection(apis=["CertView"])
    api = cert.List_Certificates_V2(conn)

    # fvo = cert.Field_Value_Operator(field="certificate.id", operator="EQUALS", value="625316")
    # filter = cert.Filter(filters=[fvo])
    # input = cert.List_CertView_Certificates_V2_Input(filter=filter)
    # test = api.call(input)

    # api.reset(echo = True)
    # test = api.load(echo=True)

    stmt = sa.select(cert.Certificate_ORM).where(cert.Certificate_ORM.id == "625316")

    hosts = api.query(stmt, echo=True)

    print("test")
