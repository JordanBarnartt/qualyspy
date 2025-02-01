# mypy: ignore-errors
# type: ignore

import inspect
import os
import sys
import unittest

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from qualyspy import asset_mgmt_tagging  # noqa: E402
from qualyspy.models.asset_mgmt_tagging import asset_request  # noqa: E402


class TestTags(unittest.TestCase):
    def test_add_update_search_tag(self):
        api = asset_mgmt_tagging.AssetMgmtTaggingAPI()
        add_resp = api.create_tag(
            name="Parent Tag",
            color="#FFFFFF",
            children=["Child 1", "Child 2", "Child 3"],
        )

        self.assertEqual(add_resp.response_code, "SUCCESS")

        parent_tag_id = add_resp.data[0].tag.id

        update_resp = api.update_tag(
            tag_id=parent_tag_id,
            add_children=["Child 4"],
        )

        self.assertEqual(update_resp.response_code, "SUCCESS")

        search_resp = api.search_tags(name="Parent Tag")

        self.assertEqual(search_resp.response_code, "SUCCESS")

        delete_resp = api.delete_tag(parent_tag_id)

        self.assertEqual(delete_resp.response_code, "SUCCESS")

    def test_asset(self):
        api = asset_mgmt_tagging.AssetMgmtTaggingAPI()
        get_resp = api.get_asset_info(asset_id=14355608)

        self.assertEqual(get_resp.response_code, "SUCCESS")

        update_resp = api.update_asset(
            asset_id=14355608,
            name="taijitu.private",
            add_tags=[12158745],
        )

        self.assertEqual(update_resp.response_code, "SUCCESS")

    def test_search_assets(self):
        api = asset_mgmt_tagging.AssetMgmtTaggingAPI()
        criteria = asset_request.Criteria(
            field="tagName", operator="EQUALS", value="Test Search Assets"
        )

        search_resp = api.search_assets(criteria=[criteria])
        
        self.assertEqual(search_resp.count, 1)
