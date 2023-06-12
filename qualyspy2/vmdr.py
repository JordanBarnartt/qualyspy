import os
from typing import Any, Callable


import sqlalchemy.orm as orm
from xsdata.formats.dataclass.parsers import XmlParser

from . import URLS, qutils
from .base import QualysAPIBase, QualysORMMixin
from .models.vmdr.host_list_vm_detection_orm import Base, HostList
from .models.vmdr.host_list_vm_detection_output import HostListVmDetectionOutput


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
        self, *, ids: int | list[int] | None = None
    ) -> HostListVmDetectionOutput:
        params = {
            k: str(v) for k, v in locals().items() if (k != "self" and v is not None)
        }
        params["action"] = "list"
        params["truncation_limit"] = "100"

        response = self.get(URLS.host_list_detection, params=params)
        parsed: HostListVmDetectionOutput = self.xmlparser.from_string(
            response, HostListVmDetectionOutput
        )
        return parsed


class HostListDetectionORM(VmdrAPI, QualysORMMixin):
    def __init__(self, echo: bool = False) -> None:
        VmdrAPI.__init__(self)
        self.orm_base = Base  # type: ignore
        QualysORMMixin.__init__(self, self, echo=echo)

    def _load(self, load_func: Callable[..., Any], **kwargs: dict[str, Any]) -> None:
        to_load = [load_func(**kwargs).response.host_list]
        to_load = [qutils.to_orm_object(obj, HostList) for obj in to_load]
        with orm.Session(self.engine) as session:
            session.add_all(to_load)
            for obj in to_load:
                session.merge(obj)
            session.commit()

    def load(self) -> None:
        self._load(self.host_list_detection)
