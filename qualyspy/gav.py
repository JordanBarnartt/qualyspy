from typing import Any

import sqlalchemy.orm as orm

from . import URLS, qutils
from .base import QualysAPIBase, QualysORMMixin
from .exceptions import QualysAPIError
from .models.gav import asset_details_orm, asset_details_output


class GavAPI(QualysAPIBase):
    """Qualys VMDR API Class.  Contains methods for interacting with the VMDR API."""

    def _convert_ipaddress(self, ips: str | None) -> list[str] | None:
        """Converts a string of IPs into a list of IP strings, for easier validation in
        Pydantic.
        """
        if ips is None:
            return None
        elif "," in ips:
            return ips.split(", ")
        return [ips]

    def asset_details(self, *, asset_id: int) -> asset_details_output.AssetItem | None:
        params = {"assetId": asset_id}
        params_cleaned = qutils.clean_dict(params)

        raw_response = self.get(URLS.asset_details, params=params_cleaned)
        if raw_response.status_code == 204:
            return None
        response_json = raw_response.json()
        if (
            response_json["assetListData"]["asset"][0]["networkInterfaceListData"]
            is not None
        ):
            for interface in response_json["assetListData"]["asset"][0][
                "networkInterfaceListData"
            ]["networkInterface"]:
                interface["addressIpV4"] = self._convert_ipaddress(
                    interface["addressIpV4"]
                )
                interface["addressIpV6"] = self._convert_ipaddress(
                    interface["addressIpV6"]
                )
        response = asset_details_output.AssetDetailsOutput(**response_json)
        return response.asset_list_data.asset[0]

    def all_asset_details(
        self,
        *,
        last_seen_asset_id: int | None = None,
        page_size: int | None = None,
    ) -> tuple[list[asset_details_output.AssetItem], bool, int | None]:
        params = {
            "lastSeenAssetId": last_seen_asset_id,
            "pageSize": page_size,
        }
        params_cleaned = qutils.clean_dict(params)
        raw_response = self.post(URLS.all_asset_details, params=params_cleaned).json()

        for asset in raw_response["assetListData"]["asset"]:
            if asset["networkInterfaceListData"] is not None:
                for interface in asset["networkInterfaceListData"]["networkInterface"]:
                    interface["addressIpV4"] = self._convert_ipaddress(
                        interface["addressIpV4"]
                    )
                    interface["addressIpV6"] = self._convert_ipaddress(
                        interface["addressIpV6"]
                    )
            if (
                asset["cloudProvider"] is not None
                and asset["cloudProvider"]["oci"] is not None
            ):
                if asset["cloudProvider"]["oci"]["tags"] is None:
                    asset["cloudProvider"]["oci"]["tags"] = []

        response = asset_details_output.AssetDetailsOutput(**raw_response)

        if response.response_code != "SUCCESS":
            raise QualysAPIError(
                f"Qualys API returned an error: {response.response_code}"
            )
        has_more = bool(response.has_more)
        return response.asset_list_data.asset, has_more, response.last_seen_asset_id


class AllAssetDetailsORM(GavAPI, QualysORMMixin):
    def __init__(self, echo: bool = False) -> None:
        GavAPI.__init__(self)
        self.orm_base = asset_details_orm.Base  # type: ignore
        QualysORMMixin.__init__(self, self, echo=echo)

    def load(self, **kwargs: Any) -> None:
        def _load_set(to_load: list[asset_details_orm.AssetItem]) -> None:
            with orm.Session(self.engine) as session:
                for obj in to_load:
                    session.merge(obj)
                session.commit()

        kwargs.setdefault("page_size", 300)
        has_more = True

        # This value can be set to a specific asset ID to start from for debugging.
        last_seen_asset_id = None

        while has_more:
            kwargs["last_seen_asset_id"] = last_seen_asset_id
            assets, has_more, last_seen_asset_id = self.all_asset_details(**kwargs)
            to_load = [
                qutils.to_orm_object(asset, asset_details_orm.AssetItem)
                for asset in assets
            ]

            # Useful for debugging
            # print(last_seen_asset_id)

            _load_set(to_load)
