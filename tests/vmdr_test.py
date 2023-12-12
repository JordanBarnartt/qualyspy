# mypy: ignore-errors
# type: ignore

import inspect
import ipaddress
import os
import sys
import unittest

import sqlalchemy as sa

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from qualyspy import vmdr  # noqa: E402
from qualyspy.models.vmdr import host_list_orm, host_list_vm_detection_orm  # noqa: E402


class TestOutputModels(unittest.TestCase):
    def test_host_list(self):
        api = vmdr.VmdrAPI()
        host_list, _, _ = api.host_list(
            ids=11619472, show_trurisk=True, show_trurisk_factors=True
        )
        host = host_list[0]

        self.assertEqual(host.ip, ipaddress.ip_address("172.16.76.84"))

    def test_host_list_vm_detection(self):
        api = vmdr.VmdrAPI()
        host_list, _, _ = api.host_list_vm_detection(ids=11619472)
        host = host_list[0]

        self.assertEqual(host.ip, ipaddress.ip_address("172.16.76.84"))

    def test_knowledgebase(self):
        api = vmdr.VmdrAPI()
        kb = api.knowledgebase(ids=120098)
        vuln = kb[0]

        self.assertEqual(vuln.qid, 120098)


class TestORM(unittest.TestCase):
    def test_sql_host_list(self):
        api = vmdr.HostListORM()
        api.init_db()
        api.load()
        stmt = sa.select(host_list_orm.Host).where(host_list_orm.Host.id == 11619472)
        result = api.query(stmt)
        host = result[0][0]
        self.assertEqual(host.ip, ipaddress.ip_address("172.16.76.84"))

    def test_sql_vm_detection(self):
        api = vmdr.HostListVMDetectionORM()
        # api.init_db()
        # api.load()
        stmt = sa.select(host_list_vm_detection_orm.Host).where(
            host_list_vm_detection_orm.Host.id == 11619472
        )
        result = api.query(stmt)
        host = result[0][0]
        self.assertEqual(host.ip, ipaddress.ip_address("172.16.76.84"))


if __name__ == "__main__":
    unittest.main()
