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

    def test_host_list_by_ip(self):
        api = vmdr.VmdrAPI()
        ips = ["172.16.68.91", "129.97.128.5", "129.97.85.51", "172.16.64.51"]
        host_list, _, _ = api.host_list(ips=ips, show_tags=True)
        host = host_list[0]

        self.assertEqual(host.ip, ipaddress.ip_address("172.16.68.91"))

    def test_host_list_vm_detection(self):
        api = vmdr.VmdrAPI()
        host_list, _, _ = api.host_list_vm_detection(ids=11619472, show_igs=True)
        host = host_list[0]

        self.assertEqual(host.ip, ipaddress.ip_address("172.16.76.84"))

    def test_knowledgebase(self):
        api = vmdr.VmdrAPI()
        kb = api.knowledgebase(ids=92203)
        vuln = kb[0]

        self.assertEqual(vuln.qid, 92203)

    def test_launch_vm_scan(self):
        api = vmdr.VmdrAPI()
        ret = api.launch_vm_scan(
            scan_title="Test Scan",
            iscanner_name="iss-qg-cr-v05",
            option_title="CertViewFree Profile",
            fqdn="learn.uwaterloo.ca",
        )
        text = ret.response.text

        self.assertEqual(text, "New vm scan launched")

    def test_map_report_list(self):
        api = vmdr.VmdrAPI()
        reports = api.map_report_list(last=True)
        report = reports.report_list[0]

        self.assertEqual(report.title, "External Map baseline")

    def test_map_report(self):
        api = vmdr.VmdrAPI()
        reports = api.map_report_list(last=True)
        report_ref = reports.report_list[0].ref

        report = api.download_saved_map_report(ref=report_ref)

        self.assertEqual(report.value, report_ref)


class TestORM(unittest.TestCase):
    def test_orm_host_list(self):
        api = vmdr.HostListORM()
        api.init_db()
        api.load(show_tags=True)
        stmt = sa.select(host_list_orm.Host).where(host_list_orm.Host.id == 11619472)
        result = api.query(stmt)
        host = result[0][0]
        self.assertEqual(host.ip, ipaddress.ip_address("172.16.76.84"))

    def test_orm_vm_detection(self):
        api = vmdr.HostListVMDetectionORM()
        api.drop()
        api.init_db()
        api.load(show_igs=True)
        stmt = sa.select(host_list_vm_detection_orm.Host).where(
            host_list_vm_detection_orm.Host.id == 11619472
        )
        result = api.query(stmt)
        host = result[0][0]
        self.assertEqual(host.ip, ipaddress.ip_address("172.16.76.84"))

    def test_orm_knowledgebase(self):
        api = vmdr.KnowledgebaseORM()
        api.init_db()
        api.load(details="All")
        stmt = sa.select(vmdr.knowledgebase_orm.Vuln).where(
            vmdr.knowledgebase_orm.Vuln.qid == 6
        )
        result = api.query(stmt)
        vuln = result[0][0]
        self.assertEqual(vuln.title, "DNS Host Name")


if __name__ == "__main__":
    unittest.main()
