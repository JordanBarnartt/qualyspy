from . import URLS
from .base import QualysAPIBase


class CertViewAPI(QualysAPIBase):
    """Qualys CertView API Class.  Contains methods for interacting with the CertView API."""

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
