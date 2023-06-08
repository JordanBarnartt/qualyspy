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

print(sys.path)

from qualyspy2 import vmdr
from tests import test_data


class TestVMDR(unittest.TestCase):
    def test_host_list_detection(self):
        api = vmdr.VmdrAPI()
        host = api.host_list_detection(ids=test_data.test_host_list_detection_id)
        ip = host.response.host_list.host[0].ip
        self.assertEqual(
            ip, ipaddress.ip_address(test_data.test_host_list_detection_ip_address)
        )

    def test_vmdr_orm_init(self):
        vmdr_orm = vmdr.VmdrORM(echo=True)
        vmdr_orm.init_db()
        with orm.Session(vmdr_orm.engine) as session:
            host_list = session.query(vmdr.HostList).all()
            self.assertEqual(len(host_list), 0)


if __name__ == "__main__":
    unittest.main()
