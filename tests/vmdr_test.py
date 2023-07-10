# mypy: ignore-errors
# type: ignore
# pylama: ignore=E402

import inspect
import ipaddress
import os
import sys
import unittest

import sqlalchemy.orm as orm

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


import qualyspy.models.vmdr.host_list_orm as host_list_orm
import qualyspy.models.vmdr.host_list_vm_detection_orm as host_list_vm_detection_orm
from qualyspy import qutils, vmdr
from tests import test_data


class TestQutils(unittest.TestCase):
    def test_to_orm_object(self):
        data = test_data.example_hostlist
        orm_object = qutils.to_orm_object(data.host[0], host_list_vm_detection_orm.Host)
        self.assertEqual(orm_object.ip, data.host[0].ip)


class TestVMDR(unittest.TestCase):
    def test_host_list_detection(self):
        api = vmdr.VmdrAPI()
        hostlist_detection, _, _ = api.host_list_detection(
            ids=test_data.test_host_list_id
        )
        ip = hostlist_detection.host[0].ip
        self.assertEqual(ip, ipaddress.ip_address(test_data.test_host_list_ip_address))

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

    def test_vmdr_host_list(self):
        api = vmdr.VmdrAPI()
        host_list, _, _ = api.host_list(ids=test_data.test_host_list_id)
        ip = host_list.host[0].ip
        self.assertEqual(ip, ipaddress.ip_address(test_data.test_host_list_ip_address))

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
