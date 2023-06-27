# mypy: ignore-errors
# type: ignore
# pylama: ignore=E402

import inspect
import ipaddress
import os
import sys
import unittest

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from qualyspy import gav


class TestGAV(unittest.TestCase):
    def test_gav_asset_details(self):
        api = gav.GavAPI()
        asset_details = api.asset_details(asset_id=14355608)
        ip = asset_details.address
        self.assertEqual(ip, ipaddress.ip_address("172.16.76.84"))

    def test_gav_all_asset_details(self):
        api = gav.GavAPI()
        assets, has_more, last_seen_asset_id = api.all_asset_details()
        self.assertTrue(len(assets) == 100)
