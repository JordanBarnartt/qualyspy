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

    # fvo = cert.Field_Value_Operator(field="certificate.id", operator="EQUALS", value="39534")
    # filter = cert.Filter(filters=[fvo])
    # input = cert.List_CertView_Certificates_V2_Input(filter=filter)
    # test = api.call(input)

    # api.reset(echo = True)
    # test = api.load(echo=True)

    # stmt = sa.Select(cert.Certificate_ORM).where(cert.Certificate_ORM.self_signed == False)
    # test = api.query(stmt, echo = True)

    stmt = (
        sa.select(
            cert.Subject_ORM.name,
            cert.Asset_Interface_ORM.address,
            cert.Host_Instance_ORM.protocol,
            cert.Host_Instance_ORM.port,
        )
        .join(cert.Certificate_ORM)
        .join(cert.Asset_ORM)
        .join(cert.Asset_Interface_ORM)
        .join(cert.Asset_ORM.host_instances)
    )

    hosts = api.query(stmt, echo=True)
    for host in hosts:
        print(host)

    print("test")
