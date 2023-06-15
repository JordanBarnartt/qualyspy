import os
import re
from typing import Any

import sqlalchemy.orm as orm
from xsdata.formats.dataclass.parsers import XmlParser

from . import URLS, qutils
from .base import QualysAPIBase, QualysORMMixin
from .models.vmdr import host_list_vm_detection_orm
from .models.vmdr import host_list_vm_detection_output


class VmdrAPI(QualysAPIBase):
    def __init__(
        self,
        config_file: str = str(
            os.path.join(os.path.expanduser("~"), "etc", "qualyspy", "config.ini")
        ),
        x_requested_with: str = "QualysPy Python Library",
    ) -> None:
        super().__init__(config_file, x_requested_with)
        self.xmlparser = XmlParser()

    def host_list_detection(
        self,
        *,
        ids: int | list[int] | None = None,
        truncation_limit: int | None = None,
        id_min: int | None = None,
    ) -> tuple[host_list_vm_detection_output.HostList, bool, int]:
        params = {
            k: str(v) for k, v in locals().items() if (k != "self" and v is not None)
        }
        params["action"] = "list"

        truncated = False
        next_id_min = 0

        response = self.get(URLS.host_list_detection, params=params)
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
            print(parsed.response.warning)
            truncated = True
            next_id_min = int(next_id_match.group(1))
        return ret, truncated, next_id_min


class HostListDetectionORM(VmdrAPI, QualysORMMixin):
    def __init__(self, echo: bool = False) -> None:
        VmdrAPI.__init__(self)
        self.orm_base = host_list_vm_detection_orm.Base  # type: ignore
        QualysORMMixin.__init__(self, self, echo=echo)

    def _load(self, load_func: Any, **kwargs: Any) -> None:
        def load_set(to_load: list[host_list_vm_detection_orm.Host]) -> None:
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
        self.safe_load(self._load, self.host_list_detection, **kwargs)
