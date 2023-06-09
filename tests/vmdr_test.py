# mypy: ignore-errors
# type: ignore
# pylama: ignore=E402

import datetime
import inspect
import ipaddress
import os
import sys
import unittest

import sqlalchemy.orm as orm

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from ipaddress import IPv4Address

from qualyspy2 import vmdr, qutils
from qualyspy2.models.vmdr.host_list_vm_detection_orm import \
    HostList as HostListORM
from qualyspy2.models.vmdr.host_list_vm_detection_output import (Detection,
                                                                 DetectionList,
                                                                 DnsData, Host,
                                                                 HostList)
from tests import test_data

example_hostlist = HostList(
    host=[
        Host(
            id=12361,
            asset_id=None,
            ip=IPv4Address("129.97.83.13"),
            ipv6=None,
            tracking_method="IP",
            network_id=None,
            os="Linux 2.x",
            os_cpe=None,
            dns="mattermost-1.uwaterloo.ca",
            dns_data=DnsData(
                hostname="mattermost-1",
                domain="uwaterloo.ca",
                fqdn="mattermost-1.uwaterloo.ca",
            ),
            cloud_provider=None,
            cloud_service=None,
            cloud_resource_id=None,
            ec2_instance_id=None,
            netbios=None,
            qg_hostid=None,
            last_scan_datetime=datetime.datetime(2023, 6, 6, 5, 58, 25),
            last_vm_scanned_date=datetime.datetime(2023, 6, 6, 5, 57, 33),
            last_vm_scanned_duration=datetime.timedelta(seconds=1399),
            last_vm_auth_scanned_date=None,
            last_vm_auth_scanned_duration=None,
            last_pc_scanned_date=None,
            tags=None,
            metadata_=None,
            cloud_provider_tags=None,
            detection_list=DetectionList(
                detection=[
                    Detection(
                        qid=38739,
                        type="Confirmed",
                        severity=3,
                        port=22,
                        protocol="tcp",
                        fqdn=None,
                        ssl=False,
                        instance=None,
                        results="Type\\tName\\nkey exchange\\tdiffie-hellman-group1-sha1\\nci"
                        "pher\\tblowfish-cbc\\ncipher\\tcast128-cbc\\ncipher\\t3des-cbc",
                        status="Active",
                        first_found_datetime=datetime.datetime(2019, 5, 6, 16, 55, 48),
                        last_found_datetime=datetime.datetime(2023, 6, 6, 5, 57, 33),
                        qds=None,
                        qds_factors=None,
                        times_found=657,
                        last_test_datetime=datetime.datetime(2023, 6, 6, 5, 57, 33),
                        last_update_datetime=datetime.datetime(2023, 6, 6, 5, 58, 25),
                        last_fixed_datetime=None,
                        first_reopened_datetime=None,
                        last_reopened_datetime=None,
                        times_reopened=None,
                        service=None,
                        is_ignored=False,
                        is_disabled=False,
                        affect_running_kernel=None,
                        affect_running_service=None,
                        affect_exploitable_config=None,
                        last_processed_datetime=datetime.datetime(
                            2023, 6, 6, 5, 58, 25
                        ),
                        asset_cve=None,
                    )
                ]
            ),
        )
    ]
)


class TestQutils(unittest.TestCase):
    def test_to_orm_object(self):
        orm_object = qutils.to_orm_object(vars(example_hostlist), HostListORM)
        self.assertEqual(orm_object.host[0].ip, example_hostlist.host[0].ip)


class TestVMDR(unittest.TestCase):
    def test_host_list_detection(self):
        api = vmdr.VmdrAPI()
        host = api.host_list_detection(ids=test_data.test_host_list_detection_id)
        ip = host.response.host_list.host[0].ip
        self.assertEqual(
            ip, ipaddress.ip_address(test_data.test_host_list_detection_ip_address)
        )

    def test_vmdr_orm_init(self):
        vmdr_orm = vmdr.HostListDetectionORM(echo=True)
        vmdr_orm.init_db()
        with orm.Session(vmdr_orm.engine) as session:
            host_list = session.query(vmdr.HostList).all()
            test = len(host_list) >= 0
            self.assertTrue(test)

    def test_vmdr_orm_load(self):
        vmdr_orm = vmdr.HostListDetectionORM(echo=True)
        vmdr_orm.load()
        with orm.Session(vmdr_orm.engine) as session:
            host_list = session.query(vmdr.HostList).all()
            test = len(host_list) == 100
            self.assertTrue(test)


if __name__ == "__main__":
    unittest.main()
