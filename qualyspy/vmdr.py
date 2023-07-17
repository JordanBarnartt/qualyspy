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

import os
import re
from typing import Any
import zoneinfo

import sqlalchemy.orm as orm
from xsdata.formats.dataclass.parsers import XmlParser

from . import URLS, qutils
from .base import QualysAPIBase, QualysORMMixin
from .models.vmdr import (
    host_list_vm_detection_orm,
    host_list_vm_detection_output,
    knowledge_base_vuln_list_output,
)
from .models.vmdr import host_list_output, host_list_orm


class VmdrAPI(QualysAPIBase):
    """Qualys VMDR API Class.  Contains methods for interacting with the VMDR API."""

    def __init__(
        self,
        config_file: str = str(os.path.join(os.path.expanduser("~"), ".qualyspy")),
        x_requested_with: str = "QualysPy Python Library",
    ) -> None:
        """Initialize the VMDR API Class.

        Args:
            config_file (str, optional): Path to config file. Defaults to ~/etc/qualysby/config.ini.
            x_requested_with (str, optional): Value for X-Requested-With header. Defaults to
                "QualysPy Python Library".
        """
        super().__init__(config_file, x_requested_with)
        self.xmlparser = XmlParser()

    def host_list_detection(
        self,
        *,
        ids: int | list[int] | None = None,
        truncation_limit: int | None = None,
        id_min: int | None = None,
        qids: int | list[int] | None = None,
        show_qds: bool | None = None,
        qds_min: int | None = None,
        qds_max: int | None = None,
    ) -> tuple[host_list_vm_detection_output.HostList, bool, int]:
        """Get a list of hosts with associated vulnerability detections from the VMDR API.  A value
        of None for the parameters will use their default values in the API.

        Args:
            ids (int | list[int] | None, optional): Host IDs to query. Defaults to None.
            truncation_limit (int | None, optional): Maximum number of hosts to return. Defaults to
                None.
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
        }
        cleaned_params = qutils.clean_dict(params)
        cleaned_params["action"] = "list"

        truncated = False
        next_id_min = 0

        response = self.get(URLS.host_list_detection, params=cleaned_params).text
        parsed: host_list_vm_detection_output.HostListVmDetectionOutput = (
            self.xmlparser.from_string(
                response, host_list_vm_detection_output.HostListVmDetectionOutput
            )
        )
        if parsed.response is None:
            raise ValueError("API call returned no response.")
        ret = parsed.response.host_list
        if ret is None:
            raise ValueError("API call returned no host_list.")
        if (
            parsed.response.warning is not None
            and parsed.response.warning.url is not None
        ):
            next_id_match = re.search(r"id_min=(\d+)", parsed.response.warning.url)
            if next_id_match is None:
                raise ValueError(
                    "Unable to parse URL in warning message. No id_min found.\n"
                    f"{parsed.response.warning}"
                )
            truncated = True
            next_id_min = int(next_id_match.group(1))

        return ret, truncated, next_id_min

    def host_list(
        self,
        *,
        ids: int | list[int] | None = None,
        truncation_limit: int | None = None,
        id_min: int | None = None,
    ) -> tuple[host_list_output.HostList, bool, int]:
        """Get a list of hosts from the VMDR API.  A value of None for the parameters will use their
            default values in the API.

        Args:
            ids (int | list[int] | None, optional): Host IDs to query. Defaults to None.

        Returns:
            tuple[host_list_vm_detection_output.HostList, bool, int]: A tuple containing the
                host_list_vm_detection_output.HostList object, a boolean indicating whether the
                results were truncated, and the next id_min to use for the next call.
        """

        params = {
            k: str(v) for k, v in locals().items() if (k != "self" and v is not None)
        }
        params["action"] = "list"

        truncated = False
        next_id_min = 0

        response = self.get(URLS.host_list, params=params).text
        parsed: host_list_output.HostListOutput = self.xmlparser.from_string(
            response, host_list_output.HostListOutput
        )
        if parsed.response is None:
            raise ValueError("API call returned no response.")
        ret = parsed.response.host_list
        if ret is None:
            raise ValueError("API call returned no host_list.")
        if (
            parsed.response.warning is not None
            and parsed.response.warning.url is not None
        ):
            next_id_match = re.search(r"id_min=(\d+)", parsed.response.warning.url)
            if next_id_match is None:
                raise ValueError(
                    "Unable to parse URL in warning message. No id_min found.\n"
                    f"{parsed.response.warning}"
                )
            truncated = True
            next_id_min = int(next_id_match.group(1))

        return ret, truncated, next_id_min

    def knowledgebase(
        self, *, details: str | None = None, ids: int | list[int] | None = None
    ) -> knowledge_base_vuln_list_output.VulnList:
        params = {"details": details, "ids": ids}
        params["action"] = "list"
        params_cleaned = qutils.clean_dict(params)

        raw_response = self.get(URLS.knowledgebase, params=params_cleaned).text
        parsed: knowledge_base_vuln_list_output.KnowledgeBaseVulnListOutput = (
            self.xmlparser.from_string(
                raw_response,
                knowledge_base_vuln_list_output.KnowledgeBaseVulnListOutput,
            )
        )
        if parsed.response is not None and parsed.response.vuln_list is not None:
            for vuln in parsed.response.vuln_list.vuln:
                if vuln.published_datetime is not None:
                    vuln.published_datetime = vuln.published_datetime.replace(
                        tzinfo=zoneinfo.ZoneInfo("UTC")
                    )
            return parsed.response.vuln_list
        else:
            return knowledge_base_vuln_list_output.VulnList()


class HostListDetectionORM(VmdrAPI, QualysORMMixin):
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

    def _load(self, load_func: Any, **kwargs: Any) -> None:
        """Load host detections into the ORM database.

        Args:
            load_func (Any): Function to call to get host detections.
            **kwargs (Any): Keyword arguments to pass to load_func.
        """

        def load_set(to_load: list[host_list_vm_detection_orm.Host]) -> None:
            """Load a single set of host detections into the ORM database.

            Args:
                to_load (list[host_list_vm_detection_orm.Host]): List of host list detections to
                    load.
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
            to_load, truncated, next_id_min = load_func(**kwargs)
            to_load = [
                qutils.to_orm_object(obj, host_list_vm_detection_orm.Host)
                for obj in to_load.host
            ]
            load_set(to_load)

    def load(self, **kwargs: Any) -> None:
        """Load host detections into the ORM database.

        Args:
            **kwargs (Any): Keyword arguments to pass to VmdrAPI.host_list_detection().
        """

        self.safe_load(self._load, self.host_list_detection, **kwargs)


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

    def _load(self, load_func: Any, **kwargs: Any) -> None:
        """Load hosts into the ORM database.

        Args:
            load_func (Any): Function to call to get hosts.
            **kwargs (Any): Keyword arguments to pass to load_func.
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
            to_load, truncated, next_id_min = load_func(**kwargs)
            to_load = [
                qutils.to_orm_object(obj, host_list_orm.Host) for obj in to_load.host
            ]
            load_set(to_load)

    def load(self, **kwargs: Any) -> None:
        """Load hosts into the ORM database.

        Args:
            **kwargs (Any): Keyword arguments to pass to VmdrAPI.host_list().
        """

        self.safe_load(self._load, self.host_list, **kwargs)
