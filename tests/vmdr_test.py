# mypy: ignore-errors
# type: ignore
# pylama: ignore=E402

import unittest
import ipaddress
import os
import inspect
import sys

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
        self.assertEqual(ip, ipaddress.ip_address(test_data.test_host_list_detection_ip_address))


if __name__ == "__main__":
    unittest.main()
