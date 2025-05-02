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

from qualyspy import gav  # noqa: E402
from qualyspy.models.gav import asset_details_orm  # noqa: E402


class TestOutputModels(unittest.TestCase):
    def test_asset_details(self):
        api = gav.GavAPI()
        asset = api.asset_details(asset_id=14355608)

        self.assertEqual(asset.address, ipaddress.ip_address("172.16.76.84"))

    def test_all_asset_details(self):
        api = gav.GavAPI()
        assets, _, _ = api.all_asset_details()


class TestORM(unittest.TestCase):
    def test_sql_all_asset_details(self):
        api = gav.AllAssetDetailsORM()
        api.drop()
        api.init_db()
        api.load()
        stmt = sa.select(asset_details_orm.AssetItem).where(
            asset_details_orm.AssetItem.asset_id == 14355608
        )
        result = api.query(stmt)
        asset = result[0][0]

        self.assertEqual(asset.address, ipaddress.ip_address("172.16.76.84"))
