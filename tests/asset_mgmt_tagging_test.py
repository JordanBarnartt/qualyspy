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

import qualyspy.models.asset_mgmt_tagging.tag as tag_models  # noqa: E402


class TestTags(unittest.TestCase):
    def test_create_update_delete_tag(self):
        api = asset_mgmt_tagging.Tags()
        tag = tag_models.Tag(name="Test Tag", description="Test Description")
        new_tag = api.create_tag(tag=tag)
        tag = tag_models.Tag(name="Updated Test Tag")
        updated_tag = api.update_tag(id=new_tag.id, tag=tag)
        self.assertEqual(updated_tag.id, new_tag.id)
        deleted_tag = api.delete_tag(id=new_tag.id)
        self.assertEqual(deleted_tag.id, new_tag.id)

    def test_search_tags(self):
        api = asset_mgmt_tagging.Tags()
        tag = tag_models.Tag(name="Test Tag", description="Test Description")
        new_tag = api.create_tag(tag=tag)
        filters = [
            asset_mgmt_tagging.Filter(field="name", operator="EQUALS", value="Test Tag")
        ]
        tags = api.search_tags(filters=filters)
        self.assertEqual(tags[0].id, new_tag.id)
        deleted_tag = api.delete_tag(id=new_tag.id)
        self.assertEqual(deleted_tag.id, new_tag.id)

    def test_count_tags(self):
        api = asset_mgmt_tagging.Tags()
        tag = tag_models.Tag(name="Test Tag", description="Test Description")
        new_tag = api.create_tag(tag=tag)
        filters = [
            asset_mgmt_tagging.Filter(field="name", operator="EQUALS", value="Test Tag")
        ]
        count = api.count_tags(filters=filters)
        self.assertEqual(count, 1)
        deleted_tag = api.delete_tag(id=new_tag.id)
        self.assertEqual(deleted_tag.id, new_tag.id)
