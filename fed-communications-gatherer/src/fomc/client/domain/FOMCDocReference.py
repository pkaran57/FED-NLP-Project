from datetime import date
from typing import List
from urllib.parse import urljoin
from urllib.request import urlopen

from bs4 import BeautifulSoup
from pydantic import Field
from pydantic.main import BaseModel

from src.definitions import FOMC_HOST_BASE_URL
from src.fomc.FOMCDoc import FOMCDoc
from src.fomc.client.domain.FOMCDocType import FOMCDocType
from src.fomc.client.domain.FOMCFileReference import FOMCFileReference


class FOMCDocReference(BaseModel):
    meeting_date: date = Field(..., alias="d")
    document_date: str = Field(None, alias="dt")
    type: str
    url: str = None
    files: List[FOMCFileReference] = None

    def get_html_doc_url(self):
        if self.files:
            html_doc_refs = [
                ref
                for ref in self.files
                if ref.url.endswith(".htm") or ref.url.endswith(".html")
            ]
            if len(html_doc_refs) > 0:
                return html_doc_refs[0].get_full_url()
        else:
            if self.url:
                return urljoin(FOMC_HOST_BASE_URL, self.url)

        raise Exception("Unable to find link to HTML doc for {}".format(self))

    def get_fomc_Doc(self) -> FOMCDoc:
        html = urlopen(self.get_html_doc_url())
        soup = BeautifulSoup(html, "lxml")

        return FOMCDoc(
            meeting_date=self.meeting_date,
            paragraphs=self._get_paragraphs(soup),
            doc_type=self.type,
        )

    def _get_paragraphs(self, soup) -> List[str]:
        if self.type == FOMCDocType.POLICY_STATEMENTS.value:
            statement_div = soup.find("div", {"class": "col-xs-12 col-sm-8 col-md-8"})
            if statement_div:
                paragraphs = statement_div.find_all("p")
            else:
                paragraphs = soup.find_all("p")
            return [paragraph.text for paragraph in paragraphs if paragraph.text and paragraph.text.strip()]
        else:
            raise NotImplementedError(
                "Method not implemented for doc type - " + self.type
            )
