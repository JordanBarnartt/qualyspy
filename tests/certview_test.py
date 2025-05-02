# mypy: ignore-errors
# type: ignore

import inspect
import os
import sys
import unittest

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from qualyspy import certview  # noqa: E402


class TestCertViewAPI(unittest.TestCase):
    def test_list_instances(self):
        api = certview.CertViewAPI()
        filter_request = certview.FilterRequest(
            filters=[
                certview.Filter(field="asset.id", value="42967118", operator="EQUALS"),
            ],
        )
        instances = api.list_instances(filter_request=filter_request)
        self.assertEqual(instances[0].service, "https")


    def test_add_bulk_external_sites(self):
        api = certview.CertViewAPI()
        sites = [
            "www.uwaterloo.ca",
            "www.quest.uwaterloo.ca",
            "quest.uwaterloo.ca",
            "lib.uwaterloo.ca",
        ]
        api.add_bulk_external_sites(sites=sites)
