from urllib.parse import urljoin

from pydantic import Field
from pydantic.main import BaseModel

from definitions import FOMC_HOST_BASE_URL


class FOMCFileReference(BaseModel):
    format: str = Field(None, alias='name')
    url: str

    def get_full_url(self):
        return urljoin(FOMC_HOST_BASE_URL + '/', self.url)
