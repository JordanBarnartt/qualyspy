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


from qualyspy import qutils, vmdr
from qualyspy.models.vmdr.host_list_vm_detection_orm import Host as HostORM
from qualyspy.models.vmdr.host_list_vm_detection_output import Host as HostOutput
from tests import test_data


class TestQutils(unittest.TestCase):
    def test_to_orm_object(self):
        data = test_data.example_hostlist
        orm_object = qutils.to_orm_object(data.host[0], HostORM)
        self.assertEqual(orm_object.ip, data.host[0].ip)


class TestVMDR(unittest.TestCase):
    def test_host_list_detection(self):
        api = vmdr.VmdrAPI()
        hostlist_detection, _, _ = api.host_list_detection(
            ids=test_data.test_host_list_id
        )
        ip = hostlist_detection.host[0].ip
        self.assertEqual(
            ip, ipaddress.ip_address(test_data.test_host_list_ip_address)
        )

    def test_vmdr_host_list_det_orm_load(self):
        vmdr_orm = vmdr.HostListDetectionORM()
        vmdr_orm.load()
        with orm.Session(vmdr_orm.engine) as session:
            host_list = session.query(HostORM).where(HostORM.id == 11619472).all()
            self.assertEqual(host_list[0].ip, ipaddress.ip_address("172.16.76.84"))

    def test_vmdr_host_list_det_orm_query(self):
        vmdr_orm = vmdr.HostListDetectionORM(echo=False)
        with orm.Session(vmdr_orm.engine) as session:
            stmt = session.query(HostORM)
            host_list = vmdr_orm.query(stmt)[0]
            host = host_list.host[0]
            self.assertIsInstance(host, HostOutput)
            self.assertTrue(host.ip in ipaddress.ip_network("129.97.0.0/16"))

    def test_vmdr_host_list(self):
        api = vmdr.VmdrAPI()
        host_list, _, _ = api.host_list(ids=test_data.test_host_list_id)
        ip = host_list.host[0].ip
        self.assertEqual(ip, ipaddress.ip_address(test_data.test_host_list_ip_address))


if __name__ == "__main__":
    unittest.main()
