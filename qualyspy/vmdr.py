"""
Qualys VMDR API Module

Typical usage example:
vmdr_orm = vmdr.HostListDetectionORM()
vmdr_orm.load()
session = orm.Session(vmdr_orm.engine):
host_list = session.query(HostORM).all()
stmt = session.query(HostORM)
hosts = vmdr_orm.query(stmt)[0]
host = hosts.host[0]
session.close()
"""

import datetime
import ipaddress
import re
from typing import Any, Literal

import sqlalchemy.orm as orm
from lxml import etree
from lxml.etree import XMLSyntaxError
from psycopg import OperationalError as pgOperationalError
from sqlalchemy.exc import OperationalError as saOperationalError

from . import URLS, qutils
from .base import QualysAPIBase, QualysORMMixin
from .models.vmdr import (
    asset_group_list_output,
    host_list_orm,
    host_list_output,
    host_list_vm_detection_orm,
    host_list_vm_detection_output,
    knowledgebase_orm,
    knowledgebase_output,
    map_report,
    map_report_list,
    scan_list_output,
    simple_return,
)


class VmdrAPI(QualysAPIBase):
    """Qualys VMDR API Class.  Contains methods for interacting with the VMDR API."""

    def host_list(
        self,
        *,
        show_asset_id: bool | None = None,
        details: Literal["Basic", "Basic/AGs", "All", "All/AGs", "None"] | None = None,
        os_pattern: str | None = None,
        truncation_limit: int | None = None,
        ips: (
            list[str | ipaddress.IPv4Address | ipaddress.IPv6Address]
            | str
            | ipaddress.IPv4Address
            | ipaddress.IPv6Address
            | None
        ) = None,
        ag_ids: int | list[int] | None = None,
        ag_titles: str | list[str] | None = None,
        ids: int | list[int] | None = None,
        id_min: int | None = None,
        id_max: int | None = None,
        network_ids: int | list[int] | None = None,
        compliance_enabled: bool | None = None,
        no_vm_scan_since: datetime.datetime | None = None,
        no_compliance_scan_since: datetime.datetime | None = None,
        vm_scan_since: datetime.datetime | None = None,
        compliance_scan_since: datetime.datetime | None = None,
        vm_processed_before: datetime.datetime | None = None,
        vm_processed_after: datetime.datetime | None = None,
        vm_scan_date_before: datetime.datetime | None = None,
        vm_scan_date_after: datetime.datetime | None = None,
        vm_auth_scan_date_before: datetime.datetime | None = None,
        vm_auth_scan_date_after: datetime.datetime | None = None,
        scap_scan_since: datetime.datetime | None = None,
        no_scap_scan_since: datetime.datetime | None = None,
        use_tags: bool | None = None,
        tag_set_by: Literal["id", "name"] | None = None,
        tag_include_selector: Literal["any", "all"] | None = None,
        tag_exclude_selector: Literal["any", "all"] | None = None,
        tag_set_include: list[str | int] | None = None,
        tag_set_exclude: list[str | int] | None = None,
        show_tags: bool | None = None,
        show_trurisk: bool | None = None,
        trurisk_min: int | None = None,
        trurisk_max: int | None = None,
        show_trurisk_factors: bool | None = None,
    ) -> tuple[list[host_list_output.Host], bool, int]:
        """Get a list of hosts from the VMDR API.  A value of None for the parameters will use their
            default values in the API.

        Args:
            ids (int | list[int] | None, optional): Host IDs to query. Defaults to None.

        Returns:
            tuple[host_list_vm_detection_output.HostList, bool, int]: A tuple containing the
                host_list_vm_detection_output.HostList object, a boolean indicating whether the
                results were truncated, and the next id_min to use for the next call.
        """

        if ips is not None:
            if not isinstance(ips, list):
                ips = [ips]
            ipv4_ips: (
                list[str | ipaddress.IPv4Address | ipaddress.IPv6Address] | None
            ) = [
                ip
                for ip in ips
                if isinstance(ip, ipaddress.IPv4Address)
                or isinstance(ipaddress.ip_address(ip), ipaddress.IPv4Address)
            ]
            ipv6_ips: (
                list[str | ipaddress.IPv4Address | ipaddress.IPv6Address] | None
            ) = [
                ip
                for ip in ips
                if isinstance(ip, ipaddress.IPv6Address)
                or isinstance(ipaddress.ip_address(ip), ipaddress.IPv6Address)
            ]

            if not ipv4_ips:
                ipv4_ips = None
            if not ipv6_ips:
                ipv6_ips = None
        else:
            ipv4_ips = None
            ipv6_ips = None

        # Cannot pass both IPv4 and IPv6 addresses in the same call.
        if ipv4_ips and ipv6_ips:
            raise ValueError(
                "Cannot pass both IPv4 and IPv6 addresses in the same call."
            )

        params: dict[str, Any] = {
            "show_asset_id": show_asset_id,
            "details": details,
            "os_pattern": os_pattern,
            "truncation_limit": truncation_limit,
            "ips": ipv4_ips,
            "ipv6": ipv6_ips,
            "ag_ids": ag_ids,
            "ag_titles": ag_titles,
            "ids": ids,
            "id_min": id_min,
            "id_max": id_max,
            "network_ids": network_ids,
            "compliance_enabled": compliance_enabled,
            "no_vm_scan_since": no_vm_scan_since,
            "no_compliance_scan_since": no_compliance_scan_since,
            "vm_scan_since": vm_scan_since,
            "compliance_scan_since": compliance_scan_since,
            "vm_processed_before": vm_processed_before,
            "vm_processed_after": vm_processed_after,
            "vm_scan_date_before": vm_scan_date_before,
            "vm_scan_date_after": vm_scan_date_after,
            "vm_auth_scan_date_before": vm_auth_scan_date_before,
            "vm_auth_scan_date_after": vm_auth_scan_date_after,
            "scap_scan_since": scap_scan_since,
            "no_scap_scan_since": no_scap_scan_since,
            "use_tags": use_tags,
            "tag_set_by": tag_set_by,
            "tag_include_selector": tag_include_selector,
            "tag_exclude_selector": tag_exclude_selector,
            "tag_set_include": tag_set_include,
            "tag_set_exclude": tag_set_exclude,
            "show_tags": show_tags,
            "show_trurisk": show_trurisk,
            "trurisk_min": trurisk_min,
            "trurisk_max": trurisk_max,
            "show_trurisk_factors": show_trurisk_factors,
        }
        params["action"] = "list"
        params_cleaned = qutils.clean_dict(params)

        raw_response = self.get(URLS.host_list, params=params_cleaned).text
        match = re.search(
            r"<HOST_LIST_OUTPUT>.*?</HOST_LIST_OUTPUT>", raw_response, re.DOTALL
        )
        if match is None:
            raise ValueError("Cannot find HOST_LIST_OUTPUT in response.")
        host_list_output_str = match.group(0)
        host_list_output_obj = host_list_output.HostListOutput.from_xml(
            host_list_output_str
        )
        if host_list_output_obj.response.host_list is None:
            raise ValueError("Response has no host_list")

        host_list = host_list_output_obj.response.host_list
        warning = host_list_output_obj.response.warning
        if warning is None:
            return host_list, False, 0
        next_id_match = re.search(r"id_min=(\d+)", warning.url)
        if next_id_match is None:
            raise ValueError(
                "Unable to parse URL in warning message. No id_min found.\n"
                f"{warning.url}"
            )
        truncated = True
        next_id_min = int(next_id_match.group(1))

        return host_list, truncated, next_id_min

    def host_list_vm_detection(
        self,
        *,
        ids: int | list[int] | None = None,
        truncation_limit: int | None = None,
        id_min: int | None = None,
        qids: int | list[int] | None = None,
        show_qds: bool | None = None,
        qds_min: int | None = None,
        qds_max: int | None = None,
        arf_kernel_filter: int | None = None,
        show_igs: bool | None = None,
    ) -> tuple[list[host_list_vm_detection_output.Host], bool, int]:
        """Get a list of hosts with associated vulnerability detections from the VMDR API.  A
        value of None for the parameters will use their default values in the API.

            Args:
                ids (int | list[int] | None, optional): Host IDs to query. Defaults to None.
                truncation_limit (int | None, optional): Maximum number of hosts to return. Defaults
                     to None.
                id_min (int | None, optional): Minimum host list ID to return. Defaults to None.

            Returns:
                tuple[host_list_vm_detection_output.HostList, bool, int]: A tuple containing the
                    host_list_vm_detection_output.HostList object, a boolean indicating whether the
                    results were truncated, and the next id_min to use for the next call.
        """

        params = {
            "ids": ids,
            "truncation_limit": truncation_limit,
            "id_min": id_min,
            "qids": qids,
            "show_qds": show_qds,
            "qds_min": qds_min,
            "qds_max": qds_max,
            "arf_kernel_filter": arf_kernel_filter,
            "show_igs": show_igs,
        }
        cleaned_params = qutils.clean_dict(params)
        cleaned_params["action"] = "list"

        # Detections results can be quite large, so we need to set the parser to allow for large
        # trees.
        parser = etree.XMLParser(huge_tree=True)

        raw_response = self.get(URLS.host_list_vm_detection, params=cleaned_params).text
        match = re.search(
            r"<HOST_LIST_VM_DETECTION_OUTPUT>.*?</HOST_LIST_VM_DETECTION_OUTPUT>",
            raw_response,
            re.DOTALL,
        )
        if match is None:
            raise ValueError("Cannot find HOST_LIST_VM_DETECTION_OUTPUT in response.")
        host_list_vm_detection_output_str = match.group(0)
        host_list_vm_detection_output_obj = (
            host_list_vm_detection_output.HostListVMDetectionOutput.from_xml(
                host_list_vm_detection_output_str, parser=parser
            )
        )
        if host_list_vm_detection_output_obj.response.host_list is None:
            raise ValueError("Response has no host_list")

        host_list = host_list_vm_detection_output_obj.response.host_list
        warning = host_list_vm_detection_output_obj.response.warning
        if warning is None:
            return host_list, False, 0
        next_id_match = re.search(r"id_min=(\d+)", warning.url)
        if next_id_match is None:
            raise ValueError(
                "Unable to parse URL in warning message. No id_min found.\n"
                f"{warning.url}"
            )
        truncated = True
        next_id_min = int(next_id_match.group(1))

        return host_list, truncated, next_id_min

    def knowledgebase(
        self,
        *,
        details: str | None = None,
        ids: int | list[int] | None = None,
        id_min: int | None = None,
        id_max: int | None = None,
    ) -> list[knowledgebase_output.Vuln]:
        """Get a list of vulnerabilities from the VMDR API.  A value of None for the parameters
        will use their default values in the API.

            Args:
                details (str | None, optional): Details to return. Defaults to None.
                ids (int | list[int] | None, optional): Vulnerability IDs to query. Defaults to
                  None.

            Returns:
                knowledge_base_vuln_list_output.VulnList: A VulnList object containing the list of
                    vulnerabilities.
        """
        params = {"details": details, "ids": ids, "id_min": id_min, "id_max": id_max}
        params["action"] = "list"
        params_cleaned = qutils.clean_dict(params)

        raw_response = self.get(URLS.knowledgebase, params=params_cleaned).text
        match = re.search(
            r"<KNOWLEDGE_BASE_VULN_LIST_OUTPUT>.*?</KNOWLEDGE_BASE_VULN_LIST_OUTPUT>",
            raw_response,
            re.DOTALL,
        )
        if match is None:
            raise ValueError("Cannot find KNOWLEDGE_BASE_VULN_LIST_OUTPUT in response.")
        knowledge_base_output_str = match.group(0)
        try:
            knowledge_base_output_obj = (
                knowledgebase_output.KnowledgeBaseOutput.from_xml(
                    knowledge_base_output_str
                )
            )
        except XMLSyntaxError as e:
            self.log.error(
                f"Error parsing XML response: {e}\nResponse:\n{raw_response}"
            )
            raise

        return knowledge_base_output_obj.response.vuln_list

    def launch_vm_scan(
        self,
        *,
        scan_title: str | None = None,
        iscanner_name: str | None = None,
        option_title: str | None = None,
        fqdn: str | list[str] | None = None,
    ) -> simple_return.SimpleReturn:
        params = {
            "scan_title": scan_title,
            "iscanner_name": iscanner_name,
            "option_title": option_title,
            "fqdn": fqdn,
        }
        params["action"] = "launch"
        params_cleaned = qutils.clean_dict(params)

        raw_response = self.post(
            URLS.launch_vm_scan, params=params_cleaned
        ).text.encode("utf-8")
        launch_vm_scan_output_obj = simple_return.SimpleReturn.from_xml(raw_response)

        if launch_vm_scan_output_obj.response.text != "New vm scan launched":
            raise ValueError(
                f"Failed to launch VM scan.  Response: {launch_vm_scan_output_obj.response.text}"
            )

        return launch_vm_scan_output_obj

    def vm_scan_list(
        self, *, scan_ref: str | None = None
    ) -> scan_list_output.ScanListOutput:
        params = {"scan_ref": scan_ref}
        params["action"] = "list"
        params_cleaned = qutils.clean_dict(params)

        raw_response = self.get(URLS.vm_scan_list, params=params_cleaned).text.encode(
            "utf-8"
        )
        vm_scan_list_output_obj = scan_list_output.ScanListOutput.from_xml(raw_response)

        return vm_scan_list_output_obj

    def map_report_list(
        self, *, last: bool | None = None, domain: str | None = None
    ) -> map_report_list.MapReportList:
        params = {"domain": domain}
        if last:
            params["last"] = "yes"
        params_cleaned = qutils.clean_dict(params)

        raw_response = self.get(
            URLS.map_report_list, params=params_cleaned
        ).text.encode("utf-8")
        map_report_list_output_obj = map_report_list.MapReportList.from_xml(
            raw_response
        )

        return map_report_list_output_obj

    def download_saved_map_report(self, *, ref: str | None) -> map_report.Map:
        params = {"ref": ref}
        params_cleaned = qutils.clean_dict(params)

        raw_response = self.get(
            URLS.download_saved_map_report, params=params_cleaned
        ).text.encode("utf-8")
        map_report_output_obj = map_report.Map.from_xml(raw_response)

        return map_report_output_obj

    def asset_group_list(self) -> list[asset_group_list_output.AssetGroup]:
        params = {"action": "list"}
        params_cleaned = qutils.clean_dict(params)

        raw_response = self.get(URLS.asset_group, params=params_cleaned).text.encode(
            "utf-8"
        )
        asset_group_list_output_obj = (
            asset_group_list_output.AssetGroupListOutput.from_xml(raw_response)
        )
        if asset_group_list_output_obj.response.asset_group_list is None:
            raise ValueError("Response has no asset_group_list")

        return asset_group_list_output_obj.response.asset_group_list

    def edit_asset_group(
        self,
        *,
        id: int,
        set_ips: list[str | ipaddress.IPv4Address | ipaddress.IPv4Network]
        | None = None,
    ) -> simple_return.SimpleReturn:
        params = {"action": "edit"}
        data = {"id": str(id)}
        if set_ips is not None:
            ips_str = ",".join([str(ip) for ip in set_ips])
            data["set_ips"] = ips_str

        raw_response = self.post(
            URLS.asset_group,
            params=params,
            data=data,
            content_type="application/x-www-form-urlencoded",
        ).text.encode("utf-8")
        edit_asset_group_output_obj = simple_return.SimpleReturn.from_xml(raw_response)

        if (
            edit_asset_group_output_obj.response.text
            != "Asset Group Updated Successfully"
        ):
            raise ValueError(
                f"Failed to edit asset group.  Response: {edit_asset_group_output_obj.response.text}"
            )
        return edit_asset_group_output_obj


class HostListORM(VmdrAPI, QualysORMMixin):
    """Qualys VMDR Host List ORM Class.  Contains methods for loading hosts into an ORM database."""

    def __init__(self, echo: bool = False) -> None:
        """Initialize the Host List ORM Class.

        Args:
            echo (bool, optional): Whether to echo SQL statements. Defaults to False.
        """
        VmdrAPI.__init__(self)
        self.orm_base = host_list_orm.Base  # type: ignore
        QualysORMMixin.__init__(self, self, echo=echo)

    def load(self, **kwargs: Any) -> None:
        """Load hosts into the ORM database.

        Args:
            load_func (Any): Function to call to get hosts.
            **kwargs (Any): Keyword arguments to pass to host_list.
        """

        def load_set(to_load: list[host_list_orm.Host]) -> None:
            """Load a single set of hosts into the ORM database.

            Args:
                to_load (list[host_list_orm.Host]): List of hosts to load.
            """
            with orm.Session(self.engine) as session:
                session.add_all(to_load)
                for obj in to_load:
                    session.merge(obj)
                session.commit()

        kwargs.setdefault("truncation_limit", 10000)
        truncated = True
        next_id_min = None
        while truncated:
            kwargs["id_min"] = next_id_min
            hosts, truncated, next_id_min = self.host_list(**kwargs)
            to_load = [qutils.to_orm_object(host, host_list_orm.Host) for host in hosts]
            load_set(to_load)


class HostListVMDetectionORM(VmdrAPI, QualysORMMixin):
    """Qualys VMDR Host List Detection ORM Class.  Contains methods for loading host
    detections into an ORM database.
    """

    def __init__(self, echo: bool = False) -> None:
        """Initialize the Host List Detection ORM Class.

        Args:
            echo (bool, optional): Whether to echo SQL statements. Defaults to False.
        """
        VmdrAPI.__init__(self)
        self.orm_base = host_list_vm_detection_orm.Base  # type: ignore
        QualysORMMixin.__init__(self, self, echo=echo)

    def load(self, **kwargs: Any) -> None:
        """Load hosts into the ORM database.

        Args:
            load_func (Any): Function to call to get hosts.
            **kwargs (Any): Keyword arguments to pass to host_list_vm_detection.
        """

        def load_set(to_load: list[host_list_vm_detection_orm.Host]) -> None:
            """Load a single set of hosts into the ORM database.

            Args:
                to_load (list[host_list_vm_detection_orm.Host]): List of hosts to load.
            """
            with orm.Session(self.engine) as session:
                session.add_all(to_load)
                # for obj in to_load:
                #     session.merge(obj)
                session.commit()

        kwargs.setdefault("truncation_limit", 1000)
        truncated = True
        next_id_min = None
        while truncated:
            kwargs["id_min"] = next_id_min
            success = False
            # Attempt to fetch hosts, halving the truncation limit on errors
            # which typically means the system ran out of memory, presumably due to the size
            # of the input.
            while not success:
                try:
                    hosts, truncated, next_id_min = self.host_list_vm_detection(
                        **kwargs
                    )
                    to_load = qutils.to_orm_objects(
                        hosts, host_list_vm_detection_orm.Host
                    )
                    load_set(to_load)
                    success = True
                except (
                    XMLSyntaxError,
                    OverflowError,
                    pgOperationalError,
                    saOperationalError,
                ):
                    if kwargs["truncation_limit"] > 1:
                        kwargs["truncation_limit"] //= 2
                    else:
                        raise
            kwargs["truncation_limit"] = 1000
            # to_load = [
            #     qutils.to_orm_object(host, host_list_vm_detection_orm.Host)
            #     for host in hosts
            # ]


class KnowledgebaseORM(VmdrAPI, QualysORMMixin):
    def __init__(self, echo: bool = False) -> None:
        VmdrAPI.__init__(self)
        self.orm_base = knowledgebase_orm.Base  # type: ignore
        QualysORMMixin.__init__(self, self, echo=echo)

    def load(self, **kwargs: Any) -> None:
        MAX_QID = 10000000
        NUM_PER_CALL = 50000
        for id_min in range(1, MAX_QID, NUM_PER_CALL):
            kwargs["id_min"] = id_min
            kwargs["id_max"] = id_min + (NUM_PER_CALL - 1)
            vulns = self.knowledgebase(**kwargs)
            to_load = qutils.to_orm_objects(vulns, knowledgebase_orm.Vuln)
            with orm.Session(self.engine) as session:
                for item in to_load:
                    session.merge(item)
                session.commit()
