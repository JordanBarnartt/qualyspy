from . import URLS, qutils
from .base import QualysAPIBase
from .models.gav import asset_details_output
from .exceptions import QualysAPIError


class GavAPI(QualysAPIBase):
    """Qualys VMDR API Class.  Contains methods for interacting with the VMDR API."""

    def _convert_ipaddress(self, ips: str) -> list[str]:
        """Converts a string of IPs into a list of IP strings, for easier validation in
        Pydantic.
        """
        if ips is None:
            return None
        elif "," in ips:
            return ips.split(", ")
        return [ips]

    def asset_details(self, *, asset_id: int) -> asset_details_output.AssetItem:
        params = {"assetID": asset_id}
        params_cleaned = qutils.clean_dict(params)

        raw_response = self.get(URLS.asset_details, params=params_cleaned).json()
        for interface in raw_response["assetListData"]["asset"][0][
            "networkInterfaceListData"
        ]["networkInterface"]:
            interface["addressIpV4"] = self._convert_ipaddress(interface["addressIpV4"])
            interface["addressIpV6"] = self._convert_ipaddress(interface["addressIpV6"])
        response = asset_details_output.AssetDetailsOutput(**raw_response)
        return response.asset_list_data.asset[0]

    def all_asset_details(
        self, *, last_seen_asset_id: int | None = None, page_size: int | None = None
    ) -> tuple[list[asset_details_output.AssetItem], bool, int | None]:
        data = {"lastSeenAssetID": last_seen_asset_id, "pageSize": page_size}
        data["lastSeenAssetID"] = last_seen_asset_id
        data_cleaned = qutils.clean_dict(data)
        raw_response = self.post(URLS.all_asset_details, data=data_cleaned).json()
        for asset in raw_response["assetListData"]["asset"]:
            for interface in asset["networkInterfaceListData"]["networkInterface"]:
                interface["addressIpV4"] = self._convert_ipaddress(
                    interface["addressIpV4"]
                )
                interface["addressIpV6"] = self._convert_ipaddress(
                    interface["addressIpV6"]
                )
        response = asset_details_output.AssetDetailsOutput(**raw_response)

        if response.response_code != "SUCCESS":
            raise QualysAPIError(
                f"Qualys API returned an error: {response.response_code}"
            )
        has_more = bool(response.has_more)
        return response.asset_list_data.asset, has_more, response.last_seen_asset_id
