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
from qualyspy.models.asset_mgmt_tagging import (  # noqa: E402
    azure_asset_data_connector as aadc_models,
)
from qualyspy.models.asset_mgmt_tagging import (  # noqa: E402
    asset_data_connector as adc_models,
)
from qualyspy.models.asset_mgmt_tagging import azure_service as as_models  # noqa: E402


class TestTags(unittest.TestCase):
    def test_create_update_delete_tag(self):
        api = asset_mgmt_tagging.TagsAPI()
        tag = tag_models.Tag(
            name="Test Tag",
            description="Test Description",
            children=tag_models.TagSimpleQlist(
                set=tag_models.TagSimpleList(
                    tag_simple=[
                        tag_models.TagSimple(name="Child 1"),
                        tag_models.TagSimple(name="Child 2"),
                    ]
                ),
            ),
        )
        new_tag = api.create_tag(tag=tag)
        tag = tag_models.Tag(name="Updated Test Tag")
        updated_tag = api.update_tag(id=new_tag.id, tag=tag)
        self.assertEqual(updated_tag.id, new_tag.id)
        deleted_tag = api.delete_tag(id=new_tag.id)
        self.assertEqual(deleted_tag.id, new_tag.id)

    def test_search_tags(self):
        api = asset_mgmt_tagging.TagsAPI()
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
        api = asset_mgmt_tagging.TagsAPI()
        tag = tag_models.Tag(name="Test Tag", description="Test Description")
        new_tag = api.create_tag(tag=tag)
        filters = [
            asset_mgmt_tagging.Filter(field="name", operator="EQUALS", value="Test Tag")
        ]
        count = api.count_tags(filters=filters)
        self.assertEqual(count, 1)
        deleted_tag = api.delete_tag(id=new_tag.id)
        self.assertEqual(deleted_tag.id, new_tag.id)


class TestAzureConnectors(unittest.TestCase):
    def test_create_delete_azure_connector(self):
        tag_api = asset_mgmt_tagging.TagsAPI()
        azure_tag = tag_api.search_tags(
            filters=[asset_mgmt_tagging.Filter("name", "EQUALS", "Microsoft Azure")]
        )
        azure_tag = tag_models.TagSimple(id=azure_tag[0].id)
        tag_qlist = tag_models.TagSimpleQlist(
            set=tag_models.TagSimpleList(tag_simple=[azure_tag])
        )

        activation_qlist = adc_models.ActivationModuleQlist(
            set=adc_models.ActivationModuleObj(
                [adc_models.ActivationModule.VM, adc_models.ActivationModule.CERTVIEW]
            )
        )

        auth_record_fields = {
            "application_id": "4d989e82-1a55-4811-8c30-14d05663ddf9",
            "directory_id": "4d989e82-1a55-4811-8c30-14d05663ddf9",
            "subscription_id": "4d989e82-1a55-4811-8c30-14d05663ddf5",
            "authentication_key": "NotARealKey",
        }
        auth_record = as_models.AzureAuthRecordSimple(**auth_record_fields)

        connector_app_infos = adc_models.ConnectorAppInfoList(
            set=adc_models.ConnectorAppInfoQlistList(
                connector_app_info_q_list=[
                    adc_models.ConnectorAppInfoQlist(
                        set=adc_models.ConnectorAppInfoObj(
                            connector_app_info=adc_models.ConnectorAppInfo(
                                name="AI",
                                identifier=auth_record_fields["subscription_id"],
                                tag_id=azure_tag.id,
                            )
                        )
                    ),
                    adc_models.ConnectorAppInfoQlist(
                        set=adc_models.ConnectorAppInfoObj(
                            connector_app_info=adc_models.ConnectorAppInfo(
                                name="CI",
                                identifier=auth_record_fields["subscription_id"],
                                tag_id=azure_tag.id,
                            )
                        )
                    ),
                ]
            )
        )

        new_aadc = aadc_models.AzureAssetDataConnector(
            name="Test Azure Connector",
            default_tags=tag_qlist,
            activation=activation_qlist,
            auth_record=auth_record,
            disabled=True,
            run_frequency=240,
            is_gov_cloud_configured=False,
            connector_app_infos=connector_app_infos,
        )

        api = asset_mgmt_tagging.AzureConnectorsAPI()
        new_connector = api.create_azure_connector(new_aadc)
        self.assertEqual(new_connector.name, new_aadc.name)
        deleted_connector = api.delete_azure_connector(new_connector.id)
        self.assertEqual(deleted_connector.id, new_connector.id)

    def test_search_azure_connector(self):
        tag_api = asset_mgmt_tagging.TagsAPI()
        azure_tag = tag_api.search_tags(
            filters=[asset_mgmt_tagging.Filter("name", "EQUALS", "Microsoft Azure")]
        )
        azure_tag = tag_models.TagSimple(id=azure_tag[0].id)
        tag_qlist = tag_models.TagSimpleQlist(
            set=tag_models.TagSimpleList(tag_simple=[azure_tag])
        )

        activation_qlist = adc_models.ActivationModuleQlist(
            set=[adc_models.ActivationModule.VM, adc_models.ActivationModule.CERTVIEW]
        )

        auth_record_fields = {
            "application_id": "4d989e82-1a55-4811-8c30-14d05663ddf9",
            "directory_id": "4d989e82-1a55-4811-8c30-14d05663ddf9",
            "subscription_id": "4d989e82-1a55-4811-8c30-14d05663ddf8",
            "authentication_key": "NotARealKey",
        }
        auth_record = as_models.AzureAuthRecordSimple(**auth_record_fields)

        connector_app_infos = adc_models.ConnectorAppInfoList(
            set=adc_models.ConnectorAppInfoQlistList(
                connector_app_info_q_list=[
                    adc_models.ConnectorAppInfoQlist(
                        set=adc_models.ConnectorAppInfoObj(
                            connector_app_info=adc_models.ConnectorAppInfo(
                                name="AI",
                                identifier=auth_record_fields["subscription_id"],
                                tag_id=azure_tag.id,
                            )
                        )
                    ),
                    adc_models.ConnectorAppInfoQlist(
                        set=adc_models.ConnectorAppInfoObj(
                            connector_app_info=adc_models.ConnectorAppInfo(
                                name="CI",
                                identifier=auth_record_fields["subscription_id"],
                                tag_id=azure_tag.id,
                            )
                        )
                    ),
                ]
            )
        )

        new_aadc = aadc_models.AzureAssetDataConnector(
            name="Test Azure Connector",
            default_tags=tag_qlist,
            activation=activation_qlist,
            auth_record=auth_record,
            disabled=True,
            run_frequency=240,
            is_gov_cloud_configured=False,
            connector_app_infos=connector_app_infos,
        )

        api = asset_mgmt_tagging.AzureConnectorsAPI()
        new_connector = api.create_azure_connector(new_aadc)
        self.assertEqual(new_connector.name, new_aadc.name)

        filters = [asset_mgmt_tagging.Filter("name", "EQUALS", "Test Azure Connector")]
        searched_connectors = api.search_azure_connectors(filters=filters)
        self.assertEqual(searched_connectors[0].id, new_connector.id)

        deleted_connector = api.delete_azure_connector(new_connector.id)
        self.assertEqual(deleted_connector.id, new_connector.id)
