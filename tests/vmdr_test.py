# mypy: ignore-errors
# type: ignore

import inspect
import ipaddress
import os
import sys
import unittest

import sqlalchemy.orm as orm

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


import qualyspy.models.vmdr.host_list_orm as host_list_orm  # noqa: E402
import qualyspy.models.vmdr.host_list_vm_detection_orm as host_list_vm_detection_orm  # noqa: E402
from qualyspy import vmdr  # noqa: E402


class TestVMDR(unittest.TestCase):
    def test_vmdr_host_list_det_orm_load(self):
        vmdr_orm = vmdr.HostListDetectionORM(echo=True)
        vmdr_orm.load()
        with orm.Session(vmdr_orm.engine) as session:
            host_list = (
                session.query(host_list_vm_detection_orm.Host)
                .where(host_list_vm_detection_orm.Host.id == 11619472)
                .all()
            )
            self.assertEqual(host_list[0].ip, ipaddress.ip_address("172.16.76.84"))

    def test_vmdr_host_list_orm_load(self):
        vmdr_orm = vmdr.HostListORM(echo=True)
        vmdr_orm.load()
        with orm.Session(vmdr_orm.engine) as session:
            host_list = (
                session.query(host_list_orm.Host)
                .where(host_list_orm.Host.id == 11619472)
                .all()
            )
            self.assertEqual(host_list[0].ip, ipaddress.ip_address("172.16.76.84"))


class TestKnowledgebase(unittest.TestCase):
    def test_vmdr_knowledgebase(self):
        api = vmdr.VmdrAPI()
        knowledgebase = api.knowledgebase(ids=105943)
        print("test")
        self.assertEqual(knowledgebase.vuln[0].qid, 105943)


if __name__ == "__main__":
    unittest.main()
