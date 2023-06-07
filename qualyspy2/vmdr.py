import os


from xsdata.formats.dataclass.parsers import XmlParser

from . import URLS
from .base import QualysAPIBase
from .models.vmdr.host_list_vm_detection_output import HostListVmDetectionOutput


class VmdrAPI(QualysAPIBase):
    def __init__(
        self,
        config_file: str = str(
            os.path.join(os.path.expanduser("~"), "etc", "qualyspy", "config.ini")
        ),
        x_requested_with: str = "QualysPy Python Library",
    ) -> None:
        self.xmlparser = XmlParser()
        super().__init__(config_file, x_requested_with)

    def host_list_detection(self, *, ids: int | list[int]) -> HostListVmDetectionOutput:
        params = {"action": "list", "ids": str(ids)}
        response = self.get(URLS.host_list_detection, params=params)
        parsed: HostListVmDetectionOutput = self.xmlparser.from_string(
            response, HostListVmDetectionOutput
        )
        return parsed


class VmdrORM:
    pass
