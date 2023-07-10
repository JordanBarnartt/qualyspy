# mypy: ignore-errors
# type: ignore
# pylama: ignore=E402

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import qualyspy_legacy.certview.certificate as cert
from qualyspy_legacy.qualysapi import Connection

conn = Connection(apis=["CertView"])
api = cert.List_Certificates_V2(conn)

api.reset(echo=True)
api.load(echo=True)
