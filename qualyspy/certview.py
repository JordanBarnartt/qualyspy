import dataclasses
from typing import Any

from . import URLS
from .base import QualysAPIBase
from .models.certview import instances_output


@dataclasses.dataclass
class Filter:
    field: str
    value: str
    operator: str

    def to_dict(self) -> dict[str, Any]:
        """Convert the filter to a dictionary.

        Returns:
            dict[str, Any]: A dictionary representation of the filter.
        """
        return dataclasses.asdict(self)


@dataclasses.dataclass
class FilterRequest:
    filters: list[Filter]
    operation: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert the filter request to a dictionary.

        Returns:
            dict[str, Any]: A dictionary representation of the filter request.
        """

        if len(self.filters) > 1 and self.operation is None:
            raise ValueError(
                "Operation must be specified when multiple filters are provided."
            )
        ret: dict[str, Any] = {
            "filters": [filter_.to_dict() for filter_ in self.filters]
        }
        if self.operation is not None:
            ret["operation"] = self.operation
        return ret


class CertViewAPI(QualysAPIBase):
    """Qualys CertView API Class.  Contains methods for interacting with the CertView API."""

    def list_instances(
        self,
        *,
        filter_request: FilterRequest | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> list[instances_output.Instance]:
        """List instances in CertView.

        Args:
            filter (Filter | None): Optional filter to apply to the list of instances.
            page_number (int | None): Optional page number for pagination.
            page_size (int | None): Optional page size for pagination.

        Returns:
            list[instances_output.Instance]: A list of instances in CertView.
        """

        data: dict[str, str | dict[str, Any]] = {}
        if filter_request is not None:
            data["filterRequest"] = filter_request.to_dict()
        if page_number is not None:
            data["pageNumber"] = str(page_number)
        if page_size is not None:
            data["pageSize"] = str(page_size)

        response = self.post(
            URLS.list_instances,
            json=data,
            content_type="application/json",
            accept="application/json",
        )
        response.raise_for_status()
        response_json = response.json()
        instances = [
            instances_output.Instance(**instance) for instance in response_json
        ]
        return instances

    def add_bulk_external_sites(self, *, sites: list[str]) -> None:
        """Add a list of external sites to CertView.

        Args:
            sites (list[str]): A list of external sites to add to CertView.
        """

        # A single CSV file can contain up to 1000 records, so add in batches of 1000
        for i in range(0, len(sites), 1000):
            sites_batch = sites[i : i + 1000]
            csv_string = "Sites\n" + "\n".join(sites_batch) + "\n"
            files = {"file": ("sites.csv", csv_string, "text/csv")}

            self.post(
                URLS.add_bulk_external_sites,
                params={"action": "SAVE_AND_LAUNCH"},
                files=files,
                # The content type is set automatically by requests based on the file type
                content_type=None,
                accept="application/json",
            )
